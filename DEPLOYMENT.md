# Ejecución y despliegue

**Estado:** Fase 02 ejecutable localmente. Sin autenticación ni operaciones comerciales reales; contenedores definidos pero no ejecutados en este equipo.

## Empezar en este equipo

El entorno ya está preparado. Hacer doble clic en [Iniciar POINT.cmd](Iniciar%20POINT.cmd) desde la carpeta del proyecto. Inicia solo PostgreSQL propio de POINT, aplica migraciones pendientes y arranca web/API. Abrir [la aplicación](http://127.0.0.1:5173/) y consultar Estado de conexión.

Ctrl+C en la ventana detiene web y API. No elimina datos. Para detener también PostgreSQL propio:

```powershell
.\.venv\Scripts\python.exe infrastructure/scripts/local.py stop
```

No se crean servicios de Windows ni se modifica PostgreSQL de otras aplicaciones.

## Instalación nativa reproducible

Requisitos: Node 24, Python 3.12 y PostgreSQL 18. En esta máquina se comprobaron Node 24.15.0, Python 3.12.14 y PostgreSQL 18.3. Dependencias exactas en `package-lock.json`, `requirements.txt` y `requirements-dev.txt`. Las versiones se consultaron en los registros oficiales; se instaló y probó también un segundo entorno Python desde el archivo fijado.

Desde la raíz del proyecto, con Python disponible:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r apps/api/requirements-dev.txt
npm.cmd ci
.\.venv\Scripts\python.exe infrastructure/scripts/local.py setup
.\.venv\Scripts\python.exe infrastructure/scripts/local.py migrate
.\.venv\Scripts\python.exe infrastructure/scripts/dev.py
```

El asistente crea `.env` con contraseñas aleatorias sin mostrarlas. No sustituye valores existentes. El clúster vive en `.local/postgres/data`, puerto 55432; verifica su ruta antes de crear bases. Usa un administrador local propio y un usuario de aplicación sin superusuario. `point_dev` y `point_test` son independientes.

Si PostgreSQL no está en PATH, se busca su instalación 18 estándar en Windows; también se puede definir `POINT_PG_BIN`. Si el puerto está ocupado, no se altera otro servicio: elegir otro puerto propio y actualizar consistentemente `POSTGRES_PORT` y `POINT_DATABASE_URL`. No usar una base comercial existente para preparar el entorno.

Web: puerto 5173. API: puerto 8000. Solo se escucha en 127.0.0.1. El servidor Vite redirige `/api` y `/health` a la API; no incorpora secretos POINT al código enviado al navegador.

## Configuración

| Variable | Uso |
| --- | --- |
| `POINT_ENVIRONMENT` | development/test/production; documentación técnica desactivada en production |
| `POINT_DATABASE_URL` | Conexión privada PostgreSQL con psycopg |
| `POINT_TEST_DATABASE_URL` | Base aislada obligatoriamente llamada point_test para integración |
| `POINT_APP_NAME` | Nombre público de la instalación |
| `POINT_DEFAULT_LOCALE`, `POINT_DEFAULT_CURRENCY`, `POINT_DEFAULT_TIMEZONE` | Valores iniciales públicos, validados; no sustituyen configuración por tenant |
| `POINT_CORS_ORIGINS` | Lista JSON de orígenes explícitos; HTTPS en producción |
| `POINT_LOG_LEVEL` | Nivel de registros sanitizados |
| `POINT_WEB_PORT`, `POINT_API_PORT` | Puertos de desarrollo; reiniciar tras cambiarlos |
| `POSTGRES_PASSWORD`, `POSTGRES_ADMIN_PASSWORD` | Contraseñas locales generadas; nunca versionar |
| `POSTGRES_PORT` | Puerto PostgreSQL propio en el host |

Cambiar reglas comerciales de un cliente requerirá su configuración autorizada/versionada cuando exista el módulo tenants. No habilitar tasas, comisiones, integraciones ni permisos cambiando solamente el cliente web.

## Migraciones, pruebas y contratos

```powershell
.\.venv\Scripts\python.exe -m alembic -c apps/api/alembic.ini upgrade head
.\.venv\Scripts\python.exe -m alembic -c apps/api/alembic.ini check
.\.venv\Scripts\python.exe -m pytest -c apps/api/pyproject.toml apps/api/tests
.\.venv\Scripts\python.exe infrastructure/scripts/export_openapi.py --check
node infrastructure/scripts/generate-contracts.mjs --check
npm.cmd run build
```

Para actualizar un contrato tras cambiar esquemas, ejecutar los dos generadores sin `--check` y comprobar el cambio. Las pruebas de integración aplican migraciones en `point_test`; rechazan otro nombre de base. El recorrido de reversión se realiza dentro de un esquema temporal, sin borrar datos de la aplicación.

## Respaldar y comprobar recuperación

Con PostgreSQL propio iniciado:

```powershell
.\.venv\Scripts\python.exe infrastructure/scripts/local.py backup
.\.venv\Scripts\python.exe infrastructure/scripts/local.py restore-check --file .local/backups/ARCHIVO.dump
```

El primer comando crea un respaldo nuevo en `.local/backups`, sin sobrescribir uno existente. El segundo crea una base nueva `point_restore_*`, restaura en una transacción y comprueba revisión y tabla. Nunca restaura sobre point_dev. Sustituir ARCHIVO por el nombre real devuelto al respaldar.

Para repetir el ensayo completo con un registro ficticio en bases nuevas independientes:

```powershell
.\.venv\Scripts\python.exe infrastructure/scripts/verify_restore.py
```

El resultado comprobado está en [backup-restore.json](docs/phases/02-base-tecnica/evidence/backup-restore.json). Las bases del ensayo se conservan para revisión. Este procedimiento valida recuperación local; no implementa todavía copias programadas fuera del servidor, cifrado operativo ni los objetivos de RPO/RTO de producción.

## Alternativa Docker Compose · pendiente de ejecución

No se instaló Docker en este equipo ni se afirma haber construido las imágenes. Antes de considerar comprobado este recorrido, ejecutarlo en un equipo con motor Docker y Compose disponibles:

```powershell
python infrastructure/scripts/configure_env.py
docker compose config --quiet
docker compose up --build --wait
docker compose --profile test run --build --rm tests
```

Abrir `http://127.0.0.1:8080/`. PostgreSQL debe estar saludable antes de migrar; la API espera migración completada y la web espera API saludable. Los puertos se publican solo en el equipo. El administrador de PostgreSQL y el usuario de aplicación son distintos; las contraseñas se generan en `.env`.

Usar el modo nativo o Docker, no ambos en los mismos puertos. El volumen Compose y `.local/postgres/data` tienen datos independientes. Detener con `docker compose down` conserva el volumen; no agregar opciones de eliminación de datos.

El [flujo CI](.github/workflows/ci.yml) instala versiones fijadas, verifica contratos, compila web, arranca Compose y ejecuta pruebas. El repositorio ya está compartido en [MrG0N3R/pointcase](https://github.com/MrG0N3R/pointcase); el flujo se activa con push y pull request. Consultar [Actions](https://github.com/MrG0N3R/pointcase/actions) para el resultado de cada commit. La primera ejecución permitió detectar una ruta de pruebas incompatible con `/app`, corregida junto con su prueba de regresión.

## Revisar la Fase 01

Abrir [POINT-Prototipo.html](prototypes/phase-01/POINT-Prototipo.html) en un navegador o hacer doble clic en `prototypes/phase-01/Abrir POINT.cmd` desde la carpeta del proyecto. El archivo único incluye todos sus estilos, ilustraciones y scripts; no requiere instalación ni conexión a proveedores.

Vista previa opcional para desarrollo: `node prototypes/phase-01/serve.mjs`; luego abrir `http://127.0.0.1:4173/`. El servidor entrega solo los archivos de demostración y escucha únicamente en este equipo. Cerrar el proceso al terminar. La apertura directa del archivo único funciona sin ese servidor.

Para recomponer el archivo: `node prototypes/phase-01/build.mjs`. Para comprobar el modelo de demostración: `node --test prototypes/phase-01/model.test.mjs`.

Recorrido, capturas y límites en [la revisión de diseño](docs/phases/01-diseno/REVISION.md).

## Revisar la Fase 00

Abrir [REVISION.md](docs/phases/00-definicion/REVISION.md) y [PLAN_DE_ENTREGAS.md](docs/PLAN_DE_ENTREGAS.md). Todos los documentos son Markdown y pueden leerse desde el editor. No requieren instalar paquetes ni crear cuentas.

## Entorno local · Fase 02

La entrega deberá incluir:

1. Versiones comprobadas de Node, Python, PostgreSQL y dependencias, con archivos de instalación reproducible.
2. Aplicación web y API separadas, estructura modular y configuración mediante variables.
3. `docker-compose.yml` para desarrollo y `.env.example` con valores de ejemplo sin secretos.
4. Migraciones para crear/actualizar el esquema y datos ficticios opcionales identificados como tales.
5. Instrucciones exactas para instalar, arrancar, consultar salud, ejecutar pruebas y detener los servicios.
6. Pruebas de instalación limpia y registro de resultados, con URLs/puertos realmente comprobados.
7. Procedimiento inicial de backup/restore local y tratamiento de fallos.

Documentar en ese momento las variables reales para conexión a base de datos, sesión/orígenes, rutas de archivos, registros y ambiente. Añadir variables PAC, correo, almacenamiento o pagos solamente cuando exista su integración. No crear ni contratar proveedores para completar un ejemplo.

## Piloto · Fases 14–15

Elegir infraestructura, región, presupuesto, comercios participantes, datos y alcance autorizado. Separar desarrollo, pruebas y piloto. Verificar HTTPS, aislamiento, auditoría, recuperación, monitoreo y soporte. Confirmar proveedor fiscal/equipos y pruebas correspondientes cuando sean requisito del piloto.

Probar migración y restauración en ambiente aislado, registrar resultados y objetivos reales de pérdida/recuperación. La meta del maestro RPO ≤ 15 minutos/RTO ≤ 4 horas es una referencia condicionada a la solución aprobada; no se considera alcanzada por escribir este documento.

## Producción · Fase 16

Salida condicionada a piloto revisado, aprobación del lanzamiento y disponibilidad de dominio/infraestructura/configuración. Preparar despliegue reproducible, plan de reversión compatible con migraciones, secretos, copias fuera del host, alertas y responsables de soporte/incidentología.

No se activan cargos POINT ni integraciones de cobro reales por la aprobación de una fase documental o visual. Sus parámetros y activación se revisan con la parte comercial correspondiente.

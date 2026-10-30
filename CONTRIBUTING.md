# Desarrollo en equipo de POINT

Repositorio: [MrG0N3R/pointcase](https://github.com/MrG0N3R/pointcase), rama principal `main`.

## Estado que recibe el equipo

Base local 0.2.0 correspondiente a la Fase 02. Las fases 00 y 01 están aprobadas. La revisión de 02 sigue pendiente, incluida la ejecución de Docker. El código comercial de acceso, empresas, catálogo, inventario y ventas todavía no está implementado.

Leer primero [README.md](README.md), [el plan por fases](docs/PLAN_DE_ENTREGAS.md) y [la entrega 02](docs/phases/02-base-tecnica/REVISION.md). El [hito de cascarón SaaS](docs/HITO_CASCARON_SAAS.md) distingue lo que ya se comparte de lo necesario para personalizar por cliente.

## Primera instalación

```text
git clone https://github.com/MrG0N3R/pointcase.git
cd pointcase
```

Seguir [DEPLOYMENT.md](DEPLOYMENT.md) para crear el entorno Python, instalar las versiones fijadas con pip/npm y preparar PostgreSQL propio. Cada colaborador genera su `.env` y sus bases; esos archivos no viajan en el repositorio. No copiar la carpeta `.local` de otra persona.

Node 24, Python 3.12 y PostgreSQL 18 son la referencia local comprobada. GitHub Actions valida adicionalmente la construcción y ejecución Docker; revisar el resultado del commit correspondiente. `Iniciar POINT.cmd` es un acceso para Windows una vez instaladas las dependencias; en otros sistemas usar los comandos Python de la guía.

## Ramas y revisión de cambios

Propuesta para el equipo: `main` como base compartida; una rama por tarea y revisión mediante pull request. La protección de ramas y los permisos se configuran en GitHub por el propietario; no se consideran activados por esta guía.

```text
git switch main
git pull --ff-only
git switch -c feature/03-modelo-empresas
```

Antes de trabajar, acordar una tarea y sus criterios de aceptación. Conservar el avance por fases solicitado por el propietario. Una tarea terminada o un commit no equivalen a aprobación de la fase. Evitar combinar cambios de varios módulos en una sola entrega difícil de revisar.

La personalización será configuración por empresa/sucursal sobre un producto común: identidad visual, preferencias y capacidades autorizadas. Las decisiones particulares de cada cliente se incorporan progresivamente y quedan documentadas.

## Distribución propuesta para la Fase 03

Este reparto organiza trabajo humano; no declara la fase iniciada ni asigna personas.

| Área | Entrega | Dependencia y prueba |
| --- | --- | --- |
| Modelo SaaS | Empresas, membresías, sucursales, almacenes y configuración inicial; FK real de outbox a empresa | Migraciones compatibles y referencias de la misma empresa |
| Identidad | Registro, sesión, cierre, recuperación y controles de acceso | Contexto autorizado de empresa; sesión revocada deja de funcionar |
| Permisos y auditoría | Roles como plantillas, permisos por acción y alcance; eventos sensibles | Dos empresas/sucursales no acceden a datos ajenos por cambiar IDs |
| Interfaz | Pantallas reales de acceso, alta de negocio, colaboradores y configuración | Integración con contratos de API y estados de error/carga |
| Personalización | Configuración validada por empresa, identidad y capacidades de módulos existentes | Empresas A/B con configuraciones distintas; autorización en servidor |
| Calidad e infraestructura | Pruebas de separación, instalación y mantenimiento de Docker/CI | Evidencia de resultados; registrar lo que siga sin comprobarse |

Coordinar las migraciones y el contrato de API antes de desarrollar en paralelo sus consumidores. Las funcionalidades de catálogo, inventario y ventas conservan sus fases posteriores.

## Reglas para ampliar el código

- Mantener el monolito modular y la separación web/API. Usar servicios de aplicación para operaciones y transacciones.
- Crear migraciones nuevas; `20261028_0001` ya se aplicó en el entorno local. No cambiar retroactivamente su contenido para actualizar una base existente.
- Obtener el contexto de empresa desde una sesión autorizada. Validar también sucursal, almacén y caja. El `tenant_id` de un formulario no concede acceso.
- Integrar el outbox con empresas reales antes de usarlo para comercios; su unicidad actual no demuestra aislamiento completo.
- Usar decimales para dinero y guardar valores históricos. Los ajustes de configuración no deben recalcular operaciones antiguas.
- Derivar permisos/capacidades en el servidor. Ocultar un menú no es un control de acceso.
- Mantener el prototipo 01 identificado como demostración independiente. Las siguientes fases funcionales requieren persistencia, validación y servidor reales.
- Actualizar documentación, variables de ejemplo, pruebas aplicables y CHANGELOG con cada cambio.

## Contratos compartidos

Después de cambiar esquemas de respuesta:

```text
python infrastructure/scripts/export_openapi.py
node infrastructure/scripts/generate-contracts.mjs
```

Versionar juntos OpenAPI, tipos generados y los consumidores afectados. No editar manualmente `packages/shared/src/api.generated.ts`.

## Comprobaciones antes de integrar

Con PostgreSQL de pruebas preparado y el entorno Python activo:

```text
python -m pytest -c apps/api/pyproject.toml apps/api/tests
python infrastructure/scripts/export_openapi.py --check
node infrastructure/scripts/generate-contracts.mjs --check
npm run build
```

Añadir las pruebas relevantes de la tarea, especialmente permisos, separación de empresas, transacciones e idempotencia cuando correspondan. Revisar el resultado de GitHub Actions después de subir; el flujo está definido pero no se debe anunciar como aprobado antes de su ejecución.

No subir `.env`, contraseñas, datos de PostgreSQL, respaldos, entornos Python ni dependencias instaladas. `.env.example` contiene únicamente marcadores y valores públicos de referencia. La verificación local `verify_foundation.py` comprueba el estado preparado en esta máquina; las instrucciones de instalación y las pruebas son la referencia para una clonación nueva.

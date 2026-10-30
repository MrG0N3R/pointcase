# POINT TODO EN UNO

Punto de venta SaaS para pequeñas y medianas empresas en México: ventas, cobros, inventario, caja y administración en una misma plataforma.

## Estado actual

**Fases 00 y 01 aprobadas. Fase 02: base ejecutable lista para revisión, comprobada localmente y con Docker en GitHub Actions.**

Ya funcionan React/TypeScript, FastAPI y PostgreSQL de desarrollo, con migraciones, estado de conexión, contratos compartidos y respaldo/restauración comprobados. El prototipo aprobado se conserva por separado. Registro, empresas, permisos y funcionalidades comerciales comienzan en las siguientes fases; todavía no se realizan ventas reales.

Fuente de requisitos: [documento maestro](POINT_Todo_en_Uno_Prompt_Maestro_PyMEs_Mexico.md). Se conserva como referencia original.

## Desarrollo con colaboradores

Repositorio: [MrG0N3R/pointcase](https://github.com/MrG0N3R/pointcase), rama principal `main`. Leer [CONTRIBUTING.md](CONTRIBUTING.md) para clonar, preparar el entorno y organizar las tareas. El [hito de cascarón SaaS](docs/HITO_CASCARON_SAAS.md) explica lo disponible ahora y lo necesario para personalizar por negocio. Consultar [GitHub Actions](https://github.com/MrG0N3R/pointcase/actions) para el resultado de cada comprobación remota.

La base técnica actual puede compartirse para continuar el desarrollo. El cascarón SaaS personalizable requiere cerrar acceso/empresas/permisos y configuración por empresa en la Fase 03. Un núcleo de POS operativo requiere además las fases 04–07.

## Revisar esta entrega

1. En este equipo, hacer doble clic en [Iniciar POINT.cmd](Iniciar%20POINT.cmd) desde la carpeta del proyecto y abrir [POINT local](http://127.0.0.1:5173/).
2. Entrar a Estado de conexión y consultar los resultados y límites de la [Fase 02](docs/phases/02-base-tecnica/REVISION.md).
3. Revisar esta parte antes de comenzar la Fase 03. Las instrucciones de instalación, inicio, pruebas y recuperación están en [DEPLOYMENT.md](DEPLOYMENT.md).

Docker no está instalado en este equipo. La aplicación se comprobó localmente con PostgreSQL nativo y una instalación Python limpia. La [ejecución de GitHub Actions del 30 de octubre](https://github.com/MrG0N3R/pointcase/actions/runs/41124362283) también aprobó compilación, arranque de contenedores, pruebas y conexión de servicios.

**Forma de trabajo acordada:** desarrollar una parte, entregar evidencia e instrucciones para revisarla y esperar la confirmación del usuario antes de empezar la siguiente. Una entrega preparada no equivale a una entrega aprobada.

## Documentación

| Documento | Contenido |
| --- | --- |
| [Plan de entregas](docs/PLAN_DE_ENTREGAS.md) | Partes, dependencias, demostraciones y avance |
| [Colaboración](CONTRIBUTING.md) | Instalación, ramas, tareas, contratos y revisión de cambios |
| [Hito de cascarón SaaS](docs/HITO_CASCARON_SAAS.md) | Alcance de una base adaptable a distintos negocios |
| [Revisión de la base técnica](docs/phases/02-base-tecnica/REVISION.md) | Ejecución local, pruebas, recuperación y pendientes |
| [Revisión del diseño](docs/phases/01-diseno/REVISION.md) | Prototipo, recorrido, comprobaciones y capturas |
| [Sistema visual](docs/phases/01-diseno/DESIGN_SYSTEM.md) | Colores, tipografía, componentes y adaptación |
| [Estructura de pantallas](docs/phases/01-diseno/WIREFRAMES.md) | Esquemas y recorridos principales |
| [Definición del producto](docs/phases/00-definicion/PRD.md) | Alcance, propuestas, módulos, casos de uso, métricas y riesgos |
| [Requisitos](docs/phases/00-definicion/REQUISITOS.md) | Funcionalidades, calidad y reglas del negocio |
| [Backlog](docs/phases/00-definicion/BACKLOG.md) | Trabajo organizado por fase y criterios de salida |
| [Aceptación](docs/phases/00-definicion/ACEPTACION.md) | Revisión documental y escenarios que deberá cumplir el sistema |
| [Arquitectura](ARCHITECTURE.md) | Propuesta técnica y límites entre módulos |
| [Datos](DATABASE.md) | Modelo inicial de relaciones e integridad |
| [API](API.md) | Contratos actuales de sistema y planificación comercial |
| [Seguridad](SECURITY.md) | Controles y pruebas previstos por etapa |
| [Despliegue](DEPLOYMENT.md) | Requisitos de desarrollo, piloto y producción |
| [Cambios](CHANGELOG.md) | Registro de las entregas |

## Continuidad del trabajo

Antes de retomar, consultar este archivo, el plan de entregas y la revisión de la fase actual. Registrar la aprobación solamente cuando el usuario la exprese. Conservar la numeración 00–16 del documento maestro. Si una parte resulta demasiado grande, proponer subentregas con revisión individual sin omitir su alcance.

La implementación usará datos de prueba. Los importes, impuestos, comisiones, proveedores y credenciales de producción no se consideran autorizados por esta definición.

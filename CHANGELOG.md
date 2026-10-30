# Historial de cambios

## 2026-10-30 · Preparación para desarrollo colaborativo

- Se documentó el hito de cascarón SaaS: base técnica compartible ahora; empresas, acceso, permisos y configuración por negocio pendientes de Fase 03.
- Se añadió guía para colaboradores con instalación, propuesta de reparto de tareas, ramas, contratos y criterios de revisión.
- Se añadió plantilla de pull request y se fijó la conservación del archivo maestro sin conversión de saltos de línea.
- Se identificó `MrG0N3R/pointcase` como destino indicado por el usuario. Esta preparación no aprueba la Fase 02 ni inicia la 03.

## 2026-10-28 · 0.2.0 · Fase 02 lista para revisión local

- Diseño 01 aprobado por el usuario; los parámetros por cliente se ajustarán progresivamente.
- Repositorio Git local, aplicación React/TypeScript/Vite, API FastAPI modular y contratos TypeScript generados desde OpenAPI.
- PostgreSQL propio separado del instalado para otras aplicaciones, primera migración Alembic y outbox interno transaccional.
- Configuración validada, secretos locales aleatorios ignorados por Git, usuario de aplicación sin superusuario, request IDs, errores uniformes y registros sanitizados.
- Estado de conexión real en la web con carga, error, reintento y detección de migraciones pendientes.
- Asistente de arranque local, dependencias fijadas, 16 pruebas aprobadas tras instalación Python limpia y recuperación comprobada de un dato ficticio en una base nueva.
- Diseño aprobado conservado como demostración separada; sin operaciones comerciales simuladas en la base real.
- Dockerfiles, Compose, Nginx y CI definidos. Ejecución de contenedores y CI remoto pendiente por falta de Docker y de repositorio remoto conectado.

Revisión de Fase 02 pendiente. Fase 03 sin comenzar.

## 2026-10-25 · Fase 01 preparada para revisión

- Se registró la aprobación del usuario de la Fase 00: «ok, sigamos».
- Se creó el diseño navegable local de Inicio, POS, cobro/ticket, productos, inventario, caja y configuración inicial.
- Se añadieron búsqueda por nombre/SKU/código, cantidades, espera/recuperación, cliente/nota/descuento, métodos de pago de ejemplo y cálculo de cambio.
- Se conectaron las ventas simuladas con stock, historial, indicadores y efectivo de caja de la demostración.
- Se diseñaron alta/edición de producto, validación de duplicados, ajuste con motivo, movimientos y corte con diferencia visible.
- Se prepararon vistas de escritorio/tableta/móvil, sistema visual, esquemas y capturas para revisión.
- Se incluyó un archivo HTML único que se abre sin instalaciones, un acceso de apertura y vista previa local opcional.
- Se aprobaron seis pruebas del modelo de demostración y se recorrieron los flujos principales en navegador.

El prototipo utiliza datos ficticios guardados en el navegador. No implementa la API, autenticación, aislamiento, base de datos ni transacciones comerciales del sistema real. Fase 01 pendiente de aprobación; Fase 02 sin comenzar.

## 2026-10-25 · Fase 00 preparada para revisión

- Se revisó el documento maestro de POINT y se conservó como referencia original.
- Se organizó el proyecto en sus fases 00–16, con un resultado revisable y confirmación del usuario entre partes.
- Se definieron propuestas de mercado inicial, alcance MVP, stock, conectividad, impuestos, cobros, facturación y equipos, indicando decisiones pendientes.
- Se añadieron requisitos identificados, reglas de negocio, mapa de módulos, casos de uso, backlog, riesgos y criterios de aceptación.
- Se documentaron arquitectura modular, modelo de datos/ERD inicial, API candidata, seguridad y preparación de despliegue.
- Se identificaron los servicios mínimos de caja/pagos y cliente necesarios en 06, con ampliación en 07/09.
- Se dejó la Fase 00 lista para revisión, sin aprobación registrada. La Fase 01 permanece pendiente.

Entrega documental. Aún no se han implementado ni probado funciones del punto de venta.

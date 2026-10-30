# Hito: cascarón SaaS personalizable

## En qué punto estamos

La Fase 02 proporciona un **cascarón técnico que ya puede compartirse con desarrolladores**: web, API modular, PostgreSQL, migraciones, tipos compartidos, configuración de instalación, pruebas y documentación.

Todavía no es un cascarón SaaS completo para dar de alta negocios independientes: faltan identidad, empresas, membresías, permisos y configuración por empresa. Las pruebas actuales del outbox validan su persistencia y unicidad; no sustituyen las pruebas de aislamiento de acceso de la Fase 03.

| Hito | Cuándo | Qué permite |
| --- | --- | --- |
| Base para colaborar | Ahora, Fase 02 | Clonar, preparar el entorno y desarrollar sobre una arquitectura común |
| Cascarón SaaS personalizable | Al cerrar Fase 03 y su bloque de configuración por empresa | Crear negocios separados, asignar colaboradores y personalizar cada espacio |
| Núcleo de POS operativo | Al completar 04–07 | Catálogo, inventario, venta, cobro y control de caja reales |
| MVP comercial | Con el resto del alcance obligatorio y sus validaciones/piloto | Operar con devoluciones, reportes y controles comprobados; facturación cuando el lanzamiento la requiera |

El bloque de personalización concreta el requisito de configuración del maestro; su detalle se propone para revisión del propietario. No cambia a aprobada la Fase 02 ni declara iniciada la 03.

## Qué debe incluir el cascarón SaaS

1. **Acceso y contexto autorizado.** Registro/inicio/cierre, recuperación, membresías y elección de empresa autorizada. Cambiar un ID desde el navegador no cambia los permisos.
2. **Estructura del negocio.** Empresa, sucursales, almacenes y colaboradores con estados y referencias coherentes.
3. **Permisos y auditoría.** Acciones y alcances autorizados por servidor; cambios sensibles con responsable y motivo.
4. **Configuración por empresa.** Nombre comercial, identidad visual, idioma, moneda, zona y preferencias iniciales con valores validados. Reglas comerciales específicas se amplían en sus módulos.
5. **Capacidades por negocio.** Habilitar las capacidades que estén implementadas; permisos y configuración se comprueban en servidor. Una opción de menú no habilita por sí sola una función aún inexistente.
6. **Extensión ordenada.** Esquemas/versiones de configuración, valores iniciales y cambios de esquema compatibles; referencias preparadas para agregar catálogo, inventario, ventas y fiscalidad.

## Cómo personalizar sin perder integridad

Propuesta: valores iniciales de instalación → configuración de empresa → ajustes de sucursal cuando apliquen. El servidor resuelve la configuración efectiva desde el contexto autorizado. Los cambios sensibles requieren permiso y auditoría.

El aspecto visual y las preferencias no deben cambiar los importes o impuestos de operaciones anteriores. Inventario, impuestos, comisiones, facturación e integraciones conservan reglas y pruebas propias en las fases que los implementan.

Para un nuevo giro, comenzar por configuración y catálogo. Las reglas especializadas de restaurante, taller, farmacia o salón se añadirán como módulos/extensiones cuando se acuerden; el cascarón no las implementa por adelantado.

## Demostración para aceptar el hito

- Crear dos empresas de prueba A/B con nombres, identidad y preferencias distintas.
- Entrar con usuarios diferentes y comprobar que ven el espacio y las sucursales autorizados.
- Invitar o crear un colaborador mediante el mecanismo aprobado y limitar sus acciones/alcance.
- Rechazar lectura y modificación de recursos de B desde A, incluyendo referencias relacionadas y llamadas directas a la API.
- Cambiar una preferencia en A sin modificar B; registrar el cambio cuando sea sensible.
- Comprobar que una capacidad deshabilitada no se ejecuta enviando una petición directa.
- Ejecutar migraciones y pruebas relevantes desde una clonación nueva y registrar resultados de CI/Docker.

Los recorridos de venta reales se incorporan después. El propietario revisa este hito antes de considerarlo terminado.

## Entrega inmediata al equipo

Compartir ahora la base actual y su [guía de colaboración](../CONTRIBUTING.md). Los colaboradores pueden preparar el entorno y acordar las tareas pendientes sin esperar a terminar todo el POS. El [plan de entregas](PLAN_DE_ENTREGAS.md) conserva las revisiones y dependencias.

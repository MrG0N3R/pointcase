# POINT · Sistema visual inicial

**Fase 01 · Propuesta visual para revisión.** Se implementa en [styles.css](../../../prototypes/phase-01/styles.css). El diseño se trasladará a componentes React después de aprobar esta fase.

## Dirección visual

Un mostrador digital tranquilo, con el producto al centro y el cobro siempre identificable. Fondo claro, superficies blancas, navegación verde oscuro y una sola acción principal por área. La ilustración de cada producto es SVG local, sin descargas ni servicios externos.

## Colores

| Uso | Valor | Aplicación |
| --- | --- | --- |
| Texto principal | `#223c36` | Títulos, totales y datos importantes |
| Acción principal | `#19664d` | Cobrar, guardar y continuar |
| Acción al señalar | `#11523c` | Respuesta de botones principales |
| Navegación | `#163d36` | Barra lateral y marca |
| Fondo | `#f6f7f5` | Área de trabajo |
| Superficie | `#ffffff` | Tarjetas, tablas y formularios |
| Separación | `#e5e9e3` | Bordes y divisiones |
| Información secundaria | `#67756f` | Descripciones y ayuda |
| Acierto | Verde suave con texto verde | Caja abierta, disponible, cambio válido |
| Atención | Amarillo suave con texto marrón | Stock bajo, diferencia de caja |
| Error | `#a43536` y etiqueta explícita | Validación, falta de efectivo o stock |
| Foco de teclado | `#4d8cd0` | Contorno visible de campos y acciones |

Los estados usan texto además de color. Las superficies de producto tienen tonos arena, azul, melocotón, rosa, menta y lila para distinguirlos sin recargar la pantalla.

## Tipografía y medidas

- Fuente del sistema: Segoe UI, fuentes de sistema y Arial. Sin fuentes remotas.
- Título principal: 25–34 px según ancho; total de venta: 27 px; total de cobro: 30–38 px.
- Texto operativo compacto en escritorio; campos de cobro grandes y cifras alineadas.
- Espaciado base de 4/8 px; paneles separados por 18–28 px.
- Botones principales de al menos 44 px de alto; áreas de producto completas como botones.
- Radios: 8 px en campos/acciones, 12–16 px en tarjetas y 18 px en ventanas.
- Movimiento breve al señalar y abrir avisos; respeta `prefers-reduced-motion`.

## Componentes disponibles

| Componente | Estados de ejemplo |
| --- | --- |
| Navegación | Activa, normal, iconos en tableta, menú y barra inferior en móvil |
| Botones | Primario, secundario, icono, deshabilitado y foco |
| Campo de búsqueda | Vacío, con texto, sin coincidencias y lectura de código exacto |
| Tarjeta de producto | Disponible, últimas piezas, agotado y servicio |
| Carrito | Vacío, con productos, cantidades, descuento, cliente/nota y espera |
| Cobro | Efectivo exacto, recibido insuficiente, cambio, terminal externa y transferencia |
| Formularios | Requerido, tipo/importe inválido, SKU/código repetido y guardado de ejemplo |
| Estado de inventario | Disponible, stock bajo, agotado y movimiento con motivo |
| Caja | Abierta, cerrada, diferencia pendiente de explicación y corte registrado |
| Avisos | Información, advertencia, error del campo y confirmación breve |
| Tablas | Lista con filas y desplazamiento interno horizontal cuando es necesario |
| Modal | Fondo atenuado, foco nativo, cierre por botón/Escape y restauración de foco |
| Asistente | Paso actual, completado, anterior y confirmación final |

En este prototipo no hay solicitudes de datos remotas ni un tiempo de carga que simular. En la Fase 02, el estado de carga de tablas/tarjetas reservará sus dimensiones con esqueletos y el botón de envío mostrará progreso y bloqueará envíos repetidos hasta respuesta. No se introduce una espera artificial para aparentar servicios existentes.

## Adaptación de pantalla

| Tamaño de revisión | Comportamiento |
| --- | --- |
| Escritorio · 1280 × 800 | Barra lateral completa, catálogo y carrito en columnas, cobro visible y productos del carrito desplazables |
| Tableta · 768 × 1024 | Barra lateral de iconos con nombres accesibles, dos columnas de productos y carrito lateral |
| Móvil · 360 × 800 | Navegación inferior, catálogo en dos columnas, botón persistente de venta y carrito superpuesto; formulario de cobro en una columna |

Las tablas conservan sus columnas en un contenedor desplazable, sin ensanchar toda la página. La configuración usa un paso por pantalla en móvil. Las capturas están en [evidence](evidence).

## Accesibilidad prevista en el prototipo

Idioma es-MX, etiquetas de campos, nombres accesibles de iconos, foco visible, enlace para saltar al contenido, navegación con teclado, modales nativos, `role=status` para avisos y `role=alert` para errores. Los productos agotados y botones no disponibles se deshabilitan con indicación visible.

La revisión automatizada y manual de accesibilidad de producción se ampliará con los componentes reales. Este documento no declara certificación de accesibilidad ni autorización real de usuarios.

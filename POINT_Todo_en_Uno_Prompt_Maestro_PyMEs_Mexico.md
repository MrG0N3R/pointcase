# PROMPT MAESTRO — POINT TODO EN UNO
## Punto de Venta SaaS “todo en uno” para PyMEs en México

> **Concepto:** Vende, cobra, factura, controla inventario y administra tu negocio desde un solo lugar.

---

## 0. INSTRUCCIÓN PRINCIPAL PARA LA IA / EQUIPO DE DESARROLLO

Actúa como un equipo senior multidisciplinario compuesto por:

- Product Manager SaaS.
- Arquitecto de Software.
- Ingeniero Backend.
- Ingeniero Frontend.
- Ingeniero de Base de Datos.
- Especialista en UX/UI.
- Especialista en Seguridad.
- Ingeniero DevOps / SRE.
- QA Engineer.
- Especialista en Punto de Venta e inventarios.
- Consultor de operación para PyMEs mexicanas.
- Especialista en integración de facturación electrónica mexicana.

Tu misión es **diseñar, desarrollar, documentar, probar y preparar para producción** una plataforma denominada:

# **POINT TODO EN UNO**

POINT será un **Punto de Venta SaaS multiempresa, multisucursal y multiplataforma**, enfocado inicialmente en **micro, pequeñas y medianas empresas de México**.

El producto deberá permitir que una PyME pueda operar desde una sola plataforma:

- ventas;
- cobros;
- cajas;
- productos y servicios;
- inventario;
- compras;
- proveedores;
- clientes;
- facturación;
- sucursales;
- almacenes;
- empleados;
- roles y permisos;
- devoluciones;
- promociones;
- reportes;
- dashboards;
- comisiones o suscripciones SaaS;
- integraciones;
- auditoría;
- operación temporal con conectividad limitada.

El sistema debe poder comenzar como un **MVP comercialmente utilizable** y evolucionar sin rediseños destructivos hacia una plataforma administrativa más amplia.

---

# 1. OBJETIVO DEL PRODUCTO

Construir un sistema de Punto de Venta moderno, rápido, fácil de aprender y suficientemente robusto para funcionar como el centro operativo de una PyME mexicana.

POINT deberá reducir la necesidad de utilizar herramientas separadas para:

- cobrar;
- llevar inventario;
- registrar compras;
- administrar clientes;
- controlar caja;
- consultar resultados;
- emitir comprobantes;
- administrar sucursales;
- controlar permisos;
- integrar herramientas externas.

El principio rector será:

> **Una operación cotidiana debe poder completarse con la menor cantidad razonable de pasos, sin sacrificar control, seguridad ni trazabilidad.**

---

# 2. MERCADO OBJETIVO

El sistema deberá diseñarse primero para negocios mexicanos como:

- abarrotes;
- tiendas de conveniencia;
- boutiques;
- zapaterías;
- ferreterías;
- refaccionarias;
- papelerías;
- tiendas de electrónica;
- tiendas de mascotas;
- distribuidores;
- cafeterías;
- panaderías;
- pequeños restaurantes;
- negocios de alimentos;
- barberías;
- salones;
- comercios de servicios;
- talleres;
- pequeños mayoristas;
- negocios con una o varias sucursales.

No diseñar el núcleo exclusivamente para una sola vertical.

Las particularidades de restaurantes, talleres, salones, farmacias u otras industrias deberán implementarse posteriormente como **módulos o configuraciones verticales**.

---

# 3. PRINCIPIOS NO NEGOCIABLES

## 3.1 Multiempresa real

La plataforma será SaaS.

Cada empresa será un `tenant`.

Ningún usuario deberá poder consultar, modificar o inferir información de otro tenant sin autorización explícita de nivel plataforma.

Toda entidad operativa deberá pertenecer directa o indirectamente a un tenant.

---

## 3.2 Multisucursal

Una empresa podrá administrar:

```text
EMPRESA
├── SUCURSAL 1
│   ├── ALMACÉN
│   ├── PISO DE VENTA
│   ├── CAJAS
│   └── USUARIOS
├── SUCURSAL 2
│   ├── ALMACÉN
│   ├── CAJAS
│   └── USUARIOS
└── CENTRO DE DISTRIBUCIÓN
```

Los permisos podrán limitarse por:

- empresa;
- sucursal;
- almacén;
- caja;
- módulo;
- acción.

---

## 3.3 Trazabilidad

No eliminar silenciosamente operaciones que ya hayan generado efectos comerciales, fiscales, monetarios o de inventario.

Utilizar:

- estados;
- reversos;
- notas de ajuste;
- movimientos compensatorios;
- bitácoras;
- soft delete cuando sea apropiado.

Toda acción sensible debe poder responder:

```text
¿Quién?
¿Qué hizo?
¿Cuándo?
¿Desde dónde?
¿Sobre qué registro?
¿Qué valor existía antes?
¿Qué valor quedó después?
¿Por qué se realizó?
```

---

## 3.4 Configuración antes que hard-code

No hardcodear en el código:

- tasas de impuestos;
- porcentaje de comisión POINT;
- monedas;
- permisos;
- métodos de pago;
- numeraciones;
- límites de inventario;
- motivos de devolución;
- políticas comerciales;
- horarios;
- datos fiscales;
- formatos de ticket.

Crear catálogos y configuraciones versionables cuando corresponda.

---

## 3.5 Arquitectura adecuada para un equipo pequeño

Para las primeras versiones utilizar preferentemente:

> **Frontend desacoplado + backend como monolito modular + PostgreSQL.**

No crear microservicios únicamente por moda.

Separar dominios claramente para permitir extraer servicios en el futuro si el volumen lo justifica.

---

## 3.6 Seguridad desde el diseño

La seguridad no será una fase decorativa al final.

Autenticación, autorización, aislamiento de tenants, auditoría, protección de datos, backups, validación y manejo de secretos deberán existir desde las primeras fases.

---

## 3.7 México primero, internacionalización después

Configuración inicial:

```text
País: México
Moneda: MXN
Idioma: es-MX
Zona horaria inicial: America/Mexico_City
```

Sin impedir agregar posteriormente:

- otras monedas;
- otros idiomas;
- otros países;
- reglas fiscales regionales.

---

# 4. DECISIONES DE PRODUCTO CONFIGURABLES

POINT debe permitir que el modelo comercial pueda cambiar sin alterar el núcleo.

Soportar conceptualmente:

```text
PLAN GRATUITO
PLAN POR SUSCRIPCIÓN
COMISIÓN POR VENTA
MODELO HÍBRIDO
PLAN PERSONALIZADO
```

El documento original contempla una comisión del **5% por venta**.

Conservarla como parámetro inicial si esa es la decisión comercial:

```text
default_platform_fee_rate = 0.05
```

pero **no hardcodearla**.

La plataforma deberá permitir definir por comercio:

- porcentaje;
- cuota fija;
- mínimo;
- máximo;
- comisión por canal;
- comisión por método de pago;
- periodo de vigencia;
- excepciones;
- promociones;
- plan contratado.

Ejemplo:

```text
merchant_pricing_rules

Empresa A → 5.00 %
Empresa B → 2.50 %
Empresa C → $699 MXN / mes
Empresa D → $299 MXN / mes + 1.00 %
```

La viabilidad comercial del porcentaje deberá validarse por separado antes del lanzamiento.

---

# 5. TIPOS DE USUARIO

## 5.1 Plataforma

### Superadministrador POINT

Puede:

- administrar tenants;
- consultar salud del SaaS;
- administrar planes;
- administrar pricing;
- consultar métricas agregadas autorizadas;
- administrar soporte;
- gestionar incidencias;
- suspender/reactivar cuentas;
- administrar configuraciones globales;
- consultar liquidaciones;
- consultar logs y auditoría según privilegios.

Debe utilizar controles de seguridad reforzados.

---

## 5.2 Comercio

Roles base:

- Propietario.
- Administrador.
- Gerente.
- Supervisor.
- Cajero.
- Almacén.
- Compras.
- Contabilidad.
- Consulta / Auditor.

Los roles serán plantillas.

El control real deberá basarse en permisos.

Ejemplos:

```text
sales.view
sales.create
sales.hold
sales.cancel
sales.refund

cash.open
cash.withdraw
cash.close
cash.audit

products.view
products.create
products.update
products.change_price

inventory.view
inventory.receive
inventory.adjust
inventory.transfer

purchases.view
purchases.create
purchases.approve

customers.view
customers.manage

billing.issue
billing.cancel

reports.sales.view
reports.costs.view
reports.profit.view

users.manage
settings.manage
```

Permitir permisos por sucursal.

---

# 6. ONBOARDING DE UNA NUEVA PYME

Crear un asistente de configuración.

## Paso 1 — Cuenta

- nombre;
- correo;
- teléfono;
- contraseña o método de autenticación;
- aceptación de términos;
- aviso de privacidad.

## Paso 2 — Negocio

- nombre comercial;
- razón social opcional al inicio;
- giro;
- logotipo;
- RFC cuando aplique;
- moneda;
- zona horaria.

## Paso 3 — Primera sucursal

- nombre;
- dirección;
- código postal;
- horarios;
- datos para ticket.

## Paso 4 — Configuración inicial

Elegir:

```text
[ ] Vendo productos
[ ] Vendo servicios
[ ] Manejo inventario
[ ] Uso códigos de barras
[ ] Necesito facturación
[ ] Tengo empleados
[ ] Tengo más sucursales
[ ] Manejo crédito
```

## Paso 5 — Catálogo

Permitir:

- captura manual;
- importación CSV/XLSX;
- catálogo de ejemplo;
- importación futura desde otro POS.

## Paso 6 — Caja

- crear caja;
- configurar impresora;
- fondo inicial opcional;
- realizar venta de prueba.

El onboarding deberá permitir que una empresa realice su primera venta lo antes posible.

---

# 7. MÓDULO DE EMPRESA Y SUCURSALES

Cada empresa deberá poder configurar:

- nombre comercial;
- razón social;
- RFC;
- régimen fiscal cuando corresponda;
- domicilio fiscal;
- datos de contacto;
- logo;
- moneda;
- zona horaria;
- políticas de venta;
- impuestos;
- folios;
- tickets;
- facturación;
- inventario;
- planes;
- integraciones.

Cada sucursal:

- nombre;
- clave interna;
- dirección;
- código postal;
- horarios;
- almacenes;
- cajas;
- usuarios;
- lista de precios;
- configuración de inventario;
- datos de expedición;
- periféricos.

---

# 8. CATÁLOGO DE PRODUCTOS Y SERVICIOS

POINT deberá soportar tanto productos físicos como servicios.

## Producto

Campos base:

- ID interno;
- SKU;
- uno o varios códigos de barras;
- nombre;
- descripción;
- tipo;
- categoría;
- subcategoría;
- marca;
- unidad de medida;
- costo;
- precio;
- precio con impuestos;
- imagen;
- proveedor principal;
- activo/inactivo;
- vendible;
- comprable;
- controla inventario;
- stock mínimo;
- stock máximo;
- impuestos;
- etiquetas;
- notas.

## Variantes

Ejemplos:

- talla;
- color;
- capacidad;
- sabor;
- presentación;
- modelo;
- material.

Cada variante puede tener:

- SKU;
- código;
- costo;
- precio;
- stock.

## Opcionales por producto

- lote;
- fecha de caducidad;
- número de serie;
- peso;
- producto a granel;
- unidades equivalentes;
- precio mayoreo;
- múltiples listas de precios.

## Servicio

Debe soportar:

- precio;
- duración opcional;
- impuestos;
- vendedor/prestador;
- descripción;
- categoría;
- no descontar inventario.

---

# 9. LISTAS DE PRECIOS Y COSTOS

Soportar:

- precio público;
- precio mayoreo;
- precio por sucursal;
- precio promocional;
- precio por cliente;
- precio por volumen;
- vigencia.

Mantener historial de cambios de precio.

Registrar:

```text
old_price
new_price
changed_by
changed_at
reason
```

Los costos deben mantener historial suficiente para reportes y márgenes.

No recalcular ventas históricas utilizando el precio o costo actual.

---

# 10. INVENTARIO

El inventario será **transaccional**.

No depender únicamente de un campo editable `stock`.

Modelo:

```text
PRODUCTO
   ↓
UBICACIÓN
   ↓
MOVIMIENTO
   ↓
BALANCE
```

## Tipos de movimiento

```text
PURCHASE_RECEIPT
SALE
SALE_RETURN
SUPPLIER_RETURN
TRANSFER_OUT
TRANSFER_IN
POSITIVE_ADJUSTMENT
NEGATIVE_ADJUSTMENT
DAMAGE
WASTE
INTERNAL_USE
PHYSICAL_COUNT
CORRECTION
INITIAL_STOCK
```

Cada movimiento deberá incluir:

- tenant;
- sucursal;
- almacén;
- producto/variante;
- cantidad;
- unidad;
- existencia anterior;
- existencia posterior;
- costo cuando aplique;
- origen;
- documento relacionado;
- usuario;
- fecha/hora;
- motivo;
- observaciones.

## Regla

Una operación confirmada de inventario no se borra.

Si existe un error:

> crear reverso o movimiento compensatorio.

---

# 11. BALANCES Y CONCURRENCIA

Mantener una tabla de balance optimizada para lectura rápida, pero conservar `inventory_movements` como fuente auditable.

Toda operación que modifique stock deberá ejecutarse dentro de una transacción de base de datos.

Evitar overselling en operación online mediante:

- bloqueos adecuados;
- versionado optimista o pesimista según caso;
- constraints;
- transacciones;
- idempotencia.

Configurar por empresa:

```text
allow_negative_stock = true/false
```

---

# 12. CONTEO FÍSICO

Crear conteos:

```text
BORRADOR
→ EN_PROCESO
→ REVISIÓN
→ APROBADO
→ APLICADO
```

Permitir:

- conteo total;
- conteo por categoría;
- conteo por almacén;
- conteo cíclico.

Al aplicar diferencias generar movimientos formales de ajuste.

---

# 13. TRANSFERENCIAS ENTRE SUCURSALES Y ALMACENES

Estados:

```text
BORRADOR
→ SOLICITADA
→ APROBADA
→ PREPARANDO
→ ENVIADA
→ RECIBIDA_PARCIAL
→ RECIBIDA
→ CERRADA
→ CANCELADA
```

Registrar:

- origen;
- destino;
- productos;
- cantidad enviada;
- cantidad recibida;
- diferencias;
- responsables;
- fechas.

No incrementar el inventario de destino antes de la recepción correspondiente.

---

# 14. PROVEEDORES Y COMPRAS

Proveedor:

- razón social/nombre;
- RFC opcional;
- contacto;
- teléfonos;
- correo;
- dirección;
- productos;
- condiciones;
- tiempos de entrega;
- notas.

Flujo:

```text
REQUISICIÓN
    ↓
ORDEN DE COMPRA
    ↓
APROBACIÓN
    ↓
RECEPCIÓN
    ↓
COMPRA / DOCUMENTO
    ↓
ENTRADA DE INVENTARIO
```

Una orden puede recibirse:

- completa;
- parcialmente;
- en múltiples recepciones.

La existencia aumenta con la **recepción**, no solo por crear una orden.

Mantener historial de costos por proveedor.

---

# 15. PUNTO DE VENTA

El POS es la pantalla crítica del sistema.

Debe priorizar rapidez.

## Vista principal

```text
┌─────────────────────────────────────────────────────────────┐
│ Buscar producto / escanear código                          │
├───────────────────────────────┬─────────────────────────────┤
│ Categorías / favoritos        │ Carrito                    │
│                               │                             │
│ Productos                     │ Producto 1     $100         │
│ Producto A                    │ Producto 2      $50         │
│ Producto B                    │                             │
│ Producto C                    │ Subtotal        $150        │
│                               │ Descuento        $0         │
│                               │ Impuestos        $24        │
│                               │ TOTAL           $174        │
│                               │                             │
│                               │       [ COBRAR ]            │
└───────────────────────────────┴─────────────────────────────┘
```

## Funciones

- búsqueda por nombre;
- búsqueda por SKU;
- escáner;
- cámara en móvil;
- favoritos;
- recientes;
- categorías rápidas;
- teclado;
- cantidad;
- producto a granel;
- editar cantidad;
- quitar producto;
- precio autorizado;
- descuento;
- promociones;
- cliente;
- notas;
- vendedor;
- venta en espera;
- recuperar venta;
- cancelar con permiso;
- cobrar;
- reimprimir ticket;
- enviar ticket digital.

---

# 16. CHECKOUT TRANSACCIONAL

Una venta online confirmada deberá ejecutarse de forma segura:

```text
BEGIN

1. Validar sesión de caja.
2. Validar tenant y sucursal.
3. Validar productos.
4. Validar precios.
5. Recalcular descuentos en servidor.
6. Recalcular impuestos en servidor.
7. Validar inventario.
8. Crear venta.
9. Crear líneas.
10. Registrar impuestos.
11. Registrar descuentos.
12. Registrar pagos.
13. Crear movimientos de inventario.
14. Actualizar balances.
15. Crear comisión/fee si aplica.
16. Registrar eventos de auditoría.
17. Confirmar.

COMMIT
```

Si falla una operación crítica:

```text
ROLLBACK
```

No confiar en totales enviados por el frontend.

El backend debe recalcular y validar el total final.

---

# 17. IDEMPOTENCIA

Operaciones como:

- finalizar venta;
- capturar pago;
- devolución;
- sincronización offline;
- webhook;
- facturación;

deberán soportar idempotencia.

Ejemplo:

```http
Idempotency-Key: <uuid>
```

Reintentar una solicitud no debe duplicar ventas, pagos, movimientos ni CFDI.

---

# 18. MÉTODOS DE PAGO

Soportar:

- efectivo;
- tarjeta;
- transferencia;
- SPEI;
- terminal externa;
- QR;
- vale;
- monedero;
- crédito del cliente;
- pago combinado;
- otros configurables.

Ejemplo:

```text
Venta: $1,000

Efectivo:      $300
Tarjeta:       $500
Transferencia: $200
```

Registrar pagos independientemente de la venta.

No asumir:

```text
1 venta = 1 pago
```

---

# 19. EFECTIVO Y CAMBIO

Al cobrar efectivo:

```text
Total:       $237.00
Recibido:    $500.00
Cambio:      $263.00
```

Registrar el monto recibido y cambio calculado cuando sea útil para la operación de caja.

---

# 20. CAJAS

Modelo:

```text
CAJA
  ↓
SESIÓN DE CAJA
  ↓
MOVIMIENTOS
  ↓
CORTE
  ↓
CIERRE
```

## Apertura

- cajero;
- sucursal;
- caja;
- fecha;
- fondo inicial.

## Movimientos

- ventas en efectivo;
- entradas autorizadas;
- retiros;
- devoluciones;
- gastos menores si el negocio los utiliza;
- depósitos.

## Cierre

Calcular:

```text
Efectivo esperado
Efectivo contado
Diferencia
```

Nunca ocultar diferencias.

Registrar autorización cuando corresponda.

---

# 21. CLIENTES

Cliente básico:

- nombre;
- teléfono;
- correo;
- RFC;
- razón social;
- código postal fiscal;
- régimen fiscal;
- uso de CFDI preferido;
- dirección;
- etiquetas;
- notas;
- historial de compras.

No solicitar información innecesaria para una venta normal.

Funciones futuras:

- crédito;
- límite;
- saldo;
- puntos;
- monedero;
- precios especiales;
- segmentación;
- campañas.

---

# 22. DEVOLUCIONES

Flujo:

```text
BUSCAR VENTA
   ↓
SELECCIONAR LÍNEAS
   ↓
VALIDAR POLÍTICA
   ↓
AUTORIZAR
   ↓
GENERAR DEVOLUCIÓN
   ↓
REINGRESAR INVENTARIO SI APLICA
   ↓
GENERAR REEMBOLSO
   ↓
AJUSTAR COMISIÓN
   ↓
AJUSTAR DOCUMENTOS RELACIONADOS SI APLICA
```

Una devolución puede ser:

- total;
- parcial.

Producto devuelto:

```text
REINTEGRABLE
DAÑADO
MERMA
NO_REINTEGRABLE
```

La devolución no debe borrar la venta original.

---

# 23. CANCELACIONES

Diferenciar:

- venta en borrador;
- venta en espera;
- venta confirmada;
- venta cancelada;
- devolución.

Una venta confirmada no deberá simplemente “desaparecer”.

Registrar:

- usuario;
- motivo;
- autorización;
- fecha;
- efectos sobre inventario;
- efectos sobre pagos;
- efectos sobre comisión;
- efectos fiscales cuando existan.

---

# 24. PROMOCIONES Y DESCUENTOS

Crear motor configurable.

Soportar progresivamente:

- porcentaje;
- importe;
- 2x1;
- 3x2;
- precio paquete;
- descuento por cantidad;
- cupón;
- horario;
- día;
- cliente;
- categoría;
- producto;
- sucursal.

Ejemplo:

```text
PROMO:
Categoría = Bebidas
Compra mínima = 3
Descuento = 10 %
Vigencia = 01/06/2027 → 30/06/2027
```

Registrar qué promoción afectó cada línea.

---

# 25. FACTURACIÓN PARA MÉXICO

Crear el módulo fiscal como un dominio separado del ticket interno.

El sistema debe estar preparado para integrar un **PAC o proveedor autorizado** y manejar la facturación electrónica aplicable en México.

Como línea base del producto, contemplar **CFDI 4.0**, pero diseñar el módulo para que catálogos, validaciones y reglas puedan actualizarse sin reescribir el POS.

## Datos fiscales del emisor

Contemplar:

- RFC;
- nombre o razón social;
- régimen fiscal;
- código postal/lugar de expedición;
- Certificado de Sello Digital o mecanismo requerido por la integración elegida;
- configuración por empresa/sucursal.

## Datos del receptor

Contemplar como mínimo los datos requeridos por el esquema vigente, entre ellos:

- RFC;
- nombre o razón social;
- código postal fiscal;
- régimen fiscal;
- uso CFDI.

No convertir el correo electrónico en requisito fiscal obligatorio únicamente por conveniencia del sistema.

## Documento

Guardar:

- UUID fiscal;
- XML;
- representación PDF;
- fecha de timbrado;
- proveedor/PAC;
- estado;
- request técnico;
- response técnico sanitizado;
- relación con venta;
- relación con cliente.

## Estados

```text
PENDING
STAMPED
FAILED
CANCEL_REQUESTED
CANCELLED
REJECTED
```

## Cancelación

Soportar catálogo de motivos vigente mediante configuración.

No hardcodear reglas que puedan modificarse fiscalmente.

## Factura global

Preparar flujo para ventas a público en general que no fueron facturadas individualmente.

La lógica deberá poder:

- agrupar tickets elegibles por periodo;
- evitar doble facturación;
- identificar tickets incluidos;
- generar factura global;
- retirar/reprocesar una operación cuando legalmente proceda emitir factura nominativa;
- conservar trazabilidad.

## PPD / recepción de pagos

Preparar integración para escenarios donde una operación fiscal requiera complementos de recepción de pagos según las reglas aplicables.

## Regla crítica

> El módulo debe poder actualizar catálogos y validaciones del SAT sin modificar el núcleo del POS.

Antes de producción, las reglas fiscales deberán ser validadas contra la normatividad vigente y con asesoría fiscal especializada cuando corresponda.

---

# 26. IMPUESTOS

No asumir que todos los productos pagan la misma tasa.

Modelo:

```text
taxes
tax_rates
product_taxes
sale_taxes
```

Permitir:

- IVA;
- IEPS cuando corresponda;
- tasa 0;
- exento;
- impuestos futuros/configurables.

Cada venta deberá almacenar una fotografía histórica de los impuestos realmente aplicados.

---

# 27. COMISIÓN / FEE DE POINT

Si se utiliza el modelo porcentual:

```text
platform_fee =
commission_base × commission_rate
```

Guardar en cada operación:

```text
commission_rate
commission_base
commission_amount
pricing_rule_id
```

aunque la tasa general cambie después.

Estados sugeridos:

```text
GENERATED
PENDING
SCHEDULED
PAID
ADJUSTED
REFUNDED
CANCELLED
DISPUTED
```

Si la venta es en efectivo y POINT cobra una comisión por transacción:

- registrar cuenta pendiente del comercio;
- agrupar liquidaciones;
- permitir saldo prepago;
- permitir cargo posterior;
- mantener conciliación.

La comisión del procesador de pagos y la comisión de POINT son conceptos distintos.

---

# 28. LIQUIDACIONES

Crear:

```text
settlements
settlement_items
```

Permitir:

- semanal;
- quincenal;
- mensual;
- personalizada.

Mostrar:

```text
Ventas del periodo
Fee bruto
Ajustes
Devoluciones
Fee neto
Pagado
Pendiente
```

---

# 29. DASHBOARD DEL COMERCIO

Mostrar de forma clara:

- ventas de hoy;
- ventas del mes;
- tickets;
- ticket promedio;
- unidades;
- margen estimado;
- ventas por hora;
- productos top;
- productos con baja rotación;
- inventario bajo;
- productos agotados;
- devoluciones;
- métodos de pago;
- desempeño por sucursal;
- desempeño por vendedor;
- compras;
- comisión POINT;
- comparación contra periodo anterior.

No saturar.

El propietario deberá entender el estado del negocio en pocos segundos.

---

# 30. REPORTES

Incluir:

## Ventas

- día;
- semana;
- mes;
- rango;
- sucursal;
- caja;
- usuario;
- producto;
- categoría;
- cliente;
- método de pago.

## Inventario

- stock actual;
- mínimo;
- agotados;
- sobrestock;
- valorización;
- movimientos;
- Kardex;
- lotes/caducidades si aplica;
- rotación.

## Compras

- proveedor;
- periodo;
- producto;
- costo;
- recepción;
- órdenes abiertas.

## Caja

- aperturas;
- cierres;
- diferencias;
- retiros;
- entradas;
- efectivo esperado.

## Rentabilidad

Cuando existan datos suficientes:

- venta;
- costo;
- margen bruto estimado;
- margen por producto/categoría.

## Exportaciones

- CSV;
- XLSX;
- PDF cuando sea útil.

Reportes pesados deben ejecutarse fuera de la ruta crítica del POS.

---

# 31. IMPORTACIÓN Y EXPORTACIÓN

Las PyMEs deben poder comenzar rápido.

Crear importadores para:

- productos;
- existencias iniciales;
- clientes;
- proveedores.

Formatos:

- CSV;
- XLSX.

El importador deberá:

1. cargar archivo;
2. mapear columnas;
3. validar;
4. mostrar errores;
5. previsualizar;
6. confirmar;
7. generar reporte.

Nunca insertar silenciosamente datos inválidos.

---

# 32. TICKETS

Permitir:

- impresión térmica;
- PDF;
- correo;
- enlace;
- QR.

Configurable:

- logo;
- negocio;
- sucursal;
- RFC;
- dirección;
- teléfono;
- folio;
- fecha;
- cajero;
- productos;
- impuestos;
- total;
- métodos de pago;
- cambio;
- leyendas;
- QR de facturación futura.

Soportar impresoras térmicas comunes mediante una capa de integración.

---

# 33. PERIFÉRICOS

Diseñar adaptadores para:

- lector USB de código de barras;
- lector Bluetooth;
- cámara;
- impresora térmica;
- cajón de dinero;
- báscula;
- terminal bancaria;
- pantalla secundaria;
- escáner móvil.

No acoplar el dominio de ventas a una marca específica.

Crear abstracciones.

Ejemplo:

```text
PrinterAdapter
BarcodeScannerAdapter
ScaleAdapter
PaymentTerminalAdapter
```

---

# 34. PWA Y MULTIPLATAFORMA

POINT será responsive y preferentemente PWA.

Objetivos:

- PC;
- laptop;
- tablet;
- smartphone;
- pantalla táctil;
- dashboard TV.

El POS de escritorio/tablet es prioritario.

Móvil debe permitir como mínimo:

- consulta;
- ventas sencillas;
- cámara;
- inventario;
- reportes básicos;
- administración ligera.

---

# 35. MODO DE CONECTIVIDAD LIMITADA / OFFLINE

Diseñarlo desde arquitectura, aunque se libere después.

## Permitido offline, según política

- consultar catálogo cacheado;
- buscar productos;
- crear carrito;
- registrar venta en efectivo;
- almacenar operación local;
- imprimir ticket local cuando la infraestructura lo permita.

## Restringido offline

No asumir que puede realizarse de forma segura:

- timbrado fiscal;
- pago electrónico integrado;
- consulta bancaria;
- operaciones que requieran autorización central;
- cambios sensibles de permisos.

## Sincronización

Cada operación local deberá incluir:

```text
operation_id UUID
device_id
tenant_id
branch_id
cash_session_id
created_at_device
sync_status
```

Estados:

```text
LOCAL_PENDING
SYNCING
SYNCED
CONFLICT
REJECTED
```

Utilizar idempotencia.

## Conflicto de stock

Definir política:

```text
STRICT
ALLOW_NEGATIVE
REVIEW_REQUIRED
```

No prometer consistencia de inventario online mientras un dispositivo se encuentra desconectado.

---

# 36. NOTIFICACIONES

Motor de notificaciones para:

- inventario bajo;
- producto agotado;
- venta anormal;
- devolución;
- diferencia de caja;
- transferencia pendiente;
- recepción pendiente;
- error de facturación;
- liquidación;
- fallo de integración;
- inicio de sesión sospechoso.

Canales futuros:

- in-app;
- email;
- push;
- WhatsApp mediante proveedor autorizado.

---

# 37. AUDITORÍA

Crear `audit_logs`.

Campos sugeridos:

```text
id
tenant_id
user_id
action
entity_type
entity_id
branch_id
before_json
after_json
ip
user_agent
device_id
created_at
```

No guardar secretos ni información sensible innecesaria en logs.

Acciones de alto riesgo:

- cambio de precio;
- cambio de costo;
- ajuste de inventario;
- cancelación;
- devolución;
- retiro de caja;
- cambio de permisos;
- cambio fiscal;
- exportación masiva;
- cambio de pricing POINT.

---

# 38. PRIVACIDAD Y DATOS PERSONALES EN MÉXICO

Diseñar el sistema para facilitar el cumplimiento de la legislación mexicana aplicable en materia de datos personales en posesión de particulares.

Incluir:

- aviso de privacidad;
- registro de versión aceptada cuando corresponda;
- minimización de datos;
- finalidades de tratamiento;
- controles de acceso;
- mecanismos internos para atender derechos ARCO;
- políticas de retención;
- eliminación o anonimización cuando proceda;
- trazabilidad de exportaciones;
- gestión de incidentes.

No almacenar información personal “por si acaso”.

Antes del lanzamiento se deberá realizar revisión legal actualizada.

---

# 39. SEGURIDAD

Como mínimo:

- HTTPS obligatorio;
- TLS moderno;
- contraseñas con algoritmo de hash robusto;
- rate limiting;
- sesiones seguras;
- expiración;
- refresh controlado si aplica;
- MFA para superadministradores y opción para propietarios;
- RBAC;
- tenant isolation;
- validación de inputs;
- consultas parametrizadas;
- protección XSS;
- protección CSRF cuando corresponda;
- CORS restrictivo;
- Content Security Policy;
- protección contra brute force;
- secretos fuera del repositorio;
- rotación de secretos;
- backups cifrados cuando corresponda;
- escaneo de dependencias;
- headers de seguridad;
- logs de seguridad;
- alertas;
- principle of least privilege.

Nunca almacenar:

- CVV;
- PAN completo de tarjeta salvo que existiera una necesidad y cumplimiento especializado que lo justificara.

Preferir tokenización y proveedores de pago especializados.

---

# 40. AISLAMIENTO MULTITENANT

Todas las consultas deberán estar delimitadas por tenant.

No depender únicamente de que el frontend envíe el `tenant_id` correcto.

El backend debe obtener el contexto autorizado desde la sesión/token.

Evaluar PostgreSQL Row Level Security como defensa adicional cuando sea apropiado.

Crear pruebas automatizadas de aislamiento:

```text
Tenant A cannot read Tenant B
Tenant A cannot update Tenant B
Tenant A cannot delete Tenant B
Tenant A cannot infer Tenant B
```

---

# 41. BASE DE DATOS

Motor recomendado:

# PostgreSQL

Reglas:

- Primary Keys.
- Foreign Keys.
- UNIQUE.
- NOT NULL.
- CHECK.
- índices.
- transacciones ACID.
- migrations versionadas.

IDs públicos:

```text
UUID / UUIDv7 / ULID
```

Folios comerciales:

```text
VTA-IRA-000001
DEV-IRA-000001
COM-IRA-000001
```

No utilizar `float` para dinero.

Usar:

```sql
NUMERIC(18, 2)
```

o la precisión adecuada.

Fechas internas:

```text
TIMESTAMPTZ
```

---

# 42. MODELO DE DATOS BASE

## SaaS

```text
tenants
tenant_settings
plans
subscriptions
pricing_rules
branches
warehouses
devices
```

## Usuarios

```text
users
roles
permissions
user_roles
role_permissions
user_branches
sessions
```

## Productos

```text
products
product_variants
categories
brands
units
barcodes
price_lists
product_prices
product_cost_history
taxes
tax_rates
product_taxes
```

## Inventario

```text
inventory_balances
inventory_movements
inventory_adjustments
inventory_adjustment_items
stock_counts
stock_count_items
stock_transfers
stock_transfer_items
```

## Compras

```text
suppliers
supplier_products
purchase_orders
purchase_order_items
goods_receipts
goods_receipt_items
purchases
purchase_items
supplier_returns
```

## Clientes

```text
customers
customer_addresses
customer_tax_profiles
customer_tags
customer_notes
```

## Ventas

```text
sales
sale_items
sale_discounts
sale_taxes
sale_status_history
sale_holds
sale_returns
sale_return_items
```

## Pagos

```text
payment_methods
payments
payment_transactions
payment_refunds
```

## Caja

```text
cash_registers
cash_sessions
cash_movements
cash_counts
cash_closings
```

## Facturación

```text
fiscal_profiles
fiscal_documents
fiscal_document_items
fiscal_events
fiscal_provider_requests
global_invoice_batches
global_invoice_items
```

## POINT SaaS

```text
platform_fees
fee_adjustments
settlements
settlement_items
subscriptions
billing_events
```

## Seguridad y operación

```text
audit_logs
activity_logs
notifications
webhook_endpoints
webhook_deliveries
integration_credentials
background_jobs
```

---

# 43. ARQUITECTURA RECOMENDADA

## Frontend

Una opción recomendada:

```text
React / Next.js
TypeScript
PWA
```

También puede utilizarse Vue/Nuxt si el equipo lo domina mejor.

## Backend

Para un equipo reducido:

```text
Python
FastAPI
SQLAlchemy
Alembic
Pydantic
```

Alternativas técnicamente válidas:

- NestJS;
- .NET;
- Spring Boot.

No mezclar stacks sin necesidad.

## Datos

```text
PostgreSQL
Redis
Object Storage compatible con S3
```

## Infraestructura

```text
Docker
Docker Compose para desarrollo
CI/CD
Reverse Proxy
HTTPS
Cloud / VPS inicialmente
```

## Evolución

Comenzar con modular monolith.

Dominios:

```text
auth
tenants
catalog
inventory
purchases
sales
payments
cash
billing
customers
reports
platform
notifications
integrations
```

Extraer servicios únicamente cuando métricas o escalabilidad lo justifiquen.

---

# 44. API

Estilo recomendado:

```text
/api/v1/
```

Ejemplo:

```text
POST   /api/v1/auth/login
GET    /api/v1/products
POST   /api/v1/products
GET    /api/v1/inventory/balances
POST   /api/v1/sales
POST   /api/v1/sales/{id}/refund
POST   /api/v1/cash-sessions/open
POST   /api/v1/cash-sessions/{id}/close
POST   /api/v1/invoices
GET    /api/v1/reports/sales
```

Requisitos:

- versionada;
- documentada;
- validación;
- paginación;
- filtros;
- ordenamiento;
- permisos;
- idempotencia;
- errores consistentes.

Formato de error:

```json
{
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "No existe inventario suficiente.",
    "details": {},
    "request_id": "..."
  }
}
```

---

# 45. WEBHOOKS

Preparar webhooks para:

```text
sale.completed
sale.refunded
inventory.low
inventory.adjusted
invoice.stamped
invoice.cancelled
payment.completed
payment.failed
settlement.completed
```

Requisitos:

- firma;
- secreto;
- reintentos;
- backoff;
- idempotencia;
- historial de entregas;
- dead letter / estado fallido.

---

# 46. COLAS Y PROCESOS ASÍNCRONOS

No ejecutar trabajos pesados en la misma solicitud que cobra una venta.

Utilizar background jobs para:

- emails;
- exportaciones;
- generación de reportes;
- notificaciones;
- sincronización;
- reintento de webhooks;
- tareas de facturación que lo permitan;
- conciliaciones;
- limpieza controlada.

---

# 47. CACHÉ

Redis podrá utilizarse para:

- rate limiting;
- sesiones según arquitectura;
- caché;
- locks distribuidos;
- colas;
- eventos temporales.

No utilizar Redis como única fuente permanente de una transacción comercial.

---

# 48. OBSERVABILIDAD

Implementar:

- logs estructurados;
- request ID;
- métricas;
- trazas cuando sea viable;
- health checks;
- alertas;
- dashboard de infraestructura.

Métricas:

```text
API latency
error rate
checkout failures
payment failures
invoice failures
database connections
queue depth
sync conflicts
active tenants
sales/minute
```

---

# 49. BACKUPS Y RECUPERACIÓN

Incluir:

- backup automático;
- retención;
- backup fuera del host principal;
- restauración probada;
- documentación;
- simulacro periódico.

Objetivos iniciales de referencia para MVP:

```text
RPO objetivo: <= 15 minutos cuando la infraestructura lo permita
RTO objetivo: <= 4 horas
```

Estos objetivos deberán ajustarse al presupuesto y criticidad real.

---

# 50. RENDIMIENTO

Definir presupuestos de rendimiento.

Objetivos iniciales:

- agregar producto al carrito: percepción inmediata;
- búsqueda local/cacheada: prácticamente instantánea;
- endpoints comunes online: P95 bajo carga normal dentro de un rango objetivo definido por pruebas;
- confirmar venta: sin bloqueos innecesarios;
- dashboard: carga progresiva;
- reportes pesados: asíncronos.

No declarar rendimiento únicamente por intuición.

Medir.

---

# 51. UX / UI

Identidad:

- moderna;
- clara;
- confiable;
- limpia;
- rápida.

Paleta base sugerida:

```text
Blanco
Gris claro
Azul
Verde
```

Estados:

```text
Verde    → correcto
Azul     → información
Amarillo → advertencia
Rojo     → error / acción peligrosa
Gris     → inactivo
```

Principios:

- botones grandes en POS;
- contraste accesible;
- soporte de teclado;
- navegación consistente;
- tablas densas en escritorio;
- tarjetas en móvil;
- confirmación para acciones destructivas;
- mostrar primero lo importante;
- skeleton/loading states;
- estados vacíos útiles;
- mensajes de error accionables.

---

# 52. PANTALLAS PRINCIPALES

Crear como mínimo:

1. Login.
2. Recuperar acceso.
3. Registro.
4. Onboarding.
5. Inicio / Dashboard.
6. POS.
7. Cobro.
8. Ventas.
9. Detalle de venta.
10. Devolución.
11. Productos.
12. Nuevo producto.
13. Inventario.
14. Kardex.
15. Ajustes.
16. Conteos.
17. Transferencias.
18. Compras.
19. Proveedores.
20. Clientes.
21. Cajas.
22. Corte.
23. Facturación.
24. Reportes.
25. Usuarios.
26. Roles.
27. Sucursales.
28. Almacenes.
29. Configuración.
30. Plan / cobros POINT.
31. Centro de notificaciones.
32. Soporte.

---

# 53. ACCESIBILIDAD

Aplicar buenas prácticas de accesibilidad:

- etiquetas;
- foco visible;
- navegación por teclado;
- contraste;
- mensajes no dependientes únicamente de color;
- áreas táctiles adecuadas;
- texto escalable.

---

# 54. PRUEBAS

## Unitarias

Para reglas de:

- impuestos;
- precios;
- promociones;
- comisión;
- inventario;
- devoluciones;
- caja.

## Integración

- DB;
- inventario;
- venta;
- pago;
- factura;
- devolución.

## E2E

Escenarios completos.

## Seguridad

- permisos;
- tenant isolation;
- autenticación;
- endpoints sensibles.

## Concurrencia

Ejemplo:

```text
Stock = 1

Caja A intenta vender 1
Caja B intenta vender 1
```

El resultado debe cumplir la política configurada sin corrupción de datos.

## Idempotencia

Enviar dos veces el mismo checkout.

Resultado:

```text
1 sola venta
1 solo pago
1 solo conjunto de movimientos
```

---

# 55. CASOS DE ACEPTACIÓN CRÍTICOS

## Venta normal

```gherkin
Given una caja abierta
And un producto con stock suficiente
When el cajero agrega el producto
And confirma un pago
Then se crea exactamente una venta
And se registra el pago
And disminuye el inventario
And se genera el movimiento de Kardex
And se genera el fee POINT si aplica
And se genera el ticket
```

## Venta sin stock

```gherkin
Given allow_negative_stock = false
And el producto no tiene existencia suficiente
When se intenta confirmar la venta
Then la venta no se confirma
And no se captura el pago
And el inventario no queda inconsistente
```

## Devolución parcial

```gherkin
Given una venta confirmada de 5 unidades
When se devuelven 2
Then la venta original permanece
And se crea una devolución por 2
And se ajusta inventario según condición
And se ajusta el pago/reembolso
And se ajusta el fee correspondiente
```

## Aislamiento SaaS

```gherkin
Given Usuario A pertenece a Tenant A
When solicita un recurso de Tenant B
Then el sistema responde como no autorizado/no disponible
And no revela información sensible
```

---

# 56. POLÍTICAS DE CÓDIGO

- código limpio;
- nombres consistentes;
- tipado cuando sea posible;
- módulos pequeños;
- separación de responsabilidades;
- evitar duplicación;
- migrations;
- tests;
- lint;
- formatter;
- documentación;
- `.env.example`;
- nunca subir secretos;
- manejo centralizado de errores.

No entregar únicamente prototipos visuales simulados cuando una fase solicite funcionalidad real.

---

# 57. DOCUMENTACIÓN OBLIGATORIA

Mantener:

```text
README.md
ARCHITECTURE.md
DATABASE.md
API.md
SECURITY.md
DEPLOYMENT.md
CHANGELOG.md
```

Además:

- OpenAPI;
- diagrama de arquitectura;
- ERD;
- variables de entorno;
- backup/restore;
- guía de desarrollo;
- guía de despliegue.

---

# 58. ESTRUCTURA DE PROYECTO SUGERIDA

```text
point-todo-en-uno/
│
├── apps/
│   ├── web/
│   └── api/
│
├── packages/
│   └── shared/
│
├── infrastructure/
│   ├── docker/
│   ├── nginx/
│   └── scripts/
│
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── database/
│   └── phases/
│
├── tests/
│
├── docker-compose.yml
├── .env.example
├── README.md
└── CHANGELOG.md
```

Adaptar al stack elegido sin perder separación.

---

# 59. FASES DE DESARROLLO

Cada fase deberá terminar en un estado funcional, documentado y comprobable.

---

## FASE 00 — Descubrimiento y definición

### Objetivo

Cerrar decisiones fundamentales antes de programar.

### Definir

- mercado inicial;
- vertical inicial;
- MVP;
- pricing;
- política de stock;
- offline;
- facturación;
- hardware;
- proveedores externos;
- métricas.

### Entregables

- PRD;
- RF;
- RNF;
- reglas de negocio;
- mapa de módulos;
- casos de uso;
- backlog;
- ERD inicial;
- riesgos;
- criterios de aceptación.

---

## FASE 01 — UX/UI y Design System

### Construir

- navegación;
- layout;
- componentes;
- paleta;
- tipografía;
- responsive;
- prototipo.

### Diseñar primero

- onboarding;
- POS;
- cobro;
- inventario;
- producto;
- caja;
- dashboard.

### Entregables

- Design System;
- wireframes;
- prototipo;
- vistas desktop/tablet/mobile.

---

## FASE 02 — Fundación técnica SaaS

### Implementar

- repositorio;
- frontend;
- backend;
- PostgreSQL;
- migrations;
- Docker;
- configuración;
- CI inicial;
- healthcheck;
- logs.

### Entregables

- proyecto ejecutable;
- documentación;
- entorno local reproducible.

---

## FASE 03 — Autenticación, tenants y permisos

### Implementar

- registro;
- login;
- recuperación;
- tenant;
- sucursal;
- usuarios;
- roles;
- permisos;
- auditoría.

### Prueba obligatoria

Aislamiento entre tenants.

---

## FASE 04 — Catálogo

### Implementar

- productos;
- servicios;
- categorías;
- variantes;
- códigos;
- precios;
- impuestos;
- importación.

---

## FASE 05 — Inventario

### Implementar

- balances;
- movimientos;
- Kardex;
- entradas;
- salidas;
- ajustes;
- conteos;
- transferencias;
- alertas.

---

## FASE 06 — POS

### Implementar

- búsqueda;
- escáner;
- carrito;
- cliente;
- descuentos;
- impuestos;
- hold;
- checkout;
- ticket;
- historial.

### Obligatorio

Checkout transaccional e idempotente.

---

## FASE 07 — Cajas y pagos

### Implementar

- apertura;
- fondo;
- pagos;
- pagos mixtos;
- cambio;
- retiros;
- entradas;
- corte;
- cierre;
- diferencias.

---

## FASE 08 — Proveedores y compras

### Implementar

- proveedores;
- órdenes;
- recepciones;
- compras;
- costos;
- devoluciones a proveedor.

---

## FASE 09 — Clientes, devoluciones y promociones

### Implementar

- clientes;
- perfiles fiscales;
- devoluciones;
- reembolsos;
- promociones;
- descuentos;
- políticas.

---

## FASE 10 — Facturación México

### Implementar

- capa de proveedor/PAC;
- configuración fiscal;
- emisión;
- XML;
- PDF;
- estados;
- cancelación;
- factura global;
- trazabilidad;
- reintentos.

### Obligatorio

No acoplar POS directamente a un PAC concreto.

---

## FASE 11 — Pricing y monetización POINT

### Implementar

- planes;
- fee configurable;
- liquidaciones;
- ajustes;
- panel comercio;
- panel plataforma.

---

## FASE 12 — Dashboard y reportes

### Implementar

- KPIs;
- reportes;
- gráficas;
- filtros;
- exportación;
- consultas optimizadas.

---

## FASE 13 — PWA, periféricos y contingencia

### Implementar

- manifest;
- service worker;
- impresión;
- escáner;
- adaptadores;
- caché;
- cola offline;
- sync;
- conflictos.

---

## FASE 14 — Seguridad, QA y hardening

### Ejecutar

- pruebas;
- concurrencia;
- load tests;
- tenant tests;
- restore test;
- security review;
- dependency scan;
- observabilidad;
- alertas.

---

## FASE 15 — Piloto

Lanzar con pocas PyMEs reales.

Medir:

- tiempo para primera venta;
- tiempo por venta;
- errores;
- tickets;
- sincronización;
- diferencias de caja;
- errores de stock;
- fallas de facturación;
- soporte;
- churn temprano;
- activación;
- uso por módulo.

---

## FASE 16 — Producción V1

### Entregables

- infraestructura;
- dominio;
- HTTPS;
- CI/CD;
- backups;
- monitoreo;
- documentación;
- onboarding;
- soporte;
- versión 1.0.

---

# 60. MVP OBLIGATORIO

El MVP deberá incluir:

- registro;
- login;
- tenant;
- sucursales;
- usuarios;
- roles;
- productos;
- categorías;
- precios;
- impuestos básicos configurables;
- códigos de barras;
- inventario;
- Kardex;
- ajustes;
- POS;
- venta;
- pagos;
- ticket;
- caja;
- clientes básicos;
- devoluciones básicas;
- dashboard;
- reportes;
- auditoría;
- backups;
- responsive.

Facturación podrá incorporarse dentro del MVP si el mercado de lanzamiento la requiere como condición comercial.

---

# 61. FUNCIONES POST-MVP

## Comercial

- puntos;
- monedero;
- crédito;
- apartados;
- promociones avanzadas;
- precios B2B.

## Omnicanal

- ecommerce;
- marketplaces;
- catálogo online;
- pedidos;
- pickup.

## Administración

- cuentas por cobrar;
- cuentas por pagar;
- gastos;
- conciliación.

## Inteligencia

- pronóstico de ventas;
- sugerencias de compra;
- detección de anomalías;
- riesgo de agotado;
- clasificación ABC;
- productos relacionados;
- recomendaciones.

## Verticales

- restaurante;
- cafetería;
- farmacia;
- taller;
- salón;
- mayoreo.

---

# 62. MÉTRICAS DEL SaaS

Medir:

- tenants registrados;
- tenants activos;
- tiempo hasta primera venta;
- usuarios activos;
- sucursales activas;
- GMV;
- ventas procesadas;
- tickets;
- fee POINT;
- MRR cuando aplique;
- ARPU;
- activación;
- retención;
- churn;
- fallos de checkout;
- fallos de facturación;
- uptime;
- latencia.

---

# 63. MÉTRICAS DEL COMERCIO

- ventas;
- unidades;
- tickets;
- ticket promedio;
- costo;
- margen;
- inventario;
- rotación;
- stockouts;
- compras;
- devoluciones;
- ventas por usuario;
- ventas por sucursal;
- ventas por método;
- descuentos;
- diferencias de caja.

---

# 64. DEFINITION OF DONE

Una funcionalidad no está terminada porque “se ve”.

Debe cumplir:

```text
[ ] Diseño aprobado
[ ] Backend real
[ ] Persistencia real
[ ] Permisos
[ ] Tenant isolation
[ ] Validación
[ ] Manejo de errores
[ ] Auditoría cuando aplique
[ ] Tests
[ ] Responsive
[ ] Loading states
[ ] Empty states
[ ] Documentación
[ ] Migration
[ ] Sin secretos
[ ] Criterios de aceptación
```

---

# 65. REGLAS PARA CADA FASE QUE SE SOLICITE A LA IA

Cuando el usuario diga:

> “Continúa con la Fase X”

deberás:

1. Revisar la arquitectura y código existentes antes de modificar.
2. Mantener compatibilidad con fases anteriores.
3. No eliminar funcionalidad que ya sirve.
4. Crear migrations en lugar de modificar la base sin control.
5. Implementar frontend y backend reales cuando la fase lo requiera.
6. Integrar la funcionalidad con autenticación y permisos.
7. Integrar tenant y sucursal.
8. Incluir validaciones.
9. Incluir manejo de errores.
10. Incluir pruebas relevantes.
11. Actualizar documentación.
12. Actualizar `.env.example` si aparecen variables.
13. Actualizar `CHANGELOG.md`.
14. Entregar instrucciones de ejecución.
15. Indicar claramente qué quedó implementado y qué permanece pendiente.
16. No sustituir módulos funcionales por mocks salvo que el objetivo de la fase sea explícitamente prototipado.
17. No hardcodear credenciales ni secretos.
18. No utilizar datos de producción en pruebas.
19. Mantener consistencia de estilos.
20. Evitar reescrituras innecesarias del proyecto.

---

# 66. FORMATO DE ENTREGA DE CADA FASE

Cada fase deberá incluir:

## 1. Resumen

Qué se construyó.

## 2. Arquitectura

Qué módulos fueron agregados o modificados.

## 3. Base de datos

- tablas;
- campos;
- migrations;
- índices.

## 4. Backend

- endpoints;
- servicios;
- reglas;
- permisos.

## 5. Frontend

- páginas;
- componentes;
- flujos.

## 6. Seguridad

Controles implementados.

## 7. Pruebas

Qué escenarios fueron cubiertos.

## 8. Instrucciones

Cómo ejecutar/probar.

## 9. Criterios de aceptación

Checklist verificable.

## 10. Pendientes

Qué queda para fases posteriores.

---

# 67. REGLAS DE NEGOCIO ESENCIALES

```text
RN-01
Una venta confirmada no se elimina físicamente.

RN-02
Toda venta que controla inventario genera movimientos.

RN-03
Toda devolución referencia una venta.

RN-04
Todo ajuste de inventario requiere motivo.

RN-05
Toda operación pertenece a un tenant.

RN-06
Toda operación física pertenece a una sucursal cuando aplique.

RN-07
Todo pago pertenece a una venta o documento financiero válido.

RN-08
Una reejecución idempotente no duplica transacciones.

RN-09
El frontend nunca es autoridad final de precios/totales.

RN-10
El porcentaje de fee se guarda históricamente.

RN-11
Los impuestos aplicados se conservan históricamente.

RN-12
Una orden de compra no incrementa stock hasta la recepción.

RN-13
Una transferencia no incrementa destino antes de recepción.

RN-14
Una diferencia de caja nunca se oculta.

RN-15
Los CFDI no sustituyen el historial interno de ventas.

RN-16
Los tickets internos y documentos fiscales son objetos relacionados pero diferentes.

RN-17
Los permisos se validan en backend.

RN-18
Un usuario no puede cambiar su tenant mediante parámetros del cliente.

RN-19
No se almacenan datos completos de tarjetas sin una arquitectura especializada y cumplimiento aplicable.

RN-20
Los procesos sensibles generan auditoría.
```

---

# 68. REQUERIMIENTOS NO FUNCIONALES

## Disponibilidad

Diseñar para alta disponibilidad razonable según etapa.

## Escalabilidad

Permitir crecimiento horizontal de frontend/API cuando sea necesario.

## Mantenibilidad

Monolito modular bien separado.

## Portabilidad

Docker.

## Seguridad

Defense in depth.

## Auditoría

Eventos sensibles trazables.

## Rendimiento

Medido mediante pruebas.

## Recuperación

Backups y restore probado.

## Usabilidad

Una persona no técnica debe aprender operaciones básicas rápidamente.

---

# 69. RIESGOS QUE DEBEN CONTROLARSE

1. Mezclar datos entre tenants.
2. Duplicar ventas por reintentos.
3. Duplicar pagos.
4. Inventario negativo accidental.
5. Conflictos offline.
6. Eliminar historial.
7. Aplicar precios incorrectos.
8. Hardcodear impuestos.
9. Hardcodear comisión.
10. Dependencia excesiva de un PAC.
11. Dependencia excesiva de una terminal.
12. Bloquear el POS por reportes.
13. No poder restaurar backups.
14. Filtrar datos sensibles en logs.
15. Crear demasiados microservicios para un equipo pequeño.
16. Crear una UI bonita pero lenta para cobrar.
17. Facturación acoplada a la venta de forma que una falla fiscal impida conservar la operación comercial.
18. No distinguir pagos, ventas y documentos fiscales.
19. No probar concurrencia.
20. No probar aislamiento multiempresa.

---

# 70. CRITERIO DE ÉXITO DEL PRODUCTO

POINT será exitoso técnicamente cuando una PyME pueda:

```text
1. Registrarse.
2. Configurar su negocio.
3. Importar productos.
4. Abrir caja.
5. Vender.
6. Cobrar.
7. Imprimir/enviar ticket.
8. Actualizar inventario automáticamente.
9. Realizar compras.
10. Revisar caja.
11. Consultar reportes.
12. Facturar cuando corresponda.
13. Administrar empleados y permisos.
14. Operar varias sucursales.
```

sin depender de hojas de cálculo externas para su operación cotidiana básica.

---

# 71. RESULTADO FINAL ESPERADO

```text
                     POINT TODO EN UNO
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
       VENTA             OPERACIÓN         ADMINISTRACIÓN
        │                   │                   │
     ┌──┴──┐       ┌────────┼────────┐     ┌────┼─────────┐
     │     │       │        │        │     │    │         │
    POS  PAGOS  INVENTARIO COMPRAS CAJA  USERS REPORTES FACTURA
     │     │       │        │        │     │    │         │
     └─────┴───────┴────────┴────────┴─────┴────┴─────────┘
                            │
                       POSTGRESQL
                            │
                AUDITORÍA + SEGURIDAD
                            │
                API + INTEGRACIONES
```

POINT deberá diferenciarse por:

1. **Rapidez de operación.**
2. **Facilidad de uso.**
3. **Inventario confiable.**
4. **Adaptación al mercado mexicano.**
5. **Facturación desacoplada e integrable.**
6. **Multiempresa y multisucursal.**
7. **Trazabilidad completa.**
8. **Uso multiplataforma.**
9. **Arquitectura simple de operar pero preparada para crecer.**
10. **Modelo SaaS configurable.**

---

# 72. INSTRUCCIÓN FINAL

No construyas POINT como una colección de pantallas CRUD independientes.

Constrúyelo como un **sistema transaccional de operación comercial** donde:

```text
VENTA
  ↓
PAGO
  ↓
INVENTARIO
  ↓
CAJA
  ↓
CLIENTE
  ↓
FEE / PLAN
  ↓
FACTURACIÓN
  ↓
REPORTES
  ↓
AUDITORÍA
```

estén correctamente relacionados.

Prioriza siempre:

```text
CORRECTITUD
→ TRAZABILIDAD
→ SEGURIDAD
→ RAPIDEZ OPERATIVA
→ FACILIDAD DE USO
→ ESCALABILIDAD
```

Si existe un conflicto entre “hacerlo rápido” y “proteger la integridad de una transacción”, debe prevalecer la integridad de la operación.

# **POINT TODO EN UNO**
### **Vende, cobra, factura, controla y administra tu negocio desde un solo lugar.**

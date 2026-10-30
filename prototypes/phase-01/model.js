/* Reglas exclusivas del prototipo. No sustituyen la validación del servidor. */
globalThis.PointDemo = (() => {
  'use strict';
  const products = [
    { id: 'p1', name: 'Café de especialidad', detail: 'Molido · Bolsa 250 g', category: 'Despensa', sku: 'CAF-001', barcode: '7501000000011', price: 12900, stock: 24, min: 5, unit: 'pieza', tax: 0, art: 'coffee', color: 'sand' },
    { id: 'p2', name: 'Leche de avena', detail: 'Natural · 1 litro', category: 'Bebidas', sku: 'BEB-002', barcode: '7501000000028', price: 4200, stock: 18, min: 5, unit: 'pieza', tax: 0, art: 'milk', color: 'blue' },
    { id: 'p3', name: 'Pan artesanal', detail: 'Masa madre · 500 g', category: 'Panadería', sku: 'PAN-003', barcode: '7501000000035', price: 6500, stock: 8, min: 4, unit: 'pieza', tax: 0, art: 'bread', color: 'peach' },
    { id: 'p4', name: 'Mermelada de fresa', detail: 'Frasco · 250 g', category: 'Despensa', sku: 'DES-004', barcode: '7501000000042', price: 7800, stock: 12, min: 4, unit: 'pieza', tax: 0, art: 'jar', color: 'rose' },
    { id: 'p5', name: 'Agua mineral', detail: 'Botella · 600 ml', category: 'Bebidas', sku: 'BEB-005', barcode: '7501000000059', price: 2200, stock: 32, min: 8, unit: 'pieza', tax: 0.16, art: 'bottle', color: 'mint' },
    { id: 'p6', name: 'Galletas de avena', detail: 'Paquete · 180 g', category: 'Panadería', sku: 'PAN-006', barcode: '7501000000066', price: 3800, stock: 3, min: 5, unit: 'pieza', tax: 0, art: 'cookies', color: 'sand' },
    { id: 'p7', name: 'Chocolate oscuro', detail: '70% cacao · 100 g', category: 'Despensa', sku: 'DES-007', barcode: '7501000000073', price: 5600, stock: 15, min: 5, unit: 'pieza', tax: 0, art: 'chocolate', color: 'lilac' },
    { id: 'p8', name: 'Té verde', detail: 'Caja · 20 sobres', category: 'Bebidas', sku: 'BEB-008', barcode: '7501000000080', price: 4900, stock: 0, min: 4, unit: 'pieza', tax: 0, art: 'tea', color: 'mint' },
    { id: 'p9', name: 'Envoltura de regalo', detail: 'Servicio · por paquete', category: 'Servicios', sku: 'SER-009', barcode: '7501000000097', price: 2500, stock: null, min: 0, unit: 'servicio', tax: 0.16, art: 'gift', color: 'peach' },
  ];
  const seed = () => ({
    version: 1,
    business: { name: 'La Esquina', branch: 'Sucursal Centro', owner: 'Andrea', type: 'Tienda de productos y servicios', ticket: '¡Gracias por comprar local!' },
    products: structuredClone(products), cart: [], held: [], discount: 0, customer: '', notes: '',
    cash: { open: true, fund: 50000, entries: [], closed: null, session: 'demo-initial' },
    sales: [], movements: [], onboardingStep: 1,
  });
  const cents = (value) => {
    const text = String(value).trim();
    if (!/^\d{1,8}(?:\.\d{1,2})?$/.test(text)) return null;
    const [whole, decimals = ''] = text.split('.');
    return Number(whole) * 100 + Number(decimals.padEnd(2, '0'));
  };
  const money = value => new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(value / 100);
  function totals(state) {
    const lines = state.cart.map(item => {
      const product = state.products.find(p => p.id === item.id);
      return { ...item, product, gross: product.price * item.qty };
    });
    const gross = lines.reduce((sum, line) => sum + line.gross, 0);
    const discount = Math.round(gross * state.discount / 100);
    let allocated = 0;
    for (const [index, line] of lines.entries()) {
      line.discount = index === lines.length - 1 ? discount - allocated : Math.round(discount * line.gross / Math.max(gross, 1));
      allocated += line.discount;
      line.total = line.gross - line.discount;
      line.tax = Math.round(line.total - line.total / (1 + line.product.tax));
    }
    const total = gross - discount;
    const tax = lines.reduce((sum, line) => sum + line.tax, 0);
    return { lines, gross, discount, total, tax, subtotal: total - tax, count: state.cart.reduce((sum, item) => sum + item.qty, 0) };
  }
  const cashExpected = state => state.cash.fund + state.sales.filter(s => s.session === state.cash.session && s.method === 'cash').reduce((sum, sale) => sum + sale.total, 0) + state.cash.entries.reduce((sum, movement) => sum + movement.amount, 0);
  function addItem(state, id, delta = 1) {
    const product = state.products.find(p => p.id === id);
    if (!product) return 'No encontramos ese producto.';
    const existing = state.cart.find(item => item.id === id);
    const quantity = (existing?.qty || 0) + delta;
    if (quantity > 999) return 'El máximo de la demostración es de 999 unidades.';
    if (product.stock !== null && quantity > product.stock) return `Solo hay ${product.stock} unidades disponibles.`;
    if (quantity <= 0) state.cart = state.cart.filter(item => item.id !== id);
    else if (existing) existing.qty = quantity;
    else state.cart.push({ id, qty: quantity });
    return null;
  }
  function completeSale(state, method, received) {
    if (!state.cash.open) return { error: 'Abre una caja antes de cobrar.' };
    if (!state.cart.length) return { error: 'Agrega un producto para continuar.' };
    if (!['cash', 'card', 'transfer'].includes(method)) return { error: 'Elige una forma de pago.' };
    const summary = totals(state);
    if (method === 'cash' && (received === null || received < summary.total)) return { error: 'El efectivo recibido debe cubrir el total.' };
    for (const line of summary.lines) if (line.product.stock !== null && line.qty > line.product.stock) return { error: `Revisa la existencia de ${line.product.name}.` };
    const sale = {
      id: `DEMO-${String(state.sales.length + 1).padStart(4, '0')}`, total: summary.total,
      subtotal: summary.subtotal, tax: summary.tax, discount: summary.discount, method,
      received: method === 'cash' ? received : summary.total, change: method === 'cash' ? received - summary.total : 0,
      customer: state.customer || 'Público en general', notes: state.notes,
      items: summary.lines.map(line => ({ name: line.product.name, qty: line.qty, total: line.total })),
      createdAt: new Date().toISOString(), session: state.cash.session,
      business: structuredClone(state.business),
    };
    for (const line of summary.lines) if (line.product.stock !== null) {
      line.product.stock -= line.qty;
      state.movements.unshift({ id: `m-${Date.now()}-${line.id}`, productId: line.id, label: `Venta de prueba · ${sale.id}`, quantity: -line.qty, after: line.product.stock, createdAt: sale.createdAt });
    }
    state.sales.unshift(sale); state.cart = []; state.discount = 0; state.customer = ''; state.notes = '';
    return { sale };
  }
  return { seed, cents, money, totals, addItem, completeSale, cashExpected };
})();

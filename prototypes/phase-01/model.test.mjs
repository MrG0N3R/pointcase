import test from 'node:test';
import assert from 'node:assert/strict';
import './model.js';
const D = globalThis.PointDemo;

test('importes: centavos exactos y rechazo de formatos ambiguos', () => {
  assert.equal(D.cents('237.05'), 23705);
  assert.equal(D.cents('0.1'), 10);
  for (const value of ['-1', '1,000.00', '1.001', '', 'NaN']) assert.equal(D.cents(value), null);
});
test('venta de ejemplo: cambio, stock, caja e histórico coordinados', () => {
  const state = D.seed();
  D.addItem(state, 'p1'); D.addItem(state, 'p3');
  const result = D.completeSale(state, 'cash', 50000);
  assert.equal(result.sale.total, 19400);
  assert.equal(result.sale.change, 30600);
  assert.equal(state.products.find(p => p.id === 'p1').stock, 23);
  assert.equal(state.products.find(p => p.id === 'p3').stock, 7);
  assert.equal(D.cashExpected(state), 69400);
  assert.equal(state.movements.length, 2);
  assert.equal(state.cart.length, 0);
  assert(D.completeSale(state, 'cash', 50000).error);
  assert.equal(state.sales.length, 1);
  state.products.find(p => p.id === 'p1').name = 'Nombre cambiado';
  assert.equal(result.sale.items[0].name, 'Café de especialidad');
});
test('efectivo insuficiente o caja cerrada no cambia inventario ni ventas', () => {
  const state = D.seed(); D.addItem(state, 'p1');
  const before = JSON.stringify(state);
  assert(D.completeSale(state, 'cash', 1000).error);
  assert.equal(JSON.stringify(state), before);
  state.cash.open = false;
  assert(D.completeSale(state, 'cash', 50000).error);
  assert.equal(state.sales.length, 0);
});
test('el catálogo de prueba bloquea agotados y cantidades sobre la existencia', () => {
  const state = D.seed();
  assert(D.addItem(state, 'p8'));
  assert.equal(D.addItem(state, 'p6', 3), null);
  assert(D.addItem(state, 'p6'));
  assert.equal(state.cart.find(item => item.id === 'p6').qty, 3);
  state.products.find(p => p.id === 'p6').stock = 2;
  assert(D.completeSale(state, 'card', null).error);
  assert.equal(state.sales.length, 0);
});
test('servicio e impuesto incluido concilian sin movimiento de mercancía', () => {
  const state = D.seed(); D.addItem(state, 'p9', 2); state.discount = 10;
  const t = D.totals(state);
  assert.equal(t.total, 4500);
  assert.equal(t.subtotal + t.tax, t.total);
  assert.equal(t.lines.reduce((sum, line) => sum + line.total, 0), t.total);
  const result = D.completeSale(state, 'card', null);
  assert.equal(result.sale.total, 4500);
  assert.equal(state.movements.length, 0);
  assert.equal(D.cashExpected(state), 50000);
});
test('un turno nuevo no vuelve a sumar ventas del anterior', () => {
  const state = D.seed(); D.addItem(state, 'p1'); D.completeSale(state, 'cash', 20000);
  state.cash = { open: true, fund: 10000, session: 'otro-turno', entries: [{ amount: 5000 }] };
  assert.equal(D.cashExpected(state), 15000);
});

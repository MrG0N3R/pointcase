import { useEffect, useState, type ReactNode } from 'react';
import { loadConnection, type ConnectionState } from './api';

const icons: Record<string, ReactNode> = {
  home: <><path d="m3 10 9-7 9 7v10H15v-7H9v7H3z" /></>,
  sell: <><rect x="3" y="3" width="18" height="18" rx="3" /><path d="M3 9h18M9 9v12M13 13h4m-4 4h4" /></>,
  box: <><path d="m3 7 9-4 9 4-9 4zM3 7v10l9 4 9-4V7M12 11v10" /></>,
  layers: <path d="m3 7 9-4 9 4-9 4zm0 5 9 4 9-4M3 17l9 4 9-4" />,
  cash: <><rect x="3" y="5" width="18" height="15" rx="2" /><path d="M3 10h18m-6 5h3M7 2v5" /></>,
  arrow: <path d="M4 12h16m-6-6 6 6-6 6" />,
  check: <path d="m5 12 4 4L19 6" />,
  clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
  link: <><path d="m8 8 3-3a5 5 0 0 1 7 7l-3 3M9 9l-3 3a5 5 0 0 0 7 7l3-3m-7-1 6-6" /></>,
  settings: <><circle cx="12" cy="12" r="4" /><path d="M12 2v3m0 14v3M2 12h3m14 0h3M5 5l2 2m10 10 2 2M5 19l2-2M17 7l2-2" /></>,
  menu: <path d="M4 6h16M4 12h16M4 18h16" />,
  info: <><circle cx="12" cy="12" r="9" /><path d="M12 11v6m0-10h.01" /></>,
};
function Icon({ name }: { name: string }) { return <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{icons[name] || icons.box}</svg>; }
const sections = [
  { id: 'inicio', name: 'Inicio', icon: 'home', title: 'Tu negocio, en un solo lugar', phase: 2 },
  { id: 'vender', name: 'Punto de venta', icon: 'sell', title: 'Un mostrador que trabaja contigo', phase: 6 },
  { id: 'productos', name: 'Productos', icon: 'box', title: 'Un lugar para todo lo que vendes', phase: 4 },
  { id: 'inventario', name: 'Inventario', icon: 'layers', title: 'Cada pieza, bajo control', phase: 5 },
  { id: 'caja', name: 'Caja', icon: 'cash', title: 'Tu caja, con cuentas claras', phase: 7 },
  { id: 'configuracion', name: 'Configuración', icon: 'settings', title: 'Un espacio a la medida de tu negocio', phase: 3 },
];
function currentRoute() { const value = window.location.hash.slice(1); return value === 'estado' || sections.some(item => item.id === value) ? value : 'inicio'; }
function AppLink({ to, children, className = '' }: { to: string; children: ReactNode; className?: string }) { return <a href={`#${to}`} className={className}>{children}</a>; }

export function App() {
  const [route, setRoute] = useState(currentRoute);
  const [menu, setMenu] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const [connection, setConnection] = useState<ConnectionState>({ loading: true, metadata: null, health: null, requestId: null, error: null });
  useEffect(() => {
    const navigate = () => { setRoute(currentRoute()); setMenu(false); requestAnimationFrame(() => document.querySelector<HTMLElement>('#content')?.focus()); window.scrollTo(0, 0); };
    window.addEventListener('hashchange', navigate); return () => window.removeEventListener('hashchange', navigate);
  }, []);
  useEffect(() => {
    const controller = new AbortController();
    const timer = window.setTimeout(() => controller.abort(new Error('La comprobación tardó demasiado. Intenta de nuevo.')), 7000);
    let active = true;
    setConnection(previous => ({ ...previous, loading: true, error: null }));
    loadConnection(controller.signal).then(data => { if (active) setConnection({ ...data, loading: false }); })
      .catch(() => { if (active) setConnection({ metadata: null, health: null, requestId: null, loading: false, error: 'No pudimos conectar con POINT. Comprueba que los servicios estén iniciados e intenta de nuevo.' }); })
      .finally(() => window.clearTimeout(timer));
    return () => { active = false; window.clearTimeout(timer); controller.abort(); };
  }, [attempt]);
  const ready = connection.health?.status === 'ok';
  const section = sections.find(item => item.id === route);
  useEffect(() => { document.title = `POINT · ${section?.name || 'Conexión'}`; }, [section?.name]);
  const retry = () => setAttempt(value => value + 1);
  const prototypeLink = <a className="button secondary" href="/diseno/" target="_blank" rel="noreferrer">Explorar diseño aprobado <Icon name="arrow" /></a>;
  const connectionLabel = connection.loading ? 'Comprobando conexión' : ready ? 'Conexión disponible' : 'Revisar conexión';
  return <>
    <a className="skip-link" href="#content" onClick={event => { event.preventDefault(); document.querySelector<HTMLElement>('#content')?.focus(); }}>Saltar al contenido</a>
    <div className={`workspace ${menu ? 'menu-open' : ''}`}>
      <aside className="sidebar" aria-label="Navegación principal">
        <AppLink to="inicio" className="brand">point<span>●</span><small>TODO EN UNO</small></AppLink>
        <div className="business-card"><span className="business-avatar">P</span><div><strong>Tu próximo negocio</strong><small>Espacio por configurar</small></div></div>
        <span className="nav-label">TU OPERACIÓN</span>
        <nav>{sections.filter(item => item.id !== 'configuracion').map(item => <a key={item.id} href={`#${item.id}`} aria-label={item.name} aria-current={route === item.id ? 'page' : undefined} className={`nav-item ${route === item.id ? 'active' : ''}`}><Icon name={item.icon} /><span>{item.name}</span>{route === item.id && <i />}</a>)}</nav>
        <div className="sidebar-bottom"><div className="phase-card"><span className="phase-dot" /> En desarrollo<p>Una base para crecer<br />con cada negocio.</p><a href="/diseno/" target="_blank" rel="noreferrer">Ver diseño aprobado <Icon name="arrow" /></a></div><a href="#configuracion" aria-label="Configuración" className={`nav-item ${route === 'configuracion' ? 'active' : ''}`}><Icon name="settings" /><span>Configuración</span></a><a href="#estado" aria-label="Estado de conexión" className={`nav-item ${route === 'estado' ? 'active' : ''}`}><Icon name="link" /><span>Estado de conexión</span></a></div>
      </aside>
      {menu && <button className="menu-scrim" onClick={() => setMenu(false)} aria-label="Cerrar menú" />}
      <div className="main-shell">
        <header className="topbar"><div className="topbar-start"><button className="icon-button menu-toggle" onClick={() => setMenu(!menu)} aria-label={menu ? 'Cerrar menú principal' : 'Abrir menú'} aria-expanded={menu}><Icon name="menu" /></button><span className="breadcrumb">Mi negocio <span>/</span><strong>{section?.name || 'Conexión'}</strong></span></div><AppLink to="estado" className={`connection-pill ${ready ? 'online' : ''}`}><span className={connection.loading ? 'pulse' : ''} />{connectionLabel}</AppLink></header>
        <div className="demo-strip"><Icon name="info" /><span><strong>Entorno de desarrollo</strong> · Aún no habilitado para ventas reales.</span></div>
        <main id="content" tabIndex={-1} className="main-content foundation-content">
          <div className="page-heading"><div><div className="eyebrow">POINT / TODO EN UNO</div><h1>{section?.title || 'Conexión de POINT'}</h1><p>{route === 'estado' ? 'Comprueba que tu espacio pueda comunicarse correctamente.' : 'Más claridad para operar. Más tiempo para hacer crecer tu negocio.'}</p></div>{prototypeLink}</div>
          {(connection.error || (!connection.loading && !ready)) && <div className="connection-error" role="alert"><Icon name="info" /><div><strong>La conexión necesita atención</strong><p>{connection.error || 'El servidor responde, pero los datos o sus actualizaciones todavía no están listos.'}</p></div><button className="button secondary" onClick={retry}>Reintentar</button></div>}
          {route === 'estado' ? <>
            <section className="panel status-panel" aria-busy={connection.loading}><div className="panel-heading"><div><h2>Todo empieza con una buena conexión</h2><p>Este estado se consulta al servidor, sin datos de ejemplo.</p></div><button className="button secondary" onClick={retry} disabled={connection.loading}>Comprobar de nuevo</button></div>
              {connection.loading ? <div className="status-loading" role="status"><div className="skeleton" /><div className="skeleton" /><p>Comprobando servicios…</p></div> : <div className="status-list">{[['Aplicación web', true], ['Comunicación con el servidor', !!connection.metadata], ['Conexión con los datos', !!connection.health?.checks.database], ['Actualizaciones de los datos', !!connection.health?.checks.migrations]].map(([label, ok]) => <div className="service-row" key={String(label)}><span className={`service-icon ${ok ? 'good' : ''}`}><Icon name={ok ? 'check' : 'clock'} /></span><strong>{label}</strong><span className={`badge ${ok ? 'success' : 'warning'}`}>{ok ? 'Disponible' : 'Por revisar'}</span></div>)}</div>}
              <details className="technical-details"><summary>Detalles para la revisión técnica</summary><dl><div><dt>Versión</dt><dd>{connection.metadata?.version || 'Sin conexión'}</dd></div><div><dt>Fase actual</dt><dd>{connection.metadata?.phase || '—'}</dd></div><div><dt>Idioma / moneda / zona</dt><dd>{connection.metadata ? `${connection.metadata.defaults.locale} / ${connection.metadata.defaults.currency} / ${connection.metadata.defaults.timezone}` : '—'}</dd></div><div><dt>Solicitud</dt><dd>{connection.requestId || '—'}</dd></div></dl></details>
            </section><div className="notice"><Icon name="info" />Los servicios de registro, catálogo, inventario y venta se incorporan en las siguientes entregas.</div>
          </> : route === 'inicio' ? <>
            <section className="overview-banner foundation-hero"><div><span className="badge success">UN ESPACIO PARA CADA NEGOCIO</span><h2>Todo conectado.<br />Desde el primer día.</h2><p>Ventas, inventario y caja compartirán la misma información para ayudarte a tomar mejores decisiones.</p><AppLink to="estado">Ver estado de conexión <Icon name="arrow" /></AppLink></div><div className="foundation-mark" aria-hidden="true"><div><Icon name="box" /><span>Productos</span></div><div><Icon name="sell" /><span>Ventas</span></div><div><Icon name="cash" /><span>Caja</span></div><span className="mark-dot">●</span></div></section>
            <div className="next-steps"><article className="panel next-step"><span className="step-number">01</span><Icon name="settings" /><h2>Configura tu negocio</h2><p>Empresa, sucursales y colaboradores en un espacio propio.</p><AppLink to="configuracion" className="text-link">Conocer el siguiente paso <Icon name="arrow" /></AppLink></article><article className="panel next-step"><span className="step-number">02</span><Icon name="box" /><h2>Dale lugar a tu catálogo</h2><p>Productos y servicios con precios e inventario claros.</p><AppLink to="productos" className="text-link">Ver el área de productos <Icon name="arrow" /></AppLink></article><article className="panel next-step"><span className="step-number">03</span><Icon name="sell" /><h2>Prepárate para vender</h2><p>Un recorrido sencillo desde el producto hasta el ticket.</p><AppLink to="vender" className="text-link">Ver el área de venta <Icon name="arrow" /></AppLink></article></div>
            <section className="panel foundation-note"><span className="service-icon good"><Icon name="check" /></span><div><h2>El diseño ya tiene un lugar para todo</h2><p>Puedes explorar el recorrido aprobado mientras construimos los módulos de tu espacio.</p></div>{prototypeLink}</section>
          </> : <section className="panel upcoming-panel"><span className="upcoming-icon"><Icon name={section?.icon || 'box'} /></span><span className="badge neutral">Próximamente</span><h2>{section?.name === 'Configuración' ? 'Pronto podrás crear tu espacio' : `Estamos preparando ${section?.name.toLocaleLowerCase()}`}</h2><p>{route === 'productos' ? 'Aquí administrarás tus productos y servicios. El catálogo real se habilitará después de configurar el acceso a cada negocio.' : route === 'inventario' ? 'Aquí consultarás existencias y movimientos por sucursal y almacén.' : route === 'caja' ? 'Aquí abrirás turnos y revisarás el efectivo, los movimientos y las diferencias.' : route === 'vender' ? 'Aquí buscarás productos, cobrarás y entregarás el ticket. Todavía no se pueden registrar ventas reales.' : 'Aquí definirás tu empresa, sucursales y permisos. La configuración se podrá adaptar a las necesidades de cada cliente.'}</p>{prototypeLink}<small>El recorrido de diseño usa datos ficticios y se abre por separado.</small></section>}
        </main>
        <nav className="mobile-nav" aria-label="Accesos rápidos">{sections.filter(item => item.id !== 'configuracion').map(item => <a key={item.id} href={`#${item.id}`} aria-current={route === item.id ? 'page' : undefined}><Icon name={item.icon} /><span>{item.id === 'vender' ? 'Vender' : item.name}</span></a>)}</nav>
      </div>
    </div>
  </>;
}

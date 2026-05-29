import streamlit as st
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================
# LANDING PAGE — FreightMetrics
# ============================================================

st.markdown("""
<style>
    /* Ocultar header de Streamlit en esta pagina */
    header[data-testid="stHeader"] { display: none; }

    .hero-section {
        background: linear-gradient(135deg, #0b1326 0%, #11203a 50%, #1a2d4a 100%);
        border-radius: 16px;
        padding: 3rem 2.5rem;
        margin-bottom: 2rem;
        border: 1px solid #29B5E820;
    }
    .hero-logo {
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #F4F7F6;
        margin: 0;
        line-height: 1.2;
    }
    .hero-accent {
        color: #29B5E8;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #c8d0e0;
        margin-top: 0.8rem;
        margin-bottom: 1.5rem;
        font-weight: 300;
        line-height: 1.6;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(41,181,232,0.15);
        border: 1px solid #29B5E840;
        color: #29B5E8;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    .feature-card {
        background: linear-gradient(135deg, #11101D 80%, #1a2d4a);
        border: 1px solid #29B5E830;
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        transition: border-color 0.2s;
    }
    .feature-card:hover {
        border-color: #29B5E870;
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .feature-title {
        font-size: 1rem;
        font-weight: 700;
        color: #F4F7F6;
        margin-bottom: 0.4rem;
    }
    .feature-desc {
        font-size: 0.85rem;
        color: #c8d0e0;
        line-height: 1.5;
    }
    .stat-box {
        background: #11101D;
        border: 1px solid #29B5E830;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
    }
    .stat-num {
        font-size: 2rem;
        font-weight: 800;
        color: #29B5E8;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.78rem;
        color: #8899aa;
        margin-top: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .cta-btn {
        display: inline-block;
        background: #29B5E8;
        color: #0b1326 !important;
        font-weight: 700;
        font-size: 1rem;
        padding: 14px 32px;
        border-radius: 8px;
        text-decoration: none;
        margin-right: 12px;
        margin-top: 12px;
    }
    .cta-btn-secondary {
        display: inline-block;
        background: transparent;
        color: #29B5E8 !important;
        font-weight: 600;
        font-size: 1rem;
        padding: 13px 30px;
        border-radius: 8px;
        border: 1px solid #29B5E8;
        text-decoration: none;
        margin-top: 12px;
    }
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #F4F7F6;
        margin-bottom: 0.3rem;
    }
    .section-sub {
        font-size: 0.95rem;
        color: #8899aa;
        margin-bottom: 1.5rem;
    }
    .corridor-tag {
        display: inline-block;
        background: rgba(64,112,244,0.15);
        border: 1px solid #4070F440;
        color: #4070F4;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 3px;
    }
    .testimonial {
        background: #11101D;
        border-left: 3px solid #29B5E8;
        border-radius: 0 10px 10px 0;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .testimonial-text {
        color: #c8d0e0;
        font-size: 0.92rem;
        font-style: italic;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    .testimonial-author {
        color: #8899aa;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <div class="hero-logo">🚛</div>
    <h1 class="hero-title">
        Freight<span class="hero-accent">Metrics</span>
    </h1>
    <p class="hero-subtitle">
        La plataforma de inteligencia logistica para el corredor comercial 
        <strong style="color:#F4F7F6;">Mexico · USA · Canada</strong>.<br>
        Datos en tiempo real, analisis predictivo y herramientas para directivos 
        que toman decisiones con informacion — no con suposiciones.
    </p>
    <div>
        <span class="hero-badge">📊 Datos en Tiempo Real</span>
        <span class="hero-badge">🛃 Monitoreo CBP</span>
        <span class="hero-badge">🤖 IA Integrada</span>
        <span class="hero-badge">🌎 Mexico · USA</span>
        <span class="hero-badge">🎓 Academy Gratuita</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── STATS ─────────────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
stats = [
    ("15+", "Fuentes de datos integradas"),
    ("22", "Cruces fronterizos monitoreados"),
    ("$873B", "Comercio MX-USA 2025"),
    ("5 min", "Frecuencia de actualizacion"),
    ("$0", "Acceso basico gratuito"),
]
for col, (num, label) in zip([col1,col2,col3,col4,col5], stats):
    with col:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-num">{num}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── MODULOS ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-title">Modulos de Inteligencia</div>
<div class="section-sub">Todo lo que el director de logistica moderno necesita en un solo lugar</div>
""", unsafe_allow_html=True)

modulos = [
    ("🛃", "Monitoreo de Aduanas",
     "Tiempos de espera en tiempo real en los 22 principales cruces USA-Mexico via API CBP. Planea cruces inteligentes y evita horas pico."),
    ("📦", "Flujos de Carga",
     "Analisis de volumenes, tendencias y proyecciones de carga por corredor. Datos BTS actualizados mensualmente."),
    ("👥", "Fuerza Laboral",
     "KPIs del sector autotransporte: operadores, permisionarios, capacidad y tendencias de empleo por region."),
    ("🗺️", "Corredores Logisticos",
     "Analisis geoespacial de rutas estrategicas Mexico-USA. Costo, tiempo y riesgo por corredor."),
    ("🚢", "Puertos Maritimos",
     "Saturacion y operaciones en tiempo real en Manzanillo, Lazaro Cardenas, Veracruz y mas."),
    ("🏭", "Nearshoring",
     "Mapa de parques industriales, demanda logistica y oportunidades para posicionar tu flota."),
    ("⏱️", "CBP Wait Times",
     "Tiempos de espera por puerto, carril comercial y FAST Lane. Datos actualizados cada 5 minutos."),
    ("🎓", "Academy",
     "Ebooks gratuitos: KPIs de logistica, compliance DOT/SICT, apoyos gubernamentales y mas."),
]

col_a, col_b = st.columns(2)
for i, (icon, titulo, desc) in enumerate(modulos):
    with (col_a if i % 2 == 0 else col_b):
        st.markdown(f"""
        <div class="feature-card" style="margin-bottom:1rem;">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{titulo}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ORACLE RATE ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#0b1326,#11203a);
     border:1px solid #4070F440;border-radius:16px;padding:2rem 2.5rem;margin-bottom:2rem;">
    <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem;">
        <span style="font-size:2.5rem;">🔮</span>
        <div>
            <div style="font-size:1.3rem;font-weight:800;color:#F4F7F6;">Oracle Rate</div>
            <div style="font-size:0.9rem;color:#29B5E8;">Cotizacion inteligente con IA</div>
        </div>
    </div>
    <p style="color:#c8d0e0;font-size:0.95rem;line-height:1.6;margin-bottom:1rem;">
        Genera cotizaciones de flete Mexico-USA en menos de <strong style="color:#F4F7F6;">12 minutos</strong> 
        integrando precio de diesel CRE, distancias Google Maps, tipo de cambio y datos DAT. 
        El <strong style="color:#F4F7F6;">Sr. Oraculo</strong> — nuestro asistente de IA — 
        analiza cada cotizacion y emite un veredicto: <strong style="color:#00CC96;">ACEPTAR</strong> / 
        <strong style="color:#F59E0B;">NEGOCIAR</strong> / <strong style="color:#EF553B;">RECHAZAR</strong>.
    </p>
    <div style="display:flex;flex-wrap:wrap;gap:0.5rem;">
        <span class="corridor-tag">Caja Seca</span>
        <span class="corridor-tag">Refrigerado</span>
        <span class="corridor-tag">Plataforma</span>
        <span class="corridor-tag">Full/Doble</span>
        <span class="corridor-tag">Mexico → USA</span>
        <span class="corridor-tag">USA → Mexico</span>
        <span class="corridor-tag">Canada incluido</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── CORREDORES ────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("""
    <div class="section-title">Corredores Cubiertos</div>
    <div class="section-sub">Los principales ejes logisticos Mexico-USA</div>
    """, unsafe_allow_html=True)
    
    corredores = [
        "Tijuana → San Diego (CA)",
        "Mexicali → Calexico (CA)",
        "Nogales → Nogales (AZ)",
        "Ciudad Juarez → El Paso (TX)",
        "Nuevo Laredo → Laredo (TX)",
        "Reynosa → McAllen (TX)",
        "Matamoros → Brownsville (TX)",
        "Monterrey → Houston (TX)",
        "CDMX → Dallas (TX)",
        "Guadalajara → Los Angeles (CA)",
        "Puebla → Chicago (IL)",
        "Queretaro → Detroit (MI)",
    ]
    cols = st.columns(2)
    for i, c in enumerate(corredores):
        with cols[i % 2]:
            st.markdown(f'<span class="corridor-tag">🛣️ {c}</span>', unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class="section-title">Para quien es FreightMetrics</div>
    <div class="section-sub">Disenado para profesionales del comercio exterior</div>
    """, unsafe_allow_html=True)
    
    perfiles = [
        ("🏢", "Directores de Logistica", "Vision ejecutiva del corredor MX-USA"),
        ("🚛", "Transportistas y Carriers", "Cotizaciones y monitoreo de rutas"),
        ("🛃", "Agentes Aduanales", "Tiempos de cruce y alertas de aduana"),
        ("🏭", "Empresas de Nearshoring", "Inteligencia de corredores industriales"),
        ("💼", "Importadores/Exportadores", "Analisis de flujos y tendencias"),
        ("📊", "Analistas de Supply Chain", "Datos y KPIs del sector"),
    ]
    for icon, perfil, desc in perfiles:
        st.markdown(f"""
        <div style="display:flex;gap:0.8rem;align-items:flex-start;
             margin-bottom:0.8rem;padding:0.7rem;background:#11101D;
             border-radius:8px;border:1px solid #29B5E815;">
            <span style="font-size:1.4rem;">{icon}</span>
            <div>
                <div style="font-size:0.88rem;font-weight:700;color:#F4F7F6;">{perfil}</div>
                <div style="font-size:0.78rem;color:#8899aa;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ACADEMY PROMO ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#11101D 80%,#1a2d4a);
     border:1px solid #F59E0B30;border-left:4px solid #F59E0B;
     border-radius:12px;padding:1.5rem 2rem;margin-bottom:2rem;">
    <div style="font-size:1.2rem;font-weight:700;color:#F4F7F6;margin-bottom:0.5rem;">
        🎓 FreightMetrics Academy — Recursos Gratuitos
    </div>
    <p style="color:#c8d0e0;font-size:0.9rem;line-height:1.5;margin-bottom:1rem;">
        Ebooks gratuitos disenados para el mercado mexicano: KPIs de logistica, 
        compliance DOT/SICT, apoyos gubernamentales para transportistas y guias 
        de nearshoring. Bilingues Espanol/Ingles.
    </p>
    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;">
        <span style="background:#F59E0B20;border:1px solid #F59E0B40;color:#F59E0B;
              padding:3px 10px;border-radius:12px;font-size:0.75rem;font-weight:600;">
              📊 KPIs de Logistica
        </span>
        <span style="background:#F59E0B20;border:1px solid #F59E0B40;color:#F59E0B;
              padding:3px 10px;border-radius:12px;font-size:0.75rem;font-weight:600;">
              🔧 Guia Hombre-Camion
        </span>
        <span style="background:#F59E0B20;border:1px solid #F59E0B40;color:#F59E0B;
              padding:3px 10px;border-radius:12px;font-size:0.75rem;font-weight:600;">
              ⚠️ Cero Tolerancia Compliance
        </span>
        <span style="background:#F59E0B20;border:1px solid #F59E0B40;color:#F59E0B;
              padding:3px 10px;border-radius:12px;font-size:0.75rem;font-weight:600;">
              🚛 Apoyo al Autotransporte
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── CTA FINAL ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;background:linear-gradient(135deg,#0b1326,#11203a);
     border-radius:16px;padding:2.5rem 2rem;border:1px solid #29B5E820;">
    <div style="font-size:2rem;font-weight:800;color:#F4F7F6;margin-bottom:0.5rem;">
        Inteligencia logistica para mover Mexico.
    </div>
    <p style="color:#c8d0e0;font-size:1rem;margin-bottom:1.5rem;">
        Acceso gratuito. Sin tarjeta de credito. Empieza en segundos.
    </p>
    <p style="color:#8899aa;font-size:0.85rem;margin-top:1rem;">
        📧 contacto@freightmetrics.mx · 🌐 freightmetrics.mx · 📍 Tijuana, BC · Mexico
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

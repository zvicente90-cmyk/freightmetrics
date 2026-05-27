# <<Inicio>>
"""
FreightMetrics Pro - Página de Inicio (Landing Page)
Plataforma de inteligencia logística para la ruta México-USA
"""

import streamlit as st
import base64
from datetime import datetime
import pytz
import requests

# ============================================================
# CONFIGURACIÓN CRÍTICA
# ============================================================
st.set_page_config(
    page_title="FreightMetrics Pro - Inteligencia Logística México-USA",
    layout="wide",
    page_icon="🚛",
    initial_sidebar_state="expanded"
)

# Aplicar tema global
from modules.estilos_globales import aplicar_estilos_globales
aplicar_estilos_globales()

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def load_image_as_base64(image_path):
    """Carga una imagen y la convierte a base64"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

def get_current_metrics():
    """Obtiene métricas actuales"""
    try:
        resp = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=5)
        if resp.status_code == 200:
            rate = resp.json()['rates'].get('MXN', 17.0)
        else:
            rate = 17.0
    except:
        rate = 17.0
    
    # Obtener hora en zona México
    mexico_tz = pytz.timezone('America/Mexico_City')
    now = datetime.now(mexico_tz)
    
    return {
        'usd_mxn': f"${rate:.2f}",
        'fecha': now.strftime("%d/%m/%Y"),
        'hora': now.strftime("%H:%M:%S")
    }

# ============================================================
# HEADER CON LOGO
# ============================================================

col_logo, col_title = st.columns([1, 4])

with col_logo:
    try:
        logo_b64 = load_image_as_base64("assets/logo.png")
        if logo_b64:
            st.markdown(
                f'<img src="data:image/png;base64,{logo_b64}" width="80">',
                unsafe_allow_html=True
            )
    except:
        st.markdown("🚛", unsafe_allow_html=True)

with col_title:
    st.markdown("### 🚛 FreightMetrics Pro")
    st.markdown("**Inteligencia Logística - México USA**")

st.markdown("---")

# ============================================================
# HERO SECTION
# ============================================================

hero_col1, hero_col2 = st.columns([2, 1])

with hero_col1:
    st.markdown("""
    # 🌍 Connecting Borders, Delivering Insights
    
    FreightMetrics es tu **plataforma integral de inteligencia logística** 
    especializada en la ruta comercial México-USA.
    
    Obtén acceso a datos en tiempo real, análisis predictivos y reportes 
    estratégicos para optimizar tus operaciones logísticas.
    """)
    
    st.markdown("")
    if st.button("🚀 Explorar Dashboard", key="hero_btn", use_container_width=True):
        st.switch_page("pages/01_Dashboard.py")

with hero_col2:
    st.info("""
    **📊 Datos en Tiempo Real**
    
    Actualización cada 5 minutos
    
    **✅ 15+ Fuentes Verificadas**
    
    CBP, INEGI, Aduanas
    
    **🎯 Acceso Gratuito**
    
    Inicio inmediato
    """)

st.markdown("---")

# ============================================================
# ¿QUÉ ES FREIGHTMETRICS?
# ============================================================

st.markdown("## 📋 ¿Qué es FreightMetrics?")

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    st.markdown("""
    ### 🎯 Misión
    
    Democratizar el acceso a datos logísticos 
    de calidad para optimizar la toma de 
    decisiones en la ruta México-USA.
    """)

with info_col2:
    st.markdown("""
    ### 👁️ Visión
    
    Ser la plataforma de referencia para 
    inteligencia logística y comercial en 
    el corredor México-USA.
    """)

with info_col3:
    st.markdown("""
    ### ⚡ Valor
    
    Ahorrar tiempo, reducir costos y 
    aumentar eficiencia operativa con 
    datos inteligentes.
    """)

st.markdown("---")

# ============================================================
# CARACTERÍSTICAS PRINCIPALES
# ============================================================

st.markdown("## ✨ Características Principales")

char_col1, char_col2, char_col3, char_col4 = st.columns(4)

with char_col1:
    st.markdown("""
    ### 📊 Dashboard Ejecutivo
    
    Resumen visual de cruces 
    fronterizos y KPIs clave
    
    [Explorar →](./Dashboard)
    """)

with char_col2:
    st.markdown("""
    ### 📦 Flujos de Carga
    
    Análisis detallado de 
    movimientos comerciales
    
    [Explorar →](./Flujos_de_Carga)
    """)

with char_col3:
    st.markdown("""
    ### 👥 Inteligencia Laboral
    
    Datos del mercado laboral 
    en logística
    
    [Explorar →](./Fuerza_Laboral)
    """)

with char_col4:
    st.markdown("""
    ### 🛣️ Corredores Logísticos
    
    Mapeo de rutas estratégicas 
    México-USA
    
    [Explorar →](./Corredores_Logisticos)
    """)

char_col5, char_col6, char_col7, char_col8 = st.columns(4)

with char_col5:
    st.markdown("""
    ### ⛴️ Puertos Marítimos
    
    Estadísticas de puertos 
    principales
    
    [Explorar →](./Puertos_Maritimos)
    """)

with char_col6:
    st.markdown("""
    ### 🏭 Nearshoring
    
    Análisis de relocalización 
    industrial
    
    [Explorar →](./Nearshoring)
    """)

with char_col7:
    st.markdown("""
    ### ⏱️ Tiempos CBP Real-Time
    
    Actualización cada 5 minutos 
    de cruces fronterizos
    
    [Explorar →](./CBP_Wait_Times)
    """)

with char_col8:
    st.markdown("""
    ### 📚 Academia
    
    Ebooks gratuitos y recursos 
    educativos en logística
    
    [Explorar →](./Academy)
    """)

st.markdown("---")

# ============================================================
# VENTAJAS CLAVE
# ============================================================

st.markdown("## 💡 Ventajas Clave")

venta_col1, venta_col2 = st.columns(2)

with venta_col1:
    st.markdown("""
    ✅ **Datos en Tiempo Real**
    - CBP Wait Times (cada 5 min)
    - Tasas de cambio USD/MXN
    - Status de puertos fronterizos
    
    ✅ **Análisis Inteligentes**
    - Predicciones de demanda
    - Tendencias mensuales
    - Comparativas por corredor
    
    ✅ **Reportes Exportables**
    - Descarga en CSV
    - Gráficos interactivos
    - Dashboards personalizables
    """)

with venta_col2:
    st.markdown("""
    ✅ **Acceso Gratuito**
    - Sin suscripción requerida
    - Actualización diaria
    - Histórico de datos
    
    ✅ **Interfaz Intuitiva**
    - Fácil de navegar
    - Filtros potentes
    - Diseño responsivo
    
    ✅ **Soporte Educativo**
    - Academia con 4 ebooks
    - Guías de autotransporte
    - Recursos de nearshoring
    """)

st.markdown("---")

# ============================================================
# PARA QUIÉN ES FREIGHTMETRICS
# ============================================================

st.markdown("## 👥 ¿Para Quién es FreightMetrics?")

audience_col1, audience_col2, audience_col3 = st.columns(3)

with audience_col1:
    st.markdown("""
    ### 🚚 Transportistas
    
    - Optimiza rutas y tiempos
    - Evita cuellos de botella
    - Planifica mejor tu logística
    - Reduce costos operativos
    """)

with audience_col2:
    st.markdown("""
    ### 📊 Logistics Managers
    
    - Monitorea KPIs en tiempo real
    - Toma decisiones basadas en datos
    - Genera reportes automáticos
    - Identifica oportunidades
    """)

with audience_col3:
    st.markdown("""
    ### 🏢 Empresarios
    
    - Evalúa viabilidad de nearshoring
    - Entiende dinámicas comerciales
    - Identifica mercados
    - Planea expansión
    """)

st.markdown("---")

# ============================================================
# MÉTRICAS EN VIVO
# ============================================================

st.markdown("## 🌍 Métricas en Vivo")

metrics = get_current_metrics()

metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric("💱 Tipo de Cambio", metrics['usd_mxn'])

with metric_col2:
    st.metric("📅 Fecha", metrics['fecha'])

with metric_col3:
    st.metric("🕐 Hora (México)", metrics['hora'])

st.markdown("---")

# ============================================================
# SELECTOR DE IDIOMA
# ============================================================

st.markdown("## 🌐 Idioma / Language / Langue")

lang_col1, lang_col2, lang_col3 = st.columns(3)

with lang_col1:
    if st.button("🇲🇽 Español", use_container_width=True):
        st.session_state.language = 'es'
        st.rerun()

with lang_col2:
    if st.button("🇺🇸 English", use_container_width=True):
        st.session_state.language = 'en'
        st.rerun()

with lang_col3:
    if st.button("🇫🇷 Français", use_container_width=True):
        st.session_state.language = 'fr'
        st.rerun()

st.markdown("---")

# ============================================================
# LLAMADA A ACCIÓN FINAL
# ============================================================

st.markdown("""
## 🎓 Aprende con Nuestra Academia

Accede a **4 ebooks gratuitos** sobre logística, autotransporte 
y nearshoring. Perfectos para profesionales que quieren 
mejorar su expertise.
""")

if st.button("📚 Acceder a Academia", use_container_width=True, type="primary"):
    st.switch_page("pages/08_Academy.py")

st.markdown("---")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div style='text-align: center; color: #666; margin-top: 50px; font-size: 0.9em;'>
    <p>FreightMetrics Pro © 2026 | Inteligencia Logística para México-USA</p>
    <p>Datos actualizados cada 5 minutos | Fuentes verificadas: CBP, INEGI, Aduanas</p>
</div>
""", unsafe_allow_html=True)

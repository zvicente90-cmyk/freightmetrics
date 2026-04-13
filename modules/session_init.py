"""
Módulo centralizado para inicializar session_state y constantes globales.
Evita duplicación de código en múltiples páginas.
"""

import streamlit as st


def initialize_session_state():
    """
    Inicializa todas las variables de session_state de una sola vez.
    Debe ser llamado una sola vez al inicio de app.py.
    """
    
    # Idioma
    if 'language' not in st.session_state:
        st.session_state.language = 'es'
    
    # Selección de página
    if 'selected_page_index' not in st.session_state:
        st.session_state.selected_page_index = 0  # Dashboard es la primera opción
    
    # Monitoreo de aduanas
    if 'cache_aduanas_time' not in st.session_state:
        st.session_state.cache_aduanas_time = 0
    
    # Sistema de alertas de puertos
    if 'sistema_alertas_puertos' not in st.session_state:
        st.session_state.sistema_alertas_puertos = None
    
    # Contador de gráficos (para Corredores Logísticos)
    if 'chart_counter_corredores' not in st.session_state:
        st.session_state.chart_counter_corredores = 0
    
    # Puedes agregar más variables aquí según sea necesario


# ============================================================
# FALLBACK DE COMPONENTES UI (Centralizados para evitar duplicación)
# ============================================================

def metric_card(title, value, icon="📊", color="#4070F4", delta=None, delta_color="normal"):
    """Tarjeta de métrica básica"""
    st.metric(title, value, delta=delta, delta_color=delta_color)

def metric_card_compact(title, value, icon="📊", color="#4070F4"):
    """Tarjeta de métrica compacta"""
    st.metric(title, value)

def page_header(title, subtitle="", icon="📊"):
    """Encabezado de página"""
    st.title(f"{icon} {title}")
    if subtitle:
        st.markdown(f"**{subtitle}**")

def section_header(title="", icon="", color=""):
    """Encabezado de sección"""
    st.subheader(f"{icon} {title}")

def info_card(title, content, icon="ℹ️", color="#4070F4"):
    """Tarjeta de información"""
    st.info(f"**{icon} {title}**\n{content}")

def spacer(height=20):
    """Espaciador vertical"""
    st.markdown(f"<div style='height: {height}px;'></div>", unsafe_allow_html=True)


# ============================================================
# CONSTANTES GLOBALES
# ============================================================

# Años disponibles
YEARS = [2023, 2024, 2025, 2026]

# Meses disponibles
MONTHS = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
          "Julio", "Agosto", "Setembre", "Octubre", "Noviembre", "Diciembre"]

# Mapeo de meses a números
MONTHS_MAP = {
    'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
    'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
    'Setembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
}

# Fronteras
BORDERS = ["México", "Canadá", "Ambas"]

# Puntos geográficos principales (puertos y ciudades fronterizas)
GEOGRAPHICAL_POINTS = {
    "Manzanillo": {"lat": 19.0522, "lon": -104.3158},
    "Veracruz": {"lat": 19.1738, "lon": -96.1342},
    "Lázaro Cárdenas": {"lat": 17.9585, "lon": -102.1891},
    "Altamira": {"lat": 22.3943, "lon": -97.9377},
    "Puerto Vallarta": {"lat": 20.6295, "lon": -105.2381},
    "Los Cabos": {"lat": 22.8898, "lon": -109.9789},
}

# Tipos de transporte
TRANSPORT_TYPES = [
    "Autotransporte",
    "Ferrocarril",
    "Marítimo",
    "Aéreo",
    "Multimodal"
]

# Corredores logísticos principales
LOGISTICS_CORRIDORS = [
    "México - Canadá",
    "México - USA (Este)",
    "México - USA (Oeste)",
    "México - Guatemala",
    "México - Belice"
]

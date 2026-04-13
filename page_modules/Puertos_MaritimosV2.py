import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

# Importar componentes UI centralizados
try:
    from modules.session_init import (
        metric_card, metric_card_compact, info_card, page_header, section_header, spacer
    )
    UI_COMPONENTS_AVAILABLE = True
except ImportError:
    UI_COMPONENTS_AVAILABLE = False
    # Fallback mínimo si no está disponible
    def metric_card(title, value, icon="📊", color="#4070F4", delta=None, delta_color="normal"):
        st.metric(title, value, delta=delta, delta_color=delta_color)
    
    def metric_card_compact(title, value, icon="📊", color="#4070F4"):
        st.metric(title, value)
    
    def page_header(title, subtitle="", icon="📊"):
        st.title(f"{icon} {title}")
        if subtitle:
            st.markdown(f"**{subtitle}**")
    
    def section_header(title="", icon="", color=""):
        st.subheader(f"{icon} {title}")
    
    def spacer(height=20):
        st.markdown(f"<div style='height: {height}px;'></div>", unsafe_allow_html=True)


def page_puertos_maritimos_v2():
    """Página de Puertos Marítimos V2"""
    
    page_header(
        title="Puertos Marítimos V2",
        subtitle="Análisis y Monitoreo de Puertos",
        icon="⚓"
    )
    
    st.info("Esta página está en desarrollo...")

"""
FreightMetrics Pro - Punto de Entrada
Las páginas reales están en la carpeta pages/
"""

import streamlit as st

st.set_page_config(
    page_title="FreightMetrics Pro",
    layout="wide",
    page_icon="🚛"
)

# Aplicar tema global
from modules.estilos_globales import aplicar_estilos_globales
aplicar_estilos_globales()

# Redirect a página de inicio
st.switch_page("pages/_00_Inicio.py")

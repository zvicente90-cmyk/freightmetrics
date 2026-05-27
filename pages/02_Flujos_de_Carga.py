import streamlit as st
from page_modules._02_Flujos_de_Carga import page_flujos_de_carga
from modules.estilos_globales import aplicar_estilos_globales

st.set_page_config(page_title="Flujos de Carga - FreightMetrics", layout="wide", page_icon="📦")
aplicar_estilos_globales()

if page_flujos_de_carga:
    page_flujos_de_carga()
else:
    st.error("Flujos de Carga module not available")

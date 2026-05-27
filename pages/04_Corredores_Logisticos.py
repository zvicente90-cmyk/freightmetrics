import streamlit as st
from page_modules._04_Corredores_Logisticos import page_corredores_logisticos
from modules.estilos_globales import aplicar_estilos_globales

st.set_page_config(page_title="Corredores Logísticos - FreightMetrics", layout="wide", page_icon="🛣️")
aplicar_estilos_globales()

if page_corredores_logisticos:
    page_corredores_logisticos()
else:
    st.error("Corredores Logísticos module not available")

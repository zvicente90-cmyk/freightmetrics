import streamlit as st
from page_modules._03_Fuerza_Laboral import page_fuerza_laboral
from modules.estilos_globales import aplicar_estilos_globales

st.set_page_config(page_title="Fuerza Laboral - FreightMetrics", layout="wide", page_icon="👥")
aplicar_estilos_globales()

if page_fuerza_laboral:
    page_fuerza_laboral()
else:
    st.error("Fuerza Laboral module not available")

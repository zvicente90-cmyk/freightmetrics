import streamlit as st
from page_modules._00_Inicio import page_dashboard
from modules.estilos_globales import aplicar_estilos_globales

st.set_page_config(page_title="Dashboard - FreightMetrics", layout="wide", page_icon="🚛")
aplicar_estilos_globales()

if page_dashboard:
    page_dashboard()
else:
    st.error("Dashboard module not available")

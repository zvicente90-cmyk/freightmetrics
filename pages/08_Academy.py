import streamlit as st
from page_modules._08_Academy import page_academy
from modules.estilos_globales import aplicar_estilos_globales

st.set_page_config(page_title="Academy - FreightMetrics", layout="wide", page_icon="📚")
aplicar_estilos_globales()

if page_academy:
    page_academy()
else:
    st.error("Academy module not available")

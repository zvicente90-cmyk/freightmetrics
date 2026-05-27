import streamlit as st
from page_modules._06_Nearshoring import page_nearshoring
from modules.estilos_globales import aplicar_estilos_globales

st.set_page_config(page_title="Nearshoring - FreightMetrics", layout="wide", page_icon="🌎")
aplicar_estilos_globales()

if page_nearshoring:
    page_nearshoring()
else:
    st.error("Nearshoring module not available")

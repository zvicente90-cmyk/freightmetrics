import streamlit as st
from page_modules._04_Corredores_Logisticos import page_corredores_logisticos

st.set_page_config(page_title="Corredores Logísticos - FreightMetrics", layout="wide", page_icon="🛣️")

if page_corredores_logisticos:
    page_corredores_logisticos()
else:
    st.error("Corredores Logísticos module not available")

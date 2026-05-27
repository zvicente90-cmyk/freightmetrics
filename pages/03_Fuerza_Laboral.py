import streamlit as st
from page_modules._03_Fuerza_Laboral import page_fuerza_laboral

st.set_page_config(page_title="Fuerza Laboral - FreightMetrics", layout="wide", page_icon="👥")

if page_fuerza_laboral:
    page_fuerza_laboral()
else:
    st.error("Fuerza Laboral module not available")

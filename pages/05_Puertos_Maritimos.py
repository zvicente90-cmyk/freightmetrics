import streamlit as st
from page_modules._05_Puertos_Maritimos import page_puertos_maritimos

st.set_page_config(page_title="Puertos Marítimos - FreightMetrics", layout="wide", page_icon="⛴️")

if page_puertos_maritimos:
    page_puertos_maritimos()
else:
    st.error("Puertos Marítimos module not available")

import streamlit as st
from page_modules._00_Inicio import page_dashboard

st.set_page_config(page_title="Dashboard - FreightMetrics", layout="wide", page_icon="🚛")

if page_dashboard:
    page_dashboard()
else:
    st.error("Dashboard module not available")

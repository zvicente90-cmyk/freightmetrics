import streamlit as st
from page_modules._06_Nearshoring import page_nearshoring

st.set_page_config(page_title="Nearshoring - FreightMetrics", layout="wide", page_icon="🌎")

if page_nearshoring:
    page_nearshoring()
else:
    st.error("Nearshoring module not available")

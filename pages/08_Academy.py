import streamlit as st
from page_modules._08_Academy import page_academy

st.set_page_config(page_title="Academy - FreightMetrics", layout="wide", page_icon="📚")

if page_academy:
    page_academy()
else:
    st.error("Academy module not available")

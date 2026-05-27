import streamlit as st
from page_modules._06_CBP_Wait_Times import page_cbp_wait_times

st.set_page_config(page_title="CBP Wait Times - FreightMetrics", layout="wide", page_icon="⏱️")

if page_cbp_wait_times:
    page_cbp_wait_times()
else:
    st.error("CBP Wait Times module not available")

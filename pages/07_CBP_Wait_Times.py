import streamlit as st
from page_modules._06_CBP_Wait_Times import page_cbp_wait_times
from modules.estilos_globales import aplicar_estilos_globales

# st.set_page_config ya está definido en app.py
aplicar_estilos_globales()

if page_cbp_wait_times:
    page_cbp_wait_times()
else:
    st.error("CBP Wait Times module not available")

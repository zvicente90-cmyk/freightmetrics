import streamlit as st
from page_modules._05_Puertos_Maritimos import page_puertos_maritimos
from modules.estilos_globales import aplicar_estilos_globales

# st.set_page_config ya está definido en app.py
aplicar_estilos_globales()

if page_puertos_maritimos:
    page_puertos_maritimos()
else:
    st.error("Puertos Marítimos module not available")

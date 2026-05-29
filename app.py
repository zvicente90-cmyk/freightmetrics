import streamlit as st

st.set_page_config(
    page_title="FreightMetrics Pro",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# NAVEGACION CENTRALIZADA
# st.navigation() controla el sidebar completamente
# y elimina el item "app" automaticamente
# ============================================================

pg = st.navigation([
    st.Page("pages/_00_Inicio.py",               title="Inicio",                icon="🏠", default=True),
    st.Page("pages/_01_Monitoreo_Aduanas.py",     title="Monitoreo Aduanas",     icon="🛃"),
    st.Page("pages/_02_Flujos_de_Carga.py",       title="Flujos de Carga",       icon="📦"),
    st.Page("pages/_03_Fuerza_Laboral.py",        title="Fuerza Laboral",        icon="👥"),
    st.Page("pages/_04_Corredores_Logisticos.py", title="Corredores Logisticos", icon="🗺️"),
    st.Page("pages/_05_Puertos_Maritimos.py",     title="Puertos Maritimos",     icon="🚢"),
    st.Page("pages/_06_CBP_Wait_Times.py",        title="CBP Wait Times",        icon="⏱️"),
    st.Page("pages/_06_Nearshoring.py",           title="Nearshoring",           icon="🏭"),
    st.Page("pages/_08_Academy.py",               title="Academy",               icon="🎓"),
])

pg.run()

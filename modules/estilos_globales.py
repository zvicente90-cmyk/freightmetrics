"""
Módulo de estilos CSS globales para FreightMetrics
Tema: Dark Navy — consistente con la landing page
Paleta:
  Fondo principal:  #0b1326
  Superficie:       #F4F7F6 / #131b2e / #1a2d4a
  Acento primario:  #29B5E8 (Cyan)
  Acento secundario:#29B5E8 (Blue)
  Texto principal:  #F4F7F6
  Texto secundario: #c8d0e0
  Texto muted:      #8899aa
  Éxito:            #00CC96
  Advertencia:      #F59E0B
  Error:            #EF553B
"""
import streamlit as st


def aplicar_estilos_globales():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    
    /* ── FONDO GLOBAL ─────────────────────────────────────── */
    .stApp, .main, .block-container {
        background-color: #0b1326 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ── SIDEBAR ──────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        border-right: 1px solid #29B5E820 !important;
    }

    /* Target specific sidebar text only, avoiding icons */
    [data-testid="stSidebar"] [data-testid="stSidebarNavLink"] span,
    [data-testid="stSidebar"] .stMarkdown p {
        color: #c8d0e0 !important;
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stSidebar"] [aria-selected="true"] {
        background-color: #29B5E815 !important;
        border-left: 3px solid #29B5E8 !important;
        color: #F4F7F6 !important;
        border-radius: 0 8px 8px 0 !important;

    }

    [data-testid="stSidebarNavLink"]:hover {
        background-color: #29B5E810 !important;
        color: #F4F7F6 !important;
    }

    /* ── TITULOS ──────────────────────────────────────────── */
    h1 {
        color: #F4F7F6 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;

    }

    h2 {
        color: #F4F7F6 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;

    }

    h3 {
        color: #29B5E8 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }

    h4, h5, h6 {
        color: #c8d0e0 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ── TEXTO GENERAL ────────────────────────────────────── */
    p, span, li {
        color: #c8d0e0 !important;
    }

    .stMarkdown p {
        color: #c8d0e0 !important;

    }

    label {
        color: #c8d0e0 !important;
        font-weight: 500 !important;
    }

    /* ── METRICAS ─────────────────────────────────────────── */
    [data-testid="metric-container"] {
        background-color: #131b2e !important;
        border: 1px solid #29B5E825 !important;
        border-left: 4px solid #29B5E8 !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
    }

    [data-testid="stMetricValue"] {
        color: #F4F7F6 !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
    }

    [data-testid="stMetricLabel"] {
        color: #8899aa !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.82rem !important;
    }

    /* ── BOTONES ──────────────────────────────────────────── */
    .stButton > button {
        background-color: #29B5E8 !important;
        color: #0b1326 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
        padding: 0.5rem 1.5rem !important;
    }

    .stButton > button:hover {
        background-color: #1da0d4 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(41,181,232,0.3) !important;
    }

    .stButton > button[kind="secondary"] {
        background-color: transparent !important;
        color: #29B5E8 !important;
        border: 1px solid #29B5E8 !important;
    }

    /* ── INPUTS Y SELECTBOX ───────────────────────────────── */
    .stTextInput input, .stNumberInput input, .stDateInput input {
        background-color: #1a2d4a !important;
        border: 1px solid #29B5E830 !important;
        border-radius: 8px !important;
        color: #F4F7F6 !important;

    }

    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #29B5E8 !important;
        box-shadow: 0 0 0 2px rgba(41,181,232,0.2) !important;
    }

    [data-baseweb="select"] {
        background-color: #1a2d4a !important;
        border-color: #29B5E830 !important;
        border-radius: 8px !important;

    }

    [data-baseweb="select"] * {
        color: #F4F7F6 !important;
        background-color: #1a2d4a !important;

    }

    [data-baseweb="menu"] {
        background-color: #131b2e !important;
        border: 1px solid #29B5E830 !important;
    }
    
    [role="option"] {
        color: #c8d0e0 !important;
    }

    [role="option"]:hover {
        background-color: #29B5E815 !important;
        color: #F4F7F6 !important;
    }

    /* ── TABS ─────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid #29B5E820 !important;
        gap: 4px !important;

    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #8899aa !important;
        border-radius: 8px 8px 0 0 !important;
        font-weight: 600 !important;
        padding: 8px 20px !important;

    }
    
    .stTabs [aria-selected="true"] {
        background-color: #29B5E815 !important;
        color: #29B5E8 !important;
        border-bottom: 2px solid #29B5E8 !important;
    }

    .stTabs [data-baseweb="tab-panel"] {
        background-color: transparent !important;
        padding-top: 1rem !important;
    }

    /* ── TABLAS ───────────────────────────────────────────── */
    .dataframe {
        background-color: #131b2e !important;
        border: 1px solid #29B5E825 !important;
        border-radius: 10px !important;
    }

    .dataframe thead tr th {
        background-color: #0d1117 !important;
        color: #29B5E8 !important;
        font-weight: 700 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        padding: 10px 12px !important;
        border-bottom: 1px solid #29B5E830 !important;
    }

    .dataframe tbody tr td {
        color: #c8d0e0 !important;
        background-color: #131b2e !important;
        border-bottom: 1px solid #29B5E815 !important;
        padding: 8px 12px !important;
    }

    .dataframe tbody tr:nth-child(even) td {
        background-color: #0d1117 !important;
    }

    .dataframe tbody tr:hover td {
        background-color: #29B5E810 !important;
    }

    /* ── EXPANDERS ────────────────────────────────────────── */
    .streamlit-expanderHeader {
        background-color: #1a2d4a !important;
        color: #F4F7F6 !important;
        border: 1px solid #29B5E825 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    .streamlit-expanderContent {
        background-color: #0d1117 !important;
        border: 1px solid #29B5E820 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;

    }

    /* ── ALERTS ───────────────────────────────────────────── */
    [data-baseweb="notification"] {
        border-radius: 10px !important;
        border-left: 4px solid !important;
    }

    .stSuccess {
        background-color: #00CC9615 !important;
        border-left-color: #00CC96 !important;
        color: #c8d0e0 !important;
    }
    .stWarning {
        background-color: #F59E0B15 !important;
        border-left-color: #F59E0B !important;
        color: #c8d0e0 !important;
    }

    .stError {

        background-color: #EF553B15 !important;
        border-left-color: #EF553B !important;
        color: #c8d0e0 !important;

    }

    .stInfo {
        background-color: #29B5E815 !important;
        border-left-color: #29B5E8 !important;
        color: #c8d0e0 !important;
    }

    /* ── PLOTLY CHARTS ────────────────────────────────────── */
    .js-plotly-plot {
        background-color: #131b2e !important;
        border-radius: 12px !important;
        border: 1px solid #29B5E820 !important;
        padding: 8px !important;
    }

    /* ── SLIDERS ──────────────────────────────────────────── */
    .stSlider [data-baseweb="slider"] {
        color: #29B5E8 !important;
    }

    /* ── SPINNER ──────────────────────────────────────────── */
    .stSpinner > div {
        border-top-color: #29B5E8 !important;
    }

    /* ── PROGRESS BAR ─────────────────────────────────────── */
    .stProgress > div > div {
        background-color: #29B5E8 !important;
    }

    /* ── LINKS ────────────────────────────────────────────── */
    a {
        color: #29B5E8 !important;
        text-decoration: none !important;
    }

    a:hover {

        color: #29B5E8 !important;
        text-decoration: underline !important;
    }

    /* ── DIVIDER ──────────────────────────────────────────── */
    hr {

        border-color: #29B5E820 !important;
    }

    /* ── TOGGLE SIDEBAR ───────────────────────────────────── */
    [data-testid="collapseSidebarButton"] {

        color: #c8d0e0 !important;
        visibility: visible !important;

    }


    [data-testid="collapseSidebarButton"] > svg {
        fill: #c8d0e0 !important;

    /* ── SCROLLBAR ────────────────────────────────────────── */

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0b1326; }
    ::-webkit-scrollbar-thumb { background: #29B5E840; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #29B5E8; }
    </style>
    """, unsafe_allow_html=True)
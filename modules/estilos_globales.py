"""
Módulo de estilos CSS globales para FreightMetrics
Aplica la paleta Executive Navy & Slate a todas las páginas
"""
import streamlit as st

def aplicar_estilos_globales():
    """
    Inyecta CSS global para toda la aplicación
    Paleta: Azul Medianoche, Azul Eléctrico, Gris Nube, Azul Acero, Rojo Coral
    """
    st.markdown("""
        <style>
        /* ===== PALETA EXECUTIVE NAVY & SLATE ===== */
        /* Azul Medianoche: #11101D - Sidebar/Navegación */
        /* Azul Eléctrico: #4070F4 - Botones/Enlaces/Acentos */
        /* Azul Acero: #29B5E8 - Gráficas/Datos */
        /* Gris Nube: #F4F7F6 - Fondo Principal */
        /* Rojo Coral: #EF553B - Alertas/Déficit */
        
        /* Cambiar el fondo principal de la aplicación a Gris Nube */
        .main, .block-container {
            background-color: #F4F7F6 !important;
        }
        
        .stApp {
            background-color: #F4F7F6 !important;
        }
        
        /* Sidebar - Azul Medianoche */
        [data-testid="stSidebar"] {
            background-color: #11101D !important;
        }
        
        /* Todos los textos en el sidebar en blanco */
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] .st-emotion-cache-10trblm {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] label {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] p {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] [role="radiogroup"] label {
            color: #ffffff !important;
        }

        /* Títulos principales - Azul Medianoche */
        h1 {
            color: #11101D !important;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
        }
        
        h2 {
            color: #11101D !important;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
        }
        
        h3 {
            color: #4070F4 !important;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
        }

        /* Botones - Azul Eléctrico */
        .stButton>button {
            background-color: #4070F4 !important;
            color: white !important;
            border-radius: 10px;
            border: none;
            padding: 0.5rem 1.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #3060e4 !important;
            box-shadow: 0 4px 12px rgba(64, 112, 244, 0.4);
            transform: translateY(-2px);
        }
        
        /* Métricas - Azul Medianoche y Azul Eléctrico */
        [data-testid="stMetricValue"] {
            color: #11101D !important;
            font-weight: 700;
            font-size: 2rem;
        }
        
        [data-testid="stMetricLabel"] {
            color: #4070F4 !important;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
        }
        
        /* Contenedor de métricas - Fondo blanco para destacar */
        [data-testid="metric-container"] {
            background-color: #ffffff !important;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 10px rgba(17, 16, 29, 0.08);
            border-left: 4px solid #4070F4;
        }
        
        /* Tabs - Azul Eléctrico */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #ffffff !important;
            border-radius: 8px;
            color: #11101D !important;
            padding: 10px 20px;
            font-weight: 500;
            border: 2px solid transparent;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #4070F4 !important;
            color: white !important;
            border: 2px solid #4070F4;
        }
        
        /* Labels de inputs - Azul Medianoche */
        .stSelectbox label, .stMultiSelect label, .stTextInput label, 
        .stDateInput label, .stNumberInput label, .stSlider label {
            color: #11101D !important;
            font-weight: 600;
        }
        
        /* Tablas - Headers Azul Medianoche */
        .dataframe {
            border: 2px solid #29B5E8;
            border-radius: 10px;
            overflow: hidden;
        }
        
        .dataframe thead tr th {
            background-color: #11101D !important;
            color: white !important;
            font-weight: 600;
            padding: 12px;
        }
        
        .dataframe tbody tr:nth-child(even) {
            background-color: #F4F7F6;
        }
        
        .dataframe tbody tr:hover {
            background-color: #e8f4f8;
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            background-color: #ffffff !important;
            color: #11101D !important;
            border-radius: 10px;
            font-weight: 600;
            border: 1px solid #29B5E8;
        }
        
        /* Alerts - Diferentes colores según tipo */
        .stAlert {
            border-radius: 10px;
            border-left: 4px solid;
        }
        
        /* Alert de error - Rojo Coral */
        [data-baseweb="notification"][kind="error"],
        .stAlert[data-baseweb="notification"] {
            border-left-color: #EF553B !important;
        }
        
        /* Alert de éxito - Azul Acero */
        [data-baseweb="notification"][kind="success"] {
            border-left-color: #29B5E8 !important;
        }
        
        /* Alert de info - Azul Eléctrico */
        [data-baseweb="notification"][kind="info"] {
            border-left-color: #4070F4 !important;
        }
        
        /* Texto general */
        p, span, div {
            color: #11101D;
        }
        
        /* Links - Azul Eléctrico */
        a {
            color: #4070F4 !important;
            text-decoration: none;
            font-weight: 500;
        }
        
        a:hover {
            color: #29B5E8 !important;
            text-decoration: underline;
        }
        
        /* Contenedores de columnas - Fondo transparente */
        [data-testid="column"] {
            background-color: transparent;
        }
        
        /* Cards/Containers blancos para destacar sobre Gris Nube */
        .element-container {
            background-color: transparent;
        }
        
        /* Plotly charts - Fondo blanco */
        .js-plotly-plot {
            background-color: #ffffff !important;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 2px 8px rgba(17, 16, 29, 0.06);
        }
        
        /* Spinner/Loading - Azul Eléctrico */
        .stSpinner > div {
            border-top-color: #4070F4 !important;
        }
        
        /* Progress bar - Azul Eléctrico */
        .stProgress > div > div {
            background-color: #4070F4 !important;
        }
        </style>
        """, unsafe_allow_html=True)

"""
Estilos Globales - CSS profesional para toda la aplicación
Aplica automáticamente a TODOS los componentes de Streamlit
"""

import streamlit as st

def apply_global_styles():
    """
    Aplica estilos profesionales globales a toda la aplicación.
    Mejora: st.metric, expandibles, tabs, forms, inputs, etc.
    
    Usar en app.py:
        from page_modules.global_styles import apply_global_styles
        apply_global_styles()
    """
    st.markdown("""
    <style>
        /* ============================================================
           ESTILOS GLOBALES - COMPONENTES STREAMLIT PROFESIONALES
           ============================================================ */
        
        /* TARJETAS DE MÉTRICA (st.metric) - EL CORAZÓN DEL DASHBOARD */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, rgba(0, 61, 122, 0.12) 0%, rgba(0, 82, 163, 0.08) 100%) !important;
            padding: 20px !important;
            border-radius: 14px !important;
            border: 2px solid #0066cc !important;
            box-shadow: 
                0 0 20px rgba(0, 102, 204, 0.4),
                0 8px 24px rgba(0, 0, 0, 0.15),
                inset 0 1px 2px rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(8px) !important;
            transition: all 0.3s ease !important;
        }
        
        [data-testid="metric-container"]:hover {
            box-shadow: 
                0 0 30px rgba(0, 102, 204, 0.6),
                0 12px 32px rgba(0, 0, 0, 0.2),
                inset 0 1px 2px rgba(255, 255, 255, 0.15) !important;
            transform: translateY(-4px) !important;
        }
        
        /* Etiqueta de métrica */
        [data-testid="metric-container"] > div:nth-child(1) {
            color: #0052a3 !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            letter-spacing: 0.5px !important;
            text-transform: uppercase !important;
            opacity: 0.9 !important;
        }
        
        /* Valor principal de métrica */
        [data-testid="metric-container"] > div:nth-child(2) {
            color: #0066cc !important;
            font-size: 2.2rem !important;
            font-weight: 900 !important;
            text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3) !important;
            letter-spacing: -1px !important;
        }
        
        /* Delta (cambio) en métrica */
        [data-testid="metric-container"] > div:nth-child(3) {
            color: #1976d2 !important;
            font-weight: 700 !important;
        }
        
        /* ============================================================
           EXPANDIBLES (EXPANDERS)
           ============================================================ */
        [data-testid="stExpander"] {
            border: 2px solid #0066cc !important;
            border-radius: 12px !important;
            box-shadow: 0 0 15px rgba(0, 102, 204, 0.25) !important;
            background: linear-gradient(135deg, rgba(0, 61, 122, 0.05) 0%, rgba(0, 82, 163, 0.03) 100%) !important;
        }
        
        [data-testid="stExpander"] > details > summary {
            padding: 12px 16px !important;
            color: #0066cc !important;
            font-weight: 700 !important;
        }
        
        [data-testid="stExpander"] > details > summary:hover {
            background: rgba(0, 102, 204, 0.1) !important;
            border-radius: 10px !important;
        }
        
        /* ============================================================
           TABS
           ============================================================ */
        [data-testid="stTabs"] {
            background: linear-gradient(135deg, rgba(0, 82, 163, 0.08) 0%, rgba(25, 118, 210, 0.05) 100%) !important;
            border-radius: 12px !important;
            padding: 12px !important;
            border: 1px solid rgba(0, 102, 204, 0.2) !important;
        }
        
        [data-testid="stTabs"] button {
            color: #0052a3 !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
        }
        
        [data-testid="stTabs"] button[aria-selected="true"] {
            background: linear-gradient(135deg, #0066cc 0%, #1976d2 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.4) !important;
        }
        
        /* ============================================================
           FORMULARIOS
           ============================================================ */
        [data-testid="stForm"] {
            background: linear-gradient(135deg, rgba(0, 61, 122, 0.08) 0%, rgba(0, 82, 163, 0.05) 100%) !important;
            border: 2px solid #0066cc !important;
            border-radius: 12px !important;
            padding: 20px !important;
            box-shadow: 0 0 12px rgba(0, 102, 204, 0.2) !important;
        }
        
        /* ============================================================
           SELECTORES Y INPUTS
           ============================================================ */
        .stSelectbox > div > div {
            border-color: #0066cc !important;
            border-radius: 8px !important;
        }
        
        .stMultiSelect > div > div {
            border-color: #0066cc !important;
            border-radius: 8px !important;
        }
        
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input {
            border-color: #0066cc !important;
            color: #0066cc !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stDateInput > div > div > input:focus {
            border-color: #1976d2 !important;
            box-shadow: 0 0 12px rgba(0, 102, 204, 0.4) !important;
        }
        
        /* ============================================================
           BOTONES
           ============================================================ */
        .stButton > button {
            background: linear-gradient(135deg, #0066cc 0%, #1976d2 100%) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3) !important;
            font-weight: 700 !important;
            padding: 10px 24px !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            box-shadow: 0 6px 20px rgba(0, 102, 204, 0.5) !important;
            transform: translateY(-2px) !important;
        }
        
        /* ============================================================
           COLUMNAS Y CONTENEDORES
           ============================================================ */
        [data-testid="column"] {
            animation: fadeInUp 0.5s ease;
        }
        
        /* ============================================================
           ANIMACIONES
           ============================================================ */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Efecto glow en hover para cualquier elemento interactivo */
        button:hover, input:hover, select:hover {
            transition: all 0.3s ease !important;
        }
        
    </style>
    """, unsafe_allow_html=True)

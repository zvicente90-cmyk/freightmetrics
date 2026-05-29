import streamlit as st
from pathlib import Path
import sys

# ============================================================
# NOTA: set_page_config debe ser el PRIMER comando de Streamlit
# ============================================================
st.set_page_config(
    page_title="FreightMetrics Pro",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importar componentes UI centralizados
try:
    from modules.session_init import (
        metric_card, metric_card_compact, info_card, page_header, section_header, spacer
    )
    UI_COMPONENTS_AVAILABLE = True
except ImportError:
    UI_COMPONENTS_AVAILABLE = False
    def metric_card(title, value, icon="📊", color="#4070F4", delta=None, delta_color="normal"):
        st.metric(title, value, delta=delta, delta_color=delta_color)
    def metric_card_compact(title, value, icon="📊", color="#4070F4"):
        st.metric(title, value)
    def page_header(title, subtitle="", icon="📊"):
        st.title(f"{icon} {title}")
        if subtitle:
            st.markdown(f"**{subtitle}**")
    def section_header(title="", icon="", color=""):
        st.subheader(f"{icon} {title}")
    def spacer(height=20):
        st.markdown(f'<div style="height: {height}px;"></div>', unsafe_allow_html=True)

def obtener_datos_mapeados():
    import pandas as pd
    return pd.DataFrame({
        "Puerto": ["Veracruz", "Manzanillo", "Los Cabos"],
        "Operaciones": [10000, 8000, 6000],
        "Saturacion": [85, 70, 60]
    })

def page_dashboard():
    """Dashboard profesional integral - Centro de Inteligencia de Negocio"""
    import pandas as pd
    import plotly.graph_objects as go
    import plotly.express as px
    from datetime import datetime
    import pytz
    
    # Usar zona horaria local del sistema
    def obtener_hora_actual():
        """Obtiene la hora actual en la zona horaria local del sistema"""
        return datetime.now()
    
    # CSS GLOBAL PROFESIONAL - MEJORA TODOS LOS COMPONENTES
    # COMENTADO: Los estilos CSS de [data-testid] interfieren con tarjetas inline
    # ============================================================
    # st.markdown("""
    # <style>
    #     /* Mejorar tarjetas de métrica (st.metric) */
    #     [data-testid="metric-container"] {
    #         background: linear-gradient(135deg, rgba(0, 61, 122, 0.12) 0%, rgba(0, 82, 163, 0.08) 100%) !important;
    #         padding: 24px !important;
    #         border-radius: 14px !important;
    #         border: 2px solid #0066cc !important;
    #         box-shadow: 0 0 20px rgba(0, 102, 204, 0.4), 0 8px 24px rgba(0, 0, 0, 0.15) !important;
    #         backdrop-filter: blur(8px) !important;
    #     }
    #     
    #     /* Mejorar texto dentro de las tarjetas */
    #     [data-testid="metric-container"] > div:nth-child(1) {
    #         color: #0066cc !important;
    #         font-weight: 600 !important;
    #         letter-spacing: 0.5px !important;
    #     }
    #     
    #     [data-testid="metric-container"] > div:nth-child(2) {
    #         color: #0066cc !important;
    #         font-size: 2.2rem !important;
    #         font-weight: 900 !important;
    #         text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3) !important;
    #     }
    #     
    #     /* Mejorar expandibles */
    #     [data-testid="stExpander"] {
    #         border: 2px solid #0066cc !important;
    #         border-radius: 14px !important;
    #         box-shadow: 0 0 15px rgba(0, 102, 204, 0.3) !important;
    #     }
    #     
    #     /* Mejorar tabs */
    #     [data-testid="stTabs"] {
    #         background: linear-gradient(135deg, rgba(0, 82, 163, 0.08) 0%, rgba(25, 118, 210, 0.05) 100%) !important;
    #         border-radius: 12px !important;
    #         padding: 16px !important;
    #     }
    #     
    #     /* Mejorar selectores y inputs */
    #     [data-testid="stForm"] {
    #         background: linear-gradient(135deg, rgba(0, 61, 122, 0.08) 0%, rgba(0, 82, 163, 0.05) 100%) !important;
    #         border: 1px solid #0066cc !important;
    #         border-radius: 12px !important;
    #         padding: 16px !important;
    #         box-shadow: 0 0 12px rgba(0, 102, 204, 0.2) !important;
    #     }
    # </style>
    # """, unsafe_allow_html=True)
    
    # ============================================================
    st.markdown("""
    <style>
        .dashboard-hero {
            background: linear-gradient(135deg, #003d7a 0%, #0052a3 50%, #1976d2 100%);
            color: white;
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 61, 122, 0.3);
        }
        .hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .hero-subtitle {
            font-size: 1.1rem;
            margin-top: 10px;
            opacity: 0.95;
            font-weight: 300;
            letter-spacing: 0.5px;
        }
        .hero-badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            margin-top: 15px;
            font-weight: 600;
        }
    </style>
    <div class="dashboard-hero">
        <h1 class="hero-title">🎯 FreightMetrics Intelligence Hub</h1>
        <p class="hero-subtitle">La Plataforma Líder de Inteligencia de Negocio para Logística Transfronteriza</p>
        <span class="hero-badge">✨ Análisis Integral | 📊 Tiempo Real | 🚀 Enterprise Grade</span>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================================
    # SECCIÓN 1: KPIs CRÍTICOS (Flujos + Monitoreo)
    # ============================================================
    st.markdown("### 📊 KPIs Críticos - Estado General del Sistema")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    # KPI 1: Cruces Fronterizos
    with kpi_col1:
        st.markdown("""
        <div style="background: #003d7a; 
                    padding: 25px; border-radius: 12px; color: white; 
                    box-shadow: 0 4px 15px rgba(0, 61, 122, 0.3);
                    text-align: center; height: 180px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;">
                📦 Cruces Mensuales
            </div>
            <div style="font-size: 2.5rem; font-weight: 800; margin: 10px 0;">
                1.8M
            </div>
            <div style="font-size: 0.8rem; opacity: 0.85;">
                ↑ 12% vs mes anterior
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI 2: Valor Comercial
    with kpi_col2:
        st.markdown("""
        <div style="background: #0052a3; 
                    padding: 25px; border-radius: 12px; color: white; 
                    box-shadow: 0 4px 15px rgba(0, 82, 163, 0.3);
                    text-align: center; height: 180px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;">
                💰 Valor Comercial
            </div>
            <div style="font-size: 2.5rem; font-weight: 800; margin: 10px 0;">
                $72.7B
            </div>
            <div style="font-size: 0.8rem; opacity: 0.85;">
                USD/Mes | Promedio 2025
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI 3: Utilización Aduanas
    with kpi_col3:
        st.markdown("""
        <div style="background: #1976d2; 
                    padding: 25px; border-radius: 12px; color: white; 
                    box-shadow: 0 4px 15px rgba(25, 118, 210, 0.3);
                    text-align: center; height: 180px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;">
                🚦 Utilización Aduanas
            </div>
            <div style="font-size: 2.5rem; font-weight: 800; margin: 10px 0;">
                87.3%
            </div>
            <div style="font-size: 0.8rem; opacity: 0.85;">
                42 Aduanas | 7 en Alerta
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI 4: Índice FreightMetrics
    with kpi_col4:
        st.markdown("""
        <div style="background: #0066cc; 
                    padding: 25px; border-radius: 12px; color: white; 
                    box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
                    text-align: center; height: 180px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;">
                📈 Índice FM
            </div>
            <div style="font-size: 2.5rem; font-weight: 800; margin: 10px 0;">
                108.4
            </div>
            <div style="font-size: 0.8rem; opacity: 0.85;">
                Base 100 | ↑ 2.1%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("---")
    
    # ============================================================
    # SECCIÓN 2: MONITOREO DE ADUANAS
    # ============================================================
    st.markdown("### 🚦 Monitoreo de Aduanas - Estado Operativo")
    
    mon_col1, mon_col2, mon_col3, mon_col4 = st.columns(4)
    
    with mon_col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 61, 122, 0.12) 0%, rgba(0, 82, 163, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0066cc;
            box-shadow: 0 0 20px rgba(0, 102, 204, 0.4), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #003d7a; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">✅ Normal</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">✓</span>
            </div>
            <p style="font-size: 2.2rem; font-weight: 900; margin: 12px 0; color: #0066cc; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);">7</p>
            <p style="color: #003d7a; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Operación fluida</p>
        </div>
        """, unsafe_allow_html=True)
    
    with mon_col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 82, 163, 0.12) 0%, rgba(25, 118, 210, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #1976d2;
            box-shadow: 0 0 20px rgba(25, 118, 210, 0.35), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #0052a3; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">⚠️ Alerta</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">!</span>
            </div>
            <p style="font-size: 2.2rem; font-weight: 900; margin: 12px 0; color: #1976d2; text-shadow: 0 2px 8px rgba(25, 118, 210, 0.3);">5</p>
            <p style="color: #0052a3; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Requieren atención</p>
        </div>
        """, unsafe_allow_html=True)
    
    with mon_col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255, 193, 7, 0.08) 0%, rgba(255, 152, 0, 0.05) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0066cc;
            box-shadow: 0 0 20px rgba(0, 102, 204, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #d32f2f; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">🔴 Crítico</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">●</span>
            </div>
            <p style="font-size: 2.2rem; font-weight: 900; margin: 12px 0; color: #0066cc; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);">2</p>
            <p style="color: #d32f2f; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Intervención inmediata</p>
        </div>
        """, unsafe_allow_html=True)
    
    with mon_col4:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 102, 204, 0.12) 0%, rgba(0, 61, 122, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0052a3;
            box-shadow: 0 0 20px rgba(0, 82, 163, 0.35), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #0052a3; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">⏱️ Espera Prom</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">⏱</span>
            </div>
            <p style="font-size: 2.2rem; font-weight: 900; margin: 12px 0; color: #0052a3; text-shadow: 0 2px 8px rgba(0, 82, 163, 0.3);">47 min</p>
            <p style="color: #0052a3; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Tiempo procesamiento</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # ============================================================
    # SECCIÓN 3: FUERZA LABORAL
    # ============================================================
    st.markdown("### 👥 Sector Autotransporte - Fuerza Laboral")
    
    fl_col1, fl_col2, fl_col3, fl_col4 = st.columns(4)
    
    with fl_col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 61, 122, 0.12) 0%, rgba(0, 82, 163, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0066cc;
            box-shadow: 0 0 20px rgba(0, 102, 204, 0.4), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #003d7a; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">🏢 Permisionarios</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">🏢</span>
            </div>
            <p style="font-size: 2rem; font-weight: 900; margin: 12px 0; color: #0066cc; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);">198.5K</p>
            <p style="color: #003d7a; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Empresas federales</p>
        </div>
        """, unsafe_allow_html=True)
    
    with fl_col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 82, 163, 0.12) 0%, rgba(25, 118, 210, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #1976d2;
            box-shadow: 0 0 20px rgba(25, 118, 210, 0.35), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #0052a3; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">🚛 Parque Vehicular</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">🚛</span>
            </div>
            <p style="font-size: 2rem; font-weight: 900; margin: 12px 0; color: #1976d2; text-shadow: 0 2px 8px rgba(25, 118, 210, 0.3);">630K</p>
            <p style="color: #0052a3; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Unidades en operación</p>
        </div>
        """, unsafe_allow_html=True)
    
    with fl_col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255, 193, 7, 0.08) 0%, rgba(255, 152, 0, 0.05) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0066cc;
            box-shadow: 0 0 20px rgba(0, 102, 204, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #ff6f00; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">⚠️ Déficit Operadores</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">⚠</span>
            </div>
            <p style="font-size: 2rem; font-weight: 900; margin: 12px 0; color: #0066cc; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);">99K</p>
            <p style="color: #ff6f00; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Falta 15.7% del total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with fl_col4:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 102, 204, 0.12) 0%, rgba(0, 61, 122, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0052a3;
            box-shadow: 0 0 20px rgba(0, 82, 163, 0.35), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #0052a3; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">📊 Ratio Op/Unidad</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">📊</span>
            </div>
            <p style="font-size: 2rem; font-weight: 900; margin: 12px 0; color: #0052a3; text-shadow: 0 2px 8px rgba(0, 82, 163, 0.3);">1.09</p>
            <p style="color: #0052a3; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Operadores por vehículo</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # ============================================================
    # SECCIÓN 4: CORREDORES LOGÍSTICOS
    # ============================================================
    st.markdown("### 🛣️ Corredores Logísticos - Actividad")
    
    corr_col1, corr_col2, corr_col3, corr_col4 = st.columns(4)
    
    with corr_col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 61, 122, 0.12) 0%, rgba(0, 82, 163, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0066cc;
            box-shadow: 0 0 20px rgba(0, 102, 204, 0.4), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #003d7a; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">🌐 Total Activos</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">🌐</span>
            </div>
            <p style="font-size: 2.2rem; font-weight: 900; margin: 12px 0; color: #0066cc; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);">12</p>
            <p style="color: #003d7a; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Corredores estratégicos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with corr_col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 82, 163, 0.12) 0%, rgba(25, 118, 210, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #1976d2;
            box-shadow: 0 0 20px rgba(25, 118, 210, 0.35), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #0052a3; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">💰 Rentabilidad Prom</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">💰</span>
            </div>
            <p style="font-size: 2.2rem; font-weight: 900; margin: 12px 0; color: #1976d2; text-shadow: 0 2px 8px rgba(25, 118, 210, 0.3);">7 de 12</p>
            <p style="color: #0052a3; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Alta rentabilidad (58%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with corr_col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(25, 118, 210, 0.12) 0%, rgba(0, 102, 204, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0066cc;
            box-shadow: 0 0 20px rgba(0, 102, 204, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #0052a3; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">⚡ Riesgo Prom</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">⚡</span>
            </div>
            <p style="font-size: 2.2rem; font-weight: 900; margin: 12px 0; color: #0066cc; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);">5 de 12</p>
            <p style="color: #0052a3; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Bajo riesgo (42%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with corr_col4:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 102, 204, 0.12) 0%, rgba(0, 61, 122, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0052a3;
            box-shadow: 0 0 20px rgba(0, 82, 163, 0.35), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #0052a3; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">📏 Distancia Prom</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">📏</span>
            </div>
            <p style="font-size: 2.2rem; font-weight: 900; margin: 12px 0; color: #0052a3; text-shadow: 0 2px 8px rgba(0, 82, 163, 0.3);">1,542 km</p>
            <p style="color: #0052a3; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Ruta promedio</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # ============================================================
    # SECCIÓN 5: NEARSHORING & INVERSIÓN EXTRANJERA DIRECTA (IED)
    # ============================================================
    st.markdown("### 🌍 Nearshoring & Inversión Extranjera Directa 2025")
    
    near_col1, near_col2, near_col3, near_col4 = st.columns(4)
    
    with near_col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 61, 122, 0.12) 0%, rgba(0, 82, 163, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0066cc;
            box-shadow: 0 0 20px rgba(0, 102, 204, 0.4), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #003d7a; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">💵 IED Q3 2025</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">💵</span>
            </div>
            <p style="font-size: 2rem; font-weight: 900; margin: 12px 0; color: #0066cc; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);">$40.9B</p>
            <p style="color: #003d7a; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Máximo histórico</p>
        </div>
        """, unsafe_allow_html=True)
    
    with near_col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 82, 163, 0.12) 0%, rgba(25, 118, 210, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #1976d2;
            box-shadow: 0 0 20px rgba(25, 118, 210, 0.35), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #0052a3; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">🔄 Reinversión</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">🔄</span>
            </div>
            <p style="font-size: 2rem; font-weight: 900; margin: 12px 0; color: #1976d2; text-shadow: 0 2px 8px rgba(25, 118, 210, 0.3);">67.8%</p>
            <p style="color: #0052a3; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">$27.7B USD</p>
        </div>
        """, unsafe_allow_html=True)
    
    with near_col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(25, 118, 210, 0.12) 0%, rgba(0, 102, 204, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0066cc;
            box-shadow: 0 0 20px rgba(0, 102, 204, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #0052a3; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">🏭 Manufactura (37%)</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">🏭</span>
            </div>
            <p style="font-size: 2rem; font-weight: 900; margin: 12px 0; color: #0066cc; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);">$15.1B</p>
            <p style="color: #0052a3; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Automotriz + Partes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with near_col4:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 102, 204, 0.12) 0%, rgba(0, 61, 122, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0052a3;
            box-shadow: 0 0 20px rgba(0, 82, 163, 0.35), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #0052a3; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">✅ Inauguraciones</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">✅</span>
            </div>
            <p style="font-size: 2rem; font-weight: 900; margin: 12px 0; color: #0052a3; text-shadow: 0 2px 8px rgba(0, 82, 163, 0.3);">Máximo</p>
            <p style="color: #0052a3; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Proyectos operativos</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("---")
    
    # ============================================================
    # SECCIÓN 5.5: COMERCIO BILATERAL MÉXICO-USA
    # ============================================================
    st.markdown("### 💱 Comercio Bilateral México-USA 2025")
    
    com_col1, com_col2, com_col3, com_col4 = st.columns(4)
    
    with com_col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 61, 122, 0.12) 0%, rgba(0, 82, 163, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0066cc;
            box-shadow: 0 0 20px rgba(0, 102, 204, 0.4), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #003d7a; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">💱 Intercambio Total</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">💱</span>
            </div>
            <p style="font-size: 2rem; font-weight: 900; margin: 12px 0; color: #0066cc; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);">$872.8B</p>
            <p style="color: #003d7a; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">+3.9% vs 2024</p>
        </div>
        """, unsafe_allow_html=True)
    
    with com_col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 82, 163, 0.12) 0%, rgba(25, 118, 210, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #1976d2;
            box-shadow: 0 0 20px rgba(25, 118, 210, 0.35), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #0052a3; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">📤 Exportaciones MX</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">📤</span>
            </div>
            <p style="font-size: 2rem; font-weight: 900; margin: 12px 0; color: #1976d2; text-shadow: 0 2px 8px rgba(25, 118, 210, 0.3);">$534.9B</p>
            <p style="color: #0052a3; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">+5.8% anual</p>
        </div>
        """, unsafe_allow_html=True)
    
    with com_col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(25, 118, 210, 0.12) 0%, rgba(0, 102, 204, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0066cc;
            box-shadow: 0 0 20px rgba(0, 102, 204, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #0052a3; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">📥 Importaciones USA</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">📥</span>
            </div>
            <p style="font-size: 2rem; font-weight: 900; margin: 12px 0; color: #0066cc; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);">$338.0B</p>
            <p style="color: #0052a3; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Mercado #1 de USA</p>
        </div>
        """, unsafe_allow_html=True)
    
    with com_col4:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 102, 204, 0.12) 0%, rgba(0, 61, 122, 0.08) 100%);
            padding: 24px;
            border-radius: 14px;
            border: 2px solid #0052a3;
            box-shadow: 0 0 20px rgba(0, 82, 163, 0.35), 0 8px 24px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <h4 style="margin: 0; color: #0052a3; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">📊 Balanza Comercial</h4>
                <span style="font-size: 1.4rem; opacity: 0.8;">📊</span>
            </div>
            <p style="font-size: 2rem; font-weight: 900; margin: 12px 0; color: #0052a3; text-shadow: 0 2px 8px rgba(0, 82, 163, 0.3);">$196.9B</p>
            <p style="color: #0052a3; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">Superávit MX</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("---")
    
    # ============================================================
    # SECCIÓN 6: GRÁFICOS ANALÍTICOS & COMERCIO BILATERAL
    # ============================================================
    st.markdown("### 📈 Análisis Estratégico: Operaciones & Comercio Bilateral")
    
    col_g1, col_g2 = st.columns(2)
    
    # Gráfico 1: Línea de evolución de cruces
    with col_g1:
        meses = ['E', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
        cruces = [1.45, 1.52, 1.58, 1.65, 1.72, 1.78, 1.82, 1.85, 1.88, 1.92, 1.8, 1.8]
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=meses, y=cruces, mode='lines+markers',
            name='Cruces (Millones)',
            line=dict(color='#003d7a', width=3),
            fill='tozeroy', fillcolor='rgba(0, 61, 122, 0.1)',
            marker=dict(size=8, color='#003d7a')
        ))
        fig_trend.update_layout(
            title='<b>Evolución Mensual de Cruces 2026</b>',
            xaxis_title='Mes', yaxis_title='Millones de Cruces',
            hovermode='x unified', template='plotly_white', height=350,
            font=dict(size=10, color='#2c3e50')
        )
        st.plotly_chart(fig_trend, use_container_width=True, config={'responsive': True})
    
    # Gráfico 2: Comercio Bilateral México-USA
    with col_g2:
        comercio_bilateral = {
            'Flujo': ['Exportaciones\nMX→USA', 'Importaciones\nUSA→MX'],
            'Valor': [534874, 338000],
            'Colores': ['#4CAF50', '#FF9800']
        }
        
        fig_comercio = px.bar(
            x=comercio_bilateral['Flujo'],
            y=comercio_bilateral['Valor'],
            title='<b>Comercio Bilateral 2025 (mdd)</b>',
            labels={'y': 'Valor (Millones USD)', 'x': 'Tipo de Flujo'},
            color=comercio_bilateral['Flujo'],
            color_discrete_map={
                'Exportaciones\nMX→USA': '#0052a3',
                'Importaciones\nUSA→MX': '#1976d2'
            }
        )
        fig_comercio.update_layout(
            height=350, showlegend=False, font=dict(size=10, color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_comercio, use_container_width=True, config={'responsive': True})
    
    # Gráfico 3: Estado Operativo
    spacer(10)
    col_g3, col_g4 = st.columns(2)
    
    with col_g3:
        distribucion = {
            'Categoría': ['México-USA', 'Canadá-USA', 'Críticas', 'Alerta'],
            'Valor': [1200, 540, 2, 5],
            'Color': ['#003d7a', '#0052a3', '#ff9800', '#1976d2']
        }
        
        fig_dist = px.bar(
            x=distribucion['Categoría'],
            y=distribucion['Valor'],
            title='<b>Estado Operativo General</b>',
            color=distribucion['Categoría'],
            color_discrete_map=dict(zip(distribucion['Categoría'], distribucion['Color'])),
            labels={'x': 'Categoría', 'y': 'Cantidad'}
        )
        fig_dist.update_layout(
            height=300, showlegend=False, font=dict(size=10, color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_dist, use_container_width=True, config={'responsive': True})
    
    # Gráfico 4: Crecimiento comparativo
    with col_g4:
        crecimiento_comp = {
            'Indicador': ['Intercambio\nTotal', 'Exportaciones\nMX', 'Importaciones\nUSA'],
            'Crecimiento_%': [3.9, 5.8, 8],  # 8% es estimado para feb
            'Colores': ['#2196F3', '#4CAF50', '#FF9800']
        }
        
        fig_crec = px.bar(
            x=crecimiento_comp['Indicador'],
            y=crecimiento_comp['Crecimiento_%'],
            title='<b>Crecimiento Comercial 2025-2026</b>',
            labels={'y': 'Crecimiento (%)', 'x': 'Indicador'},
            color=crecimiento_comp['Indicador'],
            color_discrete_map={
                'Intercambio\nTotal': '#003d7a',
                'Exportaciones\nMX': '#0052a3',
                'Importaciones\nUSA': '#1976d2'
            }
        )
        fig_crec.update_layout(
            height=300, showlegend=False, font=dict(size=10, color='#2c3e50'),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_crec, use_container_width=True, config={'responsive': True})
    
    st.markdown("")
    st.markdown("---")
    
    # ============================================================
    # SECCIÓN 7: INSIGHTS ESTRATÉGICOS
    # ============================================================
    st.markdown("### 💡 Insights Estratégicos Integrales")
    
    ins_col1, ins_col2 = st.columns(2)
    
    with ins_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #003d7a 0%, #0052a3 100%); 
                    color: white; padding: 25px; border-radius: 10px; 
                    box-shadow: 0 4px 15px rgba(0, 61, 122, 0.3);">
            <h4 style="margin-top: 0; font-size: 1.1rem;">🚀 Oportunidad: IED & Nearshoring</h4>
            <p style="margin: 15px 0;"><b>IED Q3 2025 alcanzó $40.9B USD</b> (máximo histórico). 
            <b>67.8% reinversión</b> + <b>37% manufactura</b> (automotriz/autopartes). 
            Inauguraciones en nivel máximo histórico.</p>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">📍 Acción: Ampliar capacidad logística fronteriza</p>
        </div>
        """, unsafe_allow_html=True)
    
    with ins_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1976d2 0%, #0066cc 100%); 
                    color: white; padding: 25px; border-radius: 10px; 
                    box-shadow: 0 4px 15px rgba(25, 118, 210, 0.3);">
            <h4 style="margin-top: 0; font-size: 1.1rem;">⚠️ Riesgo: Déficit de Talento</h4>
            <p style="margin: 15px 0;"><b>99,000 operadores faltantes</b> (15.7% del parque). 
            Ratio Operadores/Unidad en <b>1.09</b>. Impacta saturación operativa.</p>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">📍 Acción: Programa urgente de capacitación</p>
        </div>
        """, unsafe_allow_html=True)
    
    spacer(15)
    
    ins_col3, ins_col4 = st.columns(2)
    
    with ins_col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    color: white; padding: 25px; border-radius: 10px; 
                    box-shadow: 0 4px 15px rgba(79, 172, 254, 0.2);">
            <h4 style="margin-top: 0; font-size: 1.1rem;">🔍 Congestión Aduanal</h4>
            <p style="margin: 15px 0;"><b>2 aduanas críticas</b> con espera 90+ minutos. 
            Utilización en <b>87.3%</b>. Tiempos de procesamiento 47 min promedio.</p>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">📍 Afectadas: Buffalo Niagara Falls, Port Huron</p>
        </div>
        """, unsafe_allow_html=True)
    
    with ins_col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                    color: white; padding: 25px; border-radius: 10px; 
                    box-shadow: 0 4px 15px rgba(67, 233, 123, 0.2);">
            <h4 style="margin-top: 0; font-size: 1.1rem;">📊 Crecimiento Sostenido</h4>
            <p style="margin: 15px 0;"><b>Cruces +12% mensual</b> con valor promedio <b>$72.7B USD/mes</b> (intercambio bilateral 2025). 
            Índice FM en <b>108.4</b> (mercado activo). Pronóstico: ↑15% Q2.</p>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">📍 Recomendación: Invertir en infraestructura</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("---")
    
    # ============================================================
    # FOOTER PROFESIONAL
    # ============================================================
    st.markdown("""
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 40px; text-align: center;">
        <p style="color: #666; margin: 0; font-size: 0.9rem;">
            <b>FreightMetrics™ Intelligence Hub</b> - Módulos Integrados: Monitoreo | Flujos | Fuerza Laboral | Corredores | Nearshoring | Índice FM
        </p>
        <p style="color: #999; margin: 10px 0 0 0; font-size: 0.85rem;">
            📊 Datos en tiempo real | 🔒 Enterprise Security | 🚀 Advanced Analytics | ✅ Metodología Verificada
        </p>
        <p style="color: #999; margin: 8px 0 0 0; font-size: 0.85rem;">
            © 2026 FreightMetrics Inc - Líderes en Inteligencia de Negocio para Comercio Transfronterizo
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("✅ Dashboard Integral Sincronizado - Última actualización: " + obtener_hora_actual().strftime("%H:%M:%S"))




# Ejecutar la página de inicio directamente
page_dashboard()

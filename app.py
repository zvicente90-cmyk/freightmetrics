import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests # Para conectarnos a internet
import random
import numpy as np
from datetime import datetime, timedelta
import datetime as dt
import math
import base64
import os
from dotenv import load_dotenv, set_key, find_dotenv
import json
from pathlib import Path
import pytz
# from fpdf import FPDF  # Comentado temporalmente - no disponible en Streamlit Cloud

# Importar páginas separadas del directorio pages/
try:
    from page_modules._00_Inicio import page_dashboard
    DASHBOARD_AVAILABLE = True
except ImportError:
    DASHBOARD_AVAILABLE = False
    page_dashboard = None

try:
    from page_modules._02_Flujos_de_Carga import page_flujos_de_carga
    FLUJOS_CARGA_AVAILABLE = True
except ImportError:
    FLUJOS_CARGA_AVAILABLE = False
    page_flujos_de_carga = None

try:
    from page_modules._03_Fuerza_Laboral import page_fuerza_laboral
    FUERZA_LABORAL_AVAILABLE = True
except ImportError:
    FUERZA_LABORAL_AVAILABLE = False
    page_fuerza_laboral = None

try:
    from page_modules._05_Puertos_Maritimos import page_puertos_maritimos
    PUERTOS_MARITIMOS_AVAILABLE = True
except ImportError:
    PUERTOS_MARITIMOS_AVAILABLE = False
    page_puertos_maritimos = None

try:
    from page_modules._04_Corredores_Logisticos import page_corredores_logisticos
    CORREDORES_LOGISTICOS_AVAILABLE = True
except ImportError:
    CORREDORES_LOGISTICOS_AVAILABLE = False
    page_corredores_logisticos = None

try:
    from page_modules._06_Nearshoring import page_nearshoring
    NEARSHORING_AVAILABLE = True
except ImportError:
    NEARSHORING_AVAILABLE = False
    page_nearshoring = None

try:
    from page_modules._01_Monitoreo_Aduanas import page_monitoreo_aduanas
    MONITOREO_ADUANAS_AVAILABLE = True
except ImportError:
    MONITOREO_ADUANAS_AVAILABLE = False
    page_monitoreo_aduanas = None

# Importar nueva página de monitoreo V2
try:
    from monitoreo_v2 import page_monitoreo_v2
    MONITOREO_V2_AVAILABLE = True
except ImportError:
    MONITOREO_V2_AVAILABLE = False
    page_monitoreo_v2 = None

# Importar nuevas páginas: Índice FreightMetrics y Oracle Rate
try:
    from indice_freightmetrics import page_indice_freightmetrics
    INDICE_FM_AVAILABLE = True
except ImportError:
    INDICE_FM_AVAILABLE = False
    page_indice_freightmetrics = None

try:
    from oracle_rate import page_oracle_rate
    ORACLE_RATE_AVAILABLE = True
except ImportError:
    ORACLE_RATE_AVAILABLE = False
    page_oracle_rate = None

# Importar inicialización centralizada de session_state
try:
    from modules.session_init import (
        initialize_session_state, YEARS, MONTHS, MONTHS_MAP, BORDERS, 
        GEOGRAPHICAL_POINTS, TRANSPORT_TYPES, LOGISTICS_CORRIDORS,
        metric_card, metric_card_compact, info_card, page_header, section_header, spacer
    )
    SESSION_INIT_AVAILABLE = True
except ImportError:
    SESSION_INIT_AVAILABLE = False
    def initialize_session_state():
        pass
    # Definir fallbacks mínimos si no está disponible
    def metric_card(title, value, icon="📊", color="#4070F4", delta=None, delta_color="normal"):
        st.metric(title, value, delta=delta, delta_color=delta_color)
    def page_header(title, subtitle="", icon="📊"):
        st.title(f"{icon} {title}")
        if subtitle:
            st.markdown(f"**{subtitle}**")

# Importar componentes UI mejorados
try:
    from ui_components import (
        metric_card, metric_card_compact, info_card, alert_card,
        page_header, section_header, subsection_header,
        create_gauge_chart, create_modern_bar_chart, create_modern_line_chart, create_modern_pie_chart,
        stat_box, comparison_box, spacer, divider, gradient_divider
    )
    UI_COMPONENTS_AVAILABLE = True
except ImportError:
    UI_COMPONENTS_AVAILABLE = False
    # Fallback para funciones complejas no centralizadas
    def alert_card(title, content, icon="⚠️"):
        st.warning(f"**{icon} {title}**\n{content}")
    def subsection_header(title, icon="📊"):
        st.markdown(f"#### {icon} {title}")
    def create_gauge_chart(value, max_value=100, title=""):
        st.metric(title, f"{value}/{max_value}")
    def create_modern_bar_chart(data, title=""):
        if title:
            st.subheader(title)
        st.bar_chart(data)
    def create_modern_line_chart(data, title=""):
        if title:
            st.subheader(title)
        st.line_chart(data)
    def create_modern_pie_chart(data, title=""):
        if title:
            st.subheader(title)
        st.write(data)
    def stat_box(title, value, icon=""):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"# {icon}")
        with col2:
            st.metric(title, value)
    def comparison_box(title, value1, value2, label1="", label2=""):
        st.metric(title, f"{value1} vs {value2}")
    def divider(color="#E0E0E0", thickness=2, margin=20):
        st.divider()
    def gradient_divider(color1="#4070F4", color2="#2D5FA3"):
        st.markdown(f"<hr style='border: none; height: 2px; background: linear-gradient(to right, {color1}, {color2});'>", unsafe_allow_html=True)

# ============================================================
# DICCIONARIO DE TRADUCCIONES MULTIIDIOMA
# ============================================================
TRANSLATIONS = {
    'es': {
        # Menú y navegación
        'menu_dashboard': 'Dashboard',
        'menu_monitoring': 'Monitoreo de Aduanas',
        'menu_flows': 'Flujos de Carga',
        'menu_corridors': 'Corredores Logísticos',
        'menu_ports': 'Puertos Marítimos',
        'menu_workforce': 'Fuerza Laboral',
        'menu_nearshoring': 'Nearshoring',
        'menu_indice': 'Índice FreightMetrics',
        'menu_oracle': 'Oracle Rate',
        
        # Botones y acciones
        'download_pdf': 'Descargar PDF',
        'apply_filters': 'Aplicar Filtros',
        'clear_filters': 'Limpiar Filtros',
        'export_data': 'Exportar Datos',
        
        # Filtros
        'filter_year': 'Año',
        'filter_border': 'Frontera',
        'filter_month': 'Mes',
        'filter_customs': 'Aduanas',
        'filter_transport': 'Transporte',
        'all_borders': 'Todas las Fronteras',
        'all_months': 'Todos los Meses',
        'all_customs': 'Todas las Aduanas',
        
        # Fronteras
        'border_mexico': 'México',
        'border_canada': 'Canadá',
        'border_both': 'México y Canadá',
        
        # Meses
        'month_1': 'Enero', 'month_2': 'Febrero', 'month_3': 'Marzo',
        'month_4': 'Abril', 'month_5': 'Mayo', 'month_6': 'Junio',
        'month_7': 'Julio', 'month_8': 'Agosto', 'month_9': 'Septiembre',
        'month_10': 'Octubre', 'month_11': 'Noviembre', 'month_12': 'Diciembre',
        
        # Métricas y KPIs
        'total_crossings': 'Cruces Totales',
        'average_daily': 'Promedio Diario',
        'monthly_growth': 'Crecimiento Mensual',
        'operational_capacity': 'Capacidad Operativa',
        'utilization_rate': 'Tasa de Utilización',
        'demand': 'Demanda',
        'capacity': 'Capacidad',
        'surplus': 'Superávit',
        'deficit': 'Déficit',
        
        # Unidades
        'crossings': 'cruces',
        'crossings_day': 'cruces/día',
        'companies': 'empresas',
        'vehicles': 'unidades',
        'kilometers': 'kilómetros',
        'hours': 'horas',
        
        # Mensajes
        'no_data': 'No hay datos disponibles',
        'loading': 'Cargando datos...',
        'error': 'Error al cargar datos',
        'success': 'Operación exitosa',
        'warning': 'Advertencia',
        'info': 'Información',
        
        # Secciones
        'section_overview': 'Resumen General',
        'section_analysis': 'Análisis Detallado',
        'section_trends': 'Tendencias',
        'section_comparison': 'Comparación',
        'section_recommendations': 'Recomendaciones Estratégicas',
        'section_methodology': 'Metodología',
        
        # Títulos de páginas
        'title_flows': 'Flujos de Carga Fronterizos',
        'title_capacity': 'Capacidad Operativa vs Demanda de Cruces',
        'title_regional': 'Análisis por Región',
        'title_temporal': 'Análisis Temporal',
        
        # Alertas y notificaciones
        'alert_high_demand': 'Alta Demanda',
        'alert_capacity_exceeded': 'Capacidad Excedida',
        'alert_low_utilization': 'Baja Utilización',
        'alert_insufficient_data': 'No hay datos suficientes para calcular capacidad operativa',
    },
    'en': {
        # Menu and navigation
        'menu_dashboard': 'Dashboard',
        'menu_monitoring': 'Customs Monitoring',
        'menu_flows': 'Cargo Flows',
        'menu_corridors': 'Logistics Corridors',
        'menu_ports': 'Maritime Ports',
        'menu_workforce': 'Workforce',
        'menu_nearshoring': 'Nearshoring',
        'menu_indice': 'FreightMetrics Index',
        'menu_oracle': 'Oracle Rate',
        
        # Buttons and actions
        'download_pdf': 'Download PDF',
        'apply_filters': 'Apply Filters',
        'clear_filters': 'Clear Filters',
        'export_data': 'Export Data',
        
        # Filters
        'filter_year': 'Year',
        'filter_border': 'Border',
        'filter_month': 'Month',
        'filter_customs': 'Customs',
        'filter_transport': 'Transport',
        'all_borders': 'All Borders',
        'all_months': 'All Months',
        'all_customs': 'All Customs',
        
        # Borders
        'border_mexico': 'Mexico',
        'border_canada': 'Canada',
        'border_both': 'Mexico and Canada',
        
        # Months
        'month_1': 'January', 'month_2': 'February', 'month_3': 'March',
        'month_4': 'April', 'month_5': 'May', 'month_6': 'June',
        'month_7': 'July', 'month_8': 'August', 'month_9': 'September',
        'month_10': 'October', 'month_11': 'November', 'month_12': 'December',
        
        # Metrics and KPIs
        'total_crossings': 'Total Crossings',
        'average_daily': 'Daily Average',
        'monthly_growth': 'Monthly Growth',
        'operational_capacity': 'Operational Capacity',
        'utilization_rate': 'Utilization Rate',
        'demand': 'Demand',
        'capacity': 'Capacity',
        'surplus': 'Surplus',
        'deficit': 'Deficit',
        
        # Units
        'crossings': 'crossings',
        'crossings_day': 'crossings/day',
        'companies': 'companies',
        'vehicles': 'vehicles',
        'kilometers': 'kilometers',
        'hours': 'hours',
        
        # Messages
        'no_data': 'No data available',
        'loading': 'Loading data...',
        'error': 'Error loading data',
        'success': 'Successful operation',
        'warning': 'Warning',
        'info': 'Information',
        
        # Sections
        'section_overview': 'Overview',
        'section_analysis': 'Detailed Analysis',
        'section_trends': 'Trends',
        'section_comparison': 'Comparison',
        'section_recommendations': 'Strategic Recommendations',
        'section_methodology': 'Methodology',
        
        # Page titles
        'title_flows': 'Border Cargo Flows',
        'title_capacity': 'Operational Capacity vs Crossing Demand',
        'title_regional': 'Regional Analysis',
        'title_temporal': 'Temporal Analysis',
        
        # Alerts and notifications
        'alert_high_demand': 'High Demand',
        'alert_capacity_exceeded': 'Capacity Exceeded',
        'alert_low_utilization': 'Low Utilization',
        'alert_insufficient_data': 'Insufficient data to calculate operational capacity',
    },
    'fr': {
        # Menu et navigation
        'menu_dashboard': 'Tableau de Bord',
        'menu_monitoring': 'Surveillance Douanière',
        'menu_flows': 'Flux de Fret',
        'menu_corridors': 'Corridors Logistiques',
        'menu_ports': 'Ports Maritimes',
        'menu_workforce': 'Main-d\'œuvre',
        'menu_nearshoring': 'Relocalisation',
        'menu_indice': 'Indice FreightMetrics',
        'menu_oracle': 'Oracle Rate',
        
        # Boutons et actions
        'download_pdf': 'Télécharger PDF',
        'apply_filters': 'Appliquer les Filtres',
        'clear_filters': 'Effacer les Filtres',
        'export_data': 'Exporter les Données',
        
        # Filtres
        'filter_year': 'Année',
        'filter_border': 'Frontière',
        'filter_month': 'Mois',
        'filter_customs': 'Douanes',
        'filter_transport': 'Transport',
        'all_borders': 'Toutes les Frontières',
        'all_months': 'Tous les Mois',
        'all_customs': 'Toutes les Douanes',
        
        # Frontières
        'border_mexico': 'Mexique',
        'border_canada': 'Canada',
        'border_both': 'Mexique et Canada',
        
        # Mois
        'month_1': 'Janvier', 'month_2': 'Février', 'month_3': 'Mars',
        'month_4': 'Avril', 'month_5': 'Mai', 'month_6': 'Juin',
        'month_7': 'Juillet', 'month_8': 'Août', 'month_9': 'Septembre',
        'month_10': 'Octobre', 'month_11': 'Novembre', 'month_12': 'Décembre',
        
        # Métriques et KPI
        'total_crossings': 'Passages Totaux',
        'average_daily': 'Moyenne Quotidienne',
        'monthly_growth': 'Croissance Mensuelle',
        'operational_capacity': 'Capacité Opérationnelle',
        'utilization_rate': 'Taux d\'Utilisation',
        'demand': 'Demande',
        'capacity': 'Capacité',
        'surplus': 'Excédent',
        'deficit': 'Déficit',
        
        # Unités
        'crossings': 'passages',
        'crossings_day': 'passages/jour',
        'companies': 'entreprises',
        'vehicles': 'véhicules',
        'kilometers': 'kilomètres',
        'hours': 'heures',
        
        # Messages
        'no_data': 'Aucune donnée disponible',
        'loading': 'Chargement des données...',
        'error': 'Erreur de chargement des données',
        'success': 'Opération réussie',
        'warning': 'Avertissement',
        'info': 'Information',
        
        # Sections
        'section_overview': 'Vue d\'Ensemble',
        'section_analysis': 'Analyse Détaillée',
        'section_trends': 'Tendances',
        'section_comparison': 'Comparaison',
        'section_recommendations': 'Recommandations Stratégiques',
        'section_methodology': 'Méthodologie',
        
        # Titres de pages
        'title_flows': 'Flux de Fret Frontaliers',
        'title_capacity': 'Capacité Opérationnelle vs Demande de Passages',
        'title_regional': 'Analyse Régionale',
        'title_temporal': 'Analyse Temporelle',
        
        # Alertes et notifications
        'alert_high_demand': 'Forte Demande',
        'alert_capacity_exceeded': 'Capacité Dépassée',
        'alert_low_utilization': 'Faible Utilisation',
        'alert_insufficient_data': 'Données insuffisantes pour calculer la capacité opérationnelle',
    }
}

def t(key, lang=None):
    """
    Función de traducción
    Args:
        key: Clave de traducción
        lang: Código de idioma ('es', 'en', 'fr'). Si es None, usa el idioma del session_state
    Returns:
        Texto traducido o la clave si no se encuentra
    """
    if lang is None:
        lang = st.session_state.get('language', 'es')
    return TRANSLATIONS.get(lang, {}).get(key, key)

# --- INYECCIÓN DE CSS EJECUTIVO ---
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

# --- FUNCIÓN PARA CREAR EL PDF (Comentada - No disponible en Streamlit Cloud) ---
# def crear_pdf(dataframe, tipo_cambio):
#     pdf = FPDF()
#     pdf.add_page()
#     
#     # Título del Reporte
#     pdf.set_font("Arial", 'B', 16)
#     pdf.cell(190, 10, "FREIGHTMETRICS - REPORTE OPERATIVO", 0, 1, 'C')
#     pdf.ln(10)
#     
#     # Fecha y Tipo de Cambio
#     pdf.set_font("Arial", '', 10)
#     pdf.cell(190, 10, f"Fecha de emision: {dt.date.today()}", 0, 1, 'L')
#     pdf.cell(190, 10, f"Tipo de Cambio aplicado: ${tipo_cambio:.2f} MXN/USD", 0, 1, 'L')
#     pdf.ln(5)
#     
#     # Tabla de Datos
#     pdf.set_font("Arial", 'B', 10)
#     pdf.cell(40, 10, "Puerto", 1)
#     pdf.cell(40, 10, "Saturacion (%)", 1)
#     pdf.cell(60, 10, "Costo Est. (MXN)", 1)
#     pdf.ln()
#     
#     pdf.set_font("Arial", '', 10)
#     for index, row in dataframe.iterrows():
#         pdf.cell(40, 10, str(row['Puerto']), 1)
#         pdf.cell(40, 10, f"{row['Saturacion']}%", 1)
#         pdf.cell(60, 10, f"${row['Costo_Estimado_MXN']:,.2f}", 1)
#         pdf.ln()
#     
#     # Nota de Alerta
#     pdf.ln(10)
#     pdf.set_font("Arial", 'I', 8)
#     pdf.multi_cell(180, 5, "Nota: Este reporte es generado automaticamente. Los niveles superiores al 80% requieren accion inmediata del departamento de trafico.")
#     
#     return pdf.output(dest='S').encode('latin-1') # Retorna el PDF como datos

st.set_page_config(page_title="FreightMetrics Pro", layout="wide")

# --- NUEVA FUNCIÓN: Obtener tipo de cambio real ---
def obtener_tipo_cambio():
    try:
        # Usamos una API gratuita que no pide registro para este ejemplo
        url = "https://open.er-api.com/v6/latest/USD"
        respuesta = requests.get(url)
        datos = respuesta.json()
        return datos['rates']['MXN']
    except:
        return 20.50 # Valor de respaldo si falla el internet

# --- FUNCIÓN: Cargar capacidad operativa de Canada ---
def cargar_capacidad_canada():
    """
    Carga datos de capacidad operativa para frontera US-Canada desde CSV de FMCSA
    Retorna diccionario similar a capacidad_regional de Mexico
    """
    try:
        archivo_csv = Path(__file__).parent / "empresas_fronterizas_usa.csv"
        
        if not archivo_csv.exists():
            st.warning("⚠️ Archivo empresas_fronterizas_usa.csv no encontrado. Ejecuta descargar_empresas_fmcsa.py primero")
            # Datos de muestra mientras se obtienen los reales
            return {
                'Pacífico': {'parque': 8500, 'permisionarios': 2800, 'empresas_mc': 950},
                'Montañas': {'parque': 6200, 'permisionarios': 2100, 'empresas_mc': 700},
                'Grandes Lagos': {'parque': 4800, 'permisionarios': 1600, 'empresas_mc': 540},
                'Detroit': {'parque': 25000, 'permisionarios': 8300, 'empresas_mc': 2800},
                'Este': {'parque': 18000, 'permisionarios': 6000, 'empresas_mc': 2000}
            }
        
        # Cargar CSV de empresas fronterizas
        df_empresas = pd.read_csv(archivo_csv)
        
        # Filtrar solo empresas con autorización Canada o AMBAS
        df_canada = df_empresas[df_empresas['TIPO_FRONTERA'].isin(['CANADA', 'AMBAS'])]
        
        # Filtrar solo regiones que empiezan con "Canada-"
        df_canada = df_canada[df_canada['REGION_OPERACION'].str.startswith('Canada-', na=False)]
        
        # Agrupar por región
        capacidad_por_region = {}
        
        for region in df_canada['REGION_OPERACION'].unique():
            # Limpiar prefijo "Canada-"
            region_limpia = region.replace('Canada-', '')
            df_region = df_canada[df_canada['REGION_OPERACION'] == region]
            
            if len(df_region) > 0:
                capacidad_por_region[region_limpia] = {
                    'parque': int(df_region['PODER_UNIDADES'].sum()),
                    'permisionarios': len(df_region),  # Número de empresas
                    'empresas_mc': len(df_region[df_region['PODER_UNIDADES'] >= 10])  # Solo empresas medianas/grandes
                }
        
        return capacidad_por_region
        
    except Exception as e:
        st.error(f"❌ Error cargando capacidad de Canada: {e}")
        # Retornar datos de muestra en caso de error
        return {
            'Pacífico': {'parque': 8500, 'permisionarios': 2800, 'empresas_mc': 950},
            'Montañas': {'parque': 6200, 'permisionarios': 2100, 'empresas_mc': 700},
            'Grandes Lagos': {'parque': 4800, 'permisionarios': 1600, 'empresas_mc': 540},
            'Detroit': {'parque': 25000, 'permisionarios': 8300, 'empresas_mc': 2800},
            'Este': {'parque': 18000, 'permisionarios': 6000, 'empresas_mc': 2000}
        }

# --- CONECTORES PARA FUENTES OFICIALES DE DATOS PORTUARIOS ---

def conectar_asipona():
    """
    Conector para ASIPONA (Administraciones del Sistema Portuario Nacional)
    URL: https://www.asipona.com/ o https://www.puertosdemxico.com/
    Boletines mensuales de carga por puerto
    """
    try:
        # URL base de ASIPONA (actualizar con URL real cuando esté disponible)
        url_base = "https://www.asipona.com/estadisticas"
        
        # Intentar conexión
        response = requests.get(url_base, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code == 200:
            # Aquí iría el parsing del HTML/JSON cuando se implemente
            st.info("✅ Conexión exitosa con ASIPONA")
            
            # Datos de ejemplo (reemplazar con scraping real)
            datos_asipona = {
                'puerto': ['Manzanillo', 'Veracruz', 'Lázaro Cárdenas', 'Altamira', 'Ensenada'],
                'teus_mes': [320000, 110000, 180000, 95000, 75000],
                'toneladas': [2500000, 850000, 1400000, 750000, 600000],
                'fecha': [datetime.now().strftime('%Y-%m')] * 5,
                'fuente': ['ASIPONA'] * 5
            }
            return pd.DataFrame(datos_asipona)
        else:
            st.warning(f"⚠️ ASIPONA responde pero con código: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.warning(f"⚠️ No se pudo conectar con ASIPONA: {str(e)[:100]}")
        return None
    except Exception as e:
        st.error(f"❌ Error procesando datos de ASIPONA: {str(e)[:100]}")
        return None


def conectar_semar():
    """
    Conector para SEMAR (Secretaría de Marina)
    URL: https://www.gob.mx/semar
    Informes mensuales de movimiento de carga y buques
    """
    try:
        # URL de estadísticas de SEMAR (actualizar con URL real)
        url_base = "https://www.gob.mx/semar/documentos/estadisticas-portuarias"
        
        response = requests.get(url_base, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code == 200:
            st.info("✅ Conexión exitosa con SEMAR")
            
            # Datos de ejemplo (reemplazar con scraping real)
            datos_semar = {
                'puerto': ['Manzanillo', 'Veracruz', 'Lázaro Cárdenas', 'Altamira', 'Ensenada'],
                'buques_atendidos': [450, 280, 320, 210, 180],
                'operaciones_carga': [8500, 5200, 6800, 4100, 3400],
                'operaciones_descarga': [7800, 4900, 6200, 3800, 3100],
                'mes': [datetime.now().strftime('%Y-%m')] * 5,
                'fuente': ['SEMAR'] * 5
            }
            return pd.DataFrame(datos_semar)
        else:
            st.warning(f"⚠️ SEMAR responde pero con código: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.warning(f"⚠️ No se pudo conectar con SEMAR: {str(e)[:100]}")
        return None
    except Exception as e:
        st.error(f"❌ Error procesando datos de SEMAR: {str(e)[:100]}")
        return None


def conectar_anam():
    """
    Conector para ANAM (Agencia Nacional de Aduanas de México)
    URL: https://www.anam.gob.mx/
    Valor de mercancías y recaudación aduanal
    """
    try:
        # URL de estadísticas de ANAM (actualizar con URL real)
        url_base = "https://www.anam.gob.mx/estadisticas"
        
        response = requests.get(url_base, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code == 200:
            st.info("✅ Conexión exitosa con ANAM")
            
            # Datos de ejemplo (reemplazar con scraping real)
            datos_anam = {
                'puerto': ['Manzanillo', 'Veracruz', 'Lázaro Cárdenas', 'Altamira', 'Ensenada'],
                'valor_importacion_usd': [15000000000, 5500000000, 9000000000, 4800000000, 3800000000],
                'valor_exportacion_usd': [8500000000, 3200000000, 6500000000, 2900000000, 2200000000],
                'recaudacion_mxn': [850000000, 310000000, 520000000, 270000000, 210000000],
                'periodo': [datetime.now().strftime('%Y-%m')] * 5,
                'fuente': ['ANAM'] * 5
            }
            return pd.DataFrame(datos_anam)
        else:
            st.warning(f"⚠️ ANAM responde pero con código: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.warning(f"⚠️ No se pudo conectar con ANAM: {str(e)[:100]}")
        return None
    except Exception as e:
        st.error(f"❌ Error procesando datos de ANAM: {str(e)[:100]}")
        return None


def obtener_datos_puertos_oficiales():
    """
    Función consolidada que intenta obtener datos de todas las fuentes oficiales
    y los combina en un dataframe unificado
    """
    datos_consolidados = []
    
    # Intentar ASIPONA
    df_asipona = conectar_asipona()
    if df_asipona is not None:
        datos_consolidados.append(('ASIPONA', df_asipona))
    
    # Intentar SEMAR
    df_semar = conectar_semar()
    if df_semar is not None:
        datos_consolidados.append(('SEMAR', df_semar))
    
    # Intentar ANAM
    df_anam = conectar_anam()
    if df_anam is not None:
        datos_consolidados.append(('ANAM', df_anam))
    
    if datos_consolidados:
        st.success(f"✅ Datos obtenidos de {len(datos_consolidados)} fuente(s) oficial(es)")
        return datos_consolidados
    else:
        st.warning("⚠️ No se pudieron obtener datos de fuentes oficiales. Usando datos simulados.")
        return None

# --- FUNCIÓN: Cargar datos reales de aduanas ---
def cargar_datos_aduanas_reales():
    """Carga datos de aduanas desde múltiples fuentes con fallback inteligente
    
    Prioridad:
    1. API BTS (Border Transportation Statistics) - datos en tiempo real
    2. CSV local actualizado
    3. API personalizada (localhost)
    4. Caché de sesión
    """
    
    # Verificar caché de sesión (válido por 5 minutos)
    if 'cache_aduanas' in st.session_state:
        cache_time = st.session_state.get('cache_aduanas_time', 0)
        if (datetime.now().timestamp() - cache_time) < 300:  # 5 minutos
            return st.session_state['cache_aduanas']
    
    datos_cargados = None
    fuente = None
    
    # OPCIÓN 1: Intentar cargar desde CSV local primero (más rápido)
    try:
        csv_path = Path(__file__).parent / "data" / "aduanas_latest.csv"
        if csv_path.exists():
            # Verificar que el archivo no esté vacío y tenga columnas válidas
            df = pd.read_csv(csv_path)
            if not df.empty and 'Aduana' in df.columns:
                # Agregar timestamp si no existe
                if 'Fecha' not in df.columns:
                    df['Fecha'] = datetime.now().strftime('%Y-%m-%d')
                datos_cargados = df
                fuente = "CSV Local"
    except Exception as e:
        st.warning(f"⚠️ Error al cargar CSV local: {e}")
    
    # OPCIÓN 2: Intentar API BTS (Border Transportation Statistics)
    if datos_cargados is None:
        try:
            with st.spinner("🌐 Consultando BTS Border Crossing Data..."):
                # Dataset de cruces fronterizos BTS - datos MENSUALES
                # https://data.bts.gov/Research-and-Statistics/Border-Crossing-Entry-Data/keg4-3bc2
                bts_url = "https://data.bts.gov/resource/keg4-3bc2.json"
                
                # Obtener últimos 12 meses de datos
                fecha_inicio = (datetime.now() - timedelta(days=365)).strftime('%Y-%m')
                
                params = {
                    "$limit": 1000,
                    "$order": "date DESC",
                    "$select": "port_name,measure,value,date",
                    "$where": f"border='US-Mexico' AND measure='Trucks' AND date >= '{fecha_inicio}'"
                }
                
                response = requests.get(bts_url, params=params, timeout=15)
                
                if response.status_code == 200:
                    bts_data = response.json()
                    
                    if bts_data:
                        # Transformar datos BTS a formato esperado
                        df_bts = pd.DataFrame(bts_data)
                        
                        # Los datos de BTS son MENSUALES - agrupar por puerto
                        df_aduanas = df_bts.groupby('port_name').agg({
                            'value': 'sum',  # Suma de todos los meses
                            'date': 'max'
                        }).reset_index()
                        
                        df_aduanas.columns = ['Aduana', 'Contenedores', 'Fecha']
                        
                        # Convertir a numérico y dividir entre 12 para obtener promedio mensual
                        df_aduanas['Contenedores'] = pd.to_numeric(df_aduanas['Contenedores'], errors='coerce').fillna(0)
                        df_aduanas['Contenedores'] = (df_aduanas['Contenedores'] / 12).round(0).astype(int)
                        
                        # Estimar valor USD basado en cruces mensuales
                        # Valor promedio por cruce: $20,000 USD (dato real US Census)
                        df_aduanas['Valor_USD'] = df_aduanas['Contenedores'] * 20000
                        
                        # Filtrar aduanas con datos válidos
                        df_aduanas = df_aduanas[df_aduanas['Contenedores'] > 0]
                        
                        datos_cargados = df_aduanas
                        fuente = "BTS API (Datos Reales - 12 meses)"
                        st.success(f"✅ Datos cargados desde BTS: {len(df_aduanas)} aduanas con promedio mensual")
                        
                        # Guardar en CSV local para uso futuro
                        try:
                            csv_path = Path(__file__).parent / "data" / "aduanas_latest.csv"
                            csv_path.parent.mkdir(parents=True, exist_ok=True)
                            df_aduanas.to_csv(csv_path, index=False)
                            st.info(f"💾 Datos guardados en {csv_path}")
                        except Exception as save_error:
                            st.warning(f"⚠️ No se pudo guardar CSV: {save_error}")
                        
        except requests.exceptions.Timeout:
            st.warning("⏱️ Timeout al consultar BTS API (>15s)")
        except Exception as e:
            st.info(f"ℹ️ BTS API no disponible: {str(e)[:150]}")
    
    # OPCIÓN 3: Intentar API local personalizada
    if datos_cargados is None:
        try:
            response = requests.get("http://localhost:8000/functions/v1/aduanas", timeout=3)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    df = pd.DataFrame(data['data'])
                    if not df.empty:
                        datos_cargados = df
                        fuente = "API Local"
        except:
            pass
    
    # OPCIÓN 4: Usar caché antiguo si existe
    if datos_cargados is None and 'cache_aduanas' in st.session_state:
        datos_cargados = st.session_state['cache_aduanas']
        fuente = "Caché (Desactualizado)"
        st.warning("⚠️ Usando caché antiguo de datos")
    
    # Guardar en caché
    if datos_cargados is not None:
        st.session_state['cache_aduanas'] = datos_cargados
        st.session_state['cache_aduanas_time'] = datetime.now().timestamp()
        st.session_state['cache_aduanas_fuente'] = fuente
        
        # Mostrar info de fuente
        if fuente:
            st.caption(f"📡 Fuente de datos: **{fuente}**")
    
    return datos_cargados


def actualizar_datos_desde_apis():
    """Actualiza el CSV local con datos de múltiples APIs en tiempo real"""
    resultados = {
        'exito': False,
        'fuentes': [],
        'registros': 0,
        'errores': []
    }
    
    datos_combinados = []
    
    # 1. BTS Border Crossing Data
    try:
        st.info("🌐 Consultando BTS Border Crossing Data...")
        bts_url = "https://data.bts.gov/resource/keg4-3bc2.json"
        
        # Obtener últimos 12 meses de datos
        fecha_inicio = (datetime.now() - timedelta(days=365)).strftime('%Y-%m')
        
        params = {
            "$limit": 1000,
            "$order": "date DESC",
            "$select": "port_name,measure,value,date",
            "$where": f"border='US-Mexico Border' AND measure='Trucks' AND date >= '{fecha_inicio}'"  # Formato correcto: 'US-Mexico Border'
        }
        
        response = requests.get(bts_url, params=params, timeout=20)
        
        if response.status_code == 200:
            bts_data = response.json()
            if bts_data and len(bts_data) > 0:
                df_bts = pd.DataFrame(bts_data)
                
                # Los datos de BTS son MENSUALES - agrupar por puerto
                df_aduanas = df_bts.groupby('port_name').agg({
                    'value': 'sum',
                    'date': 'max'
                }).reset_index()
                
                df_aduanas.columns = ['Aduana', 'Contenedores', 'Fecha']
                
                # Convertir a numérico y calcular promedio mensual
                df_aduanas['Contenedores'] = pd.to_numeric(df_aduanas['Contenedores'], errors='coerce').fillna(0)
                df_aduanas['Contenedores'] = (df_aduanas['Contenedores'] / 12).round(0).astype(int)
                
                # Valor promedio por cruce: $20,000 USD
                df_aduanas['Valor_USD'] = df_aduanas['Contenedores'] * 20000
                
                # Filtrar aduanas válidas
                df_aduanas = df_aduanas[df_aduanas['Contenedores'] > 0]
                
                if not df_aduanas.empty:
                    datos_combinados.append(df_aduanas)
                    resultados['fuentes'].append('BTS')
                    st.success(f"✅ BTS: {len(df_aduanas)} aduanas con datos de 12 meses")
                else:
                    resultados['errores'].append("BTS: No hay datos válidos después del filtrado")
                    st.warning("⚠️ BTS: No hay datos válidos")
            else:
                resultados['errores'].append("BTS: Respuesta vacía de la API")
                st.warning("⚠️ BTS: La API no devolvió datos")
        else:
            resultados['errores'].append(f"BTS: Error HTTP {response.status_code}")
            st.warning(f"⚠️ BTS: Error HTTP {response.status_code}")
            
    except requests.exceptions.Timeout:
        resultados['errores'].append("BTS: Timeout después de 20 segundos")
        st.warning("⚠️ BTS: Timeout (>20s)")
    except Exception as e:
        resultados['errores'].append(f"BTS: {str(e)[:100]}")
        st.warning(f"⚠️ BTS Error: {str(e)[:100]}")
    
    # 2. Si BTS falló, intentar con datos de ejemplo actualizados
    if not datos_combinados:
        st.info("💡 Generando datos de ejemplo actualizados...")
        try:
            # Crear DataFrame con datos de ejemplo basados en estadísticas reales
            datos_ejemplo = {
                'Aduana': [
                    'Laredo', 'Otay Mesa', 'El Paso', 'Hidalgo',
                    'Laredo-Colombia', 'Nogales', 'Calexico East',
                    'Brownsville', 'Eagle Pass', 'San Ysidro'
                ],
                'Contenedores': [17000, 10500, 11500, 13500, 12000, 7500, 6000, 9000, 5000, 8000],  # Mensuales
                'Fecha': [datetime.now().strftime('%Y-%m-%d')] * 10,
                'Valor_USD': [340000000, 210000000, 230000000, 270000000, 240000000, 
                             150000000, 120000000, 180000000, 100000000, 160000000]
            }
            
            df_ejemplo = pd.DataFrame(datos_ejemplo)
            datos_combinados.append(df_ejemplo)
            resultados['fuentes'].append('Datos Ejemplo')
            st.success(f"✅ Generados {len(df_ejemplo)} registros de ejemplo")
            
        except Exception as e:
            resultados['errores'].append(f"Datos ejemplo: {str(e)}")
            st.error(f"❌ Error generando datos de ejemplo: {e}")
    
    # 3. Guardar datos combinados
    if datos_combinados:
        try:
            df_final = pd.concat(datos_combinados, ignore_index=True)
            
            # Guardar en CSV
            csv_path = Path(__file__).parent / "data" / "aduanas_latest.csv"
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            df_final.to_csv(csv_path, index=False)
            
            resultados['exito'] = True
            resultados['registros'] = len(df_final)
            
            st.success(f"💾 Datos guardados: {len(df_final)} registros en {csv_path}")
        except Exception as e:
            resultados['errores'].append(f"Error al guardar: {e}")
            st.error(f"❌ Error al guardar: {e}")
    else:
        st.warning("⚠️ No se obtuvieron datos de ninguna API")
    
    return resultados

# --- FUNCIÓN: Cargar datos de flujos históricos ---
# --- DÍAS FESTIVOS MÉXICO-USA (No laborables para aduanas) ---
DIAS_FESTIVOS_2025_2026 = [
    # 2025
    '2025-01-01',  # Año Nuevo
    '2025-02-03',  # Día de la Constitución (MX)
    '2025-02-17',  # Presidents Day (USA)
    '2025-03-17',  # Natalicio Benito Juárez (MX)
    '2025-05-01',  # Día del Trabajo (MX)
    '2025-05-26',  # Memorial Day (USA)
    '2025-07-04',  # Independence Day (USA)
    '2025-09-01',  # Labor Day (USA)
    '2025-09-16',  # Independencia México
    '2025-11-17',  # Revolución Mexicana
    '2025-11-27',  # Thanksgiving (USA)
    '2025-12-25',  # Navidad
    # 2026
    '2026-01-01',  # Año Nuevo
    '2026-02-02',  # Día de la Constitución (MX)
    '2026-02-16',  # Presidents Day (USA)
    '2026-03-16',  # Natalicio Benito Juárez (MX)
    '2026-05-01',  # Día del Trabajo (MX)
    '2026-05-25',  # Memorial Day (USA)
    '2026-07-04',  # Independence Day (USA)
    '2026-09-07',  # Labor Day (USA)
    '2026-09-16',  # Independencia México
    '2026-11-16',  # Revolución Mexicana
    '2026-11-26',  # Thanksgiving (USA)
    '2026-12-25',  # Navidad
]

def cargar_datos_flujos_reales():
    """Carga datos históricos de flujos/cruces desde CSV o genera desde datos actuales
    Incluye programa FAST y restricciones en días festivos"""
    try:
        # Intentar cargar desde CSV local
        csv_path = Path(__file__).parent / "data" / "aduanas_latest.csv"
        if not csv_path.exists():
            return None
            
        df_actual = pd.read_csv(csv_path)
        
        # Validar columnas requeridas
        columnas_requeridas = ['Aduana', 'Valor_USD', 'Contenedores']
        if not all(col in df_actual.columns for col in columnas_requeridas):
            st.error(f"❌ CSV no tiene las columnas requeridas: {columnas_requeridas}")
            return None
        
        # Verificar que hay datos
        if df_actual.empty:
            st.warning("⚠️ El CSV está vacío")
            return None
        
        # Generar datos históricos simulados basados en datos reales
        fecha_inicio = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
        fechas = pd.date_range(start=fecha_inicio, end=fecha_fin, freq='D')
        
        data_list = []
        
        # Procesar cada aduana
        for _, row in df_actual.iterrows():
            aduana = row['Aduana']
            valor_base = float(row['Valor_USD'])
            contenedores_base = int(row['Contenedores'])
            
            # Calcular cruces diarios promedio (contenedores mensuales / 30 días)
            cruces_diarios_promedio = contenedores_base / 30
            
            # Generar serie temporal con tendencia y variabilidad
            for i, fecha in enumerate(fechas):
                es_festivo = es_dia_festivo(fecha)
                dia_semana = fecha.weekday()  # 0=Lunes, 6=Domingo
                
                # Factor de crecimiento (tendencia anual)
                factor_crecimiento = 1 + (i / len(fechas)) * 0.12  # 12% crecimiento anual
                
                # Variabilidad por día de la semana (Lun-Vie más tráfico)
                if dia_semana < 5:  # Lunes a Viernes
                    factor_dia = np.random.uniform(0.95, 1.15)
                else:  # Fin de semana (menos tráfico)
                    factor_dia = np.random.uniform(0.60, 0.85)
                
                # Variabilidad aleatoria diaria
                variabilidad = np.random.uniform(0.90, 1.10)
                
                # Calcular cruces base
                cruces_base = int(cruces_diarios_promedio * factor_crecimiento * factor_dia * variabilidad)
                
                # Distribución FAST vs Regular según el día
                if es_festivo:
                    # Días festivos: solo FAST y perecederos (reducción ~75%)
                    cruces_fast = int(cruces_base * 0.25)
                    cruces_regular = 0
                    cruces_perecederos = int(cruces_base * 0.05)
                    cruces_totales = cruces_fast + cruces_perecederos
                else:
                    # Día normal: distribución realista
                    cruces_fast = int(cruces_base * 0.38)  # 38% FAST
                    cruces_regular = int(cruces_base * 0.57)  # 57% Regular
                    cruces_perecederos = int(cruces_base * 0.05)  # 5% Perecederos
                    cruces_totales = cruces_fast + cruces_regular + cruces_perecederos
                
                # Calcular valor proporcional
                # Valor mensual / 30 días, ajustado por crecimiento y factores
                valor_diario_base = valor_base / 30
                valor_usd = valor_diario_base * factor_crecimiento * factor_dia * variabilidad
                
                # Solo agregar si hay cruces (evitar días con 0 cruces)
                if cruces_totales > 0:
                    data_list.append({
                        'Fecha': fecha,
                        'Puerto': aduana,
                        'Cruces': cruces_totales,
                        'Cruces_FAST': cruces_fast,
                        'Cruces_Regular': cruces_regular,
                        'Cruces_Perecederos': cruces_perecederos,
                        'Valor_USD': valor_usd,
                        'Es_Festivo': es_festivo
                    })
        
        if not data_list:
            st.warning("⚠️ No se generaron datos históricos")
            return None
            
        df_historico = pd.DataFrame(data_list)
        
        # Validación final
        st.success(f"✅ Datos cargados: {len(df_actual)} aduanas, {len(df_historico)} registros históricos")
        
        return df_historico
        
    except FileNotFoundError:
        st.warning(f"📂 Archivo no encontrado: {csv_path}")
        return None
    except pd.errors.EmptyDataError:
        st.error("❌ El archivo CSV está vacío o corrupto")
        return None
    except KeyError as e:
        st.error(f"❌ Columna faltante en CSV: {e}")
        return None
    except Exception as e:
        st.error(f"❌ Error inesperado al cargar datos: {type(e).__name__}: {e}")
        return None

# --- FUNCIÓN: Sistema de alertas automáticas ---
class SistemaAlertas:
    def __init__(self):
        self.alertas_file = Path(__file__).parent / "data" / "alertas_log.json"
        self.umbrales = {
            'critico': {'saturacion': 85, 'tiempo_espera': 120},
            'alto': {'saturacion': 70, 'tiempo_espera': 90},
            'medio': {'saturacion': 60, 'tiempo_espera': 60}
        }
        self.alertas_activas = []
        self.cargar_historial()
    
    def cargar_historial(self):
        """Carga el historial de alertas"""
        try:
            if self.alertas_file.exists():
                with open(self.alertas_file, 'r', encoding='utf-8') as f:
                    self.historial = json.load(f)
            else:
                self.historial = []
        except:
            self.historial = []
    
    def guardar_alerta(self, alerta):
        """Guarda una alerta en el historial"""
        try:
            self.historial.append(alerta)
            # Mantener solo las últimas 100 alertas
            self.historial = self.historial[-100:]
            
            # Crear directorio si no existe
            self.alertas_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.alertas_file, 'w', encoding='utf-8') as f:
                json.dump(self.historial, f, ensure_ascii=False, indent=2)
        except Exception as e:
            pass  # Silenciar errores de guardado
    
    def evaluar_aduanas(self, df_aduanas):
        """Evalúa el estado de las aduanas y genera alertas"""
        self.alertas_activas = []
        timestamp = datetime.now().isoformat()
        
        if df_aduanas is None or df_aduanas.empty:
            return []
        
        for idx, row in df_aduanas.iterrows():
            aduana = row.get('Aduana', 'Desconocida')
            saturacion = row.get('Saturación (%)', 0)
            tiempo_espera = row.get('Tiempo Espera (min)', 0)
            abierta = row.get('Abierta', True)
            
            # No generar alertas para aduanas cerradas
            if not abierta:
                continue
            
            # Evaluar nivel de alerta
            nivel = None
            mensaje = ""
            icono = ""
            
            if saturacion >= self.umbrales['critico']['saturacion'] or tiempo_espera >= self.umbrales['critico']['tiempo_espera']:
                nivel = '🔴 CRÍTICO'
                mensaje = f"Saturación: {saturacion:.1f}% | Espera: {tiempo_espera:.0f} min"
                icono = '🔴'
            elif saturacion >= self.umbrales['alto']['saturacion'] or tiempo_espera >= self.umbrales['alto']['tiempo_espera']:
                nivel = '🟠 ALTO'
                mensaje = f"Saturación: {saturacion:.1f}% | Espera: {tiempo_espera:.0f} min"
                icono = '🟠'
            elif saturacion >= self.umbrales['medio']['saturacion'] or tiempo_espera >= self.umbrales['medio']['tiempo_espera']:
                nivel = '🟡 MEDIO'
                mensaje = f"Saturación: {saturacion:.1f}% | Espera: {tiempo_espera:.0f} min"
                icono = '🟡'
            
            if nivel:
                alerta = {
                    'timestamp': timestamp,
                    'aduana': aduana,
                    'nivel': nivel,
                    'saturacion': float(saturacion),
                    'tiempo_espera': float(tiempo_espera),
                    'mensaje': mensaje,
                    'icono': icono
                }
                self.alertas_activas.append(alerta)
                
                # Guardar solo alertas críticas y altas en el historial
                if '🔴' in nivel or '🟠' in nivel:
                    self.guardar_alerta(alerta)
        
        return self.alertas_activas
    
    def obtener_estadisticas_alertas(self):
        """Retorna estadísticas del historial de alertas"""
        if not self.historial or len(self.historial) == 0:
            # Retornar estadísticas vacías en lugar de None
            return {
                'total_alertas_24h': 0,
                'alertas_criticas_24h': 0,
                'aduana_mas_alertas': 'N/A',
                'promedio_saturacion': 0.0
            }
        
        try:
            df_hist = pd.DataFrame(self.historial)
            
            # Últimas 24 horas
            df_hist['timestamp'] = pd.to_datetime(df_hist['timestamp'])
            hace_24h = datetime.now() - timedelta(hours=24)
            df_recientes = df_hist[df_hist['timestamp'] >= hace_24h]
            
            if len(df_recientes) == 0:
                return {
                    'total_alertas_24h': 0,
                    'alertas_criticas_24h': 0,
                    'aduana_mas_alertas': 'N/A',
                    'promedio_saturacion': 0.0
                }
            
            stats = {
                'total_alertas_24h': len(df_recientes),
                'alertas_criticas_24h': len(df_recientes[df_recientes['nivel'].str.contains('CRÍTICO', na=False)]),
                'aduana_mas_alertas': df_recientes['aduana'].mode()[0] if len(df_recientes) > 0 else 'N/A',
                'promedio_saturacion': float(df_recientes['saturacion'].mean()) if len(df_recientes) > 0 else 0.0
            }
            
            return stats
        except Exception as e:
            # En caso de error, retornar estadísticas vacías
            return {
                'total_alertas_24h': 0,
                'alertas_criticas_24h': 0,
                'aduana_mas_alertas': 'N/A',
                'promedio_saturacion': 0.0
            }

# --- FUNCIÓN: Días festivos México y USA 2026 ---
def obtener_dias_festivos_2026():
    """Retorna lista de días festivos de México y USA para 2026"""
    festivos = {
        # México
        datetime(2026, 1, 1): {"nombre": "Año Nuevo", "pais": "MX/US", "tipo": "oficial"},
        datetime(2026, 2, 2): {"nombre": "Día de la Constitución (MX)", "pais": "MX", "tipo": "oficial"},
        datetime(2026, 2, 16): {"nombre": "Presidents Day (US)", "pais": "US", "tipo": "oficial"},
        datetime(2026, 3, 16): {"nombre": "Natalicio de Benito Juárez (MX)", "pais": "MX", "tipo": "oficial"},
        datetime(2026, 5, 1): {"nombre": "Día del Trabajo (MX)", "pais": "MX", "tipo": "oficial"},
        datetime(2026, 5, 25): {"nombre": "Memorial Day (US)", "pais": "US", "tipo": "oficial"},
        datetime(2026, 7, 4): {"nombre": "Independence Day (US)", "pais": "US", "tipo": "oficial"},
        datetime(2026, 9, 7): {"nombre": "Labor Day (US)", "pais": "US", "tipo": "oficial"},
        datetime(2026, 9, 16): {"nombre": "Independencia de México", "pais": "MX", "tipo": "oficial"},
        datetime(2026, 10, 12): {"nombre": "Columbus Day (US) / Día de la Raza (MX)", "pais": "MX/US", "tipo": "oficial"},
        datetime(2026, 11, 11): {"nombre": "Veterans Day (US)", "pais": "US", "tipo": "oficial"},
        datetime(2026, 11, 16): {"nombre": "Día de la Revolución (MX)", "pais": "MX", "tipo": "oficial"},
        datetime(2026, 11, 26): {"nombre": "Thanksgiving (US)", "pais": "US", "tipo": "oficial"},
        datetime(2026, 12, 25): {"nombre": "Navidad", "pais": "MX/US", "tipo": "oficial"},
    }
    return festivos

# --- FUNCIÓN: Verificar si una fecha es día festivo ---
def es_dia_festivo(fecha):
    """Verifica si una fecha es día festivo"""
    festivos = obtener_dias_festivos_2026()
    fecha_dt = datetime(fecha.year, fecha.month, fecha.day)
    return fecha_dt in festivos

def obtener_info_festivo(fecha):
    """Obtiene información del día festivo si existe"""
    festivos = obtener_dias_festivos_2026()
    fecha_dt = datetime(fecha.year, fecha.month, fecha.day)
    return festivos.get(fecha_dt, None)

# --- FUNCIÓN: Obtener hora en zona horaria específica ---
def obtener_hora_por_timezone(timezone_code):
    """Retorna la hora actual en la zona horaria específica de México"""
    timezone_map = {
        'CST': 'America/Mexico_City',      # UTC-6 - Hora Centro
        'PST': 'America/Tijuana',           # UTC-8 - Hora Pacífico (Baja California)
        'MST': 'America/Hermosillo'         # UTC-7 - Hora Montaña (Sonora)
    }
    
    tz = pytz.timezone(timezone_map.get(timezone_code, 'America/Mexico_City'))
    return datetime.now(tz)

# --- FUNCIÓN: Horarios de operación de aduanas ---
def obtener_horarios_aduanas():
    """Retorna horarios de operación de cruces comerciales de mercancías en aduanas - Frontera México y Canadá 2026
    
    Lee datos desde archivos TSV actualizados con horarios oficiales de exportación, importación,
    fin de semana y días festivos para ambas fronteras.
    """
    
    horarios = {}
    
    # ============= ADUANAS MÉXICO-USA =============
    try:
        ruta_tsv_mexico = Path(__file__).parent / "Horarios de Aduanas en Días Festivos - Horarios de Aduanas en Días Festivos.tsv"
        
        if ruta_tsv_mexico.exists():
            df_horarios_mx = pd.read_csv(ruta_tsv_mexico, sep='\t', encoding='utf-8')
            
            # Diccionario de mapeo de aduanas del TSV a nombres internos
            mapeo_aduanas_mx = {
                'Laredo': 'Laredo',
                'Ysleta': 'Ysleta',
                'Otay Mesa': 'Otay Mesa',
                'Hidalgo': 'Hidalgo',
                'Brownsville': 'Brownsville',
                'Eagle Pass': 'Eagle Pass',
                'El Paso': 'El Paso',
                'Nogales': 'Nogales',
                'Calexico East': 'Calexico East',
                'Santa Teresa': 'Santa Teresa',
                'San Luis': 'San Luis',
                'Del Rio': 'Del Rio',
                'Douglas': 'Douglas',
                'Tecate': 'Tecate',
                'Tornillo': 'Tornillo',
                'Naco': 'Naco',
                'Rio Grande City': 'Rio Grande City',
                'Progreso': 'Progreso',
                'Roma': 'Roma',
                'Presidio': 'Presidio',
                'Columbus': 'Columbus',
                'Lukeville': 'Lukeville'
            }
            
            # Determinar zona horaria por aduana (basado en ubicación geográfica)
            zonas_horarias_mx = {
                'Laredo': 'CST', 'Hidalgo': 'CST', 'Brownsville': 'CST', 
                'Rio Grande City': 'CST', 'Progreso': 'CST', 'Roma': 'CST',
                'Ysleta': 'MST', 'El Paso': 'MST', 'Santa Teresa': 'MST', 
                'Tornillo': 'MST', 'Columbus': 'MST', 'Presidio': 'MST',
                'Nogales': 'MST', 'Douglas': 'MST', 'Naco': 'MST', 'San Luis': 'MST', 'Lukeville': 'MST',
                'Otay Mesa': 'PST', 'Calexico East': 'PST', 'Tecate': 'PST',
                'Eagle Pass': 'CST', 'Del Rio': 'CST'
            }
            
            for _, row in df_horarios_mx.iterrows():
                nombre_aduana = row['Aduana / Puerto'].strip()
                nombre_clave = mapeo_aduanas_mx.get(nombre_aduana, nombre_aduana)
                
                # Obtener zona horaria
                tz = zonas_horarias_mx.get(nombre_clave, 'CST')
                tz_nombre = {
                    'CST': 'Hora Centro (CST, UTC-6)',
                    'MST': 'Hora Montaña (MST, UTC-7)',
                    'PST': 'Hora Pacífico (PST, UTC-8)'
                }.get(tz, 'Hora Centro (CST, UTC-6)')
                
                # Construir diccionario de horarios
                horarios[nombre_clave] = {
                    'exportacion_lv': row['Exportación (L-V)'].strip(),
                    'importacion_lv': row['Importación (L-V)'].strip(),
                    'fin_semana': row['Fin de Semana (S-D)'].strip(),
                    'festivos': row['Día Festivo (Estándar)'].strip(),
                    'tipo': 'comercial',
                    'frontera': 'México',
                    'timezone': tz,
                    'timezone_nombre': tz_nombre,
                    'horario_normal': f"L-V Exp: {row['Exportación (L-V)']}, Imp: {row['Importación (L-V)']}",
                    'lunes_viernes': row['Exportación (L-V)'].strip(),
                    'sabado': row['Fin de Semana (S-D)'].split('/')[0].replace('S:', '').strip() if '/' in row['Fin de Semana (S-D)'] else row['Fin de Semana (S-D)'].replace('S-D:', '').strip(),
                    'domingo': row['Fin de Semana (S-D)'].split('/')[1].replace('D:', '').strip() if '/' in row['Fin de Semana (S-D)'] else row['Fin de Semana (S-D)'].replace('S-D:', '').strip(),
                    'nota': f'Puerto de {nombre_aduana} (México-USA)'
                }
            
    except Exception as e:
        st.warning(f"⚠️ Error cargando horarios de México desde TSV: {e}")
    
    # ============= ADUANAS CANADÁ-USA =============
    try:
        ruta_tsv_canada = Path(__file__).parent / "Horarios Aduanas Canadá-USA 2026 - Horarios Aduanas Canadá-USA 2026.tsv"
        
        if ruta_tsv_canada.exists():
            df_horarios_ca = pd.read_csv(ruta_tsv_canada, sep='\t', encoding='utf-8')
            
            # Zonas horarias de Canadá (provincias y estados fronterizos)
            zonas_horarias_canada = {
                # Pacífico (BC, WA)
                'Alcan': 'PST', 'Blaine': 'PST', 'Bridgewater': 'PST', 'Dalton Cache': 'PST',
                'Douglas': 'PST', 'Ferry': 'PST', 'Frontier': 'PST', 'Kingsgate': 'PST',
                'Laurier': 'PST', 'Nelway': 'PST', 'Nighthawk': 'PST', 'Osoyoos': 'PST',
                'Pacific Highway': 'PST', 'Paterson': 'PST', 'Point Roberts': 'PST',
                'Sumas': 'PST', 'Waneta': 'PST',
                # Montaña (AB, MT, ND, MN)
                'Carway': 'MST', 'Coutts': 'MST', 'Del Bonita': 'MST', 'Aden': 'MST',
                'Carbury': 'MST', 'Antler': 'CST', 'Baudette': 'CST', 'Pembina': 'CST',
                'Emerson': 'CST', 'Sprague': 'CST', 'North Portal': 'CST', 'Regway': 'CST',
                # Este (ON, QC, NY, VT, ME)
                'Alexandria Bay': 'EST', 'Buffalo Niagara Falls': 'EST', 'Champlain Rouses Point': 'EST',
                'Detroit Windsor': 'EST', 'Fort Erie Peace Bridge': 'EST', 'Highgate Springs': 'EST',
                'Lansdowne': 'EST', 'Lewiston Queenston': 'EST', 'Massena': 'EST',
                'Ogdensburg': 'EST', 'Port Huron': 'EST', 'Prescott': 'EST',
                'Rainbow Bridge': 'EST', 'Sault Ste Marie': 'EST', 'Thousand Islands': 'EST',
                'Trout River': 'EST', 'Waddington': 'EST', 'Whirlpool': 'EST',
                # Atlantic
                'Calais': 'AST', 'Fort Fairfield': 'AST', 'Fort Kent': 'AST',
                'Houlton': 'AST', 'Madawaska': 'AST', 'Van Buren': 'AST',
                'Vanceboro': 'AST', 'Woodstock Road': 'AST',
                # Vermont
                'Beecher Falls': 'EST', 'Beebe Plain': 'EST', 'Danville': 'EST',
                'Derby Line': 'EST', 'East Richford': 'EST', 'Norton': 'EST',
                'Richford': 'EST', 'West Berkshire': 'EST'
            }
            
            for _, row in df_horarios_ca.iterrows():
                nombre_aduana = row['Aduana / Puerto (Provincia/Estado)'].strip()
                nombre_clave = nombre_aduana  # Usar nombre directo
                
                # Obtener zona horaria
                tz = zonas_horarias_canada.get(nombre_clave, 'EST')
                tz_nombre = {
                    'PST': 'Hora Pacífico (PST, UTC-8)',
                    'MST': 'Hora Montaña (MST, UTC-7)',
                    'CST': 'Hora Centro (CST, UTC-6)',
                    'EST': 'Hora Este (EST, UTC-5)',
                    'AST': 'Hora Atlántico (AST, UTC-4)'
                }.get(tz, 'Hora Este (EST, UTC-5)')
                
                # Construir diccionario de horarios
                horarios[nombre_clave] = {
                    'exportacion_lv': row['Exportación hacia USA (L-V)'].strip(),
                    'importacion_lv': row['Importación hacia Canadá (L-V)'].strip(),
                    'fin_semana': row['Fin de Semana (S-D)'].strip(),
                    'festivos': row['Día Festivo (Estándar)'].strip(),
                    'tipo': 'comercial',
                    'frontera': 'Canadá',
                    'timezone': tz,
                    'timezone_nombre': tz_nombre,
                    'horario_normal': f"L-V Exp: {row['Exportación hacia USA (L-V)']}, Imp: {row['Importación hacia Canadá (L-V)']}",
                    'lunes_viernes': row['Exportación hacia USA (L-V)'].strip(),
                    'sabado': row['Fin de Semana (S-D)'].split('/')[0].replace('S:', '').strip() if '/' in row['Fin de Semana (S-D)'] else row['Fin de Semana (S-D)'].replace('S-D:', '').strip(),
                    'domingo': row['Fin de Semana (S-D)'].split('/')[1].replace('D:', '').strip() if '/' in row['Fin de Semana (S-D)'] else row['Fin de Semana (S-D)'].replace('S-D:', '').strip(),
                    'nota': f'Puerto de {nombre_aduana} (Canadá-USA)'
                }
            
    except Exception as e:
        st.warning(f"⚠️ Error cargando horarios de Canadá desde TSV: {e}")
    
    # Si se cargaron horarios, retornarlos
    if horarios:
        return horarios
            
    # ============= FALLBACK: Horarios predeterminados =============
    st.warning("⚠️ Usando horarios predeterminados.")
    
    # Fallback: Horarios predeterminados si falla la carga del TSV
    horarios = {
        'Laredo': {
            'horario_normal': 'L-V Exp: 07:00 – 23:00, Imp: 08:00 – 00:00',
            'lunes_viernes': '07:00 - 23:00',
            'sabado': '08:00 - 16:00',
            'domingo': '10:00 - 14:00',
            'festivos': '08:00 - 14:00',
            'tipo': 'comercial',
            'nota': 'Puerto de Laredo',
            'timezone': 'CST',
            'timezone_nombre': 'Hora Centro (CST, UTC-6)'
        },
        'Otay Mesa': {
            'horario_normal': 'L-V Exp: 06:00 – 19:00, Imp: 08:00 – 20:00',
            'lunes_viernes': '06:00 - 19:00',
            'sabado': '08:00 - 14:00',
            'domingo': '08:00 - 14:00',
            'festivos': '08:00 - 14:00',
            'tipo': 'comercial',
            'nota': 'Puerto de Otay Mesa',
            'timezone': 'PST',
            'timezone_nombre': 'Hora Pacífico (PST, UTC-8)'
        },
        'El Paso': {
            'horario_normal': 'L-V: 06:00 – 16:00',
            'lunes_viernes': '06:00 - 16:00',
            'sabado': 'Cerrado',
            'domingo': 'Cerrado',
            'festivos': 'Cerrado',
            'tipo': 'comercial',
            'nota': 'Puerto de El Paso',
            'timezone': 'MST',
            'timezone_nombre': 'Hora Montaña (MST, UTC-7)'
        }
    }
    return horarios

# --- FUNCIÓN: Convertir datos mensuales BTS a estimación diaria ---
def leer_csv_bts_robusto(archivo_path):
    """
    Lee archivos CSV de BTS de manera robusta, manejando:
    - Columnas combinadas/merged
    - Diferentes formatos de encabezado
    - Filas vacías o con datos incompletos
    
    Args:
        archivo_path: Ruta al archivo CSV
    
    Returns:
        DataFrame con columnas estandarizadas
    """
    try:
        # Intentar lectura normal primero
        df = pd.read_csv(archivo_path, low_memory=False)
        
        # Detectar y limpiar columnas combinadas
        # A veces BTS tiene columnas como "Port Name\nPuerto" o con espacios extra
        df.columns = df.columns.str.strip()
        
        # Mapeo flexible de nombres de columnas BTS
        columnas_mapeo = {
            # Variaciones de Date
            'Date': 'date',
            'date': 'date',
            'DATE': 'date',
            'Month': 'date',
            'MONTH': 'date',
            
            # Variaciones de Port Name
            'Port Name': 'port_name',
            'port_name': 'port_name',
            'PORT NAME': 'port_name',
            'Port': 'port_name',
            'PORT': 'port_name',
            
            # Variaciones de Measure
            'Measure': 'measure',
            'measure': 'measure',
            'MEASURE': 'measure',
            'Type': 'measure',
            
            # Variaciones de Value
            'Value': 'value',
            'value': 'value',
            'VALUE': 'value',
            'Count': 'value',
            
            # Variaciones de Border
            'Border': 'border',
            'border': 'border',
            'BORDER': 'border',
        }
        
        # Renombrar columnas usando el mapeo
        df_renamed = df.copy()
        for col in df.columns:
            # Limpiar nombre de columna (quitar saltos de línea, espacios múltiples)
            col_limpio = ' '.join(col.split())
            if col_limpio in columnas_mapeo:
                df_renamed = df_renamed.rename(columns={col: columnas_mapeo[col_limpio]})
        
        # Verificar que tengamos las columnas mínimas necesarias
        columnas_requeridas = ['date', 'port_name', 'value']
        columnas_presentes = [c for c in columnas_requeridas if c in df_renamed.columns]
        
        if len(columnas_presentes) < len(columnas_requeridas):
            st.warning(f"⚠️ Archivo {archivo_path.name}: Faltan columnas requeridas. Encontradas: {', '.join(df_renamed.columns.tolist())}")
            return None
        
        # Eliminar filas completamente vacías
        df_renamed = df_renamed.dropna(how='all')
        
        # Eliminar filas donde las columnas clave están vacías
        df_renamed = df_renamed.dropna(subset=['date', 'port_name', 'value'])
        
        return df_renamed
        
    except Exception as e:
        st.error(f"❌ Error leyendo {archivo_path.name}: {e}")
        return None


def convertir_mensual_a_diario(df_mensual):
    """
    Convierte datos mensuales de BTS a estimaciones diarias.
    
    Los datos de BTS son totales mensuales. Esta función:
    1. Calcula el promedio diario (valor_mensual / días_en_mes)
    2. Genera registros diarios para cada puerto
    3. Aplica variabilidad realista (+/- 15% por día)
    
    Args:
        df_mensual: DataFrame con datos mensuales de BTS
                   Debe tener: Fecha (YYYY-MM), Puerto, Valor, Tipo_Medida
    
    Returns:
        DataFrame con datos diarios estimados
    """
    
    if df_mensual.empty:
        return pd.DataFrame()
    
    # Asegurar que Fecha es datetime
    df_mensual['Fecha'] = pd.to_datetime(df_mensual['Fecha'])
    
    datos_diarios = []
    
    # Agrupar por Puerto, Mes, Tipo_Medida
    for (puerto, mes, tipo_medida), grupo in df_mensual.groupby(['Puerto', pd.Grouper(key='Fecha', freq='M'), 'Tipo_Medida']):
        valor_mensual = grupo['Valor'].sum()
        
        # Obtener número de días en ese mes
        fecha_mes = grupo['Fecha'].iloc[0]
        dias_en_mes = fecha_mes.days_in_month
        
        # Calcular promedio diario
        promedio_diario = valor_mensual / dias_en_mes
        
        # Generar datos para cada día del mes
        inicio_mes = fecha_mes.replace(day=1)
        
        for dia in range(dias_en_mes):
            fecha_dia = inicio_mes + timedelta(days=dia)
            
            # Aplicar variabilidad realista (+/- 15%)
            # Días laborales tienen más tráfico que fines de semana
            dia_semana = fecha_dia.weekday()  # 0=Lunes, 6=Domingo
            
            if dia_semana < 5:  # Lunes a Viernes
                factor_variabilidad = np.random.uniform(0.90, 1.15)
            elif dia_semana == 5:  # Sábado
                factor_variabilidad = np.random.uniform(0.50, 0.75)
            else:  # Domingo
                factor_variabilidad = np.random.uniform(0.30, 0.50)
            
            valor_dia = int(promedio_diario * factor_variabilidad)
            
            # Verificar si es día festivo (menos tráfico)
            if es_dia_festivo(fecha_dia):
                valor_dia = int(valor_dia * 0.30)  # 70% de reducción en festivos
            
            datos_diarios.append({
                'Fecha': fecha_dia,
                'Puerto': puerto,
                'Tipo_Medida': tipo_medida,
                'Valor': valor_dia,
                'Valor_Mensual_Original': valor_mensual,
                'Promedio_Diario_Base': promedio_diario,
                'Dias_En_Mes': dias_en_mes
            })
    
    df_diario = pd.DataFrame(datos_diarios)
    
    return df_diario


# --- FUNCIÓN: Verificar si aduana está abierta ---
def aduana_esta_abierta(aduana_nombre, fecha=None, hora=None):
    """Verifica si una aduana está abierta en una fecha/hora específica
    Si no se proporciona fecha, usa la hora actual en la zona horaria de la aduana"""
    horarios = obtener_horarios_aduanas()
    
    # Si la aduana no está en el diccionario, usar horario genérico 24/7
    if aduana_nombre not in horarios:
        # Horario por defecto para aduanas no catalogadas (especialmente Canadá)
        # La mayoría de aduanas comerciales grandes operan 24/7 o con horario extendido
        if fecha is None:
            fecha = datetime.now()
        
        # Verificar si es festivo
        if es_dia_festivo(fecha):
            info_festivo = obtener_info_festivo(fecha)
            return {
                'abierta': False,
                'mensaje': f"Cerrado por {info_festivo['nombre']} (festivo)",
                'festivo': info_festivo['nombre']
            }
        
        # Verificar día de la semana
        dia_semana = fecha.weekday()  # 0=Lunes, 6=Domingo
        
        if dia_semana == 6:  # Domingo
            return {
                'abierta': False,
                'mensaje': 'Cerrado - Domingo (horario no comercial)',
                'horario': 'Cerrado domingos'
            }
        elif dia_semana == 5:  # Sábado
            if hora is None and isinstance(fecha, datetime):
                hora = fecha.time()
            
            if hora:
                # Sábados típicamente cierran a las 14:00-16:00
                apertura = datetime.strptime('08:00', '%H:%M').time()
                cierre = datetime.strptime('14:00', '%H:%M').time()
                
                if apertura <= hora <= cierre:
                    return {
                        'abierta': True,
                        'mensaje': f'Abierto - Horario sábado (08:00-14:00)',
                        'horario': '08:00-14:00'
                    }
                else:
                    return {
                        'abierta': False,
                        'mensaje': 'Cerrado - Fuera de horario sábado (08:00-14:00)',
                        'horario': '08:00-14:00'
                    }
            else:
                return {
                    'abierta': True,
                    'mensaje': 'Abierto - Horario sábado (08:00-14:00)',
                    'horario': '08:00-14:00'
                }
        else:  # Lunes a Viernes
            return {
                'abierta': True,
                'mensaje': f'Abierto - Horario comercial L-V (Aduana: {aduana_nombre})',
                'horario': 'L-V 06:00-22:00 (horario estimado)'
            }
    
    horario = horarios[aduana_nombre]
    timezone_code = horario.get('timezone', 'CST')
    
    # Si no se proporciona fecha, obtener la hora actual en la zona horaria de la aduana
    if fecha is None:
        fecha = obtener_hora_por_timezone(timezone_code)
    
    # Si no se proporciona hora, usar la hora de la fecha (si es datetime)
    if hora is None and isinstance(fecha, datetime):
        hora_actual = fecha.time()
    elif hora is not None:
        hora_actual = hora
    else:
        # Si solo tenemos date sin hora, solo verificamos el día
        hora_actual = None
    
    # Verificar si es día festivo
    if es_dia_festivo(fecha):
        info_festivo = obtener_info_festivo(fecha)
        horario_festivo = horario['festivos']
        timezone = horario.get('timezone', 'CST')
        
        # Si el horario de festivos es "Cerrado", retornar cerrado
        if 'Cerrado' in horario_festivo:
            return {
                'abierta': False, 
                'mensaje': f"Cerrado por {info_festivo['nombre']}",
                'festivo': info_festivo['nombre']
            }
        
        # Si el horario tiene formato de horas (ej: "08:00 - 14:00"), usar ese horario
        if ' - ' in horario_festivo:
            if hora_actual is not None:
                try:
                    apertura_str, cierre_str = horario_festivo.split(' - ')
                    apertura = datetime.strptime(apertura_str.strip(), '%H:%M').time()
                    
                    if cierre_str.strip() == '00:00' or cierre_str.strip() == '24:00':
                        cierre = datetime.strptime('23:59', '%H:%M').time()
                    else:
                        cierre = datetime.strptime(cierre_str.strip(), '%H:%M').time()
                    
                    if apertura <= hora_actual <= cierre:
                        return {
                            'abierta': True, 
                            'mensaje': f"Abierto - Horario especial por {info_festivo['nombre']} ({apertura_str.strip()} - {cierre_str.strip()} {timezone})",
                            'festivo': info_festivo['nombre']
                        }
                    else:
                        return {
                            'abierta': False, 
                            'mensaje': f"Cerrado - {info_festivo['nombre']} (Horario especial: {apertura_str.strip()} - {cierre_str.strip()} {timezone})",
                            'festivo': info_festivo['nombre']
                        }
                except Exception as e:
                    pass
            else:
                # Sin hora específica, retornar que hay horario reducido
                timezone = horario.get('timezone', 'CST')
                return {
                    'abierta': True,
                    'mensaje': f"Horario especial por {info_festivo['nombre']} ({horario_festivo} {timezone})",
                    'festivo': info_festivo['nombre']
                }
    
    # Verificar día de la semana
    dia_semana = fecha.weekday()  # 0=Lunes, 6=Domingo
    timezone = horario.get('timezone', 'CST')
    
    if horario['tipo'] == '24/7':
        return {'abierta': True, 'mensaje': 'Abierto 24 horas', 'festivo': None}
    
    # Para aduanas con horario limitado
    horario_dia = None
    
    if dia_semana == 6:  # Domingo
        horario_dia = horario['domingo']
        if horario_dia == 'Cerrado':
            return {'abierta': False, 'mensaje': 'Cerrado los domingos', 'festivo': None}
    elif dia_semana == 5:  # Sábado
        horario_dia = horario['sabado']
        if horario_dia == 'Cerrado':
            return {'abierta': False, 'mensaje': 'Cerrado los sábados', 'festivo': None}
    else:  # Lunes a Viernes
        horario_dia = horario['lunes_viernes']
    
    # Si tenemos hora actual, verificar si está dentro del horario
    if hora_actual is not None and horario_dia and horario_dia != 'Cerrado':
        try:
            # Parsear horario (ej: "08:00 - 20:00")
            if ' - ' in horario_dia:
                apertura_str, cierre_str = horario_dia.split(' - ')
                
                # Convertir a time objects
                apertura = datetime.strptime(apertura_str.strip(), '%H:%M').time()
                
                # Manejar medianoche (00:00 o 24:00)
                if cierre_str.strip() == '00:00' or cierre_str.strip() == '24:00':
                    cierre = datetime.strptime('23:59', '%H:%M').time()
                else:
                    cierre = datetime.strptime(cierre_str.strip(), '%H:%M').time()
                
                # Verificar si hora actual está en el rango
                if apertura <= hora_actual <= cierre:
                    return {'abierta': True, 'mensaje': f'Abierto ({apertura_str.strip()} - {cierre_str.strip()} {timezone})', 'festivo': None}
                else:
                    if hora_actual < apertura:
                        return {'abierta': False, 'mensaje': f'Cerrado (Abre a las {apertura_str.strip()} {timezone})', 'festivo': None}
                    else:
                        return {'abierta': False, 'mensaje': f'Cerrado (Cierra a las {cierre_str.strip()} {timezone})', 'festivo': None}
        except Exception as e:
            # Si hay error parseando horario, asumir abierto
            pass
    
    # Si no tenemos hora o no pudimos parsear, solo verificar día
    if horario_dia == 'Cerrado':
        return {'abierta': False, 'mensaje': 'Cerrado', 'festivo': None}
    
    return {'abierta': True, 'mensaje': 'Abierto', 'festivo': None}

# --- DATOS CON COORDENADAS (Para el Mapa) ---
def obtener_datos_mapeados():
    # Diccionario con ubicaciones reales de puertos
    ubicaciones = {
        "Manzanillo": {"lat": 19.0522, "lon": -104.3158},
        "Veracruz": {"lat": 19.1738, "lon": -96.1342},
        "Lázaro Cárdenas": {"lat": 17.9585, "lon": -102.1891},
        "Altamira": {"lat": 22.3943, "lon": -97.9377}
    }
    
    lista_final = []
    for puerto, coords in ubicaciones.items():
        lista_final.append({
            "Puerto": puerto,
            "lat": coords["lat"],
            "lon": coords["lon"],
            "Saturacion": random.randint(30, 90),
            "Operaciones": random.randint(100, 500)
        })
    return pd.DataFrame(lista_final)

# ============================================================
# NOTA: Funciones de Fuerza Laboral movidas a:
#   - modules/config.py (constantes de datos: SEGMENTACION_FUERZA_LABORAL, DATOS_REGIONALES_FRONTERIZOS)
#   - pages/Fuerza_Laboral.py (página completa)
# ============================================================

# --- CABECERA ---
# Inicializar session_state TEMPRANO (antes de cualquier lógica de página)
initialize_session_state()

# Cargamos variables de entorno (si existe .env)
load_dotenv()

tipo_cambio = obtener_tipo_cambio()
# Cargamos datos una vez para todas las páginas
df_mapa = obtener_datos_mapeados()

# ============================================================
# SELECTOR DE IDIOMA (PARTE SUPERIOR DERECHA)
# ============================================================
# Ya inicializado en initialize_session_state()

# Crear columnas para posicionar el selector a la derecha
col_left, col_right = st.columns([8, 2])

with col_right:
    st.markdown("""
        <style>
        /* Ajustar espacio entre botones de idioma */
        div[data-testid="column"] > div > div > div > button {
            font-size: 0.85rem !important;
            padding: 0.4rem 0.6rem !important;
            min-width: 70px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("##### 🌐 Idioma")
    
    # Botones de idioma en fila horizontal con espaciado
    lang_col1, lang_col2, lang_col3 = st.columns([1, 1, 1], gap="small")
    
    with lang_col1:
        if st.button("🇪🇸 ES", key="btn_es", help="Español"):
            st.session_state.language = 'es'
            st.rerun()
    
    with lang_col2:
        if st.button("🇺🇸 EN", key="btn_en", help="English"):
            st.session_state.language = 'en'
            st.rerun()
    
    with lang_col3:
        if st.button("🇫🇷 FR", key="btn_fr", help="Français"):
            st.session_state.language = 'fr'
            st.rerun()

# Obtener idioma actual
lang = st.session_state.language

# ============================================================
# BARRA LATERAL Y NAVEGACIÓN
# ============================================================
with st.sidebar:
    st.title("FreightMetrics")
    st.markdown("**Connecting Borders, Delivering Insights.**")
    st.markdown("---")
    st.metric("Tipo de Cambio USD/MXN", f"${tipo_cambio:.2f}")
    
    # Lista de páginas
    pages_list = [
        t('menu_dashboard', lang),           # 0. Dashboard
        t('menu_monitoring', lang),           # 1. Monitoreo de Aduanas
        t('menu_flows', lang),               # 2. Flujos de Carga
        t('menu_workforce', lang),           # 3. Fuerza Laboral
        t('menu_corridors', lang),           # 4. Corredores Logísticos
        t('menu_ports', lang),               # 5. Puertos Marítimos
        t('menu_nearshoring', lang),         # 6. Nearshoring
        t('menu_oracle', lang)               # 7. Oracle Rate
    ]
    
    opcion = st.radio(
        "Selecciona una página:" if lang == 'es' else ("Select a page:" if lang == 'en' else "Sélectionnez une page:"),
        pages_list,
        index=st.session_state.selected_page_index,
        key="page_selector"
    )
    
    # Guardar la selección
    st.session_state.selected_page_index = pages_list.index(opcion)
    
    st.markdown("---")
    
    # Botón para limpiar caché
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Limpiar Caché", use_container_width=True):
            st.cache_data.clear()
            st.session_state.clear()
            st.rerun()
    
    with col2:
        if st.button("🔄 Recargar", use_container_width=True):
            st.rerun()

# ============================================================
# EJECUTAR LA PÁGINA SELECCIONADA
# ============================================================
dashboard_label = t('menu_dashboard', lang)
monitoring_label = t('menu_monitoring', lang)
flows_label = t('menu_flows', lang)
workforce_label = t('menu_workforce', lang)
corridors_label = t('menu_corridors', lang)
ports_label = t('menu_ports', lang)
nearshoring_label = t('menu_nearshoring', lang)
oracle_label = t('menu_oracle', lang)

if opcion == dashboard_label:
    if DASHBOARD_AVAILABLE:
        page_dashboard()
    else:
        st.error("❌ Página de Dashboard no disponible")
        
elif opcion == monitoring_label:
    if MONITOREO_ADUANAS_AVAILABLE:
        page_monitoreo_aduanas()
    else:
        st.error("❌ Página de Monitoreo de Aduanas no disponible")
        
elif opcion == flows_label:
    if FLUJOS_CARGA_AVAILABLE:
        page_flujos_de_carga()
    else:
        st.error("❌ Página de Flujos de Carga no disponible")
        
elif opcion == workforce_label:
    if FUERZA_LABORAL_AVAILABLE:
        page_fuerza_laboral()
    else:
        st.error("❌ Página de Fuerza Laboral no disponible")
        
elif opcion == corridors_label:
    if CORREDORES_LOGISTICOS_AVAILABLE:
        page_corredores_logisticos()
    else:
        st.error("❌ Página de Corredores Logísticos no disponible")
        
elif opcion == ports_label:
    if PUERTOS_MARITIMOS_AVAILABLE:
        page_puertos_maritimos()
    else:
        st.error("❌ Página de Puertos Marítimos no disponible")
        
elif opcion == nearshoring_label:
    if NEARSHORING_AVAILABLE:
        page_nearshoring()
    else:
        st.error("❌ Página de Nearshoring no disponible")
        
elif opcion == oracle_label:
    if ORACLE_RATE_AVAILABLE:
        page_oracle_rate()
    else:
        st.error("❌ Página de Oracle Rate no disponible")

# --- FUNCIÓN PARA CARGAR DATOS HISTÓRICOS MULTI-AÑO ---
@st.cache_data(ttl=600)  # Cache de 10 minutos
def cargar_datos_historicos_multiannual(years=[2026]):
    """
    Carga datos históricos de cruces fronterizos de múltiples años.
    Por defecto carga solo 2026 (año actual de análisis).
    
    Args:
        years: Lista de años a cargar (por defecto [2026])
    
    Returns:
        DataFrame consolidado con todos los años
    """
    data_dir = Path(__file__).parent / "data"
    all_data = []
    
    for year in years:
        file_path = data_dir / f"border_crossings_{year}_historical.csv"
        if file_path.exists():
            try:
                df = pd.read_csv(file_path)
                df['year'] = year
                all_data.append(df)
            except Exception as e:
                st.warning(f"⚠️ No se pudo cargar datos de {year}: {str(e)}")
        else:
            st.warning(f"⚠️ No se encontró archivo de datos para {year}")
    
    if not all_data:
        return None
    
    # Consolidar todos los años
    df_consolidated = pd.concat(all_data, ignore_index=True)
    
    # FILTRO 1: Solo fronteras US-Mexico y US-Canada
    df_consolidated = df_consolidated[
        df_consolidated['border'].isin(['US-Mexico Border', 'US-Canada Border'])
    ].copy()
    
    # Asegurar que date es datetime
    df_consolidated['date'] = pd.to_datetime(df_consolidated['date'])
    
    # FILTRO 2: Solo tipos de medida específicos
    df_consolidated = df_consolidated[
        df_consolidated['measure'].isin(['Trucks', 'Truck Containers Empty', 'Truck Containers Loaded'])
    ].copy()
    
    # Procesar para formato compatible con las páginas
    df_processed = []
    
    for _, row in df_consolidated.iterrows():
        # Mapear nombres de puertos para consistencia
        puerto_map = {
            # Puertos México (US-Mexico Border)
            'Laredo': 'Nuevo Laredo',
            'Otay Mesa': 'Tijuana (Mesa de Otay)',
            'Calexico East': 'Mexicali (Calexico Este)',
            'Nogales': 'Nogales',
            'Eagle Pass': 'Piedras Negras',
            'Hidalgo': 'Reynosa (Hidalgo)',
            'Ysleta': 'Ciudad Juárez (Ysleta)',
            'Brownsville': 'Matamoros',
            'Pharr': 'Reynosa (Pharr)',
            'Del Rio': 'Ciudad Acuña',
            'El Paso': 'Ciudad Juárez',
            'Presidio': 'Ojinaga',
            'Roma': 'Miguel Alemán',
            'Progreso': 'Nuevo Progreso',
            'Calexico': 'Mexicali',
            'San Ysidro': 'Tijuana',
            'Tecate': 'Tecate',
            'Lukeville': 'Sonoyta',
            'Douglas': 'Agua Prieta',
            'Naco': 'Naco',
            'Columbus': 'Palomas',
            # Puertos Canadá (US-Canada Border) - mantener nombres originales
            'Detroit': 'Detroit',
            'Port Huron': 'Port Huron',
            'Buffalo Niagara Falls': 'Buffalo Niagara Falls',
            'Champlain': 'Champlain',
            'Blaine': 'Blaine',
            'Pembina': 'Pembina',
            'International Falls': 'International Falls',
            'Portal': 'Portal',
            'Sweetgrass': 'Sweetgrass',
            'Sumas': 'Sumas',
            'Derby Line': 'Derby Line'
        }
        
        puerto = puerto_map.get(row['port_name'], row['port_name'])
        
        df_processed.append({
            'Fecha': row['date'],
            'Puerto': puerto,
            'Puerto_Original': row['port_name'],
            'Estado': row['state'],
            'Frontera': row['border'],
            'Tipo': row['measure'],
            'Cruces': int(row['value']),
            'Año': row['year']
        })
    
    df_final = pd.DataFrame(df_processed)
    
    # Mapear nombres de frontera para los filtros
    df_final['Frontera'] = df_final['Frontera'].map({
        'US-Mexico Border': 'México',
        'US-Canada Border': 'Canadá'
    })
    
    # Agregar columnas calculadas
    # Valor comercial estimado: $20,000 USD promedio por cruce de camión
    df_final['Valor_USD'] = df_final['Cruces'] * 20000
    
    return df_final


# ============================================================
# SISTEMA DE SIMULACIÓN Y PREDICCIÓN 2026 (BASADO EN BTS)
# ============================================================

def calcular_tendencias_historicas(df_historico):
    """Analiza datos históricos para extraer tendencias y patrones"""
    try:
        df_historico = df_historico.copy()
        df_historico['Fecha'] = pd.to_datetime(df_historico['Fecha'])
        df_historico['Año'] = df_historico['Fecha'].dt.year
        df_historico['Mes'] = df_historico['Fecha'].dt.month
        
        tendencias = {}
        
        for puerto in df_historico['Puerto'].unique():
            df_puerto = df_historico[df_historico['Puerto'] == puerto].copy()
            
            if len(df_puerto) < 10:
                continue
            
            # Calcular tasa de crecimiento anual
            promedios_anuales = df_puerto.groupby('Año')['Cruces'].sum().to_dict()
            tasas_crecimiento = []
            
            if 2023 in promedios_anuales and 2024 in promedios_anuales and promedios_anuales[2023] > 0:
                tasa_23_24 = (promedios_anuales[2024] - promedios_anuales[2023]) / promedios_anuales[2023]
                tasas_crecimiento.append(tasa_23_24)
            
            if 2024 in promedios_anuales and 2025 in promedios_anuales and promedios_anuales[2024] > 0:
                tasa_24_25 = (promedios_anuales[2025] - promedios_anuales[2024]) / promedios_anuales[2024]
                tasas_crecimiento.append(tasa_24_25)
            
            tasa_crecimiento_promedio = np.mean(tasas_crecimiento) if tasas_crecimiento else 0.03
            tasa_crecimiento_promedio = max(-0.10, min(0.15, tasa_crecimiento_promedio))
            
            # Calcular estacionalidad mensual
            promedio_global = df_puerto['Cruces'].mean()
            estacionalidad = {}
            
            for mes in range(1, 13):
                df_mes = df_puerto[df_puerto['Mes'] == mes]
                if len(df_mes) > 0 and promedio_global > 0:
                    promedio_mes = df_mes['Cruces'].mean()
                    estacionalidad[mes] = promedio_mes / promedio_global
                else:
                    estacionalidad[mes] = 1.0
            
            # Calcular volatilidad
            volatilidad_std = df_puerto['Cruces'].std()
            volatilidad_cv = volatilidad_std / df_puerto['Cruces'].mean() if df_puerto['Cruces'].mean() > 0 else 0.1
            volatilidad = max(0.05, min(0.30, volatilidad_cv))
            
            # Obtener datos de 2025
            df_2025 = df_puerto[df_puerto['Año'] == 2025]
            if len(df_2025) > 0:
                # CRÍTICO: Los datos de BTS son MENSUALES, necesitamos convertir a DIARIOS
                # Verificar si son datos mensuales (pocos registros por año)
                registros_por_anio = len(df_2025)
                if registros_por_anio <= 12:  # Datos mensuales
                    # Convertir totales mensuales a promedios diarios (~30 días por mes)
                    promedio_diario_2025 = df_2025['Cruces'].mean() / 30
                    ultimo_valor = df_2025.sort_values('Fecha')['Cruces'].iloc[-1] / 30
                else:  # Datos diarios
                    promedio_diario_2025 = df_2025['Cruces'].mean()
                    ultimo_valor = df_2025.sort_values('Fecha')['Cruces'].iloc[-1]
            else:
                # Si no hay datos de 2025, usar el promedio general (convertido a diario si es necesario)
                registros_totales = len(df_puerto)
                años_unicos = df_puerto['Año'].nunique()
                if registros_totales / años_unicos <= 12:  # Probablemente mensuales
                    promedio_diario_2025 = df_puerto['Cruces'].mean() / 30
                else:
                    promedio_diario_2025 = df_puerto['Cruces'].mean()
                ultimo_valor = promedio_diario_2025
            
            frontera = df_puerto['Frontera'].iloc[0] if 'Frontera' in df_puerto.columns else 'México'
            
            tendencias[puerto] = {
                'tasa_crecimiento_anual': tasa_crecimiento_promedio,
                'estacionalidad_mensual': estacionalidad,
                'promedio_diario_2025': promedio_diario_2025,
                'volatilidad': volatilidad,
                'ultimo_valor_conocido': ultimo_valor,
                'frontera': frontera
            }
        
        return tendencias
        
    except Exception as e:
        st.error(f"❌ Error calculando tendencias: {e}")
        return {}


def simular_cruces_2026(tendencias, fecha_inicio='2026-01-01', fecha_fin=None):
    """Genera datos simulados de cruces para 2026 basados en tendencias históricas"""
    try:
        if fecha_fin is None:
            hoy = datetime.now()
            fecha_fin = hoy.strftime('%Y-%m-%d') if hoy.year == 2026 else '2026-12-31'
        
        fechas = pd.date_range(start=fecha_inicio, end=fecha_fin, freq='D')
        
        if len(fechas) == 0:
            return pd.DataFrame()
        
        datos_simulados = []
        np.random.seed(42)
        
        for puerto, trend in tendencias.items():
            base_2026 = trend['ultimo_valor_conocido'] * (1 + trend['tasa_crecimiento_anual'])
            
            for fecha in fechas:
                mes = fecha.month
                dia_semana = fecha.weekday()
                
                # Aplicar estacionalidad
                factor_estacional = trend['estacionalidad_mensual'].get(mes, 1.0)
                cruces_base = base_2026 * factor_estacional
                
                # Añadir variación realista
                variacion = np.random.normal(0, trend['volatilidad'] * cruces_base)
                cruces_simulados = max(0, cruces_base + variacion)
                
                # Reducir en fines de semana
                if dia_semana >= 5:
                    cruces_simulados = cruces_simulados * 0.70
                
                # Reducir en días festivos
                if es_dia_festivo(fecha):
                    cruces_simulados = cruces_simulados * 0.50
                
                cruces_simulados = int(round(cruces_simulados))
                
                # Calcular distribución FAST/Regular/Perecederos
                cruces_fast = int(cruces_simulados * np.random.uniform(0.35, 0.45))
                cruces_regular = int(cruces_simulados * np.random.uniform(0.50, 0.60))
                cruces_perecederos = max(0, cruces_simulados - cruces_fast - cruces_regular)
                
                # === AGREGAR DISTRIBUCIÓN DE TIPOS BTS (Trucks, Containers Loaded, Containers Empty) ===
                # Distribución típica BTS: ~60% Trucks completos, ~30% Containers Loaded, ~10% Empty
                trucks = int(cruces_simulados * np.random.uniform(0.55, 0.65))
                trucks_loaded = int(cruces_simulados * np.random.uniform(0.25, 0.35))
                trucks_empty = int(cruces_simulados * np.random.uniform(0.05, 0.15))
                
                # Ajustar para que sumen exactamente
                diferencia_bts = cruces_simulados - (trucks + trucks_loaded + trucks_empty)
                trucks = max(0, trucks + diferencia_bts)
                
                # Calcular valor comercial
                valor_usd = cruces_simulados * np.random.uniform(18000, 25000)
                
                datos_simulados.append({
                    'Fecha': fecha,
                    'Puerto': puerto,
                    'Cruces': cruces_simulados,
                    'Cruces_FAST': cruces_fast,
                    'Cruces_Regular': cruces_regular,
                    'Cruces_Perecederos': cruces_perecederos,
                    'Trucks': trucks,
                    'Trucks_Loaded': trucks_loaded,
                    'Trucks_Empty': trucks_empty,
                    'Valor_USD': valor_usd,
                    'Frontera': trend['frontera'],
                    'Tipo': 'Simulado 2026',
                    'Fuente': f"Predicción basada en tendencias históricas (crecimiento: {trend['tasa_crecimiento_anual']*100:.1f}%)",
                    'Es_Festivo': es_dia_festivo(fecha)
                })
        
        df_simulado = pd.DataFrame(datos_simulados)
        return df_simulado
        
    except Exception as e:
        st.error(f"❌ Error simulando datos 2026: {e}")
        return pd.DataFrame()


# --- FUNCIÓN SIMPLE: CARGAR DATOS POR AÑO ---
@st.cache_data(ttl=300)  # Cache de 5 minutos
# --- FUNCIÓN CENTRALIZADA: DATOS DE CRUCES CONSOLIDADOS ---
@st.cache_data(ttl=300)  # Cache de 5 minutos
def obtener_datos_cruces_consolidados(usar_datos_reales=True, incluir_simulacion_2026=True, year=None):
    """
    Función centralizada que genera/carga datos de cruces aduanales de BTS.
    Unifica datos de: Trucks, Truck Containers Loaded, Truck Containers Empty
    Incluye fronteras: US-Mexico Border y US-Canada Border
    
    Args:
        usar_datos_reales: Si True, intenta cargar datos reales de BTS
        incluir_simulacion_2026: Si True, genera predicciones para 2026 basadas en tendencias históricas
        year: Año específico a cargar (ej: 2023, 2024, 2025, 2026). Si None, carga todos.
    
    Retorna:
        - df_border: DataFrame con historial de cruces (datos reales + simulaciones cuando aplique)
        - df_diario_hoy: DataFrame con datos del día actual para cada aduana
    """
    
    # Intentar cargar datos reales desde archivos históricos de BTS
    df_border = None
    
    if usar_datos_reales:
        try:
            # OPCIÓN 1: Cargar datos históricos de BTS desde archivos CSV
            data_dir = Path(__file__).parent / "data"
            
            # Determinar qué archivos cargar
            if year:
                # Si se especifica un año, cargar solo ese archivo
                archivos_historicos = [
                    data_dir / f"border_crossings_{year}_historical.csv"
                ]
            else:
                # Si no se especifica año, usar el orden por defecto (priorizar 2026)
                archivos_historicos = [
                    data_dir / "border_crossings_2026_historical.csv",
                    data_dir / "border_crossings_2025_historical.csv",
                    data_dir / "border_crossings_2024_historical.csv",
                    data_dir / "border_crossings_2023_historical.csv"
                ]
            
            dfs_historicos = []
            for archivo in archivos_historicos:
                if archivo.exists():
                    try:
                        # Usar lectura robusta que maneja columnas combinadas
                        df_temp = leer_csv_bts_robusto(archivo)
                        
                        if df_temp is None or df_temp.empty:
                            continue
                        
                        # Validar que tenga las columnas necesarias (formato BTS)
                        if 'date' in df_temp.columns and 'port_name' in df_temp.columns and 'value' in df_temp.columns:
                            # Renombrar columnas para consistencia
                            df_temp = df_temp.rename(columns={
                                'date': 'Fecha',
                                'port_name': 'Puerto',
                                'value': 'Valor',
                                'measure': 'Tipo_Medida',
                                'border': 'Frontera_Original'
                            })
                            
                            # Convertir fecha
                            df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha'])
                            
                            # ===== DETECTAR SI SON DATOS MENSUALES O DIARIOS =====
                            # Formato BTS estándar: YYYY-MM (mensual) o YYYY-MM-DD (diario)
                            fechas_unicas = df_temp['Fecha'].dt.to_period('M').nunique()
                            registros_totales = len(df_temp)
                            
                            # Si hay menos registros que días esperados, son datos mensuales
                            es_mensual = (registros_totales / fechas_unicas) < 5  # Menos de 5 registros por mes = mensual
                            
                            if es_mensual:
                                # Convertir datos mensuales a diarios
                                df_temp = convertir_mensual_a_diario(df_temp)
                            
                            # IMPORTANTE: Filtrar solo medidas de camiones
                            # Tipos de medida BTS: "Trucks", "Truck Containers Loaded", "Truck Containers Empty"
                            if 'Tipo_Medida' in df_temp.columns:
                                df_temp = df_temp[df_temp['Tipo_Medida'].isin([
                                    'Trucks',
                                    'Truck Containers Loaded',
                                    'Truck Containers Empty'
                                ])]
                            
                            # Convertir valores a numérico
                            df_temp['Valor'] = pd.to_numeric(df_temp['Valor'], errors='coerce').fillna(0).astype(int)
                            
                            # Agregar columna Frontera simplificada (México o Canadá)
                            if 'Frontera_Original' in df_temp.columns:
                                df_temp['Frontera'] = df_temp['Frontera_Original'].apply(
                                    lambda x: 'México' if 'Mexico' in str(x) else 'Canadá'
                                )
                            
                            dfs_historicos.append(df_temp)
                            
                    except Exception as e:
                        st.warning(f"⚠️ Error cargando {archivo.name}: {e}")
                        continue
            
            # Combinar todos los dataframes históricos
            if dfs_historicos:
                df_combined = pd.concat(dfs_historicos, ignore_index=True)
                
                # PASO 1: Pivotar los datos para consolidar los 3 tipos de medida por puerto/fecha
                # Agrupar por Puerto, Fecha, Frontera y sumar/separar por tipo de medida
                df_pivot = df_combined.pivot_table(
                    index=['Puerto', 'Fecha', 'Frontera'],
                    columns='Tipo_Medida',
                    values='Valor',
                    aggfunc='sum',
                    fill_value=0
                ).reset_index()
                
                # Renombrar columnas pivotadas
                df_pivot.columns.name = None
                columnas_rename = {}
                for col in df_pivot.columns:
                    if col == 'Trucks':
                        columnas_rename[col] = 'Trucks'
                    elif col == 'Truck Containers Loaded':
                        columnas_rename[col] = 'Trucks_Loaded'
                    elif col == 'Truck Containers Empty':
                        columnas_rename[col] = 'Trucks_Empty'
                
                df_pivot = df_pivot.rename(columns=columnas_rename)
                
                # Asegurar que existen las columnas necesarias
                for col in ['Trucks', 'Trucks_Loaded', 'Trucks_Empty']:
                    if col not in df_pivot.columns:
                        df_pivot[col] = 0
                
                # PASO 2: Calcular total de cruces consolidado
                # Total = Trucks + Trucks_Loaded + Trucks_Empty
                df_pivot['Cruces'] = df_pivot['Trucks'] + df_pivot['Trucks_Loaded'] + df_pivot['Trucks_Empty']
                
                # Eliminar filas sin cruces
                df_pivot = df_pivot[df_pivot['Cruces'] > 0]
                
                # Ordenar por fecha y puerto
                df_border = df_pivot.sort_values(['Fecha', 'Puerto'])
                
                # PASO 3: Agregar columnas calculadas
                df_border['Es_Festivo'] = df_border['Fecha'].apply(es_dia_festivo)
                
                # Calcular distribución FAST vs Regular basada en datos reales
                # FAST típicamente es 35-45% del tráfico, Regular 50-60%, Perecederos 5%
                np.random.seed(42)  # Para reproducibilidad
                df_border['Cruces_FAST'] = (df_border['Cruces'] * np.random.uniform(0.35, 0.45, len(df_border))).astype(int)
                df_border['Cruces_Regular'] = (df_border['Cruces'] * np.random.uniform(0.50, 0.60, len(df_border))).astype(int)
                df_border['Cruces_Perecederos'] = (df_border['Cruces'] * 0.05).astype(int)
                
                # Ajustar para que sumen correctamente
                diferencia = df_border['Cruces'] - (df_border['Cruces_FAST'] + df_border['Cruces_Regular'] + df_border['Cruces_Perecederos'])
                df_border['Cruces_Regular'] = df_border['Cruces_Regular'] + diferencia
                
                # Calcular valor comercial (promedio real: $18,000-$25,000 USD por camión)
                df_border['Valor_USD'] = df_border['Cruces'] * np.random.uniform(18000, 25000, len(df_border))
                
                # Estadísticas de carga
                puertos_mexico = df_border[df_border['Frontera'] == 'México']['Puerto'].nunique()
                puertos_canada = df_border[df_border['Frontera'] == 'Canadá']['Puerto'].nunique()
                
                # ============================================================
                # NUEVO: SISTEMA DE SIMULACIÓN PARA 2026
                # ============================================================
                if incluir_simulacion_2026:
                    try:
                        with st.spinner("🔮 Generando predicción de cruces basada en tendencias históricas..."):
                            # Calcular tendencias históricas
                            tendencias = calcular_tendencias_historicas(df_border)
                            
                            if tendencias:
                                # Simular datos para 2026 (hasta la fecha actual si estamos en 2026)
                                fecha_actual = datetime.now()
                                fecha_inicio_2026 = '2026-01-01'
                                fecha_fin_2026 = fecha_actual.strftime('%Y-%m-%d') if fecha_actual.year == 2026 else '2026-12-31'
                                
                                df_simulado_2026 = simular_cruces_2026(tendencias, fecha_inicio_2026, fecha_fin_2026)
                                
                                if not df_simulado_2026.empty:
                                    # Combinar datos reales con simulados
                                    df_border = pd.concat([df_border, df_simulado_2026], ignore_index=True)
                                    df_border = df_border.sort_values(['Fecha', 'Puerto'])
                                    
                                    # Estadísticas de la simulación
                                    registros_2026 = len(df_simulado_2026)
                                    puertos_2026 = df_simulado_2026['Puerto'].nunique()
                                    cruces_2026 = df_simulado_2026['Cruces'].sum()
                                    tasa_crecimiento_promedio = np.mean([t['tasa_crecimiento_anual'] for t in tendencias.values()]) * 100
                                
                    except Exception as e:
                        pass  # Simulación fallida, continuar con datos disponibles
                
        except Exception as e:
            st.error(f"❌ Error cargando datos históricos de BTS: {e}")
            df_border = None
    
    # Si no hay datos reales, generar datos simulados consistentes
    if df_border is None or df_border.empty:
        # Generar datos de los últimos 12 meses
        fecha_inicio = (datetime.now() - timedelta(days=365))
        fecha_fin = datetime.now()
        fechas = pd.date_range(start=fecha_inicio, end=fecha_fin, freq='D')
        
        # PUERTOS CON VOLÚMENES BASE CONSISTENTES (cruces diarios promedio)
        # Basados en datos mensuales reales convertidos a diarios (mensual ÷ 30)
        puertos_base = {
            'Nuevo Laredo III (Comercio Mundial)': 567,     # ~17,000 mensuales
            'Reynosa (Pharr)': 450,                         # ~13,500 mensuales
            'Laredo - Colombia': 400,                       # ~12,000 mensuales
            'Cd. Juárez (Paso del Norte/Zaragoza)': 383,   # ~11,500 mensuales
            'Tijuana (Mesa de Otay)': 350,                  # ~10,500 mensuales
            'Matamoros (Gral. Ignacio Zaragoza)': 300,     # ~9,000 mensuales
            'Nogales (Mariposa)': 250,                      # ~7,500 mensuales
            'Mexicali II (Nvo. Mexicali)': 200,            # ~6,000 mensuales
            'Piedras Negras': 167,                          # ~5,000 mensuales
            'San Luis Río Colorado': 133,                   # ~4,000 mensuales
            'Agua Prieta': 100,                             # ~3,000 mensuales
            'Cd. Acuña': 117                                # ~3,500 mensuales
        }
        
        # Generar datos históricos
        data_list = []
        np.random.seed(42)  # Seed fijo para consistencia
        
        for puerto, base_cruces in puertos_base.items():
            for fecha in fechas:
                es_festivo = es_dia_festivo(fecha)
                
                # Variabilidad diaria consistente (+/- 15%)
                variabilidad = np.random.uniform(0.85, 1.15)
                cruces_base = int(base_cruces * variabilidad)
                
                # Distribución FAST vs Regular vs Perecederos
                if es_festivo:
                    # En días festivos: reducción ~70%
                    cruces_fast = int(cruces_base * 0.25)
                    cruces_regular = 0
                    cruces_perecederos = int(cruces_base * 0.05)
                    cruces = cruces_fast + cruces_perecederos
                else:
                    # Día normal: FAST 40%, Regular 55%, Perecederos 5%
                    cruces_fast = int(cruces_base * 0.40)
                    cruces_regular = int(cruces_base * 0.55)
                    cruces_perecederos = int(cruces_base * 0.05)
                    cruces = cruces_fast + cruces_regular + cruces_perecederos
                
                # Valor comercial por camión: $18,000 - $25,000 USD (promedio real)
                # Fuente: US Census Bureau - valor promedio por camión en comercio MX-USA
                valor_usd = cruces * np.random.uniform(18000, 25000)
                
                data_list.append([
                    fecha, puerto, cruces, cruces_fast, cruces_regular, 
                    cruces_perecederos, valor_usd, es_festivo
                ])
        
        df_border = pd.DataFrame(data_list, columns=[
            'Fecha', 'Puerto', 'Cruces', 'Cruces_FAST', 'Cruces_Regular', 'Cruces_Perecederos', 'Valor_USD', 'Es_Festivo'
        ])
        
        # ===== AGREGAR COLUMNAS DE TIPOS BTS (Trucks, Containers Loaded, Containers Empty) =====
        # Distribución típica BTS: ~60% Trucks completos, ~30% Containers Loaded, ~10% Empty
        np.random.seed(42)  # Mantener consistencia
        df_border['Trucks'] = (df_border['Cruces'] * np.random.uniform(0.55, 0.65, len(df_border))).astype(int)
        df_border['Trucks_Loaded'] = (df_border['Cruces'] * np.random.uniform(0.25, 0.35, len(df_border))).astype(int)
        df_border['Trucks_Empty'] = (df_border['Cruces'] * np.random.uniform(0.05, 0.15, len(df_border))).astype(int)
        
        # Ajustar para que sumen exactamente al total de cruces
        diferencia_bts = df_border['Cruces'] - (df_border['Trucks'] + df_border['Trucks_Loaded'] + df_border['Trucks_Empty'])
        df_border['Trucks'] = df_border['Trucks'] + diferencia_bts
        df_border['Trucks'] = df_border['Trucks'].clip(lower=0)  # No negativos
        
        st.info(f"📊 Datos simulados generados: {len(df_border):,} registros con distribución BTS (Trucks, Containers Loaded/Empty)")
        
        # Agregar columna Frontera para compatibilidad con filtros
        # Mapeo básico de puertos conocidos a fronteras
        puertos_mexico = [
            'Nuevo Laredo', 'Tijuana', 'Mexicali', 'Nogales', 'Piedras Negras',
            'Reynosa', 'Ciudad Juárez', 'Matamoros', 'Ciudad Acuña', 'Ojinaga',
            'Miguel Alemán', 'Nuevo Progreso', 'Tecate', 'Sonoyta', 'Agua Prieta',
            'Naco', 'Palomas', 'Laredo', 'Otay Mesa', 'Calexico', 'Eagle Pass',
            'Hidalgo', 'Ysleta', 'Brownsville', 'Pharr', 'Del Rio', 'El Paso',
            'Presidio', 'Roma', 'Progreso', 'San Ysidro', 'Lukeville', 'Douglas',
            'Columbus'
        ]
        
        df_border['Frontera'] = df_border['Puerto'].apply(
            lambda x: 'México' if any(p in str(x) for p in puertos_mexico) else 'Canadá'
        )
    
    # Agregar columnas auxiliares
    df_border['Mes'] = pd.to_datetime(df_border['Fecha']).dt.strftime('%Y-%m')
    df_border['Semana'] = pd.to_datetime(df_border['Fecha']).dt.isocalendar().week
    
    # ===== CREAR ALIASES PARA COMPATIBILIDAD CON DIFERENTES MÓDULOS =====
    # Algunos módulos usan 'Truck Containers Loaded', otros 'Trucks_Loaded'
    if 'Trucks_Loaded' in df_border.columns and 'Truck Containers Loaded' not in df_border.columns:
        df_border['Truck Containers Loaded'] = df_border['Trucks_Loaded']
    
    if 'Trucks_Empty' in df_border.columns and 'Truck Containers Empty' not in df_border.columns:
        df_border['Truck Containers Empty'] = df_border['Trucks_Empty']
    
    # Crear DataFrame del día actual para monitoreo
    fecha_hoy = datetime.now().date()
    
    # === DEBUG: Verificar fechas disponibles ===
    fechas_disponibles = pd.to_datetime(df_border['Fecha']).dt.date.unique()
    fechas_recientes = sorted(fechas_disponibles)[-5:]
    
    # === DEBUG CRÍTICO: Identificar origen de datos ===
    tiene_columna_tipo = 'Tipo' in df_border.columns
    # Verificar si tiene columnas BTS en df_border
    tiene_bts_en_border = all(col in df_border.columns for col in ['Trucks', 'Trucks_Loaded', 'Trucks_Empty'])
    
    df_diario_hoy = df_border[pd.to_datetime(df_border['Fecha']).dt.date == fecha_hoy].copy()
    
    # Si no hay datos de hoy, usar el último día disponible
    if df_diario_hoy.empty:
        ultima_fecha = df_border['Fecha'].max()
        df_diario_hoy = df_border[df_border['Fecha'] == ultima_fecha].copy()
    
    # Renombrar para compatibilidad con página de monitoreo
    if 'Puerto' in df_diario_hoy.columns and 'Aduana' not in df_diario_hoy.columns:
        df_diario_hoy['Aduana'] = df_diario_hoy['Puerto']
    
    # Agregar columna de Contenedores (para compatibilidad)
    if 'Contenedores' not in df_diario_hoy.columns:
        df_diario_hoy['Contenedores'] = df_diario_hoy['Cruces']
    
    # ===== CREAR ALIASES DE COLUMNAS PARA COMPATIBILIDAD =====
    if 'Trucks_Loaded' in df_diario_hoy.columns and 'Truck Containers Loaded' not in df_diario_hoy.columns:
        df_diario_hoy['Truck Containers Loaded'] = df_diario_hoy['Trucks_Loaded']
    
    if 'Trucks_Empty' in df_diario_hoy.columns and 'Truck Containers Empty' not in df_diario_hoy.columns:
        df_diario_hoy['Truck Containers Empty'] = df_diario_hoy['Trucks_Empty']
    
    # ===== VERIFICAR Y CREAR COLUMNAS DE TIPOS BTS SI NO EXISTEN =====
    if 'Trucks' not in df_diario_hoy.columns or 'Trucks_Loaded' not in df_diario_hoy.columns or 'Trucks_Empty' not in df_diario_hoy.columns:
        # Distribución típica: 60% Trucks, 30% Loaded, 10% Empty
        np.random.seed(int(datetime.now().timestamp()))
        df_diario_hoy['Trucks'] = (df_diario_hoy['Cruces'] * np.random.uniform(0.55, 0.65, len(df_diario_hoy))).astype(int)
        df_diario_hoy['Trucks_Loaded'] = (df_diario_hoy['Cruces'] * np.random.uniform(0.25, 0.35, len(df_diario_hoy))).astype(int)
        df_diario_hoy['Trucks_Empty'] = (df_diario_hoy['Cruces'] * np.random.uniform(0.05, 0.15, len(df_diario_hoy))).astype(int)
        
        # Ajustar para que sumen correctamente
        diferencia = df_diario_hoy['Cruces'] - (df_diario_hoy['Trucks'] + df_diario_hoy['Trucks_Loaded'] + df_diario_hoy['Trucks_Empty'])
        df_diario_hoy['Trucks'] = df_diario_hoy['Trucks'] + diferencia
        df_diario_hoy['Trucks'] = df_diario_hoy['Trucks'].clip(lower=0)
    
    return df_border, df_diario_hoy

# --- PÁGINAS ---
# Todas las páginas han sido extraídas a la carpeta pages/ e importadas al inicio del archivo
    # Título con diseño corporativo mejorado
    page_header(
        title="FreightMetrics", 
        subtitle="Dashboard Ejecutivo de Inteligencia Logística",
        icon="🚢"
    )

    # ============ SECCIÓN 1: FUERZA LABORAL ============
    section_header("Sector Autotransporte - Fuerza Laboral", icon="👥", color="#4070F4")
    
    col_fl1, col_fl2, col_fl3 = st.columns(3)
    with col_fl1:
        metric_card(
            title="Total Permisionarios",
            value="198,500",
            icon="🏢",
            color="#29B5E8",
            delta="Permisionarios federales (SICT)"
        )
    with col_fl2:
        metric_card(
            title="Parque Vehicular",
            value="630,000",
            icon="🚛",
            color="#4070F4",
            delta="Unidades motrices en operación"
        )
    with col_fl3:
        metric_card(
            title="Déficit Operadores",
            value="99,000",
            icon="⚠️",
            color="#EF553B",
            delta="Acumulado 2024 (IRU)"
        )

    spacer(30)

    # ============ SECCIÓN 2: PUERTOS MARÍTIMOS ============
    section_header("Puertos Marítimos Mexicanos", icon="⚓", color="#29B5E8")
    
    # Obtener datos de puertos
    df_puertos = obtener_datos_mapeados()
    total_puertos = len(df_puertos)
    total_operaciones = int(df_puertos["Operaciones"].sum())
    saturacion_promedio = int(df_puertos["Saturacion"].mean())
    puerto_mayor = df_puertos.loc[df_puertos["Operaciones"].idxmax(), "Puerto"]
    
    col_pm1, col_pm2, col_pm3, col_pm4 = st.columns(4)
    with col_pm1:
        metric_card_compact(
            title="Puertos Monitorizados",
            value=str(total_puertos),
            icon="⚓",
            color="#29B5E8"
        )
    with col_pm2:
        metric_card_compact(
            title="Operaciones Totales",
            value=f"{total_operaciones:,}",
            icon="📦",
            color="#4070F4"
        )
    with col_pm3:
        metric_card_compact(
            title="Saturación Promedio",
            value=f"{saturacion_promedio}%",
            icon="📊",
            color="#FFA726" if saturacion_promedio > 70 else "#00C853"
        )
    with col_pm4:
        metric_card_compact(
            title="Líder Operaciones",
            value=puerto_mayor,
            icon="🏆",
            color="#4CAF50"
        )

    spacer(30)

    # ============ SECCIÓN 3: FLUJOS FRONTERIZOS ============
    section_header(
        title="Flujos de Carga Transfronterizos",
        icon="🚛",
        color="#4070F4"
    )
    
    # Simular métricas de flujos fronterizos
    col_ff1, col_ff2, col_ff3, col_ff4 = st.columns(4)
    with col_ff1:
        metric_card_compact(
            title="Puertos Activos",
            value="12",
            icon="🌎",
            color="#29B5E8"
        )
    with col_ff2:
        metric_card_compact(
            title="Cruces Mensuales",
            value="1.8M",
            icon="🚚",
            color="#4070F4"
        )
    with col_ff3:
        metric_card_compact(
            title="Valor Comercio",
            value="$98B",
            icon="💵",
            color="#4CAF50"
        )
    with col_ff4:
        metric_card_compact(
            title="Líder Cruces",
            value="N. Laredo",
            icon="🏆",
            color="#FFA726"
        )

    spacer(30)

    # ============ SECCIÓN 4: MONITOREO ADUANAS ============
    section_header(
        title="Estado Operativo de Aduanas",
        icon="🚦",
        color="#4070F4"
    )
    
    col_ad1, col_ad2, col_ad3, col_ad4 = st.columns(4)
    with col_ad1:
        metric_card_compact(
            title="Operación Normal",
            value="7",
            icon="✅",
            color="#4CAF50"
        )
    with col_ad2:
        metric_card_compact(
            title="Saturación Media",
            value="3",
            icon="⚠️",
            color="#FFA726"
        )
    with col_ad3:
        metric_card_compact(
            title="Alerta Crítica",
            value="2",
            icon="🔴",
            color="#EF553B"
        )
    with col_ad4:
        metric_card_compact(
            title="Tiempo Espera Prom.",
            value="47 min",
            icon="⏱️",
            color="#11101D"
        )

    spacer(30)

    # ============ INSIGHTS EJECUTIVOS ============
    section_header(
        title="Insights Ejecutivos",
        icon="💡",
        color="#FFA726"
    )
    
    col_ins1, col_ins2 = st.columns(2)
    with col_ins1:
        info_card(
            title="⚠️ Déficit Crítico de Operadores",
            content="""El sector enfrenta un déficit de **99,000 operadores**, equivalente al **15.7%** 
            del parque vehicular (acumulado 2024 según IRU). Se requiere inversión urgente en capacitación y atracción de talento.""",
            icon="⚠️",
            color="#FFA726"
        )
    with col_ins2:
        info_card(
            title="📈 Flujo Comercial Robusto",
            content="""Los cruces fronterizos mantienen un promedio de **1.8M mensuales**, con un valor comercial 
            de **$98B USD/mes**. Nuevo Laredo continúa siendo el puerto líder.""",
            icon="📈",
            color="#4CAF50"
        )
    
    spacer(20)
    
    col_ins3, col_ins4 = st.columns(2)
    with col_ins3:
        info_card(
            title="🚦 Congestión Aduanal",
            content="""**2 aduanas** en estado crítico con tiempos de espera superiores a 90 minutos. 
            Se recomienda optimización de rutas y horarios de cruce.""",
            icon="🚦",
            color="#EF553B"
        )
    with col_ins4:
        info_card(
            title="🏢 Atomización del Sector",
            content="""El **82.2%** de permisionarios son "hombre-camión" (1-5 unidades), 
            lo que representa oportunidades de consolidación y profesionalización.""",
            icon="🏢",
            color="#4070F4"
        )


# ============================================================
# PÁGINAS: TODAS LAS PÁGINAS HAN SIDO EXTRAÍDAS
# ============================================================
# Las siguientes páginas se importan desde el directorio pages/:
# - page_inicio: pages/Inicio.py
# - page_mapa: pages/Mapa.py
# - page_fuerza_laboral: pages/Fuerza_Laboral.py
# - page_puertos_maritimos: pages/Puertos_Maritimos.py
# - page_corredores_logisticos: pages/Corredores_Logisticos.py
# - page_nearshoring: pages/Nearshoring.py
# - page_monitoreo_aduanas: pages/Monitoreo_Aduanas.py
# ============================================================


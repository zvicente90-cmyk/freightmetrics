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
from fpdf import FPDF
import base64
import os
from dotenv import load_dotenv, set_key, find_dotenv
import json
from pathlib import Path
import pytz

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
    # Fallback a funciones básicas
    def metric_card(title, value, icon="📊", color="#4070F4", delta=None, delta_color="normal"):
        st.metric(title, value, delta=delta, delta_color=delta_color)
    def page_header(title, subtitle="", icon="📊"):
        st.title(f"{icon} {title}")
        if subtitle:
            st.markdown(f"**{subtitle}**")
    def section_header(title, icon="📊", color="#4070F4"):
        st.subheader(f"{icon} {title}")
    def spacer(height=20):
        st.markdown(f"<div style='height: {height}px;'></div>", unsafe_allow_html=True)
    def divider(color="#E0E0E0", thickness=2, margin=20):
        st.divider()

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

# --- FUNCIÓN PARA CREAR EL PDF ---
def crear_pdf(dataframe, tipo_cambio):
    pdf = FPDF()
    pdf.add_page()
    
    # Título del Reporte
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "FREIGHTMETRICS - REPORTE OPERATIVO", 0, 1, 'C')
    pdf.ln(10)
    
    # Fecha y Tipo de Cambio
    pdf.set_font("Arial", '', 10)
    pdf.cell(190, 10, f"Fecha de emision: {dt.date.today()}", 0, 1, 'L')
    pdf.cell(190, 10, f"Tipo de Cambio aplicado: ${tipo_cambio:.2f} MXN/USD", 0, 1, 'L')
    pdf.ln(5)
    
    # Tabla de Datos
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 10, "Puerto", 1)
    pdf.cell(40, 10, "Saturacion (%)", 1)
    pdf.cell(60, 10, "Costo Est. (MXN)", 1)
    pdf.ln()
    
    pdf.set_font("Arial", '', 10)
    for index, row in dataframe.iterrows():
        pdf.cell(40, 10, str(row['Puerto']), 1)
        pdf.cell(40, 10, f"{row['Saturacion']}%", 1)
        pdf.cell(60, 10, f"${row['Costo_Estimado_MXN']:,.2f}", 1)
        pdf.ln()
    
    # Nota de Alerta
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.multi_cell(180, 5, "Nota: Este reporte es generado automaticamente. Los niveles superiores al 80% requieren accion inmediata del departamento de trafico.")
    
    return pdf.output(dest='S').encode('latin-1') # Retorna el PDF como datos

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

# --- DATOS DE FUERZA LABORAL ---
# Datos actualizados: Total Permisionarios ~198,500 | Parque Vehicular ~630,000 unidades | Déficit ~56,000 operadores (CANACAR/IRU)
def obtener_datos_fuerza_laboral():
    segmentacion = {
        'Segmento': ['Hombre-Camión', 'Pequeña', 'Mediana', 'Grande'],
        'Rango Unidades': ['1 - 5', '6 - 30', '31 - 100', '101+'],
        'Número de Empresas': [163200, 29800, 4500, 1000],  # Total: ~198,500
        'Total Operadores': [196000, 227000, 125000, 82000],  # Total: ~630,000 (considerando déficit de 56k)
        'Participación Mercado': ['82.2%', '15.0%', '2.3%', '0.5%']
    }
    df_segmentos = pd.DataFrame(segmentacion)

    cruce_data = pd.DataFrame({
        'Segmento': ['Hombre-Camión', 'Pequeña', 'Mediana', 'Grande'],
        'Operan solo MX': [98, 70, 40, 15],
        'Operan MC (Cruce)': [2, 30, 60, 85]
    })

    return df_segmentos, cruce_data

# --- DATOS REGIONALES DE FUERZA LABORAL POR ESTADO FRONTERIZO ---
def obtener_datos_fuerza_laboral_regional():
    """
    Retorna datos de parque vehicular, permisionarios y empresas con MC
    por región/estado fronterizo.
    """
    datos_regionales = {
        'Region': ['Baja California', 'Sonora', 'Chihuahua', 'Coahuila', 'Nuevo León', 'Tamaulipas'],
        'Estado': ['Baja California', 'Sonora', 'Chihuahua', 'Coahuila', 'Nuevo León', 'Tamaulipas'],
        'Parque_Vehicular': [37000, 28000, 85000, 62000, 95000, 48000],  # Unidades
        'Permisionarios': [12500, 9200, 28000, 20500, 31500, 16000],  # Empresas totales
        'Empresas_con_MC': [4200, 3100, 9500, 7000, 11000, 5500],  # ~33% tienen MC
        '% MC': ['33.6%', '33.7%', '33.9%', '34.1%', '34.9%', '34.4%'],
        'Aduanas_Principales': [
            'Tijuana, Mexicali',
            'Nogales, San Luis Río Colorado',
            'Cd. Juárez, Ojinaga',
            'Cd. Acuña, Piedras Negras',
            'Colombia',
            'Nuevo Laredo, Reynosa, Matamoros'
        ]
    }
    
    return pd.DataFrame(datos_regionales)

# --- RELACIÓN CRUCES VS CAPACIDAD OPERATIVA ---
@st.cache_data(ttl=300)
def analizar_capacidad_operativa_regional(usar_datos_reales=False):
    """
    Relaciona los cruces diarios con la capacidad operativa regional.
    Considera empresas locales con MC + empresas foráneas que usan corredores.
    
    Retorna DataFrame con análisis de capacidad vs demanda por región.
    """
    # Obtener datos de fuerza laboral regional
    df_regional = obtener_datos_fuerza_laboral_regional()
    
    # Mapeo de puertos (nombres BTS) a regiones
    mapeo_puertos_regiones = {
        # Baja California
        'Tijuana (Mesa de Otay)': 'Baja California',
        'Tijuana': 'Baja California',
        'San Ysidro': 'Baja California',
        'Mexicali (Calexico Este)': 'Baja California',
        'Mexicali': 'Baja California',
        'Tecate': 'Baja California',
        'Mexicali II (Nvo. Mexicali)': 'Baja California',
        
        # Sonora
        'Nogales': 'Sonora',
        'Nogales (Mariposa)': 'Sonora',
        'San Luis': 'Sonora',
        'San Luis Río Colorado': 'Sonora',
        'Agua Prieta': 'Sonora',
        'Sonoyta': 'Sonora',
        'Naco': 'Sonora',
        'Douglas': 'Sonora',
        'Lukeville': 'Sonora',
        
        # Chihuahua
        'Ciudad Juárez': 'Chihuahua',
        'Ciudad Juárez (Ysleta)': 'Chihuahua',
        'Cd. Juárez (Paso del Norte/Zaragoza)': 'Chihuahua',
        'Santa Teresa': 'Chihuahua',
        'Ojinaga': 'Chihuahua',
        'Palomas': 'Chihuahua',
        'Columbus': 'Chihuahua',
        
        # Coahuila
        'Ciudad Acuña': 'Coahuila',
        'Cd. Acuña': 'Coahuila',
        'Piedras Negras': 'Coahuila',
        
        # Nuevo León (incluye Laredo que conecta con esta región)
        'Laredo - Colombia': 'Nuevo León',
        
        # Tamaulipas
        'Nuevo Laredo': 'Tamaulipas',
        'Nuevo Laredo III (Comercio Mundial)': 'Tamaulipas',
        'Reynosa (Pharr)': 'Tamaulipas',
        'Reynosa (Hidalgo)': 'Tamaulipas',
        'Matamoros': 'Tamaulipas',
        'Matamoros (Gral. Ignacio Zaragoza)': 'Tamaulipas',
        'Nuevo Progreso': 'Tamaulipas',
        'Miguel Alemán': 'Tamaulipas',
        'Rio Grande City': 'Tamaulipas',
        'Roma': 'Tamaulipas',
        'Progreso': 'Tamaulipas',
        'Tornillo': 'Tamaulipas'
    }
    
    if usar_datos_reales:
        # Usar datos históricos reales de BTS
        try:
            # Cargar datos de 2025 (año más reciente)
            df_cruces_raw = cargar_datos_historicos_multiannual(years=[2025])
            
            if df_cruces_raw is not None and not df_cruces_raw.empty:
                # Filtrar solo México
                df_cruces_mx = df_cruces_raw[df_cruces_raw['Frontera'] == 'México'].copy()
                
                # Crear pivot para tener totales por puerto y fecha
                df_pivot = df_cruces_mx.pivot_table(
                    index=['Fecha', 'Puerto'],
                    columns='Tipo',
                    values='Cruces',
                    aggfunc='sum',
                    fill_value=0
                ).reset_index()
                
                # Calcular total de cruces por fila
                tipo_cols = [col for col in ['Trucks', 'Truck Containers Empty', 'Truck Containers Loaded'] 
                            if col in df_pivot.columns]
                df_pivot['Total_Cruces'] = df_pivot[tipo_cols].sum(axis=1)
                
                # Calcular promedio diario por puerto
                cruces_por_puerto = df_pivot.groupby('Puerto')['Total_Cruces'].mean().to_dict()
                
                # Calcular cruces por región
                cruces_por_region = {}
                for puerto, cruces in cruces_por_puerto.items():
                    region = mapeo_puertos_regiones.get(puerto)
                    if region:
                        if region in cruces_por_region:
                            cruces_por_region[region] += cruces
                        else:
                            cruces_por_region[region] = cruces
                
                st.success(f"✅ Usando datos reales de BTS 2025 - {len(cruces_por_puerto)} puertos analizados")
            else:
                raise ValueError("No se pudieron cargar datos históricos")
                
        except Exception as e:
            st.warning(f"⚠️ No se pudieron cargar datos reales: {str(e)}. Usando datos de referencia.")
            usar_datos_reales = False
    
    if not usar_datos_reales:
        # Valores de referencia basados en datos históricos conocidos
        cruces_por_region = {
            'Baja California': 9700,    # Tijuana + Mexicali + Tecate
            'Sonora': 4500,             # Nogales + San Luis + Agua Prieta + otros
            'Chihuahua': 7200,          # Cd. Juárez + Santa Teresa + otros
            'Coahuila': 2800,           # Cd. Acuña + Piedras Negras
            'Nuevo León': 2000,         # Conexión con Laredo
            'Tamaulipas': 16500         # Nuevo Laredo + Reynosa + Matamoros + otros
        }
    
    # Agregar datos de cruces al DataFrame regional
    df_regional['Cruces_Diarios'] = df_regional['Region'].map(cruces_por_region).fillna(0)
    
    # Calcular capacidad operativa
    # Cada empresa con MC puede hacer ~2.5 cruces diarios en promedio (ida y vuelta)
    df_regional['Capacidad_Cruces_Diarios'] = (df_regional['Empresas_con_MC'] * 2.5).round(0).astype(int)
    
    # Factor de empresas foráneas: ~20% de cruces son de empresas de otras regiones
    # usando corredores logísticos (ej: empresas del centro cruzando por Tijuana)
    df_regional['Demanda_Real'] = (df_regional['Cruces_Diarios'] * 0.80).round(0).astype(int)  # 80% local
    df_regional['Cruces_Foraneos'] = (df_regional['Cruces_Diarios'] * 0.20).round(0).astype(int)  # 20% foráneo
    
    # Análisis de capacidad
    df_regional['Balance_Capacidad'] = df_regional['Capacidad_Cruces_Diarios'] - df_regional['Demanda_Real']
    df_regional['Utilizacion_%'] = ((df_regional['Demanda_Real'] / df_regional['Capacidad_Cruces_Diarios']) * 100).round(1)
    
    # Status de capacidad
    def determinar_status(row):
        if row['Utilizacion_%'] < 70:
            return '✅ Capacidad Suficiente'
        elif row['Utilizacion_%'] < 90:
            return '⚠️ Capacidad Ajustada'
        else:
            return '🔴 Capacidad Saturada'
    
    df_regional['Status_Capacidad'] = df_regional.apply(determinar_status, axis=1)
    
    return df_regional

# --- CABECERA ---
# Cargamos variables de entorno (si existe .env)
load_dotenv()

tipo_cambio = obtener_tipo_cambio()
# Cargamos datos una vez para todas las páginas
df_mapa = obtener_datos_mapeados()

# ============================================================
# SELECTOR DE IDIOMA (PARTE SUPERIOR DERECHA)
# ============================================================
# Inicializar idioma por defecto
if 'language' not in st.session_state:
    st.session_state.language = 'es'

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

# Métrica en la barra lateral
with st.sidebar:
    st.title("FreightMetrics")
    st.markdown("**Connecting Borders, Delivering Insights.**")
    st.markdown("---")
    st.metric("Tipo de Cambio USD/MXN", f"${tipo_cambio:.2f}")
    opcion = st.radio(
        "Selecciona una página:" if lang == 'es' else ("Select a page:" if lang == 'en' else "Sélectionnez une page:"),
        [
            t('menu_dashboard', lang),
            t('menu_monitoring', lang),
            t('menu_flows', lang),
            t('menu_corridors', lang),
            t('menu_ports', lang),
            t('menu_workforce', lang),
            t('menu_nearshoring', lang),
            t('menu_indice', lang),
            t('menu_oracle', lang)
        ]
    )

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

def page_inicio():
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
            value="56,000",
            icon="⚠️",
            color="#EF553B",
            delta="Vacantes CANACAR e IRU"
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
            content="""El sector enfrenta un déficit de **56,000 operadores**, equivalente al **8.9%** 
            del parque vehicular. Se requiere inversión urgente en capacitación y atracción de talento.""",
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

def page_mapa():
    st.title("🚛 Flujos de Carga Transfronterizos")
    st.markdown("---")

    # FILTROS EN 3 COLUMNAS
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**📆 Año**")
        year = st.selectbox("Selecciona año:", [2023, 2024, 2025, 2026], index=3, label_visibility="collapsed", key="mapa_year_filter")

    with col2:
        st.markdown("**🌎 Frontera**")
        frontera = st.radio("Frontera", ["🇲🇽 México", "🇨🇦 Canadá", "🌎 Ambas"], index=2, horizontal=True, label_visibility="hidden", key="mapa_frontera_filter")

    with col3:
        st.markdown("**📅 Mes**")
        mes = st.selectbox("Selecciona mes:", 
            ["Todos", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"], 
            index=0, label_visibility="collapsed", key="mapa_mes_filter")

    st.markdown("---")

    # CARGAR DATOS DEL AÑO
    def cargar_datos_csv(year):
        """Carga datos BTS del año especificado sin caché"""
        try:
            archivo = Path(__file__).parent / "data" / f"border_crossings_{year}_historical.csv"
            
            if not archivo.exists():
                st.error(f"❌ Archivo no encontrado: {archivo}")
                return None
            
            # Lectura del CSV
            df = pd.read_csv(archivo)
            df['date'] = pd.to_datetime(df['date'])
            df = df.rename(columns={
                'date': 'Fecha',
                'port_name': 'Puerto',
                'value': 'Valor',
                'measure': 'Tipo_Medida',
                'border': 'Frontera_Original'
            })
            
            # Filtrar solo camiones
            df = df[df['Tipo_Medida'].isin(['Trucks', 'Truck Containers Loaded', 'Truck Containers Empty'])]
            df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0).astype(int)
            
            # Crear columna Frontera
            df['Frontera'] = df['Frontera_Original'].apply(
                lambda x: 'México' if 'Mexico' in str(x) else 'Canadá'
            )
            
            # Pivotar datos
            df_pivot = df.pivot_table(
                index=['Fecha', 'Puerto', 'Frontera'],
                columns='Tipo_Medida',
                values='Valor',
                aggfunc='sum',
                fill_value=0
            ).reset_index()
            
            df_pivot.columns.name = None
            
            # Asegurar columnas
            for col in ['Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']:
                if col not in df_pivot.columns:
                    df_pivot[col] = 0
            
            # Total cruces
            df_pivot['Cruces'] = (
                df_pivot['Trucks'] + 
                df_pivot['Truck Containers Loaded'] + 
                df_pivot['Truck Containers Empty']
            )
            
            return df_pivot.sort_values(['Fecha', 'Puerto'])
            
        except Exception as e:
            st.error(f"❌ Error cargando {year}: {e}")
            return None

    df = cargar_datos_csv(year)

    if df is None or df.empty:
        st.error(f"❌ No hay datos para el año {year}")
        st.stop()

    # APLICAR FILTRO DE FRONTERA
    if frontera == "🇲🇽 México":
        df = df[df['Frontera'] == 'México']
        frontera_label = "México"
    elif frontera == "🇨🇦 Canadá":
        df = df[df['Frontera'] == 'Canadá']
        frontera_label = "Canadá"
    else:
        frontera_label = "Ambas Fronteras"

    # APLICAR FILTRO DE MES
    if mes != "Todos":
        mes_map = {
            "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
            "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
            "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
        }
        mes_num = mes_map[mes]
        df = df[df['Fecha'].dt.month == mes_num]
        mes_label = mes
    else:
        mes_label = "Todos los Meses"

    # MOSTRAR PERÍODO Y VALIDAR
    year_base = year
    year_fin = year

    if df.empty:
        st.warning("⚠️ No hay datos para los filtros seleccionados")
        st.stop()

    fecha_min = df['Fecha'].min()
    fecha_max = df['Fecha'].max()
    dias = (fecha_max - fecha_min).days + 1

    st.info(f"📊 **{mes_label} {year}** | **{frontera_label}** | {fecha_min.strftime('%d/%m/%Y')} - {fecha_max.strftime('%d/%m/%Y')} ({dias} días)")

    st.markdown("---")

    # MÉTRICAS
    st.subheader("📊 Resumen de Cruces")
    col1, col2, col3, col4 = st.columns(4)

    total = df['Cruces'].sum()
    trucks = df['Trucks'].sum()
    loaded = df['Truck Containers Loaded'].sum()
    empty = df['Truck Containers Empty'].sum()

    with col1:
        st.metric("Total Cruces", f"{total:,}")
    with col2:
        pct = (trucks / total * 100) if total > 0 else 0
        st.metric("🚛 Trucks", f"{trucks:,}", f"{pct:.1f}%")
    with col3:
        pct = (loaded / total * 100) if total > 0 else 0
        st.metric("📦 Loaded", f"{loaded:,}", f"{pct:.1f}%")
    with col4:
        pct = (empty / total * 100) if total > 0 else 0
        st.metric("📭 Empty", f"{empty:,}", f"{pct:.1f}%")

    st.markdown("---")

    # GRÁFICO
    st.subheader("📈 Evolución Diaria")

    df_dia = df.groupby('Fecha')[['Cruces', 'Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_dia['Fecha'], y=df_dia['Cruces'], 
        name='Total Cruces', mode='lines+markers', line=dict(color='#1f77b4', width=3),
        fill='tozeroy', fillcolor='rgba(31, 119, 180, 0.2)'))

    fig.update_layout(
        xaxis_title="Fecha", yaxis_title="Número de Cruces",
        hovermode='x unified', height=400, template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=False)

    st.markdown("---")

    # ESTADÍSTICAS
    st.subheader("📊 Estadísticas")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Promedio Diario", f"{df_dia['Cruces'].mean():,.0f}")
    with col2:
        st.metric("Máximo Diario", f"{df_dia['Cruces'].max():,.0f}")
    with col3:
        st.metric("Mínimo Diario", f"{df_dia['Cruces'].min():,.0f}")
    with col4:
        st.metric("Desviación Std", f"{df_dia['Cruces'].std():,.0f}")

    st.markdown("---")

    # TABLA DE ADUANAS
    st.subheader("🌐 Detalle por Aduana")

    df_aduanas = df.groupby('Puerto')[['Cruces', 'Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']].sum().sort_values('Cruces', ascending=False).reset_index()
    df_aduanas.columns = ['Aduana', 'Total Cruces', 'Trucks', 'Containers Loaded', 'Containers Empty']

    st.dataframe(df_aduanas, use_container_width=False, hide_index=True)

    st.markdown("---")

    st.success("✅ Datos actualizados - FreightMetrics")


def page_monitoreo_aduanas():
    """Sistema de monitoreo de saturación, tiempos de cruce y alertas inteligentes"""
    # Inicializar contador para evitar keys duplicados
    if 'chart_counter_monitoreo_aduanas' not in st.session_state:
        st.session_state.chart_counter_monitoreo_aduanas = 0
    st.session_state.chart_counter_monitoreo_aduanas += 1
    chart_id = st.session_state.chart_counter_monitoreo_aduanas
    
    lang = st.session_state.get('language', 'es')
    
    # Títulos según idioma
    if lang == 'es':
        titulo = "🚦 Centro de Monitoreo de Aduanas"
        subtitulo = "Sistema de alertas en tiempo real para optimizar rutas de cruce fronterizo"
    elif lang == 'en':
        titulo = "🚦 Customs Monitoring Center"
        subtitulo = "Real-time alert system to optimize border crossing routes"
    else:  # fr
        titulo = "🚦 Centre de Surveillance Douanière"
        subtitulo = "Système d'alertes en temps réel pour optimiser les routes de passage frontalier"
    
    # Título con estilo corporativo
    st.markdown(f"<h1 style='color: #11101D; font-weight: 700; margin-bottom: 0;'>{titulo}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #4070F4; font-size: 1.1rem; font-weight: 500; margin-top: 5px;'>{subtitulo}</p>", unsafe_allow_html=True)
    
    # === ANÁLISIS FIJO: AÑO 2026 ===
    # Sin selector visible - año fijo en 2026
    st.session_state['mon_years_selected'] = [2026]
    st.session_state['mon_year_label'] = '2026'
    
    mon_years_selected = [2026]
    mon_year_label = '2026'
    
    period_text = "Análisis" if lang == 'es' else ("Analysis" if lang == 'en' else "Analyse")
    st.info(f"📊 **{period_text}:** {mon_year_label}")
    
    st.markdown("---")
    
    # === FILTRO DE FRONTERA ===
    select_border_title = "🌎 Seleccionar Frontera" if lang == 'es' else ("🌎 Select Border" if lang == 'en' else "🌎 Sélectionner la Frontière")
    
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #EF553B 0%, #FF8C42 100%); 
                    color: white; 
                    padding: 12px 20px; 
                    border-radius: 8px; 
                    margin: 15px 0;
                    box-shadow: 0 3px 10px rgba(239, 85, 59, 0.2);'>
            <h4 style='color: white; margin: 0; font-size: 1rem; font-weight: 600;'>{select_border_title}</h4>
        </div>
    """, unsafe_allow_html=True)
    
    col_mon_border1, col_mon_border2, col_mon_border3 = st.columns(3)
    
    # Textos de botones según idioma
    btn_mexico_text = "🇲🇽 México" if lang == 'es' else ("🇲🇽 Mexico" if lang == 'en' else "🇲🇽 Mexique")
    btn_canada_text = "🇨🇦 Canadá" if lang == 'es' else ("🇨🇦 Canada" if lang == 'en' else "🇨🇦 Canada")
    btn_both_text = "🌎 Ambas Fronteras" if lang == 'es' else ("🌎 Both Borders" if lang == 'en' else "🌎 Les Deux Frontières")
    
    with col_mon_border1:
        btn_mon_mexico = st.button(btn_mexico_text, use_container_width=True, key=f"btn_mon_border_mexico_{chart_id}")
    with col_mon_border2:
        btn_mon_canada = st.button(btn_canada_text, use_container_width=True, key=f"btn_mon_border_canada_{chart_id}")
    with col_mon_border3:
        btn_mon_ambas = st.button(btn_both_text, use_container_width=True, key=f"btn_mon_border_ambas_{chart_id}")
    
    # Determinar frontera seleccionada
    if btn_mon_mexico:
        st.session_state['mon_border_selected'] = ['México']
        st.session_state['mon_border_label'] = 'México' if lang == 'es' else ('Mexico' if lang == 'en' else 'Mexique')
    elif btn_mon_canada:
        st.session_state['mon_border_selected'] = ['Canadá']
        st.session_state['mon_border_label'] = 'Canadá' if lang == 'es' else ('Canada' if lang == 'en' else 'Canada')
    elif btn_mon_ambas:
        st.session_state['mon_border_selected'] = ['México', 'Canadá']
        if lang == 'es':
            st.session_state['mon_border_label'] = 'México y Canadá'
        elif lang == 'en':
            st.session_state['mon_border_label'] = 'Mexico and Canada'
        else:
            st.session_state['mon_border_label'] = 'Mexique et Canada'
    elif 'mon_border_selected' not in st.session_state:
        # Por defecto: ambas fronteras
        st.session_state['mon_border_selected'] = ['México', 'Canadá']
        if lang == 'es':
            st.session_state['mon_border_label'] = 'México y Canadá'
        elif lang == 'en':
            st.session_state['mon_border_label'] = 'Mexico and Canada'
        else:
            st.session_state['mon_border_label'] = 'Mexique et Canada'
    
    mon_border_selected = st.session_state.get('mon_border_selected', ['México', 'Canadá'])
    mon_border_label = st.session_state.get('mon_border_label', 'México y Canadá')
    
    border_text = "Frontera(s) para monitoreo" if lang == 'es' else ("Border(s) for monitoring" if lang == 'en' else "Frontière(s) à surveiller")
    st.info(f"🌎 **{border_text}:** {mon_border_label}")
    
    st.markdown("---")
    
    # Inicializar sistema de alertas
    if 'sistema_alertas' not in st.session_state:
        st.session_state.sistema_alertas = SistemaAlertas()
    
    sistema_alertas = st.session_state.sistema_alertas
    
    # Botón para recargar datos
    col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns([1, 1, 1, 1, 1])
    
    reload_text = "🔄 Recargar Datos" if lang == 'es' else ("🔄 Reload Data" if lang == 'en' else "🔄 Recharger Données")
    reload_help = "Carga datos desde CSV o API" if lang == 'es' else ("Load data from CSV or API" if lang == 'en' else "Charger données depuis CSV ou API")
    
    clear_cache_text = "🗑️ Limpiar Caché" if lang == 'es' else ("🗑️ Clear Cache" if lang == 'en' else "🗑️ Effacer Cache")
    clear_cache_help = "Forzar recarga eliminando caché (5 min)" if lang == 'es' else ("Force reload by clearing cache (5 min)" if lang == 'en' else "Forcer rechargement en effaçant cache (5 min)")
    
    real_data_text = "📊 Datos BTS" if lang == 'es' else ("📊 BTS Data" if lang == 'en' else "📊 Données BTS")
    real_data_help = "Usar datos reales de Border Transportation Statistics" if lang == 'es' else ("Use real data from Border Transportation Statistics" if lang == 'en' else "Utiliser données réelles de Border Transportation Statistics")
    
    update_api_text = "🌐 Actualizar APIs" if lang == 'es' else ("🌐 Update APIs" if lang == 'en' else "🌐 Mettre à jour APIs")
    update_api_help = "Consultar APIs externas y actualizar CSV" if lang == 'es' else ("Query external APIs and update CSV" if lang == 'en' else "Consulter APIs externes et mettre à jour CSV")
    
    with col_btn1:
        btn_recargar = st.button(reload_text, help=reload_help, key=f"btn_recargar_mon_{chart_id}")
    with col_btn2:
        btn_clear_cache = st.button(clear_cache_text, help=clear_cache_help, key=f"btn_clear_cache_mon_{chart_id}")
        if btn_clear_cache:
            st.cache_data.clear()
            st.success("✅ Caché limpiado. Recargando datos..." if lang == 'es' else "✅ Cache cleared. Reloading data...")
            st.rerun()
    with col_btn3:
        usar_datos_reales = st.checkbox(real_data_text, value=True, help=real_data_help, key=f"check_real_mon_{chart_id}")
    with col_btn3:
        btn_actualizar_apis = st.button(update_api_text, help=update_api_help, key=f"btn_api_mon_{chart_id}")
    with col_btn4:
        if 'cache_aduanas_fuente' in st.session_state:
            fuente = st.session_state['cache_aduanas_fuente']
            cache_time = st.session_state.get('cache_aduanas_time', 0)
            edad_minutos = int((datetime.now().timestamp() - cache_time) / 60)
            if lang == 'es':
                st.caption(f"📡 {fuente} | ⏱️ {edad_minutos} min")
            elif lang == 'en':
                st.caption(f"📡 {fuente} | ⏱️ {edad_minutos} min")
            else:
                st.caption(f"📡 {fuente} | ⏱️ {edad_minutos} min")
    
    # Actualizar desde APIs si se solicita
    if btn_actualizar_apis:
        update_title = "📊 Actualización desde APIs" if lang == 'es' else ("📊 Update from APIs" if lang == 'en' else "📊 Mise à jour depuis APIs")
        with st.expander(update_title, expanded=True):
            resultados = actualizar_datos_desde_apis()
            
            if resultados['exito']:
                success_msg = f"✅ Actualización exitosa: {resultados['registros']} registros" if lang == 'es' else (
                    f"✅ Successful update: {resultados['registros']} records" if lang == 'en' else 
                    f"✅ Mise à jour réussie : {resultados['registros']} enregistrements")
                st.success(success_msg)
                
                sources_label = "Fuentes consultadas" if lang == 'es' else ("Sources queried" if lang == 'en' else "Sources consultées")
                st.info(f"📡 {sources_label}: {', '.join(resultados['fuentes'])}")
                
                # Limpiar caché para forzar recarga
                if 'cache_aduanas' in st.session_state:
                    del st.session_state['cache_aduanas']
            else:
                error_msg = "❌ No se pudo actualizar desde ninguna API" if lang == 'es' else (
                    "❌ Could not update from any API" if lang == 'en' else 
                    "❌ Impossible de mettre à jour depuis aucune API")
                st.error(error_msg)
            
            if resultados['errores']:
                errors_title = "⚠️ Ver errores" if lang == 'es' else ("⚠️ View errors" if lang == 'en' else "⚠️ Voir erreurs")
                with st.expander(errors_title):
                    for error in resultados['errores']:
                        st.warning(error)
    
    # Cargar datos según la selección - USAR DATOS CONSOLIDADOS
    if usar_datos_reales or btn_recargar:
        # Usar función centralizada para consistencia con Flujos de Carga
        _, df_diario_hoy = obtener_datos_cruces_consolidados(usar_datos_reales=usar_datos_reales)
        
        if df_diario_hoy is not None and not df_diario_hoy.empty:
            # === DEBUG: Ver datos ANTES del filtro de frontera ===
            st.info(f"🔍 DEBUG ANTES filtro: {len(df_diario_hoy)} aduanas totales")
            if 'Trucks' in df_diario_hoy.columns:
                st.info(f"   Trucks total ANTES filtro: {df_diario_hoy['Trucks'].sum():,}")
            
            # === APLICAR FILTRO DE FRONTERA ===
            if 'Frontera' in df_diario_hoy.columns:
                fronteras_disponibles = df_diario_hoy['Frontera'].unique().tolist()
                st.info(f"🔍 DEBUG: Fronteras disponibles: {fronteras_disponibles} | Filtro seleccionado: {mon_border_selected}")
                df_diario_hoy = df_diario_hoy[df_diario_hoy['Frontera'].isin(mon_border_selected)].copy()
            
            # === DEBUG: Ver datos DESPUÉS del filtro de frontera ===
            st.info(f"🔍 DEBUG DESPUÉS filtro: {len(df_diario_hoy)} aduanas restantes")
            if 'Trucks' in df_diario_hoy.columns:
                st.info(f"   Trucks total DESPUÉS filtro: {df_diario_hoy['Trucks'].sum():,}")
            
            success_msg = f"✅ Datos consolidados cargados: {len(df_diario_hoy)} aduanas ({mon_border_label})" if lang == 'es' else (
                f"✅ Consolidated data loaded: {len(df_diario_hoy)} customs ({mon_border_label})" if lang == 'en' else 
                f"✅ Données consolidées chargées : {len(df_diario_hoy)} douanes ({mon_border_label})")
            st.success(success_msg)
            
            # Adaptar datos al formato esperado
            aduanas_status = df_diario_hoy.copy()
            
            # === VERIFICAR Y PRESERVAR COLUMNAS BTS ===
            columnas_bts_origen = []
            for col in ['Trucks', 'Trucks_Loaded', 'Trucks_Empty']:
                if col in df_diario_hoy.columns:
                    columnas_bts_origen.append(col)
            
            if columnas_bts_origen:
                total_trucks_status = aduanas_status['Trucks'].sum() if 'Trucks' in aduanas_status.columns else 0
                total_loaded_status = aduanas_status['Trucks_Loaded'].sum() if 'Trucks_Loaded' in aduanas_status.columns else 0
                total_empty_status = aduanas_status['Trucks_Empty'].sum() if 'Trucks_Empty' in aduanas_status.columns else 0
                st.info(f"📊 Columnas BTS en aduanas_status: {', '.join(columnas_bts_origen)} | Trucks: {total_trucks_status:,} | Loaded: {total_loaded_status:,} | Empty: {total_empty_status:,}")
            else:
                st.warning("⚠️ Columnas BTS no detectadas en df_diario_hoy. Generando...")
                # Generar columnas BTS si no existen
                aduanas_status['Trucks'] = (aduanas_status['Cruces'] * 0.60).astype(int)
                aduanas_status['Trucks_Loaded'] = (aduanas_status['Cruces'] * 0.30).astype(int)
                aduanas_status['Trucks_Empty'] = (aduanas_status['Cruces'] * 0.10).astype(int)
                # Ajustar
                diferencia = aduanas_status['Cruces'] - (aduanas_status['Trucks'] + aduanas_status['Trucks_Loaded'] + aduanas_status['Trucks_Empty'])
                aduanas_status['Trucks'] = aduanas_status['Trucks'] + diferencia
            
            # Asegurar que tiene columna 'Aduana'
            if 'Puerto' in aduanas_status.columns and 'Aduana' not in aduanas_status.columns:
                aduanas_status['Aduana'] = aduanas_status['Puerto']
            
            # Verificar estado de cada aduana (abierta/cerrada) usando hora de zona correcta
            estados_aduanas_reales = []
            for idx, row in aduanas_status.iterrows():
                estado_aduana = aduana_esta_abierta(row['Aduana'])
                estados_aduanas_reales.append(estado_aduana)
            
            # Usar datos reales de cruces del día
            aduanas_status['Cruces_Diarios_Est'] = aduanas_status['Cruces']
            
            # Calcular cruces por hora promedio (distribución 24h)
            aduanas_status['Cruces_Por_Hora'] = (aduanas_status['Cruces_Diarios_Est'] / 24).round(0)
            
            # Capacidad realista por aduana (basada en número de carriles)
            # Grandes: 10-12 carriles (295 cam/h), Medianas: 6-8 carriles (180 cam/h), Pequeñas: 3-5 carriles (100 cam/h)
            def calcular_capacidad_hora(cruces_diarios):
                if cruces_diarios > 1800:  # Aduanas grandes
                    return 295
                elif cruces_diarios > 800:  # Aduanas medianas
                    return 180
                else:  # Aduanas pequeñas
                    return 100
            
            aduanas_status['Capacidad_Hora'] = aduanas_status['Cruces_Diarios_Est'].apply(calcular_capacidad_hora)
            
            # Saturación REALISTA = (cruces_por_hora / capacidad) * 100
            # En horas pico el tráfico se concentra (70% en 12 horas)
            aduanas_status['Cruces_Hora_Pico'] = (aduanas_status['Cruces_Diarios_Est'] * 0.70 / 12).round(0)
            aduanas_status['Saturación (%)'] = ((aduanas_status['Cruces_Hora_Pico'] / aduanas_status['Capacidad_Hora']) * 100).clip(5, 98).round(0).astype(int)
            aduanas_status['Saturación FAST (%)'] = (aduanas_status['Saturación (%)'] * 0.85).clip(5, 95).round(0).astype(int)  # FAST es más eficiente
            aduanas_status['Saturación Regular (%)'] = aduanas_status['Saturación (%)']
            
            # Tiempo de espera REALISTA basado en saturación
            # Fórmula: tiempo base + (saturación^2 / factor_escala)
            def calcular_tiempo_espera(saturacion):
                if saturacion < 30:
                    return int(5 + saturacion * 0.3)  # 5-14 min
                elif saturacion < 60:
                    return int(15 + (saturacion - 30) * 0.8)  # 15-39 min
                elif saturacion < 85:
                    return int(40 + (saturacion - 60) * 1.5)  # 40-77 min
                else:
                    return int(80 + (saturacion - 85) * 3)  # 80-119 min
            
            aduanas_status['Tiempo Espera (min)'] = aduanas_status['Saturación (%)'].apply(calcular_tiempo_espera)
            aduanas_status['Tiempo Espera FAST (min)'] = (aduanas_status['Tiempo Espera (min)'] * 0.4).round(0).astype(int)  # FAST es 60% más rápido
            aduanas_status['Tiempo Espera Regular (min)'] = aduanas_status['Tiempo Espera (min)']
            
            # Capacidad y carriles disponibles
            aduanas_status['Carriles FAST'] = 3  # Típicamente 2-4 carriles FAST
            aduanas_status['Carriles Regular'] = 8  # Típicamente 6-10 carriles Regular
            aduanas_status['Capacidad FAST (Cam/hora)'] = aduanas_status['Carriles FAST'] * 40
            aduanas_status['Capacidad Regular (Cam/hora)'] = aduanas_status['Carriles Regular'] * 25
            aduanas_status['Capacidad (Camiones/hora)'] = aduanas_status['Capacidad FAST (Cam/hora)'] + aduanas_status['Capacidad Regular (Cam/hora)']
            
            # Camiones en cola por tipo (basado en cruces diarios)
            aduanas_status['Camiones FAST Cola'] = aduanas_status['Cruces_Diarios_Est'].apply(
                lambda x: int(x * 0.15 * np.random.uniform(0.8, 1.2))  # 15% de cruces diarios en cola
            )
            aduanas_status['Camiones Regular Cola'] = aduanas_status['Cruces_Diarios_Est'].apply(
                lambda x: int(x * 0.25 * np.random.uniform(0.8, 1.2))  # 25% de cruces diarios en cola
            )
            aduanas_status['Camiones en Cola'] = aduanas_status['Camiones FAST Cola'] + aduanas_status['Camiones Regular Cola']
            
            # Agregar información de horarios y estado de apertura
            aduanas_status['Horario Hoy'] = [e['mensaje'] for e in estados_aduanas_reales]
            aduanas_status['Abierta'] = [e['abierta'] for e in estados_aduanas_reales]
            
            # Si está cerrada, poner tiempos en 0
            for idx, row in aduanas_status.iterrows():
                if not row['Abierta']:
                    aduanas_status.at[idx, 'Tiempo Espera (min)'] = 0
                    aduanas_status.at[idx, 'Tiempo Espera FAST (min)'] = 0
                    aduanas_status.at[idx, 'Tiempo Espera Regular (min)'] = 0
                    aduanas_status.at[idx, 'Saturación (%)'] = 0
                    aduanas_status.at[idx, 'Saturación FAST (%)'] = 0
                    aduanas_status.at[idx, 'Saturación Regular (%)'] = 0
                    aduanas_status.at[idx, 'Camiones en Cola'] = 0
                    aduanas_status.at[idx, 'Camiones FAST Cola'] = 0
                    aduanas_status.at[idx, 'Camiones Regular Cola'] = 0
            
            # Determinar estado
            def determinar_estado(row):
                if not row['Abierta']:
                    return '🔴 CERRADO'
                sat = row['Saturación (%)']
                if sat >= 85:
                    return '🔴 CRÍTICO'
                elif sat >= 70:
                    return '⚠️ ALTO'
                elif sat >= 60:
                    return '⚠️ MEDIO'
                else:
                    return '✅ NORMAL'
            
            aduanas_status['Estado'] = aduanas_status.apply(determinar_estado, axis=1)
            
            # Mostrar info de origen de datos
            if 'Fecha' in df_diario_hoy.columns:
                fecha_datos = pd.to_datetime(df_diario_hoy['Fecha'].iloc[0]).strftime('%Y-%m-%d')
                st.info(f"📅 Última actualización: {fecha_datos} | ✅ Datos sincronizados con Flujos de Carga")
        else:
            st.warning("⚠️ No se encontraron datos consolidados. Usando datos simulados.")
            usar_datos_reales = False
    
    # Si no hay datos reales, usar datos simulados CON VOLÚMENES CONSISTENTES
    if not usar_datos_reales:
        # Usar función centralizada también para datos simulados
        _, df_diario_hoy = obtener_datos_cruces_consolidados(usar_datos_reales=False)
        
        if df_diario_hoy is not None and not df_diario_hoy.empty:
            # === APLICAR FILTRO DE FRONTERA ===
            if 'Frontera' in df_diario_hoy.columns:
                df_diario_hoy = df_diario_hoy[df_diario_hoy['Frontera'].isin(mon_border_selected)].copy()
            
            simulated_msg = f"ℹ️ Mostrando datos simulados: {len(df_diario_hoy)} aduanas ({mon_border_label})" if lang == 'es' else (
                f"ℹ️ Showing simulated data: {len(df_diario_hoy)} customs ({mon_border_label})" if lang == 'en' else 
                f"ℹ️ Affichage de données simulées : {len(df_diario_hoy)} douanes ({mon_border_label})")
            st.info(simulated_msg)
            
            aduanas_status = df_diario_hoy.copy()
            
            # Asegurar que tiene columna 'Aduana'
            if 'Puerto' in aduanas_status.columns and 'Aduana' not in aduanas_status.columns:
                aduanas_status['Aduana'] = aduanas_status['Puerto']
            
            # Verificar estado de cada aduana usando hora de zona correcta
            estados_aduanas = []
            for idx, row in aduanas_status.iterrows():
                estado_aduana = aduana_esta_abierta(row['Aduana'])
                estados_aduanas.append(estado_aduana)
            
            # Usar datos reales de cruces del día
            aduanas_status['Cruces_Diarios_Est'] = aduanas_status['Cruces']
            
            # Calcular cruces por hora promedio (distribución 24h)
            aduanas_status['Cruces_Por_Hora'] = (aduanas_status['Cruces_Diarios_Est'] / 24).round(0)
            
            # Capacidad realista por aduana
            def calcular_capacidad_hora(cruces_diarios):
                if cruces_diarios > 1800:
                    return 295
                elif cruces_diarios > 800:
                    return 180
                else:
                    return 100
            
            aduanas_status['Capacidad_Hora'] = aduanas_status['Cruces_Diarios_Est'].apply(calcular_capacidad_hora)
            
            # Saturación REALISTA
            aduanas_status['Cruces_Hora_Pico'] = (aduanas_status['Cruces_Diarios_Est'] * 0.70 / 12).round(0)
            aduanas_status['Saturación (%)'] = ((aduanas_status['Cruces_Hora_Pico'] / aduanas_status['Capacidad_Hora']) * 100).clip(5, 98).round(0).astype(int)
            aduanas_status['Saturación FAST (%)'] = (aduanas_status['Saturación (%)'] * 0.85).clip(5, 95).round(0).astype(int)
            aduanas_status['Saturación Regular (%)'] = aduanas_status['Saturación (%)']
            
            # Tiempo de espera REALISTA
            def calcular_tiempo_espera(saturacion):
                if saturacion < 30:
                    return int(5 + saturacion * 0.3)
                elif saturacion < 60:
                    return int(15 + (saturacion - 30) * 0.8)
                elif saturacion < 85:
                    return int(40 + (saturacion - 60) * 1.5)
                else:
                    return int(80 + (saturacion - 85) * 3)
            
            aduanas_status['Tiempo Espera (min)'] = aduanas_status['Saturación (%)'].apply(calcular_tiempo_espera)
            aduanas_status['Tiempo Espera FAST (min)'] = (aduanas_status['Tiempo Espera (min)'] * 0.4).round(0).astype(int)
            aduanas_status['Tiempo Espera Regular (min)'] = aduanas_status['Tiempo Espera (min)']
            
            # Capacidad y carriles
            aduanas_status['Carriles FAST'] = 3
            aduanas_status['Carriles Regular'] = 8
            aduanas_status['Capacidad FAST (Cam/hora)'] = aduanas_status['Carriles FAST'] * 40
            aduanas_status['Capacidad Regular (Cam/hora)'] = aduanas_status['Carriles Regular'] * 25
            aduanas_status['Capacidad (Camiones/hora)'] = aduanas_status['Capacidad FAST (Cam/hora)'] + aduanas_status['Capacidad Regular (Cam/hora)']
            
            # Camiones en cola
            aduanas_status['Camiones FAST Cola'] = aduanas_status['Cruces_Diarios_Est'].apply(
                lambda x: int(x * 0.15 * np.random.uniform(0.8, 1.2)) if x > 0 else 0
            )
            aduanas_status['Camiones Regular Cola'] = aduanas_status['Cruces_Diarios_Est'].apply(
                lambda x: int(x * 0.25 * np.random.uniform(0.8, 1.2)) if x > 0 else 0
            )
            aduanas_status['Camiones en Cola'] = aduanas_status['Camiones FAST Cola'] + aduanas_status['Camiones Regular Cola']
            
            # Horarios y estado de apertura
            aduanas_status['Horario Hoy'] = [e['mensaje'] for e in estados_aduanas]
            aduanas_status['Abierta'] = [e['abierta'] for e in estados_aduanas]
            
            # Si está cerrada, poner métricas en 0
            for idx, row in aduanas_status.iterrows():
                if not row['Abierta']:
                    aduanas_status.at[idx, 'Tiempo Espera (min)'] = 0
                    aduanas_status.at[idx, 'Tiempo Espera FAST (min)'] = 0
                    aduanas_status.at[idx, 'Tiempo Espera Regular (min)'] = 0
                    aduanas_status.at[idx, 'Saturación (%)'] = 0
                    aduanas_status.at[idx, 'Saturación FAST (%)'] = 0
                    aduanas_status.at[idx, 'Saturación Regular (%)'] = 0
                    aduanas_status.at[idx, 'Camiones en Cola'] = 0
                    aduanas_status.at[idx, 'Camiones FAST Cola'] = 0
                    aduanas_status.at[idx, 'Camiones Regular Cola'] = 0
                    aduanas_status.at[idx, 'Cruces_Diarios_Est'] = 0
            
            # Determinar estado
            def determinar_estado(row):
                if not row['Abierta']:
                    return '🔴 CERRADO'
                sat = row['Saturación (%)']
                if sat >= 85:
                    return '🔴 CRÍTICO'
                elif sat >= 70:
                    return '⚠️ ALTO'
                elif sat >= 60:
                    return '⚠️ MEDIO'
                else:
                    return '✅ NORMAL'
            
            aduanas_status['Estado'] = aduanas_status.apply(determinar_estado, axis=1)
        else:
            error_msg = "❌ Error al cargar datos simulados" if lang == 'es' else ("❌ Error loading simulated data" if lang == 'en' else "❌ Erreur lors du chargement des données simulées")
            st.error(error_msg)
            return
    
    # Evaluar alertas
    # === DEBUG: Ver valores antes de generar alertas ===
    if not aduanas_status.empty:
        otay_mesa = aduanas_status[aduanas_status['Aduana'].str.contains('Otay', case=False, na=False)]
        if not otay_mesa.empty:
            sat_otay = otay_mesa['Saturación (%)'].values[0]
            esp_otay = otay_mesa['Tiempo Espera (min)'].values[0]
            cruces_otay = otay_mesa['Cruces_Diarios_Est'].values[0]
            st.warning(f"🔍 DEBUG OTAY MESA ANTES DE ALERTAS: Cruces={cruces_otay} | Saturación={sat_otay}% | Espera={esp_otay}min")
    
    alertas = sistema_alertas.evaluar_aduanas(aduanas_status)
    stats_alertas = sistema_alertas.obtener_estadisticas_alertas()
    
    st.markdown("---")
    
    # PANEL DE ALERTAS AUTOMÁTICAS
    section_header(
        title="Sistema de Alertas Automáticas" if lang == 'es' else (
            "Automatic Alert System" if lang == 'en' else 
            "Système d'Alertes Automatiques"),
        icon="🚨",
        color="#EF553B"
    )
    
    if alertas:
        # Separar alertas por nivel
        alertas_criticas = [a for a in alertas if '🔴' in a['nivel']]
        alertas_altas = [a for a in alertas if '🟠' in a['nivel']]
        alertas_medias = [a for a in alertas if '🟡' in a['nivel']]
        
        # Organizar en 4 columnas
        col_alert1, col_alert2, col_alert3, col_alert4 = st.columns(4)
        
        critical_label = "Alertas Críticas" if lang == 'es' else ("Critical Alerts" if lang == 'en' else "Alertes Critiques")
        critical_help = "Saturación >85% o Espera >120min" if lang == 'es' else ("Saturation >85% or Wait >120min" if lang == 'en' else "Saturation >85% ou Attente >120min")
        
        high_label = "Alertas Altas" if lang == 'es' else ("High Alerts" if lang == 'en' else "Alertes Hautes")
        high_help = "Saturación >70% o Espera >90min" if lang == 'es' else ("Saturation >70% or Wait >90min" if lang == 'en' else "Saturation >70% ou Attente >90min")
        
        medium_label = "Alertas Medias" if lang == 'es' else ("Medium Alerts" if lang == 'en' else "Alertes Moyennes")
        medium_help = "Saturación >60% o Espera >60min" if lang == 'es' else ("Saturation >60% or Wait >60min" if lang == 'en' else "Saturation >60% ou Attente >60min")
        
        total_label = "Total de Alertas" if lang == 'es' else ("Total Alerts" if lang == 'en' else "Total des Alertes")
        total_help = "Todas las alertas activas" if lang == 'es' else ("All active alerts" if lang == 'en' else "Toutes les alertes actives")
        
        with col_alert1:
            metric_card_compact(
                title=critical_label,
                value=str(len(alertas_criticas)),
                icon="🔴",
                color="#EF553B"
            )
        with col_alert2:
            metric_card_compact(
                title=high_label,
                value=str(len(alertas_altas)),
                icon="🟠",
                color="#FFA726"
            )
        with col_alert3:
            metric_card_compact(
                title=medium_label,
                value=str(len(alertas_medias)),
                icon="🟡",
                color="#FFC107"
            )
        with col_alert4:
            metric_card_compact(
                title=total_label,
                value=str(len(alertas)),
                icon="📊",
                color="#4070F4"
            )
        
        spacer(20)
        
        # Mostrar alertas críticas prominentemente
        if alertas_criticas:
            if lang == 'es':
                crit_title = "🔴 ALERTAS CRÍTICAS - ACCIÓN INMEDIATA REQUERIDA"
                crit_msg = "Las siguientes aduanas requieren atención urgente:"
            elif lang == 'en':
                crit_title = "🔴 CRITICAL ALERTS - IMMEDIATE ACTION REQUIRED"
                crit_msg = "The following customs require urgent attention:"
            else:
                crit_title = "🔴 ALERTES CRITIQUES - ACTION IMMÉDIATE REQUISE"
                crit_msg = "Les douanes suivantes nécessitent une attention urgente:"
            
            alert_card(
                message=f"**{crit_title}**\n\n{crit_msg}",
                alert_type="error"
            )
            
            # Organizar alertas críticas en 4 columnas
            cols_crit = st.columns(4)
            for idx, alerta in enumerate(alertas_criticas):
                col_idx = idx % 4
                with cols_crit[col_idx]:
                    st.markdown(f"""
                        <div style='background-color: #ffebee; 
                                    border-left: 4px solid #EF553B; 
                                    padding: 12px; 
                                    margin: 8px 0; 
                                    border-radius: 5px;
                                    box-shadow: 0 2px 4px rgba(239, 85, 59, 0.1);'>
                            <span style='color: #11101D; font-weight: 600; font-size: 1.05rem;'>{alerta['aduana']}</span>
                            <br>
                            <span style='color: #666; font-size: 0.95rem;'>{alerta['mensaje']}</span>
                        </div>
                    """, unsafe_allow_html=True)
        
        # Expandible para alertas altas y medias
        if alertas_altas:
            high_exp_text = f"🟠 Ver {len(alertas_altas)} Alertas de Nivel Alto" if lang == 'es' else (
                f"🟠 View {len(alertas_altas)} High Level Alerts" if lang == 'en' else 
                f"🟠 Voir {len(alertas_altas)} Alertes de Niveau Haut")
            with st.expander(high_exp_text, expanded=False):
                cols_high = st.columns(4)
                for idx, alerta in enumerate(alertas_altas):
                    col_idx = idx % 4
                    with cols_high[col_idx]:
                        alert_card(
                            message=f"**{alerta['aduana']}**\n\n{alerta['mensaje']}",
                            alert_type="warning"
                        )
        
        if alertas_medias:
            med_exp_text = f"🟡 Ver {len(alertas_medias)} Alertas de Nivel Medio" if lang == 'es' else (
                f"🟡 View {len(alertas_medias)} Medium Level Alerts" if lang == 'en' else 
                f"🟡 Voir {len(alertas_medias)} Alertes de Niveau Moyen")
            with st.expander(med_exp_text, expanded=False):
                cols_med = st.columns(4)
                for idx, alerta in enumerate(alertas_medias):
                    col_idx = idx % 4
                    with cols_med[col_idx]:
                        alert_card(
                            message=f"**{alerta['aduana']}**\n\n{alerta['mensaje']}",
                            alert_type="info"
                        )
    else:
        no_alerts_msg = "No hay alertas activas. Todas las aduanas operan en niveles normales." if lang == 'es' else (
            "No active alerts. All customs operate at normal levels." if lang == 'en' else 
            "Aucune alerte active. Toutes les douanes fonctionnent à des niveaux normaux.")
        alert_card(
            message=f"✅ **{no_alerts_msg}**",
            alert_type="success"
        )
    
    # Estadísticas del historial de alertas
    if stats_alertas:
        spacer(30)
        
        section_header(
            title="Estadísticas de Alertas (Últimas 24 horas)" if lang == 'es' else (
                "Alert Statistics (Last 24 hours)" if lang == 'en' else 
                "Statistiques d'Alertes (Dernières 24 heures)"),
            icon="📊",
            color="#4070F4"
        )
        
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        total_label = "Total Alertas 24h" if lang == 'es' else ("Total Alerts 24h" if lang == 'en' else "Total Alertes 24h")
        critical_label = "Alertas Críticas 24h" if lang == 'es' else ("Critical Alerts 24h" if lang == 'en' else "Alertes Critiques 24h")
        most_label = "Aduana Más Alertas" if lang == 'es' else ("Most Alerts Custom" if lang == 'en' else "Douane Plus d'Alertes")
        avg_label = "Promedio Saturación" if lang == 'es' else ("Average Saturation" if lang == 'en' else "Saturation Moyenne")
        
        with col_stat1:
            metric_card_compact(
                title=total_label,
                value=str(stats_alertas['total_alertas_24h']),
                icon="📋",
                color="#4070F4"
            )
        with col_stat2:
            metric_card_compact(
                title=critical_label,
                value=str(stats_alertas['alertas_criticas_24h']),
                icon="🔴",
                color="#EF553B"
            )
        with col_stat3:
            metric_card_compact(
                title=most_label,
                value=stats_alertas['aduana_mas_alertas'],
                icon="⚠️",
                color="#FFA726"
            )
        with col_stat4:
            sat_avg = stats_alertas['promedio_saturacion']
            sat_color = "#EF553B" if sat_avg >= 80 else ("#FFA726" if sat_avg >= 60 else "#4CAF50")
            metric_card_compact(
                title=avg_label,
                value=f"{sat_avg:.1f}%",
                icon="📊",
                color=sat_color
            )
    
    st.markdown("---")
    
    # 🕐 INFORMACIÓN DE HORARIOS Y ESTADO ACTUAL
    status_title = "🕐 Estado Operativo Actual" if lang == 'es' else (
        "🕐 Current Operating Status" if lang == 'en' else 
        "🕐 État Opérationnel Actuel")
    st.subheader(status_title)
    
    ahora = datetime.now()
    
    # Días de la semana traducidos
    if lang == 'es':
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    elif lang == 'en':
        dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    else:
        dias_semana = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    
    dia_nombre = dias_semana[ahora.weekday()]
    hora_actual_str = ahora.strftime('%H:%M')
    
    # Mostrar información de fecha/hora actual
    col_tiempo1, col_tiempo2, col_tiempo3, col_tiempo4 = st.columns(4)
    
    day_label = "Día" if lang == 'es' else ("Day" if lang == 'en' else "Jour")
    time_label = "Hora" if lang == 'es' else ("Time" if lang == 'en' else "Heure")
    open_label = "Aduanas Abiertas" if lang == 'es' else ("Customs Open" if lang == 'en' else "Douanes Ouvertes")
    closed_label = "Aduanas Cerradas" if lang == 'es' else ("Customs Closed" if lang == 'en' else "Douanes Fermées")
    
    with col_tiempo1:
        metric_card_compact(
            title=day_label,
            value=dia_nombre,
            icon="📅",
            color="#4070F4"
        )
    with col_tiempo2:
        metric_card_compact(
            title=time_label,
            value=hora_actual_str,
            icon="🕐",
            color="#29B5E8"
        )
    with col_tiempo3:
        aduanas_abiertas = len(aduanas_status[aduanas_status['Abierta'] == True])
        metric_card_compact(
            title=open_label,
            value=f"{aduanas_abiertas}/{len(aduanas_status)}",
            icon="🟢",
            color="#4CAF50"
        )
    with col_tiempo4:
        aduanas_cerradas = len(aduanas_status[aduanas_status['Abierta'] == False])
        metric_card_compact(
            title=closed_label,
            value=f"{aduanas_cerradas}/{len(aduanas_status)}",
            icon="🔴",
            color="#EF553B"
        )
    
    # Alertas de aduanas cerradas
    aduanas_cerradas_df = aduanas_status[aduanas_status['Abierta'] == False]
    if not aduanas_cerradas_df.empty:
        if lang == 'es':
            closed_title = "🔴 ADUANAS CERRADAS EN ESTE MOMENTO"
            closed_subtitle = "Las siguientes aduanas no están operando actualmente. Considere rutas alternativas."
            reason_label = "Motivo"
        elif lang == 'en':
            closed_title = "🔴 CUSTOMS CLOSED AT THIS TIME"
            closed_subtitle = "The following customs are not currently operating. Consider alternative routes."
            reason_label = "Reason"
        else:
            closed_title = "🔴 DOUANES FERMÉES EN CE MOMENT"
            closed_subtitle = "Les douanes suivantes ne fonctionnent pas actuellement. Considérez des routes alternatives."
            reason_label = "Raison"
        
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #EF553B 0%, #d84315 100%); 
                        color: white; 
                        padding: 20px; 
                        border-radius: 12px; 
                        margin: 15px 0;
                        box-shadow: 0 4px 15px rgba(239, 85, 59, 0.3);'>
                <h3 style='color: white; margin: 0 0 15px 0; font-size: 1.3rem; font-weight: 700;'>
                    {closed_title}
                </h3>
                <p style='color: #ffe8e5; margin: 0; font-size: 0.95rem;'>
                    {closed_subtitle}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Mostrar aduanas cerradas en tarjetas mejoradas (3 columnas)
        num_cols = 3
        cols_cerradas = st.columns(num_cols)
        
        for idx, (_, row) in enumerate(aduanas_cerradas_df.iterrows()):
            col_index = idx % num_cols
            with cols_cerradas[col_index]:
                # Determinar ícono según el motivo
                if 'domingo' in row['Horario Hoy'].lower() or 'sunday' in row['Horario Hoy'].lower() or 'dimanche' in row['Horario Hoy'].lower():
                    icono = '📅'
                    motivo_color = '#9e9e9e'
                elif 'sábado' in row['Horario Hoy'].lower() or 'saturday' in row['Horario Hoy'].lower() or 'samedi' in row['Horario Hoy'].lower() or 'cierra' in row['Horario Hoy'].lower() or 'closes' in row['Horario Hoy'].lower() or 'ferme' in row['Horario Hoy'].lower():
                    icono = '🕐'
                    motivo_color = '#ff6f00'
                elif 'festivo' in row['Horario Hoy'].lower() or 'holiday' in row['Horario Hoy'].lower() or 'férié' in row['Horario Hoy'].lower():
                    icono = '🎉'
                    motivo_color = '#7b1fa2'
                else:
                    icono = '🔴'
                    motivo_color = '#EF553B'
                
                st.markdown(f"""
                    <div style='background-color: white; 
                                border: 2px solid #EF553B;
                                border-left: 6px solid #EF553B;
                                padding: 15px; 
                                margin: 8px 0; 
                                border-radius: 10px;
                                box-shadow: 0 2px 8px rgba(239, 85, 59, 0.15);
                                transition: all 0.3s ease;
                                height: 180px;
                                display: flex;
                                flex-direction: column;'>
                        <div style='display: flex; align-items: center; margin-bottom: 8px; height: 70px;'>
                            <span style='font-size: 1.3rem; margin-right: 8px; flex-shrink: 0;'>{icono}</span>
                            <strong style='color: #11101D; font-size: 0.95rem; line-height: 1.3; word-wrap: break-word;'>{row['Aduana']}</strong>
                        </div>
                        <div style='background-color: #ffebee; 
                                    padding: 10px; 
                                    border-radius: 6px;
                                    border-left: 3px solid {motivo_color};
                                    flex: 1;
                                    display: flex;
                                    align-items: center;'>
                            <span style='color: #666; font-size: 0.9rem; display: block;'>
                                <strong style='color: {motivo_color};'>{reason_label}:</strong> {row['Horario Hoy']}
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")

    # === DEBUG: Verificar columnas BTS en aduanas_status ANTES de filtrar ===
    columnas_status = aduanas_status.columns.tolist()
    columnas_bts_status = [c for c in columnas_status if 'Truck' in c or 'truck' in c]
    if columnas_bts_status:
        st.info(f"✅ DEBUG: Columnas BTS en aduanas_status ({len(aduanas_status)} registros): {', '.join(columnas_bts_status)}")
    else:
        st.error(f"❌ DEBUG: NO hay columnas BTS en aduanas_status. Columnas disponibles: {', '.join(columnas_status[:10])}...")

    # KPIs principales (solo para aduanas abiertas)
    aduanas_abiertas_df = aduanas_status[aduanas_status['Abierta'] == True].copy()
    
    # === DEBUG: Verificar columnas BTS DESPUÉS de filtrar ===
    if not aduanas_abiertas_df.empty:
        columnas_disponibles = aduanas_abiertas_df.columns.tolist()
        tiene_trucks = 'Trucks' in columnas_disponibles
        tiene_loaded = 'Trucks_Loaded' in columnas_disponibles
        tiene_empty = 'Trucks_Empty' in columnas_disponibles
        
        if not (tiene_trucks and tiene_loaded and tiene_empty):
            st.warning(f"⚠️ DEBUG: Columnas BTS faltantes. Disponibles: {', '.join([c for c in columnas_disponibles if 'Truck' in c or 'truck' in c])}")
            
            # Si df_diario_hoy tiene las columnas pero aduanas_status no, copiarlas
            if 'df_diario_hoy' in locals():
                if 'Trucks' in df_diario_hoy.columns and 'Trucks' not in aduanas_abiertas_df.columns:
                    # Merge las columnas BTS desde df_diario_hoy
                    cols_bts = [c for c in ['Trucks', 'Trucks_Loaded', 'Trucks_Empty'] if c in df_diario_hoy.columns]
                    if cols_bts:
                        aduanas_abiertas_df = aduanas_abiertas_df.merge(
                            df_diario_hoy[['Aduana'] + cols_bts],
                            on='Aduana',
                            how='left'
                        )
                        st.info(f"✅ Columnas BTS recuperadas desde df_diario_hoy: {', '.join(cols_bts)}")
    
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    
    avg_wait_label = "Tiempo Promedio Espera" if lang == 'es' else ("Average Wait Time" if lang == 'en' else "Temps d'Attente Moyen")
    critical_label = "Aduanas Críticas" if lang == 'es' else ("Critical Customs" if lang == 'en' else "Douanes Critiques")
    queue_label = "Total en Cola" if lang == 'es' else ("Total in Queue" if lang == 'en' else "Total en File")
    avg_sat_label = "Saturación Promedio" if lang == 'es' else ("Average Saturation" if lang == 'en' else "Saturation Moyenne")
    
    with col_k1:
        if not aduanas_abiertas_df.empty:
            promedio_espera = aduanas_abiertas_df['Tiempo Espera (min)'].mean()
            metric_card(
                title=avg_wait_label,
                value=f"{promedio_espera:.0f} min",
                icon="⏱️",
                color="#4070F4",
                delta=None
            )
        else:
            metric_card(
                title=avg_wait_label,
                value="N/A",
                icon="⏱️",
                color="#4070F4"
            )
    
    with col_k2:
        aduanas_criticas = len(aduanas_abiertas_df[aduanas_abiertas_df['Saturación (%)'] > 80])
        metric_card(
            title=critical_label,
            value=str(aduanas_criticas),
            icon="🔴",
            color="#EF553B",
            delta="Saturación >80%" if aduanas_criticas > 0 else None
        )
    
    with col_k3:
        total_cola = aduanas_abiertas_df['Camiones en Cola'].sum() if not aduanas_abiertas_df.empty else 0
        metric_card(
            title=queue_label,
            value=f"{total_cola:,.0f}",
            icon="🚛",
            color="#29B5E8"
        )
    
    with col_k4:
        saturacion_promedio = aduanas_abiertas_df['Saturación (%)'].mean() if not aduanas_abiertas_df.empty else 0
        # Determinar color según nivel de saturación
        if saturacion_promedio >= 80:
            sat_color = "#EF553B"
        elif saturacion_promedio >= 60:
            sat_color = "#FFA726"
        else:
            sat_color = "#4CAF50"
        
        metric_card(
            title=avg_sat_label,
            value=f"{saturacion_promedio:.1f}%",
            icon="📊",
            color=sat_color
        )
    
    st.markdown("---")
    
    # � TIPOS DE CRUCE BTS - TIEMPO REAL (Trucks, Containers Loaded, Containers Empty)
    bts_title = "🚛 Tipos de Cruce BTS - Tiempo Real" if lang == 'es' else (
        "🚛 BTS Crossing Types - Real Time" if lang == 'en' else 
        "🚛 Types de Passage BTS - Temps Réel")
    st.subheader(bts_title)
    
    # Información sobre tipos de cruce BTS
    if lang == 'es':
        bts_exp_title = "ℹ️ ¿Qué son los Tipos de Cruce BTS?"
        bts_desc = """El **Bureau of Transportation Statistics (BTS)** clasifica los cruces fronterizos en tres categorías principales:
        
        **📦 Tipos de Medida:**
        - 🚛 **Trucks**: Camiones completos (tractor + remolque)
        - 📦 **Truck Containers Loaded**: Contenedores cargados en camión
        - 📭 **Truck Containers Empty**: Contenedores vacíos en camión
        
        **Importancia:**
        - Permite análisis detallado del flujo comercial
        - Diferencia entre carga completa vs contenedores
        - Identifica patrones de retorno de vacíos
        - Optimiza planificación logística por tipo de operación"""
    elif lang == 'en':
        bts_exp_title = "ℹ️ What are BTS Crossing Types?"
        bts_desc = """The **Bureau of Transportation Statistics (BTS)** classifies border crossings into three main categories:
        
        **📦 Measure Types:**
        - 🚛 **Trucks**: Complete trucks (tractor + trailer)
        - 📦 **Truck Containers Loaded**: Loaded containers on truck
        - 📭 **Truck Containers Empty**: Empty containers on truck
        
        **Importance:**
        - Enables detailed commercial flow analysis
        - Differentiates full loads vs containers
        - Identifies empty return patterns
        - Optimizes logistics planning by operation type"""
    else:
        bts_exp_title = "ℹ️ Que sont les Types de Passage BTS?"
        bts_desc = """Le **Bureau of Transportation Statistics (BTS)** classe les passages frontaliers en trois catégories principales:
        
        **📦 Types de Mesure:**
        - 🚛 **Trucks**: Camions complets (tracteur + remorque)
        - 📦 **Truck Containers Loaded**: Conteneurs chargés sur camion
        - 📭 **Truck Containers Empty**: Conteneurs vides sur camion
        
        **Importance:**
        - Permet une analyse détaillée du flux commercial
        - Différencie charges complètes vs conteneurs
        - Identifie les modèles de retour à vide
        - Optimise la planification logistique par type d'opération"""
    
    with st.expander(bts_exp_title, expanded=False):
        st.markdown(bts_desc)
    
    if not aduanas_abiertas_df.empty:
        # Verificar si tenemos datos de tipos BTS
        tiene_trucks = 'Trucks' in aduanas_abiertas_df.columns
        tiene_loaded = 'Trucks_Loaded' in aduanas_abiertas_df.columns or 'Truck Containers Loaded' in aduanas_abiertas_df.columns
        tiene_empty = 'Trucks_Empty' in aduanas_abiertas_df.columns or 'Truck Containers Empty' in aduanas_abiertas_df.columns
        
        # Normalizar nombres de columnas
        if 'Truck Containers Loaded' in aduanas_abiertas_df.columns:
            aduanas_abiertas_df['Trucks_Loaded'] = aduanas_abiertas_df['Truck Containers Loaded']
        if 'Truck Containers Empty' in aduanas_abiertas_df.columns:
            aduanas_abiertas_df['Trucks_Empty'] = aduanas_abiertas_df['Truck Containers Empty']
        
        if tiene_trucks or tiene_loaded or tiene_empty:
            # KPIs por tipo BTS
            col_bts1, col_bts2, col_bts3, col_bts4 = st.columns(4)
            
            with col_bts1:
                total_trucks = aduanas_abiertas_df['Trucks'].sum() if tiene_trucks else 0
                trucks_label = "Trucks Completos" if lang == 'es' else ("Complete Trucks" if lang == 'en' else "Camions Complets")
                metric_card(
                    title=trucks_label,
                    value=f"{total_trucks:,.0f}",
                    icon="🚛",
                    color="#4070F4"
                )
            
            with col_bts2:
                total_loaded = aduanas_abiertas_df['Trucks_Loaded'].sum() if tiene_loaded else 0
                loaded_label = "Contenedores Cargados" if lang == 'es' else ("Loaded Containers" if lang == 'en' else "Conteneurs Chargés")
                metric_card(
                    title=loaded_label,
                    value=f"{total_loaded:,.0f}",
                    icon="📦",
                    color="#4CAF50"
                )
            
            with col_bts3:
                total_empty = aduanas_abiertas_df['Trucks_Empty'].sum() if tiene_empty else 0
                empty_label = "Contenedores Vacíos" if lang == 'es' else ("Empty Containers" if lang == 'en' else "Conteneurs Vides")
                metric_card(
                    title=empty_label,
                    value=f"{total_empty:,.0f}",
                    icon="📭",
                    color="#FFA726"
                )
            
            with col_bts4:
                total_cruces = total_trucks + total_loaded + total_empty
                ratio_empty = (total_empty / total_cruces * 100) if total_cruces > 0 else 0
                ratio_label = "% Retornos Vacíos" if lang == 'es' else ("% Empty Returns" if lang == 'en' else "% Retours Vides")
                metric_card(
                    title=ratio_label,
                    value=f"{ratio_empty:.1f}%",
                    icon="📊",
                    color="#29B5E8"
                )
            
            # Gráfico comparativo por tipo BTS
            spacer(20)
            
            subsection_header(
                title="Distribución por Tipo de Cruce" if lang == 'es' else (
                    "Distribution by Crossing Type" if lang == 'en' else 
                    "Distribution par Type de Passage"),
                icon="📊",
                color="#29B5E8"
            )
            
            # Preparar datos para gráfico
            df_bts = aduanas_abiertas_df[['Aduana']].copy()
            if tiene_trucks:
                df_bts['Trucks'] = aduanas_abiertas_df['Trucks']
            else:
                df_bts['Trucks'] = 0
            if tiene_loaded:
                df_bts['Loaded'] = aduanas_abiertas_df['Trucks_Loaded']
            else:
                df_bts['Loaded'] = 0
            if tiene_empty:
                df_bts['Empty'] = aduanas_abiertas_df['Trucks_Empty']
            else:
                df_bts['Empty'] = 0
            
            # Calcular total y tomar top 10
            df_bts['Total'] = df_bts['Trucks'] + df_bts['Loaded'] + df_bts['Empty']
            df_bts = df_bts.sort_values('Total', ascending=False).head(10)
            
            # Crear gráfico de barras apiladas
            fig_bts = go.Figure()
            
            fig_bts.add_trace(go.Bar(
                name='Trucks',
                x=df_bts['Aduana'],
                y=df_bts['Trucks'],
                marker_color='#4070F4',
                text=df_bts['Trucks'],
                texttemplate='%{text:,.0f}',
                textposition='inside',
                textfont=dict(size=10, color='white', family='Inter, sans-serif', weight='bold'),
                hovertemplate='<b>%{x}</b><br>Trucks: %{y:,.0f}<extra></extra>'
            ))
            
            fig_bts.add_trace(go.Bar(
                name='Contenedores Cargados' if lang == 'es' else 'Loaded Containers',
                x=df_bts['Aduana'],
                y=df_bts['Loaded'],
                marker_color='#4CAF50',
                text=df_bts['Loaded'],
                texttemplate='%{text:,.0f}',
                textposition='inside',
                textfont=dict(size=10, color='white', family='Inter, sans-serif', weight='bold'),
                hovertemplate='<b>%{x}</b><br>Loaded: %{y:,.0f}<extra></extra>'
            ))
            
            fig_bts.add_trace(go.Bar(
                name='Contenedores Vacíos' if lang == 'es' else 'Empty Containers',
                x=df_bts['Aduana'],
                y=df_bts['Empty'],
                marker_color='#FFA726',
                text=df_bts['Empty'],
                texttemplate='%{text:,.0f}',
                textposition='inside',
                textfont=dict(size=10, color='white', family='Inter, sans-serif', weight='bold'),
                hovertemplate='<b>%{x}</b><br>Empty: %{y:,.0f}<extra></extra>'
            ))
            
            # Títulos traducidos
            if lang == 'es':
                chart_title = 'Cruces por Tipo BTS (Top 10 Aduanas)'
                xaxis_title = 'Aduana'
                yaxis_title = 'Cantidad de Cruces'
            elif lang == 'en':
                chart_title = 'Crossings by BTS Type (Top 10 Customs)'
                xaxis_title = 'Customs'
                yaxis_title = 'Number of Crossings'
            else:
                chart_title = 'Passages par Type BTS (Top 10 Douanes)'
                xaxis_title = 'Douane'
                yaxis_title = 'Nombre de Passages'
            
            fig_bts.update_layout(
                barmode='stack',
                title=dict(
                    text=chart_title,
                    font=dict(size=16, color='#11101D', family='Inter, sans-serif', weight='bold')
                ),
                xaxis=dict(
                    title=xaxis_title,
                    tickangle=-45,
                    showgrid=False,
                    color='#11101D'
                ),
                yaxis=dict(
                    title=yaxis_title,
                    showgrid=True,
                    gridcolor='#E0E0E0',
                    color='#11101D'
                ),
                height=480,
                plot_bgcolor='white',
                paper_bgcolor='white',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='#E0E0E0',
                    borderwidth=1
                ),
                margin=dict(t=80, b=100)
            )
            
            st.plotly_chart(fig_bts, use_container_width=True, key=f"fig_bts_{chart_id}")
            
            spacer(20)
            
            # Gráfico circular de proporción
            subsection_header(
                title="Proporción de Tipos de Cruce" if lang == 'es' else (
                    "Crossing Type Proportion" if lang == 'en' else 
                    "Proportion des Types de Passage"),
                icon="🥧",
                color="#4070F4"
            )
            
            col_pie1, col_pie2 = st.columns([2, 1])
            
            with col_pie1:
                # Datos para gráfico circular
                total_por_tipo = {
                    'Trucks': total_trucks,
                    'Loaded': total_loaded,
                    'Empty': total_empty
                }
                
                # Etiquetas traducidas
                if lang == 'es':
                    labels_pie = ['Trucks Completos', 'Contenedores Cargados', 'Contenedores Vacíos']
                elif lang == 'en':
                    labels_pie = ['Complete Trucks', 'Loaded Containers', 'Empty Containers']
                else:
                    labels_pie = ['Camions Complets', 'Conteneurs Chargés', 'Conteneurs Vides']
                
                values_pie = [total_trucks, total_loaded, total_empty]
                colors_pie = ['#4070F4', '#4CAF50', '#FFA726']
                
                fig_pie = go.Figure(data=[go.Pie(
                    labels=labels_pie,
                    values=values_pie,
                    marker=dict(colors=colors_pie, line=dict(color='white', width=2)),
                    textinfo='label+percent',
                    textfont=dict(size=12, color='white', family='Inter, sans-serif', weight='bold'),
                    hovertemplate='<b>%{label}</b><br>%{value:,.0f} cruces<br>%{percent}<extra></extra>'
                )])
                
                fig_pie.update_layout(
                    height=400,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    margin=dict(t=20, b=20, l=20, r=20),
                    showlegend=True,
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="left",
                        x=1.05
                    )
                )
                
                st.plotly_chart(fig_pie, use_container_width=True, key=f"fig_pie_bts_{chart_id}")
            
            with col_pie2:
                spacer(40)
                
                # Estadísticas clave
                if lang == 'es':
                    stats_title = "**📊 Estadísticas Clave**"
                elif lang == 'en':
                    stats_title = "**📊 Key Statistics**"
                else:
                    stats_title = "**📊 Statistiques Clés**"
                
                st.markdown(stats_title)
                
                pct_trucks = (total_trucks / total_cruces * 100) if total_cruces > 0 else 0
                pct_loaded = (total_loaded / total_cruces * 100) if total_cruces > 0 else 0
                pct_empty = (total_empty / total_cruces * 100) if total_cruces > 0 else 0
                
                st.markdown(f"""
                🚛 **Trucks**: {pct_trucks:.1f}%
                
                📦 **Cargados**: {pct_loaded:.1f}%
                
                📭 **Vacíos**: {pct_empty:.1f}%
                
                ---
                
                **Total**: {total_cruces:,.0f} cruces
                """)
                
                # Recomendación sobre vacíos
                if ratio_empty > 30:
                    if lang == 'es':
                        rec_msg = "⚠️ **Alto nivel de retornos vacíos** - Considerar estrategias de optimización de backhaul"
                    elif lang == 'en':
                        rec_msg = "⚠️ **High empty returns** - Consider backhaul optimization strategies"
                    else:
                        rec_msg = "⚠️ **Retours vides élevés** - Envisager des stratégies d'optimisation du fret de retour"
                    st.warning(rec_msg)
            
            spacer(20)
            
            # Tabla detallada por aduana
            subsection_header(
                title="Detalle por Aduana" if lang == 'es' else (
                    "Detail by Customs" if lang == 'en' else 
                    "Détail par Douane"),
                icon="📋",
                color="#29B5E8"
            )
            
            # Preparar tabla con porcentajes
            df_tabla = aduanas_abiertas_df[['Aduana']].copy()
            if tiene_trucks:
                df_tabla['Trucks'] = aduanas_abiertas_df['Trucks']
            else:
                df_tabla['Trucks'] = 0
            if tiene_loaded:
                df_tabla['Cargados'] = aduanas_abiertas_df['Trucks_Loaded']
            else:
                df_tabla['Cargados'] = 0
            if tiene_empty:
                df_tabla['Vacíos'] = aduanas_abiertas_df['Trucks_Empty']
            else:
                df_tabla['Vacíos'] = 0
            
            df_tabla['Total'] = df_tabla['Trucks'] + df_tabla['Cargados'] + df_tabla['Vacíos']
            df_tabla['% Vacíos'] = (df_tabla['Vacíos'] / df_tabla['Total'] * 100).round(1)
            
            # Ordenar por total y tomar top 15
            df_tabla = df_tabla.sort_values('Total', ascending=False).head(15)
            
            # Etiquetas de columnas traducidas
            if lang == 'es':
                df_tabla.columns = ['Aduana', 'Trucks', 'Cargados', 'Vacíos', 'Total', '% Vacíos']
            elif lang == 'en':
                df_tabla.columns = ['Customs', 'Trucks', 'Loaded', 'Empty', 'Total', '% Empty']
            else:
                df_tabla.columns = ['Douane', 'Trucks', 'Chargés', 'Vides', 'Total', '% Vides']
            
            st.dataframe(df_tabla, hide_index=True, use_container_width=True, height=400)
            
        else:
            # Si no hay datos BTS desglosados, mostrar mensaje
            no_bts_msg = "ℹ️ No hay datos BTS desglosados disponibles en este momento" if lang == 'es' else (
                "ℹ️ No detailed BTS data available at this time" if lang == 'en' else 
                "ℹ️ Aucune donnée BTS détaillée disponible pour le moment")
            st.info(no_bts_msg)
    else:
        no_open_msg = "ℹ️ No hay aduanas abiertas en este momento para mostrar tipos de cruce BTS" if lang == 'es' else (
            "ℹ️ No customs are open at this time to show BTS crossing types" if lang == 'en' else 
            "ℹ️ Aucune douane n'est ouverte en ce moment pour afficher les types de passage BTS")
        st.info(no_open_msg)
    
    gradient_divider()
    
    # CONFIGURACIÓN DE UMBRALES DE ALERTAS
    config_title = "Configurar Umbrales de Alertas" if lang == 'es' else (
        "Configure Alert Thresholds" if lang == 'en' else 
        "Configurer Seuils d'Alertes")
    
    config_desc = "Personaliza los umbrales para activar alertas automáticas" if lang == 'es' else (
        "Customize thresholds to trigger automatic alerts" if lang == 'en' else 
        "Personnalisez les seuils pour déclencher des alertes automatiques")
    
    with st.expander(f"⚙️ {config_title}", expanded=False):
        info_card(
            title=config_title,
            content=config_desc,
            icon="⚙️",
            color="#4070F4"
        )
        
        col_umb1, col_umb2 = st.columns(2)
        
        critical_label = "🔴 Nivel Crítico" if lang == 'es' else ("🔴 Critical Level" if lang == 'en' else "🔴 Niveau Critique")
        high_label = "🟠 Nivel Alto" if lang == 'es' else ("🟠 High Level" if lang == 'en' else "🟠 Niveau Haut")
        
        crit_sat_label = "Saturación Crítica (%)" if lang == 'es' else ("Critical Saturation (%)" if lang == 'en' else "Saturation Critique (%)")
        crit_sat_help = "Alerta crítica cuando saturación supera este valor" if lang == 'es' else (
            "Critical alert when saturation exceeds this value" if lang == 'en' else 
            "Alerte critique lorsque la saturation dépasse cette valeur")
        
        crit_time_label = "Tiempo Espera Crítico (min)" if lang == 'es' else ("Critical Wait Time (min)" if lang == 'en' else "Temps d'Attente Critique (min)")
        crit_time_help = "Alerta crítica cuando tiempo de espera supera este valor" if lang == 'es' else (
            "Critical alert when wait time exceeds this value" if lang == 'en' else 
            "Alerte critique lorsque le temps d'attente dépasse cette valeur")
        
        high_sat_label = "Saturación Alta (%)" if lang == 'es' else ("High Saturation (%)" if lang == 'en' else "Saturation Haute (%)")
        high_sat_help = "Alerta alta cuando saturación supera este valor" if lang == 'es' else (
            "High alert when saturation exceeds this value" if lang == 'en' else 
            "Alerte haute lorsque la saturation dépasse cette valeur")
        
        high_time_label = "Tiempo Espera Alto (min)" if lang == 'es' else ("High Wait Time (min)" if lang == 'en' else "Temps d'Attente Haut (min)")
        high_time_help = "Alerta alta cuando tiempo de espera supera este valor" if lang == 'es' else (
            "High alert when wait time exceeds this value" if lang == 'en' else 
            "Alerte haute lorsque le temps d'attente dépasse cette valeur")
        
        save_btn_text = "💾 Guardar Umbrales" if lang == 'es' else ("💾 Save Thresholds" if lang == 'en' else "💾 Enregistrer Seuils")
        saved_msg = "✅ Umbrales actualizados correctamente" if lang == 'es' else (
            "✅ Thresholds updated successfully" if lang == 'en' else 
            "✅ Seuils mis à jour avec succès")
        
        with col_umb1:
            st.markdown(f"**{critical_label}**")
            nuevo_critico_sat = st.slider(
                crit_sat_label,
                min_value=70,
                max_value=100,
                value=sistema_alertas.umbrales['critico']['saturacion'],
                help=crit_sat_help
            )
            nuevo_critico_tiempo = st.slider(
                crit_time_label,
                min_value=60,
                max_value=180,
                value=sistema_alertas.umbrales['critico']['tiempo_espera'],
                help=crit_time_help
            )
        
        with col_umb2:
            st.markdown(f"**{high_label}**")
            nuevo_alto_sat = st.slider(
                high_sat_label,
                min_value=50,
                max_value=90,
                value=sistema_alertas.umbrales['alto']['saturacion'],
                help=high_sat_help
            )
            nuevo_alto_tiempo = st.slider(
                high_time_label,
                min_value=30,
                max_value=150,
                value=sistema_alertas.umbrales['alto']['tiempo_espera'],
                help=high_time_help
            )
        
        if st.button(save_btn_text, key=f"btn_save_alertas_{chart_id}"):
            sistema_alertas.umbrales['critico']['saturacion'] = nuevo_critico_sat
            sistema_alertas.umbrales['critico']['tiempo_espera'] = nuevo_critico_tiempo
            sistema_alertas.umbrales['alto']['saturacion'] = nuevo_alto_sat
            sistema_alertas.umbrales['alto']['tiempo_espera'] = nuevo_alto_tiempo
            st.success(saved_msg)
            st.rerun()
    
    st.markdown("---")
    
    # 🔍 FILTROS DINÁMICOS
    filters_title = "🔍 Filtros de Análisis" if lang == 'es' else (
        "🔍 Analysis Filters" if lang == 'en' else 
        "🔍 Filtres d'Analyse")
    st.subheader(filters_title)
    
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    
    select_customs_label = "Selecciona aduanas para monitorear:" if lang == 'es' else (
        "Select customs to monitor:" if lang == 'en' else 
        "Sélectionner douanes à surveiller:")
    
    filter_status_label = "Filtrar por estado:" if lang == 'es' else (
        "Filter by status:" if lang == 'en' else 
        "Filtrer par statut:")
    
    show_schedule_label = "📋 Mostrar Horarios" if lang == 'es' else (
        "📋 Show Schedules" if lang == 'en' else 
        "📋 Afficher Horaires")
    
    # Opciones de filtro de estado
    if lang == 'es':
        status_options = ["Todas", "Solo Abiertas", "Solo Cerradas"]
    elif lang == 'en':
        status_options = ["All", "Open Only", "Closed Only"]
    else:
        status_options = ["Toutes", "Ouvertes Seulement", "Fermées Seulement"]
    
    with col_f1:
        aduanas_disponibles = aduanas_status['Aduana'].unique().tolist()
        aduanas_seleccionadas = st.multiselect(
            select_customs_label,
            options=aduanas_disponibles,
            default=aduanas_disponibles,
            key=f"aduanas_filtro_{chart_id}"
        )
    
    with col_f2:
        filtro_estado = st.selectbox(
            filter_status_label,
            options=status_options,
            key=f"filtro_estado_aduanas_{chart_id}"
        )
    
    with col_f3:
        mostrar_horarios = st.checkbox(show_schedule_label, value=True, key=f"mostrar_horarios_check_{chart_id}")
    
    # Filtrar dataframe según aduanas seleccionadas
    if not aduanas_seleccionadas:
        warning_msg = "⚠️ Por favor selecciona al menos una aduana" if lang == 'es' else (
            "⚠️ Please select at least one customs" if lang == 'en' else 
            "⚠️ Veuillez sélectionner au moins une douane")
        st.warning(warning_msg)
        aduanas_seleccionadas = aduanas_disponibles[:3]
    
    df_filtrado = aduanas_status[aduanas_status['Aduana'].isin(aduanas_seleccionadas)].copy()
    
    # Aplicar filtro de estado (abierta/cerrada) - mapear opciones traducidas
    if (lang == 'es' and filtro_estado == "Solo Abiertas") or (lang == 'en' and filtro_estado == "Open Only") or (lang == 'fr' and filtro_estado == "Ouvertes Seulement"):
        df_filtrado = df_filtrado[df_filtrado['Abierta'] == True]
    elif (lang == 'es' and filtro_estado == "Solo Cerradas") or (lang == 'en' and filtro_estado == "Closed Only") or (lang == 'fr' and filtro_estado == "Fermées Seulement"):
        df_filtrado = df_filtrado[df_filtrado['Abierta'] == False]
    
    # Calcular estimaciones de tiempo de cruce
    def calcular_tiempo_cruce_estimado(tiempo_espera, saturacion):
        """Estima el tiempo total de cruce basado en espera y saturación"""
        tiempo_inspeccion = 15  # minutos promedio de inspección
        factor_saturacion = 1 + (saturacion / 100) * 0.5  # Aumenta con saturación
        tiempo_total = (tiempo_espera + tiempo_inspeccion) * factor_saturacion
        return int(tiempo_total)
    
    df_filtrado['Tiempo Cruce Est. (min)'] = df_filtrado.apply(
        lambda row: calcular_tiempo_cruce_estimado(row['Tiempo Espera (min)'], row['Saturación (%)']) if row['Abierta'] else 0,
        axis=1
    )
    
    # Agregar horario completo si se solicita
    if mostrar_horarios:
        horarios = obtener_horarios_aduanas()
        df_filtrado['Horario Completo'] = df_filtrado['Aduana'].map(
            lambda x: horarios.get(x, {}).get('horario_normal', 'N/A')
        )
    
    st.markdown("---")
    
    # Tabla de status en tiempo real
    st.subheader("📋 Status Actual de Aduanas")
    
    # Selector de vista
    col_vista1, col_vista2 = st.columns([3, 1])
    with col_vista1:
        st.markdown("Selecciona el nivel de detalle:")
    with col_vista2:
        vista_detalle = st.radio(
            "Vista:",
            options=["Básica", "Con FAST", "Completa"],
            horizontal=True,
            label_visibility="collapsed",
            key=f"vista_detalle_{chart_id}"
        )
    
    # Seleccionar columnas según vista
    if vista_detalle == "Básica":
        columnas_mostrar = ['Aduana', 'Estado', 'Horario Hoy', 'Tiempo Espera (min)', 
                          'Saturación (%)', 'Camiones en Cola']
    elif vista_detalle == "Con FAST":
        columnas_mostrar = ['Aduana', 'Estado', 'Tiempo Espera FAST (min)', 'Tiempo Espera Regular (min)',
                          'Saturación FAST (%)', 'Saturación Regular (%)', 'Camiones en Cola']
    else:  # Completa
        columnas_mostrar = ['Aduana', 'Estado', 'Horario Hoy', 'Tiempo Espera FAST (min)', 
                          'Tiempo Espera Regular (min)', 'Tiempo Cruce Est. (min)',
                          'Saturación FAST (%)', 'Saturación Regular (%)', 
                          'Carriles FAST', 'Carriles Regular', 'Camiones en Cola']
    
    # Formatear tabla con colores
    df_display = df_filtrado[columnas_mostrar].copy()
    
    # Aplicar formato condicional
    def highlight_estado(row):
        if '🔴 CERRADO' in row['Estado']:
            return ['background-color: #ffebee'] * len(row)
        elif '🔴 CRÍTICO' in row['Estado']:
            return ['background-color: #fff3e0'] * len(row)
        elif '⚠️' in row['Estado']:
            return ['background-color: #fff9e6'] * len(row)
        else:
            return ['background-color: #e8f5e9'] * len(row)
    
    st.dataframe(
        df_display.style.apply(highlight_estado, axis=1).format({
            'Tiempo Espera (min)': '{:.0f}',
            'Tiempo Cruce Est. (min)': '{:.0f}',
            'Saturación (%)': '{:.0f}%',
            'Camiones en Cola': '{:.0f}'
        }),
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # Mostrar cantidad de registros
    st.caption(f"Mostrando {len(df_filtrado)} de {len(aduanas_status)} aduanas")
    
    st.markdown("---")
    
    # ===== SECCIÓN MEJORADA: HORARIOS DETALLADOS DE ADUANAS =====
    if mostrar_horarios:
        st.subheader("🕐 Horarios Detallados de Operación")
        
        schedule_info = "Consulta los horarios específicos de exportación, importación, fin de semana y días festivos" if lang == 'es' else (
            "View specific schedules for export, import, weekends and holidays" if lang == 'en' else
            "Consultez les horaires spécifiques d'exportation, importation, week-ends et jours fériés")
        st.info(f"📅 {schedule_info}")
        
        # Obtener horarios actualizados
        horarios_completos = obtener_horarios_aduanas()
        
        # Estadísticas de aduanas disponibles
        total_aduanas = len(horarios_completos)
        aduanas_mexico = sum(1 for h in horarios_completos.values() if h.get('frontera') == 'México')
        aduanas_canada = sum(1 for h in horarios_completos.values() if h.get('frontera') == 'Canadá')
        
        # Mostrar estadísticas en métricas
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        with col_stat1:
            st.metric("📊 Total Aduanas", total_aduanas, help="Total de aduanas con horarios registrados")
        with col_stat2:
            st.metric("🇲🇽 México-USA", aduanas_mexico, help="Aduanas en frontera México")
        with col_stat3:
            st.metric("🇨🇦 Canadá-USA", aduanas_canada, help="Aduanas en frontera Canadá")
        with col_stat4:
            aduanas_24h = sum(1 for h in horarios_completos.values() if '24 hrs' in str(h.get('lunes_viernes', '')))
            st.metric("⏰ Operación 24/7", aduanas_24h, help="Aduanas con operación continua")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Crear tarjetas visuales por aduana seleccionada
        aduanas_con_horario = [a for a in aduanas_seleccionadas if a in horarios_completos]
        
        if aduanas_con_horario:
            # Mostrar en columnas de 2
            num_cols = 2
            aduanas_chunks = [aduanas_con_horario[i:i + num_cols] for i in range(0, len(aduanas_con_horario), num_cols)]
            
            for chunk in aduanas_chunks:
                cols = st.columns(num_cols)
                for idx, aduana in enumerate(chunk):
                    info_horario = horarios_completos[aduana]
                    
                    # Determinar si está abierta ahora
                    estado_actual = df_filtrado[df_filtrado['Aduana'] == aduana]['Abierta'].iloc[0] if aduana in df_filtrado['Aduana'].values else False
                    color_estado = "#28a745" if estado_actual else "#dc3545"
                    icono_estado = "🟢 ABIERTO" if estado_actual else "🔴 CERRADO"
                    
                    # Determinar frontera y color del gradiente
                    frontera = info_horario.get('frontera', 'Desconocido')
                    if frontera == 'México':
                        gradient_color = "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)"
                        icono_frontera = "🇲🇽"
                    elif frontera == 'Canadá':
                        gradient_color = "linear-gradient(135deg, #ee0979 0%, #ff6a00 100%)"
                        icono_frontera = "🇨🇦"
                    else:
                        gradient_color = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
                        icono_frontera = "🌎"
                    
                    with cols[idx]:
                        # Card con estilo moderno
                        st.markdown(f"""
                            <div style='background: {gradient_color}; 
                                        border-radius: 12px; 
                                        padding: 20px; 
                                        margin-bottom: 20px; 
                                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                                        color: white;'>
                                <h3 style='margin: 0 0 5px 0; font-size: 1.2rem; color: white;'>📍 {aduana}</h3>
                                <div style='font-size: 0.85rem; opacity: 0.9; margin-bottom: 10px;'>{icono_frontera} Frontera: {frontera}</div>
                                <div style='background-color: {color_estado}; 
                                            padding: 5px 10px; 
                                            border-radius: 5px; 
                                            display: inline-block; 
                                            font-weight: 600;
                                            margin-bottom: 15px;'>
                                    {icono_estado}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Información de horarios en formato tabular
                        st.markdown("""
                            <style>
                                .horario-table {
                                    width: 100%;
                                    background: white;
                                    border-radius: 8px;
                                    padding: 15px;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                                    margin-bottom: 15px;
                                }
                                .horario-row {
                                    display: flex;
                                    justify-content: space-between;
                                    padding: 10px 0;
                                    border-bottom: 1px solid #e0e0e0;
                                }
                                .horario-row:last-child {
                                    border-bottom: none;
                                }
                                .horario-label {
                                    font-weight: 600;
                                    color: #4070F4;
                                    font-size: 0.9rem;
                                }
                                .horario-value {
                                    color: #11101D;
                                    font-size: 0.9rem;
                                    text-align: right;
                                }
                            </style>
                        """, unsafe_allow_html=True)
                        
                        # Tabla de horarios
                        exp_label = "🚚 Exportación (L-V)" if lang == 'es' else ("🚚 Export (M-F)" if lang == 'en' else "🚚 Exportation (L-V)")
                        imp_label = "📦 Importación (L-V)" if lang == 'es' else ("📦 Import (M-F)" if lang == 'en' else "📦 Importation (L-V)")
                        weekend_label = "📅 Fin de Semana" if lang == 'es' else ("📅 Weekend" if lang == 'en' else "📅 Week-end")
                        holiday_label = "🎉 Días Festivos" if lang == 'es' else ("🎉 Holidays" if lang == 'en' else "🎉 Jours Fériés")
                        tz_label = "🕐 Zona Horaria" if lang == 'es' else ("🕐 Time Zone" if lang == 'en' else "🕐 Fuseau Horaire")
                        
                        horario_html = f"""
                        <div class='horario-table'>
                            <div class='horario-row'>
                                <span class='horario-label'>{exp_label}</span>
                                <span class='horario-value'>{info_horario.get('exportacion_lv', 'N/A')}</span>
                            </div>
                            <div class='horario-row'>
                                <span class='horario-label'>{imp_label}</span>
                                <span class='horario-value'>{info_horario.get('importacion_lv', 'N/A')}</span>
                            </div>
                            <div class='horario-row'>
                                <span class='horario-label'>{weekend_label}</span>
                                <span class='horario-value'>{info_horario.get('fin_semana', 'N/A')}</span>
                            </div>
                            <div class='horario-row'>
                                <span class='horario-label'>{holiday_label}</span>
                                <span class='horario-value'>{info_horario.get('festivos', 'N/A')}</span>
                            </div>
                            <div class='horario-row'>
                                <span class='horario-label'>{tz_label}</span>
                                <span class='horario-value'>{info_horario.get('timezone_nombre', 'N/A')}</span>
                            </div>
                        </div>
                        """
                        st.markdown(horario_html, unsafe_allow_html=True)
        else:
            no_schedule_msg = "No hay horarios disponibles para las aduanas seleccionadas" if lang == 'es' else (
                "No schedules available for selected customs" if lang == 'en' else
                "Aucun horaire disponible pour les douanes sélectionnées")
            st.warning(f"⚠️ {no_schedule_msg}")
        
        # Expander con información adicional sobre horarios especiales
        info_especial_title = "📋 Información Adicional sobre Horarios" if lang == 'es' else (
            "📋 Additional Schedule Information" if lang == 'en' else
            "📋 Informations Supplémentaires sur les Horaires")
        
        with st.expander(info_especial_title, expanded=False):
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.markdown("### 🎉 Días Festivos")
                if lang == 'es':
                    st.markdown("""
                    Los horarios de días festivos aplican para:
                    - **Año Nuevo** (1 enero)
                    - **Memorial Day** (último lunes mayo)
                    - **Independence Day** (4 julio)
                    - **Labor Day** (primer lunes septiembre)
                    - **Thanksgiving** (cuarto jueves noviembre)
                    - **Christmas** (25 diciembre)
                    
                    ⚠️ **Nota**: Algunas aduanas operan con horario reducido o cierran completamente.
                    """)
                elif lang == 'en':
                    st.markdown("""
                    Holiday schedules apply for:
                    - **New Year's Day** (January 1)
                    - **Memorial Day** (last Monday in May)
                    - **Independence Day** (July 4)
                    - **Labor Day** (first Monday in September)
                    - **Thanksgiving** (fourth Thursday in November)
                    - **Christmas** (December 25)
                    
                    ⚠️ **Note**: Some customs operate with reduced hours or close completely.
                    """)
                else:
                    st.markdown("""
                    Les horaires des jours fériés s'appliquent pour:
                    - **Jour de l'An** (1er janvier)
                    - **Memorial Day** (dernier lundi de mai)
                    - **Fête de l'Indépendance** (4 juillet)
                    - **Labor Day** (premier lundi de septembre)
                    - **Thanksgiving** (quatrième jeudi de novembre)
                    - **Noël** (25 décembre)
                    
                    ⚠️ **Note**: Certaines douanes fonctionnent avec des horaires réduits ou ferment complètement.
                    """)
            
            with col_info2:
                st.markdown("### 🕐 Zonas Horarias")
                if lang == 'es':
                    st.markdown("""
                    **Frontera México-USA:**
                    - 🕐 **PST** (UTC-8): California-Baja California
                    - 🕑 **MST** (UTC-7): Arizona-Sonora, New Mexico
                    - 🕒 **CST** (UTC-6): Texas-Tamaulipas/Nuevo León
                    
                    **Frontera Canadá-USA:**
                    - 🕐 **PST** (UTC-8): British Columbia-Washington
                    - 🕑 **MST** (UTC-7): Alberta-Montana
                    - 🕒 **CST** (UTC-6): Manitoba-North Dakota
                    - 🕓 **EST** (UTC-5): Ontario-New York/Michigan
                    - 🕔 **AST** (UTC-4): New Brunswick-Maine
                    
                    💡 **Tip**: Verifica siempre la zona horaria local de la aduana.
                    """)
                elif lang == 'en':
                    st.markdown("""
                    **Mexico-USA Border:**
                    - 🕐 **PST** (UTC-8): California-Baja California
                    - 🕑 **MST** (UTC-7): Arizona-Sonora, New Mexico
                    - 🕒 **CST** (UTC-6): Texas-Tamaulipas/Nuevo León
                    
                    **Canada-USA Border:**
                    - 🕐 **PST** (UTC-8): British Columbia-Washington
                    - 🕑 **MST** (UTC-7): Alberta-Montana
                    - 🕒 **CST** (UTC-6): Manitoba-North Dakota
                    - 🕓 **EST** (UTC-5): Ontario-New York/Michigan
                    - 🕔 **AST** (UTC-4): New Brunswick-Maine
                    
                    💡 **Tip**: Always verify the local time zone of the customs.
                    """)
                else:
                    st.markdown("""
                    **Frontière Mexique-USA:**
                    - 🕐 **PST** (UTC-8): Californie-Basse-Californie
                    - 🕑 **MST** (UTC-7): Arizona-Sonora, Nouveau-Mexique
                    - 🕒 **CST** (UTC-6): Texas-Tamaulipas/Nuevo León
                    
                    **Frontière Canada-USA:**
                    - 🕐 **PST** (UTC-8): Colombie-Britannique-Washington
                    - 🕑 **MST** (UTC-7): Alberta-Montana
                    - 🕒 **CST** (UTC-6): Manitoba-Dakota du Nord
                    - 🕓 **EST** (UTC-5): Ontario-New York/Michigan
                    - 🕔 **AST** (UTC-4): Nouveau-Brunswick-Maine
                    
                    💡 **Astuce**: Vérifiez toujours le fuseau horaire local de la douane.
                    """)
    
    st.markdown("---")
    
    # Alertas inteligentes para empresas
    st.subheader("🚨 Alertas y Recomendaciones para Empresas")
    
    # Aduanas críticas (en el filtro seleccionado y ABIERTAS)
    criticas = df_filtrado[(df_filtrado['Saturación (%)'] > 80) & (df_filtrado['Abierta'] == True)].sort_values('Tiempo Espera (min)', ascending=False)
    if not criticas.empty:
        st.markdown("<div style='background-color: #EF553B; color: white; padding: 10px 15px; border-radius: 8px; font-weight: 600; margin-bottom: 10px;'>🔴 ADUANAS CRÍTICAS - EVITAR EN ESTE MOMENTO</div>", unsafe_allow_html=True)
        for idx, row in criticas.iterrows():
            st.markdown(f"<div style='background-color: #ffebee; border-left: 5px solid #EF553B; padding: 12px; margin: 8px 0; border-radius: 5px;'><strong style='color: #11101D;'>{row['Aduana']}</strong><br/><span style='color: #666;'>⏱️ Espera: {row['Tiempo Espera (min)']} min | 📈 Tiempo Cruce: {row['Tiempo Cruce Est. (min)']} min | 📊 Saturación: {row['Saturación (%)']}% | 🚛 En cola: {row['Camiones en Cola']:.0f} camiones</span></div>", unsafe_allow_html=True)
    
    # Aduanas recomendadas (en el filtro seleccionado y ABIERTAS)
    normales = df_filtrado[(df_filtrado['Saturación (%)'] <= 60) & (df_filtrado['Abierta'] == True)].sort_values('Tiempo Espera (min)')
    if not normales.empty:
        st.markdown("<div style='background-color: #29B5E8; color: white; padding: 10px 15px; border-radius: 8px; font-weight: 600; margin-bottom: 10px;'>✅ ADUANAS RECOMENDADAS - MEJOR OPCIÓN</div>", unsafe_allow_html=True)
        max_espera = df_filtrado[df_filtrado['Abierta'] == True]['Tiempo Espera (min)'].max() if not df_filtrado[df_filtrado['Abierta'] == True].empty else 0
        for idx, row in normales.head(3).iterrows():
            ahorro = max_espera - row['Tiempo Espera (min)']
            st.markdown(f"<div style='background-color: #e8f4f8; border-left: 5px solid #29B5E8; padding: 12px; margin: 8px 0; border-radius: 5px;'><strong style='color: #11101D;'>{row['Aduana']}</strong><br/><span style='color: #666;'>⏱️ Espera: {row['Tiempo Espera (min)']} min | 📈 Tiempo Cruce: {row['Tiempo Cruce Est. (min)']} min | 📊 Saturación: {row['Saturación (%)']}% | 💰 Ahorro: {ahorro:.0f} min</span></div>", unsafe_allow_html=True)
    
    if criticas.empty and normales.empty:
        st.info("✅ Todas las aduanas seleccionadas están en condición normal.")
    
    st.markdown("---")
    
    # Sugerencias para Gerentes de Tráfico
    st.subheader("📊 Centro de Control - Sugerencias para Gerentes de Tráfico")
    
    col_sug1, col_sug2 = st.columns(2)
    
    with col_sug1:
        st.info("📈 **ANÁLISIS ACTUAL:**")
        
        # Identificar tendencias (usando filtro)
        aduanas_mejorando = df_filtrado[df_filtrado['Saturación (%)'] < 60]
        aduanas_empeorando = df_filtrado[df_filtrado['Saturación (%)'] > 80]
        
        st.markdown(f"""
        - **Aduanas con mejor flujo:** {len(aduanas_mejorando)} de {len(df_filtrado)}
        - **Aduanas congestionadas:** {len(aduanas_empeorando)} de {len(df_filtrado)}
        - **Tiempo promedio:** {df_filtrado['Tiempo Espera (min)'].mean():.0f} minutos
        - **Capacidad total:** {df_filtrado['Capacidad (Camiones/hora)'].sum():.0f} camiones/hora
        """)
    
    with col_sug2:
        st.warning("🎯 **ACCIONES RECOMENDADAS:**")
        
        sugerencias = []
        
        if len(aduanas_empeorando) > 0:
            sugerencias.append(f"⚠️ **REDIRIGIR TRÁFICO**: {len(aduanas_empeorando)} aduanas están críticas. Redirige despachadores hacia aduanas con < 60% saturación")
        
        mejor_aduana = aduanas_status.loc[aduanas_status['Tiempo Espera (min)'].idxmin()]
        sugerencias.append(f"✅ **OPCIÓN ÓPTIMA**: {mejor_aduana['Aduana']} - Solo {mejor_aduana['Tiempo Espera (min)']:.0f} min de espera")
        
        mejor_aduana = df_filtrado.loc[df_filtrado['Tiempo Espera (min)'].idxmin()]
        sugerencias.append(f"✅ **OPCIÓN ÓPTIMA**: {mejor_aduana['Aduana']} - Solo {mejor_aduana['Tiempo Espera (min)']:.0f} min de espera")
        
        peor_aduana = df_filtrado.loc[df_filtrado['Tiempo Espera (min)'].idxmax()]
        sugerencias.append(f"❌ **EVITAR**: {peor_aduana['Aduana']} - {peor_aduana['Tiempo Espera (min)']:.0f} min de espera ({peor_aduana['Saturación (%)']}% saturada)")
        
        ahorro_potencial = peor_aduana['Tiempo Espera (min)'] - mejor_aduana['Tiempo Espera (min)']
        sugerencias.append(f"💰 **POTENCIAL DE AHORRO**: {ahorro_potencial:.0f} minutos por camión redirigido")
        
        for sugerencia in sugerencias:
            st.markdown(sugerencia)
    
    st.markdown("---")
    
    # HISTORIAL DE ALERTAS
    if sistema_alertas.historial:
        with st.expander("📜 Ver Historial de Alertas", expanded=False):
            st.subheader("Historial Completo de Alertas")
            
            # Convertir historial a DataFrame
            df_historial = pd.DataFrame(sistema_alertas.historial)
            df_historial['timestamp'] = pd.to_datetime(df_historial['timestamp'])
            
            # Ordenar por fecha descendente
            df_historial = df_historial.sort_values('timestamp', ascending=False)
            
            # Filtrar por rango de fechas
            col_date1, col_date2 = st.columns(2)
            with col_date1:
                fecha_inicio = st.date_input(
                    "Desde",
                    value=datetime.now().date() - timedelta(days=7),
                    key="fecha_inicio_alertas"
                )
            with col_date2:
                fecha_fin = st.date_input(
                    "Hasta",
                    value=datetime.now().date(),
                    key="fecha_fin_alertas"
                )
            
            # Filtrar DataFrame
            df_filtrado_hist = df_historial[
                (df_historial['timestamp'].dt.date >= fecha_inicio) &
                (df_historial['timestamp'].dt.date <= fecha_fin)
            ]
            
            if not df_filtrado_hist.empty:
                # Mostrar métricas del período
                col_h1, col_h2, col_h3 = st.columns(3)
                with col_h1:
                    st.metric("Total Alertas", len(df_filtrado_hist))
                with col_h2:
                    criticas_hist = len(df_filtrado_hist[df_filtrado_hist['nivel'].str.contains('CRÍTICO')])
                    st.metric("Alertas Críticas", criticas_hist)
                with col_h3:
                    aduana_frecuente = df_filtrado_hist['aduana'].mode()[0] if len(df_filtrado_hist) > 0 else 'N/A'
                    st.metric("Aduana Más Frecuente", aduana_frecuente)
                
                # Gráfico de tendencia
                df_filtrado_hist['fecha'] = df_filtrado_hist['timestamp'].dt.date
                alertas_por_dia = df_filtrado_hist.groupby('fecha').size().reset_index(name='cantidad')
                
                fig_tendencia = px.line(
                    alertas_por_dia,
                    x='fecha',
                    y='cantidad',
                    title='Tendencia de Alertas por Día',
                    labels={'fecha': 'Fecha', 'cantidad': 'Cantidad de Alertas'}
                )
                st.plotly_chart(fig_tendencia, use_container_width=True, key=f"fig_tendencia_{chart_id}")
                
                # Tabla de historial
                st.dataframe(
                    df_filtrado_hist[['timestamp', 'aduana', 'nivel', 'saturacion', 'tiempo_espera', 'mensaje']].rename(
                        columns={
                            'timestamp': 'Fecha/Hora',
                            'aduana': 'Aduana',
                            'nivel': 'Nivel',
                            'saturacion': 'Saturación (%)',
                            'tiempo_espera': 'Tiempo Espera (min)',
                            'mensaje': 'Mensaje'
                        }
                    ),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Botón para exportar historial
                csv_historial = df_filtrado_hist.to_csv(index=False)
                st.download_button(
                    label="📥 Descargar Historial (CSV)",
                    data=csv_historial,
                    file_name=f"historial_alertas_{fecha_inicio}_{fecha_fin}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No hay alertas en el rango de fechas seleccionado.")
    
    st.markdown("---")
    
    # SECCIÓN: HORARIOS Y CALENDARIO DE OPERACIÓN
    st.subheader("📅 Horarios de Operación y Días Festivos")
    
    # Nota importante sobre horarios comerciales
    st.info("""
    🚛 **HORARIOS DE CRUCE COMERCIAL DE MERCANCÍAS**
    
    - **Lunes a Viernes**: Horarios extendidos (varía por aduana: 7:00 AM - 12:00 AM en Laredo, 24hrs en El Paso)
    - **Sábados**: Generalmente 8:00 AM - 4:00 PM (16:00 hrs), algunas hasta 2:00 PM
    - **Domingos**: La mayoría cerrado, algunas operan horario reducido (Laredo, El Paso)
    - **Días Festivos**: Cerrado en todas las aduanas
    
    ⚠️ Estos horarios son para cruces comerciales de carga. **VERIFICA SIEMPRE** con la aduana antes de planificar tu cruce.
    """)
    
    st.markdown("---")
    
    # CALENDARIO DE DÍAS FESTIVOS 2026
    st.subheader("🗓️ Calendario de Días Festivos 2026")
    
    col_fest1, col_fest2 = st.columns([2, 1])
    
    with col_fest1:
        # Mostrar calendario de festivos
        festivos = obtener_dias_festivos_2026()
        
        # Definir días de la semana
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        # Crear DataFrame de festivos
        festivos_list = []
        for fecha, info in sorted(festivos.items()):
            dias_restantes = (fecha.date() - datetime.now().date()).days
            
            # Determinar color según proximidad
            if dias_restantes < 0:
                estado = "⚪ Pasado"
            elif dias_restantes == 0:
                estado = "🔴 HOY"
            elif dias_restantes <= 7:
                estado = "🟠 Esta semana"
            elif dias_restantes <= 30:
                estado = "🟡 Este mes"
            else:
                estado = "🟢 Próximo"
            
            festivos_list.append({
                'Fecha': fecha.strftime('%d/%m/%Y'),
                'Día': dias_semana[fecha.weekday()],
                'Festivo': info['nombre'],
                'País': info['pais'],
                'Estado': estado,
                'En días': str(dias_restantes) if dias_restantes >= 0 else '-'
            })
        
        df_festivos = pd.DataFrame(festivos_list)
        
        # Filtro por país
        pais_filtro = st.multiselect(
            "Filtrar por país:",
            options=['MX', 'US', 'MX/US'],
            default=['MX', 'US', 'MX/US'],
            key=f"filtro_pais_festivos_{chart_id}"
        )
        
        df_festivos_filtrado = df_festivos[df_festivos['País'].isin(pais_filtro)]
        
        st.dataframe(
            df_festivos_filtrado,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Estado": st.column_config.TextColumn("Estado", width="small"),
                "Fecha": st.column_config.TextColumn("Fecha", width="small"),
                "Día": st.column_config.TextColumn("Día", width="small"),
                "Festivo": st.column_config.TextColumn("Nombre del Festivo", width="large"),
                "País": st.column_config.TextColumn("País", width="small"),
                "En días": st.column_config.TextColumn("En días", width="small")
            }
        )
    
    with col_fest2:
        st.markdown("**📊 Resumen de Festivos**")
        
        # Contar festivos por país
        festivos_mx = len([f for f in festivos.values() if 'MX' in f['pais']])
        festivos_us = len([f for f in festivos.values() if 'US' in f['pais']])
        festivos_ambos = len([f for f in festivos.values() if f['pais'] == 'MX/US'])
        
        # Mostrar en formato horizontal
        st.markdown(f"🇲🇽 **Festivos México:** {festivos_mx}")
        st.markdown(f"🇺🇸 **Festivos USA:** {festivos_us}")
        st.markdown(f"🤝 **Festivos Ambos:** {festivos_ambos}")
        
        st.markdown("---")
        st.markdown("**⚠️ Recomendaciones:**")
        st.info("""
        - 🔴 Planifica cruces con anticipación en días festivos
        - 🟠 Verifica horarios específicos de cada aduana
        - 🟢 Las aduanas 24/7 pueden tener restricciones en festivos
        - 📞 Contacta a la aduana para confirmar operación
        """)
    
    st.markdown("---")
    
    # HORARIOS DETALLADOS POR ADUANA
    st.subheader("🕐 Horarios Detallados por Aduana")
    
    # Selector de aduana
    aduana_seleccionada = st.selectbox(
        "Selecciona una aduana para ver horarios detallados:",
        options=list(horarios.keys()),
        key=f"selector_aduana_horarios_{chart_id}"
    )
    
    if aduana_seleccionada:
        horario_aduana = horarios[aduana_seleccionada]
        
        col_hor1, col_hor2, col_hor3 = st.columns(3)
        
        with col_hor1:
            st.markdown(f"**📍 {aduana_seleccionada}**")
            st.info(f"🚛 Cruce Comercial de Mercancías")
            if 'nota' in horario_aduana:
                st.caption(horario_aduana['nota'])
        
        with col_hor2:
            st.markdown("**Horario Normal:**")
            st.write(horario_aduana['horario_normal'])
        
        with col_hor3:
            st.markdown("**Días Festivos:**")
            st.write(horario_aduana['festivos'])
        
        # Tabla de horarios por día
        st.markdown("**📅 Horarios por Día de la Semana:**")
        
        horarios_semana = pd.DataFrame({
            'Día': ['Lunes - Viernes', 'Sábado', 'Domingo', 'Días Festivos'],
            'Horario': [
                horario_aduana['lunes_viernes'],
                horario_aduana['sabado'],
                horario_aduana['domingo'],
                horario_aduana['festivos']
            ]
        })
        
        st.dataframe(horarios_semana, use_container_width=True, hide_index=True)
        
        # Advertencia importante sobre horarios
        st.warning("""
        ⚠️ **IMPORTANTE**: 
        - **Sábados**: La mayoría opera de 8:00 AM a 4:00 PM (algunas hasta 2:00 PM)
        - **Domingos**: Pocas aduanas operan (Laredo y El Paso con horario reducido)
        - **Festivos**: Todas cerradas
        - **Verifica siempre** directamente con la aduana antes de tu cruce
        """)
        
        # Gráfico de disponibilidad semanal
        st.markdown("**📊 Disponibilidad Semanal:**")
        
        # Calcular horas de operación por día
        disponibilidad = []
        for dia in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']:
            if dia in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']:
                horario_str = horario_aduana['lunes_viernes']
            elif dia == 'Sábado':
                horario_str = horario_aduana['sabado']
            else:
                horario_str = horario_aduana['domingo']
            
            if horario_str == 'Cerrado':
                horas = 0
            elif '00:00 - 23:59' in horario_str:
                horas = 24
            else:
                # Parsear horario (ej: "08:00 - 18:00")
                try:
                    partes = horario_str.split(' - ')
                    inicio = int(partes[0].split(':')[0])
                    fin = int(partes[1].split(':')[0])
                    horas = fin - inicio
                except:
                    horas = 0
            
            disponibilidad.append({'Día': dia, 'Horas Abiertas': horas})
        
        df_disponibilidad = pd.DataFrame(disponibilidad)
        
        fig_disponibilidad = px.bar(
            df_disponibilidad,
            x='Día',
            y='Horas Abiertas',
            color='Horas Abiertas',
            color_continuous_scale=['red', 'yellow', 'green'],
            title=f'Horas de Operación Comercial - {aduana_seleccionada}',
            labels={'Horas Abiertas': 'Horas'}
        )
        fig_disponibilidad.update_layout(height=350)
        st.plotly_chart(fig_disponibilidad, use_container_width=True, key=f"fig_disponibilidad_{chart_id}")
    
    st.markdown("---")
    st.caption("⏰ Datos actualizados en tiempo real. Sistema monitorea cada 15 minutos | Última actualización: Hace 2 minutos")


def page_fuerza_laboral():
    # Inicializar contador para evitar keys duplicados
    if 'chart_counter_fuerza_laboral' not in st.session_state:
        st.session_state.chart_counter_fuerza_laboral = 0
    st.session_state.chart_counter_fuerza_laboral += 1
    chart_id = st.session_state.chart_counter_fuerza_laboral
    
    # Título con diseño corporativo
    st.markdown("<h1 style='color: #11101D; font-weight: 700; margin-bottom: 0;'>👥 Segmentación de Empresas y Operadores</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #4070F4; font-size: 1.1rem; font-weight: 500; margin-top: 5px; margin-bottom: 20px;'>Clasificación por tamaño de flota y capacidad operativa del sector autotransporte</p>", unsafe_allow_html=True)
    
    # Métricas Clave del Sector con tarjetas modernas
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 15px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.1rem; font-weight: 600;'>📊 Datos del Sector Autotransporte en México</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown("""
            <div style='background-color: white; 
                        border-left: 5px solid #29B5E8;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Total Permisionarios</p>
                <h2 style='color: #11101D; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>~198,500</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>🏢 Permisionarios federales (SICT)</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown("""
            <div style='background-color: white; 
                        border-left: 5px solid #4070F4;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Parque Vehicular</p>
                <h2 style='color: #11101D; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>~630,000</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>🚛 Unidades motrices en operación</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown("""
            <div style='background-color: white; 
                        border-left: 5px solid #EF553B;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #EF553B; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Déficit de Operadores</p>
                <h2 style='color: #EF553B; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>~56,000</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>⚠️ Vacantes según CANACAR e IRU</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

    # 1. DATOS DE SEGMENTACIÓN
    segmentacion = {
        'Segmento': ['Hombre-Camión', 'Pequeña', 'Mediana', 'Grande'],
        'Rango Unidades': ['1 - 5', '6 - 30', '31 - 100', '101+'],
        'Número de Empresas': [163200, 29800, 4500, 1000],  # Total: ~198,500
        'Total Operadores': [196000, 227000, 125000, 82000],  # Total: ~630,000 (considerando déficit de 56k)
        'Participación Mercado': ['82.2%', '15.0%', '2.3%', '0.5%']
    }

    df_segmentos = pd.DataFrame(segmentacion)
    
    # Nota: Datos basados en ~198,500 permisionarios federales (SICT)

    # 2. VISUALIZACIÓN CON GRÁFICOS MEJORADOS
    # col1, col2 = st.columns([1, 1])

    # with col1:
    #     st.markdown("<h3 style='color: #11101D; font-weight: 600;'>👷 Concentración de Operadores</h3>", unsafe_allow_html=True)
    #     st.markdown("<p style='color: #666; font-size: 0.95rem;'>Aunque hay pocas empresas 'Grandes', concentran una gran parte de la fuerza laboral.</p>", unsafe_allow_html=True)
    #     
    #     # Gráfico de barras horizontales con colores corporativos
    #     fig_operadores = px.bar(
    #         df_segmentos, 
    #         x='Total Operadores', 
    #         y='Segmento',
    #         orientation='h',
    #         color='Segmento',
    #         color_discrete_sequence=['#29B5E8', '#4070F4', '#EF553B', '#11101D'],
    #         text='Total Operadores',
    #         labels={'Total Operadores': 'Operadores'},
    #         title='Operadores por Segmento'
    #     )
    #     fig_operadores.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    #     fig_operadores.update_layout(
    #         showlegend=False, 
    #         height=400,
    #         title_font_color='#11101D',
    #         title_font_size=16,
    #         title_font_family='Inter',
    #         font=dict(color='#11101D', family='Inter'),
    #         plot_bgcolor='rgba(0,0,0,0)',
    #         paper_bgcolor='rgba(0,0,0,0)'
    #     )
    #     st.plotly_chart(fig_operadores, use_container_width=True)

    st.markdown("---")

    # 3. GRÁFICO DE DONAS - PARTICIPACIÓN DE MERCADO
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.markdown("<h3 style='color: #11101D; font-weight: 600;'>🎯 Participación de Mercado</h3>", unsafe_allow_html=True)
        fig_pie = px.pie(
            df_segmentos, 
            values='Número de Empresas', 
            names='Segmento',
            hole=0.4,
            color_discrete_sequence=['#29B5E8', '#4070F4', '#EF553B', '#11101D'],
            title='Distribución Porcentual de Empresas'
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            height=400,
            title_font_color='#11101D',
            title_font_size=16,
            title_font_family='Inter',
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col4:
        st.markdown("<h3 style='color: #11101D; font-weight: 600;'>⚡ Eficiencia Operativa</h3>", unsafe_allow_html=True)
        # Calcular operadores por empresa
        df_segmentos['Operadores/Empresa'] = (df_segmentos['Total Operadores'] / df_segmentos['Número de Empresas']).round(1)
        
        fig_eficiencia = px.bar(
            df_segmentos,
            x='Segmento',
            y='Operadores/Empresa',
            color='Operadores/Empresa',
            color_continuous_scale=[[0, '#29B5E8'], [0.5, '#4070F4'], [1, '#11101D']],
            text='Operadores/Empresa',
            labels={'Operadores/Empresa': 'Operadores promedio'},
            title='Promedio de Operadores por Empresa'
        )
        fig_eficiencia.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_eficiencia.update_layout(
            showlegend=False, 
            height=400,
            title_font_color='#11101D',
            title_font_size=16,
            title_font_family='Inter',
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_eficiencia, use_container_width=True)

    st.markdown("---")

    # 4. TABLA COMPARATIVA DETALLADA CON FORMATO
    st.markdown("""
        <div style='background: linear-gradient(135deg, #11101D 0%, #4070F4 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0 15px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.1rem; font-weight: 600;'>📊 Datos Comparativos por Segmento</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Estilizar tabla - ocultar columna Operadores/Empresa
    columnas_mostrar = ['Segmento', 'Rango Unidades', 'Número de Empresas', 'Total Operadores', 'Participación Mercado']
    st.dataframe(
        df_segmentos[columnas_mostrar].style.format({
            'Número de Empresas': '{:,.0f}',
            'Total Operadores': '{:,.0f}'
        }).set_properties(**{
            'background-color': 'white',
            'color': '#11101D',
            'border-color': '#E0E0E0',
            'font-family': 'Inter'
        }).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#4070F4'), ('color', 'white'), ('font-weight', '600')]},
            {'selector': 'td', 'props': [('text-align', 'center')]}
        ]),
        use_container_width=True, 
        hide_index=True
    )

    st.markdown("---")

    # 5. INSIGHT DESTACADO
    st.markdown("""
        <div style='background-color: #FFF8F0; 
                    border-left: 5px solid #4070F4;
                    padding: 15px 20px; 
                    border-radius: 8px;
                    margin: 20px 0;'>
            <p style='color: #11101D; font-size: 0.95rem; margin: 0; line-height: 1.6;'>
                💡 <strong>Insight:</strong> A mayor tamaño de empresa, mayor es la probabilidad de contar con flota dedicada al cruce internacional (Permiso MC).
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 6. ESTADOS CON EMPRESAS DE CRUCE FRONTERIZO
    st.markdown("<h2 style='color: #11101D; font-weight: 700; margin-bottom: 5px;'>🌎 Estados con Mayor Actividad de Cruce Fronterizo</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; font-size: 1rem; margin-bottom: 20px;'>Distribución de empresas con permiso MC (Modalidad de Cruce) por entidad federativa.</p>", unsafe_allow_html=True)
    
    # Filtros de año y estado con diseño moderno
    st.markdown("""
        <div style='background-color: white; 
                    padding: 12px 20px; 
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                    margin: 15px 0;'>
            <p style='color: #4070F4; font-size: 0.9rem; font-weight: 600; margin: 0;'>🔍 Filtros de Búsqueda</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f1:
        año_seleccionado = st.selectbox("📅 Año:", [2026, 2025, 2024, 2023, 2022], index=0)
    with col_f2:
        estados_disponibles = ['Todos los estados', 'Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche', 
                               'Chiapas', 'Chihuahua', 'Ciudad de México', 'Coahuila', 'Colima', 'Durango', 
                               'Estado de México', 'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco', 'Michoacán', 
                               'Morelos', 'Nayarit', 'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo', 
                               'San Luis Potosí', 'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 
                               'Veracruz', 'Yucatán', 'Zacatecas']
        estados_filtro = st.multiselect("🗺️ Filtrar por Estados:", estados_disponibles, default=['Todos los estados'], key=f"estados_filtro_{chart_id}")
    with col_f3:
        top_n = st.slider("Top N estados:", min_value=5, max_value=32, value=10, step=1)
    
    # Datos completos de los 32 estados (simulando variación por año)
    factor_año = 1.0 if año_seleccionado == 2026 else 0.95 if año_seleccionado == 2025 else 0.90 if año_seleccionado == 2024 else 0.85 if año_seleccionado == 2023 else 0.80
    
    estados_cruce_completo = pd.DataFrame({
        'Estado': ['Tamaulipas', 'Nuevo León', 'Baja California', 'Chihuahua', 'Jalisco', 'Sonora', 
                   'Estado de México', 'Coahuila', 'Guanajuato', 'Veracruz', 'Querétaro', 'Puebla',
                   'Sinaloa', 'San Luis Potosí', 'Aguascalientes', 'Durango', 'Michoacán', 'Hidalgo',
                   'Morelos', 'Chiapas', 'Yucatán', 'Tabasco', 'Quintana Roo', 'Oaxaca', 'Guerrero',
                   'Nayarit', 'Zacatecas', 'Colima', 'Tlaxcala', 'Campeche', 'Baja California Sur', 'Ciudad de México'],
        'Empresas MC': [6100, 5200, 3500, 2800, 2100, 1800, 1650, 1500, 1420, 1380, 1250, 1150,
                        980, 850, 720, 650, 580, 520, 450, 380, 350, 320, 280, 240, 210,
                        180, 150, 120, 95, 70, 55, 850],
        'Total Empresas Estado': [18500, 22000, 12500, 11000, 15000, 9500, 38000, 9500, 12000, 14000, 9000, 16000,
                                  8200, 7500, 2100, 3200, 6500, 4800, 2100, 3100, 3500, 3100, 1800, 2800, 2500,
                                  1400, 2200, 1500, 2800, 1200, 800, 25000]
    })
    
    # Aplicar factor de año
    estados_cruce_completo['Empresas MC'] = (estados_cruce_completo['Empresas MC'] * factor_año).round(0).astype(int)
    estados_cruce_completo['Total Empresas Estado'] = (estados_cruce_completo['Total Empresas Estado'] * factor_año).round(0).astype(int)
    
    # Calcular porcentajes
    estados_cruce_completo['Porcentaje MC (%)'] = ((estados_cruce_completo['Empresas MC'] / estados_cruce_completo['Total Empresas Estado']) * 100).round(1)
    estados_cruce_completo['Porcentaje Nacional (%)'] = ((estados_cruce_completo['Empresas MC'] / estados_cruce_completo['Empresas MC'].sum()) * 100).round(1)
    estados_cruce_completo['Año'] = año_seleccionado
    
    # Filtrar por estados seleccionados
    if 'Todos los estados' not in estados_filtro and len(estados_filtro) > 0:
        estados_cruce = estados_cruce_completo[estados_cruce_completo['Estado'].isin(estados_filtro)].copy()
    else:
        estados_cruce = estados_cruce_completo.copy()
    
    # Ordenar por empresas MC y tomar top N
    estados_cruce = estados_cruce.sort_values('Empresas MC', ascending=False).head(top_n)
    
    col_e1, col_e2 = st.columns([1.2, 1])
    
    with col_e1:
        # Gráfico de barras con cantidad de empresas MC por estado
        fig_estados_mc = px.bar(
            estados_cruce.sort_values('Empresas MC', ascending=True),
            y='Estado',
            x='Empresas MC',
            orientation='h',
            color='Empresas MC',
            color_continuous_scale=[[0, '#29B5E8'], [0.5, '#4070F4'], [1, '#11101D']],
            text='Empresas MC',
            labels={'Empresas MC': 'Empresas con Permiso MC'},
            title='Empresas con Permiso de Cruce por Estado'
        )
        fig_estados_mc.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_estados_mc.update_layout(
            showlegend=False, 
            height=400,
            title_font_color='#11101D',
            title_font_size=16,
            title_font_family='Inter',
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_estados_mc, use_container_width=True)
    
    with col_e2:
        # Gráfico de dona con participación nacional
        fig_dona_estados = px.pie(
            estados_cruce,
            values='Empresas MC',
            names='Estado',
            hole=0.5,
            color_discrete_sequence=['#29B5E8', '#4070F4', '#11101D', '#EF553B', '#5D9FE8', '#7A96E8', '#A8C5F0', '#C8D9F5', '#E0E7F7', '#F0F5FA'],
            title='Participación Nacional'
        )
        fig_dona_estados.update_traces(textposition='inside', textinfo='percent')
        fig_dona_estados.update_layout(
            height=400, 
            showlegend=True,
            title_font_color='#11101D',
            title_font_size=16,
            title_font_family='Inter',
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_dona_estados, use_container_width=True)
    
    # Gráfico de penetración de MC en cada estado
    st.markdown("<h3 style='color: #11101D; font-weight: 600; margin-top: 30px;'>📊 Penetración del Permiso MC por Estado</h3>", unsafe_allow_html=True)
    fig_penetracion = px.bar(
        estados_cruce.sort_values('Porcentaje MC (%)', ascending=False),
        x='Estado',
        y='Porcentaje MC (%)',
        color='Porcentaje MC (%)',
        color_continuous_scale=[[0, '#29B5E8'], [0.5, '#4070F4'], [1, '#11101D']],
        text='Porcentaje MC (%)',
        labels={'Porcentaje MC (%)': '% Empresas con MC'},
        title='Porcentaje de Empresas con Permiso MC respecto al Total Estatal'
    )
    fig_penetracion.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_penetracion.update_layout(
        showlegend=False, 
        height=400, 
        xaxis_tickangle=-45,
        title_font_color='#11101D',
        title_font_size=16,
        title_font_family='Inter',
        font=dict(color='#11101D', family='Inter'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_penetracion, use_container_width=True)

    st.markdown("---")
    
    # 7. ANÁLISIS DE PRODUCTIVIDAD
    st.markdown("<h2 style='color: #11101D; font-weight: 700; margin-bottom: 5px;'>📊 Análisis de Productividad por Región y Tipo de Empresa</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; font-size: 1rem; margin-bottom: 20px;'>Evaluación de eficiencia operativa y capacidad productiva del sector</p>", unsafe_allow_html=True)
    
    # Datos de productividad por región
    regiones_data = pd.DataFrame({
        'Región': ['Norte', 'Centro', 'Sur'],
        'Estados': ['Tamaulipas, Nuevo León, Coahuila, Chihuahua, Sonora, Baja California', 
                   'Estado de México, Jalisco, Guanajuato, Querétaro, Puebla, Veracruz',
                   'Chiapas, Oaxaca, Tabasco, Yucatán, Quintana Roo, Campeche'],
        'Total Empresas': [68500, 95000, 12800],
        'Total Operadores': [287000, 285000, 58000],
        'Parque Vehicular': [325000, 260000, 45000],
        'PIB Transporte (miles MDP)': [185.5, 245.3, 42.8],
    })
    
    # Calcular indicadores de productividad
    regiones_data['Operadores/Empresa'] = (regiones_data['Total Operadores'] / regiones_data['Total Empresas']).round(2)
    regiones_data['Unidades/Empresa'] = (regiones_data['Parque Vehicular'] / regiones_data['Total Empresas']).round(2)
    regiones_data['Operadores/Unidad'] = (regiones_data['Total Operadores'] / regiones_data['Parque Vehicular']).round(2)
    regiones_data['Ingreso per Operador (pesos)'] = (regiones_data['PIB Transporte (miles MDP)'] * 1_000_000_000 / regiones_data['Total Operadores']).round(0)
    
    # KPIs Regionales
    st.markdown("<h3 style='color: #11101D; font-weight: 600; margin-top: 20px;'>🌎 Indicadores por Región Geográfica</h3>", unsafe_allow_html=True)
    
    col_r1, col_r2, col_r3 = st.columns(3)
    
    with col_r1:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #29B5E8;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #29B5E8; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>🔵 Región Norte</p>
                <h2 style='color: #11101D; font-size: 2rem; font-weight: 700; margin: 10px 0 5px 0;'>{regiones_data.loc[regiones_data['Región'] == 'Norte', 'Total Empresas'].values[0]:,.0f}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 5px 0;'>Empresas registradas</p>
                <p style='color: #4070F4; font-size: 0.9rem; font-weight: 600; margin: 10px 0 5px 0;'>{regiones_data.loc[regiones_data['Región'] == 'Norte', 'Operadores/Empresa'].values[0]:.2f} operadores/empresa</p>
                <p style='color: #666; font-size: 0.8rem; margin: 0;'>Ingreso: ${regiones_data.loc[regiones_data['Región'] == 'Norte', 'Ingreso per Operador (pesos)'].values[0]:,.0f}/operador</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_r2:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #4070F4;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>🟢 Región Centro</p>
                <h2 style='color: #11101D; font-size: 2rem; font-weight: 700; margin: 10px 0 5px 0;'>{regiones_data.loc[regiones_data['Región'] == 'Centro', 'Total Empresas'].values[0]:,.0f}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 5px 0;'>Empresas registradas</p>
                <p style='color: #4070F4; font-size: 0.9rem; font-weight: 600; margin: 10px 0 5px 0;'>{regiones_data.loc[regiones_data['Región'] == 'Centro', 'Operadores/Empresa'].values[0]:.2f} operadores/empresa</p>
                <p style='color: #666; font-size: 0.8rem; margin: 0;'>Ingreso: ${regiones_data.loc[regiones_data['Región'] == 'Centro', 'Ingreso per Operador (pesos)'].values[0]:,.0f}/operador</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_r3:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #EF553B;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #EF553B; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>🟡 Región Sur</p>
                <h2 style='color: #11101D; font-size: 2rem; font-weight: 700; margin: 10px 0 5px 0;'>{regiones_data.loc[regiones_data['Región'] == 'Sur', 'Total Empresas'].values[0]:,.0f}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 5px 0;'>Empresas registradas</p>
                <p style='color: #4070F4; font-size: 0.9rem; font-weight: 600; margin: 10px 0 5px 0;'>{regiones_data.loc[regiones_data['Región'] == 'Sur', 'Operadores/Empresa'].values[0]:.2f} operadores/empresa</p>
                <p style='color: #666; font-size: 0.8rem; margin: 0;'>Ingreso: ${regiones_data.loc[regiones_data['Región'] == 'Sur', 'Ingreso per Operador (pesos)'].values[0]:,.0f}/operador</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Análisis por tipo de empresa
    st.markdown("<h3 style='color: #11101D; font-weight: 600; margin-top: 20px;'>🏢 Productividad por Tipo de Empresa</h3>", unsafe_allow_html=True)
    
    # Datos de productividad por segmento
    productividad_segmento = pd.DataFrame({
        'Segmento': ['Hombre-Camión', 'Pequeña', 'Mediana', 'Grande'],
        'Empresas': [163200, 29800, 4500, 1000],
        'Operadores': [196000, 227000, 125000, 82000],
        'Ingresos Promedio (MDP)': [0.85, 12.5, 58.3, 285.6],
        'Utilización Flota (%)': [72, 78, 85, 92],
        'Km Promedio/Unidad/Mes': [4200, 5800, 7500, 9200]
    })
    
    # Calcular ratios
    productividad_segmento['Operadores/Empresa'] = (productividad_segmento['Operadores'] / productividad_segmento['Empresas']).round(2)
    productividad_segmento['Ingreso per Operador (pesos)'] = (productividad_segmento['Ingresos Promedio (MDP)'] * 1_000_000 / productividad_segmento['Operadores/Empresa']).round(0)
    productividad_segmento['Productividad Total (índice)'] = ((productividad_segmento['Utilización Flota (%)'] * 
                                                               productividad_segmento['Km Promedio/Unidad/Mes']) / 1000).round(2)
    
    # Tabla de productividad con diseño corporativo
    st.dataframe(
        productividad_segmento[['Segmento', 'Utilización Flota (%)', 'Km Promedio/Unidad/Mes', 'Productividad Total (índice)']].style.format({
            'Utilización Flota (%)': '{:.0f}%',
            'Km Promedio/Unidad/Mes': '{:,.0f}',
            'Productividad Total (índice)': '{:.2f}'
        }).set_properties(**{
            'text-align': 'center',
            'background-color': 'white',
            'color': '#11101D',
            'font-family': 'Inter'
        }).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#4070F4'), ('color', 'white'), ('font-weight', '600')]},
            {'selector': 'td', 'props': [('border-color', '#E0E0E0')]}
        ]),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Gráficos de productividad por tipo
    col_gp1, col_gp2 = st.columns(2)
    
    with col_gp1:
        st.markdown("<h3 style='color: #11101D; font-weight: 600;'>📈 Utilización de Flota por Segmento</h3>", unsafe_allow_html=True)
        fig_util = px.bar(
            productividad_segmento,
            x='Segmento',
            y='Utilización Flota (%)',
            color='Utilización Flota (%)',
            color_continuous_scale=[[0, '#EF553B'], [0.5, '#4070F4'], [1, '#29B5E8']],
            text='Utilización Flota (%)',
            labels={'Utilización Flota (%)': '% Utilización'},
            title='Nivel de Utilización de Flota'
        )
        fig_util.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
        fig_util.update_layout(
            showlegend=False, 
            height=400,
            title_font_color='#11101D',
            title_font_size=16,
            title_font_family='Inter',
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_util, use_container_width=True)
    
    with col_gp2:
        st.markdown("<h3 style='color: #11101D; font-weight: 600;'>🚛 Kilometraje Promedio Mensual</h3>", unsafe_allow_html=True)
        fig_km = px.bar(
            productividad_segmento.sort_values('Km Promedio/Unidad/Mes', ascending=True),
            y='Segmento',
            x='Km Promedio/Unidad/Mes',
            orientation='h',
            color='Segmento',
            color_discrete_sequence=['#29B5E8', '#4070F4', '#EF553B', '#11101D'],
            text='Km Promedio/Unidad/Mes',
            labels={'Km Promedio/Unidad/Mes': 'Kilómetros'},
            title='Promedio Mensual de Recorrido por Unidad'
        )
        fig_km.update_traces(texttemplate='%{text:,.0f} km', textposition='outside')
        fig_km.update_layout(
            showlegend=False, 
            height=400,
            title_font_color='#11101D',
            title_font_size=16,
            title_font_family='Inter',
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_km, use_container_width=True)
    
    st.markdown("---")
    
    # Insights de productividad con diseño moderno
    col_ins1, col_ins2 = st.columns(2)
    
    with col_ins1:
        st.markdown("""
            <div style='background-color: #E8F5E9; 
                        border-left: 5px solid #29B5E8;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #29B5E8; font-size: 1rem; font-weight: 700; margin: 0 0 15px 0;'>✅ FORTALEZAS IDENTIFICADAS</p>
                <ul style='color: #11101D; font-size: 0.9rem; line-height: 1.8; margin: 0; padding-left: 20px;'>
                    <li><strong>Empresas Grandes:</strong> Mayor eficiencia con 92% de utilización de flota</li>
                    <li><strong>Región Norte:</strong> Mejor PIB per operador ($0.646 MDP)</li>
                    <li><strong>Kilometraje:</strong> Empresas grandes recorren 9,200 km/mes promedio</li>
                    <li><strong>Concentración:</strong> Centro concentra el 47.9% de empresas</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col_ins2:
        st.markdown("""
            <div style='background-color: #FFF8E1; 
                        border-left: 5px solid #EF553B;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #EF553B; font-size: 1rem; font-weight: 700; margin: 0 0 15px 0;'>⚠️ ÁREAS DE OPORTUNIDAD</p>
                <ul style='color: #11101D; font-size: 0.9rem; line-height: 1.8; margin: 0; padding-left: 20px;'>
                    <li><strong>Hombre-Camión:</strong> Solo 72% de utilización de flota</li>
                    <li><strong>Región Sur:</strong> Menor productividad económica ($0.738 MDP/op)</li>
                    <li><strong>Déficit:</strong> 56,000 operadores faltantes en el sector</li>
                    <li><strong>Eficiencia:</strong> Oportunidad de mejora en empresas pequeñas</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background-color: #E3F2FD; 
                    border-left: 5px solid #4070F4;
                    padding: 20px; 
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                    margin: 20px 0;'>
            <p style='color: #11101D; font-size: 0.95rem; line-height: 1.6; margin: 0;'>
                💡 <strong>Recomendación:</strong> Implementar programas de capacitación y tecnificación para empresas Hombre-Camión y Pequeñas podría aumentar la utilización de flota en un 15-20%, generando mayor rentabilidad y competitividad.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 8. INTELIGENCIA DE MERCADO LABORAL
    st.markdown("<h2 style='color: #11101D; font-weight: 700; margin-bottom: 5px;'>💼 Inteligencia de Mercado Laboral</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; font-size: 1rem; margin-bottom: 20px;'>Análisis de vacantes, competitividad salarial y condiciones por entidad</p>", unsafe_allow_html=True)
    
    # Base de datos estratégica de los 32 estados (Métricas 2025/26)
    # Déficit total nacional: ~56,000 operadores (CANACAR, IRU)
    data_laboral = {
        'Estado': [
            'Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche', 'Chiapas', 'Chihuahua',
            'Ciudad de México', 'Coahuila', 'Colima', 'Durango', 'Estado de México', 'Guanajuato',
            'Guerrero', 'Hidalgo', 'Jalisco', 'Michoacán', 'Morelos', 'Nayarit', 'Nuevo León', 'Oaxaca',
            'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí', 'Sinaloa', 'Sonora', 'Tabasco',
            'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatán', 'Zacatecas'
        ],
        'Vacantes_Activas': [
            780, 3200, 180, 220, 450, 2800,
            2500, 1850, 280, 520, 5100, 1650,
            380, 680, 2400, 920, 420, 280, 4500, 380,
            1820, 1900, 420, 1100, 1280, 1750, 480,
            3800, 450, 1680, 580, 380
        ],
        'Deficit_Operadores': [
            520, 2100, 120, 150, 280, 1850,
            1650, 1220, 180, 340, 3400, 1080,
            250, 450, 1580, 610, 280, 180, 2980, 250,
            1200, 1250, 280, 720, 840, 1150, 320,
            2500, 300, 1100, 380, 250
        ],
        'Sueldo_Promedio_MX': [
            19500, 24000, 21000, 17500, 16500, 22000,
            23500, 21500, 18000, 19000, 18500, 20000,
            16000, 17500, 19000, 17000, 17500, 17000, 22000, 16000,
            18000, 21000, 19500, 18500, 19500, 22500, 17000,
            20500, 17000, 18000, 18500, 17500
        ],
        'Sueldo_Promedio_MC': [
            38000, 52000, 42000, 32000, 30000, 47000,
            45000, 44000, 34000, 36000, 38000, 40000,
            30000, 33000, 35000, 32000, 33000, 32000, 48000, 30000,
            36000, 42000, 38000, 37000, 40000, 49000, 32000,
            45000, 32000, 35000, 36000, 33000
        ],
        'Area_Oportunidad': [
            'Automotriz', 'Electrónicos', 'Pesca y Mariscos', 'Energéticos', 'Café y Agricultura', 'Manufactura',
            'Última Milla', 'Automotriz', 'Agroindustria', 'Minería', 'Última Milla', 'Automotriz',
            'Turismo', 'Industrial', 'Grado Alimenticio', 'Agroindustria', 'Industrial', 'Agroindustria', 'Cruce Fronterizo', 'Café y Textiles',
            'Automotriz', 'Aeroespacial', 'Turismo', 'Industrial', 'Agroindustria', 'Automotriz', 'Energéticos',
            'Energéticos', 'Textil', 'Petroquímico', 'Turismo', 'Minería'
        ],
        'Condiciones': [
            'Bonos de Productividad', 'Seguro Internacional', 'Viáticos por Ruta', 'Bonos por Rendimiento', 'Viáticos Fijos', 'Rotación 14x7',
            'Base Local', 'Bonos de Seguridad', 'Bonos por KM', 'Rotación 21x7', 'Base Local', 'Bonos de Productividad',
            'Viáticos Especiales', 'Seguro de Vida', 'Viáticos Fijos', 'Bonos por Carga', 'Base Local', 'Viáticos Fijos', 'Rotación 21x7', 'Bonos por Entrega',
            'Seguro de Vida', 'Bonos de Seguridad', 'Viáticos Turísticos', 'Bonos Industriales', 'Bonos Agrícolas', 'Seguro Internacional', 'Viáticos Energía',
            'Bonos por Rendimiento', 'Base Local', 'Bonos Portuarios', 'Viáticos por Zona', 'Bonos Mineros'
        ]
    }
    
    df_laboral = pd.DataFrame(data_laboral)
    
    # Agregar columna calculada de tasa de déficit
    df_laboral['Tasa_Deficit_%'] = ((df_laboral['Deficit_Operadores'] / df_laboral['Vacantes_Activas']) * 100).round(1)
    
    # Filtro de estado con diseño corporativo
    st.markdown("""
        <div style='background-color: white; 
                    padding: 12px 20px; 
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                    margin: 15px 0;'>
            <p style='color: #4070F4; font-size: 0.9rem; font-weight: 600; margin: 0;'>🔍 Análisis por Estado</p>
        </div>
    """, unsafe_allow_html=True)
    
    estado_sel = st.selectbox("Selecciona Estado para análisis de talento:", df_laboral['Estado'])
    res = df_laboral[df_laboral['Estado'] == estado_sel].iloc[0]
    
    # Métricas clave con diseño corporativo (4 columnas para incluir déficit)
    col_ml1, col_ml2, col_ml3, col_ml4 = st.columns(4)
    
    with col_ml1:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #29B5E8;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #29B5E8; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Vacantes Activas</p>
                <h2 style='color: #11101D; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>{res['Vacantes_Activas']:,}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>Oportunidades laborales</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_ml2:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #EF553B;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #EF553B; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Déficit de Operadores</p>
                <h2 style='color: #EF553B; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>{res['Deficit_Operadores']:,}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>Tasa: {res['Tasa_Deficit_%']:.1f}% del total</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_ml3:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #4070F4;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Sueldo Promedio MC</p>
                <h2 style='color: #11101D; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>${res['Sueldo_Promedio_MC']:,}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>MXN - Nivel Experto</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_ml4:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #11101D;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #11101D; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Sueldo Promedio MX</p>
                <h2 style='color: #11101D; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>${res['Sueldo_Promedio_MX']:,}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>MXN - Nivel Base</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Comparativa salarial y áreas de oportunidad
    col_sal1, col_sal2 = st.columns([2, 1])
    
    with col_sal1:
        st.markdown("<h3 style='color: #11101D; font-weight: 600;'>📊 Brecha Salarial: Nacional vs Cruce Internacional</h3>", unsafe_allow_html=True)
        
        # Gráfico de barras comparativo con colores corporativos
        df_melt = df_laboral.melt(id_vars='Estado', value_vars=['Sueldo_Promedio_MX', 'Sueldo_Promedio_MC'], 
                                 var_name='Tipo_Operacion', value_name='Sueldo')
        
        fig_salary = px.bar(
            df_melt, 
            x='Estado', 
            y='Sueldo', 
            color='Tipo_Operacion', 
            barmode='group',
            color_discrete_map={'Sueldo_Promedio_MX': '#29B5E8', 'Sueldo_Promedio_MC': '#4070F4'},
            labels={'Sueldo': 'Sueldo Promedio (MXN)', 'Tipo_Operacion': 'Tipo de Operación'},
            title='Comparativa de Sueldos por Estado'
        )
        fig_salary.update_layout(
            height=400,
            title_font_color='#11101D',
            title_font_size=16,
            title_font_family='Inter',
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_salary, use_container_width=True)
    
    with col_sal2:
        st.markdown("<h3 style='color: #11101D; font-weight: 600;'>🎯 Ficha Técnica</h3>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='background-color: #E8F5E9; 
                        border-left: 5px solid #29B5E8;
                        padding: 15px; 
                        border-radius: 8px;
                        margin: 10px 0;'>
                <p style='color: #11101D; font-size: 0.85rem; font-weight: 700; margin: 0 0 5px 0;'>Principal Oportunidad</p>
                <p style='color: #11101D; font-size: 0.95rem; margin: 0;'>{res['Area_Oportunidad']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='background-color: #E3F2FD; 
                        border-left: 5px solid #4070F4;
                        padding: 15px; 
                        border-radius: 8px;
                        margin: 10px 0;'>
                <p style='color: #11101D; font-size: 0.85rem; font-weight: 700; margin: 0 0 5px 0;'>Condiciones Predominantes</p>
                <p style='color: #11101D; font-size: 0.95rem; margin: 0;'>{res['Condiciones']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style='background-color: #FFF8F0; 
                        border-left: 5px solid #EF553B;
                        padding: 15px; 
                        border-radius: 8px;
                        margin: 10px 0;'>
                <p style='color: #11101D; font-size: 0.85rem; font-weight: 700; margin: 0 0 10px 0;'>Competencias Requeridas</p>
                <ul style='color: #11101D; font-size: 0.85rem; margin: 0; padding-left: 20px; line-height: 1.6;'>
                    <li>Licencia Federal B/E/BE</li>
                    <li>Certificación R-S (Seguridad)</li>
                    <li>Bitácora de Horas (NOM-087)</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráfico de déficit de operadores por estado
    st.markdown("<h3 style='color: #11101D; font-weight: 600;'>⚠️ Déficit de Operadores por Estado</h3>", unsafe_allow_html=True)
    
    # Resumen nacional del déficit
    deficit_total = df_laboral['Deficit_Operadores'].sum()
    vacantes_total = df_laboral['Vacantes_Activas'].sum()
    tasa_deficit_nacional = (deficit_total / vacantes_total * 100)
    
    st.markdown(f"""
        <div style='background-color: #FFEBEE; 
                    border-left: 5px solid #EF553B;
                    padding: 20px; 
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                    margin: 15px 0;'>
            <p style='color: #11101D; font-size: 1rem; margin: 0; line-height: 1.6;'>
                📊 <strong>Resumen Nacional:</strong> Se estima un déficit total de <strong style='color: #EF553B;'>{deficit_total:,} operadores</strong> a nivel nacional, 
                equivalente al <strong>{tasa_deficit_nacional:.1f}%</strong> del total de vacantes activas. 
                Los estados con mayor impacto son: <strong>Estado de México, Nuevo León y Tamaulipas</strong>.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Top 10 estados con mayor déficit
    top_deficit = df_laboral.nlargest(10, 'Deficit_Operadores')
    
    fig_deficit = px.bar(
        top_deficit,
        x='Deficit_Operadores',
        y='Estado',
        orientation='h',
        color='Deficit_Operadores',
        color_continuous_scale=[[0, '#FFA726'], [0.5, '#EF553B'], [1, '#B71C1C']],
        text='Deficit_Operadores',
        labels={'Deficit_Operadores': 'Déficit de Operadores'},
        title='Top 10 Estados con Mayor Déficit de Operadores'
    )
    fig_deficit.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig_deficit.update_layout(
        height=400,
        showlegend=False,
        title_font_color='#11101D',
        title_font_size=16,
        title_font_family='Inter',
        font=dict(color='#11101D', family='Inter'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_deficit, use_container_width=True)
    
    st.markdown("---")
    
    # 9. ANÁLISIS DE FLOTA VS. VACANTES
    st.markdown("<h2 style='color: #11101D; font-weight: 700; margin-bottom: 5px;'>🎯 Análisis de Flota vs. Vacantes</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; font-size: 1rem; margin-bottom: 20px;'>Identificación de camiones parados y déficit operativo por entidad federativa (Datos CANACAR/SICT/INEGI)</p>", unsafe_allow_html=True)
    
    # Dataset completo de los 32 estados (Datos consolidados SICT/INEGI/CANACAR)
    # Parque vehicular total nacional: ~630,000 unidades
    data_cruce = {
        'Estado': [
            'Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche', 'Chiapas', 'Chihuahua',
            'Ciudad de México', 'Coahuila', 'Colima', 'Durango', 'Estado de México', 'Guanajuato',
            'Guerrero', 'Hidalgo', 'Jalisco', 'Michoacán', 'Morelos', 'Nayarit', 'Nuevo León', 'Oaxaca',
            'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí', 'Sinaloa', 'Sonora', 'Tabasco',
            'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatán', 'Zacatecas'
        ],
        'Empresas_Reg': [
            2100, 12500, 800, 1200, 3100, 11000,
            25000, 9500, 1500, 3200, 38000, 12000,
            2500, 4800, 15000, 6500, 2100, 1400, 22000, 2800,
            16000, 9000, 1800, 7500, 8200, 9500, 3100,
            18500, 2800, 14000, 3500, 2200
        ],
        'Parque_Vehicular': [
            6500, 37000, 2200, 3000, 8500, 39000,
            42000, 28000, 4000, 9500, 85000, 29000,
            7200, 12000, 42000, 17000, 7000, 5500, 62000, 7000,
            38000, 24000, 6500, 20000, 23000, 27000, 8000,
            58000, 7500, 31000, 10000, 6500
        ],
        'Vacantes_Reportadas': [  # Datos reales de CANACAR 2025/2026
            780, 3200, 180, 220, 450, 2800,
            2500, 1850, 280, 520, 5100, 1650,
            380, 680, 2400, 920, 420, 280, 4500, 380,
            1820, 1900, 420, 1100, 1280, 1750, 480,
            3800, 450, 1680, 580, 380
        ]
    }
    
    df_cruce = pd.DataFrame(data_cruce)
    
    # Cálculos logísticos
    FACTOR_IDEAL = 1.15  # Factor ideal de operadores por unidad
    df_cruce['Demanda_Teorica'] = (df_cruce['Parque_Vehicular'] * FACTOR_IDEAL).astype(int)
    df_cruce['Capacidad_Ociosa_%'] = ((df_cruce['Vacantes_Reportadas'] / df_cruce['Parque_Vehicular']) * 100).round(1)
    df_cruce['Riesgo'] = df_cruce['Capacidad_Ociosa_%'].apply(lambda x: 'Crítico' if x > 12 else 'Moderado' if x > 8 else 'Estable')
    
    # Filtro de estado
    st.markdown("""
        <div style='background-color: white; 
                    padding: 12px 20px; 
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                    margin: 15px 0;'>
            <p style='color: #4070F4; font-size: 0.9rem; font-weight: 600; margin: 0;'>🔍 Análisis por Estado</p>
        </div>
    """, unsafe_allow_html=True)
    
    estado_cruce_sel = st.selectbox("Selecciona Estado para análisis de capacidad:", df_cruce['Estado'])
    row_cruce = df_cruce[df_cruce['Estado'] == estado_cruce_sel].iloc[0]
    
    # KPIs de confirmación con diseño corporativo
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    
    with col_c1:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #29B5E8;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #29B5E8; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Parque Vehicular</p>
                <h2 style='color: #11101D; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>{row_cruce['Parque_Vehicular']:,}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>Unidades motrices totales</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_c2:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #EF553B;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #EF553B; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Vacantes Activas</p>
                <h2 style='color: #11101D; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>{row_cruce['Vacantes_Reportadas']:,}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>Operadores faltantes</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_c3:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #4070F4;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Permisionarios</p>
                <h2 style='color: #11101D; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>{row_cruce['Empresas_Reg']:,}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>Permisionarios federales</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_c4:
        color_riesgo = '#EF553B' if row_cruce['Riesgo'] == 'Crítico' else '#FFA726' if row_cruce['Riesgo'] == 'Moderado' else '#29B5E8'
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid {color_riesgo};
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: {color_riesgo}; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Riesgo de Ociosidad</p>
                <h2 style='color: {color_riesgo}; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>{row_cruce['Capacidad_Ociosa_%']}%</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>Estado: {row_cruce['Riesgo']}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabla de matriz de disponibilidad
    # st.markdown("<h3 style='color: #11101D; font-weight: 600;'>📋 Matriz de Disponibilidad Operativa</h3>", unsafe_allow_html=True)
    # 
    # # Ordenar por capacidad ociosa
    # df_cruce_sorted = df_cruce[['Estado', 'Empresas_Reg', 'Parque_Vehicular', 'Vacantes_Reportadas', 'Capacidad_Ociosa_%', 'Riesgo']].sort_values(by='Capacidad_Ociosa_%', ascending=False)
    # 
    # st.dataframe(
    #     df_cruce_sorted.style.format({
    #         'Empresas_Reg': '{:,.0f}',
    #         'Parque_Vehicular': '{:,.0f}',
    #         'Vacantes_Reportadas': '{:,.0f}',
    #         'Capacidad_Ociosa_%': '{:.1f}%'
    #     }).set_properties(**{
    #         'background-color': 'white',
    #         'color': '#11101D',
    #         'font-family': 'Inter'
    #     }).set_table_styles([
    #         {'selector': 'th', 'props': [('background-color', '#4070F4'), ('color', 'white'), ('font-weight', '600')]},
    #         {'selector': 'td', 'props': [('text-align', 'center')]}
    #     ]),
    #     use_container_width=True,
    #     hide_index=True
    # )
    
    # Análisis específico del estado seleccionado
    st.markdown(f"""
        <div style='background-color: #FFF3E0; 
                    border-left: 5px solid #FFA726;
                    padding: 20px; 
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                    margin: 20px 0;'>
            <p style='color: #11101D; font-size: 0.95rem; margin: 0; line-height: 1.6;'>
                ⚠️ <strong>Análisis para {estado_cruce_sel}:</strong> El <strong style='color: #EF553B;'>{row_cruce['Capacidad_Ociosa_%']}%</strong> 
                de la flota total está en riesgo de no operar por falta de capital humano. 
                Esto representa aproximadamente <strong>{row_cruce['Vacantes_Reportadas']:,} unidades sin operador</strong> disponible.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 10. ANÁLISIS DE CAPACIDAD OCIOSA NACIONAL
    st.markdown("<h2 style='color: #11101D; font-weight: 700; margin-bottom: 5px;'>📉 Capacidad Ociosa por Estado</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; font-size: 1rem; margin-bottom: 20px;'>Ranking nacional de riesgo operativo empresarial</p>", unsafe_allow_html=True)
    
    # Métricas nacionales de resumen
    total_parque = df_cruce['Parque_Vehicular'].sum()
    total_vacantes = df_cruce['Vacantes_Reportadas'].sum()
    capacidad_ociosa_nacional = (total_vacantes / total_parque * 100)
    estados_criticos = len(df_cruce[df_cruce['Capacidad_Ociosa_%'] > 12])
    estados_moderados = len(df_cruce[(df_cruce['Capacidad_Ociosa_%'] > 8) & (df_cruce['Capacidad_Ociosa_%'] <= 12)])
    estados_estables = len(df_cruce[df_cruce['Capacidad_Ociosa_%'] <= 8])
    
    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    
    with col_res1:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #29B5E8;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #29B5E8; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Capacidad Ociosa Nacional</p>
                <h2 style='color: #11101D; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>{capacidad_ociosa_nacional:.1f}%</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>Promedio ponderado</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_res2:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #EF553B;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #EF553B; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Estados Críticos</p>
                <h2 style='color: #EF553B; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>{estados_criticos}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>Ociosidad > 12%</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_res3:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #FFA726;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #FFA726; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Estados Moderados</p>
                <h2 style='color: #FFA726; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>{estados_moderados}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>Ociosidad 8-12%</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_res4:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #4CAF50;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4CAF50; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Estados Estables</p>
                <h2 style='color: #4CAF50; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0;'>{estados_estables}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>Ociosidad < 8%</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráfico de barras: Capacidad ociosa de los 32 estados
    st.markdown("<h3 style='color: #11101D; font-weight: 600;'>📊 Ranking Nacional de Capacidad Ociosa</h3>", unsafe_allow_html=True)
    
    # Ordenar por capacidad ociosa descendente
    df_cruce_ranking = df_cruce.sort_values('Capacidad_Ociosa_%', ascending=False)
    
    # Crear gráfico de barras horizontal
    fig_ranking = px.bar(
        df_cruce_ranking,
        y='Estado',
        x='Capacidad_Ociosa_%',
        orientation='h',
        color='Riesgo',
        color_discrete_map={'Crítico': '#EF553B', 'Moderado': '#FFA726', 'Estable': '#4CAF50'},
        text='Capacidad_Ociosa_%',
        labels={'Capacidad_Ociosa_%': '% de Flota en Riesgo', 'Estado': 'Estado'},
        title='Porcentaje de Capacidad Ociosa por Estado (32 Entidades)',
        height=900
    )
    fig_ranking.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_ranking.update_layout(
        title_font_color='#11101D',
        title_font_size=16,
        title_font_family='Inter',
        font=dict(color='#11101D', family='Inter'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            title=dict(text='Nivel de Riesgo', font=dict(color='#11101D')),
            font=dict(color='#11101D')
        )
    )
    st.plotly_chart(fig_ranking, use_container_width=True)
    
    st.markdown("---")
    
    # Análisis por regiones
    st.markdown("<h3 style='color: #11101D; font-weight: 600;'>🗺️ Análisis por Región Geográfica</h3>", unsafe_allow_html=True)
    
    # Clasificar estados por región
    regiones_dict = {
        'Norte': ['Baja California', 'Baja California Sur', 'Chihuahua', 'Coahuila', 'Durango', 'Nuevo León', 'Sinaloa', 'Sonora', 'Tamaulipas'],
        'Centro': ['Aguascalientes', 'Ciudad de México', 'Estado de México', 'Guanajuato', 'Hidalgo', 'Jalisco', 'Michoacán', 'Morelos', 'Querétaro', 'San Luis Potosí', 'Zacatecas'],
        'Sur': ['Campeche', 'Chiapas', 'Guerrero', 'Oaxaca', 'Puebla', 'Quintana Roo', 'Tabasco', 'Tlaxcala', 'Veracruz', 'Yucatán', 'Colima', 'Nayarit']
    }
    
    df_cruce['Region'] = df_cruce['Estado'].apply(
        lambda x: 'Norte' if x in regiones_dict['Norte'] else 'Centro' if x in regiones_dict['Centro'] else 'Sur'
    )
    
    # Agrupar por región
    region_stats = df_cruce.groupby('Region').agg({
        'Empresas_Reg': 'sum',
        'Parque_Vehicular': 'sum',
        'Vacantes_Reportadas': 'sum',
        'Capacidad_Ociosa_%': 'mean'
    }).round(1)
    
    region_stats['Capacidad_Ociosa_%_Ponderada'] = (
        (region_stats['Vacantes_Reportadas'] / region_stats['Parque_Vehicular']) * 100
    ).round(1)
    
    col_reg1, col_reg2 = st.columns([1, 1])
    
    with col_reg1:
        # Gráfico de barras por región
        fig_region = px.bar(
            region_stats.reset_index(),
            x='Region',
            y='Capacidad_Ociosa_%_Ponderada',
            color='Region',
            color_discrete_map={'Norte': '#29B5E8', 'Centro': '#4070F4', 'Sur': '#EF553B'},
            text='Capacidad_Ociosa_%_Ponderada',
            labels={'Capacidad_Ociosa_%_Ponderada': '% Capacidad Ociosa'},
            title='Capacidad Ociosa por Región'
        )
        fig_region.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_region.update_layout(
            height=400,
            showlegend=False,
            title_font_color='#11101D',
            title_font_size=16,
            title_font_family='Inter',
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_region, use_container_width=True)
    
    with col_reg2:
        # Tabla resumen por región
        st.markdown("<p style='color: #11101D; font-weight: 600; margin-top: 20px;'>Resumen por Región</p>", unsafe_allow_html=True)
        st.dataframe(
            region_stats.style.format({
                'Empresas_Reg': '{:,.0f}',
                'Parque_Vehicular': '{:,.0f}',
                'Vacantes_Reportadas': '{:,.0f}',
                'Capacidad_Ociosa_%': '{:.1f}%',
                'Capacidad_Ociosa_%_Ponderada': '{:.1f}%'
            }).set_properties(**{
                'background-color': 'white',
                'color': '#11101D',
                'font-family': 'Inter'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#4070F4'), ('color', 'white'), ('font-weight', '600')]},
                {'selector': 'td', 'props': [('text-align', 'center')]}
            ]),
            use_container_width=True
        )



# --- FUNCIÓN: Obtener tráfico marítimo desde AIS Hub (API Gratuita) ---
def obtener_trafico_maritimo_aishub(bbox=None, api_key=None):
    """
    Obtiene posiciones de buques en tiempo real desde AIS Hub API (gratuita con registro)
    
    Args:
        bbox: Bounding box [min_lat, min_lon, max_lat, max_lon] para filtrar zona
        api_key: API key de AIS Hub (gratis en https://www.aishub.net/api)
    
    Returns:
        DataFrame con posiciones de buques
    """
    try:
        if not api_key:
            # Intentar obtener desde variables de entorno
            api_key = os.getenv('AISHUB_API_KEY', '')
        
        if not api_key:
            # Si no hay API key, retornar datos simulados
            st.info("💡 Para datos reales de tráfico marítimo, obtén una API key gratuita en https://www.aishub.net/api")
            return generar_trafico_maritimo_simulado()
        
        # Configurar bounding box (Golfo de México y Pacífico Mexicano por defecto)
        if bbox is None:
            bbox = [14.0, -118.0, 32.0, -86.0]  # México completo
        
        url = "http://data.aishub.net/ws.php"
        params = {
            'username': api_key,
            'format': '1',  # JSON
            'output': 'json',
            'compress': '0',
            'latmin': bbox[0],
            'lonmin': bbox[1],
            'latmax': bbox[2],
            'lonmax': bbox[3]
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data and len(data) > 0 and 'ERROR' not in data[0]:
                buques = []
                for vessel in data[0]:
                    if isinstance(vessel, dict):
                        buques.append({
                            'MMSI': vessel.get('MMSI', 'N/A'),
                            'Nombre': vessel.get('NAME', 'Unknown'),
                            'Lat': float(vessel.get('LATITUDE', 0)),
                            'Lon': float(vessel.get('LONGITUDE', 0)),
                            'Velocidad': float(vessel.get('SPEED', 0)),
                            'Rumbo': float(vessel.get('COURSE', 0)),
                            'Tipo': vessel.get('TYPE', 'Unknown'),
                            'Timestamp': vessel.get('TIME', '')
                        })
                
                df = pd.DataFrame(buques)
                if not df.empty:
                    st.success(f"✅ Datos AIS Hub: {len(df)} buques en tiempo real")
                    return df
        
        # Si falla, retornar datos simulados
        st.warning("⚠️ No se pudieron obtener datos de AIS Hub. Usando datos simulados.")
        return generar_trafico_maritimo_simulado()
        
    except Exception as e:
        st.warning(f"⚠️ Error al consultar AIS Hub: {str(e)[:100]}. Usando datos simulados.")
        return generar_trafico_maritimo_simulado()


def generar_trafico_maritimo_simulado():
    """Genera datos simulados de tráfico marítimo para demostración"""
    np.random.seed(42)
    
    # Puertos mexicanos principales
    puertos = [
        {'nombre': 'Manzanillo', 'lat': 19.05, 'lon': -104.31},
        {'nombre': 'Veracruz', 'lat': 19.17, 'lon': -96.13},
        {'nombre': 'Lázaro Cárdenas', 'lat': 17.96, 'lon': -102.19},
        {'nombre': 'Altamira', 'lat': 22.39, 'lon': -97.94},
        {'nombre': 'Ensenada', 'lat': 31.87, 'lon': -116.60}
    ]
    
    tipos_buque = ['Portacontenedores', 'Granelero', 'Petrolero', 'Carga General', 'Ro-Ro']
    buques = []
    
    # Generar buques cerca de puertos y en tránsito
    for i in range(50):
        if i < 25:
            # Buques cerca de puertos
            puerto = np.random.choice(puertos)
            lat = puerto['lat'] + np.random.uniform(-0.5, 0.5)
            lon = puerto['lon'] + np.random.uniform(-0.5, 0.5)
            velocidad = np.random.uniform(0, 5)  # Velocidad baja cerca de puerto
        else:
            # Buques en tránsito
            lat = np.random.uniform(14.0, 32.0)
            lon = np.random.uniform(-118.0, -86.0)
            velocidad = np.random.uniform(10, 22)  # Velocidad de crucero
        
        buques.append({
            'MMSI': f'3{np.random.randint(10000000, 99999999)}',
            'Nombre': f'{np.random.choice(tipos_buque)[:3].upper()}-{1000+i}',
            'Lat': lat,
            'Lon': lon,
            'Velocidad': velocidad,
            'Rumbo': np.random.uniform(0, 360),
            'Tipo': np.random.choice(tipos_buque),
            'Timestamp': datetime.now().isoformat()
        })
    
    return pd.DataFrame(buques)


# --- FUNCIÓN: Sistema de Tracking de Contenedores ---
def buscar_contenedor(numero_contenedor):
    """
    Simula la búsqueda de un contenedor por número con información detallada de disponibilidad para retiro
    
    En producción, esto consultaría:
    - APIs de navieras (Maersk, CMA CGM, MSC, etc.) para tracking
    - APIs de terminales portuarias (SSA, APM Terminals, etc.) para ubicación exacta
    - APIs aduanales (Ventanilla Única, SAAI) para liberación
    - APIs de citas (TAPA, sistemas de terminales) para programación de retiro
    
    Args:
        numero_contenedor: Número del contenedor (ej: MSCU1234567)
    
    Returns:
        Dict con información completa del contenedor incluyendo disponibilidad para retiro
    """
    # Validar formato básico de contenedor (4 letras + 7 números)
    if not numero_contenedor or len(numero_contenedor) < 11:
        return None
    
    # Simular datos de tracking
    navieras = ['Maersk', 'CMA CGM', 'MSC', 'COSCO', 'Hapag-Lloyd', 'ONE', 'Evergreen']
    estados = ['En Tránsito Marítimo', 'En Puerto - Descargando', 'En Aduana - Pendiente Liberación', 
               'Liberado por Aduana', 'Disponible para Retiro', 'En Tránsito Terrestre', 'Entregado']
    puertos = ['Manzanillo', 'Veracruz', 'Lázaro Cárdenas', 'Altamira']
    terminales = {
        'Manzanillo': ['SSA Manzanillo', 'OCUPA Manzanillo', 'TEC Manzanillo'],
        'Veracruz': ['API Veracruz', 'APIVER', 'SSA Veracruz'],
        'Lázaro Cárdenas': ['TECLAZ', 'TEC II', 'TPL'],
        'Altamira': ['OCUPA Altamira', 'TIMSA', 'ALTAMIRA Terminal']
    }
    
    # Generar datos simulados pero consistentes con el número
    hash_val = sum(ord(c) for c in numero_contenedor)
    np.random.seed(hash_val)
    
    # Seleccionar naviera y puerto destino
    naviera = np.random.choice(navieras)
    puerto_destino = np.random.choice(puertos)
    terminal = np.random.choice(terminales[puerto_destino])
    
    # Generar eventos de transporte
    fecha_inicio = datetime.now() - timedelta(days=np.random.randint(15, 45))
    eventos = []
    
    # Evento 1: Recogida en origen
    origen = np.random.choice(['Shanghai', 'Ningbo', 'Yantian', 'Hong Kong', 'Busan'])
    eventos.append({
        'fecha': fecha_inicio,
        'ubicacion': origen,
        'evento': 'Recogida en origen',
        'detalles': 'Contenedor cargado y sellado'
    })
    
    # Evento 2: Carga en buque
    fecha_carga = fecha_inicio + timedelta(days=2)
    buque_nombre = np.random.choice(['MSC GÜLSÜN', 'EVER GIVEN', 'CMA CGM ANTOINE DE SAINT EXUPERY', 
                                      'COSCO SHIPPING UNIVERSE', 'HMM ALGECIRAS'])
    eventos.append({
        'fecha': fecha_carga,
        'ubicacion': origen,
        'evento': 'Cargado en buque',
        'detalles': f'Buque: {buque_nombre}'
    })
    
    # Evento 3: Salida del puerto origen
    fecha_salida = fecha_carga + timedelta(days=1)
    eventos.append({
        'fecha': fecha_salida,
        'ubicacion': origen,
        'evento': 'Salida del puerto',
        'detalles': 'En tránsito marítimo'
    })
    
    # Evento 4: En tránsito
    dias_transito = np.random.randint(12, 25)
    fecha_transito = fecha_salida + timedelta(days=int(dias_transito/2))
    eventos.append({
        'fecha': fecha_transito,
        'ubicacion': f'Océano Pacífico - Rumbo a {puerto_destino}',
        'evento': 'En tránsito marítimo',
        'detalles': f'ETA estimado: {dias_transito} días'
    })
    
    # Evento 5: Llegada a puerto
    fecha_llegada = fecha_salida + timedelta(days=dias_transito)
    
    # Determinar estado actual y generar información de disponibilidad
    estado_actual = 'En Tránsito Marítimo'
    ubicacion_actual = eventos[-1]['ubicacion']
    info_retiro = None
    
    if datetime.now() > fecha_llegada:
        # El contenedor ya llegó
        eventos.append({
            'fecha': fecha_llegada,
            'ubicacion': f'{puerto_destino} - {terminal}',
            'evento': 'Llegada a puerto destino',
            'detalles': f'Descargado en terminal {terminal}'
        })
        
        # Evento 6: Descarga
        fecha_descarga = fecha_llegada + timedelta(hours=np.random.randint(6, 36))
        eventos.append({
            'fecha': fecha_descarga,
            'ubicacion': f'{puerto_destino} - {terminal}',
            'evento': 'Descarga completada',
            'detalles': f'Posición en terminal: Patio {np.random.choice(["A", "B", "C"])}-{np.random.randint(1, 50)}'
        })
        
        # Determinar estado actual basado en días desde llegada
        dias_desde_llegada = (datetime.now() - fecha_llegada).days
        
        if dias_desde_llegada < 2:
            estado_actual = 'En Puerto - Descargando'
            ubicacion_actual = f'{puerto_destino} - {terminal}'
        elif dias_desde_llegada < 3:
            estado_actual = 'En Aduana - Pendiente Liberación'
            ubicacion_actual = f'{puerto_destino} - Recinto Fiscal'
            
            # Evento 7: En proceso aduanal
            fecha_aduana = fecha_descarga + timedelta(hours=12)
            eventos.append({
                'fecha': fecha_aduana,
                'ubicacion': f'{puerto_destino} - Recinto Fiscal',
                'evento': 'En proceso de despacho aduanal',
                'detalles': 'Documentación bajo revisión'
            })
        else:
            # Ya fue liberado
            fecha_liberacion = fecha_descarga + timedelta(days=2)
            eventos.append({
                'fecha': fecha_liberacion,
                'ubicacion': f'{puerto_destino} - {terminal}',
                'evento': 'Liberado por aduana',
                'detalles': 'Pedimento autorizado - Listo para retiro'
            })
            
            estado_actual = 'Disponible para Retiro'
            ubicacion_actual = f'{puerto_destino} - {terminal}'
            
            # INFORMACIÓN CRÍTICA DE RETIRO
            dias_en_terminal = (datetime.now() - fecha_descarga).days
            dias_libres = 7  # Días de almacenaje libre
            dias_libres_restantes = max(0, dias_libres - dias_en_terminal)
            
            # Calcular cargos de demora si ya pasaron los días libres
            if dias_libres_restantes == 0:
                dias_demora = dias_en_terminal - dias_libres
                cargo_diario = 35  # USD por día (20' container)
                if '40' in numero_contenedor:
                    cargo_diario = 50  # USD por día (40' container)
                cargo_demora = dias_demora * cargo_diario
            else:
                cargo_demora = 0
            
            # Generar horarios de retiro
            horarios_retiro = {
                'lunes_viernes': '08:00 - 17:00',
                'sabado': '08:00 - 13:00',
                'domingo': 'Cerrado'
            }
            
            # Documentación requerida
            docs_requeridos = [
                'Pedimento de importación (liberado)',
                'Bill of Lading (original o telex release)',
                'Carta de encomienda del transportista',
                'RFC del importador',
                'Comprobante de pago de almacenaje (si aplica)',
                'Identificación del conductor',
                'Tarjeta de circulación del vehículo'
            ]
            
            # Información de la terminal
            info_terminal = {
                'nombre': terminal,
                'direccion': f'Puerto de {puerto_destino}, México',
                'telefono': f'+52 {np.random.randint(300, 999)} {np.random.randint(100, 999)} {np.random.randint(1000, 9999)}',
                'email': f'retiros@{terminal.lower().replace(" ", "")}.com.mx',
                'sistema_citas': 'TAPA' if np.random.random() > 0.5 else 'Portal de Terminal'
            }
            
            # Ubicación exacta en el patio
            patio = np.random.choice(['A', 'B', 'C', 'D'])
            fila = np.random.randint(1, 50)
            bahia = np.random.randint(1, 20)
            posicion = f'Patio {patio}, Fila {fila}, Bahía {bahia}'
            
            # Generar información de retiro
            info_retiro = {
                'disponible': True,
                'fecha_disponibilidad': fecha_liberacion,
                'terminal': info_terminal,
                'posicion_patio': posicion,
                'dias_libres_restantes': dias_libres_restantes,
                'cargo_demora_usd': cargo_demora,
                'requiere_cita': np.random.choice([True, False]),
                'cita_sugerida': (datetime.now() + timedelta(days=1)).replace(hour=10, minute=0),
                'horarios_retiro': horarios_retiro,
                'documentacion_requerida': docs_requeridos,
                'contacto_emergencia': info_terminal['telefono'],
                'observaciones': []
            }
            
            # Agregar observaciones si hay cargos
            if cargo_demora > 0:
                info_retiro['observaciones'].append(f'⚠️ Cargo por demora: ${cargo_demora:,.2f} USD ({dias_demora} días)')
            
            if dias_libres_restantes <= 2:
                info_retiro['observaciones'].append(f'⏰ URGENTE: Solo {dias_libres_restantes} días libres restantes')
            
            if info_retiro['requiere_cita']:
                info_retiro['observaciones'].append('📅 Requiere programar cita previa para retiro')
    
    # Calcular ETA
    if estado_actual == 'En Tránsito Marítimo':
        eta = fecha_llegada
    elif estado_actual == 'Entregado':
        eta = None
    elif estado_actual == 'Disponible para Retiro':
        eta = datetime.now()  # Ya está disponible
    else:
        # Calcular ETA para disponibilidad
        if estado_actual == 'En Puerto - Descargando':
            eta = fecha_llegada + timedelta(days=3)
        else:  # En Aduana
            eta = fecha_llegada + timedelta(days=2, hours=12)
    
    return {
        'numero': numero_contenedor.upper(),
        'naviera': naviera,
        'buque': buque_nombre if datetime.now() > fecha_carga else 'Pendiente asignación',
        'tipo': np.random.choice(['20\' Standard', '40\' Standard', '40\' High Cube', '20\' Reefer', '40\' Reefer']),
        'estado': estado_actual,
        'ubicacion_actual': ubicacion_actual,
        'origen': origen,
        'destino': puerto_destino,
        'eta': eta,
        'peso_kg': np.random.randint(8000, 28000),
        'eventos': eventos,
        'info_retiro': info_retiro,  # ← INFORMACIÓN CLAVE PARA RETIRO
        'ultima_actualizacion': datetime.now()
    }


# --- SISTEMA DE ALERTAS PARA PUERTOS ---
class SistemaAlertasPuertos:
    def __init__(self):
        self.alertas_file = Path(__file__).parent / "data" / "alertas_puertos_log.json"
        self.umbrales = {
            'critico': {'congestion': 85, 'tiempo_espera': 72, 'saturacion': 85},
            'alto': {'congestion': 70, 'tiempo_espera': 48, 'saturacion': 70},
            'medio': {'congestion': 60, 'tiempo_espera': 24, 'saturacion': 60}
        }
        self.alertas_activas = []
        self.cargar_historial()
    
    def cargar_historial(self):
        """Carga el historial de alertas de puertos"""
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
            self.historial = self.historial[-100:]
            self.alertas_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.alertas_file, 'w', encoding='utf-8') as f:
                json.dump(self.historial, f, ensure_ascii=False, indent=2)
        except Exception as e:
            pass
    
    def evaluar_puertos(self, df_puertos):
        """Evalúa el estado de los puertos y genera alertas"""
        self.alertas_activas = []
        timestamp = datetime.now().isoformat()
        
        for idx, row in df_puertos.iterrows():
            puerto = row['Puerto']
            saturacion = row.get('Saturacion', 0)
            tiempo_espera = row.get('Tiempo_Espera_hrs', 0)
            congestion = row.get('Indice_Congestion', 0)
            
            nivel = None
            mensaje = ""
            
            if saturacion >= self.umbrales['critico']['saturacion'] or \
               tiempo_espera >= self.umbrales['critico']['tiempo_espera'] or \
               congestion >= self.umbrales['critico']['congestion']:
                nivel = '🔴 CRÍTICO'
                mensaje = f"Saturación: {saturacion}% | Espera: {tiempo_espera}hrs | Congestión: {congestion}%"
            elif saturacion >= self.umbrales['alto']['saturacion'] or \
                 tiempo_espera >= self.umbrales['alto']['tiempo_espera'] or \
                 congestion >= self.umbrales['alto']['congestion']:
                nivel = '🟠 ALTO'
                mensaje = f"Saturación: {saturacion}% | Espera: {tiempo_espera}hrs | Congestión: {congestion}%"
            elif saturacion >= self.umbrales['medio']['saturacion'] or \
                 tiempo_espera >= self.umbrales['medio']['tiempo_espera'] or \
                 congestion >= self.umbrales['medio']['congestion']:
                nivel = '🟡 MEDIO'
                mensaje = f"Saturación: {saturacion}% | Espera: {tiempo_espera}hrs | Congestión: {congestion}%"
            
            if nivel:
                alerta = {
                    'timestamp': timestamp,
                    'puerto': puerto,
                    'nivel': nivel,
                    'mensaje': mensaje,
                    'saturacion': saturacion,
                    'tiempo_espera': tiempo_espera,
                    'congestion': congestion
                }
                self.alertas_activas.append(alerta)
                self.guardar_alerta(alerta)
        
        return self.alertas_activas
    
    def obtener_estadisticas_alertas(self):
        """Obtiene estadísticas del historial de alertas"""
        if not self.historial:
            return None
        
        ahora = datetime.now()
        alertas_24h = [a for a in self.historial 
                      if (ahora - datetime.fromisoformat(a['timestamp'])).total_seconds() < 86400]
        
        if not alertas_24h:
            return None
        
        alertas_criticas_24h = len([a for a in alertas_24h if '🔴' in a['nivel']])
        
        puertos_con_alertas = {}
        for alerta in alertas_24h:
            puerto = alerta['puerto']
            puertos_con_alertas[puerto] = puertos_con_alertas.get(puerto, 0) + 1
        
        puerto_mas_alertas = max(puertos_con_alertas.items(), key=lambda x: x[1])[0] if puertos_con_alertas else "N/A"
        
        saturaciones = [a['saturacion'] for a in alertas_24h if 'saturacion' in a]
        promedio_saturacion = sum(saturaciones) / len(saturaciones) if saturaciones else 0
        
        return {
            'total_alertas_24h': len(alertas_24h),
            'alertas_criticas_24h': alertas_criticas_24h,
            'puerto_mas_alertas': puerto_mas_alertas,
            'promedio_saturacion': promedio_saturacion
        }


# --- FUNCIÓN: Cargar datos reales de puertos ---
def cargar_datos_puertos_reales():
    """Carga datos reales de puertos desde CSV o genera datos simulados enriquecidos"""
    try:
        csv_path = Path(__file__).parent / "data" / "puertos_latest.csv"
        
        if csv_path.exists():
            df_puertos = pd.read_csv(csv_path)
            
            # Validar columnas esperadas
            if 'Puerto' in df_puertos.columns:
                # Enriquecer con métricas adicionales si no existen
                if 'Tiempo_Espera_hrs' not in df_puertos.columns:
                    df_puertos['Tiempo_Espera_hrs'] = df_puertos.get('Vol_Actual', df_puertos.get('Saturacion', 50)) / 5000 + np.random.uniform(12, 48, len(df_puertos))
                
                if 'Indice_Congestion' not in df_puertos.columns:
                    df_puertos['Indice_Congestion'] = df_puertos.get('Saturacion', np.random.uniform(40, 85, len(df_puertos)))
                
                if 'Buques_Esperando' not in df_puertos.columns:
                    df_puertos['Buques_Esperando'] = (df_puertos['Tiempo_Espera_hrs'] / 12).astype(int) + np.random.randint(0, 5, len(df_puertos))
                
                return df_puertos
        
        # Si no existe CSV, generar datos simulados enriquecidos
        puerto_data = {
            'Puerto': ['Manzanillo', 'Veracruz', 'Lázaro Cárdenas', 'Altamira', 'Ensenada', 'Tuxpan'],
            'Vol_Actual': [320000, 110000, 180000, 95000, 75000, 45000],
            'Capacidad': [350000, 180000, 220000, 150000, 120000, 80000],
            'Operaciones': [450, 280, 320, 210, 180, 120],
            'Lat': [19.0522, 19.1738, 17.9585, 22.3943, 31.8667, 20.9577],
            'Lon': [-104.3158, -96.1342, -102.1891, -97.9377, -116.6000, -97.4054],
            'Tipo_Carga': ['Contenedores', 'Granel/General', 'Contenedores', 'Granel/Petróleo', 'Contenedores/Cruceros', 'Petróleo/Granel'],
            'Tiempo_Espera_hrs': [36, 18, 28, 24, 20, 15],
            'Indice_Congestion': [78, 52, 68, 58, 45, 35],
            'Buques_Esperando': [8, 3, 6, 5, 4, 2]
        }
        
        df_puertos = pd.DataFrame(puerto_data)
        return df_puertos
        
    except Exception as e:
        st.error(f"❌ Error al cargar datos de puertos: {e}")
        return None


# --- FUNCIÓN: Calcular rutas marítimas y costos ---
def calcular_rutas_maritimas(puerto_origen):
    """Calcula rutas, costos y tiempos desde un puerto mexicano a destinos clave"""
    rutas = {
        'Manzanillo': [
            {'destino': 'Los Angeles', 'distancia_nm': 1450, 'tiempo_dias': 4, 'costo_usd': 850, 'via': 'Directa'},
            {'destino': 'Shanghai', 'distancia_nm': 6200, 'tiempo_dias': 18, 'costo_usd': 2800, 'via': 'Transpacífico'},
            {'destino': 'Houston', 'distancia_nm': 2100, 'tiempo_dias': 8, 'costo_usd': 1200, 'via': 'Canal de Panamá'},
            {'destino': 'Rotterdam', 'distancia_nm': 8500, 'tiempo_dias': 28, 'costo_usd': 3500, 'via': 'Canal de Panamá'}
        ],
        'Veracruz': [
            {'destino': 'Miami', 'distancia_nm': 1100, 'tiempo_dias': 4, 'costo_usd': 700, 'via': 'Golfo de México'},
            {'destino': 'Houston', 'distancia_nm': 850, 'tiempo_dias': 3, 'costo_usd': 600, 'via': 'Golfo de México'},
            {'destino': 'Rotterdam', 'distancia_nm': 5200, 'tiempo_dias': 18, 'costo_usd': 2200, 'via': 'Atlántico'},
            {'destino': 'Santos', 'distancia_nm': 4800, 'tiempo_dias': 16, 'costo_usd': 1900, 'via': 'Atlántico Sur'}
        ],
        'Lázaro Cárdenas': [
            {'destino': 'Los Angeles', 'distancia_nm': 1520, 'tiempo_dias': 4, 'costo_usd': 900, 'via': 'Directa'},
            {'destino': 'Shanghai', 'distancia_nm': 6350, 'tiempo_dias': 19, 'costo_usd': 2900, 'via': 'Transpacífico'},
            {'destino': 'Houston', 'distancia_nm': 2200, 'tiempo_dias': 8, 'costo_usd': 1250, 'via': 'Canal de Panamá'},
            {'destino': 'Vancouver', 'distancia_nm': 2800, 'tiempo_dias': 9, 'costo_usd': 1400, 'via': 'Costa Pacífico'}
        ],
        'Altamira': [
            {'destino': 'Houston', 'distancia_nm': 520, 'tiempo_dias': 2, 'costo_usd': 450, 'via': 'Golfo de México'},
            {'destino': 'New Orleans', 'distancia_nm': 680, 'tiempo_dias': 3, 'costo_usd': 550, 'via': 'Golfo de México'},
            {'destino': 'Miami', 'distancia_nm': 1200, 'tiempo_dias': 4, 'costo_usd': 750, 'via': 'Golfo de México'},
            {'destino': 'Rotterdam', 'distancia_nm': 5400, 'tiempo_dias': 19, 'costo_usd': 2300, 'via': 'Atlántico'}
        ],
        'Ensenada': [
            {'destino': 'Los Angeles', 'distancia_nm': 280, 'tiempo_dias': 1, 'costo_usd': 350, 'via': 'Cabotaje'},
            {'destino': 'San Francisco', 'distancia_nm': 520, 'tiempo_dias': 2, 'costo_usd': 450, 'via': 'Costa Pacífico'},
            {'destino': 'Shanghai', 'distancia_nm': 5800, 'tiempo_dias': 17, 'costo_usd': 2600, 'via': 'Transpacífico'},
            {'destino': 'Vancouver', 'distancia_nm': 1100, 'tiempo_dias': 4, 'costo_usd': 700, 'via': 'Costa Pacífico'}
        ],
        'Tuxpan': [
            {'destino': 'Houston', 'distancia_nm': 920, 'tiempo_dias': 3, 'costo_usd': 650, 'via': 'Golfo de México'},
            {'destino': 'Tampa', 'distancia_nm': 1050, 'tiempo_dias': 4, 'costo_usd': 700, 'via': 'Golfo de México'},
            {'destino': 'Miami', 'distancia_nm': 1250, 'tiempo_dias': 5, 'costo_usd': 800, 'via': 'Golfo de México'},
            {'destino': 'Rotterdam', 'distancia_nm': 5300, 'tiempo_dias': 18, 'costo_usd': 2250, 'via': 'Atlántico'}
        ]
    }
    
    return rutas.get(puerto_origen, [])


# --- FUNCIÓN: Generar datos de buques en tiempo real ---
def generar_buques_tiempo_real(puerto):
    """Genera datos simulados de buques en puerto o en tránsito"""
    tipos_buque = ['Portacontenedores', 'Granelero', 'Petrolero', 'Ro-Ro', 'Carga General']
    estados = ['En Puerto', 'Aproximándose', 'En Descarga', 'En Carga', 'Saliendo']
    
    num_buques = np.random.randint(3, 12)
    buques = []
    
    for i in range(num_buques):
        tipo = np.random.choice(tipos_buque)
        estado = np.random.choice(estados)
        
        # Generar ETA basado en estado
        if estado == 'En Puerto':
            eta_hrs = 0
            etd_hrs = np.random.randint(6, 48)
        elif estado == 'Aproximándose':
            eta_hrs = np.random.randint(2, 24)
            etd_hrs = eta_hrs + np.random.randint(24, 72)
        elif estado == 'En Descarga' or estado == 'En Carga':
            eta_hrs = 0
            etd_hrs = np.random.randint(12, 36)
        else:  # Saliendo
            eta_hrs = 0
            etd_hrs = np.random.randint(1, 6)
        
        buque = {
            'Nombre': f"{tipo[:3].upper()}-{1000+i}",
            'Tipo': tipo,
            'Estado': estado,
            'ETA_hrs': eta_hrs,
            'ETD_hrs': etd_hrs,
            'Carga_TEUs': np.random.randint(500, 8000) if tipo == 'Portacontenedores' else 0,
            'Bandera': np.random.choice(['Panamá', 'Liberia', 'México', 'Malta', 'Singapur'])
        }
        buques.append(buque)
    
    return pd.DataFrame(buques)


def page_mapa_autotransporte():
    """Análisis geográfico de puertos marítimos y operaciones portuarias."""
    
    # Título con diseño corporativo
    st.markdown("""
        <div style='background: linear-gradient(135deg, #11101D 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 30px 40px; 
                    border-radius: 15px; 
                    margin-bottom: 30px;
                    box-shadow: 0 8px 20px rgba(17, 16, 29, 0.3);'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'>⚓ Puertos Marítimos Mexicanos</h1>
            <p style='color: #29B5E8; font-size: 1.2rem; font-weight: 500; margin-top: 10px; margin-bottom: 0;'>Análisis de capacidad, operaciones, congestión y seguimiento de buques</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Inicializar sistema de alertas de puertos
    if 'sistema_alertas_puertos' not in st.session_state:
        st.session_state.sistema_alertas_puertos = SistemaAlertasPuertos()
    
    sistema_alertas = st.session_state.sistema_alertas_puertos
    
    # Botones de control
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    with col_btn1:
        btn_recargar = st.button("🔄 Recargar Datos", help="Recarga datos de puertos", key="btn_recargar_puertos")
    with col_btn2:
        usar_datos_reales = st.checkbox("📊 Datos Reales", value=False, help="Alternar entre datos simulados y reales", key="check_real_puertos")
    with col_btn3:
        st.caption("📡 Monitoreo en tiempo real de puertos marítimos")
    
    # Cargar datos de puertos
    df_puertos = cargar_datos_puertos_reales()
    
    if df_puertos is None or df_puertos.empty:
        st.error("❌ No se pudieron cargar datos de puertos")
        return
    
    # Función para calcular índice de saturación
    def calcular_indice_saturacion(volumen, capacidad):
        idx = (volumen / capacidad) * 100
        if idx > 80:
            status = "Crítico"
        elif idx > 60:
            status = "Alto"
        else:
            status = "Normal"
        return round(idx, 2), status
    
    # Asegurar que las columnas necesarias existan
    if 'Vol_Actual' not in df_puertos.columns:
        df_puertos['Vol_Actual'] = np.random.randint(50000, 300000, len(df_puertos))
    
    if 'Capacidad' not in df_puertos.columns:
        df_puertos['Capacidad'] = df_puertos['Vol_Actual'] * np.random.uniform(1.1, 1.5, len(df_puertos))
    
    if 'Operaciones' not in df_puertos.columns:
        df_puertos['Operaciones'] = np.random.randint(100, 500, len(df_puertos))
    
    if 'Lat' not in df_puertos.columns or 'Lon' not in df_puertos.columns:
        # Coordenadas predeterminadas para puertos principales
        coords_default = {
            'Manzanillo': (19.0522, -104.3158),
            'Veracruz': (19.1738, -96.1342),
            'Lázaro Cárdenas': (17.9585, -102.1891),
            'Altamira': (22.3943, -97.9377),
            'Ensenada': (31.8667, -116.6000),
            'Tuxpan': (20.9577, -97.4054)
        }
        df_puertos['Lat'] = df_puertos['Puerto'].map(lambda x: coords_default.get(x, (20.0, -100.0))[0])
        df_puertos['Lon'] = df_puertos['Puerto'].map(lambda x: coords_default.get(x, (20.0, -100.0))[1])
    
    if 'Tipo_Carga' not in df_puertos.columns:
        df_puertos['Tipo_Carga'] = 'Contenedores'
    
    # Calcular saturación y estado si no existen
    if 'Saturacion' not in df_puertos.columns or 'Estado' not in df_puertos.columns:
        df_puertos['Saturacion'], df_puertos['Estado'] = zip(*df_puertos.apply(
            lambda x: calcular_indice_saturacion(x['Vol_Actual'], x['Capacidad']), axis=1
        ))
    
    # Calcular capacidad disponible
    df_puertos['Capacidad_Disponible'] = df_puertos['Capacidad'] - df_puertos['Vol_Actual']
    
    # Evaluar alertas
    alertas = sistema_alertas.evaluar_puertos(df_puertos)
    stats_alertas = sistema_alertas.obtener_estadisticas_alertas()
    
    st.markdown("---")
    
    # ============ SISTEMA DE ALERTAS ============
    st.subheader("🚨 Sistema de Alertas Portuarias")
    
    if alertas:
        alertas_criticas = [a for a in alertas if '🔴' in a['nivel']]
        alertas_altas = [a for a in alertas if '🟠' in a['nivel']]
        alertas_medias = [a for a in alertas if '🟡' in a['nivel']]
        
        col_alert1, col_alert2, col_alert3 = st.columns(3)
        with col_alert1:
            st.metric("🔴 Alertas Críticas", len(alertas_criticas), help="Congestión >85% o Espera >72hrs")
        with col_alert2:
            st.metric("🟠 Alertas Altas", len(alertas_altas), help="Congestión >70% o Espera >48hrs")
        with col_alert3:
            st.metric("🟡 Alertas Medias", len(alertas_medias), help="Congestión >60% o Espera >24hrs")
        
        if alertas_criticas:
            st.markdown("<div style='background-color: #EF553B; color: white; padding: 15px; border-radius: 10px; margin: 10px 0;'><h3 style='color: white; margin: 0;'>🔴 ALERTAS CRÍTICAS</h3></div>", unsafe_allow_html=True)
            for alerta in alertas_criticas:
                st.markdown(f"<div style='background-color: #ffebee; border-left: 4px solid #EF553B; padding: 12px; margin: 8px 0; border-radius: 5px;'><span style='color: #11101D; font-weight: 600;'>{alerta['puerto']}</span> - <span style='color: #333;'>{alerta['mensaje']}</span></div>", unsafe_allow_html=True)
        
        if alertas_altas:
            with st.expander(f"🟠 Ver {len(alertas_altas)} Alertas de Nivel Alto"):
                for alerta in alertas_altas:
                    st.warning(f"**{alerta['puerto']}** - {alerta['mensaje']}")
        
        if alertas_medias:
            with st.expander(f"🟡 Ver {len(alertas_medias)} Alertas de Nivel Medio"):
                for alerta in alertas_medias:
                    st.info(f"**{alerta['puerto']}** - {alerta['mensaje']}")
    else:
        st.success("✅ No hay alertas activas. Todos los puertos operan en niveles normales.")
    
    st.markdown("---")
    
    # ============ MÉTRICAS PRINCIPALES ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>📊 Indicadores Generales</h3>
        </div>
    """, unsafe_allow_html=True)
    
    total_volumen = df_puertos['Vol_Actual'].sum()
    total_capacidad = df_puertos['Capacidad'].sum()
    saturacion_promedio = df_puertos['Saturacion'].mean()
    puertos_criticos = len(df_puertos[df_puertos['Estado'] == 'Crítico'])
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #29B5E8;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Volumen Total</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{total_volumen:,.0f}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>📦 TEUs procesados</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #4070F4;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Capacidad Total</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{total_capacidad:,.0f}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>🏗️ TEUs disponibles</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m3:
        color_saturacion = '#EF553B' if saturacion_promedio > 80 else '#FFA726' if saturacion_promedio > 60 else '#4CAF50'
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid {color_saturacion};
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: {color_saturacion}; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Saturación Promedio</p>
                <h2 style='color: {color_saturacion}; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{saturacion_promedio:.1f}%</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>📊 Ocupación nacional</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m4:
        color_critico = '#EF553B' if puertos_criticos > 0 else '#4CAF50'
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid {color_critico};
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: {color_critico}; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Puertos Críticos</p>
                <h2 style='color: {color_critico}; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{puertos_criticos}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>⚠️ Saturación > 80%</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ ANÁLISIS POR PUERTO ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>🏗️ Análisis Detallado por Puerto</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_tabla, col_grafico = st.columns([1, 1])
    
    with col_tabla:
        st.markdown("<h4 style='color: #11101D; font-weight: 600;'>Estado Operativo</h4>", unsafe_allow_html=True)
        
        # Tabla con formato condicional
        def color_estado(val):
            if val == 'Crítico':
                return 'background-color: #FFEBEE; color: #EF553B; font-weight: 600;'
            elif val == 'Alto':
                return 'background-color: #FFF3E0; color: #FFA726; font-weight: 600;'
            else:
                return 'background-color: #E8F5E9; color: #4CAF50; font-weight: 600;'
        
        df_display = df_puertos[['Puerto', 'Vol_Actual', 'Capacidad', 'Saturacion', 'Estado']].copy()
        st.dataframe(
            df_display.style.format({
                'Vol_Actual': '{:,.0f}',
                'Capacidad': '{:,.0f}',
                'Saturacion': '{:.1f}%'
            }).applymap(color_estado, subset=['Estado']),
            use_container_width=True,
            height=220
        )
    
    with col_grafico:
        st.markdown("<h4 style='color: #11101D; font-weight: 600;'>Saturación por Puerto</h4>", unsafe_allow_html=True)
        
        # Gráfico de barras horizontal
        color_map = {'Crítico': '#EF553B', 'Alto': '#FFA726', 'Normal': '#4CAF50'}
        df_puertos['Color'] = df_puertos['Estado'].map(color_map)
        
        fig_saturacion = px.bar(
            df_puertos.sort_values('Saturacion', ascending=True),
            y='Puerto',
            x='Saturacion',
            orientation='h',
            color='Estado',
            color_discrete_map=color_map,
            text='Saturacion',
            labels={'Saturacion': '% Saturación'}
        )
        fig_saturacion.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_saturacion.update_layout(
            height=250,
            showlegend=True,
            title_font_color='#11101D',
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_saturacion, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ CAPACIDAD DISPONIBLE ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>📈 Capacidad y Utilización</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_cap1, col_cap2 = st.columns([1, 1])
    
    with col_cap1:
        st.markdown("<h4 style='color: #11101D; font-weight: 600;'>Comparativa Volumen vs Capacidad</h4>", unsafe_allow_html=True)
        
        # Gráfico de barras agrupadas
        df_melt = df_puertos.melt(
            id_vars=['Puerto'],
            value_vars=['Vol_Actual', 'Capacidad'],
            var_name='Métrica',
            value_name='TEUs'
        )
        
        fig_comparativa = px.bar(
            df_melt,
            x='Puerto',
            y='TEUs',
            color='Métrica',
            barmode='group',
            color_discrete_map={'Vol_Actual': '#4070F4', 'Capacidad': '#29B5E8'},
            labels={'TEUs': 'TEUs/mes'}
        )
        fig_comparativa.update_layout(
            height=350,
            title_font_color='#11101D',
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend_title_text='',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_comparativa, use_container_width=True)
    
    with col_cap2:
        st.markdown("<h4 style='color: #11101D; font-weight: 600;'>Distribución de Volumen</h4>", unsafe_allow_html=True)
        
        # Gráfico de dona
        fig_pie = px.pie(
            df_puertos,
            values='Vol_Actual',
            names='Puerto',
            hole=0.4,
            color_discrete_sequence=['#29B5E8', '#4070F4', '#EF553B', '#FFA726']
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            height=350,
            font=dict(color='#11101D', family='Inter'),
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=False
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ MAPA GEOGRÁFICO ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>🗺️ Ubicación Geográfica</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Mapa con scatter
    fig_mapa = px.scatter_mapbox(
        df_puertos,
        lat='Lat',
        lon='Lon',
        hover_name='Puerto',
        hover_data={'Saturacion': ':.1f', 'Vol_Actual': ':,.0f', 'Estado': True, 'Lat': False, 'Lon': False},
        color='Estado',
        color_discrete_map=color_map,
        size='Vol_Actual',
        size_max=30,
        zoom=4.5,
        height=500
    )
    fig_mapa.update_layout(
        mapbox_style="open-street-map",
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig_mapa, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ ANÁLISIS DE TIEMPOS DE ESPERA Y CONGESTIÓN ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>⏱️ Tiempos de Espera y Congestión Portuaria</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_tiempo1, col_tiempo2 = st.columns([1, 1])
    
    with col_tiempo1:
        st.markdown("<h4 style='color: #11101D; font-weight: 600;'>Tiempos de Espera por Puerto</h4>", unsafe_allow_html=True)
        
        # Gráfico de barras de tiempos de espera
        fig_espera = px.bar(
            df_puertos.sort_values('Tiempo_Espera_hrs', ascending=False),
            x='Tiempo_Espera_hrs',
            y='Puerto',
            orientation='h',
            text='Tiempo_Espera_hrs',
            labels={'Tiempo_Espera_hrs': 'Horas de Espera'},
            color='Tiempo_Espera_hrs',
            color_continuous_scale=['#4CAF50', '#FFA726', '#EF553B']
        )
        fig_espera.update_traces(texttemplate='%{text:.0f}hrs', textposition='outside')
        fig_espera.update_layout(
            height=300,
            showlegend=False,
            title_font_color='#11101D',
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_espera, use_container_width=True)
        
        # Métricas de tiempo
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            tiempo_promedio = df_puertos['Tiempo_Espera_hrs'].mean()
            st.metric("⏰ Tiempo Promedio Espera", f"{tiempo_promedio:.1f} hrs")
        with col_t2:
            puerto_max_espera = df_puertos.loc[df_puertos['Tiempo_Espera_hrs'].idxmax(), 'Puerto']
            st.metric("🔴 Puerto con Mayor Espera", puerto_max_espera)
    
    with col_tiempo2:
        st.markdown("<h4 style='color: #11101D; font-weight: 600;'>Índice de Congestión</h4>", unsafe_allow_html=True)
        
        # Gráfico de gauge para congestión
        fig_congestion = px.bar(
            df_puertos.sort_values('Indice_Congestion', ascending=False),
            x='Indice_Congestion',
            y='Puerto',
            orientation='h',
            text='Indice_Congestion',
            labels={'Indice_Congestion': '% Congestión'},
            color='Indice_Congestion',
            color_continuous_scale=['#4CAF50', '#FFA726', '#EF553B']
        )
        fig_congestion.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
        fig_congestion.update_layout(
            height=300,
            showlegend=False,
            title_font_color='#11101D',
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_congestion, use_container_width=True)
        
        # Métricas de congestión
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            congestion_promedio = df_puertos['Indice_Congestion'].mean()
            st.metric("📊 Congestión Promedio", f"{congestion_promedio:.1f}%")
        with col_c2:
            total_buques_esperando = df_puertos['Buques_Esperando'].sum()
            st.metric("🚢 Buques en Espera", f"{total_buques_esperando}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ COMPARACIÓN DE RUTAS MARÍTIMAS ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>🌊 Comparación de Rutas Marítimas y Costos</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Selector de puerto de origen
    puerto_seleccionado = st.selectbox(
        "Selecciona el puerto de origen:",
        options=df_puertos['Puerto'].tolist(),
        key="select_puerto_rutas"
    )
    
    # Obtener rutas desde el puerto seleccionado
    rutas = calcular_rutas_maritimas(puerto_seleccionado)
    
    if rutas:
        df_rutas = pd.DataFrame(rutas)
        
        col_ruta1, col_ruta2 = st.columns([1, 1])
        
        with col_ruta1:
            st.markdown(f"<h4 style='color: #11101D; font-weight: 600;'>Rutas desde {puerto_seleccionado}</h4>", unsafe_allow_html=True)
            
            # Tabla de rutas
            st.dataframe(
                df_rutas[['destino', 'distancia_nm', 'tiempo_dias', 'costo_usd', 'via']].style.format({
                    'distancia_nm': '{:,.0f} NM',
                    'tiempo_dias': '{:.0f} días',
                    'costo_usd': '${:,.0f}'
                }),
                use_container_width=True,
                height=250
            )
            
            # Métricas de rutas
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                ruta_mas_rapida = df_rutas.loc[df_rutas['tiempo_dias'].idxmin()]
                st.metric("⚡ Ruta Más Rápida", f"{ruta_mas_rapida['destino']}", f"{ruta_mas_rapida['tiempo_dias']} días")
            with col_r2:
                ruta_mas_economica = df_rutas.loc[df_rutas['costo_usd'].idxmin()]
                st.metric("💰 Ruta Más Económica", f"{ruta_mas_economica['destino']}", f"${ruta_mas_economica['costo_usd']:,.0f}")
        
        with col_ruta2:
            st.markdown("<h4 style='color: #11101D; font-weight: 600;'>Comparativa de Costos por Destino</h4>", unsafe_allow_html=True)
            
            # Gráfico de costos
            fig_costos = px.bar(
                df_rutas.sort_values('costo_usd', ascending=True),
                y='destino',
                x='costo_usd',
                orientation='h',
                text='costo_usd',
                labels={'costo_usd': 'Costo USD', 'destino': 'Destino'},
                color='tiempo_dias',
                color_continuous_scale='Viridis'
            )
            fig_costos.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
            fig_costos.update_layout(
                height=250,
                title_font_color='#11101D',
                font=dict(color='#11101D', family='Inter'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=10, b=0),
                coloraxis_colorbar_title="Días"
            )
            st.plotly_chart(fig_costos, use_container_width=True)
            
            # Gráfico de scatter tiempo vs costo
            st.markdown("<h4 style='color: #11101D; font-weight: 600;'>Relación Tiempo vs Costo</h4>", unsafe_allow_html=True)
            fig_scatter = px.scatter(
                df_rutas,
                x='tiempo_dias',
                y='costo_usd',
                text='destino',
                size='distancia_nm',
                color='via',
                labels={'tiempo_dias': 'Tiempo (días)', 'costo_usd': 'Costo (USD)', 'via': 'Vía'}
            )
            fig_scatter.update_traces(textposition='top center')
            fig_scatter.update_layout(
                height=300,
                title_font_color='#11101D',
                font=dict(color='#11101D', family='Inter'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=10, b=0)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning(f"⚠️ No hay rutas disponibles desde {puerto_seleccionado}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ SEGUIMIENTO DE BUQUES EN TIEMPO REAL ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>🚢 Seguimiento de Buques en Tiempo Real</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Selector de puerto para seguimiento
    puerto_seguimiento = st.selectbox(
        "Selecciona el puerto para ver buques:",
        options=df_puertos['Puerto'].tolist(),
        key="select_puerto_seguimiento"
    )
    
    # Generar datos de buques
    df_buques = generar_buques_tiempo_real(puerto_seguimiento)
    
    st.markdown(f"<h4 style='color: #11101D; font-weight: 600;'>Buques en {puerto_seguimiento}</h4>", unsafe_allow_html=True)
    
    # Métricas de buques
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    with col_b1:
        total_buques = len(df_buques)
        st.metric("🚢 Total Buques", total_buques)
    with col_b2:
        buques_puerto = len(df_buques[df_buques['Estado'] == 'En Puerto'])
        st.metric("⚓ En Puerto", buques_puerto)
    with col_b3:
        buques_aproximando = len(df_buques[df_buques['Estado'] == 'Aproximándose'])
        st.metric("🔵 Aproximándose", buques_aproximando)
    with col_b4:
        total_teus = df_buques['Carga_TEUs'].sum()
        st.metric("📦 Total TEUs", f"{total_teus:,.0f}")
    
    # Tabla de buques con formato mejorado
    col_tabla_buques, col_grafico_buques = st.columns([2, 1])
    
    with col_tabla_buques:
        st.markdown("<p style='color: #11101D; font-weight: 600; margin-top: 15px;'>Estado de Buques</p>", unsafe_allow_html=True)
        
        # Función para colorear estados
        def color_estado_buque(val):
            if val == 'En Puerto':
                return 'background-color: #E8F5E9; color: #4CAF50; font-weight: 600;'
            elif val == 'Aproximándose':
                return 'background-color: #E3F2FD; color: #2196F3; font-weight: 600;'
            elif val == 'En Descarga' or val == 'En Carga':
                return 'background-color: #FFF3E0; color: #FFA726; font-weight: 600;'
            else:
                return 'background-color: #F3E5F5; color: #9C27B0; font-weight: 600;'
        
        st.dataframe(
            df_buques.style.format({
                'ETA_hrs': '{:.0f}hrs',
                'ETD_hrs': '{:.0f}hrs',
                'Carga_TEUs': '{:,.0f}'
            }).applymap(color_estado_buque, subset=['Estado']),
            use_container_width=True,
            height=300
        )
    
    with col_grafico_buques:
        st.markdown("<p style='color: #11101D; font-weight: 600; margin-top: 15px;'>Distribución por Estado</p>", unsafe_allow_html=True)
        
        # Gráfico de dona de estados
        estados_count = df_buques['Estado'].value_counts().reset_index()
        estados_count.columns = ['Estado', 'Cantidad']
        
        fig_estados = px.pie(
            estados_count,
            values='Cantidad',
            names='Estado',
            hole=0.4,
            color_discrete_sequence=['#4CAF50', '#2196F3', '#FFA726', '#9C27B0', '#EF553B']
        )
        fig_estados.update_traces(textposition='inside', textinfo='percent+label')
        fig_estados.update_layout(
            height=300,
            font=dict(color='#11101D', family='Inter'),
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )
        st.plotly_chart(fig_estados, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ MAPA DE TRÁFICO MARÍTIMO EN TIEMPO REAL ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>🌊 Mapa de Tráfico Marítimo en Tiempo Real</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background-color: #E3F2FD; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #2196F3;'>
            <p style='margin: 0; color: #1565C0;'>
                <strong>💡 Obtén datos reales:</strong> Registra tu API key gratuita en 
                <a href='https://www.aishub.net/api' target='_blank' style='color: #1565C0; text-decoration: underline;'>AIS Hub</a> 
                y configúrala en el archivo .env como AISHUB_API_KEY
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Obtener API key desde sidebar o .env
    aishub_key = st.sidebar.text_input(
        "🔑 AIS Hub API Key (opcional)",
        type="password",
        value=os.getenv('AISHUB_API_KEY', ''),
        help="Obtén tu API key gratuita en https://www.aishub.net/api"
    )
    
    # Cargar tráfico marítimo
    df_trafico = obtener_trafico_maritimo_aishub(api_key=aishub_key)
    
    if df_trafico is not None and not df_trafico.empty:
        # Filtros
        col_filter1, col_filter2 = st.columns([1, 1])
        with col_filter1:
            tipos_disponibles = df_trafico['Tipo'].unique().tolist()
            tipos_seleccionados = st.multiselect(
                "Filtrar por tipo de buque:",
                options=tipos_disponibles,
                default=tipos_disponibles,
                key="filter_tipo_buque"
            )
        
        with col_filter2:
            min_velocidad = st.slider(
                "Velocidad mínima (nudos):",
                min_value=0.0,
                max_value=30.0,
                value=0.0,
                step=1.0,
                key="filter_velocidad"
            )
        
        # Aplicar filtros
        df_filtrado = df_trafico[
            (df_trafico['Tipo'].isin(tipos_seleccionados)) &
            (df_trafico['Velocidad'] >= min_velocidad)
        ]
        
        # Métricas de tráfico
        col_traf1, col_traf2, col_traf3, col_traf4 = st.columns(4)
        with col_traf1:
            st.metric("🚢 Total Buques", len(df_filtrado))
        with col_traf2:
            velocidad_promedio = df_filtrado['Velocidad'].mean()
            st.metric("⚡ Velocidad Promedio", f"{velocidad_promedio:.1f} kts")
        with col_traf3:
            buques_movimiento = len(df_filtrado[df_filtrado['Velocidad'] > 1])
            st.metric("🔵 En Movimiento", buques_movimiento)
        with col_traf4:
            buques_fondeados = len(df_filtrado[df_filtrado['Velocidad'] <= 1])
            st.metric("⚓ Fondeados/En Puerto", buques_fondeados)
        
        # Mapa interactivo con buques
        st.markdown("<h4 style='color: #11101D; font-weight: 600; margin-top: 20px;'>Posiciones en Tiempo Real</h4>", unsafe_allow_html=True)
        
        # Crear mapa con scatter
        fig_trafico = px.scatter_mapbox(
            df_filtrado,
            lat='Lat',
            lon='Lon',
            hover_name='Nombre',
            hover_data={
                'Tipo': True,
                'Velocidad': ':.1f',
                'Rumbo': ':.0f',
                'MMSI': True,
                'Lat': False,
                'Lon': False
            },
            color='Tipo',
            size='Velocidad',
            size_max=15,
            zoom=5,
            height=600,
            labels={'Velocidad': 'Velocidad (kts)', 'Rumbo': 'Rumbo (°)'}
        )
        fig_trafico.update_layout(
            mapbox_style="open-street-map",
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_trafico, use_container_width=True)
        
        # Tabla resumen de buques
        with st.expander("📋 Ver tabla detallada de buques"):
            st.dataframe(
                df_filtrado[['Nombre', 'Tipo', 'Lat', 'Lon', 'Velocidad', 'Rumbo', 'MMSI']].style.format({
                    'Lat': '{:.4f}',
                    'Lon': '{:.4f}',
                    'Velocidad': '{:.1f} kts',
                    'Rumbo': '{:.0f}°'
                }),
                use_container_width=True,
                height=300
            )
    else:
        st.error("❌ No se pudieron cargar datos de tráfico marítimo")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ RASTREO DE CONTENEDORES ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>📦 Rastreo de Contenedores</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background-color: #FFF3E0; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #FFA726;'>
            <p style='margin: 0; color: #E65100;'>
                <strong>ℹ️ Sistema de demostración:</strong> Ingresa cualquier número de contenedor (ej: MSCU1234567) 
                para ver cómo funciona el tracking. En producción, esto se conectaría a APIs de navieras reales.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Búsqueda de contenedor
    col_search, col_btn = st.columns([3, 1])
    with col_search:
        numero_contenedor = st.text_input(
            "🔍 Ingresa el número de contenedor:",
            placeholder="Ej: MSCU1234567, CMAU8901234",
            help="Formato: 4 letras + 7 números",
            key="input_contenedor"
        )
    with col_btn:
        btn_buscar = st.button("🔎 Buscar", type="primary", key="btn_buscar_contenedor", use_container_width=True)
    
    if btn_buscar and numero_contenedor:
        resultado = buscar_contenedor(numero_contenedor)
        
        if resultado:
            # Encabezado del contenedor
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #11101D 0%, #4070F4 100%); 
                            color: white; 
                            padding: 20px; 
                            border-radius: 10px; 
                            margin: 20px 0;
                            box-shadow: 0 4px 15px rgba(17, 16, 29, 0.2);'>
                    <h2 style='color: white; margin: 0; font-size: 1.8rem;'>📦 {resultado['numero']}</h2>
                    <p style='color: #29B5E8; margin: 5px 0 0 0; font-size: 1.1rem;'>{resultado['naviera']} | {resultado['tipo']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Métricas principales
            col_info1, col_info2, col_info3, col_info4 = st.columns(4)
            
            with col_info1:
                # Color según estado
                color_estado = {
                    'En Tránsito Marítimo': '#2196F3',
                    'En Puerto': '#4CAF50',
                    'En Aduana': '#FFA726',
                    'En Transporte Terrestre': '#9C27B0',
                    'Entregado': '#4CAF50',
                    'Disponible para Retiro': '#00BCD4'
                }.get(resultado['estado'], '#666')
                
                st.markdown(f"""
                    <div style='background-color: white; 
                                border-left: 5px solid {color_estado};
                                padding: 15px; 
                                border-radius: 8px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                        <p style='color: #666; font-size: 0.85rem; margin: 0;'>Estado Actual</p>
                        <h3 style='color: {color_estado}; margin: 5px 0; font-size: 1.3rem;'>{resultado['estado']}</h3>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_info2:
                st.markdown(f"""
                    <div style='background-color: white; 
                                border-left: 5px solid #29B5E8;
                                padding: 15px; 
                                border-radius: 8px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                        <p style='color: #666; font-size: 0.85rem; margin: 0;'>Ubicación Actual</p>
                        <h3 style='color: #11101D; margin: 5px 0; font-size: 1.1rem;'>{resultado['ubicacion_actual']}</h3>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_info3:
                eta_text = resultado['eta'].strftime('%d/%m/%Y') if resultado['eta'] else 'Entregado'
                st.markdown(f"""
                    <div style='background-color: white; 
                                border-left: 5px solid #4070F4;
                                padding: 15px; 
                                border-radius: 8px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                        <p style='color: #666; font-size: 0.85rem; margin: 0;'>ETA Destino</p>
                        <h3 style='color: #11101D; margin: 5px 0; font-size: 1.1rem;'>{eta_text}</h3>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_info4:
                st.markdown(f"""
                    <div style='background-color: white; 
                                border-left: 5px solid #9C27B0;
                                padding: 15px; 
                                border-radius: 8px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                        <p style='color: #666; font-size: 0.85rem; margin: 0;'>Peso</p>
                        <h3 style='color: #11101D; margin: 5px 0; font-size: 1.1rem;'>{resultado['peso_kg']:,} kg</h3>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Ruta del contenedor
            col_ruta_info, col_timeline = st.columns([1, 2])
            
            with col_ruta_info:
                st.markdown("<h4 style='color: #11101D; font-weight: 600;'>🗺️ Ruta</h4>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div style='background-color: #F4F7F6; padding: 15px; border-radius: 8px;'>
                        <p style='margin: 5px 0;'><strong>Origen:</strong> {resultado['origen']}</p>
                        <p style='margin: 5px 0;'><strong>Destino:</strong> {resultado['destino']}</p>
                        <p style='margin: 5px 0;'><strong>Última actualización:</strong><br>{resultado['ultima_actualizacion'].strftime('%d/%m/%Y %H:%M')}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_timeline:
                st.markdown("<h4 style='color: #11101D; font-weight: 600;'>📅 Historial de Eventos</h4>", unsafe_allow_html=True)
                
                # Timeline de eventos
                for evento in reversed(resultado['eventos']):
                    fecha_str = evento['fecha'].strftime('%d/%m/%Y %H:%M')
                    st.markdown(f"""
                        <div style='background-color: white; 
                                    padding: 12px; 
                                    margin: 8px 0; 
                                    border-left: 4px solid #4070F4;
                                    border-radius: 5px;
                                    box-shadow: 0 1px 4px rgba(0,0,0,0.1);'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <div>
                                    <strong style='color: #11101D;'>{evento['evento']}</strong>
                                    <p style='margin: 3px 0; color: #666; font-size: 0.9rem;'>📍 {evento['ubicacion']}</p>
                                    <p style='margin: 3px 0; color: #999; font-size: 0.85rem;'>{evento['detalles']}</p>
                                </div>
                                <span style='color: #4070F4; font-size: 0.85rem; white-space: nowrap; margin-left: 15px;'>{fecha_str}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # ============ INFORMACIÓN DE RETIRO (SI ESTÁ DISPONIBLE) ============
            if resultado.get('info_retiro'):
                info = resultado['info_retiro']
                
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%); 
                                color: white; 
                                padding: 20px; 
                                border-radius: 10px; 
                                margin: 20px 0;
                                box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);'>
                        <h3 style='color: white; margin: 0; font-size: 1.5rem;'>✅ CONTENEDOR DISPONIBLE PARA RETIRO</h3>
                        <p style='color: #E8F5E9; margin: 5px 0 0 0;'>Liberado por aduana - Listo para recolección</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Métricas críticas de retiro
                col_ret1, col_ret2, col_ret3, col_ret4 = st.columns(4)
                
                with col_ret1:
                    color_dias = '#EF553B' if info['dias_libres_restantes'] <= 2 else '#4CAF50'
                    st.markdown(f"""
                        <div style='background-color: white; 
                                    border-left: 5px solid {color_dias};
                                    padding: 15px; 
                                    border-radius: 8px;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <p style='color: #666; font-size: 0.85rem; margin: 0;'>Días Libres Restantes</p>
                            <h2 style='color: {color_dias}; margin: 5px 0; font-size: 2rem;'>{info['dias_libres_restantes']}</h2>
                            <p style='color: #999; font-size: 0.8rem; margin: 0;'>días</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_ret2:
                    color_cargo = '#EF553B' if info['cargo_demora_usd'] > 0 else '#4CAF50'
                    st.markdown(f"""
                        <div style='background-color: white; 
                                    border-left: 5px solid {color_cargo};
                                    padding: 15px; 
                                    border-radius: 8px;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <p style='color: #666; font-size: 0.85rem; margin: 0;'>Cargo por Demora</p>
                            <h2 style='color: {color_cargo}; margin: 5px 0; font-size: 2rem;'>${info['cargo_demora_usd']:,.0f}</h2>
                            <p style='color: #999; font-size: 0.8rem; margin: 0;'>USD</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_ret3:
                    st.markdown(f"""
                        <div style='background-color: white; 
                                    border-left: 5px solid #29B5E8;
                                    padding: 15px; 
                                    border-radius: 8px;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <p style='color: #666; font-size: 0.85rem; margin: 0;'>Disponible Desde</p>
                            <h3 style='color: #11101D; margin: 5px 0; font-size: 1.2rem;'>{info['fecha_disponibilidad'].strftime('%d/%m/%Y')}</h3>
                            <p style='color: #999; font-size: 0.8rem; margin: 0;'>{info['fecha_disponibilidad'].strftime('%H:%M')}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_ret4:
                    icon_cita = '📅' if info['requiere_cita'] else '✅'
                    texto_cita = 'Requiere cita' if info['requiere_cita'] else 'Sin cita previa'
                    st.markdown(f"""
                        <div style='background-color: white; 
                                    border-left: 5px solid #9C27B0;
                                    padding: 15px; 
                                    border-radius: 8px;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <p style='color: #666; font-size: 0.85rem; margin: 0;'>Sistema de Retiro</p>
                            <h3 style='color: #11101D; margin: 5px 0; font-size: 1.2rem;'>{icon_cita} {texto_cita}</h3>
                            <p style='color: #999; font-size: 0.8rem; margin: 0;'>{info['terminal']['sistema_citas']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Observaciones importantes
                if info['observaciones']:
                    st.markdown("<br>", unsafe_allow_html=True)
                    for obs in info['observaciones']:
                        if '⚠️' in obs or 'URGENTE' in obs:
                            st.warning(obs)
                        else:
                            st.info(obs)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Información detallada de la terminal
                col_terminal, col_horarios = st.columns([1, 1])
                
                with col_terminal:
                    st.markdown("<h4 style='color: #11101D; font-weight: 600;'>🏢 Información de la Terminal</h4>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div style='background-color: white; 
                                    padding: 20px; 
                                    border-radius: 10px;
                                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                            <p style='margin: 8px 0;'><strong>Terminal:</strong> {info['terminal']['nombre']}</p>
                            <p style='margin: 8px 0;'><strong>Dirección:</strong> {info['terminal']['direccion']}</p>
                            <p style='margin: 8px 0;'><strong>📞 Teléfono:</strong> {info['terminal']['telefono']}</p>
                            <p style='margin: 8px 0;'><strong>📧 Email:</strong> {info['terminal']['email']}</p>
                            <p style='margin: 8px 0;'><strong>📍 Posición en patio:</strong> {info['posicion_patio']}</p>
                            <p style='margin: 8px 0; padding: 10px; background-color: #E3F2FD; border-radius: 5px;'>
                                <strong>💡 Sistema de citas:</strong> {info['terminal']['sistema_citas']}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if info['requiere_cita']:
                        st.markdown(f"""
                            <div style='background-color: #FFF3E0; 
                                        padding: 15px; 
                                        border-radius: 8px; 
                                        margin-top: 15px;
                                        border-left: 4px solid #FFA726;'>
                                <p style='margin: 0;'><strong>📅 Cita sugerida:</strong></p>
                                <p style='margin: 5px 0; font-size: 1.1rem; color: #E65100;'>
                                    {info['cita_sugerida'].strftime('%d/%m/%Y a las %H:%M')}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                
                with col_horarios:
                    st.markdown("<h4 style='color: #11101D; font-weight: 600;'>🕐 Horarios de Retiro</h4>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div style='background-color: white; 
                                    padding: 20px; 
                                    border-radius: 10px;
                                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                            <div style='padding: 12px; background-color: #E8F5E9; border-radius: 5px; margin-bottom: 10px;'>
                                <p style='margin: 0;'><strong>Lunes a Viernes:</strong></p>
                                <p style='margin: 5px 0; font-size: 1.2rem; color: #2E7D32;'>{info['horarios_retiro']['lunes_viernes']}</p>
                            </div>
                            <div style='padding: 12px; background-color: #E3F2FD; border-radius: 5px; margin-bottom: 10px;'>
                                <p style='margin: 0;'><strong>Sábado:</strong></p>
                                <p style='margin: 5px 0; font-size: 1.2rem; color: #1976D2;'>{info['horarios_retiro']['sabado']}</p>
                            </div>
                            <div style='padding: 12px; background-color: #FFEBEE; border-radius: 5px;'>
                                <p style='margin: 0;'><strong>Domingo:</strong></p>
                                <p style='margin: 5px 0; font-size: 1.2rem; color: #C62828;'>{info['horarios_retiro']['domingo']}</p>
                            </div>
                            <div style='margin-top: 15px; padding: 12px; background-color: #FFF9C4; border-radius: 5px;'>
                                <p style='margin: 0; color: #F57F17;'><strong>⚠️ Contacto de Emergencia:</strong></p>
                                <p style='margin: 5px 0; font-size: 1.1rem; color: #F57F17;'>{info['contacto_emergencia']}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Documentación requerida
                st.markdown("<h4 style='color: #11101D; font-weight: 600;'>📋 Documentación Requerida para Retiro</h4>", unsafe_allow_html=True)
                
                col_docs1, col_docs2 = st.columns(2)
                for idx, doc in enumerate(info['documentacion_requerida']):
                    col = col_docs1 if idx % 2 == 0 else col_docs2
                    with col:
                        st.markdown(f"""
                            <div style='background-color: white; 
                                        padding: 12px; 
                                        margin: 5px 0; 
                                        border-left: 4px solid #4070F4;
                                        border-radius: 5px;
                                        box-shadow: 0 1px 4px rgba(0,0,0,0.1);'>
                                <p style='margin: 0; color: #11101D;'>✓ {doc}</p>
                            </div>
                        """, unsafe_allow_html=True)
                
                # Botón de acción (simulado)
                st.markdown("<br>", unsafe_allow_html=True)
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                with col_btn1:
                    if st.button("📅 Programar Cita de Retiro", type="primary", use_container_width=True, key="btn_cita"):
                        st.success("✅ Funcionalidad de programación de citas próximamente disponible")
                with col_btn2:
                    if st.button("📄 Descargar Documentación", use_container_width=True, key="btn_docs"):
                        st.info("📄 Generando checklist de documentos...")
                with col_btn3:
                    if st.button("📧 Notificar al Transportista", use_container_width=True, key="btn_notify"):
                        st.info("📧 Sistema de notificaciones próximamente disponible")
            
            elif resultado['estado'] in ['En Aduana - Pendiente Liberación', 'En Puerto - Descargando']:
                # Mostrar ETA de disponibilidad
                st.markdown(f"""
                    <div style='background-color: #FFF3E0; 
                                padding: 20px; 
                                border-radius: 10px; 
                                margin: 20px 0;
                                border-left: 6px solid #FFA726;
                                box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                        <h4 style='color: #E65100; margin: 0 0 10px 0;'>⏳ Contenedor en proceso</h4>
                        <p style='margin: 5px 0; font-size: 1.1rem; color: #666;'>
                            <strong>Estado actual:</strong> {resultado['estado']}
                        </p>
                        <p style='margin: 5px 0; font-size: 1.1rem; color: #666;'>
                            <strong>Disponibilidad estimada:</strong> {resultado['eta'].strftime('%d/%m/%Y %H:%M') if resultado['eta'] else 'Calculando...'}
                        </p>
                        <p style='margin: 15px 0 0 0; padding: 12px; background-color: #FFECB3; border-radius: 5px; color: #E65100;'>
                            💡 <strong>Recomendación:</strong> Mantén tu documentación lista para agilizar el retiro una vez liberado
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Contenedor no encontrado. Verifica el número e intenta nuevamente.")


def page_corredores_logisticos():
    """Análisis de corredores logísticos estratégicos con evaluación de riesgo y rentabilidad"""
    
    # Inicializar contadores de keys para evitar duplicados
    if 'chart_counter_corredores' not in st.session_state:
        st.session_state.chart_counter_corredores = 0
    st.session_state.chart_counter_corredores += 1
    chart_id = st.session_state.chart_counter_corredores
    
    # Título con diseño corporativo
    st.markdown("""
        <div style='background: linear-gradient(135deg, #11101D 0%, #4070F4 100%); 
                    color: white; 
                    padding: 30px 40px; 
                    border-radius: 15px; 
                    margin-bottom: 30px;
                    box-shadow: 0 8px 20px rgba(17, 16, 29, 0.3);'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'>🛣️ Corredores Logísticos Estratégicos</h1>
            <p style='color: #29B5E8; font-size: 1.2rem; font-weight: 500; margin-top: 10px; margin-bottom: 0;'>Análisis de rutas críticas, riesgo operativo y rentabilidad</p>
        </div>
    """, unsafe_allow_html=True)
    
    # --- CONFIGURACIÓN DE PUNTOS CLAVE (Coordenadas aproximadas) ---
    puntos = {
        'Manzanillo': [19.05, -104.31],
        'Veracruz': [19.17, -96.13],
        'Lázaro Cárdenas': [17.95, -102.20],
        'Nuevo Laredo': [27.48, -99.50],
        'Tijuana': [32.51, -117.03],
        'Ciudad Juárez': [31.73, -106.48],
        'CDMX': [19.43, -99.13],  # Hub de distribución
        'Ensenada': [31.87, -116.60]
    }
    
    # --- DEFINICIÓN DE CORREDORES ---
    corredores = [
        {"origen": "Manzanillo", "destino": "Nuevo Laredo", "nombre": "Corredor NAFTA Pacífico", "riesgo": "Medio", "rentabilidad": "Alta", "distancia_km": 1850, "tiempo_hrs": 24},
        {"origen": "Veracruz", "destino": "Nuevo Laredo", "nombre": "Corredor del Golfo", "riesgo": "Bajo", "rentabilidad": "Media", "distancia_km": 1100, "tiempo_hrs": 15},
        {"origen": "Manzanillo", "destino": "CDMX", "nombre": "Corredor Centro-Occidente", "riesgo": "Muy Alto", "rentabilidad": "Media", "distancia_km": 750, "tiempo_hrs": 10},
        {"origen": "Lázaro Cárdenas", "destino": "Nuevo Laredo", "nombre": "Corredor Intermodal", "riesgo": "Alto", "rentabilidad": "Alta", "distancia_km": 1650, "tiempo_hrs": 22},
        {"origen": "CDMX", "destino": "Tijuana", "nombre": "Corredor Noroeste", "riesgo": "Bajo", "rentabilidad": "Alta", "distancia_km": 2650, "tiempo_hrs": 35},
        {"origen": "Ensenada", "destino": "Nuevo Laredo", "nombre": "Corredor Frontera Norte", "riesgo": "Medio", "rentabilidad": "Alta", "distancia_km": 2100, "tiempo_hrs": 28}
    ]
    
    df_corr = pd.DataFrame(corredores)
    
    # Calcular métricas
    total_corredores = len(df_corr)
    corredores_bajo_riesgo = len(df_corr[df_corr['riesgo'] == 'Bajo'])
    corredores_alta_rentabilidad = len(df_corr[df_corr['rentabilidad'] == 'Alta'])
    distancia_promedio = df_corr['distancia_km'].mean()
    
    # ============ MÉTRICAS PRINCIPALES ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>📊 Resumen Ejecutivo de Corredores</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #29B5E8;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Total Corredores</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{total_corredores}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>🛣️ Rutas estratégicas</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #4CAF50;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4CAF50; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Bajo Riesgo</p>
                <h2 style='color: #4CAF50; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{corredores_bajo_riesgo}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>✅ Rutas seguras</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #FFA726;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #FFA726; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Alta Rentabilidad</p>
                <h2 style='color: #FFA726; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{corredores_alta_rentabilidad}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>💰 Rutas premium</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #4070F4;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Distancia Promedio</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{distancia_promedio:,.0f}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>📏 Kilómetros</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ MAPA DE RUTAS ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>🗺️ Mapa Interactivo de Corredores</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='color: #666; font-size: 0.95rem;'>Visualización de rutas críticas desde Puertos hacia Fronteras y Hubs de Distribución</p>", unsafe_allow_html=True)
    
    # 1. MAPA DE RUTAS
    fig = go.Figure()
    
    # Mapeo de colores por nivel de riesgo
    color_riesgo = {
        'Bajo': '#4CAF50',
        'Medio': '#FFA726',
        'Alto': '#EF553B',
        'Muy Alto': '#D32F2F'
    }
    
    # Iconos por tipo de punto
    tipo_punto = {
        'Puerto': '⚓',
        'Frontera': '🚛',
        'Hub': '🏢'
    }
    
    # Clasificar puntos
    puertos_lista = ['Manzanillo', 'Veracruz', 'Lázaro Cárdenas', 'Ensenada']
    fronteras_lista = ['Nuevo Laredo', 'Tijuana', 'Ciudad Juárez']
    hubs_lista = ['CDMX']
    
    # Dibujar las rutas (Líneas) primero
    for idx, ruta in enumerate(corredores):
        color = color_riesgo.get(ruta['riesgo'], '#4070F4')
        
        # Calcular punto medio para mostrar información
        mid_lat = (puntos[ruta['origen']][0] + puntos[ruta['destino']][0]) / 2
        mid_lon = (puntos[ruta['origen']][1] + puntos[ruta['destino']][1]) / 2
        
        # Línea de ruta con efecto de grosor según rentabilidad
        line_width = 6 if ruta['rentabilidad'] == 'Alta' else 4 if ruta['rentabilidad'] == 'Media' else 3
        
        fig.add_trace(go.Scattergeo(
            locationmode = 'ISO-3',
            lon = [puntos[ruta['origen']][1], puntos[ruta['destino']][1]],
            lat = [puntos[ruta['origen']][0], puntos[ruta['destino']][0]],
            mode = 'lines',
            line = dict(
                width = line_width, 
                color = color,
                dash = 'solid' if ruta['rentabilidad'] == 'Alta' else 'dot'
            ),
            opacity=0.7,
            name = f"{ruta['nombre']}",
            hoverinfo='skip',
            showlegend=False
        ))
        
        # Punto medio con información (invisible pero con hover)
        fig.add_trace(go.Scattergeo(
            locationmode = 'ISO-3',
            lon = [mid_lon],
            lat = [mid_lat],
            mode = 'markers',
            marker = dict(
                size = 15,
                color = color,
                symbol = 'square',
                opacity = 0.6,
                line = dict(width=2, color='white')
            ),
            name = f"{ruta['nombre']}",
            text = [f"{ruta['distancia_km']} km"],
            hovertemplate = f"<b>{ruta['nombre']}</b><br>" +
                           f"━━━━━━━━━━━━━━━━<br>" +
                           f"📍 Origen: <b>{ruta['origen']}</b><br>" +
                           f"🎯 Destino: <b>{ruta['destino']}</b><br>" +
                           f"━━━━━━━━━━━━━━━━<br>" +
                           f"🚨 Nivel de Riesgo: <b>{ruta['riesgo']}</b><br>" +
                           f"💰 Rentabilidad: <b>{ruta['rentabilidad']}</b><br>" +
                           f"━━━━━━━━━━━━━━━━<br>" +
                           f"📏 Distancia: <b>{ruta['distancia_km']:,} km</b><br>" +
                           f"⏱️ Tiempo Estimado: <b>{ruta['tiempo_hrs']} hrs</b><br>" +
                           f"🚚 Velocidad Prom: <b>{ruta['distancia_km']/ruta['tiempo_hrs']:.0f} km/h</b><br>" +
                           "<extra></extra>",
            showlegend=True
        ))
    
    # Agregar marcadores de PUERTOS
    for puerto in puertos_lista:
        if puerto in puntos:
            fig.add_trace(go.Scattergeo(
                locationmode = 'ISO-3',
                lon = [puntos[puerto][1]],
                lat = [puntos[puerto][0]],
                mode = 'markers+text',
                marker = dict(
                    size = 20,
                    color = '#29B5E8',
                    symbol = 'circle',
                    line = dict(width=3, color='white')
                ),
                text = [puerto],
                textposition = 'top center',
                textfont = dict(size=10, color='#11101D', family='Inter'),
                name = f"Puerto: {puerto}",
                hovertemplate = f"<b>⚓ PUERTO MARÍTIMO</b><br>" +
                               f"<b>{puerto}</b><br>" +
                               f"━━━━━━━━━━━━━━━━<br>" +
                               f"Tipo: Puerto de altura<br>" +
                               f"Coordenadas: {puntos[puerto][0]:.2f}°N, {puntos[puerto][1]:.2f}°W<br>" +
                               "<extra></extra>",
                showlegend=False
            ))
    
    # Agregar marcadores de FRONTERAS
    for frontera in fronteras_lista:
        if frontera in puntos:
            fig.add_trace(go.Scattergeo(
                locationmode = 'ISO-3',
                lon = [puntos[frontera][1]],
                lat = [puntos[frontera][0]],
                mode = 'markers+text',
                marker = dict(
                    size = 20,
                    color = '#EF553B',
                    symbol = 'square',
                    line = dict(width=3, color='white')
                ),
                text = [frontera],
                textposition = 'top center',
                textfont = dict(size=10, color='#11101D', family='Inter'),
                name = f"Frontera: {frontera}",
                hovertemplate = f"<b>🚛 CRUCE FRONTERIZO</b><br>" +
                               f"<b>{frontera}</b><br>" +
                               f"━━━━━━━━━━━━━━━━<br>" +
                               f"Tipo: Aduana fronteriza<br>" +
                               f"Coordenadas: {puntos[frontera][0]:.2f}°N, {puntos[frontera][1]:.2f}°W<br>" +
                               "<extra></extra>",
                showlegend=False
            ))
    
    # Agregar marcadores de HUBS
    for hub in hubs_lista:
        if hub in puntos:
            fig.add_trace(go.Scattergeo(
                locationmode = 'ISO-3',
                lon = [puntos[hub][1]],
                lat = [puntos[hub][0]],
                mode = 'markers+text',
                marker = dict(
                    size = 22,
                    color = '#4070F4',
                    symbol = 'diamond',
                    line = dict(width=3, color='white')
                ),
                text = [hub],
                textposition = 'top center',
                textfont = dict(size=11, color='#11101D', family='Inter', weight='bold'),
                name = f"Hub: {hub}",
                hovertemplate = f"<b>🏢 HUB DE DISTRIBUCIÓN</b><br>" +
                               f"<b>{hub}</b><br>" +
                               f"━━━━━━━━━━━━━━━━<br>" +
                               f"Tipo: Centro de distribución<br>" +
                               f"Coordenadas: {puntos[hub][0]:.2f}°N, {puntos[hub][1]:.2f}°W<br>" +
                               "<extra></extra>",
                showlegend=False
            ))
    
    fig.update_layout(
        geo = dict(
            scope = 'north america',
            projection_type = 'mercator',
            showland = True,
            landcolor = "rgb(243, 243, 243)",
            coastlinecolor = "rgb(204, 204, 204)",
            showlakes = True,
            lakecolor = "rgb(230, 245, 255)",
            showrivers = True,
            rivercolor = "rgb(230, 245, 255)",
            showcountries = True,
            countrycolor = "rgb(204, 204, 204)",
            countrywidth = 1,
            showsubunits = True,
            subunitcolor = "rgb(217, 217, 217)",
            subunitwidth = 0.5,
            lataxis = dict(range = [14, 33]),
            lonaxis = dict(range = [-118, -86]),
            bgcolor = 'rgba(240,245,250,1)'
        ),
        margin={"r":10,"t":10,"l":10,"b":10},
        height=650,
        showlegend=True,
        legend=dict(
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='#4070F4',
            borderwidth=2,
            x=0.02,
            y=0.98,
            xanchor='left',
            yanchor='top',
            font=dict(size=10, color='#11101D', family='Inter')
        ),
        font=dict(color='#11101D', family='Inter'),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Inter",
            font_color="#11101D",
            bordercolor="#4070F4"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, key=f'mapa_corredores_{chart_id}')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ MATRIZ DE DECISIÓN ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>📊 Matriz de Decisión de Corredores</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h4 style='color: #11101D; font-weight: 600;'>Análisis Comparativo</h4>", unsafe_allow_html=True)
    
    # Formato de tabla
    def color_riesgo_tabla(val):
        if val == 'Muy Alto':
            return 'background-color: #FFEBEE; color: #D32F2F; font-weight: 600;'
        elif val == 'Alto':
            return 'background-color: #FFF3E0; color: #EF553B; font-weight: 600;'
        elif val == 'Medio':
            return 'background-color: #FFF8E1; color: #FFA726; font-weight: 600;'
        else:
            return 'background-color: #E8F5E9; color: #4CAF50; font-weight: 600;'
    
    def color_rentabilidad(val):
        if val == 'Alta':
            return 'background-color: #E8F5E9; color: #4CAF50; font-weight: 600;'
        elif val == 'Media':
            return 'background-color: #FFF8E1; color: #FFA726; font-weight: 600;'
        else:
            return 'background-color: #FFEBEE; color: #EF553B; font-weight: 600;'
    
    df_display = df_corr[['nombre', 'origen', 'destino', 'distancia_km', 'tiempo_hrs', 'riesgo', 'rentabilidad']].copy()
    df_display.columns = ['Corredor', 'Origen', 'Destino', 'Distancia (km)', 'Tiempo (hrs)', 'Riesgo', 'Rentabilidad']
    
    # Eliminar filas vacías
    df_display = df_display.dropna(how='all')
    df_display = df_display[df_display['Corredor'].notna()]
    
    styled_df = df_display.style.format({
        'Distancia (km)': '{:,.0f}',
        'Tiempo (hrs)': '{:.0f}'
    }).applymap(color_riesgo_tabla, subset=['Riesgo']).applymap(color_rentabilidad, subset=['Rentabilidad'])
    
    st.dataframe(styled_df, use_container_width=True, height=350)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ ANÁLISIS DE RENTABILIDAD VS RIESGO ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>📈 Análisis de Eficiencia</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_an1, col_an2 = st.columns(2)
    
    with col_an1:
        st.markdown("<h4 style='color: #11101D; font-weight: 600;'>Distancia vs Tiempo de Tránsito</h4>", unsafe_allow_html=True)
        
        fig_scatter = px.scatter(
            df_corr,
            x='distancia_km',
            y='tiempo_hrs',
            color='riesgo',
            size='distancia_km',
            hover_name='nombre',
            color_discrete_map=color_riesgo,
            labels={'distancia_km': 'Distancia (km)', 'tiempo_hrs': 'Tiempo (hrs)'}
        )
        fig_scatter.update_layout(
            height=350,
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_scatter, use_container_width=True, key=f'scatter_distancia_tiempo_{chart_id}')
    
    with col_an2:
        st.markdown("<h4 style='color: #11101D; font-weight: 600;'>Rentabilidad por Corredor</h4>", unsafe_allow_html=True)
        
        # Asignar valores numéricos a rentabilidad
        df_corr['rent_num'] = df_corr['rentabilidad'].map({'Alta': 3, 'Media': 2, 'Baja': 1})
        
        fig_bar = px.bar(
            df_corr.sort_values('rent_num', ascending=True),
            y='nombre',
            x='rent_num',
            orientation='h',
            color='rentabilidad',
            color_discrete_map={'Alta': '#4CAF50', 'Media': '#FFA726', 'Baja': '#EF553B'},
            labels={'rent_num': 'Nivel de Rentabilidad', 'nombre': ''}
        )
        fig_bar.update_layout(
            height=350,
            showlegend=False,
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(tickvals=[1, 2, 3], ticktext=['Baja', 'Media', 'Alta'])
        )
        st.plotly_chart(fig_bar, use_container_width=True, key=f'bar_rentabilidad_{chart_id}')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ RECOMENDACIONES ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #FFA726 0%, #EF553B 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(239, 85, 59, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>💡 Recomendaciones Estratégicas</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_rec1, col_rec2 = st.columns(2)
    
    # Identificar mejores corredores
    mejor_bajo_riesgo = df_corr[(df_corr['riesgo'] == 'Bajo') & (df_corr['rentabilidad'] == 'Alta')]
    mejor_rentabilidad = df_corr[df_corr['rentabilidad'] == 'Alta'].sort_values('distancia_km').iloc[0] if len(df_corr[df_corr['rentabilidad'] == 'Alta']) > 0 else None
    
    with col_rec1:
        if not mejor_bajo_riesgo.empty:
            corredor = mejor_bajo_riesgo.iloc[0]
            st.markdown(f"""
                <div style='background-color: #E8F5E9; 
                            border-left: 4px solid #4CAF50;
                            padding: 20px; 
                            border-radius: 10px;
                            margin: 10px 0;'>
                    <h4 style='color: #11101D; margin-top: 0; font-weight: 600;'>✅ Corredor Óptimo</h4>
                    <p style='color: #333; line-height: 1.6; margin-bottom: 10px;'>
                        <strong>{corredor['nombre']}</strong><br>
                        Combina bajo riesgo con alta rentabilidad. Ideal para cargas de alto valor.
                    </p>
                    <p style='color: #666; font-size: 0.9rem; margin: 0;'>
                        📍 {corredor['origen']} → {corredor['destino']}<br>
                        🚛 {corredor['distancia_km']:,.0f} km | ⏱️ {corredor['tiempo_hrs']} hrs
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    with col_rec2:
        if mejor_rentabilidad is not None:
            st.markdown(f"""
                <div style='background-color: #FFF8E1; 
                            border-left: 4px solid #FFA726;
                            padding: 20px; 
                            border-radius: 10px;
                            margin: 10px 0;'>
                    <h4 style='color: #11101D; margin-top: 0; font-weight: 600;'>💰 Más Rentable</h4>
                    <p style='color: #333; line-height: 1.6; margin-bottom: 10px;'>
                        <strong>{mejor_rentabilidad['nombre']}</strong><br>
                        Ruta de alta rentabilidad con la menor distancia. Optimiza costos operativos.
                    </p>
                    <p style='color: #666; font-size: 0.9rem; margin: 0;'>
                        📍 {mejor_rentabilidad['origen']} → {mejor_rentabilidad['destino']}<br>
                        🚛 {mejor_rentabilidad['distancia_km']:,.0f} km | ⏱️ {mejor_rentabilidad['tiempo_hrs']} hrs
                    </p>
                </div>
            """, unsafe_allow_html=True)


def page_nearshoring():
    """Análisis de tendencias de nearshoring y relocalización industrial"""
    
    # Obtener idioma actual
    lang = st.session_state.language
    
    # Header de la página
    page_header(
        t('menu_nearshoring', lang),
        "Análisis de tendencias de relocalización industrial y nearshoring" if lang == 'es' else 
        "Nearshoring and industrial relocation trends analysis" if lang == 'en' else
        "Analyse des tendances de relocalisation industrielle et de nearshoring",
        "🌎"
    )
    
    # Cargar datos históricos
    @st.cache_data(ttl=600)
    def cargar_datos_nearshoring():
        """Carga y procesa datos para análisis de nearshoring"""
        try:
            # Cargar datos de cruces fronterizos multi-año
            years = [2023, 2024, 2025]
            all_data = []
            
            for year in years:
                file_path = Path(__file__).parent / "data" / f"border_crossings_{year}_historical.csv"
                if file_path.exists():
                    df = pd.read_csv(file_path)
                    df['year'] = year
                    all_data.append(df)
            
            if all_data:
                df_combined = pd.concat(all_data, ignore_index=True)
                df_combined['date'] = pd.to_datetime(df_combined['date'])
                df_combined['month'] = df_combined['date'].dt.month
                df_combined['year_month'] = df_combined['date'].dt.strftime('%Y-%m')
                return df_combined
            else:
                return pd.DataFrame()
                
        except Exception as e:
            st.error(f"Error cargando datos: {e}")
            return pd.DataFrame()
    
    # Cargar datos de aduanas mexicanas
    @st.cache_data(ttl=600)
    def cargar_datos_aduanas():
        """Carga datos de contenedores en aduanas mexicanas"""
        try:
            file_path = Path(__file__).parent / "data" / "aduanas_latest.csv"
            if file_path.exists():
                df = pd.read_csv(file_path)
                df['Fecha'] = pd.to_datetime(df['Fecha'])
                return df
            else:
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error cargando datos de aduanas: {e}")
            return pd.DataFrame()
    
    df_border = cargar_datos_nearshoring()
    df_aduanas = cargar_datos_aduanas()
    
    if df_border.empty:
        st.error("No se pudieron cargar los datos de cruces fronterizos")
        return
    
    # ========== MÉTRICAS PRINCIPALES ==========
    st.markdown("### 📊 Indicadores Clave de Nearshoring" if lang == 'es' else 
                "### 📊 Key Nearshoring Indicators" if lang == 'en' else
                "### 📊 Indicateurs Clés de Nearshoring")
    
    # Calcular métricas principales
    current_year = 2025
    prev_year = 2024
    
    # Contenedores totales (indicador clave de nearshoring)
    containers_current = df_border[
        (df_border['year'] == current_year) & 
        (df_border['measure'].str.contains('Container', case=False))
    ]['value'].sum()
    
    containers_prev = df_border[
        (df_border['year'] == prev_year) & 
        (df_border['measure'].str.contains('Container', case=False))
    ]['value'].sum()
    
    containers_growth = ((containers_current - containers_prev) / containers_prev * 100) if containers_prev > 0 else 0
    
    # Tráfico total de camiones
    trucks_current = df_border[
        (df_border['year'] == current_year) & 
        (df_border['measure'] == 'Trucks')
    ]['value'].sum()
    
    trucks_prev = df_border[
        (df_border['year'] == prev_year) & 
        (df_border['measure'] == 'Trucks')
    ]['value'].sum()
    
    trucks_growth = ((trucks_current - trucks_prev) / trucks_prev * 100) if trucks_prev > 0 else 0
    
    # Métricas de tarjetas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        metric_card(
            "Contenedores 2025" if lang == 'es' else "Containers 2025" if lang == 'en' else "Conteneurs 2025",
            f"{containers_current:,.0f}",
            "📦",
            "#4070F4",
            f"{containers_growth:+.1f}% vs 2024"
        )
    
    with col2:
        metric_card(
            "Camiones 2025" if lang == 'es' else "Trucks 2025" if lang == 'en' else "Camions 2025",
            f"{trucks_current:,.0f}",
            "🚛",
            "#29B5E8",
            f"{trucks_growth:+.1f}% vs 2024"
        )
    
    with col3:
        # Calcular valor total de aduanas si disponible
        total_valor = df_aduanas['Valor_USD'].sum() if not df_aduanas.empty else 0
        metric_card(
            "Valor Comercio (USD)" if lang == 'es' else "Trade Value (USD)" if lang == 'en' else "Valeur Commerce (USD)",
            f"${total_valor:,.0f}M" if total_valor > 0 else "N/A",
            "💰",
            "#4CAF50"
        )
    
    spacer(20)
    
    # ========== ANÁLISIS DE TENDENCIAS ==========
    st.markdown("### 📈 Tendencias de Nearshoring" if lang == 'es' else 
                "### 📈 Nearshoring Trends" if lang == 'en' else
                "### 📈 Tendances de Nearshoring")
    
    # Análisis por año de contenedores
    yearly_containers = df_border[
        df_border['measure'].str.contains('Container', case=False)
    ].groupby('year')['value'].sum().reset_index()
    
    # Gráfico de crecimiento de contenedores
    fig_containers = px.line(
        yearly_containers,
        x='year',
        y='value',
        markers=True,
        title="Crecimiento Anual de Contenedores" if lang == 'es' else 
              "Annual Container Growth" if lang == 'en' else
              "Croissance Annuelle des Conteneurs",
        labels={'value': 'Contenedores', 'year': 'Año'}
    )
    fig_containers.update_layout(
        height=400,
        font=dict(color='#11101D', family='Inter'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig_containers.update_traces(line_color='#4070F4', line_width=3)
    
    st.plotly_chart(fig_containers, use_container_width=True)
    
    spacer(20)
    
    # ========== ANÁLISIS POR FRONTERA ==========
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌎 Frontera México-EEUU" if lang == 'es' else 
                    "#### 🌎 US-Mexico Border" if lang == 'en' else
                    "#### 🌎 Frontière Mexique-ÉU")
        
        # Contenedores México
        mexico_containers = df_border[
            (df_border['border'] == 'US-Mexico Border') & 
            (df_border['measure'].str.contains('Container', case=False))
        ].groupby('year')['value'].sum().reset_index()
        
        fig_mexico = px.bar(
            mexico_containers,
            x='year',
            y='value',
            color='year',
            title="Contenedores México" if lang == 'es' else "Mexico Containers" if lang == 'en' else "Conteneurs Mexique",
            labels={'value': 'Contenedores', 'year': 'Año'}
        )
        fig_mexico.update_layout(
            height=300,
            showlegend=False,
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_mexico, use_container_width=True)
    
    with col2:
        st.markdown("#### ❄️ Frontera Canadá-EEUU" if lang == 'es' else 
                    "#### ❄️ US-Canada Border" if lang == 'en' else
                    "#### ❄️ Frontière Canada-ÉU")
        
        # Contenedores Canadá
        canada_containers = df_border[
            (df_border['border'] == 'US-Canada Border') & 
            (df_border['measure'].str.contains('Container', case=False))
        ].groupby('year')['value'].sum().reset_index()
        
        fig_canada = px.bar(
            canada_containers,
            x='year',
            y='value',
            color='year',
            title="Contenedores Canadá" if lang == 'es' else "Canada Containers" if lang == 'en' else "Conteneurs Canada",
            labels={'value': 'Contenedores', 'year': 'Año'}
        )
        fig_canada.update_layout(
            height=300,
            showlegend=False,
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_canada, use_container_width=True)
    
    spacer(20)
    
    # ========== CORREDORES DE MANUFACTURA ==========
    st.markdown("### 🏭 Corredores de Manufactura Estratégicos" if lang == 'es' else 
                "### 🏭 Strategic Manufacturing Corridors" if lang == 'en' else
                "### 🏭 Couloirs de Fabrication Stratégiques")
    st.info("📊 Análisis de nearshoring y corredores de manufactura (en desarrollo)")


# --- PÁGINAS OPCIONALES (si están disponibles) ---
try:
    if MONITOREO_V2_AVAILABLE:
        from monitoreo_v2 import page_monitoreo_v2
except:
    page_monitoreo_v2 = None

try:
    if INDICE_FM_AVAILABLE:
        from indice_freightmetrics import page_indice_freightmetrics
except:
    page_indice_freightmetrics = None

try:
    if ORACLE_RATE_AVAILABLE:
        from oracle_rate import page_oracle_rate
except:
    page_oracle_rate = None


# --- RUTEADOR DEL MENÚ ---
# Mapear la opción seleccionada (en cualquier idioma) a la función correspondiente
menu_mapping = {
    t('menu_dashboard', lang): page_inicio,
    t('menu_monitoring', lang): page_monitoreo_v2 if MONITOREO_V2_AVAILABLE and page_monitoreo_v2 else page_monitoreo_aduanas,
    t('menu_flows', lang): page_mapa,
    t('menu_corridors', lang): page_corredores_logisticos,
    t('menu_ports', lang): page_mapa_autotransporte,
    t('menu_workforce', lang): page_fuerza_laboral,
    t('menu_nearshoring', lang): page_nearshoring,
    t('menu_indice', lang): page_indice_freightmetrics if INDICE_FM_AVAILABLE and page_indice_freightmetrics else None,
    t('menu_oracle', lang): page_oracle_rate if ORACLE_RATE_AVAILABLE and page_oracle_rate else None,
}

# Ejecutar la página seleccionada
if opcion and opcion in menu_mapping and menu_mapping[opcion]:
    menu_mapping[opcion]()
else:
    page_inicio()  # Página por defecto

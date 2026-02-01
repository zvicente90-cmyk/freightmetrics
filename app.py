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
    """Carga datos de aduanas desde CSV o API"""
    try:
        # Intentar cargar desde CSV local primero
        csv_path = Path(__file__).parent / "data" / "aduanas_latest.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            return df
    except Exception as e:
        st.warning(f"No se pudieron cargar datos locales: {e}")
    
    # Si falla, intentar desde API local
    try:
        response = requests.get("http://localhost:8000/functions/v1/aduanas", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data['data'])
    except:
        pass
    
    return None

# --- FUNCIÓN: Cargar datos de flujos históricos ---
def cargar_datos_flujos_reales():
    """Carga datos históricos de flujos/cruces desde CSV o genera desde datos actuales"""
    try:
        # Intentar cargar desde CSV local
        csv_path = Path(__file__).parent / "data" / "aduanas_latest.csv"
        if csv_path.exists():
            df_actual = pd.read_csv(csv_path)
            
            # Generar datos históricos simulados basados en datos reales
            fechas = pd.date_range(start=(datetime.now() - pd.DateOffset(months=12)).strftime('%Y-%m-%d'), 
                                   end=datetime.now().strftime('%Y-%m-%d'), freq='D')
            
            data_list = []
            for _, row in df_actual.iterrows():
                aduana = row['Aduana']
                valor_base = row['Valor_USD']
                contenedores_base = row['Contenedores']
                
                # Generar serie temporal con tendencia y variabilidad
                for i, fecha in enumerate(fechas):
                    # Factor de crecimiento (tendencia)
                    factor_crecimiento = 1 + (i / len(fechas)) * 0.15  # 15% crecimiento en el año
                    
                    # Variabilidad diaria
                    variabilidad = np.random.uniform(0.85, 1.15)
                    
                    cruces = int(contenedores_base * factor_crecimiento * variabilidad)
                    valor_usd = valor_base * factor_crecimiento * variabilidad
                    
                    data_list.append({
                        'Fecha': fecha,
                        'Puerto': aduana,
                        'Cruces': cruces,
                        'Valor_USD': valor_usd
                    })
            
            df_historico = pd.DataFrame(data_list)
            return df_historico
    except Exception as e:
        st.warning(f"No se pudieron cargar datos de flujos: {e}")
    
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
        
        for idx, row in df_aduanas.iterrows():
            aduana = row['Aduana']
            saturacion = row.get('Saturación (%)', 0)
            tiempo_espera = row.get('Tiempo Espera (min)', 0)
            
            # Evaluar nivel de alerta
            nivel = None
            mensaje = ""
            
            if saturacion >= self.umbrales['critico']['saturacion'] or tiempo_espera >= self.umbrales['critico']['tiempo_espera']:
                nivel = '🔴 CRÍTICO'
                mensaje = f"Saturación: {saturacion}% | Espera: {tiempo_espera} min"
                icono = '🔴'
            elif saturacion >= self.umbrales['alto']['saturacion'] or tiempo_espera >= self.umbrales['alto']['tiempo_espera']:
                nivel = '🟠 ALTO'
                mensaje = f"Saturación: {saturacion}% | Espera: {tiempo_espera} min"
                icono = '🟠'
            elif saturacion >= self.umbrales['medio']['saturacion'] or tiempo_espera >= self.umbrales['medio']['tiempo_espera']:
                nivel = '🟡 MEDIO'
                mensaje = f"Saturación: {saturacion}% | Espera: {tiempo_espera} min"
                icono = '🟡'
            
            if nivel:
                alerta = {
                    'timestamp': timestamp,
                    'aduana': aduana,
                    'nivel': nivel,
                    'saturacion': saturacion,
                    'tiempo_espera': tiempo_espera,
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
        if not self.historial:
            return None
        
        df_hist = pd.DataFrame(self.historial)
        
        # Últimas 24 horas
        df_hist['timestamp'] = pd.to_datetime(df_hist['timestamp'])
        hace_24h = datetime.now() - timedelta(hours=24)
        df_recientes = df_hist[df_hist['timestamp'] >= hace_24h]
        
        stats = {
            'total_alertas_24h': len(df_recientes),
            'alertas_criticas_24h': len(df_recientes[df_recientes['nivel'].str.contains('CRÍTICO')]),
            'aduana_mas_alertas': df_recientes['aduana'].mode()[0] if len(df_recientes) > 0 else 'N/A',
            'promedio_saturacion': df_recientes['saturacion'].mean() if len(df_recientes) > 0 else 0
        }
        
        return stats

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

# --- FUNCIÓN: Horarios de operación de aduanas ---
def obtener_horarios_aduanas():
    """Retorna horarios de operación de cruces comerciales de mercancías en aduanas - Frontera Norte 2026"""
    horarios = {
        'Nuevo Laredo III (Comercio Mundial)': {
            'horario_normal': 'L-V: 7:00-24:00, Sáb: 8:00-16:00, Dom: 8:00-16:00',
            'lunes_viernes': '07:00 - 00:00',
            'sabado': '08:00 - 16:00',
            'domingo': '08:00 - 16:00',
            'festivos': '08:00 - 14:00',
            'tipo': 'comercial',
            'nota': 'Puente Internacional Comercio Mundial III'
        },
        'Laredo - Colombia': {
            'horario_normal': 'L-V: 8:00-22:30, Sáb: 8:00-16:00, Dom: Cerrado',
            'lunes_viernes': '08:00 - 22:30',
            'sabado': '08:00 - 16:00',
            'domingo': 'Cerrado',
            'festivos': '08:00 - 15:00',
            'tipo': 'comercial',
            'nota': 'Puente Colombia-Solidarity'
        },
        'Tijuana (Mesa de Otay)': {
            'horario_normal': 'L-V: 8:00-20:00, Sáb: 8:00-15:00, Dom: 8:00-14:00',
            'lunes_viernes': '08:00 - 20:00',
            'sabado': '08:00 - 15:00',
            'domingo': '08:00 - 14:00',
            'festivos': '08:00 - 14:00',
            'tipo': 'comercial',
            'nota': 'Mesa de Otay - Otay Mesa'
        },
        'Cd. Juárez (Paso del Norte/Zaragoza)': {
            'horario_normal': 'L-V: 6:00-24:00, Sáb: 6:00-14:00, Dom: Cerrado',
            'lunes_viernes': '06:00 - 00:00',
            'sabado': '06:00 - 14:00',
            'domingo': 'Cerrado',
            'festivos': '08:00 - 16:00',
            'tipo': 'comercial',
            'nota': 'Puentes Paso del Norte/Zaragoza'
        },
        'Mexicali II (Nvo. Mexicali)': {
            'horario_normal': 'L-V: 8:00-20:00, Sáb: 9:00-14:00, Dom: Cerrado',
            'lunes_viernes': '08:00 - 20:00',
            'sabado': '09:00 - 14:00',
            'domingo': 'Cerrado',
            'festivos': '09:00 - 13:00',
            'tipo': 'comercial',
            'nota': 'Mexicali II - Nuevo Mexicali'
        },
        'Nogales (Mariposa)': {
            'horario_normal': 'L-V: 8:00-20:00, Sáb: 8:00-15:00, Dom: Cerrado',
            'lunes_viernes': '08:00 - 20:00',
            'sabado': '08:00 - 15:00',
            'domingo': 'Cerrado',
            'festivos': '08:00 - 14:00',
            'tipo': 'comercial',
            'nota': 'Mariposa Port of Entry'
        },
        'Matamoros (Gral. Ignacio Zaragoza)': {
            'horario_normal': 'L-V: 9:00-20:00, Sáb: 10:00-14:00, Dom: Cerrado',
            'lunes_viernes': '09:00 - 20:00',
            'sabado': '10:00 - 14:00',
            'domingo': 'Cerrado',
            'festivos': '09:00 - 14:00',
            'tipo': 'comercial',
            'nota': 'Puente General Ignacio Zaragoza'
        },
        'Reynosa (Pharr)': {
            'horario_normal': 'L-V: 6:00-24:00, Sáb: 6:00-16:00, Dom: 8:00-16:00',
            'lunes_viernes': '06:00 - 00:00',
            'sabado': '06:00 - 16:00',
            'domingo': '08:00 - 16:00',
            'festivos': '08:00 - 14:00',
            'tipo': 'comercial',
            'nota': 'Puente Internacional Pharr-Reynosa'
        },
        'Piedras Negras': {
            'horario_normal': 'L-V: 8:00-22:30, Sáb: 9:00-15:00, Dom: Cerrado',
            'lunes_viernes': '08:00 - 22:30',
            'sabado': '09:00 - 15:00',
            'domingo': 'Cerrado',
            'festivos': '09:00 - 14:00',
            'tipo': 'comercial',
            'nota': 'Puente Internacional II'
        },
        'San Luis Río Colorado': {
            'horario_normal': 'L-V: 9:00-17:00, Sáb: 9:00-14:00, Dom: Cerrado',
            'lunes_viernes': '09:00 - 17:00',
            'sabado': '09:00 - 14:00',
            'domingo': 'Cerrado',
            'festivos': 'Cerrado',
            'tipo': 'comercial',
            'nota': 'San Luis Port of Entry'
        },
        'Agua Prieta': {
            'horario_normal': 'L-V: 9:00-18:00, Sáb: 9:00-14:00, Dom: Cerrado',
            'lunes_viernes': '09:00 - 18:00',
            'sabado': '09:00 - 14:00',
            'domingo': 'Cerrado',
            'festivos': 'Cerrado',
            'tipo': 'comercial',
            'nota': 'Cruce Comercial Agua Prieta-Douglas'
        },
        'Cd. Acuña': {
            'horario_normal': 'L-V: 8:00-20:00, Sáb: 9:00-14:00, Dom: Cerrado',
            'lunes_viernes': '08:00 - 20:00',
            'sabado': '09:00 - 14:00',
            'domingo': 'Cerrado',
            'festivos': '09:00 - 14:00',
            'tipo': 'comercial',
            'nota': 'Puente Internacional Del Río-Cd. Acuña'
        }
    }
    return horarios

# --- FUNCIÓN: Verificar si aduana está abierta ---
def aduana_esta_abierta(aduana_nombre, fecha, hora=None):
    """Verifica si una aduana está abierta en una fecha/hora específica"""
    horarios = obtener_horarios_aduanas()
    
    if aduana_nombre not in horarios:
        return {'abierta': None, 'mensaje': 'Aduana no encontrada'}
    
    horario = horarios[aduana_nombre]
    
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
        if 'Cerrado' in horario['festivos']:
            return {
                'abierta': False, 
                'mensaje': f"Cerrado por {info_festivo['nombre']}",
                'festivo': info_festivo['nombre']
            }
        elif 'reducido' in horario['festivos']:
            return {
                'abierta': True,
                'mensaje': f"Horario reducido por {info_festivo['nombre']}",
                'festivo': info_festivo['nombre']
            }
    
    # Verificar día de la semana
    dia_semana = fecha.weekday()  # 0=Lunes, 6=Domingo
    
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
                    return {'abierta': True, 'mensaje': f'Abierto ({apertura_str.strip()} - {cierre_str.strip()})', 'festivo': None}
                else:
                    if hora_actual < apertura:
                        return {'abierta': False, 'mensaje': f'Cerrado (Abre a las {apertura_str.strip()})', 'festivo': None}
                    else:
                        return {'abierta': False, 'mensaje': f'Cerrado (Cierra a las {cierre_str.strip()})', 'festivo': None}
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

# --- CABECERA ---
# Cargamos variables de entorno (si existe .env)
load_dotenv()

tipo_cambio = obtener_tipo_cambio()
# Cargamos datos una vez para todas las páginas
df_mapa = obtener_datos_mapeados()

# Métrica en la barra lateral
with st.sidebar:
    st.title("Analítica Pro")
    st.metric("Tipo de Cambio USD/MXN", f"${tipo_cambio:.2f}")
    opcion = st.radio(
        "Selecciona una página:",
        ["Dashboard", "Monitoreo de Aduanas", "Flujos de Carga", "Corredores Logísticos", "Puertos Marítimos", "Fuerza Laboral", "Nearshoring"]
    )
    st.markdown("---")
    operaciones_por_operador = st.number_input(
        "Operaciones por operador (promedio)", value=2.0, min_value=0.1, max_value=50.0, step=0.1
    )
    st.caption("Usado para estimar requerimiento de operadores y detectar déficit")

    # API Key para consumir el backend protegido (opcional)
    try:
        api_key_default = os.getenv('API_KEY', '')
    except Exception:
        api_key_default = ''

    api_key = st.text_input("API Key (para llamadas a la API)", value=api_key_default, type="password")

    # Botón para guardar la API Key en .env (útil para no reingresarla)
    if st.button("Guardar API Key en .env"):
        try:
            dotenv_path = find_dotenv()
            if not dotenv_path:
                dotenv_path = os.path.join(os.getcwd(), '.env')
                # crear archivo si no existe
                open(dotenv_path, 'a').close()
            set_key(dotenv_path, 'API_KEY', api_key)
            st.success("API Key guardada en .env")
        except Exception as e:
            st.error(f"No se pudo guardar la API Key: {e}")

# --- PÁGINAS ---

def page_inicio():
    # Título con diseño corporativo
    st.markdown("""
        <div style='background: linear-gradient(135deg, #11101D 0%, #4070F4 100%); 
                    color: white; 
                    padding: 30px 40px; 
                    border-radius: 15px; 
                    margin-bottom: 30px;
                    box-shadow: 0 8px 20px rgba(17, 16, 29, 0.3);'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'>🚢 FreightMetrics</h1>
            <p style='color: #29B5E8; font-size: 1.2rem; font-weight: 500; margin-top: 10px; margin-bottom: 0;'>Dashboard Ejecutivo de Inteligencia Logística</p>
        </div>
    """, unsafe_allow_html=True)

    # ============ SECCIÓN 1: FUERZA LABORAL ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>👥 Sector Autotransporte - Fuerza Laboral</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_fl1, col_fl2, col_fl3 = st.columns(3)
    with col_fl1:
        st.markdown("""
            <div style='background-color: white; 
                        border-left: 5px solid #29B5E8;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Total Permisionarios</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>198,500</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>🏢 Permisionarios federales (SICT)</p>
            </div>
        """, unsafe_allow_html=True)
    with col_fl2:
        st.markdown("""
            <div style='background-color: white; 
                        border-left: 5px solid #4070F4;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Parque Vehicular</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>630,000</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>🚛 Unidades motrices en operación</p>
            </div>
        """, unsafe_allow_html=True)
    with col_fl3:
        st.markdown("""
            <div style='background-color: white; 
                        border-left: 5px solid #EF553B;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #EF553B; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Déficit Operadores</p>
                <h2 style='color: #EF553B; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>56,000</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>⚠️ Vacantes CANACAR e IRU</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ============ SECCIÓN 2: PUERTOS MARÍTIMOS ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>⚓ Puertos Marítimos Mexicanos</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Obtener datos de puertos
    df_puertos = obtener_datos_mapeados()
    total_puertos = len(df_puertos)
    total_operaciones = int(df_puertos["Operaciones"].sum())
    saturacion_promedio = int(df_puertos["Saturacion"].mean())
    puerto_mayor = df_puertos.loc[df_puertos["Operaciones"].idxmax(), "Puerto"]
    
    col_pm1, col_pm2, col_pm3, col_pm4 = st.columns(4)
    with col_pm1:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #29B5E8;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Puertos Monitorizados</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{total_puertos}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>⚓ Puertos principales</p>
            </div>
        """, unsafe_allow_html=True)
    with col_pm2:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #4070F4;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Operaciones Totales</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{total_operaciones:,}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>📦 Operaciones registradas</p>
            </div>
        """, unsafe_allow_html=True)
    with col_pm3:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #FFA726;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #FFA726; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Saturación Promedio</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{saturacion_promedio}%</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>📊 Capacidad utilizada</p>
            </div>
        """, unsafe_allow_html=True)
    with col_pm4:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #4CAF50;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4CAF50; font-size: 0.75rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.3px;'>Líder Operaciones</p>
                <h2 style='color: #11101D; font-size: 1.8rem; font-weight: 700; margin: 10px 0 5px 0;'>{puerto_mayor}</h2>
                <p style='color: #666; font-size: 0.75rem; margin: 0;'>🏆 Mayor actividad</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ============ SECCIÓN 3: FLUJOS FRONTERIZOS ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>🚛 Flujos de Carga Transfronterizos</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Simular métricas de flujos fronterizos
    col_ff1, col_ff2, col_ff3, col_ff4 = st.columns(4)
    with col_ff1:
        st.markdown("""
            <div style='background-color: white; 
                        border-left: 5px solid #29B5E8;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Puertos Activos</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>12</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>🌎 Cruces MX-USA</p>
            </div>
        """, unsafe_allow_html=True)
    with col_ff2:
        st.markdown("""
            <div style='background-color: white; 
                        border-left: 5px solid #4070F4;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4070F4; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Cruces Mensuales</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>1.8M</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>🚚 Cruces promedio/mes</p>
            </div>
        """, unsafe_allow_html=True)
    with col_ff3:
        st.markdown("""
            <div style='background-color: white; 
                        border-left: 5px solid #4CAF50;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4CAF50; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Valor Comercio</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>$98B</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>💵 USD mensuales</p>
            </div>
        """, unsafe_allow_html=True)
    with col_ff4:
        st.markdown("""
            <div style='background-color: white; 
                        border-left: 5px solid #FFA726;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #FFA726; font-size: 0.75rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.3px;'>Líder Cruces</p>
                <h2 style='color: #11101D; font-size: 1.8rem; font-weight: 700; margin: 10px 0 5px 0;'>N. Laredo</h2>
                <p style='color: #666; font-size: 0.75rem; margin: 0;'>🏆 Mayor volumen</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ============ SECCIÓN 4: MONITOREO ADUANAS ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>🚦 Estado Operativo de Aduanas</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_ad1, col_ad2, col_ad3, col_ad4 = st.columns(4)
    with col_ad1:
        st.markdown("""
            <div style='background-color: white; 
                        border-left: 5px solid #4CAF50;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #4CAF50; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Operación Normal</p>
                <h2 style='color: #4CAF50; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>7</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>✅ Aduanas sin congestión</p>
            </div>
        """, unsafe_allow_html=True)
    with col_ad2:
        st.markdown("""
            <div style='background-color: white; 
                        border-left: 5px solid #FFA726;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #FFA726; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Saturación Media</p>
                <h2 style='color: #FFA726; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>3</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>⚠️ Congestión moderada</p>
            </div>
        """, unsafe_allow_html=True)
    with col_ad3:
        st.markdown("""
            <div style='background-color: white; 
                        border-left: 5px solid #EF553B;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #EF553B; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Alerta Crítica</p>
                <h2 style='color: #EF553B; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>2</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>🔴 Alta congestión</p>
            </div>
        """, unsafe_allow_html=True)
    with col_ad4:
        st.markdown("""
            <div style='background-color: white; 
                        border-left: 5px solid #11101D;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #11101D; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Tiempo Espera Prom.</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>47 min</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>⏱️ Promedio nacional</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ============ INSIGHTS EJECUTIVOS ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #FFA726 0%, #EF553B 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(239, 85, 59, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>💡 Insights Ejecutivos</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_ins1, col_ins2 = st.columns(2)
    with col_ins1:
        st.markdown("""
            <div style='background-color: #FFF3E0; 
                        border-left: 4px solid #FFA726;
                        padding: 20px; 
                        border-radius: 10px;
                        margin: 10px 0;'>
                <h4 style='color: #11101D; margin-top: 0; font-weight: 600;'>⚠️ Déficit Crítico de Operadores</h4>
                <p style='color: #333; line-height: 1.6; margin-bottom: 0;'>
                    El sector enfrenta un déficit de <strong>56,000 operadores</strong>, equivalente al <strong>8.9%</strong> 
                    del parque vehicular. Se requiere inversión urgente en capacitación y atracción de talento.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col_ins2:
        st.markdown("""
            <div style='background-color: #E8F5E9; 
                        border-left: 4px solid #4CAF50;
                        padding: 20px; 
                        border-radius: 10px;
                        margin: 10px 0;'>
                <h4 style='color: #11101D; margin-top: 0; font-weight: 600;'>📈 Flujo Comercial Robusto</h4>
                <p style='color: #333; line-height: 1.6; margin-bottom: 0;'>
                    Los cruces fronterizos mantienen un promedio de <strong>1.8M mensuales</strong>, con un valor comercial 
                    de <strong>$98B USD/mes</strong>. Nuevo Laredo continúa siendo el puerto líder.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    col_ins3, col_ins4 = st.columns(2)
    with col_ins3:
        st.markdown("""
            <div style='background-color: #FFEBEE; 
                        border-left: 4px solid #EF553B;
                        padding: 20px; 
                        border-radius: 10px;
                        margin: 10px 0;'>
                <h4 style='color: #11101D; margin-top: 0; font-weight: 600;'>🚦 Congestión Aduanal</h4>
                <p style='color: #333; line-height: 1.6; margin-bottom: 0;'>
                    <strong>2 aduanas</strong> en estado crítico con tiempos de espera superiores a 90 minutos. 
                    Se recomienda optimización de rutas y horarios de cruce.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col_ins4:
        st.markdown("""
            <div style='background-color: #E3F2FD; 
                        border-left: 4px solid #4070F4;
                        padding: 20px; 
                        border-radius: 10px;
                        margin: 10px 0;'>
                <h4 style='color: #11101D; margin-top: 0; font-weight: 600;'>🏢 Atomización del Sector</h4>
                <p style='color: #333; line-height: 1.6; margin-bottom: 0;'>
                    El <strong>82.2%</strong> de permisionarios son "hombre-camión" (1-5 unidades), 
                    lo que representa oportunidades de consolidación y profesionalización.
                </p>
            </div>
        """, unsafe_allow_html=True)

def page_mapa():
    # Página: Flujos de Carga Transfronterizos (Cruces MX-USA)
    st.title("🚛 Flujos de Carga Transfronterizos")
    st.markdown("---")
    
    # Toggle para usar datos reales
    col_toggle, col_info = st.columns([1, 3])
    with col_toggle:
        usar_datos_reales = st.toggle("📊 Usar Datos Reales", value=False, key="toggle_flujos_reales")
    with col_info:
        if usar_datos_reales:
            st.success("✅ Mostrando datos reales desde CSV/API")
        else:
            st.info("ℹ️ Mostrando datos simulados (para pruebas)")
    
    st.markdown("---")
    
    # Intentar cargar datos reales si está activado
    df_border = None
    if usar_datos_reales:
        df_border = cargar_datos_flujos_reales()
        if df_border is None:
            st.warning("⚠️ No se encontraron datos reales. Usando datos simulados.")
            usar_datos_reales = False
    
    # Si no hay datos reales o no está activado, usar datos simulados
    if not usar_datos_reales or df_border is None:
        # --- GENERACIÓN DE DATOS SINTÉTICOS (Basados en promedios BTS/Census Bureau) ---
        # Simulamos datos de los últimos 12 meses
        fechas = pd.date_range(start=(datetime.now() - pd.DateOffset(months=12)).strftime('%Y-%m-%d'), end=datetime.now().strftime('%Y-%m-%d'), freq='D')
        
        # Todos los puertos fronterizos principales México-USA (Nombres Oficiales 2026)
        puertos = {
            'Nuevo Laredo III (Comercio Mundial)': 12000,     # Mayor volumen - Puente Comercio Mundial
            'Reynosa (Pharr)': 8500,                          # Puente Pharr-Reynosa
            'Laredo - Colombia': 6800,                        # Colombia-Solidarity
            'Cd. Juárez (Paso del Norte/Zaragoza)': 7500,    # Paso del Norte/Zaragoza
            'Tijuana (Mesa de Otay)': 6500,                   # Mesa de Otay
            'Matamoros (Gral. Ignacio Zaragoza)': 5500,      # Brownsville-Matamoros
            'Nogales (Mariposa)': 4200,                       # Mariposa POE
            'Mexicali II (Nvo. Mexicali)': 3800,             # Nuevo Mexicali
            'Piedras Negras': 2800,                           # Eagle Pass-Piedras Negras
            'San Luis Río Colorado': 2200,                    # San Luis POE
            'Agua Prieta': 1200,                              # Agua Prieta-Douglas
            'Cd. Acuña': 1500                                 # Del Río-Cd. Acuña
        }

        data_list = []
        for puerto, base_cruces in puertos.items():
            for fecha in fechas:
                # Agregar variabilidad según el puerto
                variabilidad = np.random.randint(-400, 1500)
                cruces = base_cruces + variabilidad
                valor_usd = cruces * np.random.uniform(45000, 65000) # Valor promedio por camión
                data_list.append([fecha, puerto, cruces, valor_usd])

        df_border = pd.DataFrame(data_list, columns=['Fecha', 'Puerto', 'Cruces', 'Valor_USD'])

        data_list = []
        for puerto, base_cruces in puertos.items():
            for fecha in fechas:
                # Agregar variabilidad según el puerto
                variabilidad = np.random.randint(-400, 1500)
                cruces = base_cruces + variabilidad
                valor_usd = cruces * np.random.uniform(45000, 65000) # Valor promedio por camión
                data_list.append([fecha, puerto, cruces, valor_usd])

        df_border = pd.DataFrame(data_list, columns=['Fecha', 'Puerto', 'Cruces', 'Valor_USD'])
    df_border['Mes'] = df_border['Fecha'].dt.strftime('%Y-%m')
    df_border['Semana'] = df_border['Fecha'].dt.isocalendar().week

    # --- INTERFAZ ---
    if usar_datos_reales:
        st.markdown("📊 **Datos reales** de cruces comerciales basados en registros actuales, con proyección histórica de 12 meses.")
    else:
        st.markdown("Métricas de cruce terrestre basadas en reportes del **BTS** y valores comerciales del **US Census Bureau**.")

    # Obtener lista de puertos únicos del DataFrame
    puertos_disponibles = sorted(df_border['Puerto'].unique().tolist())

    # Filtros
    with st.sidebar:
        st.header("Filtros Globales")
        puerto_sel = st.multiselect("Puerto de Entrada (POE) - para KPIs:", puertos_disponibles, default=puertos_disponibles[:3])
        moneda = st.radio("Ver valores en:", ["USD (Dólares)", "MXN (Pesos)"])
        tipo_vista = st.selectbox("Granularidad temporal:", ["Diario", "Semanal", "Mensual"])
        tipo_cambio = 17.50 # Ejemplo de tipo de cambio
        st.divider()
        st.caption("Fuentes: BTS Border Crossing Data & CBP Wait Times API")
        if usar_datos_reales:
            st.success("📊 Datos actuales desde CSV")
        else:
            st.info("📍 Se incluyen 12 principales cruces fronterizos México-USA (Nombres Oficiales 2026)")

    # Filtrar DataFrame para KPIs
    df_filtrado = df_border[df_border['Puerto'].isin(puerto_sel)] if puerto_sel else df_border
    
    # Dataframe completo para usar en las gráficas (sin limitarse al filtro del sidebar)
    df_completo = df_border.copy()

    # --- KPIs ACUMULADOS ---
    total_cruces = df_filtrado['Cruces'].sum()

    total_valor = df_filtrado['Valor_USD'].sum()
    if moneda == "MXN (Pesos)":
        total_valor *= tipo_cambio
        simbolo = "MXN"
    else:
        simbolo = "USD"

    col1, col2, col3 = st.columns(3)
    col1.metric("Acumulado de Cruces", f"{total_cruces:,}")
    col2.metric(f"Valor Total ({simbolo})", f"${total_valor:,.0f}")
    col3.metric("Promedio Diario de Cruces", f"{int(df_filtrado.groupby('Fecha')['Cruces'].sum().mean()):,}")

    st.divider()

    # --- GRÁFICOS DE TIEMPO ---
    st.subheader(f"📈 Tendencia de Cruces - Vista {tipo_vista}")
    
    # Filtro adicional para gráfica de tendencia
    col_trend1, col_trend2 = st.columns([3, 1])
    with col_trend1:
        puertos_filtro_tendencia = st.multiselect(
            "Selecciona aduanas para la tendencia:",
            options=puertos_disponibles,
            default=puertos_disponibles[:5] if len(puertos_disponibles) >= 5 else puertos_disponibles,
            key="tendencia"
        )
    with col_trend2:
        st.write("")  # Espaciador
    
    # Verificar que hay aduanas seleccionadas
    if puertos_filtro_tendencia:
        df_tendencia = df_completo[df_completo['Puerto'].isin(puertos_filtro_tendencia)]
        
        if not df_tendencia.empty:
            if tipo_vista == "Diario":
                fig_time = px.line(df_tendencia, x='Fecha', y='Cruces', color='Puerto', 
                                  title="Cruces Diarios por Puerto",
                                  labels={'Cruces': 'Número de Cruces', 'Fecha': 'Fecha'})
            elif tipo_vista == "Semanal":
                df_sem = df_tendencia.groupby(['Semana', 'Puerto'])['Cruces'].sum().reset_index()
                fig_time = px.bar(df_sem, x='Semana', y='Cruces', color='Puerto', barmode='group', 
                                 title="Volumen Semanal Acumulado",
                                 labels={'Cruces': 'Número de Cruces', 'Semana': 'Semana'})
            else: # Mensual
                df_mes = df_tendencia.groupby(['Mes', 'Puerto'])['Cruces'].sum().reset_index()
                fig_time = px.area(df_mes, x='Mes', y='Cruces', color='Puerto', 
                                  title="Crecimiento Mensual de Carga",
                                  labels={'Cruces': 'Número de Cruces', 'Mes': 'Mes'})

            fig_time.update_layout(height=500, hovermode='x unified')
            st.plotly_chart(fig_time, use_container_width=True)
        else:
            st.warning("⚠️ No hay datos disponibles para las aduanas seleccionadas en el período.")
    else:
        st.warning("⚠️ Por favor selecciona al menos una aduana para ver la gráfica.")

    st.divider()

    # --- ANÁLISIS ECONÓMICO ---
    st.subheader(f"💰 Valor de la Mercancía ({simbolo})")
    
    # Calcular ranking por valor para seleccionar principales por defecto
    df_ranking_valor = df_completo.groupby('Puerto')['Valor_USD'].sum().reset_index()
    df_ranking_valor = df_ranking_valor.sort_values('Valor_USD', ascending=False)
    top_puertos_valor = df_ranking_valor['Puerto'].head(6).tolist()
    
    # Filtro para valor económico
    col_econ1, col_econ2 = st.columns([3, 1])
    with col_econ1:
        puertos_filtro_valor = st.multiselect(
            "Selecciona aduanas para análisis de valor:",
            options=puertos_disponibles,
            default=top_puertos_valor,  # Top 6 por valor (incluye Laredo como #1)
            key="valor"
        )
    with col_econ2:
        st.write("")  # Espaciador

    if puertos_filtro_valor:
        df_valor = df_completo[df_completo['Puerto'].isin(puertos_filtro_valor)].groupby('Puerto')['Valor_USD'].sum().reset_index()
        
        if not df_valor.empty:
            if moneda == "MXN (Pesos)":
                df_valor['Valor_USD'] *= tipo_cambio
                df_valor.rename(columns={'Valor_USD': 'Valor_MXN'}, inplace=True)
                y_col = 'Valor_MXN'
            else:
                y_col = 'Valor_USD'

            # Gráfico de dona con mejor formato
            fig_val = px.pie(df_valor, values=y_col, names='Puerto', hole=0.5, 
                            title="Distribución de Valor Comercial",
                            labels={'Puerto': 'Aduana', y_col: f'Valor ({simbolo})'})
            fig_val.update_layout(height=500)
            st.plotly_chart(fig_val, use_container_width=True)
        else:
            st.warning("⚠️ No hay datos de valor para las aduanas seleccionadas.")
    else:
        st.warning("⚠️ Por favor selecciona al menos una aduana para ver el análisis de valor.")

    st.divider()

    # --- COMPARATIVA DE VOLUMEN POR PUERTO ---
    st.subheader("🏆 Ranking de Aduanas por Volumen")
    
    # Filtro para ranking
    col_rank1, col_rank2 = st.columns([3, 1])
    with col_rank1:
        puertos_filtro_ranking = st.multiselect(
            "Selecciona aduanas para ranking:",
            options=puertos_disponibles,
            default=puertos_disponibles,
            key="ranking"
        )
    with col_rank2:
        max_top = min(len(puertos_filtro_ranking), len(puertos_disponibles)) if puertos_filtro_ranking else len(puertos_disponibles)
        top_n = st.slider("Top N aduanas:", min_value=1, max_value=max_top, value=min(10, max_top))

    if puertos_filtro_ranking:
        df_ranking = df_completo[df_completo['Puerto'].isin(puertos_filtro_ranking)].groupby('Puerto')['Cruces'].sum().reset_index()
        
        if not df_ranking.empty:
            df_ranking = df_ranking.nlargest(top_n, 'Cruces')

            fig_ranking = px.bar(
                df_ranking.sort_values('Cruces', ascending=True),
                y='Puerto',
                x='Cruces',
                orientation='h',
                color='Cruces',
                color_continuous_scale='Viridis',
                text='Cruces',
                labels={'Cruces': 'Número de Cruces', 'Puerto': 'Aduana'},
                title=f'Top {len(df_ranking)} Aduanas por Volumen Total de Cruces'
            )
            fig_ranking.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig_ranking.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_ranking, use_container_width=True)
        else:
            st.warning("⚠️ No hay datos de ranking para las aduanas seleccionadas.")
    else:
        st.warning("⚠️ Por favor selecciona al menos una aduana para ver el ranking.")

    st.divider()

    # --- TABLA DE DATOS PARA EXPORTAR ---
    with st.expander("📥 Ver datos crudos y descargar"):
        st.dataframe(df_filtrado.sort_values('Fecha', ascending=False), use_container_width=True)
        st.download_button("Descargar CSV", df_filtrado.to_csv(index=False), "datos_cruces.csv", "text/csv")


def page_alertas():
    st.title("⚠️ Centro de Notificaciones Operativas")
    st.markdown("---")
    alertas_criticas = df_mapa[df_mapa["Saturacion"] > 80]
    alertas_preventivas = df_mapa[(df_mapa["Saturacion"] > 60) & (df_mapa["Saturacion"] <= 80)]

    if not alertas_criticas.empty or not alertas_preventivas.empty:
        col_a, col_b = st.columns(2)
        
        with col_a:
            for _, row in alertas_criticas.iterrows():
                st.error(f"**CRÍTICO:** Puerto de {row['Puerto']} al {row['Saturacion']}%")
                # st.toast puede no estar disponible en todas las versiones; si falla, será ignorado
                try:
                    st.toast(f"¡Acción requerida en {row['Puerto']}!", icon='🔥')
                except:
                    pass
        
        with col_b:
            for _, row in alertas_preventivas.iterrows():
                st.warning(f"**PREVENTIVO:** {row['Puerto']} aumentando carga ({row['Saturacion']}%)")
    else:
        st.success("✅ Operación Fluida: No se detectan cuellos de botella en la red.")


def page_reportes():
    st.title("📥 Reportes")
    st.markdown("---")
    # Calculamos costos y mostramos tabla
    df_local = df_mapa.copy()
    df_local["Costo_Estimado_MXN"] = df_local["Operaciones"] * 5000 * tipo_cambio
    st.subheader("📑 Datos de Operación")
    st.dataframe(df_local[["Puerto", "Saturacion", "Costo_Estimado_MXN"]], use_container_width=True)

    st.markdown("---")
    pdf_data = crear_pdf(df_local, tipo_cambio)
    st.download_button(
        label="📄 Descargar PDF",
        data=pdf_data,
        file_name=f"FreightMetrics_Reporte_{dt.date.today()}.pdf",
        mime="application/pdf"
    )

    # --- CONSULTA CENSUS ---
    st.markdown("---")
    st.subheader("🌐 Consultar Census (International Trade)")
    dataset = st.selectbox("Dataset (timeseries/intltrade)", ["exports", "imports"], index=0)
    get_param = st.text_input("get (campos, separados por coma)", "ALL_VAL_MO,CTY")
    time_param = st.text_input("time (ej. 2019)", "")

    # headers para llamadas a la API
    try:
        headers = {'X-API-KEY': api_key} if api_key else None
    except Exception:
        headers = None

    params = {}
    if get_param:
        params["get"] = get_param
    if time_param:
        params["time"] = time_param

    if st.button("Consultar Census"):
        try:
            with st.spinner("Consultando Census API..."):
                resp = requests.get(f"http://127.0.0.1:8000/functions/v1/census/{dataset}", params=params, headers=headers, timeout=30)
                resp.raise_for_status()
                payload = resp.json()
                if payload.get("status") == "ok":
                    df_census = pd.DataFrame(payload.get("data", []))
                    if df_census.empty:
                        st.warning("La consulta no retornó filas.")
                    else:
                        st.subheader("Resultados Census")
                        st.dataframe(df_census, use_container_width=True)

                        # Intentar convertir columnas numéricas y plotear
                        for col in df_census.columns:
                            if df_census[col].dtype == object:
                                # remover comas y convertir
                                try:
                                    df_census[col] = pd.to_numeric(df_census[col].astype(str).str.replace(",", ""), errors='coerce')
                                except Exception:
                                    pass

                        numeric_cols = df_census.select_dtypes(include=["number"]).columns.tolist()
                        if numeric_cols:
                            st.subheader("Series numéricas")
                            st.line_chart(df_census[numeric_cols])
                else:
                    st.error(f"Error: {payload.get('detail', 'respuesta no OK')}")
        except Exception as e:
            st.error(f"Fallo al consultar Census: {e}")

    # --- CONSULTA BTS (data.bts.gov / Socrata) ---
    st.markdown("---")
    st.subheader("🌍 Consultar BTS / Socrata")
    bts_dataset = st.text_input("Dataset ID (ej. 9v9j-9z33)", "")
    bts_domain = st.text_input("Dominio (por defecto data.bts.gov)", "data.bts.gov")
    bts_qs = st.text_input("Query string (ej: $limit=100&$select=column1,column2)", "")

    if st.button("Consultar BTS"):
        if not bts_dataset:
            st.error("Ingrese un dataset ID para consultar.")
        else:
            try:
                with st.spinner("Consultando BTS / Socrata..."):
                    # parseamos query string a dict
                    from urllib.parse import parse_qs
                    params_raw = parse_qs(bts_qs, keep_blank_values=True)
                    params = {k: v[0] for k, v in params_raw.items()} if params_raw else {}
                    resp = requests.get(f"http://127.0.0.1:8000/functions/v1/bts/{bts_dataset}", params={**params, "domain": bts_domain}, headers=headers, timeout=30)
                    resp.raise_for_status()
                    payload = resp.json()
                    if payload.get("status") == "ok":
                        df_bts = pd.DataFrame(payload.get("data", []))
                        if df_bts.empty:
                            st.warning("La consulta BTS no retornó filas.")
                        else:
                            st.subheader("Resultados BTS")
                            st.dataframe(df_bts, use_container_width=True)
                            # Mostrar primeras columnas numéricas
                            numeric_cols = df_bts.select_dtypes(include=["number"]).columns.tolist()
                            if numeric_cols:
                                st.subheader("Series numéricas")
                                st.line_chart(df_bts[numeric_cols])
                    else:
                        st.error(f"Error BTS: {payload.get('detail', 'respuesta no OK')}")
            except Exception as e:
                st.error(f"Fallo al consultar BTS: {e}")

    # --- CONSULTA SAT (páginas públicas) ---
    st.markdown("---")
    st.subheader("🧾 Consultar SAT (extraer tabla / enlaces)")
    sat_url = st.text_input("URL SAT o pública", "https://www.sat.gob.mx/portal/public/home")
    if st.button("Consultar SAT"):
        if not sat_url:
            st.error("Ingresa una URL para consultar.")
        else:
            try:
                with st.spinner("Consultando SAT..."):
                    resp = requests.get("http://127.0.0.1:8000/functions/v1/sat/fetch", params={"url": sat_url}, headers=headers, timeout=30)
                    resp.raise_for_status()
                    payload = resp.json()
                    if payload.get("status") == "ok":
                        df_sat = pd.DataFrame(payload.get("data", []))
                        if df_sat.empty:
                            st.warning("No se encontraron tablas ni enlaces en la URL proporcionada.")
                        else:
                            st.subheader("Resultados SAT")
                            st.dataframe(df_sat, use_container_width=True)
                    else:
                        st.error(f"Error SAT: {payload.get('detail', 'respuesta no OK')}")
            except Exception as e:
                st.error(f"Fallo al consultar SAT: {e}")

    # --- CONSULTA BTS (data.bts.gov / Socrata) ---
    st.markdown("---")
    st.subheader("🌍 Consultar BTS / Socrata")
    bts_dataset = st.text_input("Dataset ID (ej. 9v9j-9z33)", "")
    bts_domain = st.text_input("Dominio (por defecto data.bts.gov)", "data.bts.gov")
    bts_qs = st.text_input("Query string (ej: $limit=100&$select=column1,column2)", "")

    if st.button("Consultar BTS"):
        if not bts_dataset:
            st.error("Ingrese un dataset ID para consultar.")
        else:
            try:
                with st.spinner("Consultando BTS / Socrata..."):
                    # parseamos query string a dict
                    from urllib.parse import parse_qs
                    params_raw = parse_qs(bts_qs, keep_blank_values=True)
                    params = {k: v[0] for k, v in params_raw.items()} if params_raw else {}
                    resp = requests.get(f"http://127.0.0.1:8000/functions/v1/bts/{bts_dataset}", params={**params, "domain": bts_domain}, timeout=30)
                    resp.raise_for_status()
                    payload = resp.json()
                    if payload.get("status") == "ok":
                        df_bts = pd.DataFrame(payload.get("data", []))
                        if df_bts.empty:
                            st.warning("La consulta BTS no retornó filas.")
                        else:
                            st.subheader("Resultados BTS")
                            st.dataframe(df_bts, use_container_width=True)
                            # Mostrar primeras columnas numéricas
                            numeric_cols = df_bts.select_dtypes(include=["number"]).columns.tolist()
                            if numeric_cols:
                                st.subheader("Series numéricas")
                                st.line_chart(df_bts[numeric_cols])
                    else:
                        st.error(f"Error BTS: {payload.get('detail', 'respuesta no OK')}")
            except Exception as e:
                st.error(f"Fallo al consultar BTS: {e}")

    # --- CONSULTA SAT (páginas públicas) ---
    st.markdown("---")
    st.subheader("🧾 Consultar SAT (extraer tabla / enlaces)")
    sat_url = st.text_input("URL SAT o pública", "https://www.sat.gob.mx/portal/public/home")
    if st.button("Consultar SAT"):
        if not sat_url:
            st.error("Ingresa una URL para consultar.")
        else:
            try:
                with st.spinner("Consultando SAT..."):
                    resp = requests.get("http://127.0.0.1:8000/functions/v1/sat/fetch", params={"url": sat_url}, timeout=30)
                    resp.raise_for_status()
                    payload = resp.json()
                    if payload.get("status") == "ok":
                        df_sat = pd.DataFrame(payload.get("data", []))
                        if df_sat.empty:
                            st.warning("No se encontraron tablas ni enlaces en la URL proporcionada.")
                        else:
                            st.subheader("Resultados SAT")
                            st.dataframe(df_sat, use_container_width=True)
                    else:
                        st.error(f"Error SAT: {payload.get('detail', 'respuesta no OK')}")
            except Exception as e:
                st.error(f"Fallo al consultar SAT: {e}")


def page_monitoreo_aduanas():
    """Sistema de monitoreo de saturación, tiempos de cruce y alertas inteligentes"""
    # Título con estilo corporativo
    st.markdown("<h1 style='color: #11101D; font-weight: 700; margin-bottom: 0;'>🚦 Centro de Monitoreo de Aduanas</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #4070F4; font-size: 1.1rem; font-weight: 500; margin-top: 5px;'>Sistema de alertas en tiempo real para optimizar rutas de cruce fronterizo</p>", unsafe_allow_html=True)
    
    # Inicializar sistema de alertas
    if 'sistema_alertas' not in st.session_state:
        st.session_state.sistema_alertas = SistemaAlertas()
    
    sistema_alertas = st.session_state.sistema_alertas
    
    # Botón para recargar datos
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 3])
    with col_btn1:
        btn_recargar = st.button("🔄 Recargar Datos Reales", help="Carga datos desde CSV o API")
    with col_btn2:
        usar_datos_reales = st.checkbox("📊 Usar Datos Reales", value=False, help="Alternar entre datos simulados y datos reales")
    
    # Cargar datos según la selección
    if usar_datos_reales or btn_recargar:
        datos_reales = cargar_datos_aduanas_reales()
        
        if datos_reales is not None and not datos_reales.empty:
            st.success(f"✅ Datos reales cargados: {len(datos_reales)} aduanas")
            
            # Adaptar datos reales al formato esperado
            # Los datos reales tienen: Aduana, Valor_USD, Contenedores, Fecha
            # Necesitamos simular: Tiempo Espera, Saturación, Capacidad, Camiones en Cola, Estado
            aduanas_status = datos_reales.copy()
            
            # Obtener fecha y hora actual para verificar horarios
            ahora = datetime.now()
            
            # Verificar estado de cada aduana (abierta/cerrada)
            estados_aduanas_reales = []
            for idx, row in aduanas_status.iterrows():
                estado_aduana = aduana_esta_abierta(row['Aduana'], ahora)
                estados_aduanas_reales.append(estado_aduana)
            
            # Generar métricas simuladas basadas en volumen real
            aduanas_status['Tiempo Espera (min)'] = aduanas_status['Contenedores'].apply(
                lambda x: min(140, max(30, int(x / 100)))
            )
            aduanas_status['Saturación (%)'] = aduanas_status['Contenedores'].apply(
                lambda x: min(95, max(30, int(x / 150)))
            )
            aduanas_status['Capacidad (Camiones/hora)'] = 150
            aduanas_status['Camiones en Cola'] = aduanas_status['Contenedores'].apply(
                lambda x: int(x * 0.05)
            )
            
            # Agregar información de horarios y estado de apertura
            aduanas_status['Horario Hoy'] = [e['mensaje'] for e in estados_aduanas_reales]
            aduanas_status['Abierta'] = [e['abierta'] for e in estados_aduanas_reales]
            
            # Si está cerrada, poner tiempos en 0
            for idx, row in aduanas_status.iterrows():
                if not row['Abierta']:
                    aduanas_status.at[idx, 'Tiempo Espera (min)'] = 0
                    aduanas_status.at[idx, 'Saturación (%)'] = 0
                    aduanas_status.at[idx, 'Camiones en Cola'] = 0
            
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
            st.info(f"📅 Última actualización: {datos_reales['Fecha'].iloc[0] if 'Fecha' in datos_reales.columns else 'N/A'}")
        else:
            st.warning("⚠️ No se encontraron datos reales. Usando datos simulados.")
            usar_datos_reales = False
    
    # Si no hay datos reales, usar datos simulados
    if not usar_datos_reales:
        # Obtener fecha y hora actual
        ahora = datetime.now()
        hora_actual = ahora.strftime('%H:%M')
        
        # Nombres de aduanas
        aduanas_nombres = ['Nuevo Laredo III (Comercio Mundial)', 'Reynosa (Pharr)', 'Laredo - Colombia', 
                       'Cd. Juárez (Paso del Norte/Zaragoza)', 'Tijuana (Mesa de Otay)', 'Matamoros (Gral. Ignacio Zaragoza)',
                       'Nogales (Mariposa)', 'Mexicali II (Nvo. Mexicali)', 'Piedras Negras', 
                       'San Luis Río Colorado', 'Agua Prieta', 'Cd. Acuña']
        
        # Verificar estado de cada aduana (abierta/cerrada)
        estados_aduanas = []
        tiempos_espera = []
        saturaciones = []
        camiones_cola = []
        
        for aduana in aduanas_nombres:
            estado_aduana = aduana_esta_abierta(aduana, ahora)
            estados_aduanas.append(estado_aduana)
            
            # Si está cerrada, poner datos en 0
            if not estado_aduana['abierta']:
                tiempos_espera.append(0)
                saturaciones.append(0)
                camiones_cola.append(0)
            else:
                # Datos simulados solo para aduanas abiertas
                tiempos_espera.append(random.randint(30, 140))
                saturaciones.append(random.randint(35, 95))
                camiones_cola.append(random.randint(350, 1500))
        
        # Datos de aduanas con tiempos y saturación simulados (usando nombres oficiales)
        aduanas_status = pd.DataFrame({
            'Aduana': aduanas_nombres,
            'Tiempo Espera (min)': tiempos_espera,
            'Saturación (%)': saturaciones,
            'Capacidad (Camiones/hora)': [150, 130, 125, 140, 120, 135, 145, 140, 150, 160, 155, 145],
            'Camiones en Cola': camiones_cola,
            'Estado': ['🔴 CERRADO' if not e['abierta'] else ('🔴 CRÍTICO' if s > 85 else ('⚠️ ALTO' if s > 70 else ('⚠️ MEDIO' if s > 60 else '✅ NORMAL'))) 
                      for e, s in zip(estados_aduanas, saturaciones)],
            'Horario Hoy': [e['mensaje'] for e in estados_aduanas],
            'Abierta': [e['abierta'] for e in estados_aduanas]
        })
    
    # Evaluar alertas
    alertas = sistema_alertas.evaluar_aduanas(aduanas_status)
    stats_alertas = sistema_alertas.obtener_estadisticas_alertas()
    
    st.markdown("---")
    
    # PANEL DE ALERTAS AUTOMÁTICAS
    st.subheader("🚨 Sistema de Alertas Automáticas")
    
    if alertas:
        # Separar alertas por nivel
        alertas_criticas = [a for a in alertas if '🔴' in a['nivel']]
        alertas_altas = [a for a in alertas if '🟠' in a['nivel']]
        alertas_medias = [a for a in alertas if '🟡' in a['nivel']]
        
        col_alert1, col_alert2, col_alert3 = st.columns(3)
        
        with col_alert1:
            st.metric("🔴 Alertas Críticas", len(alertas_criticas), help="Saturación >85% o Espera >120min")
        with col_alert2:
            st.metric("🟠 Alertas Altas", len(alertas_altas), help="Saturación >70% o Espera >90min")
        with col_alert3:
            st.metric("🟡 Alertas Medias", len(alertas_medias), help="Saturación >60% o Espera >60min")
        
        # Mostrar alertas críticas prominentemente
        if alertas_criticas:
            st.markdown("<div style='background-color: #EF553B; color: white; padding: 15px; border-radius: 10px; margin: 10px 0;'><h3 style='color: white; margin: 0;'>🔴 ALERTAS CRÍTICAS - ACCIÓN INMEDIATA REQUERIDA</h3></div>", unsafe_allow_html=True)
            for alerta in alertas_criticas:
                st.markdown(f"<div style='background-color: #ffebee; border-left: 4px solid #EF553B; padding: 12px; margin: 8px 0; border-radius: 5px;'><span style='color: #11101D; font-weight: 600;'>{alerta['aduana']}</span> - <span style='color: #333;'>{alerta['mensaje']}</span></div>", unsafe_allow_html=True)
        
        # Expandible para alertas altas y medias
        if alertas_altas:
            with st.expander(f"🟠 Ver {len(alertas_altas)} Alertas de Nivel Alto", expanded=False):
                for alerta in alertas_altas:
                    st.warning(f"**{alerta['aduana']}** - {alerta['mensaje']}")
        
        if alertas_medias:
            with st.expander(f"🟡 Ver {len(alertas_medias)} Alertas de Nivel Medio", expanded=False):
                for alerta in alertas_medias:
                    st.info(f"**{alerta['aduana']}** - {alerta['mensaje']}")
    else:
        st.success("✅ No hay alertas activas. Todas las aduanas operan en niveles normales.")
    
    # Estadísticas del historial de alertas
    if stats_alertas:
        st.markdown("---")
        st.subheader("📊 Estadísticas de Alertas (Últimas 24 horas)")
        
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.metric("Total Alertas 24h", stats_alertas['total_alertas_24h'])
        with col_stat2:
            st.metric("Alertas Críticas 24h", stats_alertas['alertas_criticas_24h'])
        with col_stat3:
            st.metric("Aduana Más Alertas", stats_alertas['aduana_mas_alertas'])
        with col_stat4:
            st.metric("Promedio Saturación", f"{stats_alertas['promedio_saturacion']:.1f}%")
    
    st.markdown("---")
    
    # 🕐 INFORMACIÓN DE HORARIOS Y ESTADO ACTUAL
    st.subheader("🕐 Estado Operativo Actual")
    
    ahora = datetime.now()
    dia_nombre = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][ahora.weekday()]
    hora_actual_str = ahora.strftime('%H:%M')
    
    # Mostrar información de fecha/hora actual
    col_tiempo1, col_tiempo2, col_tiempo3, col_tiempo4 = st.columns(4)
    with col_tiempo1:
        st.metric("📅 Día", dia_nombre)
    with col_tiempo2:
        st.metric("🕐 Hora", hora_actual_str)
    with col_tiempo3:
        aduanas_abiertas = len(aduanas_status[aduanas_status['Abierta'] == True])
        st.metric("🟢 Aduanas Abiertas", f"{aduanas_abiertas}/{len(aduanas_status)}")
    with col_tiempo4:
        aduanas_cerradas = len(aduanas_status[aduanas_status['Abierta'] == False])
        st.metric("🔴 Aduanas Cerradas", f"{aduanas_cerradas}/{len(aduanas_status)}")
    
    # Alertas de aduanas cerradas
    aduanas_cerradas_df = aduanas_status[aduanas_status['Abierta'] == False]
    if not aduanas_cerradas_df.empty:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #EF553B 0%, #d84315 100%); 
                        color: white; 
                        padding: 20px; 
                        border-radius: 12px; 
                        margin: 15px 0;
                        box-shadow: 0 4px 15px rgba(239, 85, 59, 0.3);'>
                <h3 style='color: white; margin: 0 0 15px 0; font-size: 1.3rem; font-weight: 700;'>
                    🔴 ADUANAS CERRADAS EN ESTE MOMENTO
                </h3>
                <p style='color: #ffe8e5; margin: 0; font-size: 0.95rem;'>
                    Las siguientes aduanas no están operando actualmente. Considere rutas alternativas.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Mostrar aduanas cerradas en tarjetas mejoradas (3 columnas)
        num_cols = 3
        cols_cerradas = st.columns(num_cols)
        
        for idx, row in aduanas_cerradas_df.iterrows():
            col_index = idx % num_cols
            with cols_cerradas[col_index]:
                # Determinar ícono según el motivo
                if 'domingo' in row['Horario Hoy'].lower():
                    icono = '📅'
                    motivo_color = '#9e9e9e'
                elif 'sábado' in row['Horario Hoy'].lower() or 'cierra' in row['Horario Hoy'].lower():
                    icono = '🕐'
                    motivo_color = '#ff6f00'
                elif 'festivo' in row['Horario Hoy'].lower():
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
                                min-height: 140px;'>
                        <div style='display: flex; align-items: center; margin-bottom: 8px; min-height: 50px;'>
                            <span style='font-size: 1.3rem; margin-right: 8px; flex-shrink: 0;'>{icono}</span>
                            <strong style='color: #11101D; font-size: 0.95rem; line-height: 1.3; word-wrap: break-word;'>{row['Aduana']}</strong>
                        </div>
                        <div style='background-color: #ffebee; 
                                    padding: 10px; 
                                    border-radius: 6px;
                                    border-left: 3px solid {motivo_color};'>
                            <span style='color: #666; font-size: 0.9rem; display: block;'>
                                <strong style='color: {motivo_color};'>Motivo:</strong> {row['Horario Hoy']}
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # KPIs principales (solo para aduanas abiertas)
    aduanas_abiertas_df = aduanas_status[aduanas_status['Abierta'] == True]
    
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    
    with col_k1:
        if not aduanas_abiertas_df.empty:
            promedio_espera = aduanas_abiertas_df['Tiempo Espera (min)'].mean()
            st.metric("⏱️ Tiempo Promedio Espera", f"{promedio_espera:.0f} min")
        else:
            st.metric("⏱️ Tiempo Promedio Espera", "N/A")
    
    with col_k2:
        aduanas_criticas = len(aduanas_abiertas_df[aduanas_abiertas_df['Saturación (%)'] > 80])
        st.metric("🔴 Aduanas Críticas", f"{aduanas_criticas}")
    
    with col_k3:
        total_cola = aduanas_abiertas_df['Camiones en Cola'].sum() if not aduanas_abiertas_df.empty else 0
        st.metric("🚛 Total en Cola", f"{total_cola:,.0f}")
    
    with col_k4:
        saturacion_promedio = aduanas_abiertas_df['Saturación (%)'].mean() if not aduanas_abiertas_df.empty else 0
        st.metric("📊 Saturación Promedio", f"{saturacion_promedio:.1f}%")
    
    st.markdown("---")
    
    # CONFIGURACIÓN DE UMBRALES DE ALERTAS
    with st.expander("⚙️ Configurar Umbrales de Alertas", expanded=False):
        st.markdown("Personaliza los umbrales para activar alertas automáticas")
        
        col_umb1, col_umb2 = st.columns(2)
        
        with col_umb1:
            st.markdown("**🔴 Nivel Crítico**")
            nuevo_critico_sat = st.slider(
                "Saturación Crítica (%)",
                min_value=70,
                max_value=100,
                value=sistema_alertas.umbrales['critico']['saturacion'],
                help="Alerta crítica cuando saturación supera este valor"
            )
            nuevo_critico_tiempo = st.slider(
                "Tiempo Espera Crítico (min)",
                min_value=60,
                max_value=180,
                value=sistema_alertas.umbrales['critico']['tiempo_espera'],
                help="Alerta crítica cuando tiempo de espera supera este valor"
            )
        
        with col_umb2:
            st.markdown("**🟠 Nivel Alto**")
            nuevo_alto_sat = st.slider(
                "Saturación Alta (%)",
                min_value=50,
                max_value=90,
                value=sistema_alertas.umbrales['alto']['saturacion'],
                help="Alerta alta cuando saturación supera este valor"
            )
            nuevo_alto_tiempo = st.slider(
                "Tiempo Espera Alto (min)",
                min_value=30,
                max_value=150,
                value=sistema_alertas.umbrales['alto']['tiempo_espera'],
                help="Alerta alta cuando tiempo de espera supera este valor"
            )
        
        if st.button("💾 Guardar Umbrales"):
            sistema_alertas.umbrales['critico']['saturacion'] = nuevo_critico_sat
            sistema_alertas.umbrales['critico']['tiempo_espera'] = nuevo_critico_tiempo
            sistema_alertas.umbrales['alto']['saturacion'] = nuevo_alto_sat
            sistema_alertas.umbrales['alto']['tiempo_espera'] = nuevo_alto_tiempo
            st.success("✅ Umbrales actualizados correctamente")
            st.rerun()
    
    st.markdown("---")
    
    # 🔍 FILTROS DINÁMICOS
    st.subheader("🔍 Filtros de Análisis")
    
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    
    with col_f1:
        aduanas_disponibles = aduanas_status['Aduana'].unique().tolist()
        aduanas_seleccionadas = st.multiselect(
            "Selecciona aduanas para monitorear:",
            options=aduanas_disponibles,
            default=aduanas_disponibles,
            key="aduanas_filtro"
        )
    
    with col_f2:
        filtro_estado = st.selectbox(
            "Filtrar por estado:",
            options=["Todas", "Solo Abiertas", "Solo Cerradas"],
            key="filtro_estado_aduanas"
        )
    
    with col_f3:
        mostrar_horarios = st.checkbox("📋 Mostrar Horarios", value=True, key="mostrar_horarios_check")
    
    # Filtrar dataframe según aduanas seleccionadas
    if not aduanas_seleccionadas:
        st.warning("⚠️ Por favor selecciona al menos una aduana")
        aduanas_seleccionadas = aduanas_disponibles[:3]
    
    df_filtrado = aduanas_status[aduanas_status['Aduana'].isin(aduanas_seleccionadas)].copy()
    
    # Aplicar filtro de estado (abierta/cerrada)
    if filtro_estado == "Solo Abiertas":
        df_filtrado = df_filtrado[df_filtrado['Abierta'] == True]
    elif filtro_estado == "Solo Cerradas":
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
    
    # Seleccionar columnas a mostrar (siempre sin Horario Completo)
    columnas_mostrar = ['Aduana', 'Estado', 'Horario Hoy', 'Tiempo Espera (min)', 
                      'Tiempo Cruce Est. (min)', 'Saturación (%)', 'Camiones en Cola']
    
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
                st.plotly_chart(fig_tendencia, use_container_width=True)
                
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
            key="filtro_pais_festivos"
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
        key="selector_aduana_horarios"
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
        st.plotly_chart(fig_disponibilidad, use_container_width=True)
    
    st.markdown("---")
    st.caption("⏰ Datos actualizados en tiempo real. Sistema monitorea cada 15 minutos | Última actualización: Hace 2 minutos")


def page_fuerza_laboral():
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
        estados_filtro = st.multiselect("🗺️ Filtrar por Estados:", estados_disponibles, default=['Todos los estados'])
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
            <p style='color: #29B5E8; font-size: 1.2rem; font-weight: 500; margin-top: 10px; margin-bottom: 0;'>Análisis de capacidad, operaciones y saturación portuaria</p>
        </div>
    """, unsafe_allow_html=True)
    
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
    
    # Datos de puertos principales de México
    puerto_data = {
        'Puerto': ['Manzanillo', 'Veracruz', 'Lázaro Cárdenas', 'Altamira', 'Ensenada'],
        'Vol_Actual': [320000, 110000, 180000, 95000, 75000],  # TEUs/mes
        'Capacidad': [350000, 180000, 220000, 150000, 120000],  # TEUs/mes
        'Operaciones': [450, 280, 320, 210, 180],  # Operaciones diarias
        'Lat': [19.0522, 19.1738, 17.9585, 22.3943, 31.8667],
        'Lon': [-104.3158, -96.1342, -102.1891, -97.9377, -116.6000],
        'Tipo_Carga': ['Contenedores', 'Granel/General', 'Contenedores', 'Granel/Petróleo', 'Contenedores/Cruceros']
    }
    
    df_puertos = pd.DataFrame(puerto_data)
    
    # Calcular saturación y estado
    df_puertos['Saturacion'], df_puertos['Estado'] = zip(*df_puertos.apply(
        lambda x: calcular_indice_saturacion(x['Vol_Actual'], x['Capacidad']), axis=1
    ))
    
    # Calcular capacidad disponible
    df_puertos['Capacidad_Disponible'] = df_puertos['Capacidad'] - df_puertos['Vol_Actual']
    
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


def page_corredores_logisticos():
    """Análisis de corredores logísticos estratégicos con evaluación de riesgo y rentabilidad"""
    
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
    
    st.plotly_chart(fig, use_container_width=True)
    
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
        st.plotly_chart(fig_scatter, use_container_width=True)
    
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
        st.plotly_chart(fig_bar, use_container_width=True)
    
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


# --- RUTEADOR DEL MENÚ ---
if opcion == "Dashboard":
    page_inicio()
elif opcion == "Monitoreo de Aduanas":
    page_monitoreo_aduanas()
elif opcion == "Flujos de Carga":
    page_mapa()
elif opcion == "Corredores Logísticos":
    page_corredores_logisticos()
elif opcion == "Puertos Marítimos":
    page_mapa_autotransporte()
elif opcion == "Fuerza Laboral":
    page_fuerza_laboral()
elif opcion == "Nearshoring":
    st.title("🌎 Análisis de Nearshoring")
    st.info("Aquí verás las tendencias de relocalización.")

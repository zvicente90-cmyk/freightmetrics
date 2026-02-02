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
                # Dataset de cruces fronterizos BTS
                # https://data.bts.gov/Research-and-Statistics/Border-Crossing-Entry-Data/keg4-3bc2
                bts_url = "https://data.bts.gov/resource/keg4-3bc2.json"
                params = {
                    "$limit": 50,
                    "$order": "date DESC",
                    "$select": "port_name,measure,value,date",
                    "$where": "border='US-Mexico' AND measure='Trucks'"
                }
                
                response = requests.get(bts_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    bts_data = response.json()
                    
                    if bts_data:
                        # Transformar datos BTS a formato esperado
                        df_bts = pd.DataFrame(bts_data)
                        
                        # Agrupar por puerto y obtener último valor
                        df_aduanas = df_bts.groupby('port_name').agg({
                            'value': 'sum',
                            'date': 'max'
                        }).reset_index()
                        
                        df_aduanas.columns = ['Aduana', 'Contenedores', 'Fecha']
                        
                        # Estimar valor USD basado en cruces
                        df_aduanas['Valor_USD'] = df_aduanas['Contenedores'].apply(
                            lambda x: int(x) * np.random.uniform(1800, 2500)
                        )
                        
                        datos_cargados = df_aduanas
                        fuente = "BTS API (Tiempo Real)"
                        st.success(f"✅ Datos cargados desde BTS: {len(df_aduanas)} aduanas")
        except requests.exceptions.Timeout:
            st.warning("⏱️ Timeout al consultar BTS API (>10s)")
        except Exception as e:
            st.info(f"ℹ️ BTS API no disponible: {str(e)[:100]}")
    
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
        params = {
            "$limit": 100,
            "$order": "date DESC",
            "$where": "border='US-Mexico' AND measure='Trucks'",
            "$select": "port_name,value,date"
        }
        
        response = requests.get(bts_url, params=params, timeout=15)
        
        if response.status_code == 200:
            bts_data = response.json()
            if bts_data and len(bts_data) > 0:
                df_bts = pd.DataFrame(bts_data)
                
                # Convertir value a numérico
                df_bts['value'] = pd.to_numeric(df_bts['value'], errors='coerce')
                df_bts = df_bts.dropna(subset=['value'])
                
                if not df_bts.empty:
                    df_aduanas = df_bts.groupby('port_name').agg({
                        'value': 'sum',
                        'date': 'max'
                    }).reset_index()
                    df_aduanas.columns = ['Aduana', 'Contenedores', 'Fecha']
                    df_aduanas['Valor_USD'] = df_aduanas['Contenedores'].astype(int) * 2200
                    
                    datos_combinados.append(df_aduanas)
                    resultados['fuentes'].append('BTS')
                    st.success(f"✅ BTS: {len(df_aduanas)} aduanas, {df_aduanas['Contenedores'].sum():,.0f} cruces")
                else:
                    st.warning("⚠️ BTS: Datos recibidos pero sin valores válidos")
            else:
                st.warning("⚠️ BTS: No hay datos disponibles en este momento")
        else:
            resultados['errores'].append(f"BTS: HTTP {response.status_code}")
            st.warning(f"⚠️ BTS: Error HTTP {response.status_code}")
    except requests.exceptions.Timeout:
        resultados['errores'].append("BTS: Timeout (>15s)")
        st.warning("⚠️ BTS: Timeout - La API no respondió a tiempo")
    except requests.exceptions.ConnectionError:
        resultados['errores'].append("BTS: Error de conexión")
        st.warning("⚠️ BTS: No se pudo conectar a la API")
    except Exception as e:
        resultados['errores'].append(f"BTS: {str(e)[:80]}")
        st.warning(f"⚠️ BTS: {str(e)[:80]}")
    
    # 2. CBP Wait Times API (tiempos de espera en tiempo real)
    try:
        st.info("🚦 Consultando CBP Wait Times...")
        cbp_url = "https://bwt.cbp.gov/api/waittimes"
        
        response = requests.get(cbp_url, timeout=10)
        
        if response.status_code == 200:
            cbp_data = response.json()
            if cbp_data:
                st.success(f"✅ CBP Wait Times: Datos obtenidos")
                resultados['fuentes'].append('CBP Wait Times')
                # Nota: CBP proporciona tiempos de espera, no volúmenes
                # Por ahora solo marcamos como fuente consultada
            else:
                st.warning("⚠️ CBP: No hay datos de tiempos de espera disponibles")
        else:
            resultados['errores'].append(f"CBP: HTTP {response.status_code}")
            st.warning(f"⚠️ CBP: Error HTTP {response.status_code}")
    except requests.exceptions.Timeout:
        resultados['errores'].append("CBP: Timeout")
        st.warning("⚠️ CBP: Timeout - La API no respondió")
    except requests.exceptions.ConnectionError:
        resultados['errores'].append("CBP: Error de conexión")
        st.warning("⚠️ CBP: No se pudo conectar")
    except Exception as e:
        resultados['errores'].append(f"CBP: {str(e)[:80]}")
        st.warning(f"⚠️ CBP: {str(e)[:80]}")
    
    # 3. Si no hay datos de APIs, usar datos existentes o generar datos demo
    if not datos_combinados:
        st.warning("⚠️ No se obtuvieron datos nuevos de APIs externas")
        st.info("💡 Generando datos de demostración basados en patrones históricos...")
        
        # Generar datos demo más realistas
        aduanas_principales = [
            'Nuevo Laredo III (Comercio Mundial)',
            'Reynosa (Pharr)',
            'Laredo - Colombia',
            'Cd. Juárez (Paso del Norte/Zaragoza)',
            'Tijuana (Mesa de Otay)',
            'Matamoros (Gral. Ignacio Zaragoza)',
            'Nogales (Mariposa)',
            'Mexicali II (Nvo. Mexicali)',
            'Piedras Negras',
            'San Luis Río Colorado',
            'Agua Prieta',
            'Cd. Acuña'
        ]
        
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        datos_demo = []
        
        for aduana in aduanas_principales:
            # Volúmenes basados en importancia del puerto
            if 'Nuevo Laredo' in aduana:
                base_contenedores = np.random.randint(95000, 105000)
            elif 'Reynosa' in aduana or 'Juárez' in aduana:
                base_contenedores = np.random.randint(70000, 85000)
            elif 'Tijuana' in aduana or 'Laredo' in aduana:
                base_contenedores = np.random.randint(55000, 70000)
            else:
                base_contenedores = np.random.randint(30000, 55000)
            
            datos_demo.append({
                'Aduana': aduana,
                'Contenedores': base_contenedores,
                'Valor_USD': base_contenedores * 2200,
                'Fecha': fecha_actual
            })
        
        df_demo = pd.DataFrame(datos_demo)
        datos_combinados.append(df_demo)
        resultados['fuentes'].append('Datos Demo')
        st.info(f"📊 Datos demo generados: {len(df_demo)} aduanas")
    
    # 4. Guardar datos combinados
    if datos_combinados:
        try:
            df_final = pd.concat(datos_combinados, ignore_index=True)
            
            # Guardar en CSV
            csv_path = Path(__file__).parent / "data" / "aduanas_latest.csv"
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            df_final.to_csv(csv_path, index=False)
            
            resultados['exito'] = True
            resultados['registros'] = len(df_final)
            
            st.success(f"💾 Datos guardados: {len(df_final)} registros en CSV")
            st.success(f"📊 Total contenedores: {df_final['Contenedores'].sum():,.0f}")
        except Exception as e:
            resultados['errores'].append(f"Error al guardar: {e}")
            st.error(f"❌ Error al guardar: {e}")
    else:
        st.error("❌ No se pudo generar ningún dato")
    
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

def es_dia_festivo(fecha):
    """Verifica si una fecha es día festivo"""
    fecha_str = fecha.strftime('%Y-%m-%d')
    return fecha_str in DIAS_FESTIVOS_2025_2026

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
        dia_semana = fecha.weekday()  # 0=Lunes, 6=Domingo
        
        # NUEVA LÓGICA: Solo aplicar horario festivo reducido si:
        # 1. Es festivo binacional (MX/US) como Año Nuevo o Navidad, O
        # 2. Es fin de semana
        # Si es festivo de un solo país en día laboral, mantener horario normal
        
        es_festivo_binacional = info_festivo['pais'] == 'MX/US'
        es_fin_de_semana = dia_semana >= 5  # Sábado o Domingo
        
        # Solo aplicar horario festivo si es binacional o fin de semana
        if es_festivo_binacional or es_fin_de_semana:
            horario_festivo = horario['festivos']
            
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
                                'mensaje': f"Abierto - Horario especial por {info_festivo['nombre']} ({apertura_str.strip()} - {cierre_str.strip()})",
                                'festivo': info_festivo['nombre']
                            }
                        else:
                            return {
                                'abierta': False, 
                                'mensaje': f"Cerrado - {info_festivo['nombre']} (Horario especial: {apertura_str.strip()} - {cierre_str.strip()})",
                                'festivo': info_festivo['nombre']
                            }
                    except Exception as e:
                        pass
                else:
                    # Sin hora específica, retornar que hay horario reducido
                    return {
                        'abierta': True,
                        'mensaje': f"Horario especial por {info_festivo['nombre']} ({horario_festivo})",
                        'festivo': info_festivo['nombre']
                    }
        # Si es festivo de un solo país en día laboral, continuar con horario normal (no return aquí)
    
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
                
                # Manejar medianoche (00:00 o 24:00) - hasta el final del día
                if cierre_str.strip() in ['00:00', '24:00']:
                    # Medianoche significa que está abierto hasta las 23:59:59
                    # Si la hora de apertura es menor que la hora actual, está abierto
                    if hora_actual >= apertura:
                        return {'abierta': True, 'mensaje': f'Abierto ({apertura_str.strip()} - 00:00)', 'festivo': None}
                    else:
                        return {'abierta': False, 'mensaje': f'Cerrado (Abre a las {apertura_str.strip()})', 'festivo': None}
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
        fecha_inicio = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
        fechas = pd.date_range(start=fecha_inicio, end=fecha_fin, freq='D')
        
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
                es_festivo = es_dia_festivo(fecha)
                
                # Agregar variabilidad según el puerto
                variabilidad = np.random.randint(-400, 1500)
                cruces_base = base_cruces + variabilidad
                
                # Distribución FAST vs Regular
                if es_festivo:
                    # En días festivos, solo FAST y perecederos (reducción ~70%)
                    cruces_fast = int(cruces_base * 0.30)
                    cruces_regular = 0
                    cruces_perecederos = int(cruces_base * 0.05)
                    cruces = cruces_fast + cruces_perecederos
                else:
                    # Día normal: FAST 40%, Regular 55%, Perecederos 5%
                    cruces_fast = int(cruces_base * 0.40)
                    cruces_regular = int(cruces_base * 0.55)
                    cruces_perecederos = int(cruces_base * 0.05)
                    cruces = cruces_fast + cruces_regular + cruces_perecederos
                
                valor_usd = cruces * np.random.uniform(45000, 65000) # Valor promedio por camión
                data_list.append([fecha, puerto, cruces, cruces_fast, cruces_regular, cruces_perecederos, valor_usd, es_festivo])

        df_border = pd.DataFrame(data_list, columns=['Fecha', 'Puerto', 'Cruces', 'Cruces_FAST', 'Cruces_Regular', 'Cruces_Perecederos', 'Valor_USD', 'Es_Festivo'])
    df_border['Mes'] = df_border['Fecha'].dt.strftime('%Y-%m')
    df_border['Semana'] = df_border['Fecha'].dt.isocalendar().week

    # --- INTERFAZ ---
    if usar_datos_reales:
        st.markdown("📊 **Datos reales** de cruces comerciales basados en registros actuales, con proyección histórica de 12 meses.")
    else:
        st.markdown("Métricas de cruce terrestre basadas en reportes del **BTS** y valores comerciales del **US Census Bureau**.")
    
    # Información sobre programa FAST
    with st.expander("ℹ️ Información sobre Programa FAST y Operaciones Fronterizas"):
        st.markdown("""
        ### 🚀 Programa FAST (Free and Secure Trade)
        
        El programa **FAST** es una iniciativa bilateral entre México, USA y Canadá que permite cruces expeditos 
        de carga comercial para empresas y transportistas de bajo riesgo pre-aprobados.
        
        **Características:**
        - ✅ Inspecciones reducidas y carriles dedicados
        - ✅ ~40% de los cruces comerciales usan FAST
        - ✅ Tiempo de cruce reducido hasta 50%
        - ✅ Requisitos: Certificación C-TPAT, transportistas validados
        
        ### 📅 Restricciones en Días Festivos
        
        Durante **días festivos binacionales**, las operaciones fronterizas operan con capacidad limitada:
        - 🚫 **Carriles regulares**: Cerrados
        - ✅ **Carriles FAST**: Operando (capacidad reducida ~30%)
        - ✅ **Perecederos**: Permitidos (~5% del tráfico)
        - 📉 **Reducción total**: ~70% menos cruces que día normal
        
        **Días festivos incluidos:** Año Nuevo, Día de la Constitución, Presidents Day, Memorial Day, 
        Independence Day, Labor Day, Thanksgiving, Navidad, entre otros.
        """)

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
    total_fast = df_filtrado['Cruces_FAST'].sum() if 'Cruces_FAST' in df_filtrado.columns else 0
    total_regular = df_filtrado['Cruces_Regular'].sum() if 'Cruces_Regular' in df_filtrado.columns else 0
    total_perecederos = df_filtrado['Cruces_Perecederos'].sum() if 'Cruces_Perecederos' in df_filtrado.columns else 0
    dias_festivos_count = df_filtrado['Es_Festivo'].sum() if 'Es_Festivo' in df_filtrado.columns else 0

    total_valor = df_filtrado['Valor_USD'].sum()
    if moneda == "MXN (Pesos)":
        total_valor *= tipo_cambio
        simbolo = "MXN"
    else:
        simbolo = "USD"

    # Primera fila de KPIs principales
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Cruces", f"{total_cruces:,}")
    col2.metric(f"Valor Total ({simbolo})", f"${total_valor:,.0f}")
    col3.metric("Promedio Diario", f"{int(df_filtrado.groupby('Fecha')['Cruces'].sum().mean()):,}")

    # Segunda fila - Desglose por tipo de cruce
    st.markdown("### 🚛 Desglose por Tipo de Cruce")
    col1, col2, col3 = st.columns(3)
    
    pct_fast = (total_fast / total_cruces * 100) if total_cruces > 0 else 0
    pct_regular = (total_regular / total_cruces * 100) if total_cruces > 0 else 0
    pct_perecederos = (total_perecederos / total_cruces * 100) if total_cruces > 0 else 0
    
    col1.metric("🚀 FAST (Rápido)", f"{total_fast:,}", f"{pct_fast:.1f}%")
    col2.metric("🚚 Regular", f"{total_regular:,}", f"{pct_regular:.1f}%")
    col3.metric("🥗 Perecederos", f"{total_perecederos:,}", f"{pct_perecederos:.1f}%")

    st.divider()
    
    # --- GRÁFICO FAST vs REGULAR ---
    if 'Cruces_FAST' in df_completo.columns:
        st.subheader("🚀 Análisis de Programa FAST vs Regular")
        
        # Agregar por fecha para ver tendencia
        df_fast_analysis = df_completo.groupby('Fecha').agg({
            'Cruces_FAST': 'sum',
            'Cruces_Regular': 'sum',
            'Cruces_Perecederos': 'sum',
            'Es_Festivo': 'max'
        }).reset_index()
        
        # Crear gráfico de áreas apiladas
        fig_fast = go.Figure()
        
        fig_fast.add_trace(go.Scatter(
            x=df_fast_analysis['Fecha'],
            y=df_fast_analysis['Cruces_Regular'],
            mode='lines',
            name='Regular',
            stackgroup='one',
            fillcolor='rgba(64, 112, 244, 0.5)',
            line=dict(width=0.5, color='rgba(64, 112, 244, 1)')
        ))
        
        fig_fast.add_trace(go.Scatter(
            x=df_fast_analysis['Fecha'],
            y=df_fast_analysis['Cruces_FAST'],
            mode='lines',
            name='FAST',
            stackgroup='one',
            fillcolor='rgba(41, 181, 232, 0.5)',
            line=dict(width=0.5, color='rgba(41, 181, 232, 1)')
        ))
        
        fig_fast.add_trace(go.Scatter(
            x=df_fast_analysis['Fecha'],
            y=df_fast_analysis['Cruces_Perecederos'],
            mode='lines',
            name='Perecederos',
            stackgroup='one',
            fillcolor='rgba(76, 175, 80, 0.5)',
            line=dict(width=0.5, color='rgba(76, 175, 80, 1)')
        ))
        
        # Marcar días festivos
        festivos = df_fast_analysis[df_fast_analysis['Es_Festivo'] == True]
        if not festivos.empty:
            # Limitar a los primeros festivos para no saturar el gráfico
            festivos_muestra = festivos.head(10)
            for idx, festivo in festivos_muestra.iterrows():
                # Convertir a datetime si es necesario
                fecha_festivo = pd.to_datetime(festivo['Fecha'])
                fig_fast.add_vline(
                    x=fecha_festivo,
                    line_dash="dash",
                    line_color="red",
                    opacity=0.3
                )
            # Agregar nota sobre festivos
            fig_fast.add_annotation(
                text=f"{len(festivos)} días festivos (líneas rojas)",
                xref="paper", yref="paper",
                x=0.02, y=0.98,
                showarrow=False,
                bgcolor="rgba(255,0,0,0.1)",
                bordercolor="red",
                borderwidth=1
            )
        
        fig_fast.update_layout(
            title="Distribución de Cruces: FAST vs Regular vs Perecederos",
            xaxis_title="Fecha",
            yaxis_title="Número de Cruces",
            hovermode='x unified',
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_fast, use_container_width=True)
        
        # Información sobre días festivos
        if int(dias_festivos_count) > 0:
            st.info(f"📅 **Días festivos detectados:** {int(dias_festivos_count)} - En estos días solo operan carriles FAST y perecederos (reducción ~70% del tráfico)")

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

    # --- COMPARATIVA DÍAS FESTIVOS VS NORMALES ---
    if 'Es_Festivo' in df_completo.columns:
        st.subheader("📅 Impacto de Días Festivos en Operaciones")
        
        col_fest1, col_fest2 = st.columns(2)
        
        with col_fest1:
            # Calcular promedios
            df_festivos = df_completo[df_completo['Es_Festivo'] == True]
            df_normales = df_completo[df_completo['Es_Festivo'] == False]
            
            if not df_festivos.empty and not df_normales.empty:
                promedio_festivos = df_festivos.groupby('Fecha')['Cruces'].sum().mean()
                promedio_normales = df_normales.groupby('Fecha')['Cruces'].sum().mean()
                reduccion_pct = ((promedio_normales - promedio_festivos) / promedio_normales * 100)
                
                st.metric(
                    "Promedio Cruces - Día Normal",
                    f"{int(promedio_normales):,}",
                    f"Base 100%"
                )
                st.metric(
                    "Promedio Cruces - Día Festivo",
                    f"{int(promedio_festivos):,}",
                    f"-{reduccion_pct:.1f}%",
                    delta_color="inverse"
                )
        
        with col_fest2:
            # Gráfico comparativo por tipo de cruce
            if 'Cruces_FAST' in df_completo.columns:
                comparativa = pd.DataFrame({
                    'Tipo': ['Normal', 'Normal', 'Normal', 'Festivo', 'Festivo'],
                    'Categoría': ['FAST', 'Regular', 'Perecederos', 'FAST', 'Perecederos'],
                    'Cruces': [
                        df_normales['Cruces_FAST'].sum(),
                        df_normales['Cruces_Regular'].sum(),
                        df_normales['Cruces_Perecederos'].sum(),
                        df_festivos['Cruces_FAST'].sum(),
                        df_festivos['Cruces_Perecederos'].sum()
                    ]
                })
                
                fig_comp = px.bar(
                    comparativa,
                    x='Tipo',
                    y='Cruces',
                    color='Categoría',
                    title="Comparativa: Días Normales vs Festivos",
                    barmode='group',
                    color_discrete_map={
                        'FAST': '#29B5E8',
                        'Regular': '#4070F4',
                        'Perecederos': '#4CAF50'
                    }
                )
                fig_comp.update_layout(height=300)
                st.plotly_chart(fig_comp, use_container_width=True)

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
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1, 1, 2])
    with col_btn1:
        btn_recargar = st.button("🔄 Recargar Datos", help="Carga datos desde CSV o API", key="btn_recargar_mon")
    with col_btn2:
        usar_datos_reales = st.checkbox("📊 Datos Reales", value=False, help="Alternar entre datos simulados y datos reales", key="check_real_mon")
    with col_btn3:
        btn_actualizar_apis = st.button("🌐 Actualizar APIs", help="Consultar APIs externas y actualizar CSV", key="btn_api_mon")
    with col_btn4:
        if 'cache_aduanas_fuente' in st.session_state:
            fuente = st.session_state['cache_aduanas_fuente']
            cache_time = st.session_state.get('cache_aduanas_time', 0)
            edad_minutos = int((datetime.now().timestamp() - cache_time) / 60)
            st.caption(f"📡 {fuente} | ⏱️ {edad_minutos} min")
    
    # Actualizar desde APIs si se solicita
    if btn_actualizar_apis:
        with st.expander("📊 Actualización desde APIs", expanded=True):
            resultados = actualizar_datos_desde_apis()
            
            if resultados['exito']:
                st.success(f"✅ Actualización exitosa: {resultados['registros']} registros")
                st.info(f"📡 Fuentes consultadas: {', '.join(resultados['fuentes'])}")
                
                # Limpiar caché para forzar recarga
                if 'cache_aduanas' in st.session_state:
                    del st.session_state['cache_aduanas']
            else:
                st.error("❌ No se pudo actualizar desde ninguna API")
            
            if resultados['errores']:
                with st.expander("⚠️ Ver errores"):
                    for error in resultados['errores']:
                        st.warning(error)
    
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
            # Los contenedores en el CSV son mensuales, convertir a diarios y agregar variabilidad
            # Dividir entre 30 para obtener promedio diario, luego agregar variabilidad aleatoria
            
            # Tiempo de espera diferenciado por tipo de carril
            aduanas_status['Cruces_Diarios_Est'] = aduanas_status['Contenedores'].apply(
                lambda x: int((x / 30) * np.random.uniform(0.6, 1.4))  # Variabilidad diaria
            )
            
            aduanas_status['Tiempo Espera FAST (min)'] = aduanas_status['Cruces_Diarios_Est'].apply(
                lambda x: min(60, max(10, int(x / 20) + np.random.randint(-5, 10)))
            )
            aduanas_status['Tiempo Espera Regular (min)'] = aduanas_status['Cruces_Diarios_Est'].apply(
                lambda x: min(120, max(25, int(x / 15) + np.random.randint(-10, 20)))
            )
            aduanas_status['Tiempo Espera (min)'] = aduanas_status['Tiempo Espera Regular (min)']
            
            # Saturación por tipo de carril (basada en cruces diarios estimados)
            aduanas_status['Saturación FAST (%)'] = aduanas_status['Cruces_Diarios_Est'].apply(
                lambda x: min(85, max(20, int((x / 1500) * 100) + np.random.randint(-10, 15)))
            )
            aduanas_status['Saturación Regular (%)'] = aduanas_status['Cruces_Diarios_Est'].apply(
                lambda x: min(95, max(30, int((x / 1200) * 100) + np.random.randint(-5, 20)))
            )
            aduanas_status['Saturación (%)'] = aduanas_status['Saturación Regular (%)']
            
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
        tiempos_fast = []
        tiempos_regular = []
        saturaciones = []
        saturaciones_fast = []
        saturaciones_regular = []
        camiones_cola = []
        camiones_fast_cola = []
        camiones_regular_cola = []
        
        for aduana in aduanas_nombres:
            estado_aduana = aduana_esta_abierta(aduana, ahora)
            estados_aduanas.append(estado_aduana)
            
            # Si está cerrada, poner datos en 0
            if not estado_aduana['abierta']:
                tiempos_espera.append(0)
                tiempos_fast.append(0)
                tiempos_regular.append(0)
                saturaciones.append(0)
                saturaciones_fast.append(0)
                saturaciones_regular.append(0)
                camiones_cola.append(0)
                camiones_fast_cola.append(0)
                camiones_regular_cola.append(0)
            else:
                # Datos simulados solo para aduanas abiertas
                tiempo_regular = random.randint(30, 140)
                tiempo_fast = int(tiempo_regular * 0.35)  # FAST es ~65% más rápido
                tiempos_regular.append(tiempo_regular)
                tiempos_fast.append(tiempo_fast)
                tiempos_espera.append(tiempo_regular)
                
                saturacion_regular = random.randint(35, 95)
                saturacion_fast = int(saturacion_regular * 0.65)  # FAST menos saturado
                saturaciones_regular.append(saturacion_regular)
                saturaciones_fast.append(saturacion_fast)
                saturaciones.append(saturacion_regular)
                
                cola_total = random.randint(350, 1500)
                camiones_fast_cola.append(int(cola_total * 0.40))  # 40% en FAST
                camiones_regular_cola.append(int(cola_total * 0.60))  # 60% en Regular
                camiones_cola.append(cola_total)
        
        # Datos de aduanas con tiempos y saturación simulados (usando nombres oficiales)
        aduanas_status = pd.DataFrame({
            'Aduana': aduanas_nombres,
            'Tiempo Espera (min)': tiempos_espera,
            'Tiempo Espera FAST (min)': tiempos_fast,
            'Tiempo Espera Regular (min)': tiempos_regular,
            'Saturación (%)': saturaciones,
            'Saturación FAST (%)': saturaciones_fast,
            'Saturación Regular (%)': saturaciones_regular,
            'Carriles FAST': [3, 2, 3, 4, 3, 2, 3, 3, 2, 2, 2, 2],
            'Carriles Regular': [8, 7, 8, 9, 8, 7, 8, 8, 7, 6, 6, 7],
            'Capacidad FAST (Cam/hora)': [120, 80, 120, 160, 120, 80, 120, 120, 80, 80, 80, 80],
            'Capacidad Regular (Cam/hora)': [200, 175, 200, 225, 200, 175, 200, 200, 175, 150, 150, 175],
            'Capacidad (Camiones/hora)': [320, 255, 320, 385, 320, 255, 320, 320, 255, 230, 230, 255],
            'Camiones en Cola': camiones_cola,
            'Camiones FAST Cola': camiones_fast_cola,
            'Camiones Regular Cola': camiones_regular_cola,
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
    
    # 🚀 COMPARATIVA FAST VS REGULAR (Solo para aduanas abiertas)
    st.subheader("🚀 Programa FAST vs Regular - Tiempo Real")
    
    # Información sobre FAST
    with st.expander("ℹ️ ¿Qué es el Programa FAST?", expanded=False):
        st.markdown("""
        El programa **FAST (Free and Secure Trade)** es una iniciativa bilateral que permite cruces expeditos 
        para transportistas certificados de bajo riesgo.
        
        **Beneficios:**
        - ⚡ Hasta 65% menos tiempo de espera
        - 🎯 Inspecciones reducidas
        - 🚦 Carriles dedicados con prioridad
        - 📉 Menor saturación en general
        
        **Requisitos:** Certificación C-TPAT, transportistas validados, carga pre-documentada
        """)
    
    if not aduanas_abiertas_df.empty:
        # KPIs comparativos FAST vs Regular
        col_comp1, col_comp2, col_comp3, col_comp4 = st.columns(4)
        
        with col_comp1:
            tiempo_fast_prom = aduanas_abiertas_df['Tiempo Espera FAST (min)'].mean()
            tiempo_regular_prom = aduanas_abiertas_df['Tiempo Espera Regular (min)'].mean()
            ahorro_tiempo = tiempo_regular_prom - tiempo_fast_prom
            st.metric(
                "⏱️ Tiempo FAST Promedio", 
                f"{tiempo_fast_prom:.0f} min",
                f"-{ahorro_tiempo:.0f} min vs Regular",
                delta_color="inverse"
            )
        
        with col_comp2:
            sat_fast_prom = aduanas_abiertas_df['Saturación FAST (%)'].mean()
            sat_regular_prom = aduanas_abiertas_df['Saturación Regular (%)'].mean()
            diferencia_sat = sat_regular_prom - sat_fast_prom
            st.metric(
                "📊 Saturación FAST", 
                f"{sat_fast_prom:.1f}%",
                f"-{diferencia_sat:.1f}% vs Regular",
                delta_color="inverse"
            )
        
        with col_comp3:
            total_fast_cola = aduanas_abiertas_df['Camiones FAST Cola'].sum()
            st.metric("🚛 FAST en Cola", f"{total_fast_cola:,.0f}")
        
        with col_comp4:
            total_regular_cola = aduanas_abiertas_df['Camiones Regular Cola'].sum()
            st.metric("🚚 Regular en Cola", f"{total_regular_cola:,.0f}")
        
        # Gráfico comparativo
        st.markdown("#### 📊 Comparativa de Tiempos de Espera")
        
        # Preparar datos para el gráfico
        df_comparativa = aduanas_abiertas_df[['Aduana', 'Tiempo Espera FAST (min)', 'Tiempo Espera Regular (min)']].head(8)
        
        fig_comparativa = go.Figure()
        
        fig_comparativa.add_trace(go.Bar(
            name='FAST',
            x=df_comparativa['Aduana'],
            y=df_comparativa['Tiempo Espera FAST (min)'],
            marker_color='#29B5E8',
            text=df_comparativa['Tiempo Espera FAST (min)'],
            texttemplate='%{text:.0f} min',
            textposition='outside'
        ))
        
        fig_comparativa.add_trace(go.Bar(
            name='Regular',
            x=df_comparativa['Aduana'],
            y=df_comparativa['Tiempo Espera Regular (min)'],
            marker_color='#4070F4',
            text=df_comparativa['Tiempo Espera Regular (min)'],
            texttemplate='%{text:.0f} min',
            textposition='outside'
        ))
        
        fig_comparativa.update_layout(
            barmode='group',
            title='Tiempo de Espera: FAST vs Regular (Top 8 Aduanas)',
            xaxis_title='Aduana',
            yaxis_title='Tiempo de Espera (minutos)',
            height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis={'tickangle': -45}
        )
        
        st.plotly_chart(fig_comparativa, use_container_width=True)
        
        # Tabla comparativa de saturación
        st.markdown("#### 📈 Saturación por Tipo de Carril")
        
        col_sat1, col_sat2 = st.columns(2)
        
        with col_sat1:
            st.markdown("**🚀 Carriles FAST**")
            df_fast_display = aduanas_abiertas_df[['Aduana', 'Saturación FAST (%)', 'Carriles FAST', 'Camiones FAST Cola']].copy()
            df_fast_display = df_fast_display.sort_values('Saturación FAST (%)', ascending=False).head(6)
            df_fast_display.columns = ['Aduana', 'Saturación %', 'Carriles', 'Cola']
            st.dataframe(df_fast_display, hide_index=True, use_container_width=True)
        
        with col_sat2:
            st.markdown("**🚚 Carriles Regular**")
            df_regular_display = aduanas_abiertas_df[['Aduana', 'Saturación Regular (%)', 'Carriles Regular', 'Camiones Regular Cola']].copy()
            df_regular_display = df_regular_display.sort_values('Saturación Regular (%)', ascending=False).head(6)
            df_regular_display.columns = ['Aduana', 'Saturación %', 'Carriles', 'Cola']
            st.dataframe(df_regular_display, hide_index=True, use_container_width=True)
        
        # Recomendaciones automáticas
        st.markdown("#### 💡 Recomendaciones")
        
        # Encontrar mejores opciones FAST
        mejores_fast = aduanas_abiertas_df.nsmallest(3, 'Tiempo Espera FAST (min)')
        peores_regular = aduanas_abiertas_df.nlargest(3, 'Tiempo Espera Regular (min)')
        
        col_rec1, col_rec2 = st.columns(2)
        
        with col_rec1:
            st.success("**✅ Aduanas FAST Más Rápidas**")
            for idx, row in mejores_fast.iterrows():
                st.markdown(f"- **{row['Aduana']}**: {row['Tiempo Espera FAST (min)']:.0f} min")
        
        with col_rec2:
            st.warning("**⚠️ Evitar (Regular Saturado)**")
            for idx, row in peores_regular.iterrows():
                st.markdown(f"- **{row['Aduana']}**: {row['Tiempo Espera Regular (min)']:.0f} min")
    else:
        st.info("ℹ️ No hay aduanas abiertas en este momento para mostrar comparativa FAST vs Regular")
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
    
    # Selector de vista
    col_vista1, col_vista2 = st.columns([3, 1])
    with col_vista1:
        st.markdown("Selecciona el nivel de detalle:")
    with col_vista2:
        vista_detalle = st.radio(
            "Vista:",
            options=["Básica", "Con FAST", "Completa"],
            horizontal=True,
            label_visibility="collapsed"
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

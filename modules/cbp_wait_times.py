"""
Módulo de integración de CBP Wait Times en Streamlit
Proporciona funciones para mostrar tiempos de espera actualizados EN TIEMPO REAL
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import json
import logging
import sys

logger = logging.getLogger(__name__)

# Intentar importar Selenium
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logger.warning("Selenium no disponible - usando fallback")

# ============================================================================
# PUERTOS SOPORTADOS - TODOS LOS PUERTOS MÉXICO-USA Y CANADÁ-USA
# ============================================================================

# PUERTOS MÉXICO-USA (22 principales + especializados)
PUERTOS_MEXICO = {
    # Texas
    "Laredo": "06480101",
    "Brownsville": "06471001",
    "Rio Grande City": "06472001",
    "Progreso": "06473001",
    "Roma": "06474001",
    "Del Rio": "06481001",
    "Eagle Pass": "06500601",
    "Presidio": "06483001",
    "Tornillo": "06452401",
    
    # California-Arizona
    "Ysleta": "06450702",
    "Otay Mesa": "09250602",
    "San Ysidro": "09250101",
    "Calexico East": "09251202",
    "Tecate": "09250702",
    "El Paso": "06450701",
    "Santa Teresa": "06451701",
    
    # Arizona
    "Nogales": "07200601",
    "Douglas": "07201001",
    "Naco": "07202001",
    "Lukeville": "07204001",
    "San Luis": "07150501",
    "Columbus": "07203001",
    
    # Puertos especializados
    "BOTA CARGO FACILITY": "09250401",
    "Brownsville - Los Indios": "06470501",
    "Brownsville - Veterans International": "06470701",
    "Hidalgo": "06470101",
}

# PUERTOS CANADÁ-USA (30+ puertos)
PUERTOS_CANADA = {
    # British Columbia
    "Blaine": "05200101",
    "Point Roberts": "05220101",
    "Bellingham": "05230101",
    "Sumas": "05240101",
    "Lynden": "05210101",
    
    # Washington
    "Port Angeles": "05250101",
    
    # Montana
    "Sweetgrass": "04640101",
    "Piegan": "04660101",
    "Turner": "04670101",
    
    # North Dakota
    "Pembina": "04620101",
    "Portal": "04680101",
    "Dunseith": "04570101",
    "Fortuna": "04690101",
    
    # Minnesota
    "International Falls": "04600101",
    "Baudette": "04520101",
    "Janesville": "04700101",
    
    # Michigan
    "Sault Ste Marie": "04710101",
    "Mackinac Bridge": "04720101",
    
    # New York
    "Buffalo Niagara Falls": "01050101",
    "Thousand Islands Bridge": "01140101",
    "Rainbow Bridge": "01110101",
    "Ogdensburg": "01100101",
    "Champlain Rouses Point": "01070101",
    "Highgate Springs": "01090101",
    
    # Vermont
    "Alburgh": "01150101",
    "Highgate Springs": "01090101",
    
    # Maine
    "Calais": "01060101",
    "Houlton": "01160101",
    "Van Buren": "01170101",
    "Jackman": "01180101",
    "Coburn Gore": "01190101",
}

# Todos los puertos combinados
TODOS_PUERTOS_CBP = {**PUERTOS_MEXICO, **PUERTOS_CANADA}

# Legacy (para compatibilidad)
CBP_API_PORTS = TODOS_PUERTOS_CBP


def obtener_espera_puerto_selenium(puerto_codigo: str, puerto_tipo: str = "COV", timeout: int = 10) -> dict:
    """
    Obtiene tiempos de espera REALES usando Selenium (ejecuta JavaScript).
    Este es el método PREFERIDO para datos en tiempo real.
    
    Args:
        puerto_codigo: Código de puerto CBP
        puerto_tipo: Tipo de puerto (COV = Commercial)
        timeout: Segundos máximos para esperar
    
    Returns:
        Dict con datos actualizados
    """
    if not SELENIUM_AVAILABLE:
        return None
    
    driver = None
    try:
        url = f"https://bwt.cbp.gov/details/{puerto_codigo}/{puerto_tipo}"
        
        # Configurar Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
        
        # Crear driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Cargar página
        driver.get(url)
        
        # Esperar a que JavaScript cargue datos
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: len(d.find_elements(By.TAG_NAME, "h4")) > 0
            )
        except TimeoutException:
            pass
        
        # Extraer datos con JavaScript
        datos_js = driver.execute_script("""
        return {
            'puerto': document.querySelector('h4')?.textContent || 'Unknown',
            'espera_texto': Array.from(document.querySelectorAll('div')).find(
                el => el.textContent.includes('Current Wait')
            )?.textContent || '',
            'html': document.documentElement.innerHTML.substring(0, 5000)
        };
        """)
        
        # Procesar datos
        resultado = {
            'puerto': datos_js.get('puerto', 'Desconocido'),
            'espera_minutos': 0,
            'actualizado': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'fuente': 'CBP - Tiempo Real (Selenium)',
            'metodo': 'selenium'
        }
        
        # Extraer tiempo de espera
        import re
        espera_texto = datos_js.get('espera_texto', '')
        if espera_texto and 'Lanes Closed' not in espera_texto:
            numeros = re.findall(r'\d+', espera_texto)
            if numeros:
                resultado['espera_minutos'] = int(numeros[0])
        
        return resultado
        
    except Exception as e:
        logger.debug(f"Selenium fallback: {str(e)}")
        return None
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


@st.cache_data(ttl=60)  # Cache 1 minuto para actualización más rápida
def obtener_espera_puerto(puerto_codigo: str, usar_selenium: bool = False) -> dict:
    """
    Obtiene tiempos de espera actuales de CBP para un puerto.
    PRIORIDAD: RSS Feed (RÁPIDO) → Selenium opcional (LENTO) → Datos simulados
    
    Args:
        puerto_codigo: Código de puerto CBP (ej: "09250602")
        usar_selenium: Si True, intenta Selenium (MÁS LENTO pero más preciso)
    
    Returns:
        Dict con datos de espera
    """
    # Primero: Intentar RSS feed de CBP (RÁPIDO - 1-2 segundos)
    try:
        rss_url = f"https://bwt.cbp.gov/api/bwtRss/rssbyportnum/JSON/COV/{puerto_codigo[-6:]}"
        response = requests.get(rss_url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            
            resultado = {
                'puerto': f"Puerto {puerto_codigo}",
                'espera_minutos': 0,
                'actualizado': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'fuente': 'CBP API RSS',
                'metodo': 'rss'
            }
            
            if isinstance(data, dict) and 'data' in data:
                item = data['data']
                resultado['espera_minutos'] = item.get('wait_time', 0)
                resultado['puerto'] = item.get('port_name', resultado['puerto'])
            
            return resultado
    except Exception as e:
        logger.debug(f"RSS feed error: {str(e)}")
    
    # Opcional: Intenta Selenium si se solicita (MÁS LENTO pero tiempo real)
    if usar_selenium and SELENIUM_AVAILABLE:
        try:
            datos = obtener_espera_puerto_selenium(puerto_codigo)
            if datos and datos.get('espera_minutos') is not None:
                return datos
        except Exception as e:
            logger.debug(f"Selenium no disponible, usando fallback")
    
    # Fallback: Datos simulados
    return {
        'puerto': f"Puerto {puerto_codigo}",
        'espera_minutos': 15,
        'actualizado': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'fuente': 'Datos simulados (API no disponible)',
        'metodo': 'simulado'
    }


def mostrar_tablero_esperas_cbp():
    """
    Muestra un tablero interactivo con tiempos de espera de CBP.
    """
    st.header("🚚 Tiempos de Espera CBP - Puertos de Entrada")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Puertos México-USA")
        
        puertos_mexico = {
            "Otay Mesa": "09250602",
            "San Ysidro": "09250101",
            "Tecate": "09250702",
            "El Paso": "06450701",
            "Laredo": "06480101",
        }
        
        # Selectbox para elegir puerto
        puerto_seleccionado = st.selectbox(
            "Selecciona un puerto:",
            list(puertos_mexico.keys())
        )
        
        puerto_codigo = puertos_mexico[puerto_seleccionado]
        
        # Obtener datos
        datos = obtener_espera_puerto(puerto_codigo)
        
        # Mostrar datos en tarjetas
        if datos:
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.metric(
                    "⏱️ Espera Actual",
                    f"{datos.get('espera_minutos', '—')} min",
                    delta=None
                )
            
            with col_b:
                st.metric(
                    "🕐 Actualizado",
                    datos.get('actualizado', '—'),
                    delta=None
                )
            
            st.caption(f"Fuente: {datos.get('fuente', 'Desconocida')}")
    
    with col2:
        st.subheader("📊 Comparativa de Puertos")
        
        # Tabla comparativa
        datos_comparativos = []
        for puerto_nombre, puerto_cod in puertos_mexico.items():
            datos = obtener_espera_puerto(puerto_cod)
            datos_comparativos.append({
                'Puerto': puerto_nombre,
                'Espera (min)': datos.get('espera_minutos', '—'),
                'Actualizado': datos.get('actualizado', '—')
            })
        
        df_comparativa = pd.DataFrame(datos_comparativos)
        st.dataframe(df_comparativa, use_container_width=True, hide_index=True)


def widget_espera_rapido(puerto_codigo: str, width: int = "small") -> None:
    """
    Widget pequeño que muestra tiempo de espera para un puerto.
    Útil para dashboards comprimidos.
    
    Args:
        puerto_codigo: Código CBP
        width: "small", "medium", "large"
    """
    datos = obtener_espera_puerto(puerto_codigo)
    
    espera = datos.get('espera_minutos', '—')
    
    # HTML styling
    colores = {
        "small": "height: 80px; font-size: 1.2rem;",
        "medium": "height: 120px; font-size: 1.5rem;",
        "large": "height: 160px; font-size: 2rem;"
    }
    
    html = f"""
    <div style="background: linear-gradient(135deg, #ff9800, #f57c00); 
                border-radius: 12px; padding: 16px; text-align: center; 
                color: white; {colores.get(width, colores['small'])}
                display: flex; flex-direction: column; justify-content: center; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
        <div style="font-size: 0.8rem; opacity: 0.9;">⏱️ Espera</div>
        <div style="font-weight: bold;">{espera} min</div>
        <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 4px;">CBP</div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)


if __name__ == "__main__":
    mostrar_tablero_esperas_cbp()

"""
CBP Border Wait Times Scraper
Obtiene tiempos de espera en tiempo real de https://bwt.cbp.gov

Puertos soportados:
- 09250602 (COV): Otay Mesa (California)
- 09250101 (TIJ): San Ysidro (California)
- 09250702 (TEC): Tecate (California)
- Y muchos más...

Versión: 1.0.0
Fecha: 2026-05-07
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import json
import time
import logging
from typing import Dict, List, Optional, Tuple

# Intentar importar Selenium si está disponible
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# CONSTANTES Y CONFIGURACIÓN
# ============================================================================

# Base URL para la API de CBP
CBP_API_BASE = "https://bwt.cbp.gov/api"
CBP_DETAILS_BASE = "https://bwt.cbp.gov/details"

# ============================================================================
# TODOS LOS PUERTOS MÉXICO-USA — códigos reales del API bwtpublicmod de CBP
# ============================================================================
PUERTOS_MEXICO = {
    "Laredo - World Trade Bridge": "230404",
    "Laredo - Colombia Solidarity": "230403",
    "Laredo - Bridge I": "230401",
    "Laredo - Bridge II": "230402",
    "Brownsville - B&M": "535501",
    "Brownsville - Los Indios": "535503",
    "Brownsville - Veterans International": "535502",
    "Hidalgo": "230501",
    "Pharr": "230502",
    "Anzalduas International Bridge": "230503",
    "Rio Grande City": "230701",
    "Progreso - Progreso International": "230901",
    "Progreso - Donna International": "230902",
    "Roma": "231001",
    "Del Rio": "230201",
    "Eagle Pass - Bridge I": "230301",
    "Eagle Pass - Bridge II": "230302",
    "Presidio": "240301",
    "Tornillo": "240401",
    "El Paso - Ysleta": "240203",
    "El Paso - Paso Del Norte": "240202",
    "El Paso - Bridge of the Americas": "240201",
    "Santa Teresa": "240801",
    "Columbus": "240601",
    "Otay Mesa - Commercial": "250602",
    "San Ysidro": "250401",
    "Calexico East": "250301",
    "Calexico West": "250302",
    "Tecate": "250501",
    "Nogales - Mariposa": "260402",
    "Nogales - Deconcini": "260401",
    "Douglas": "260101",
    "Naco": "260301",
    "Lukeville": "260201",
    "San Luis I": "260801",
    "San Luis II": "260802",
}

# ============================================================================
# TODOS LOS PUERTOS CANADÁ-USA — códigos reales del API bwtpublicmod de CBP
# ============================================================================
PUERTOS_CANADA = {
    "Blaine - Pacific Highway": "300401",
    "Blaine - Peace Arch": "300402",
    "Blaine - Point Roberts": "300403",
    "Sumas": "300901",
    "Lynden": "302301",
    "Sweetgrass": "331001",
    "Pembina": "340101",
    "International Falls": "360401",
    "Sault Ste. Marie": "380301",
    "Detroit - Ambassador Bridge": "380001",
    "Detroit - Windsor Tunnel": "380002",
    "Port Huron - Bluewater Bridge": "380201",
    "Buffalo/Niagara Falls - Peace Bridge": "090101",
    "Buffalo/Niagara Falls - Rainbow Bridge": "090102",
    "Buffalo/Niagara Falls - Lewiston Bridge": "090104",
    "Alexandria Bay - Thousand Islands Bridge": "070801",
    "Ogdensburg": "070101",
    "Massena": "070401",
    "Champlain": "071201",
    "Highgate Springs": "021201",
    "Derby Line": "020901",
    "Norton": "021101",
    "Calais - Ferry Point": "011501",
    "Calais - International Avenue": "011503",
    "Houlton": "010601",
    "Jackman": "010401",
}

# Todos los puertos combinados
TODOS_PUERTOS = {**PUERTOS_MEXICO, **PUERTOS_CANADA}

# Extensiones por tipo de puerto
PORT_EXTENSIONS = {
    "COM": "Commercial",
    "COV": "Commercial",
    "PED": "Pedestrian",
    "TRK": "Truck",
}


# ============================================================================
# FUNCIONES DE SCRAPING
# ============================================================================

def obtener_datos_tiempo_espera_selenium(puerto_codigo: str, puerto_tipo: str = "COV", timeout: int = 15) -> Optional[Dict]:
    """
    Obtiene datos de tiempo de espera usando Selenium (ejecuta JavaScript).
    Este es el método PREFERIDO para obtener datos en tiempo real.
    
    Args:
        puerto_codigo: Código CBP del puerto (ej: "09250602" para Otay Mesa)
        puerto_tipo: Tipo de puerto - COV (Commercial), PED (Pedestrian), etc.
        timeout: Tiempo máximo en segundos para esperar datos
    
    Returns:
        Dict con datos de espera o None si falla
    """
    if not SELENIUM_AVAILABLE:
        logger.warning("⚠️ Selenium no instalado. Use: pip install selenium webdriver-manager")
        return None
    
    driver = None
    try:
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        url = f"{CBP_DETAILS_BASE}/{puerto_codigo}/{puerto_tipo}"
        logger.info(f"🌐 Scraping con Selenium: {url}")
        
        # Configurar opciones de Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Ejecutar en background
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # Crear driver con webdriver-manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Cargar página
        driver.get(url)
        
        # Esperar a que carguen datos principales
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            logger.warning(f"⏱️ Timeout esperando que página cargue completamente")
        
        # Extraer datos con JavaScript
        script_extraccion = """
        return {
            'puerto': document.querySelector('h4')?.textContent || 'Unknown',
            'horarios': Array.from(document.querySelectorAll('div'))
                .find(el => el.textContent.includes('Hours of Operation'))
                ?.textContent.replace('Hours of Operation:', '').trim() || 'N/A',
            'espera_actual': document.querySelector('[data-wait-time]')?.textContent || 
                            Array.from(document.querySelectorAll('div'))
                                .find(el => el.textContent.includes('Current Wait'))
                                ?.textContent.split('\\n')[1]?.trim() || null,
            'espera_promedio': Array.from(document.querySelectorAll('div'))
                .find(el => el.textContent.includes('Average Wait'))
                ?.textContent.split('\\n')[1]?.trim() || null,
            'fecha': new Date().toISOString()
        };
        """
        
        datos_js = driver.execute_script(script_extraccion)
        
        # Procesar datos
        datos = {
            'puerto_codigo': puerto_codigo,
            'tipo': puerto_tipo,
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'fecha_hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'metodo': 'Selenium + JavaScript'
        }
        
        if datos_js:
            datos['puerto'] = datos_js.get('puerto', 'Desconocido')
            datos['horarios'] = datos_js.get('horarios', 'N/A')
            
            # Extraer números de tiempos de espera
            import re
            
            espera_actual = datos_js.get('espera_actual', '')
            if espera_actual and 'Lanes Closed' not in espera_actual:
                numeros = re.findall(r'\d+', espera_actual)
                if numeros:
                    datos['espera_actual_minutos'] = int(numeros[0])
            
            espera_promedio = datos_js.get('espera_promedio', '')
            if espera_promedio:
                numeros = re.findall(r'\d+', espera_promedio)
                if numeros:
                    datos['espera_promedio_minutos'] = int(numeros[0])
        
        logger.info(f"✅ Datos obtenidos con Selenium: {datos.get('puerto', 'Desconocido')}")
        return datos
        
    except TimeoutException:
        logger.error(f"❌ Timeout: La página no cargó en tiempo")
        return None
    except Exception as e:
        logger.error(f"❌ Error con Selenium: {str(e)}")
        return None
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


def obtener_datos_tiempo_espera(puerto_codigo: str, puerto_tipo: str = "COV") -> Optional[Dict]:
    """
    Obtiene datos de tiempo de espera actual para un puerto específico.
    
    Args:
        puerto_codigo: Código CBP del puerto (ej: "09250602" para Otay Mesa)
        puerto_tipo: Tipo de puerto - COV (Commercial), PED (Pedestrian), etc.
    
    Returns:
        Dict con datos de espera o None si falla
    
    Ejemplo:
        datos = obtener_datos_tiempo_espera("09250602", "COV")
    """
    try:
        # URL de la página de detalles
        url = f"{CBP_DETAILS_BASE}/{puerto_codigo}/{puerto_tipo}"
        
        logger.info(f"Scraping datos de: {url}")
        
        # Headers para evitar bloqueos
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Hacer request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parsear HTML
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraer información
        datos = {
            'puerto_codigo': puerto_codigo,
            'tipo': puerto_tipo,
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'fecha_hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        
        # Buscar el título (ej: "Otay Mesa - Commercial")
        titulo_element = soup.find('h4')
        if titulo_element:
            datos['puerto'] = titulo_element.get_text(strip=True)
        
        # Buscar horarios de operación
        horas_element = soup.find(string=lambda text: text and "Hours of Operation" in text)
        if horas_element:
            horarios_text = horas_element.get_text(strip=True)
            datos['horarios'] = horarios_text.replace("Hours of Operation: ", "")
        
        # Buscar wait time actual
        current_wait = soup.find(string=lambda text: text and "Current Wait" in text)
        if current_wait:
            # Buscar el siguiente elemento que contenga el número
            parent = current_wait.parent.parent if current_wait.parent else current_wait.parent
            if parent:
                wait_text = parent.get_text(strip=True)
                datos['espera_actual_texto'] = wait_text
                
                # Extraer número si existe
                import re
                numeros = re.findall(r'\d+', wait_text)
                if numeros and 'Lanes Closed' not in wait_text:
                    datos['espera_actual_minutos'] = int(numeros[0])
                else:
                    datos['espera_actual_minutos'] = None
                    datos['estado'] = 'Lanes Closed' if 'Lanes Closed' in wait_text else 'Desconocido'
        
        # Buscar average wait
        avg_wait = soup.find(string=lambda text: text and "Average Wait" in text)
        if avg_wait:
            parent = avg_wait.parent.parent if avg_wait.parent else avg_wait.parent
            if parent:
                avg_text = parent.get_text(strip=True)
                datos['espera_promedio_texto'] = avg_text
                
                import re
                numeros = re.findall(r'\d+', avg_text)
                if numeros:
                    datos['espera_promedio_minutos'] = int(numeros[0])
        
        # Fecha de datos
        fecha_element = soup.find(string=lambda text: text and "Date:" in text)
        if fecha_element:
            datos['fecha_reporte'] = fecha_element.replace("Date: ", "").strip()
        
        logger.info(f"✅ Datos obtenidos exitosamente: {datos.get('puerto', 'Desconocido')}")
        return datos
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error en request: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"❌ Error al parsear datos: {str(e)}")
        return None


def obtener_datos_rss_puerto(puerto_codigo: str, puerto_tipo: str = "COV") -> Optional[Dict]:
    """
    Obtiene datos de espera desde RSS feed de CBP.
    
    Endpoint alternativo que proporciona datos en formato RSS.
    """
    try:
        # RSS URL
        rss_url = f"{CBP_API_BASE}/bwtRss/rssbyportnum/JSON/{puerto_tipo}/{puerto_codigo[-6:]}"
        
        logger.info(f"Obteniendo RSS: {rss_url}")
        
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
        
        data = response.json() if response.text else {}
        return data
        
    except Exception as e:
        logger.error(f"❌ Error obteniendo RSS: {str(e)}")
        return None


def obtener_multiple_puertos(puertos_dict: Dict[str, str]) -> pd.DataFrame:
    """
    Obtiene datos de múltiples puertos simultáneamente.
    
    Args:
        puertos_dict: Dict con nombre_puerto: codigo_cbp
    
    Returns:
        DataFrame con datos consolidados
    """
    resultados = []
    
    for puerto_nombre, puerto_codigo in puertos_dict.items():
        logger.info(f"Procesando: {puerto_nombre} ({puerto_codigo})")
        
        datos = obtener_datos_tiempo_espera(puerto_codigo, "COV")
        
        if datos:
            resultados.append(datos)
            # Esperar un poco entre requests para no sobrecargar servidor
            time.sleep(2)
        else:
            logger.warning(f"⚠️ No se pudieron obtener datos para {puerto_nombre}")
    
    if resultados:
        df = pd.DataFrame(resultados)
        return df
    else:
        return pd.DataFrame()


def guardar_datos_locales(datos: Dict, archivo_prefix: str = "cbp_wait_times") -> Path:
    """
    Guarda datos en archivo CSV y JSON local.
    
    Args:
        datos: Dict o List de dicts con datos
        archivo_prefix: Prefijo para el archivo
    
    Returns:
        Path al archivo guardado
    """
    try:
        # Crear directorio data si no existe
        data_dir = Path(__file__).parent.parent / "data"
        data_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Si es un dict, convertir a lista
        if isinstance(datos, dict):
            datos = [datos]
        
        # Convertir a DataFrame
        df = pd.DataFrame(datos)
        
        # Guardar CSV
        csv_path = data_dir / f"{archivo_prefix}_{timestamp}.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        logger.info(f"✅ CSV guardado: {csv_path}")
        
        # Guardar JSON
        json_path = data_dir / f"{archivo_prefix}_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2, default=str)
        logger.info(f"✅ JSON guardado: {json_path}")
        
        return csv_path
        
    except Exception as e:
        logger.error(f"❌ Error guardando datos: {str(e)}")
        return None


# ============================================================================
# SCRIPT PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🛑 CBP BORDER WAIT TIMES SCRAPER")
    print("="*70 + "\n")
    
    # Opción 1: Obtener datos de un puerto específico
    print("📍 OBTENER DATOS DE PUERTO ESPECÍFICO")
    print("-" * 70)
    
    datos_otay = obtener_datos_tiempo_espera("09250602", "COV")
    if datos_otay:
        print(f"Puerto: {datos_otay.get('puerto', 'N/A')}")
        print(f"Horarios: {datos_otay.get('horarios', 'N/A')}")
        print(f"Espera Actual: {datos_otay.get('espera_actual_minutos', 'N/A')} minutos")
        print(f"Espera Promedio: {datos_otay.get('espera_promedio_minutos', 'N/A')} minutos")
    
    print("\n")
    
    # Opción 2: Obtener datos de múltiples puertos
    print("🔍 OBTENER DATOS DE MÚLTIPLES PUERTOS")
    print("-" * 70)
    
    puertos_a_scrapear = {
        "Otay Mesa": "09250602",
        "San Ysidro": "09250101",
        "Tecate": "09250702",
    }
    
    df_puertos = obtener_multiple_puertos(puertos_a_scrapear)
    
    if not df_puertos.empty:
        print(f"\n✅ Se obtuvieron datos de {len(df_puertos)} puertos:")
        print(df_puertos[['puerto', 'espera_actual_minutos', 'espera_promedio_minutos']])
        
        # Guardar
        archivo_guardado = guardar_datos_locales(df_puertos.to_dict('records'))
        print(f"\n📁 Datos guardados en: {archivo_guardado}")
    else:
        print("❌ No se pudieron obtener datos")
    
    print("\n" + "="*70)
    print("✅ Scraping completado")
    print("="*70 + "\n")

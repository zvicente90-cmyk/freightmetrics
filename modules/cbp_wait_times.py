"""
Módulo CBP Wait Times — FreightMetrics
API: https://bwt.cbp.gov/api/waittimes (XML, todos los puertos en una llamada)
"""

import streamlit as st
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# MAPEO DE NOMBRES CBP → NOMBRES AMIGABLES
# Clave: nombre exacto como aparece en el XML de CBP
# ============================================================================
PUERTOS_MEXICO = {
    # Texas
    "Laredo": "Laredo (TX)",
    "World Trade Bridge": "World Trade Bridge (TX)",
    "Colombia Solidarity": "Colombia Solidarity (TX)",
    "Brownsville": "Brownsville (TX)",
    "Los Indios": "Los Indios (TX)",
    "Veterans International": "Veterans Intl (TX)",
    "Rio Grande City": "Rio Grande City (TX)",
    "Progreso": "Progreso (TX)",
    "Roma": "Roma (TX)",
    "Del Rio": "Del Rio (TX)",
    "Eagle Pass": "Eagle Pass (TX)",
    "Presidio": "Presidio (TX)",
    "Tornillo": "Tornillo (TX)",
    "Hidalgo": "Hidalgo (TX)",
    "Pharr": "Pharr (TX)",
    "Anzalduas International Bridge": "Anzalduas (TX)",
    # El Paso
    "Ysleta": "Ysleta / El Paso (TX)",
    "El Paso": "El Paso (TX)",
    "Bridge of the Americas": "Bridge of Americas (TX)",
    "Stanton DCL": "Stanton St (TX)",
    # New Mexico
    "Santa Teresa": "Santa Teresa (NM)",
    "Columbus": "Columbus (NM)",
    # California
    "Otay Mesa": "Otay Mesa (CA)",
    "San Ysidro": "San Ysidro (CA)",
    "Calexico / West": "Calexico West (CA)",
    "Calexico / East": "Calexico East (CA)",
    "Tecate": "Tecate (CA)",
    # Arizona
    "Nogales": "Nogales (AZ)",
    "Mariposa": "Mariposa / Nogales (AZ)",
    "Douglas": "Douglas (AZ)",
    "Naco": "Naco (AZ)",
    "Lukeville": "Lukeville (AZ)",
    "San Luis": "San Luis (AZ)",
    "San Luis II": "San Luis II (AZ)",
}

PUERTOS_CANADA = {
    "Blaine": "Blaine (WA)",
    "Pacific Highway": "Pacific Hwy (WA)",
    "Sumas": "Sumas (WA)",
    "Lynden": "Lynden (WA)",
    "Sweetgrass": "Sweetgrass (MT)",
    "Pembina": "Pembina (ND)",
    "International Falls": "Intl Falls (MN)",
    "Sault Ste. Marie": "Sault Ste Marie (MI)",
    "Detroit": "Detroit (MI)",
    "Port Huron": "Port Huron (MI)",
    "Buffalo/Niagara Falls": "Buffalo/Niagara (NY)",
    "Alexandria Bay": "Alexandria Bay (NY)",
    "Ogdensburg": "Ogdensburg (NY)",
    "Massena": "Massena (NY)",
    "Champlain": "Champlain (NY)",
    "Highgate Springs": "Highgate Springs (VT)",
    "Calais": "Calais (ME)",
    "Houlton": "Houlton (ME)",
    "Jackman": "Jackman (ME)",
    "Derby Line": "Derby Line (VT)",
}

# Legacy para compatibilidad con page que importa CBP_API_PORTS
CBP_API_PORTS = {**PUERTOS_MEXICO, **PUERTOS_CANADA}

# ============================================================================
# FETCH ÚNICO — todos los puertos en una sola llamada XML
# ============================================================================

_CBP_API_DEFAULT = "https://bwt.cbp.gov/api/waittimes"


def _get_cbp_url() -> str:
    """
    Resuelve la URL del API de CBP con prioridad:
    1. st.secrets["CBP_API_URL"]   → configurado en Streamlit Cloud o .streamlit/secrets.toml
    2. Variable de entorno CBP_API_URL
    3. URL directa a bwt.cbp.gov (desarrollo local)
    """
    import os
    try:
        return st.secrets["CBP_API_URL"]
    except Exception:
        pass
    return os.environ.get("CBP_API_URL", _CBP_API_DEFAULT)


@st.cache_data(ttl=120)  # Cache 2 minutos
def _fetch_todos_los_puertos() -> dict:
    """
    Llama al XML de CBP una sola vez y devuelve dict con todos los puertos.
    Formato: { 'Nombre Puerto': { espera_minutos, espera_fast, lanes_open, ... } }
    """
    url = _get_cbp_url()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/xml, text/xml, */*",
        "Referer": "https://bwt.cbp.gov/",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"CBP API error: {e}")
        return {}

    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as e:
        logger.error(f"XML parse error: {e}")
        return {}

    puertos = {}
    timestamp = datetime.now().strftime("%H:%M:%S")

    for port in root.iter("port"):
        nombre = port.findtext("port_name", "").strip()
        crossing = port.findtext("crossing_name", "").strip()
        port_status = port.findtext("port_status", "").strip()

        # Extraer espera comercial navegando la estructura anidada
        espera_std = None
        espera_fast = None
        lanes_open = ""
        update_time = ""
        commercial_op_status = ""
        
        # Buscar element commercial_vehicle_lanes
        commercial_lanes = port.find("commercial_vehicle_lanes")
        if commercial_lanes is not None:
            # Buscar standard_lanes dentro de commercial_vehicle_lanes
            standard_lanes = commercial_lanes.find("standard_lanes")
            if standard_lanes is not None:
                delay_text = standard_lanes.findtext("delay_minutes", "")
                if delay_text and delay_text.strip().isdigit():
                    espera_std = int(delay_text)
                lanes_open = standard_lanes.findtext("lanes_open", "").strip()
                update_time = standard_lanes.findtext("update_time", "").strip()
                commercial_op_status = standard_lanes.findtext("operational_status", "").strip()
            
            # Buscar FAST_lanes dentro de commercial_vehicle_lanes
            fast_lanes = commercial_lanes.find("FAST_lanes")
            if fast_lanes is not None:
                delay_text = fast_lanes.findtext("delay_minutes", "")
                if delay_text and delay_text.strip().isdigit():
                    espera_fast = int(delay_text)
        
        hours = port.findtext("hours", "")

        key = f"{nombre} / {crossing}" if crossing else nombre
        puertos[key] = {
            "port_name": nombre,
            "crossing_name": crossing,
            "espera_minutos": espera_std,
            "espera_fast_minutos": espera_fast,
            "lanes_open": lanes_open,
            "port_status": port_status,
            "commercial_op_status": commercial_op_status,
            "hours": hours,
            "update_time": update_time,
            "actualizado": timestamp,
            "fuente": "CBP API (Tiempo Real)",
            "metodo": "xml_waittimes",
        }

    return puertos


# ============================================================================
# API PÚBLICA — misma interfaz que antes para no romper el page
# ============================================================================

def obtener_espera_puerto(puerto_codigo: str, usar_selenium: bool = False) -> dict:
    """
    Devuelve datos de espera para un puerto.
    puerto_codigo puede ser un nombre de puerto o código legacy.
    """
    todos = _fetch_todos_los_puertos()

    if not todos:
        return _fallback(puerto_codigo)

    # Buscar coincidencia por nombre exacto primero
    if puerto_codigo in todos:
        return todos[puerto_codigo]

    # Buscar coincidencia parcial (case-insensitive)
    codigo_lower = puerto_codigo.lower()
    for key, data in todos.items():
        if codigo_lower in key.lower() or codigo_lower in data.get("port_name", "").lower():
            return data

    return _fallback(puerto_codigo)


def obtener_datos_region(region: str = "mexico") -> list[dict]:
    """
    Devuelve lista de puertos con datos para una región completa.
    region: "mexico" | "canada"
    """
    todos = _fetch_todos_los_puertos()
    mapa = PUERTOS_MEXICO if region == "mexico" else PUERTOS_CANADA
    resultado = []

    for cbp_name, display_name in mapa.items():
        # Buscar en el XML por nombre (exacto, parcial, o palabras clave)
        datos = None
        cbp_lower = cbp_name.lower()
        for key, data in todos.items():
            key_lower = key.lower()
            port_lower = data.get("port_name", "").lower()
            if (
                cbp_lower in key_lower
                or cbp_lower in port_lower
                or key_lower in cbp_lower  # e.g. "East" in "Calexico East"
            ):
                datos = data
                break

        if datos is None:
            datos = _fallback(cbp_name)

        espera = datos.get("espera_minutos")
        port_status = datos.get("port_status", "")

        if espera is None:
            estado_emoji = "⚫"
            espera_display = "N/A"
        elif port_status.lower() == "closed":
            estado_emoji = "⚫"
            espera_display = "Closed"
        elif espera < 20:
            estado_emoji = "🟢"
            espera_display = espera
        elif espera < 40:
            estado_emoji = "🟡"
            espera_display = espera
        else:
            estado_emoji = "🔴"
            espera_display = espera

        resultado.append({
            "Estado": estado_emoji,
            "Puerto": display_name,
            "Espera (min)": espera if espera is not None else -1,
            "Espera Display": espera_display,
            "FAST (min)": datos.get("espera_fast_minutos", ""),
            "Carriles": datos.get("lanes_open", ""),
            "Status": port_status,
            "_datos": datos,
        })

    return sorted(resultado, key=lambda x: x["Espera (min)"], reverse=True)


def widget_espera_rapido(puerto_codigo: str, width: str = "small") -> None:
    """Widget compacto para dashboards."""
    datos = obtener_espera_puerto(puerto_codigo)
    espera = datos.get("espera_minutos", "—")
    espera_str = f"{espera} min" if isinstance(espera, int) else "—"

    sizes = {"small": "1.2rem", "medium": "1.5rem", "large": "2rem"}
    font = sizes.get(width, "1.2rem")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#ff9800,#f57c00);
                border-radius:12px;padding:16px;text-align:center;
                color:white;font-size:{font};
                box-shadow:0 4px 12px rgba(0,0,0,0.15);">
        <div style="font-size:0.8rem;opacity:0.9;">⏱️ Espera</div>
        <div style="font-weight:bold;">{espera_str}</div>
        <div style="font-size:0.7rem;opacity:0.7;margin-top:4px;">CBP</div>
    </div>
    """, unsafe_allow_html=True)


def _fallback(puerto_codigo: str) -> dict:
    return {
        "puerto": puerto_codigo,
        "espera_minutos": None,
        "espera_fast_minutos": None,
        "lanes_open": "",
        "port_status": "Unknown",
        "hours": "",
        "update_time": "",
        "actualizado": datetime.now().strftime("%H:%M:%S"),
        "fuente": "API sin respuesta",
        "metodo": "fallback",
    }

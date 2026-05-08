"""
Función reutilizable para crear tarjetas KPI con estilos profesionales
Usa estilos INLINE para que funcione correctamente en Streamlit
"""

import streamlit as st
from typing import Optional

def tarjeta_kpi(
    titulo: str,
    valor: str,
    icono: str = "📊",
    delta: Optional[str] = None,
    color_borde: str = "#0066cc",
    color_fondo_rgb: str = "rgba(0, 102, 204, 0.12)",
    color_valor: str = "#0066cc",
    color_titulo: str = "#0052a3",
    columnas: int = 1,
    ancho_completo: bool = False
):
    """
    Crea una tarjeta KPI profesional con estilos inline.
    """
    
    # Estilo base - TODO EN UNA LÍNEA (sin saltos de línea)
    estilo_tarjeta = f"border-radius: 14px; border: 2px solid {color_borde}; background: linear-gradient(135deg, {color_fondo_rgb} 0%, rgba(25, 118, 210, 0.08) 100%); padding: 24px 20px; text-align: center; box-shadow: 0 0 20px rgba(0, 102, 204, 0.2), 0 8px 24px rgba(0, 0, 0, 0.1), inset 0 1px 2px rgba(255, 255, 255, 0.1); transition: all 0.3s ease; width: {'100%' if ancho_completo else 'auto'};"
    
    # HTML de la tarjeta - TODO EN UNA LÍNEA
    html = f'<div style="{estilo_tarjeta}"><div style="color: {color_titulo}; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">{icono} {titulo}</div><div style="color: {color_valor}; font-size: 25px; font-weight: 900; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3); margin: 8px 0;">{valor}</div>'
    
    # Agregar delta si existe
    if delta:
        html += f'<div style="color: {color_borde}; font-size: 0.95rem; font-weight: 700; margin-top: 8px;">{delta}</div>'
    
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)


def tarjeta_kpi_simple(titulo: str, valor: str, icono: str = "📊"):
    """
    Versión simplificada - azul profesional por defecto
    """
    tarjeta_kpi(
        titulo=titulo,
        valor=valor,
        icono=icono,
        color_borde="#0066cc",
        color_fondo_rgb="rgba(0, 102, 204, 0.12)",
        color_valor="#0066cc",
        color_titulo="#0052a3"
    )


# Presets de colores profesionales
COLORES = {
    "azul_primario": {
        "color_borde": "#0066cc",
        "color_fondo_rgb": "rgba(0, 102, 204, 0.12)",
        "color_valor": "#0066cc",
        "color_titulo": "#0052a3",
    },
    "verde": {
        "color_borde": "#4CAF50",
        "color_fondo_rgb": "rgba(76, 175, 80, 0.12)",
        "color_valor": "#388E3C",
        "color_titulo": "#2E7D32",
    },
    "rojo": {
        "color_borde": "#F44336",
        "color_fondo_rgb": "rgba(244, 67, 54, 0.12)",
        "color_valor": "#F44336",
        "color_titulo": "#C62828",
    },
    "naranja": {
        "color_borde": "#FF9800",
        "color_fondo_rgb": "rgba(255, 152, 0, 0.12)",
        "color_valor": "#FF9800",
        "color_titulo": "#E65100",
    },
    "morado": {
        "color_borde": "#9C27B0",
        "color_fondo_rgb": "rgba(156, 39, 176, 0.12)",
        "color_valor": "#9C27B0",
        "color_titulo": "#6A1B9A",
    },
    "turquesa": {
        "color_borde": "#00BCD4",
        "color_fondo_rgb": "rgba(0, 188, 212, 0.12)",
        "color_valor": "#00BCD4",
        "color_titulo": "#00695C",
    },
    "azul_canada": {
        "color_borde": "#2196F3",
        "color_fondo_rgb": "rgba(33, 150, 243, 0.12)",
        "color_valor": "#1565C0",
        "color_titulo": "#0D47A1",
    },
}


def tarjeta_kpi_color(titulo: str, valor: str, icono: str = "📊", 
                      color_preset: str = "azul_primario", 
                      delta: Optional[str] = None):
    """
    Crea una tarjeta con un color de preset.
    
    Args:
        titulo: Nombre de la métrica
        valor: Valor a mostrar
        icono: Emoji
        color_preset: Uno de los presets en COLORES
        delta: Diferencia
    """
    colores = COLORES.get(color_preset, COLORES["azul_primario"])
    tarjeta_kpi(
        titulo=titulo,
        valor=valor,
        icono=icono,
        delta=delta,
        **colores
    )

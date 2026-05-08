"""
Card Styles Helper - Componentes de tarjetas con estilo tecnológico profesional
para uso en todas las páginas del dashboard.
"""

import streamlit as st


def crear_tarjeta_kpi(titulo, valor, icono="📊", color="#0066cc", delta=None, descripcion=""):
    """
    Crea una tarjeta KPI con efecto glow, glassmorphism y sombra profesional.
    
    Args:
        titulo: Título de la tarjeta (se convierte a mayúsculas)
        valor: Valor principal a mostrar (número, porcentaje, etc.)
        icono: Emoji o icono a mostrar
        color: Color hex del glow (#0066cc, #1976d2, #0052a3)
        delta: Texto de cambio/delta opcional (ej: "+5.2%")
        descripcion: Descripción adicional bajo el valor
    """
    
    # Validar color si es necesario
    colores_validos = {
        '#0066cc': 'rgba(0, 102, 204, 0.4)',
        '#1976d2': 'rgba(25, 118, 210, 0.35)',
        '#0052a3': 'rgba(0, 82, 163, 0.35)',
        '#003d7a': 'rgba(0, 61, 122, 0.4)',
    }
    
    glow_color = colores_validos.get(color, 'rgba(0, 102, 204, 0.4)')
    
    html_content = f"""
    <div style='
        background: linear-gradient(135deg, rgba(0, 61, 122, 0.12) 0%, rgba(0, 82, 163, 0.08) 100%);
        padding: 24px;
        border-radius: 14px;
        border: 2px solid {color};
        box-shadow: 0 0 20px {glow_color}, 0 8px 24px rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    '>
        <div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;'>
            <h4 style='margin: 0; color: {color}; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;'>{titulo}</h4>
            <span style='font-size: 1.4rem; opacity: 0.8;'>{icono}</span>
        </div>
        <p style='font-size: 2.2rem; font-weight: 900; margin: 12px 0; color: {color}; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);'>{valor}</p>
        {f'<p style="color: {color}; margin: 8px 0 0 0; font-size: 0.85rem; font-weight: 500; opacity: 0.9;">📈 {delta}</p>' if delta else ''}
        {f'<p style="color: #003d7a; margin: 0; font-size: 0.9rem; opacity: 0.85; font-weight: 500;">{descripcion}</p>' if descripcion else ''}
    </div>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)


def crear_fila_tarjetas(tarjetas_config):
    """
    Crea una fila de tarjetas en columnas automáticas.
    
    Args:
        tarjetas_config: Lista de diccionarios con configuración de tarjetas
                        Ejemplo: [
                            {
                                'titulo': 'Total Aduanas',
                                'valor': '37',
                                'icono': '🏛️',
                                'color': '#0066cc',
                                'delta': '+5%',
                                'descripcion': 'Activas'
                            },
                            ...
                        ]
    """
    
    num_cols = len(tarjetas_config)
    cols = st.columns(num_cols)
    
    for col, config in zip(cols, tarjetas_config):
        with col:
            crear_tarjeta_kpi(
                titulo=config.get('titulo', 'Sin título'),
                valor=config.get('valor', '0'),
                icono=config.get('icono', '📊'),
                color=config.get('color', '#0066cc'),
                delta=config.get('delta'),
                descripcion=config.get('descripcion', '')
            )


# Colores predefinidos para mantener consistencia
COLORES_PROFESIONALES = {
    'primario': '#003d7a',      # Azul oscuro profesional
    'secundario': '#0052a3',    # Azul medio
    'acentuado': '#1976d2',     # Azul tech
    'brillante': '#0066cc',     # Azul brillante
}

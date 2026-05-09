"""
Página: Tiempos de Espera CBP
Muestra datos en tiempo real de tiempos de espera en puertos de entrada

Versión: 1.0.0
Fecha: 2026-05-07
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import requests
from pathlib import Path
import sys

# Agregar módulos al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.cbp_wait_times import (
    obtener_espera_puerto,
    obtener_datos_region,
    widget_espera_rapido,
    CBP_API_PORTS
)
from modules.port_hours import obtener_horarios_puerto


def page_cbp_wait_times():
    """
    Página principal de tiempos de espera CBP
    """
    
    st.set_page_config(
        page_title="Tiempos de Espera CBP",
        page_icon="🚚",
        layout="wide"
    )
    
    # ========================================================================
    # HEADER
    # ========================================================================
    
    st.title("🚚 Tiempos de Espera - Puertos de Entrada USA-México")
    
    st.markdown("""
    **Datos en tiempo real** de U.S. Customs and Border Protection (CBP)
    
    Esta página monitorea los tiempos de espera actuales en los principales 
    puertos fronterizos México-USA. Los datos se actualizan automáticamente cada 5 minutos.
    """)
    
    st.markdown("---")
    
    # ========================================================================
    # SECCIÓN 1: SELECCIÓN DE REGIÓN (Similar a CBP.gov)
    # ========================================================================
    
    # Definir puertos por región — claves CBP (nombre exacto del XML waittimes)
    puertos_mexico = {
        # TEXAS - Laredo
        "Laredo - World Trade Bridge (TX)": "Laredo / World Trade Bridge",
        "Laredo - Colombia Solidarity (TX)": "Laredo / Colombia Solidarity",
        "Laredo - Bridge I (TX)": "Laredo / Bridge I",
        "Laredo - Bridge II (TX)": "Laredo / Bridge II",
        # TEXAS - Brownsville
        "Brownsville - B&M (TX)": "Brownsville / B&M",
        "Brownsville - Los Indios (TX)": "Brownsville / Los Indios",
        "Brownsville - Veterans International (TX)": "Brownsville / Veterans International",
        # TEXAS - Pharr/Hidalgo
        "Hidalgo (TX)": "Hidalgo/Pharr / Hidalgo",
        "Pharr (TX)": "Hidalgo/Pharr / Pharr",
        "Anzalduas International Bridge (TX)": "Hidalgo/Pharr / Anzalduas International Bridge",
        # TEXAS - Other
        "Rio Grande City (TX)": "Rio Grande City",
        "Progreso - Progreso International (TX)": "Progreso / Progreso International Bridge",
        "Progreso - Donna International (TX)": "Progreso / Donna International Bridge",
        "Roma (TX)": "Roma",
        "Del Rio (TX)": "Del Rio",
        "Eagle Pass - Bridge I (TX)": "Eagle Pass / Bridge I",
        "Eagle Pass - Bridge II (TX)": "Eagle Pass / Bridge II",
        "Presidio (TX)": "Presidio",
        "Tornillo (TX)": "Marcelino Serna / Tornillo",
        # TEXAS - El Paso
        "El Paso - Ysleta (TX)": "El Paso / Ysleta",
        "El Paso - Paso Del Norte (TX)": "El Paso / Paso Del Norte (PDN)",
        "El Paso - Bridge of the Americas (TX)": "El Paso / Bridge of the Americas (BOTA)",
        "Santa Teresa (NM)": "Santa Teresa / Santa Teresa Port of Entry",
        "Columbus (NM)": "Columbus",
        # CALIFORNIA
        "Otay Mesa - Commercial (CA)": "Otay Mesa / Commercial",
        "San Ysidro (CA)": "San Ysidro",
        "Calexico East (CA)": "Calexico / East",
        "Calexico West (CA)": "Calexico / West",
        "Tecate (CA)": "Tecate",
        # ARIZONA
        "Nogales - Mariposa (AZ)": "Nogales / Mariposa",
        "Nogales - Deconcini (AZ)": "Nogales / Deconcini",
        "Douglas (AZ)": "Douglas (Raul Hector Castro)",
        "Naco (AZ)": "Naco",
        "Lukeville (AZ)": "Lukeville",
        "San Luis I (AZ)": "San Luis / San Luis I",
        "San Luis II (AZ)": "San Luis / San Luis II",
    }
    
    puertos_canada = {
        # WEST COAST
        "Blaine - Pacific Highway (WA)": "Blaine / Pacific Highway",
        "Blaine - Peace Arch (WA)": "Blaine / Peace Arch",
        "Blaine - Point Roberts (WA)": "Blaine / Point Roberts",
        "Sumas (WA)": "Sumas",
        "Lynden (WA)": "Lynden",
        # MONTANA
        "Sweetgrass (MT)": "Sweetgrass",
        # NORTH DAKOTA
        "Pembina (ND)": "Pembina",
        # MINNESOTA
        "International Falls (MN)": "International Falls",
        # MICHIGAN
        "Sault Ste. Marie (MI)": "Sault Ste. Marie / International Bridge - SSM",
        "Detroit - Ambassador Bridge (MI)": "Detroit / Ambassador Bridge",
        "Detroit - Windsor Tunnel (MI)": "Detroit / Windsor Tunnel",
        "Port Huron - Bluewater Bridge (MI)": "Port Huron / Bluewater Bridge",
        # NEW YORK
        "Buffalo/Niagara Falls - Peace Bridge (NY)": "Buffalo/Niagara Falls / Peace Bridge",
        "Buffalo/Niagara Falls - Rainbow Bridge (NY)": "Buffalo/Niagara Falls / Rainbow Bridge",
        "Buffalo/Niagara Falls - Lewiston Bridge (NY)": "Buffalo/Niagara Falls / Lewiston Bridge",
        "Alexandria Bay - Thousand Islands Bridge (NY)": "Alexandria Bay / Thousand Islands Bridge",
        "Ogdensburg (NY)": "Ogdensburg",
        "Massena (NY)": "Massena",
        "Champlain (NY)": "Champlain",
        # VERMONT
        "Highgate Springs (VT)": "Highgate Springs",
        "Derby Line (VT)": "Derby Line / Derby Line I-91",
        "Norton (VT)": "Norton",
        # MAINE
        "Calais - Ferry Point (ME)": "Calais / Ferry Point",
        "Calais - International Avenue (ME)": "Calais / International Avenue",
        "Houlton (ME)": "Houlton",
        "Jackman (ME)": "Jackman",
    }
    
    # Botones para seleccionar región (estilo CBP)
    col1, col2 = st.columns(2)
    
    with col1:
        btn_mexico = st.button(
            "🇲🇽 Mexican Border Ports of Entry",
            use_container_width=True,
            key="btn_mexico"
        )
    
    with col2:
        btn_canada = st.button(
            "🇨🇦 Canadian Border Ports of Entry",
            use_container_width=True,
            key="btn_canada"
        )
    
    # Estado de la región seleccionada
    if "region_actual" not in st.session_state:
        st.session_state.region_actual = "mexico"
    
    if btn_mexico:
        st.session_state.region_actual = "mexico"
    if btn_canada:
        st.session_state.region_actual = "canada"
    
    # Mostrar región seleccionada
    if st.session_state.region_actual == "mexico":
        st.markdown("### 🇲🇽 **Mexican Border Ports of Entry**")
        puertos_region = puertos_mexico
        titulo_region = "Mexican"
    else:
        st.markdown("### 🇨🇦 **Canadian Border Ports of Entry**")
        puertos_region = puertos_canada
        titulo_region = "Canadian"
    
    st.markdown("---")
    
    # Selectbox para puerto individual
    col_select, col_action = st.columns([3, 1])
    
    with col_select:
        puerto_seleccionado = st.selectbox(
            "Select a port:",
            list(puertos_region.keys()),
            index=0
        )
    
    puerto_codigo = puertos_region[puerto_seleccionado]
    
    with col_action:
        st.write("")
        st.write("")
        actualizar = st.button("🔄 Refresh", use_container_width=True)
    
    # Obtener datos del puerto
    datos_puerto = obtener_espera_puerto(puerto_codigo)
    
    if datos_puerto:
        # Mostrar datos en formato similar a CBP
        col_puerto, col_info = st.columns([2, 2])
        
        with col_puerto:
            espera = datos_puerto.get('espera_minutos')
            espera_fast = datos_puerto.get('espera_fast_minutos')
            port_status = datos_puerto.get('port_status', '')
            
            if espera is None:
                display_val = "N/A"
                estado = "DESCONOCIDO"
                color = "#9E9E9E"
            elif port_status and port_status.lower() == 'closed':
                display_val = "CERRADO"
                estado = "CLOSED"
                color = "#9E9E9E"
            else:
                display_val = str(espera)
                estado = "NORMAL" if espera < 20 else "MODERADO" if espera < 40 else "CRÍTICO"
                color = "#4CAF50" if estado == "NORMAL" else "#FFC107" if estado == "MODERADO" else "#F44336"
            
            fast_html = ""
            if espera_fast is not None and espera_fast > 0:
                fast_html = f'<div style="font-size: 0.8rem; opacity: 0.85; margin-top: 6px;">FAST: {espera_fast} min</div>'
            
            lanes = datos_puerto.get('lanes_open', '')
            lanes_html = f'<div style="font-size: 0.8rem; opacity: 0.75; margin-top: 4px;">Lanes open: {lanes}</div>' if lanes else ""
            
            extras = fast_html + lanes_html

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}, {color}dd); 
                        border-radius: 8px; padding: 25px; text-align: center; color: white;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
                <div style="font-size: 0.85rem; opacity: 0.9; margin-bottom: 10px; font-weight: 500;">CURRENT WAIT TIME (COMMERCIAL)</div>
                <div style="font-size: 3rem; font-weight: 900;">{display_val}</div>
                <div style="font-size: 0.9rem; opacity: 0.85; margin-top: 8px;">{'minutes \u2022 ' + estado if espera is not None else estado}</div>{extras}
            </div>
            """, unsafe_allow_html=True)
        
        with col_info:
            update_time = datos_puerto.get('update_time', '') or datos_puerto.get('actualizado', '—')
            hours_info = datos_puerto.get('hours', '')
            hours_html = f'<div style="font-size: 0.85rem; color: #666; margin-bottom: 4px;"><b>Hours:</b> {hours_info}</div>' if hours_info else ""
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f5f5f5, #eeeeee); 
                        border-radius: 8px; padding: 20px; text-align: left; color: #333;
                        border-left: 4px solid #1976d2;">
                <div style="font-size: 0.85rem; color: #666; margin-bottom: 12px;"><b>PORT INFORMATION</b></div>
                <div style="font-size: 1rem; font-weight: 600; margin-bottom: 8px;">{puerto_seleccionado}</div>
                <div style="font-size: 0.85rem; color: #666; margin-bottom: 4px;">
                    <b>Port:</b> {datos_puerto.get('port_name', '') or datos_puerto.get('crossing_name', '')}
                </div>
                <div style="font-size: 0.85rem; color: #666; margin-bottom: 4px;">
                    <b>Status:</b> {datos_puerto.get('port_status', '—')}
                </div>
                {hours_html}
                <div style="font-size: 0.85rem; color: #666; margin-bottom: 4px;">
                    <b>Updated:</b> {update_time}
                </div>
                <div style="font-size: 0.75rem; color: #999; margin-top: 10px; padding-top: 10px; border-top: 1px solid #ddd;">
                    Source: {datos_puerto.get('fuente', 'CBP')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Mostrar estado de la fuente de datos
        if datos_puerto.get('metodo') == 'xml_waittimes':
            st.success("✅ Real-time data from CBP API")
        elif datos_puerto.get('metodo') == 'fallback':
            st.warning("⚠️ Datos no disponibles (API sin respuesta)")
        else:
            st.info(f"ℹ️ Fuente: {datos_puerto.get('metodo', '?')}")
        
        st.markdown("")
        
        # ====================================================================
        # HORARIOS DE OPERACIÓN
        # ====================================================================
        
        horarios = obtener_horarios_puerto(puerto_codigo)
        
        st.subheader("⏰ Operating Hours")
        
        col_dias, col_notas = st.columns([2, 1])
        
        with col_dias:
            # Tabla de horarios
            datos_horarios = [
                {
                    "Type": "🚗 Export (M-F)",
                    "Hours": horarios.get('exportacion_lv', '—')
                },
                {
                    "Type": "📦 Import (M-F)", 
                    "Hours": horarios.get('importacion_lv', '—')
                },
                {
                    "Type": "🏖️ Weekend (Sat-Sun)",
                    "Hours": horarios.get('fin_semana', '—')
                },
                {
                    "Type": "🎉 Holiday",
                    "Hours": horarios.get('dia_festivo', '—')
                }
            ]
            
            df_horarios = pd.DataFrame(datos_horarios)
            st.dataframe(
                df_horarios,
                use_container_width=True,
                hide_index=True,
                column_config={
                    'Type': st.column_config.TextColumn('Type', width=150),
                    'Hours': st.column_config.TextColumn('Hours', width=150),
                }
            )
        
        with col_notas:
            if horarios.get('notas'):
                st.markdown(f"""
                <div style="background: #f0f7ff; border-left: 4px solid #2196F3; padding: 12px; border-radius: 4px; margin-top: 12px;">
                    <div style="font-size: 0.8rem; color: #666; font-weight: 600; margin-bottom: 4px;">NOTES</div>
                    <div style="font-size: 0.85rem; color: #333;">{horarios.get('notas')}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECCIÓN 2: COMPARATIVA DE PUERTOS EN LA REGIÓN
    # ========================================================================
    
    st.subheader(f"📊 All {titulo_region} Ports - Wait Times Comparison")
    
    with st.expander("ℹ️ How the data works"):
        st.markdown("""
        - **Real-time Updates**: Data refreshes every minute from CBP API
        - **Caching**: Displayed data comes from cache for fast loading (2-5 seconds)
        - **Manual Refresh**: Click the "Refresh" button to force live web scraping (slower but most accurate)
        - **Status Colors**: 🟢 Normal (<20 min) | 🟡 Moderate (<40 min) | 🔴 Critical (>40 min)
        """)
    
    # Cargar datos usando las claves exactas del XML (sin ambigüedad en búsqueda)
    datos_comparativos = []
    for nombre_display, cbp_xml_key in puertos_region.items():
        datos = obtener_espera_puerto(cbp_xml_key)
        espera = datos.get('espera_minutos')
        port_status = datos.get('port_status', '')
        commercial_op = datos.get('commercial_op_status', '').upper()

        sin_cvl = (commercial_op == 'N/A' or commercial_op == '') and espera is None

        if port_status.lower() == 'closed':
            estado_emoji = "⚫"
            espera_display = "Closed"
        elif sin_cvl:
            estado_emoji = "⚪"
            espera_display = "Sin CVL"
        elif espera is None:
            estado_emoji = "⚫"
            espera_display = "N/A"
        elif espera < 20:
            estado_emoji = "🟢"
            espera_display = espera
        elif espera < 40:
            estado_emoji = "🟡"
            espera_display = espera
        else:
            estado_emoji = "🔴"
            espera_display = espera

        datos_comparativos.append({
            'Estado': estado_emoji,
            'Puerto': nombre_display,
            'Espera (min)': espera if espera is not None else -1,
            'Espera Display': espera_display,
            'FAST (min)': datos.get('espera_fast_minutos', ''),
            'Carriles': datos.get('lanes_open', ''),
            'Status': port_status,
        })

    df_comparativa = pd.DataFrame(datos_comparativos)
    df_comparativa = df_comparativa.sort_values('Espera (min)', ascending=False)
    
    # Mostrar tabla
    col_tabla, col_chart = st.columns([1.2, 1])
    
    with col_tabla:
        st.dataframe(
            df_comparativa[['Estado', 'Puerto', 'Espera Display', 'FAST (min)', 'Carriles', 'Status']].rename(
                columns={'Espera Display': 'Espera (min)'}
            ),
            use_container_width=True,
            hide_index=True,
            column_config={
                'Estado': st.column_config.TextColumn('', width=40),
                'Puerto': st.column_config.TextColumn('Port', width=150),
                'Espera (min)': st.column_config.TextColumn('Wait (min)', width=90),
                'FAST (min)': st.column_config.TextColumn('FAST', width=70),
                'Carriles': st.column_config.TextColumn('Lanes', width=60),
                'Status': st.column_config.TextColumn('Status', width=80),
            }
        )
    
    with col_chart:
        # Solo graficar puertos con datos numéricos
        df_chart = df_comparativa[df_comparativa['Espera (min)'] >= 0].copy()
        fig = go.Figure(data=[
            go.Bar(
                y=df_chart['Puerto'],
                x=df_chart['Espera (min)'],
                orientation='h',
                marker=dict(
                    color=df_chart['Espera (min)'],
                    colorscale='RdYlGn_r',
                    showscale=False
                ),
                text=df_chart['Espera (min)'].apply(lambda x: f"{x} min"),
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>Wait: %{x} min<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=f"{titulo_region} Ports",
            xaxis_title="Wait Time (minutes)",
            yaxis_title="",
            height=400,
            showlegend=False,
            margin=dict(l=150, r=50, t=50, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECCIÓN 3: INFORMACIÓN Y FUENTES
    # ========================================================================
    
    st.subheader("ℹ️ Information & Sources")
    
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.markdown("""
        **📍 Data Source**
        
        - U.S. Customs and Border Protection (CBP)
        - Border Wait Times Portal
        - Real-time API
        """)
    
    with col_info2:
        st.markdown("""
        **🔄 Updates**
        
        - Data updated every minute
        - Local cache storage
        - Available 24/7
        """)
    
    with col_info3:
        st.markdown("""
        **🔗 Useful Links**
        
        - [CBP Wait Times](https://bwt.cbp.gov)
        - [General Info](https://www.cbp.gov)
        - [RSS Feeds](https://bwt.cbp.gov/xml/bwt.xml)
        """)
    
    st.caption("ℹ️ Los tiempos de espera mostrados son estimados basados en datos oficiales de CBP. Pueden variar según condiciones operacionales.")


if __name__ == "__main__":
    page_cbp_wait_times()

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
    
    # Definir puertos por región
    puertos_mexico = {
        # TEXAS
        "Laredo (TX)": "06480101",
        "Brownsville (TX)": "06471001",
        "Rio Grande City (TX)": "06472001",
        "Progreso (TX)": "06473001",
        "Roma (TX)": "06474001",
        "Del Rio (TX)": "06481001",
        "Eagle Pass (TX)": "06500601",
        "Presidio (TX)": "06483001",
        "Tornillo (TX)": "06452401",
        "Ysleta (TX)": "06450702",
        "El Paso (TX)": "06450701",
        "Santa Teresa (NM)": "06451701",
        "Columbus (NM)": "07203001",
        
        # CALIFORNIA-ARIZONA
        "Otay Mesa (CA)": "09250602",
        "San Ysidro (CA)": "09250101",
        "Calexico East (CA)": "09251202",
        "Tecate (CA)": "09250702",
        
        # ARIZONA
        "Nogales (AZ)": "07200601",
        "Douglas (AZ)": "07201001",
        "Naco (AZ)": "07202001",
        "Lukeville (AZ)": "07204001",
        "San Luis (AZ)": "07150501",
    }
    
    puertos_canada = {
        # WEST COAST
        "Blaine (WA)": "05200101",
        "Point Roberts (WA)": "05220101",
        "Bellingham (WA)": "05230101",
        "Sumas (WA)": "05240101",
        "Lynden (WA)": "05210101",
        "Port Angeles (WA)": "05250101",
        
        # MONTANA-IDAHO
        "Sweetgrass (MT)": "04640101",
        "Piegan (MT)": "04660101",
        "Turner (MT)": "04670101",
        
        # NORTH DAKOTA
        "Pembina (ND)": "04620101",
        "Portal (ND)": "04680101",
        "Dunseith (ND)": "04570101",
        "Fortuna (ND)": "04690101",
        
        # MINNESOTA
        "International Falls (MN)": "04600101",
        "Baudette (MN)": "04520101",
        "Janesville (MN)": "04700101",
        
        # MICHIGAN
        "Sault Ste Marie (MI)": "04710101",
        "Mackinac Bridge (MI)": "04720101",
        
        # NEW YORK - VERMONT
        "Buffalo Niagara Falls (NY)": "01050101",
        "Thousand Islands Bridge (NY)": "01140101",
        "Rainbow Bridge (NY)": "01110101",
        "Ogdensburg (NY)": "01100101",
        "Champlain Rouses Point (NY)": "01070101",
        "Highgate Springs (VT)": "01090101",
        "Alburgh (VT)": "01150101",
        
        # MAINE
        "Calais (ME)": "01060101",
        "Houlton (ME)": "01160101",
        "Van Buren (ME)": "01170101",
        "Jackman (ME)": "01180101",
        "Coburn Gore (ME)": "01190101",
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
            espera = datos_puerto.get('espera_minutos', 0)
            estado = "NORMAL" if espera < 20 else "MODERADO" if espera < 40 else "CRÍTICO"
            color = "#4CAF50" if estado == "NORMAL" else "#FFC107" if estado == "MODERADO" else "#F44336"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}, {color}dd); 
                        border-radius: 8px; padding: 25px; text-align: center; color: white;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
                <div style="font-size: 0.85rem; opacity: 0.9; margin-bottom: 10px; font-weight: 500;">CURRENT WAIT TIME</div>
                <div style="font-size: 3rem; font-weight: 900;">{espera}</div>
                <div style="font-size: 0.9rem; opacity: 0.85; margin-top: 8px;">minutes • {estado}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_info:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f5f5f5, #eeeeee); 
                        border-radius: 8px; padding: 20px; text-align: left; color: #333;
                        border-left: 4px solid #1976d2;">
                <div style="font-size: 0.85rem; color: #666; margin-bottom: 12px;"><b>PORT INFORMATION</b></div>
                <div style="font-size: 1rem; font-weight: 600; margin-bottom: 8px;">{puerto_seleccionado}</div>
                <div style="font-size: 0.85rem; color: #666; margin-bottom: 4px;">
                    <b>Code:</b> {puerto_codigo}
                </div>
                <div style="font-size: 0.85rem; color: #666; margin-bottom: 4px;">
                    <b>Updated:</b> {datos_puerto.get('actualizado', '—')}
                </div>
                <div style="font-size: 0.75rem; color: #999; margin-top: 10px; padding-top: 10px; border-top: 1px solid #ddd;">
                    Source: {datos_puerto.get('fuente', 'CBP')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Mostrar estado de la fuente de datos
        if datos_puerto.get('metodo') == 'rss':
            st.success("✅ Real-time data from CBP API")
        elif datos_puerto.get('metodo') == 'selenium':
            st.info("🔄 Live data via web scraping")
        else:
            st.warning("⚠️ Simulated data (API currently unavailable)")
        
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
    
    # Cargar datos de todos los puertos en la región (desde caché)
    st.write(f"Loading {len(puertos_region)} ports...")
    
    datos_comparativos = []
    for puerto_nombre, puerto_cod in puertos_region.items():
        datos = obtener_espera_puerto(puerto_cod)
        espera = datos.get('espera_minutos', 0)
        
        # Clasificar estado
        if espera < 20:
            estado_emoji = "🟢"
        elif espera < 40:
            estado_emoji = "🟡"
        else:
            estado_emoji = "🔴"
        
        datos_comparativos.append({
            'Estado': estado_emoji,
            'Puerto': puerto_nombre,
            'Espera (min)': espera,
        })
    
    df_comparativa = pd.DataFrame(datos_comparativos)
    df_comparativa = df_comparativa.sort_values('Espera (min)', ascending=False)
    
    # Mostrar tabla
    col_tabla, col_chart = st.columns([1.2, 1])
    
    with col_tabla:
        st.dataframe(
            df_comparativa,
            use_container_width=True,
            hide_index=True,
            column_config={
                'Estado': st.column_config.TextColumn('Status', width=50),
                'Puerto': st.column_config.TextColumn('Port', width=150),
                'Espera (min)': st.column_config.NumberColumn('Wait (min)', width=100),
            }
        )
    
    with col_chart:
        fig = go.Figure(data=[
            go.Bar(
                y=df_comparativa['Puerto'],
                x=df_comparativa['Espera (min)'],
                orientation='h',
                marker=dict(
                    color=df_comparativa['Espera (min)'],
                    colorscale='RdYlGn_r',
                    showscale=False
                ),
                text=df_comparativa['Espera (min)'].apply(lambda x: f"{x} min"),
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

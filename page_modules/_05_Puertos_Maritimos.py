"""
Página: Puertos Marítimos Mexicanos
Análisis de capacidad, operaciones y congestión portuaria
Versión: 2.0 (Refactorizada)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from pathlib import Path

from modules.constants import (
    MONTHS_MAP, COLOR_PALETTE, SATURATION_LEVELS, WAIT_TIME_LEVELS
)
from modules.session_init import page_header, section_header, spacer


# Constantes Locales de Puertos Mexicanos
PUERTOS_PRINCIPALES = {
    'Manzanillo': {'lat': 19.0522, 'lon': -104.3158, 'region': 'Pacífico', 'capacidad_anual': 3840000},
    'Lázaro Cárdenas': {'lat': 17.9585, 'lon': -102.1891, 'region': 'Pacífico', 'capacidad_anual': 2160000},
    'Veracruz': {'lat': 19.1738, 'lon': -96.1342, 'region': 'Atlántico', 'capacidad_anual': 1320000},
    'Altamira': {'lat': 22.3943, 'lon': -97.9377, 'region': 'Golfo', 'capacidad_anual': 1140000},
    'Ensenada': {'lat': 31.8667, 'lon': -116.6000, 'region': 'Pacífico', 'capacidad_anual': 900000},
    'Tuxpan': {'lat': 20.9577, 'lon': -97.4054, 'region': 'Atlántico', 'capacidad_anual': 480000},
    'Mazatlán': {'lat': 23.1943, 'lon': -106.4160, 'region': 'Pacífico', 'capacidad_anual': 420000},
    'Tapachula': {'lat': 14.7516, 'lon': -92.3749, 'region': 'Pacífico', 'capacidad_anual': 240000},
    'Salina Cruz': {'lat': 16.1733, 'lon': -95.2000, 'region': 'Pacífico', 'capacidad_anual': 300000},
    'Progreso': {'lat': 21.2789, 'lon': -89.6639, 'region': 'Golfo', 'capacidad_anual': 360000},
}

RUTAS_PRINCIPALES = {
    'Manzanillo': ['Nuevo Laredo', 'Ciudad Juárez', 'Laredo'],
    'Veracruz': ['Nuevo Laredo', 'Reynosa'],
    'Lázaro Cárdenas': ['Nuevo Laredo', 'Hermosillo'],
    'Altamira': ['Nuevo Laredo', 'Ciudad Juárez'],
}


@st.cache_data(ttl=300)
def generar_datos_puertos_realistas():
    """Genera datos realistas de puertos mexicanos."""
    puertos_data = []
    
    for puerto, config in PUERTOS_PRINCIPALES.items():
        # TEU por día (variación realista)
        teu_diario = int(config['capacidad_anual'] / 365)
        variacion = np.random.normal(1.0, 0.15)
        vol_actual = int(teu_diario * variacion)
        
        saturacion = (vol_actual / (config['capacidad_anual'] / 365)) * 100
        saturacion = min(95, max(10, saturacion))  # Limitar entre 10% y 95%
        
        operaciones = int(50 + (vol_actual / teu_diario) * 450)
        
        # Determinar estado basado en saturación
        if saturacion > 80:
            estado = 'Crítico'
            color = COLOR_PALETTE['error']
        elif saturacion > 60:
            estado = 'Alto'
            color = COLOR_PALETTE['warning']
        else:
            estado = 'Normal'
            color = COLOR_PALETTE['success']
        
        puertos_data.append({
            'Puerto': puerto,
            'Región': config['region'],
            'Latitud': config['lat'],
            'Longitud': config['lon'],
            'TEU_Actual': vol_actual,
            'TEU_Mes': int(vol_actual * 25),  # Aprox 25 días de operación
            'Capacidad_Diaria': int(config['capacidad_anual'] / 365),
            'Capacidad_Mensual': int(config['capacidad_anual'] / 12),
            'Saturación': round(saturacion, 2),
            'Estado': estado,
            'Color': color,
            'Operaciones': operaciones,
            'Tiempo_Promedio_Espera': np.random.randint(12, 72),  # horas
            'Buques_Atracados': np.random.randint(5, 25),
            'Movimientos_Mes': np.random.randint(80, 180),
        })
    
    return pd.DataFrame(puertos_data)


@st.cache_data(ttl=600)
def generar_tendencias_mensuales():
    """Genera tendencias mensuales realistas."""
    tendencias = []
    
    for puerto in PUERTOS_PRINCIPALES.keys():
        base_teu = PUERTOS_PRINCIPALES[puerto]['capacidad_anual'] / 365
        for mes in pd.date_range(start='2025-04-01', end='2026-03-31', freq='ME'):
            # Variación estacional y aleatoria
            estacional = 1 + 0.2 * np.sin(mes.month * np.pi / 6)
            aleatoria = np.random.normal(1.0, 0.1)
            teu_mes = int(base_teu * 25 * estacional * aleatoria)
            
            tendencias.append({
                'Fecha': mes,
                'Puerto': puerto,
                'TEU': teu_mes,
                'Año_Mes': mes.strftime('%Y-%m')
            })
    
    return pd.DataFrame(tendencias)


def calcular_kpis_estrategicos(df_puertos):
    """Calcula KPIs estratégicos nacionales."""
    throughput_nacional = df_puertos['TEU_Mes'].sum()
    saturacion_promedio = df_puertos['Saturación'].mean()
    operaciones_totales = df_puertos['Operaciones'].sum()
    valor_comercial = throughput_nacional * 1500  # USD aproximado por TEU
    
    puertos_criticos = len(df_puertos[df_puertos['Estado'] == 'Crítico'])
    dias_espera_promedio = df_puertos['Tiempo_Promedio_Espera'].mean()
    
    return {
        'throughput_nacional': throughput_nacional,
        'saturacion_promedio': saturacion_promedio,
        'operaciones_totales': operaciones_totales,
        'valor_comercial': valor_comercial,
        'puertos_criticos': puertos_criticos,
        'dias_espera_promedio': dias_espera_promedio
    }


def page_puertos_maritimos():
    """Análisis geográfico de puertos marítimos y operaciones portuarias."""
    
    # Título
    page_header("⚓ Puertos Marítimos Mexicanos", "Análisis de capacidad, operaciones y congestión portuaria")
    
    # Botones de control y vista
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1.5, 2])
    
    with col_btn1:
        if st.button("🔄 Recargar Datos", help="Recarga datos de puertos", key="btn_recargar_puertos"):
            st.cache_data.clear()
            st.rerun()
    
    with col_btn2:
        vista = st.radio("Tipo de Vista", ["Dashboard", "Tabla", "Mapa"], horizontal=True, key="radio_vista_puertos")
    
    with col_btn3:
        st.caption("📡 Datos actualizados - FreightMetrics")
    
    st.markdown("---")
    
    # Cargar datos
    df_puertos = generar_datos_puertos_realistas()
    kpis = calcular_kpis_estrategicos(df_puertos)
    
    # ========== KPIs ESTRATÉGICOS ==========
    section_header("📊 Indicadores Clave de Desempeño Nacional")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.metric(
            label="🚢 Throughput Mensual",
            value=f"{kpis['throughput_nacional']:,.0f}",
            delta="TEU"
        )
    
    with kpi_col2:
        sat_change = kpis['saturacion_promedio'] - 55
        st.metric(
            label="📈 Saturación Promedio",
            value=f"{kpis['saturacion_promedio']:.1f}%",
            delta=f"{sat_change:+.1f}%" if sat_change != 0 else None
        )
    
    with kpi_col3:
        st.metric(
            label="💰 Valor Comercial",
            value=f"${kpis['valor_comercial']/1_000_000:.1f}M",
            delta="USD"
        )
    
    with kpi_col4:
        st.metric(
            label="⚠️ Puertos Críticos",
            value=kpis['puertos_criticos'],
            delta="Requieren atención",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # ========== VISTAS ==========
    if vista == "Dashboard":
        # FILTROS
        col_filtro1, col_filtro2, col_filtro3 = st.columns([2, 2, 2])
        
        with col_filtro1:
            puerto_seleccionado = st.multiselect(
                "🏴 Filtrar Puertos",
                options=df_puertos['Puerto'].tolist(),
                default=df_puertos['Puerto'].tolist()[:5],
                key="filter_puerto"
            )
            df_filtrado = df_puertos[df_puertos['Puerto'].isin(puerto_seleccionado)]
        
        with col_filtro2:
            region_seleccionada = st.multiselect(
                "🗺️ Filtrar por Región",
                options=df_puertos['Región'].unique().tolist(),
                default=df_puertos['Región'].unique().tolist(),
                key="filter_region"
            )
            df_filtrado = df_filtrado[df_filtrado['Región'].isin(region_seleccionada)]
        
        with col_filtro3:
            estado_seleccionado = st.multiselect(
                "🔴 Filtrar por Estado",
                options=df_puertos['Estado'].unique().tolist(),
                default=df_puertos['Estado'].unique().tolist(),
                key="filter_estado"
            )
            df_filtrado = df_filtrado[df_filtrado['Estado'].isin(estado_seleccionado)]
        
        st.markdown("---")
        
        # VISUALIZACIONES PRINCIPALES
        section_header("📉 Visualizaciones Analíticas")
        
        viz_col1, viz_col2 = st.columns(2)
        
        # Gráfico de barras: Throughput
        with viz_col1:
            fig_bar = px.bar(
                df_filtrado.sort_values('TEU_Mes', ascending=False),
                x='Puerto',
                y='TEU_Mes',
                color='Saturación',
                color_continuous_scale='RdYlGn_r',
                title='📦 Throughput Mensual por Puerto',
                labels={'TEU_Mes': 'TEU/Mes', 'Puerto': 'Puerto Marítimo'}
            )
            fig_bar.update_layout(
                height=400,
                showlegend=True,
                hovermode='x unified',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Gráfico de gauge: Saturación
        with viz_col2:
            fig_gauge = go.Figure(data=[go.Indicator(
                mode="gauge+number+delta",
                value=kpis['saturacion_promedio'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Saturación Promedio Nacional"},
                delta={'reference': 65, 'suffix': '%', 'position': 'top'},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"},
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 80
                    }
                }
            )])
            fig_gauge.update_layout(height=400)
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Matriz de saturación
        section_header("🔥 Matriz de Saturación por Puerto")
        df_sat_matrix = df_filtrado[['Puerto', 'Saturación', 'Estado']].sort_values('Saturación', ascending=False)
        
        fig_heatmap = px.bar(
            df_sat_matrix,
            x='Puerto',
            y='Saturación',
            color='Saturación',
            color_continuous_scale=[(0, '#51CF66'), (0.6, '#FFA500'), (1, '#FF6B6B')],
            title='🌡️ Índice de Saturación por Puerto',
            labels={'Saturación': 'Saturación (%)', 'Puerto': 'Puerto Marítimo'},
            text='Saturación'
        )
        fig_heatmap.update_traces(textposition='outside')
        fig_heatmap.update_layout(
            height=350,
            xaxis_tickangle=-45,
            coloraxis_colorbar=dict(title="Saturación (%)")
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Tendencias mensuales
        section_header("📈 Tendencias Mensuales de Throughput")
        df_tendencias = generar_tendencias_mensuales()
        
        fig_trend = px.line(
            df_tendencias[df_tendencias['Puerto'].isin(df_filtrado['Puerto'].tolist())],
            x='Fecha',
            y='TEU',
            color='Puerto',
            title='Evolución de TEU/Mes (Últimos 12 meses)',
            labels={'TEU': 'TEU', 'Fecha': 'Fecha'},
            markers=True
        )
        fig_trend.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Distribución y scatter
        section_header("⚙️ Análisis de Operaciones")
        col_op1, col_op2 = st.columns(2)
        
        with col_op1:
            fig_pie = px.pie(
                df_filtrado,
                values='Operaciones',
                names='Puerto',
                title='Proporción de Operaciones Totales',
                hole=0.4
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_op2:
            fig_scatter = px.scatter(
                df_filtrado,
                x='Operaciones',
                y='Saturación',
                size='TEU_Mes',
                color='Región',
                hover_name='Puerto',
                title='Operaciones vs Saturación',
                labels={'Operaciones': 'Operaciones Diarias', 'Saturación': 'Saturación (%)'},
                size_max=50
            )
            fig_scatter.update_layout(height=400, hovermode='closest')
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Tiempos de espera
        section_header("⏱️ Tiempos Promedio de Espera")
        df_espera = df_filtrado[['Puerto', 'Tiempo_Promedio_Espera', 'Buques_Atracados']].sort_values(
            'Tiempo_Promedio_Espera', ascending=False
        )
        
        fig_espera = px.bar(
            df_espera,
            x='Puerto',
            y='Tiempo_Promedio_Espera',
            color='Tiempo_Promedio_Espera',
            color_continuous_scale='Reds',
            title='⏳ Tiempo Promedio de Espera (Horas)',
            labels={'Tiempo_Promedio_Espera': 'Horas', 'Puerto': 'Puerto'},
            text='Tiempo_Promedio_Espera'
        )
        fig_espera.update_traces(textposition='outside')
        fig_espera.update_layout(height=350, xaxis_tickangle=-45)
        st.plotly_chart(fig_espera, use_container_width=True)
    
    elif vista == "Tabla":
        section_header("📋 Tabla Completa de Puertos")
        
        df_tabla = df_puertos[[
            'Puerto', 'Región', 'TEU_Actual', 'TEU_Mes', 'Capacidad_Mensual',
            'Saturación', 'Estado', 'Operaciones', 'Tiempo_Promedio_Espera',
            'Buques_Atracados', 'Movimientos_Mes'
        ]].copy()
        
        df_tabla.columns = [
            '🏴 Puerto', '🗺️ Región', 'TEU Diario', 'TEU/Mes', 'Capacidad/Mes',
            'Saturación (%)', 'Estado', 'Operaciones', 'Espera (h)', 'Buques', 'Movimientos'
        ]
        
        def color_estado(val):
            if 'Crítico' in str(val):
                return 'background-color: #FFB6C6'
            elif 'Alto' in str(val):
                return 'background-color: #FFE0B2'
            else:
                return 'background-color: #C8E6C9'
        
        styled_table = df_tabla.style.map(
            color_estado, subset=['Estado']
        ).format({
            'Saturación (%)': '{:.1f}',
            'TEU Diario': '{:,.0f}',
            'TEU/Mes': '{:,.0f}',
            'Capacidad/Mes': '{:,.0f}',
            'Operaciones': '{:,.0f}',
            'Espera (h)': '{:.0f}',
            'Movimientos': '{:,.0f}'
        })
        
        st.dataframe(styled_table, use_container_width=True, hide_index=True)
        
        csv = df_tabla.to_csv(index=False)
        st.download_button(
            label="📥 Descargar Tabla (CSV)",
            data=csv,
            file_name=f"puertos_maritimos_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    else:  # Mapa
        section_header("🗺️ Mapa Geográfico de Puertos")
        
        fig_map = px.scatter_mapbox(
            df_puertos,
            lat='Latitud',
            lon='Longitud',
            hover_name='Puerto',
            hover_data={
                'TEU_Mes': ':.0f',
                'Saturación': ':.1f',
                'Estado': True,
                'Región': True,
                'Latitud': ':.4f',
                'Longitud': ':.4f'
            },
            color='Saturación',
            size='TEU_Mes',
            color_continuous_scale='RdYlGn_r',
            zoom=3,
            center={'lat': 21, 'lon': -105},
            title='📍 Ubicación Geográfica y Estado de Puertos',
            size_max=40,
            mapbox_style='open-street-map'
        )
        
        fig_map.update_layout(height=600, coloraxis_colorbar=dict(title="Saturación (%)"))
        st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    
    # INTEGRACIONES
    section_header("🔗 Integraciones con Otras Secciones")
    
    int_col1, int_col2, int_col3 = st.columns(3)
    
    with int_col1:
        st.info("**📦 Flujos de Carga**\n- Vincular rutas marítimas con cruces fronterizos\n- Seguimiento de contenedores")
    
    with int_col2:
        st.warning("**🛣️ Corredores Logísticos**\n- Rutas terrestres desde puertos\n- Destinos principales: Nuevo Laredo, Cd. Juárez")
    
    with int_col3:
        st.success("**👥 Monitor Laboral**\n- Disponibilidad de transportistas\n- Coordinación temporal con operaciones")
    
    st.success("✅ Análisis actualizado - FreightMetrics")


if __name__ == "__main__":
    page_puertos_maritimos()

"""
Página: Flujos de Carga Transfronterizos
Análisis y visualización de flujos de cruces fronterizos
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from pathlib import Path


def page_flujos_de_carga():
    st.title("🚛 Flujos de Carga Transfronterizos")
    st.markdown("---")

    # FILTROS EN 3 COLUMNAS
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**📆 Año**")
        year = st.selectbox("Selecciona año:", [2023, 2024, 2025, 2026], index=3, label_visibility="collapsed", key="mapa_year_filter")

    with col2:
        st.markdown("**🌎 Frontera**")
        frontera = st.radio("Frontera", ["🇲🇽 México", "🇨🇦 Canadá", "🌎 Ambas"], index=2, horizontal=True, label_visibility="hidden", key="mapa_frontera_filter")

    with col3:
        st.markdown("**📅 Mes**")
        mes = st.selectbox("Selecciona mes:", 
            ["Todos", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"], 
            index=0, label_visibility="collapsed", key="mapa_mes_filter")

    st.markdown("---")

    # CARGAR DATOS DEL AÑO
    def cargar_datos_csv(year):
        """Carga datos BTS del año especificado - intenta usar archivo monthly primero"""
        try:
            # Intentar cargar datos mensuales (tiene completo el año)
            archivo_monthly = Path(__file__).parent.parent / "data" / f"border_crossings_{year}_monthly.csv"
            
            if archivo_monthly.exists():
                df = pd.read_csv(archivo_monthly)
                
                # Convertir year_month a fecha
                df['Fecha'] = pd.to_datetime(df['year_month'] + '-01')
                
                # Crear columna Frontera normalizada
                df['Frontera'] = df['border'].apply(
                    lambda x: 'México' if 'Mexico' in str(x) else 'Canadá'
                )
                
                # Renombrar columnas
                df = df.rename(columns={
                    'port_name': 'Puerto',
                    'measure': 'Tipo_Medida',
                    'value': 'Valor'
                })
                
                # Filtrar solo camiones
                df = df[df['Tipo_Medida'].isin(['Trucks', 'Truck Containers Loaded', 'Truck Containers Empty'])]
                df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0).astype(int)
                
                # Pivotar por Fecha y Tipo_Medida (sumando todos los puertos)
                df_pivot = df.pivot_table(
                    index=['Fecha', 'Puerto', 'Frontera'],
                    columns='Tipo_Medida',
                    values='Valor',
                    aggfunc='sum',
                    fill_value=0
                ).reset_index()
                
                df_pivot.columns.name = None
            else:
                # Fallback a archivo historical
                archivo = Path(__file__).parent.parent / "data" / f"border_crossings_{year}_historical.csv"
                
                if not archivo.exists():
                    st.error(f"❌ Archivo no encontrado: {archivo}")
                    st.info(f"ℹ️ Archivos disponibles en: {Path(__file__).parent.parent / 'data'}")
                    return None
                
                df = pd.read_csv(archivo)
                df['Fecha'] = pd.to_datetime(df['date'])
                df = df.rename(columns={
                    'port_name': 'Puerto',
                    'value': 'Valor',
                    'measure': 'Tipo_Medida',
                    'border': 'Frontera_Original'
                })
                
                # Filtrar solo camiones
                df = df[df['Tipo_Medida'].isin(['Trucks', 'Truck Containers Loaded', 'Truck Containers Empty'])]
                df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0).astype(int)
                
                # Crear columna Frontera normalizada
                df['Frontera'] = df['Frontera_Original'].apply(
                    lambda x: 'México' if 'Mexico' in str(x) else 'Canadá'
                )
                
                # Pivotar datos
                df_pivot = df.pivot_table(
                    index=['Fecha', 'Puerto', 'Frontera'],
                    columns='Tipo_Medida',
                    values='Valor',
                    aggfunc='sum',
                    fill_value=0
                ).reset_index()
                
                df_pivot.columns.name = None
            
            # Asegurar columnas
            for col in ['Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']:
                if col not in df_pivot.columns:
                    df_pivot[col] = 0
            
            # Total cruces
            df_pivot['Cruces'] = (
                df_pivot['Trucks'] + 
                df_pivot['Truck Containers Loaded'] + 
                df_pivot['Truck Containers Empty']
            )
            
            return df_pivot.sort_values(['Fecha', 'Puerto'])
            
        except Exception as e:
            st.error(f"❌ Error cargando {year}: {e}")
            import traceback
            st.error(traceback.format_exc())
            return None

    df = cargar_datos_csv(year)

    if df is None or df.empty:
        st.error(f"❌ No hay datos para el año {year}")
        st.stop()

    # APLICAR FILTRO DE FRONTERA
    if frontera == "🇲🇽 México":
        df = df[df['Frontera'] == 'México']
        frontera_label = "México"
    elif frontera == "🇨🇦 Canadá":
        df = df[df['Frontera'] == 'Canadá']
        frontera_label = "Canadá"
    else:
        frontera_label = "Ambas Fronteras"

    # APLICAR FILTRO DE MES
    if mes != "Todos":
        mes_map = {
            "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
            "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
            "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
        }
        mes_num = mes_map[mes]
        df = df[df['Fecha'].dt.month == mes_num]
        mes_label = mes
    else:
        mes_label = "Todos los Meses"

    # MOSTRAR PERÍODO Y VALIDAR
    year_base = year
    year_fin = year

    if df.empty:
        st.warning("⚠️ No hay datos para los filtros seleccionados")
        st.stop()

    fecha_min = df['Fecha'].min()
    fecha_max = df['Fecha'].max()
    dias = (fecha_max - fecha_min).days + 1

    st.info(f"📊 **{mes_label} {year}** | **{frontera_label}** | {fecha_min.strftime('%d/%m/%Y')} - {fecha_max.strftime('%d/%m/%Y')} ({dias} días)")

    st.markdown("---")

    # MÉTRICAS
    st.subheader("📊 Resumen de Cruces")
    col1, col2, col3, col4 = st.columns(4)

    total = df['Cruces'].sum()
    trucks = df['Trucks'].sum()
    loaded = df['Truck Containers Loaded'].sum()
    empty = df['Truck Containers Empty'].sum()

    with col1:
        st.metric("Total Cruces", f"{total:,}")
    with col2:
        pct = (trucks / total * 100) if total > 0 else 0
        st.metric("🚛 Trucks", f"{trucks:,}", f"{pct:.1f}%")
    with col3:
        pct = (loaded / total * 100) if total > 0 else 0
        st.metric("📦 Loaded", f"{loaded:,}", f"{pct:.1f}%")
    with col4:
        pct = (empty / total * 100) if total > 0 else 0
        st.metric("📭 Empty", f"{empty:,}", f"{pct:.1f}%")

    st.markdown("---")

    # GRÁFICO MEJORADO: Total Cruces Mensuales o Diarios
    if mes == "Todos":
        # GRÁFICO MENSUAL (todos los 12 meses del año)
        st.subheader(f"📊 Total Cruces Mensuales - Año {year}")
        
        # Cargar TODOS los datos del año (sin filtro de mes)
        df_completo = cargar_datos_csv(year)
        
        # Aplicar apenas filtro de frontera
        if frontera == "🇲🇽 México":
            df_completo = df_completo[df_completo['Frontera'] == 'México']
        elif frontera == "🇨🇦 Canadá":
            df_completo = df_completo[df_completo['Frontera'] == 'Canadá']
        
        # Extraer mes y nombre en español
        df_completo['Mes'] = df_completo['Fecha'].dt.month
        meses_nombres_es = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
            7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        df_completo['Mes_Nombre'] = df_completo['Mes'].map(meses_nombres_es)
        
        # Agrupar por mes
        df_mes = df_completo.groupby(['Mes', 'Mes_Nombre'])[['Cruces', 'Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']].sum().reset_index()
        
        # Crear dataframe con todos los 12 meses
        todos_meses = pd.DataFrame({
            'Mes': range(1, 13),
            'Mes_Nombre': [meses_nombres_es[i] for i in range(1, 13)]
        })
        
        df_mes_completo = todos_meses.merge(df_mes, on=['Mes', 'Mes_Nombre'], how='left').fillna(0)
        
        # Convertir a int
        for col in ['Cruces', 'Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']:
            df_mes_completo[col] = df_mes_completo[col].astype(int)
        
        # Calcular color según valor (gradiente de intensidad)
        max_cruces = df_mes_completo['Cruces'].max() if df_mes_completo['Cruces'].max() > 0 else 1
        colors_dynamicos = []
        for valor in df_mes_completo['Cruces']:
            intensidad = valor / max_cruces if valor > 0 else 0.2
            if intensidad < 0.3:
                colors_dynamicos.append('rgba(100, 150, 200, 0.6)')
            elif intensidad < 0.6:
                colors_dynamicos.append('rgba(70, 200, 200, 0.7)')
            elif intensidad < 0.8:
                colors_dynamicos.append('rgba(100, 150, 255, 0.8)')
            else:
                colors_dynamicos.append('rgba(255, 100, 100, 0.9)')
        
        fig = go.Figure()
        
        # Gráfico de barras
        fig.add_trace(go.Bar(
            x=df_mes_completo['Mes_Nombre'],
            y=df_mes_completo['Cruces'],
            name='Total Cruces',
            marker=dict(
                color=colors_dynamicos,
                line=dict(color='white', width=2)
            ),
            text=[f"{int(v):,}" if v > 0 else "Sin datos" for v in df_mes_completo['Cruces']],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Total Cruces: %{y:,.0f}<extra></extra>',
            showlegend=False
        ))
        
        # Línea de promedio
        datos_con_valor = df_mes_completo[df_mes_completo['Cruces'] > 0]
        if len(datos_con_valor) > 0:
            promedio = datos_con_valor['Cruces'].mean()
            fig.add_hline(y=promedio, line_dash="dash", line_color="#FF6B6B",
                          annotation_text=f"  Promedio: {promedio:,.0f}",
                          annotation_position="right")
        
        fig.update_layout(
            title=dict(
                text=f"<b>Total Cruces Mensuales - Año {year}</b><br><sub>{frontera_label}</sub>",
                x=0.5,
                xanchor='center',
                font=dict(size=18, color='#F4F7F6')
            ),
            xaxis_title="<b>Mes</b>",
            yaxis_title="<b>Número de Cruces</b>",
            hovermode='x unified',
            height=500,
            template="plotly_white",
            plot_bgcolor='rgba(240, 245, 250, 0.5)',
            paper_bgcolor='white',
            font=dict(size=12, family="Arial, sans-serif"),
            margin=dict(l=60, r=60, t=100, b=60),
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.2)',
                showline=True,
                linewidth=2,
                linecolor='#F4F7F6'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.2)',
                showline=True,
                linewidth=2,
                linecolor='#F4F7F6'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        # GRÁFICO DIARIO (para un mes específico)
        st.subheader(f"📊 Evolución Diaria - {mes} {year}")
        
        df_dia = df.groupby('Fecha')[['Cruces', 'Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']].sum().reset_index()
        
        fig = go.Figure()
        
        # Calcular color según valor
        max_cruces_dia = df_dia['Cruces'].max() if df_dia['Cruces'].max() > 0 else 1
        colors_dia = []
        for valor in df_dia['Cruces']:
            intensidad = valor / max_cruces_dia if valor > 0 else 0.2
            if intensidad < 0.3:
                colors_dia.append('rgba(100, 150, 200, 0.6)')
            elif intensidad < 0.6:
                colors_dia.append('rgba(70, 200, 200, 0.7)')
            elif intensidad < 0.8:
                colors_dia.append('rgba(100, 150, 255, 0.8)')
            else:
                colors_dia.append('rgba(255, 100, 100, 0.9)')
        
        fig.add_trace(go.Bar(
            x=df_dia['Fecha'],
            y=df_dia['Cruces'],
            name='Total Cruces',
            marker=dict(
                color=colors_dia,
                line=dict(color='white', width=1)
            ),
            text=[f"{int(v):,}" for v in df_dia['Cruces']],
            textposition='outside',
            hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Cruces: %{y:,.0f}<extra></extra>',
            showlegend=False
        ))
        
        # Promedio diario
        promedio_dia = df_dia['Cruces'].mean()
        fig.add_hline(y=promedio_dia, line_dash="dash", line_color="#FF6B6B",
                      annotation_text=f"  Promedio: {promedio_dia:,.0f}",
                      annotation_position="right")
        
        fig.update_layout(
            title=dict(
                text=f"<b>Evolución Diaria - {mes} {year}</b><br><sub>{frontera_label}</sub>",
                x=0.5,
                xanchor='center',
                font=dict(size=18, color='#F4F7F6')
            ),
            xaxis_title="<b>Fecha</b>",
            yaxis_title="<b>Número de Cruces</b>",
            hovermode='x unified',
            height=500,
            template="plotly_white",
            plot_bgcolor='rgba(240, 245, 250, 0.5)',
            paper_bgcolor='white',
            font=dict(size=12, family="Arial, sans-serif"),
            margin=dict(l=60, r=60, t=100, b=60),
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.2)',
                showline=True,
                linewidth=2,
                linecolor='#F4F7F6'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.2)',
                showline=True,
                linewidth=2,
                linecolor='#F4F7F6'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ESTADÍSTICAS
    st.subheader("📊 Estadísticas")
    
    if mes == "Todos":
        # Estadísticas mensuales
        col1, col2, col3, col4 = st.columns(4)
        
        datos_con_valor = df_mes_completo[df_mes_completo['Cruces'] > 0]
        
        with col1:
            st.metric("Promedio Mensual", f"{datos_con_valor['Cruces'].mean():,.0f}" if len(datos_con_valor) > 0 else "0")
        with col2:
            st.metric("Máximo Mensual", f"{df_mes_completo['Cruces'].max():,.0f}")
        with col3:
            st.metric("Mínimo Mensual", f"{datos_con_valor['Cruces'].min():,.0f}" if len(datos_con_valor) > 0 else "0")
        with col4:
            st.metric("Desviación Std", f"{datos_con_valor['Cruces'].std():,.0f}" if len(datos_con_valor) > 0 else "0")
    else:
        # Estadísticas diarias
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Promedio Diario", f"{df_dia['Cruces'].mean():,.0f}")
        with col2:
            st.metric("Máximo Diario", f"{df_dia['Cruces'].max():,.0f}")
        with col3:
            st.metric("Mínimo Diario", f"{df_dia['Cruces'].min():,.0f}")
        with col4:
            st.metric("Desviación Std", f"{df_dia['Cruces'].std():,.0f}")

    st.markdown("---")

    # TABLA DE ADUANAS
    st.subheader("🌐 Detalle por Aduana")

    df_aduanas = df.groupby('Puerto')[['Cruces', 'Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']].sum().sort_values('Cruces', ascending=False).reset_index()
    df_aduanas.columns = ['Aduana', 'Total Cruces', 'Trucks', 'Containers Loaded', 'Containers Empty']

    st.dataframe(df_aduanas, use_container_width=False, hide_index=True)

    st.markdown("---")

    st.success("✅ Datos actualizados - FreightMetrics")


# ============================================================================
# GUARDIA PARA PREVENIR EJECUCIÓN DURANTE IMPORT
# ============================================================================

if __name__ == "__main__":
    page_flujos_de_carga()

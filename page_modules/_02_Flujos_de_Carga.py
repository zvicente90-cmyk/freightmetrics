"""
Página: Flujos de Carga Transfronterizos
Análisis de cruces fronterizos México-USA y Canadá-USA
Versión: 2.0 (Refactorizada)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from pathlib import Path

from modules.constants import YEARS, MONTHS, MONTHS_MAP
from modules.session_init import page_header, section_header, spacer


def calcular_crecimiento_historico():
    """
    Calcula crecimiento promedio por mes usando datos 2023-2025
    """
    try:
        years_data = {}
        for year in [2023, 2024, 2025]:
            archivo = Path(__file__).parent.parent / "data" / f"border_crossings_{year}_historical.csv"
            if archivo.exists():
                df = pd.read_csv(archivo)
                df['date'] = pd.to_datetime(df['date'])
                df['month'] = df['date'].dt.month
                
                # Filtrar trucks
                trucking = df[df['measure'].isin(['Trucks', 'Truck Containers Loaded', 'Truck Containers Empty'])]
                monthly = trucking.groupby('month')['value'].sum()
                years_data[year] = monthly
        
        # Calcular crecimiento año a año
        if years_data:
            df_comparison = pd.DataFrame(years_data)
            crecimiento_por_mes = {}
            
            for month in range(1, 13):
                if month in df_comparison.index:
                    vals = df_comparison.loc[month].dropna().values
                    if len(vals) >= 2:
                        # Usar crecimiento 2024->2025 como referencia
                        if len(vals) > 1:
                            growth = ((vals[-1] - vals[-2]) / vals[-2]) if vals[-2] > 0 else 0
                            crecimiento_por_mes[month] = growth
            
            return df_comparison, crecimiento_por_mes
    except Exception:
        return None, {}
    
    return None, {}


def proyectar_2026(df_historico, crecimiento_por_mes, mes_actual=4):
    """
    Proyecta datos 2026 para Marzo-Diciembre basado en históricos + crecimiento realista
    Solo proyecta Mar-Dic (Ene-Feb ya están como REALES en el contexto principal)
    """
    projection = {}
    
    # Proyectar Marzo-Diciembre SOLO
    if df_historico is not None and len(df_historico) > 0:
        val_2025 = df_historico[2025] if 2025 in df_historico.columns else None
        
        if val_2025 is not None:
            for month in range(3, 13):
                if month in val_2025.index:
                    base_value = val_2025[month]
                    
                    # Si tenemos crecimiento calculado para este mes, usar 60% del mismo
                    if month in crecimiento_por_mes:
                        growth_rate = crecimiento_por_mes[month]
                        cautious_growth = growth_rate * 0.6
                        projected_value = int(base_value * (1 + cautious_growth))
                    else:
                        # Fallback: usar valor de 2025 directamente si no hay crecimiento
                        projected_value = int(base_value)
                    
                    projection[month] = {
                        'value': projected_value,
                        'type': 'PROYECTADO'
                    }
        else:
            # Si no hay datos 2025, usar valores por defecto
            for month in range(3, 13):
                projection[month] = {
                    'value': 0,
                    'type': 'PROYECTADO'
                }
    
    return projection


def cargar_datos_csv(year):
    """
    Carga datos BTS del año especificado.
    Intenta usar archivo monthly primero, luego historical.
    """
    try:
        # Intentar archivo monthly (datos completos del año)
        archivo_monthly = Path(__file__).parent.parent / "data" / f"border_crossings_{year}_monthly.csv"
        
        if archivo_monthly.exists():
            df = pd.read_csv(archivo_monthly)
            df['Fecha'] = pd.to_datetime(df['year_month'] + '-01')
            df['Frontera'] = df['border'].apply(
                lambda x: 'México' if 'Mexico' in str(x) else 'Canadá'
            )
            df = df.rename(columns={
                'port_name': 'Puerto',
                'measure': 'Tipo_Medida',
                'value': 'Valor'
            })
        else:
            # Fallback a historical
            archivo = Path(__file__).parent.parent / "data" / f"border_crossings_{year}_historical.csv"
            
            if not archivo.exists():
                st.error(f"❌ Archivo no encontrado: {archivo}")
                return None
            
            df = pd.read_csv(archivo)
            df['Fecha'] = pd.to_datetime(df['date'])
            df = df.rename(columns={
                'port_name': 'Puerto',
                'value': 'Valor',
                'measure': 'Tipo_Medida',
                'border': 'Frontera_Original'
            })
            
            df['Frontera'] = df['Frontera_Original'].apply(
                lambda x: 'México' if 'Mexico' in str(x) else 'Canadá'
            )
        
        # Filtrar solo camiones
        df = df[df['Tipo_Medida'].isin(['Trucks', 'Truck Containers Loaded', 'Truck Containers Empty'])]
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0).astype(int)
        
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
        return None


def page_flujos_de_carga():
    """Página principal de Flujos de Carga"""
    
    page_header("🚛 Flujos de Carga Transfronterizos", "Análisis de cruces fronterizos")
    
    # FILTROS EN 3 COLUMNAS
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📆 Año**")
        year = st.selectbox("Selecciona año:", YEARS, index=3, label_visibility="collapsed", key="flujos_year_filter")
    
    with col2:
        st.markdown("**🌎 Frontera**")
        frontera = st.radio("Frontera", ["🇲🇽 México", "🇨🇦 Canadá", "🌎 Ambas"], index=2, horizontal=True, label_visibility="hidden", key="flujos_border_filter")
    
    with col3:
        st.markdown("**📅 Mes**")
        mes = st.selectbox("Selecciona mes:", 
            ["Todos"] + MONTHS, 
            index=0, label_visibility="collapsed", key="flujos_month_filter")
    
    st.markdown("---")
    
    # CARGAR DATOS
    df = cargar_datos_csv(year)
    
    if df is None or df.empty:
        st.error(f"❌ No hay datos para el año {year}")
        return
    
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
        mes_num = MONTHS_MAP[mes]
        df = df[df['Fecha'].dt.month == mes_num]
        mes_label = mes
    else:
        mes_label = "Todos los Meses"
    
    # VALIDAR DATOS FILTRADOS
    if df.empty:
        st.warning("⚠️ No hay datos para los filtros seleccionados")
        return
    
    # ============================================================
    # LÓGICA ESPECIAL PARA 2026 - CARGAR Y PREPARAR DATOS HÍBRIDOS
    # ============================================================
    df_mes_completo_2026 = None
    df_for_display = df.copy()  # Por defecto, usar df filtrado
    
    if year == 2026 and mes == "Todos":
        # Cargar datos completos del año para procesamiento
        df_year_completo = cargar_datos_csv(year)
        
        if frontera == "🇲🇽 México":
            df_year_completo = df_year_completo[df_year_completo['Frontera'] == 'México']
        elif frontera == "🇨🇦 Canadá":
            df_year_completo = df_year_completo[df_year_completo['Frontera'] == 'Canadá']
        
        # Mantener datos por puerto para la tabla
        df_for_display = df_year_completo.copy()
        
        # Crear versión agregada por mes para gráfico y cálculos
        df_year_mes = df_year_completo.copy()
        df_year_mes['Mes'] = df_year_mes['Fecha'].dt.month
        meses_nombres_es = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
            7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        df_year_mes['Mes_Nombre'] = df_year_mes['Mes'].map(meses_nombres_es)
        df_mes_base = df_year_mes.groupby(['Mes', 'Mes_Nombre'])[['Cruces', 'Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']].sum().reset_index()
        
        # Cargar datos REALES Ene-Feb
        try:
            puerto_a_frontera = {
                'Alcan': 'Canadá', 'Blaine': 'Canadá', 'Bridgewater': 'Canadá', 
                'Buffalo Niagara Falls': 'Canadá', 'Champlain Rouses Point': 'Canadá', 
                'Detroit': 'Canadá', 'Alexandria Bay': 'Canadá', 'St. Armand': 'Canadá',
                'Osoyoos': 'Canadá', 'Sumas': 'Canadá', 'Ogdensburg': 'Canadá',
                'Laredo': 'México', 'Brownsville': 'México', 'El Paso': 'México', 
                'Eagle Pass': 'México', 'Calexico East': 'México', 'Ysleta': 'México', 
                'Hidalgo': 'México', 'Pharr': 'México',
            }
            real_2026_raw = pd.read_csv(Path(__file__).parent.parent / "data" / "Border_ crossing_ene_feb_2026.csv")
            real_2026_raw['Frontera'] = real_2026_raw['Port Name'].map(puerto_a_frontera)
            
            frontera_norm = frontera.replace('🇲🇽 ', '').replace('🇨🇦 ', '').replace('🌎 ', '')
            if frontera_norm != 'Ambas':
                real_2026_raw = real_2026_raw[real_2026_raw['Frontera'] == frontera_norm]
            
            # Extraer totales reales para Ene y Feb
            for month in [1, 2]:
                total_row = real_2026_raw[real_2026_raw['Port Name'].str.lower() == 'total']
                if len(total_row) > 0:
                    if month == 1:
                        val = int(str(total_row.iloc[0]['Jan 2026']).replace(',', ''))
                    else:
                        val = int(str(total_row.iloc[0]['Feb 2026']).replace(',', ''))
                    
                    # Actualizar o crear fila para este mes
                    if month in df_mes_base['Mes'].values:
                        df_mes_base.loc[df_mes_base['Mes'] == month, 'Cruces'] = val
                    else:
                        mes_nombre = meses_nombres_es[month]
                        df_mes_base = pd.concat([df_mes_base, pd.DataFrame({
                            'Mes': [month],
                            'Mes_Nombre': [mes_nombre],
                            'Cruces': [val],
                            'Trucks': [0],
                            'Truck Containers Loaded': [0],
                            'Truck Containers Empty': [0]
                        })], ignore_index=True)
        except Exception as e:
            st.warning(f"⚠️ Error cargando datos reales Ene-Feb: {e}")
        
        # Calcular proyecciones Mar-Dic
        df_historico, crecimiento_por_mes = calcular_crecimiento_historico()
        projection_2026 = proyectar_2026(df_historico, crecimiento_por_mes)
        
        if projection_2026:
            for month in range(3, 13):
                if month in projection_2026:
                    val = projection_2026[month]['value']
                    if month in df_mes_base['Mes'].values:
                        df_mes_base.loc[df_mes_base['Mes'] == month, 'Cruces'] = val
                    else:
                        mes_nombre = meses_nombres_es[month]
                        df_mes_base = pd.concat([df_mes_base, pd.DataFrame({
                            'Mes': [month],
                            'Mes_Nombre': [mes_nombre],
                            'Cruces': [val],
                            'Trucks': [0],
                            'Truck Containers Loaded': [0],
                            'Truck Containers Empty': [0]
                        })], ignore_index=True)
        
        # Ordenar por mes y guardar para usar en métricas y gráfico
        df_mes_base = df_mes_base.sort_values('Mes').reset_index(drop=True)
        df_mes_completo_2026 = df_mes_base.copy()
    
    # ============================================================
    # CALCULAR MÉTRICAS - USAR DF CORRECTO SEGÚN CONTEXTO
    # ============================================================
    fecha_min = pd.Timestamp.now()
    fecha_max = pd.Timestamp.now()
    dias = 1
    
    # Seleccionar fuente de datos para métricas
    if df_mes_completo_2026 is not None:
        df_metrics = df_mes_completo_2026.copy()
        mes_label = "2026 (Híbrido: Real Ene-Feb + Proyectado Mar-Dic)"
    else:
        df_metrics = df.copy()
        if 'Fecha' in df.columns:
            fecha_min = df['Fecha'].min()
            fecha_max = df['Fecha'].max()
            dias = (fecha_max - fecha_min).days + 1
    
    st.info(f"📊 **{mes_label} {year}** | **{frontera_label}** | {fecha_min.strftime('%d/%m/%Y') if 'Fecha' in df.columns else 'N/A'} - {fecha_max.strftime('%d/%m/%Y') if 'Fecha' in df.columns else 'N/A'} ({dias} días)")
    
    st.markdown("---")
    
    # MÉTRICAS
    section_header("📊 Resumen de Cruces")
    col1, col2, col3, col4 = st.columns(4)
    
    total = df_metrics['Cruces'].sum()
    trucks = df_metrics['Trucks'].sum() if 'Trucks' in df_metrics.columns else 0
    loaded = df_metrics['Truck Containers Loaded'].sum() if 'Truck Containers Loaded' in df_metrics.columns else 0
    empty = df_metrics['Truck Containers Empty'].sum() if 'Truck Containers Empty' in df_metrics.columns else 0
    
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
    
    # GRÁFICO (mensuales si "Todos", diarios si mes específico)
    if mes == "Todos":
        # Cargar datos completos del año para gráfico mensual
        df_completo = cargar_datos_csv(year)
        
        if frontera == "🇲🇽 México":
            df_completo = df_completo[df_completo['Frontera'] == 'México']
        elif frontera == "🇨🇦 Canadá":
            df_completo = df_completo[df_completo['Frontera'] == 'Canadá']
        
        df_completo['Mes'] = df_completo['Fecha'].dt.month
        meses_nombres_es = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
            7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        df_completo['Mes_Nombre'] = df_completo['Mes'].map(meses_nombres_es)
        
        df_mes = df_completo.groupby(['Mes', 'Mes_Nombre'])[['Cruces']].sum().reset_index()
        todos_meses = pd.DataFrame({
            'Mes': range(1, 13),
            'Mes_Nombre': [meses_nombres_es[i] for i in range(1, 13)]
        })
        df_mes_completo = todos_meses.merge(df_mes, on=['Mes', 'Mes_Nombre'], how='left').fillna(0)
        
        # =============== MODO 2026: USAR DATOS HÍBRIDOS ===============
        if year == 2026 and df_mes_completo_2026 is not None:
            # Usar datos ya procesados con Ene-Feb reales + Mar-Dic proyectados
            df_mes_completo = df_mes_completo_2026.copy()
            df_mes_completo['Tipo'] = df_mes_completo['Mes'].apply(
                lambda m: 'REAL' if m <= 2 else 'PROYECTADO'
            )
            
            # Mostrar información
            st.info("📊 Datos 2026: Enero-Febrero (REALES) | Marzo-Diciembre (PROYECTADOS basados en tendencias 2023-2025)")
            
            # Colores según tipo
            colors_dynamicos = []
            for idx, row in df_mes_completo.iterrows():
                tipo = row.get('Tipo', 'REAL' if row['Mes'] <= 2 else 'PROYECTADO')
                if tipo == 'REAL':
                    colors_dynamicos.append('rgba(76, 175, 80, 0.85)')  # Verde
                else:
                    colors_dynamicos.append('rgba(255, 152, 0, 0.65)')  # Naranja
        else:
            # =============== MODO NON-2026: Colores dinámicos normales ===============
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
        
        section_header(f"📊 Total Cruces Mensuales - Año {year}")
        
        fig = go.Figure()
        
        # Separar datos reales vs proyectados para 2026
        if year == 2026 and df_mes_completo_2026 is not None and 'Tipo' in df_mes_completo.columns:
            # Preparar DataFrames con TODOS los meses
            df_mes_completo = df_mes_completo.sort_values('Mes').reset_index(drop=True)
            
            # Crear series con todos los meses para alineación
            df_real_full = df_mes_completo.copy()
            df_proj_full = df_mes_completo.copy()
            
            # Datos reales: mostrar solo Ene-Feb, el resto 0
            df_real_full.loc[df_real_full['Mes'] > 2, 'Cruces'] = 0
            df_real_full.loc[df_real_full['Mes'] <= 2, 'Cruces'] = df_mes_completo.loc[df_mes_completo['Mes'] <= 2, 'Cruces'].values if len(df_mes_completo[df_mes_completo['Mes'] <= 2]) > 0 else 0
            
            # Datos proyectados: mostrar solo Mar-Dic, el resto 0
            df_proj_full.loc[df_proj_full['Mes'] <= 2, 'Cruces'] = 0
            
            # Asegurar que df_mes_completo está bien ordenado
            df_mes_completo = df_mes_completo.sort_values('Mes').reset_index(drop=True)
            x_labels_sorted = [df_mes_completo[df_mes_completo['Mes']==m]['Mes_Nombre'].iloc[0] if len(df_mes_completo[df_mes_completo['Mes']==m]) > 0 else f'M{m}' for m in range(1, 13)]
            
            # Agregar barras de datos reales
            real_cruces = []
            for m in range(1, 13):
                val = df_mes_completo[df_mes_completo['Mes'] == m]['Cruces'].iloc[0] if m <= 2 and len(df_mes_completo[df_mes_completo['Mes'] == m]) > 0 else 0
                real_cruces.append(val)
            
            if sum(real_cruces) > 0:
                fig.add_trace(go.Bar(
                    x=x_labels_sorted,
                    y=real_cruces,
                    name='REAL (Ene-Feb)',
                    marker=dict(color='rgba(76, 175, 80, 0.85)', line=dict(color='white', width=2)),
                    text=[f"{int(v):,}" if v > 0 else "" for v in real_cruces],
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Cruces: %{y:,.0f}<br><b>REAL</b><extra></extra>',
                ))
            
            # Agregar barras de datos proyectados
            proj_cruces = []
            for m in range(1, 13):
                val = df_mes_completo[df_mes_completo['Mes'] == m]['Cruces'].iloc[0] if m > 2 and len(df_mes_completo[df_mes_completo['Mes'] == m]) > 0 else 0
                proj_cruces.append(val)
            
            if sum(proj_cruces) > 0:
                fig.add_trace(go.Bar(
                    x=x_labels_sorted,
                    y=proj_cruces,
                    name='PROYECTADO (Mar-Dic)',
                    marker=dict(color='rgba(255, 152, 0, 0.7)', line=dict(color='white', width=2)),
                    text=[f"{int(v):,}" if v > 0 else "" for v in proj_cruces],
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Cruces: %{y:,.0f}<br><b>PROYECTADO</b><extra></extra>',
                ))
        else:
            # Gráfico normal sin separación
            df_mes_completo = df_mes_completo.sort_values('Mes').reset_index(drop=True)
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
        
        datos_con_valor = df_mes_completo[df_mes_completo['Cruces'] > 0]
        if len(datos_con_valor) > 0:
            promedio = datos_con_valor['Cruces'].mean()
            fig.add_hline(y=promedio, line_dash="dash", line_color="#FF6B6B",
                          annotation_text=f"  Promedio: {promedio:,.0f}",
                          annotation_position="right")
        
        fig.update_layout(
            title=dict(
                text=f"<b>Total Cruces Mensuales - Año {year}</b><br><sub>{frontera_label}</sub>",
                x=0.5, xanchor='center', font=dict(size=18, color='#2C3E50')
            ),
            xaxis_title="<b>Mes</b>",
            yaxis_title="<b>Número de Cruces</b>",
            height=500,
            template="plotly_white",
            plot_bgcolor='rgba(240, 245, 250, 0.5)',
            hovermode='x unified',
            barmode='group' if year == 2026 else 'overlay'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        # Gráfico diario
        df_dia = df.groupby('Fecha')[['Cruces']].sum().reset_index()
        
        section_header(f"📊 Evolución Diaria - {mes} {year}")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_dia['Fecha'], 
            y=df_dia['Cruces'],
            name='Total Cruces', 
            mode='lines+markers', 
            line=dict(color='#4070F4', width=3),
            fill='tozeroy', 
            fillcolor='rgba(64, 112, 244, 0.2)',
            hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Cruces: %{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text=f"<b>Evolución Diaria - {mes} {year}</b><br><sub>{frontera_label}</sub>",
                x=0.5, xanchor='center'
            ),
            xaxis_title="Fecha",
            yaxis_title="Número de Cruces",
            height=400,
            template="plotly_white",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # TABLA FINAL - MEJORADA CON FORMATOS Y ESTILOS
    section_header("🌐 Detalle por Aduana")
    
    # Usar df_for_display para 2026+"Todos", sino usar df filtrado
    df_for_table = df_for_display if (year == 2026 and mes == "Todos" and df_for_display is not None) else df
    
    df_aduanas = df_for_table.groupby('Puerto')[['Cruces', 'Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']].sum().sort_values('Cruces', ascending=False).reset_index()
    df_aduanas.columns = ['Aduana', 'Total Cruces', 'Trucks', 'Containers Loaded', 'Containers Empty']
    
    # Crear una copia para el display con formatos
    df_display = df_aduanas.copy()
    
    # Función para colorear celdas según valor
    def color_by_value(val, max_val, min_val):
        """Retorna color RGB basado en intensidad del valor"""
        if pd.isna(val) or max_val == min_val:
            return ''
        normalized = (val - min_val) / (max_val - min_val)
        if normalized > 0.75:
            return 'background-color: #d4edda; color: #155724; font-weight: bold'
        elif normalized > 0.50:
            return 'background-color: #d1ecf1; color: #0c5460'
        elif normalized > 0.25:
            return 'background-color: #fff3cd; color: #856404'
        else:
            return 'background-color: #f8f9fa; color: #495057'
    
    # Aplicar estilos
    def stylize_table(df):
        """Aplica estilos personalizados a la tabla"""
        styler = df.style
        
        # Obtener máximo y mínimo para cada columna numérica
        for col in ['Total Cruces', 'Trucks', 'Containers Loaded', 'Containers Empty']:
            max_val = df[col].max()
            min_val = df[col].min()
            
            # Aplicar color a cada columna
            styler = styler.map(
                lambda v, max_v=max_val, min_v=min_val: color_by_value(v, max_v, min_v),
                subset=[col]
            )
        
        # Formato de números con separadores de miles
        styler = styler.format({
            'Total Cruces': '{:,.0f}',
            'Trucks': '{:,.0f}',
            'Containers Loaded': '{:,.0f}',
            'Containers Empty': '{:,.0f}'
        })
        
        # Estilos adicionales
        styler = styler.set_properties(**{
            'border': '1px solid #ddd',
            'padding': '12px',
            'text-align': 'right',
            'font-size': '14px'
        }, subset=['Total Cruces', 'Trucks', 'Containers Loaded', 'Containers Empty'])
        
        styler = styler.set_properties(**{
            'text-align': 'left',
            'font-weight': 'bold',
            'background-color': '#f0f2f6',
            'border': '1px solid #ddd',
            'padding': '12px'
        }, subset=['Aduana'])
        
        return styler
    
    # Mostrar tabla estilizada
    st_styled = stylize_table(df_display)
    st.dataframe(st_styled, use_container_width=True, hide_index=True)
    
    # Agregado: Resumen con barras visuales
    st.markdown("**📊 Ranking de Aduanas por Volumen**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 5 por Total Cruces
        top5_cruces = df_aduanas.nlargest(5, 'Total Cruces')[['Aduana', 'Total Cruces']].copy()
        fig_top = px.bar(
            top5_cruces,
            y='Aduana',
            x='Total Cruces',
            orientation='h',
            title='🏆 Top 5 Aduanas por Total Cruces',
            labels={'Total Cruces': 'Cruces', 'Aduana': ''},
            text='Total Cruces',
            color='Total Cruces',
            color_continuous_scale='Blues'
        )
        fig_top.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_top.update_layout(height=350, showlegend=False, xaxis_title='Total Cruces')
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        # Distribución de tipos de cruces (Trucks vs Containers)
        distribucion = pd.DataFrame({
            'Tipo': ['Trucks', 'Containers Loaded', 'Containers Empty'],
            'Total': [
                df_aduanas['Trucks'].sum(),
                df_aduanas['Containers Loaded'].sum(),
                df_aduanas['Containers Empty'].sum()
            ]
        })
        fig_dist = px.pie(
            distribucion,
            values='Total',
            names='Tipo',
            title='🥧 Distribución de Tipos de Cruces',
            hole=0.4,
            color_discrete_map={
                'Trucks': '#4070F4',
                'Containers Loaded': '#51CF66',
                'Containers Empty': '#FFA500'
            }
        )
        fig_dist.update_traces(textposition='inside', textinfo='label+percent')
        st.plotly_chart(fig_dist, use_container_width=True)
    
    st.success("✅ Datos actualizados - FreightMetrics")


if __name__ == "__main__":
    page_flujos_de_carga()

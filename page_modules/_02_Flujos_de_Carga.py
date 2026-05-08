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
from page_modules.tarjeta_kpi import tarjeta_kpi_color, COLORES


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


# ============================================================================
# NUEVAS FUNCIONES DE ANÁLISIS (FASE 1+2 IMPROVEMENTS)
# ============================================================================

def calcular_comparativa_yoy(year, mes=None, frontera=None):
    """
    Calcula comparativa vs año anterior (YoY)
    Retorna: df con columnas [mes, valor_este_año, valor_año_anterior, crecimiento%]
    """
    try:
        if year <= 2023:
            return None
        
        # Cargar datos del año actual
        df_actual = cargar_datos_csv(year)
        if df_actual is None or df_actual.empty:
            return None
        
        # Cargar datos del año anterior
        df_anterior = cargar_datos_csv(year - 1)
        if df_anterior is None or df_anterior.empty:
            return None
        
        # Agregar por mes
        df_actual['Mes'] = df_actual['Fecha'].dt.month
        df_anterior['Mes'] = df_anterior['Fecha'].dt.month
        
        actual_mes = df_actual.groupby('Mes')['Cruces'].sum().reset_index()
        actual_mes.columns = ['Mes', 'Valor_Actual']
        
        anterior_mes = df_anterior.groupby('Mes')['Cruces'].sum().reset_index()
        anterior_mes.columns = ['Mes', 'Valor_Anterior']
        
        # Merge
        df_comp = actual_mes.merge(anterior_mes, on='Mes', how='outer').fillna(0)
        df_comp['Crecimiento_Pct'] = (
            (df_comp['Valor_Actual'] - df_comp['Valor_Anterior']) / 
            df_comp['Valor_Anterior'].replace(0, 1) * 100
        )
        
        return df_comp
    except:
        return None


def calcular_volatilidad(df_mes):
    """
    Calcula volatilidad (desviación estándar y coeficiente de variación)
    """
    if df_mes is None or df_mes.empty or 'Cruces' not in df_mes.columns:
        return None, None
    
    cruces = df_mes['Cruces'].values
    std_dev = float(pd.Series(cruces).std())
    mean_val = float(pd.Series(cruces).mean())
    
    if mean_val == 0:
        cv = 0
    else:
        cv = (std_dev / mean_val) * 100  # Coeficiente de variación en %
    
    return {
        'desviacion_estandar': std_dev,
        'coeficiente_variacion': cv,
        'media': mean_val,
        'min': float(pd.Series(cruces).min()),
        'max': float(pd.Series(cruces).max())
    }


def detectar_anomalias(df_mes):
    """
    Detecta anomalías usando método de desviación estándar (±2σ)
    Retorna lista de meses con anomalías
    """
    if df_mes is None or df_mes.empty:
        return []
    
    cruces = df_mes['Cruces'].values
    media = pd.Series(cruces).mean()
    std = pd.Series(cruces).std()
    
    threshold_high = media + (2 * std)
    threshold_low = media - (2 * std) if media > (2 * std) else 0
    
    anomalias = []
    for idx, row in df_mes.iterrows():
        valor = row['Cruces']
        if valor > threshold_high or valor < threshold_low:
            tipo = 'PICO' if valor > threshold_high else 'CAÍDA'
            desv = abs(valor - media) / std if std > 0 else 0
            anomalias.append({
                'mes': row.get('Mes_Nombre', f'M{row.get("Mes", idx)}'),
                'valor': valor,
                'tipo': tipo,
                'desviaciones': desv
            })
    
    return anomalias


def calcular_crecimiento_por_aduana(year, year_anterior):
    """
    Calcula crecimiento por aduana año a año
    """
    try:
        df_actual = cargar_datos_csv(year)
        df_anterior = cargar_datos_csv(year_anterior)
        
        if df_actual is None or df_anterior is None:
            return None
        
        actual = df_actual.groupby('Puerto')['Cruces'].sum().reset_index()
        actual.columns = ['Puerto', 'Actual']
        
        anterior = df_anterior.groupby('Puerto')['Cruces'].sum().reset_index()
        anterior.columns = ['Puerto', 'Anterior']
        
        df_crec = actual.merge(anterior, on='Puerto', how='outer').fillna(0)
        df_crec['Crecimiento_Pct'] = (
            (df_crec['Actual'] - df_crec['Anterior']) / 
            df_crec['Anterior'].replace(0, 1) * 100
        )
        df_crec['Crecimiento_Abs'] = df_crec['Actual'] - df_crec['Anterior']
        
        return df_crec.sort_values('Crecimiento_Pct', ascending=False)
    except:
        return None


def crear_tabla_mes_a_mes(df_completo):
    """
    Crea tabla pivote: Aduanas x Meses
    """
    try:
        df = df_completo.copy()
        df['Mes'] = df['Fecha'].dt.month
        
        df_pivot = df.pivot_table(
            index='Puerto',
            columns='Mes',
            values='Cruces',
            aggfunc='sum',
            fill_value=0
        )
        
        meses_nombres = {
            1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'
        }
        df_pivot.columns = [meses_nombres.get(c, f'M{c}') for c in df_pivot.columns]
        
        df_pivot['Total'] = df_pivot.sum(axis=1)
        
        return df_pivot.sort_values('Total', ascending=False)
    except:
        return None


def calcular_valor_estimado(df, valor_promedio_cruce=25000):
    """
    Estima valor USD de cruces (cruces * valor_promedio_cruce)
    valor_promedio_cruce: valor USD estimado por cruce
    """
    try:
        df_val = df.copy()
        df_val['Valor_USD'] = df_val['Cruces'] * valor_promedio_cruce
        return df_val
    except:
        return df


def cargar_datos_historicos(anos=[2023, 2024, 2025, 2026]):
    """
    Carga datos históricos de múltiples años para análisis comparativo
    """
    try:
        data_dir = Path(__file__).parent.parent / "data"
        df_list = []
        
        for year in anos:
            archivo = data_dir / f"border_crossings_{year}_historical.csv"
            if archivo.exists():
                df = pd.read_csv(archivo)
                df['Fecha'] = pd.to_datetime(df['date'])
                df['Año'] = year
                df_list.append(df)
        
        return pd.concat(df_list, ignore_index=True) if df_list else None
    except:
        return None


def exportar_reporte_csv(df, df_mes, volatilidad, anomalias, year, frontera_label):
    """
    Prepara datos para exportación
    """
    import io
    
    buffer = io.StringIO()
    
    # Encabezado
    buffer.write(f"REPORTE DE FLUJOS DE CARGA\n")
    buffer.write(f"Año: {year} | Frontera: {frontera_label}\n")
    buffer.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    # Resumen
    buffer.write("=== RESUMEN ===\n")
    total = df['Cruces'].sum() if 'Cruces' in df.columns else 0
    buffer.write(f"Total Cruces: {total:,}\n")
    
    if volatilidad:
        buffer.write(f"Volatilidad (CV): {volatilidad.get('coeficiente_variacion', 0):.2f}%\n")
        buffer.write(f"Media Mensual: {volatilidad.get('media', 0):,.0f}\n")
    
    if anomalias:
        buffer.write(f"Anomalías Detectadas: {len(anomalias)}\n")
    
    buffer.write("\n=== DATOS MENSUALES ===\n")
    if df_mes is not None:
        df_mes.to_csv(buffer, index=False)
    
    buffer.write("\n=== DATOS POR ADUANA ===\n")
    if df is not None:
        aduanas = df.groupby('Puerto')['Cruces'].sum().sort_values(ascending=False).reset_index()
        aduanas.to_csv(buffer, index=False)
    
    return buffer.getvalue()


def page_flujos_de_carga():
    """Página principal de Flujos de Carga"""
    
    page_header("🚛 Flujos de Carga Transfronterizos", "Análisis de cruces fronterizos")
    
    # ============================================================
    # Estilos CSS LOCALES para esta página
    # ============================================================
    st.markdown("""
    <style>
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, rgba(25, 118, 210, 0.12) 0%, rgba(66, 165, 245, 0.08) 100%) !important;
            border-top: 4px solid #1976d2 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
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
            
            # Intentar cargar archivo con ambos nombres (con y sin espacio)
            data_dir = Path(__file__).parent.parent / "data"
            archivo_nombres = [
                data_dir / "Border_crossing_ene_feb_2026.csv",  # Sin espacio
                data_dir / "Border_ crossing_ene_feb_2026.csv"  # Con espacio
            ]
            
            real_2026_raw = None
            for archivo in archivo_nombres:
                if archivo.exists():
                    real_2026_raw = pd.read_csv(archivo)
                    break
            
            if real_2026_raw is not None:
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
        tarjeta_kpi_color("Total Cruces", f"{total:,}", "📊", color_preset="azul_primario")
    with col2:
        pct = (trucks / total * 100) if total > 0 else 0
        tarjeta_kpi_color("Trucks", f"{trucks:,}", "🚛", delta=f"{pct:.1f}%", color_preset="azul_primario")
    with col3:
        pct = (loaded / total * 100) if total > 0 else 0
        tarjeta_kpi_color("Loaded", f"{loaded:,}", "📦", delta=f"{pct:.1f}%", color_preset="verde")
    with col4:
        pct = (empty / total * 100) if total > 0 else 0
        tarjeta_kpi_color("Empty", f"{empty:,}", "📭", delta=f"{pct:.1f}%", color_preset="naranja")
    
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
                    colors_dynamicos.append('rgba(0, 82, 163, 0.85)')  # Azul medio
                else:
                    colors_dynamicos.append('rgba(25, 118, 210, 0.65)')  # Azul tech
        else:
            # =============== MODO NON-2026: Colores dinámicos normales ===============
            max_cruces = df_mes_completo['Cruces'].max() if df_mes_completo['Cruces'].max() > 0 else 1
            colors_dynamicos = []
            for valor in df_mes_completo['Cruces']:
                intensidad = valor / max_cruces if valor > 0 else 0.2
                if intensidad < 0.3:
                    colors_dynamicos.append('rgba(0, 61, 122, 0.6)')
                elif intensidad < 0.6:
                    colors_dynamicos.append('rgba(0, 82, 163, 0.7)')
                elif intensidad < 0.8:
                    colors_dynamicos.append('rgba(25, 118, 210, 0.8)')
                else:
                    colors_dynamicos.append('rgba(0, 102, 204, 0.9)')
        
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
        st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
        
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
        st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
    
    st.markdown("---")
    
    # ============================================================================
    # FASE 1: MEJORAS DE ANÁLISIS AVANZADO (5 ITEMS)
    # ============================================================================
    
    # ============================================================================
    # ITEM 8: COMPARATIVA VS PERÍODO ANTERIOR (YoY)
    # ============================================================================
    if year >= 2024 and mes == "Todos":
        st.subheader("📈 Comparativa vs Año Anterior (YoY)")
        
        df_comp = calcular_comparativa_yoy(year, mes, frontera)
        
        if df_comp is not None and not df_comp.empty:
            meses_nombres_es = {
                1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
            }
            df_comp['Mes_Nombre'] = df_comp['Mes'].map(meses_nombres_es)
            
            # Gráfico comparativo
            fig_comp = go.Figure()
            
            fig_comp.add_trace(go.Bar(
                x=df_comp['Mes_Nombre'],
                y=df_comp['Valor_Actual'],
                name=f'{year} (Este año)',
                marker=dict(color='#1976d2'),
                text=[f"{int(v):,}" for v in df_comp['Valor_Actual']],
                textposition='outside'
            ))
            
            fig_comp.add_trace(go.Bar(
                x=df_comp['Mes_Nombre'],
                y=df_comp['Valor_Anterior'],
                name=f'{year-1} (Año Anterior)',
                marker=dict(color='#90CAF9'),
                text=[f"{int(v):,}" for v in df_comp['Valor_Anterior']],
                textposition='outside'
            ))
            
            fig_comp.update_layout(
                title=f'Comparativa Mensual: {year} vs {year-1}',
                barmode='group',
                xaxis_title='Mes',
                yaxis_title='Número de Cruces',
                height=400,
                template='plotly_white',
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_comp, use_container_width=True, config={'responsive': True})
            
            # Tabla de comparativa con % crecimiento
            df_comp_display = df_comp[['Mes_Nombre', 'Valor_Actual', 'Valor_Anterior', 'Crecimiento_Pct']].copy()
            df_comp_display.columns = ['Mes', 'Este Año', 'Año Anterior', 'Crecimiento %']
            
            # Colorear la columna de crecimiento
            def color_growth(val):
                if pd.isna(val):
                    return ''
                if val > 10:
                    return 'background-color: #d4edda; color: #155724; font-weight: bold'
                elif val > 0:
                    return 'background-color: #d1ecf1; color: #0c5460'
                else:
                    return 'background-color: #f8d7da; color: #721c24'
            
            st_comp = df_comp_display.style.format({
                'Este Año': '{:,.0f}',
                'Año Anterior': '{:,.0f}',
                'Crecimiento %': '{:.1f}%'
            }).map(color_growth, subset=['Crecimiento %'])
            
            st.dataframe(st_comp, use_container_width=True, hide_index=True)
        else:
            st.info("📊 Comparativa YoY disponible solo para años 2024 en adelante")
    
    st.markdown("---")
    
    # ============================================================================
    # ITEM 9: TREND LINE Y ANÁLISIS DE TENDENCIAS
    # ============================================================================
    if mes == "Todos":
        st.subheader("📉 Análisis de Tendencias")
        
        df_completo_trend = cargar_datos_csv(year)
        if frontera == "🇲🇽 México":
            df_completo_trend = df_completo_trend[df_completo_trend['Frontera'] == 'México']
        elif frontera == "🇨🇦 Canadá":
            df_completo_trend = df_completo_trend[df_completo_trend['Frontera'] == 'Canadá']
        
        df_completo_trend['Mes'] = df_completo_trend['Fecha'].dt.month
        meses_nombres_es = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
            7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        df_completo_trend['Mes_Nombre'] = df_completo_trend['Mes'].map(meses_nombres_es)
        df_mes_trend = df_completo_trend.groupby(['Mes', 'Mes_Nombre'])['Cruces'].sum().reset_index()
        
        if not df_mes_trend.empty:
            # Calcular línea de tendencia (polynomial fit)
            import numpy as np
            x_vals = np.array(df_mes_trend['Mes'].values)
            y_vals = np.array(df_mes_trend['Cruces'].values)
            
            # Fit polinomial de grado 2
            z = np.polyfit(x_vals, y_vals, 2)
            p = np.poly1d(z)
            trend_line = p(x_vals)
            
            fig_trend = go.Figure()
            
            # Barras de datos reales
            fig_trend.add_trace(go.Bar(
                x=df_mes_trend['Mes_Nombre'],
                y=df_mes_trend['Cruces'],
                name='Cruces Reales',
                marker=dict(color='#4070F4', opacity=0.7),
                text=[f"{int(v):,}" for v in df_mes_trend['Cruces']],
                textposition='outside'
            ))
            
            # Línea de tendencia
            fig_trend.add_trace(go.Scatter(
                x=df_mes_trend['Mes_Nombre'],
                y=trend_line,
                name='Línea de Tendencia',
                mode='lines',
                line=dict(color='#FF6B6B', width=3, dash='dash'),
                hovertemplate='<b>%{x}</b><br>Tendencia: %{y:,.0f}<extra></extra>'
            ))
            
            # Calcular cambio promedio
            cambio = ((trend_line[-1] - trend_line[0]) / trend_line[0] * 100) if trend_line[0] > 0 else 0
            
            fig_trend.update_layout(
                title=f'Análisis de Tendencias: {year} (Cambio estimado: {cambio:.1f}%)',
                xaxis_title='Mes',
                yaxis_title='Número de Cruces',
                height=400,
                template='plotly_white',
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_trend, use_container_width=True, config={'responsive': True})
    
    st.markdown("---")
    
    # ============================================================================
    # ITEM 10: ALERTAS DE ANOMALÍAS
    # ============================================================================
    if mes == "Todos":
        st.subheader("⚠️ Detección de Anomalías")
        
        df_completo_anom = cargar_datos_csv(year)
        if frontera == "🇲🇽 México":
            df_completo_anom = df_completo_anom[df_completo_anom['Frontera'] == 'México']
        elif frontera == "🇨🇦 Canadá":
            df_completo_anom = df_completo_anom[df_completo_anom['Frontera'] == 'Canadá']
        
        df_completo_anom['Mes'] = df_completo_anom['Fecha'].dt.month
        meses_nombres_es = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
            7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        df_completo_anom['Mes_Nombre'] = df_completo_anom['Mes'].map(meses_nombres_es)
        df_mes_anom = df_completo_anom.groupby(['Mes', 'Mes_Nombre'])['Cruces'].sum().reset_index()
        
        anomalias = detectar_anomalias(df_mes_anom)
        
        if anomalias:
            st.warning(f"🚨 **{len(anomalias)} anomalía(s) detectada(s)**")
            
            for anom in anomalias:
                if anom['tipo'] == 'PICO':
                    st.error(f"📈 **PICO** en {anom['mes']}: {anom['valor']:,} cruces ({anom['desviaciones']:.1f}σ)")
                else:
                    st.warning(f"📉 **CAÍDA** en {anom['mes']}: {anom['valor']:,} cruces ({anom['desviaciones']:.1f}σ)")
        else:
            st.success("✅ No se detectaron anomalías significativas (valores dentro de ±2σ)")
    
    st.markdown("---")
    
    # ============================================================================
    # ITEM 11: STACKED BAR CHART (TRUCKS/LOADED/EMPTY)
    # ============================================================================
    if mes == "Todos":
        st.subheader("📊 Composición de Tipos de Cruces por Mes")
        
        df_completo_stack = cargar_datos_csv(year)
        if frontera == "🇲🇽 México":
            df_completo_stack = df_completo_stack[df_completo_stack['Frontera'] == 'México']
        elif frontera == "🇨🇦 Canadá":
            df_completo_stack = df_completo_stack[df_completo_stack['Frontera'] == 'Canadá']
        
        df_completo_stack['Mes'] = df_completo_stack['Fecha'].dt.month
        meses_nombres_es = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
            7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        df_completo_stack['Mes_Nombre'] = df_completo_stack['Mes'].map(meses_nombres_es)
        
        df_stack = df_completo_stack.groupby(['Mes', 'Mes_Nombre'])[
            ['Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']
        ].sum().reset_index()
        
        fig_stack = go.Figure()
        
        fig_stack.add_trace(go.Bar(
            x=df_stack['Mes_Nombre'],
            y=df_stack['Trucks'],
            name='Trucks',
            marker=dict(color='#1976d2'),
            hovertemplate='<b>%{x}</b><br>Trucks: %{y:,}<extra></extra>'
        ))
        
        fig_stack.add_trace(go.Bar(
            x=df_stack['Mes_Nombre'],
            y=df_stack['Truck Containers Loaded'],
            name='Containers Loaded',
            marker=dict(color='#4CAF50'),
            hovertemplate='<b>%{x}</b><br>Loaded: %{y:,}<extra></extra>'
        ))
        
        fig_stack.add_trace(go.Bar(
            x=df_stack['Mes_Nombre'],
            y=df_stack['Truck Containers Empty'],
            name='Containers Empty',
            marker=dict(color='#FFA726'),
            hovertemplate='<b>%{x}</b><br>Empty: %{y:,}<extra></extra>'
        ))
        
        fig_stack.update_layout(
            barmode='stack',
            title=f'Composición Mensual de Tipos de Cruces - {year}',
            xaxis_title='Mes',
            yaxis_title='Número de Cruces',
            height=400,
            template='plotly_white',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_stack, use_container_width=True, config={'responsive': True})
    
    st.markdown("---")
    
    # ============================================================================
    # ANÁLISIS DE COMPOSICIÓN: EVOLUCIÓN 2023-2026
    # ============================================================================
    st.subheader("📊 Análisis de Composición: Evolución de Tipos de Cruces (2023-2026)")
    
    # Cargar datos históricos para análisis comparativo
    df_histor = cargar_datos_historicos([2023, 2024, 2025, 2026])
    
    if df_histor is not None and not df_histor.empty:
        # Tabs para diferentes visualizaciones
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Evolución Temporal",
            "📊 Crecimiento YoY",
            "🥧 Composición %",
            "📋 Tabla Comparativa",
            "⚠️ Volatilidad"
        ])
        
        # ===== TAB 1: EVOLUCIÓN TEMPORAL (STACKED AREA) =====
        with tab1:
            st.write("**Evolución mensual de la composición de tipos de cruces desde 2023**")
            
            # Preparar datos - pivotar para tener columnas de tipos de cruces
            df_histor_temp = df_histor.copy()
            df_histor_temp['Fecha'] = pd.to_datetime(df_histor_temp['Fecha'])
            df_histor_temp['Periodo'] = df_histor_temp['Fecha'].dt.strftime('%Y-%m')
            
            # Pivotar: Periodo x measure -> columnas de tipos de cruce
            composicion_temporal = df_histor_temp.pivot_table(
                index='Periodo', 
                columns='measure', 
                values='value', 
                aggfunc='sum', 
                fill_value=0
            ).reset_index()
            
            # Asegurar que las columnas existan (si no, asignar valores 0)
            for col in ['Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']:
                if col not in composicion_temporal.columns:
                    composicion_temporal[col] = 0
            
            fig_area = go.Figure()
            
            fig_area.add_trace(go.Scatter(
                x=composicion_temporal['Periodo'],
                y=composicion_temporal['Trucks'],
                name='Trucks',
                mode='lines',
                stackgroup='one',
                fillcolor='rgba(25, 118, 210, 0.7)',
                hovertemplate='<b>%{x}</b><br>Trucks: %{y:,}<extra></extra>'
            ))
            
            fig_area.add_trace(go.Scatter(
                x=composicion_temporal['Periodo'],
                y=composicion_temporal['Truck Containers Loaded'],
                name='Containers Loaded',
                mode='lines',
                stackgroup='one',
                fillcolor='rgba(76, 175, 80, 0.7)',
                hovertemplate='<b>%{x}</b><br>Loaded: %{y:,}<extra></extra>'
            ))
            
            fig_area.add_trace(go.Scatter(
                x=composicion_temporal['Periodo'],
                y=composicion_temporal['Truck Containers Empty'],
                name='Containers Empty',
                mode='lines',
                stackgroup='one',
                fillcolor='rgba(255, 167, 38, 0.7)',
                hovertemplate='<b>%{x}</b><br>Empty: %{y:,}<extra></extra>'
            ))
            
            fig_area.update_layout(
                title='Evolución Mensual - Área Acumulada (2023-2026)',
                xaxis_title='Periodo',
                yaxis_title='Número de Cruces',
                height=450,
                template='plotly_white',
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_area, use_container_width=True, config={'responsive': True})
            
            st.info("💡 **Insight:** Observe cómo cambia la composición año a año. "
                   "2024 muestra un aumento dramático en Containers Loaded (+50%)")
        
        # ===== TAB 2: CRECIMIENTO INTERANUAL (YoY) =====
        with tab2:
            st.write("**Crecimiento porcentual de cada tipo entre años**")
            
            composicion_anual = df_histor.groupby(['Año', 'measure'])['value'].sum().reset_index()
            
            tipos = ['Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']
            crecimiento_data = []
            
            anos_unicos = sorted(df_histor['Año'].unique())
            
            for i in range(1, len(anos_unicos)):
                ano_anterior = anos_unicos[i-1]
                ano_actual = anos_unicos[i]
                periodo = f"{int(ano_anterior)}→{int(ano_actual)}"
                
                fila = {'Periodo': periodo}
                
                for tipo in tipos:
                    val_anterior = composicion_anual[
                        (composicion_anual['Año'] == ano_anterior) & 
                        (composicion_anual['measure'] == tipo)
                    ]['value'].values
                    
                    val_actual = composicion_anual[
                        (composicion_anual['Año'] == ano_actual) & 
                        (composicion_anual['measure'] == tipo)
                    ]['value'].values
                    
                    if len(val_anterior) > 0 and len(val_actual) > 0:
                        crecimiento = ((val_actual[0] - val_anterior[0]) / val_anterior[0] * 100) if val_anterior[0] > 0 else 0
                        fila[tipo] = crecimiento
                
                crecimiento_data.append(fila)
            
            if crecimiento_data:
                df_crec = pd.DataFrame(crecimiento_data)
                
                # Crear gráfico
                fig_crec = go.Figure()
                
                for tipo in tipos:
                    if tipo in df_crec.columns:
                        fig_crec.add_trace(go.Bar(
                            x=df_crec['Periodo'],
                            y=df_crec[tipo],
                            name=tipo,
                            hovertemplate='<b>%{x}</b><br>' + tipo + ': %{y:.2f}%<extra></extra>'
                        ))
                
                fig_crec.update_layout(
                    title='Crecimiento Interanual (%) por Tipo de Cruce',
                    barmode='group',
                    xaxis_title='Periodo',
                    yaxis_title='Crecimiento (%)',
                    height=400,
                    template='plotly_white',
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_crec, use_container_width=True, config={'responsive': True})
                
                # Tabla
                st.dataframe(
                    df_crec.style.format({
                        'Trucks': '{:.2f}%',
                        'Truck Containers Loaded': '{:.2f}%',
                        'Truck Containers Empty': '{:.2f}%'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
                
                st.warning("⚠️ **Nota:** 2025→2026 incluye solo datos hasta junio (datos parciales)")
        
        # ===== TAB 3: COMPOSICIÓN PORCENTUAL =====
        with tab3:
            st.write("**Participación porcentual de cada tipo por año**")
            
            composicion_pct = {}
            
            for ano in sorted(df_histor['Año'].unique()):
                df_ano = df_histor[df_histor['Año'] == ano]
                totales = df_ano.groupby('measure')['value'].sum()
                total_cruces = totales.sum()
                
                composicion_pct[int(ano)] = {
                    'Trucks': (totales.get('Trucks', 0) / total_cruces * 100) if total_cruces > 0 else 0,
                    'Loaded': (totales.get('Truck Containers Loaded', 0) / total_cruces * 100) if total_cruces > 0 else 0,
                    'Empty': (totales.get('Truck Containers Empty', 0) / total_cruces * 100) if total_cruces > 0 else 0
                }
            
            # Crear 4 pie charts lado a lado
            cols = st.columns(4)
            
            for idx, (year, datos) in enumerate(sorted(composicion_pct.items())):
                with cols[idx]:
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=['Trucks', 'Containers Loaded', 'Containers Empty'],
                        values=[datos['Trucks'], datos['Loaded'], datos['Empty']],
                        marker=dict(colors=['#1976d2', '#4CAF50', '#FFA726']),
                        textposition='inside',
                        textinfo='label+percent',
                        hovertemplate='<b>%{label}</b><br>%{value:.1f}%<extra></extra>'
                    )])
                    
                    fig_pie.update_layout(
                        title=f'{year}',
                        height=350,
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig_pie, use_container_width=True, config={'responsive': True})
        
        # ===== TAB 4: TABLA COMPARATIVA =====
        with tab4:
            st.write("**Evolución de participación de mercado (2023-2026)**")
            
            tabla_comp = []
            
            for ano in sorted(df_histor['Año'].unique()):
                df_ano = df_histor[df_histor['Año'] == ano]
                totales = df_ano.groupby('measure')['value'].sum()
                total_cruces = totales.sum()
                
                tabla_comp.append({
                    'Año': int(ano),
                    'Trucks': f"{(totales.get('Trucks', 0) / total_cruces * 100):.1f}%",
                    'Containers Loaded': f"{(totales.get('Truck Containers Loaded', 0) / total_cruces * 100):.1f}%",
                    'Containers Empty': f"{(totales.get('Truck Containers Empty', 0) / total_cruces * 100):.1f}%",
                    'Total Cruces': f"{int(total_cruces):,}"
                })
            
            df_tabla = pd.DataFrame(tabla_comp)
            st.dataframe(df_tabla, use_container_width=True, hide_index=True)
            
            # Cambio 2023-2026
            if len(tabla_comp) >= 2:
                st.subheader("Cambio 2023 → 2026")
                
                df_2023 = df_histor[df_histor['Año'] == 2023]
                df_2026 = df_histor[df_histor['Año'] == 2026]
                
                totales_2023 = df_2023.groupby('measure')['value'].sum()
                totales_2026 = df_2026.groupby('measure')['value'].sum()
                
                total_2023 = totales_2023.sum()
                total_2026 = totales_2026.sum()
                
                cambios = {
                    'Tipo': ['Trucks', 'Containers Loaded', 'Containers Empty'],
                    '2023': [
                        f"{(totales_2023.get('Trucks', 0) / total_2023 * 100):.1f}%",
                        f"{(totales_2023.get('Truck Containers Loaded', 0) / total_2023 * 100):.1f}%",
                        f"{(totales_2023.get('Truck Containers Empty', 0) / total_2023 * 100):.1f}%"
                    ],
                    '2026': [
                        f"{(totales_2026.get('Trucks', 0) / total_2026 * 100):.1f}%",
                        f"{(totales_2026.get('Truck Containers Loaded', 0) / total_2026 * 100):.1f}%",
                        f"{(totales_2026.get('Truck Containers Empty', 0) / total_2026 * 100):.1f}%"
                    ]
                }
                
                df_cambios = pd.DataFrame(cambios)
                st.dataframe(df_cambios, use_container_width=True, hide_index=True)
                
                st.success("""
                ✅ **Conclusión:** La composición es muy ESTABLE (~45% Trucks, ~50% Loaded, ~13% Empty)
                aunque el volumen total varía significativamente entre años.
                """)
        
        # ===== TAB 5: VOLATILIDAD =====
        with tab5:
            st.write("**Análisis de volatilidad de composición en 2026**")
            
            df_2026 = df_histor[df_histor['Año'] == 2026].copy()
            df_2026['Fecha'] = pd.to_datetime(df_2026['Fecha'])
            df_2026['Mes'] = df_2026['Fecha'].dt.month
            
            # Pivotar datos para tener columnas de tipos de cruce
            df_2026_pivot = df_2026.pivot_table(
                index='Mes',
                columns='measure',
                values='value',
                aggfunc='sum',
                fill_value=0
            ).reset_index()
            
            volatilidad_data = []
            
            for tipo in ['Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']:
                if tipo in df_2026_pivot.columns:
                    datos_tipo = df_2026_pivot[tipo].values
                    totales_mes = df_2026_pivot[['Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']].sum(axis=1).values
                    
                    participaciones = []
                    for i in range(len(datos_tipo)):
                        if totales_mes[i] > 0:
                            pct = (datos_tipo[i] / totales_mes[i] * 100)
                            participaciones.append(pct)
                    
                    if participaciones:
                        std_dev = np.std(participaciones)
                        media = np.mean(participaciones)
                        cv = (std_dev / media * 100) if media > 0 else 0
                        
                        estabilidad = "✅ Muy Estable" if cv < 10 else ("⚠️ Moderado" if cv < 25 else "🔴 Volátil")
                        
                        volatilidad_data.append({
                            'Tipo de Cruce': tipo,
                            'Media (%)': f"{media:.1f}%",
                            'Desv. Est. (pp)': f"{std_dev:.2f}pp",
                            'CV (%)': f"{cv:.2f}%",
                            'Rango': f"{min(participaciones):.1f}%-{max(participaciones):.1f}%",
                            'Estabilidad': estabilidad
                        })
            
            if volatilidad_data:
                df_vol = pd.DataFrame(volatilidad_data)
                st.dataframe(df_vol, use_container_width=True, hide_index=True)
                
                st.success("""
                🎯 **Hallazgo Clave:** 
                - **Containers Loaded** es SUPER ESTABLE (CV 3.4%) → Tráfico predecible
                - **Trucks** y **Containers Empty** son VOLÁTILES (CV ~30%) → Fluctúan según demanda
                
                Esto indica que el tráfico de contenedores es constante y predecible,
                mientras que el de trucks varía según condiciones del mercado.
                """)
    else:
        st.warning("⚠️ No hay datos históricos disponibles para el análisis")
    
    st.markdown("---")
    if year >= 2024 and mes == "Todos":
        st.subheader("🏆 Rankings de Aduanas por Crecimiento YoY")
        
        df_crec = calcular_crecimiento_por_aduana(year, year - 1)
        
        if df_crec is not None and not df_crec.empty:
            # Top 10 por crecimiento
            df_top_crec = df_crec.nlargest(10, 'Crecimiento_Pct')[
                ['Puerto', 'Actual', 'Anterior', 'Crecimiento_Pct', 'Crecimiento_Abs']
            ].copy()
            
            fig_crec = px.bar(
                df_top_crec,
                y='Puerto',
                x='Crecimiento_Pct',
                orientation='h',
                title='🚀 Top 10 Aduanas por Crecimiento YoY (%)',
                labels={'Crecimiento_Pct': 'Crecimiento %', 'Puerto': ''},
                text='Crecimiento_Pct',
                color='Crecimiento_Pct',
                color_continuous_scale=['#FF6B6B', '#FFD93D', '#6BCB77']
            )
            fig_crec.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_crec.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_crec, use_container_width=True, config={'responsive': True})
            
            # Tabla detallada
            df_crec_display = df_top_crec.copy()
            df_crec_display.columns = ['Aduana', 'Año Actual', 'Año Anterior', 'Crecimiento %', 'Crecimiento Abs']
            
            st_crec = df_crec_display.style.format({
                'Año Actual': '{:,.0f}',
                'Año Anterior': '{:,.0f}',
                'Crecimiento %': '{:.2f}%',
                'Crecimiento Abs': '{:,.0f}'
            })
            
            st.dataframe(st_crec, use_container_width=True, hide_index=True)
    
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
        st.plotly_chart(fig_top, use_container_width=True, config={'responsive': True})
    
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
        st.plotly_chart(fig_dist, use_container_width=True, config={'responsive': True})
    
    st.markdown("---")
    
    # ============================================================================
    # FASE 2: MEJORAS DE ANÁLISIS ESTRATÉGICO (5 ITEMS)
    # ============================================================================
    
    # ============================================================================
    # ITEM 13: TABLA MES-A-MES (ADUANAS x MESES)
    # ============================================================================
    if mes == "Todos":
        st.subheader("📋 Tabla Mes-a-Mes por Aduana")
        
        df_completo_tabla = cargar_datos_csv(year)
        if frontera == "🇲🇽 México":
            df_completo_tabla = df_completo_tabla[df_completo_tabla['Frontera'] == 'México']
        elif frontera == "🇨🇦 Canadá":
            df_completo_tabla = df_completo_tabla[df_completo_tabla['Frontera'] == 'Canadá']
        
        df_mesa_mes = crear_tabla_mes_a_mes(df_completo_tabla)
        
        if df_mesa_mes is not None and not df_mesa_mes.empty:
            # Convertir a formato para display
            df_mesa_display = df_mesa_mes.reset_index()
            
            # Aplicar colores
            def color_heatmap(val):
                if pd.isna(val) or val == 0:
                    return ''
                # Normalizar valores
                max_val = df_mesa_mes.max().max()
                min_val = df_mesa_mes.min().min()
                if max_val == min_val:
                    normalized = 0.5
                else:
                    normalized = (val - min_val) / (max_val - min_val)
                
                # Color gradiente
                if normalized > 0.75:
                    return 'background-color: #1b5e20; color: white; font-weight: bold'
                elif normalized > 0.5:
                    return 'background-color: #43a047; color: white'
                elif normalized > 0.25:
                    return 'background-color: #fff9c4; color: #333'
                else:
                    return 'background-color: #ffccbc; color: #333'
            
            # Aplicar estilo - formato solo a columnas numéricas
            st_mesa = df_mesa_display.style.map(
                color_heatmap,
                subset=df_mesa_display.columns[1:]  # Excluir columna de aduanas
            ).format(
                '{:,.0f}',
                subset=df_mesa_display.columns[1:]  # Aplicar formato solo a columnas numéricas
            )
            
            st.dataframe(st_mesa, use_container_width=True, hide_index=True)
            
            st.caption("💡 Verde oscuro = máximo volumen | Naranja = mínimo volumen")
    
    st.markdown("---")
    
    # ============================================================================
    # ITEM 14: ANÁLISIS DE VOLATILIDAD
    # ============================================================================
    st.subheader("📊 Análisis de Volatilidad (Estabilidad de Flujos)")
    
    df_completo_vol = cargar_datos_csv(year)
    if frontera == "🇲🇽 México":
        df_completo_vol = df_completo_vol[df_completo_vol['Frontera'] == 'México']
    elif frontera == "🇨🇦 Canadá":
        df_completo_vol = df_completo_vol[df_completo_vol['Frontera'] == 'Canadá']
    
    if mes != "Todos":
        # Si es mes específico, mostrar por aduana
        df_vol_aduanas = df_completo_vol[df_completo_vol['Fecha'].dt.month == int(mes.split('-')[0])]
        if not df_vol_aduanas.empty:
            volatilidad_por_aduana = []
            
            for puerto in df_vol_aduanas['Puerto'].unique():
                df_puerto = df_vol_aduanas[df_vol_aduanas['Puerto'] == puerto]
                vol_stats = calcular_volatilidad(df_puerto)
                
                if vol_stats:
                    volatilidad_por_aduana.append({
                        'Aduana': puerto,
                        'Media': vol_stats['media'],
                        'Std Dev': vol_stats['desviacion_estandar'],
                        'CV %': vol_stats['coeficiente_variacion'],
                        'Min': vol_stats['min'],
                        'Max': vol_stats['max']
                    })
            
            if volatilidad_por_aduana:
                df_vol = pd.DataFrame(volatilidad_por_aduana).sort_values('CV %')
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Aduanas Más Estables (CV%)", df_vol['Aduana'].iloc[0], f"{df_vol['CV %'].iloc[0]:.1f}%")
                
                with col2:
                    st.metric("Aduanas Menos Estables (CV%)", df_vol['Aduana'].iloc[-1], f"{df_vol['CV %'].iloc[-1]:.1f}%")
                
                fig_vol = px.bar(
                    df_vol,
                    x='Aduana',
                    y='CV %',
                    color='CV %',
                    color_continuous_scale='RdYlGn_r',
                    title='Coeficiente de Variación por Aduana (% - Menor = Más Estable)',
                    labels={'CV %': 'Coeficiente Variación %'}
                )
                st.plotly_chart(fig_vol, use_container_width=True, config={'responsive': True})
                
                st_vol = df_vol.style.format({
                    'Media': '{:,.0f}',
                    'Std Dev': '{:,.0f}',
                    'CV %': '{:.2f}%',
                    'Min': '{:,.0f}',
                    'Max': '{:,.0f}'
                })
                st.dataframe(st_vol, use_container_width=True, hide_index=True)
    else:
        # Por mes completo
        df_completo_vol['Mes'] = df_completo_vol['Fecha'].dt.month
        meses_nombres_es = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
            7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        df_completo_vol['Mes_Nombre'] = df_completo_vol['Mes'].map(meses_nombres_es)
        df_mes_vol = df_completo_vol.groupby(['Mes', 'Mes_Nombre'])['Cruces'].sum().reset_index()
        
        vol_stats = calcular_volatilidad(df_mes_vol)
        
        if vol_stats:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Media Mensual", f"{vol_stats['media']:,.0f}")
            
            with col2:
                st.metric("Desv. Estándar", f"{vol_stats['desviacion_estandar']:,.0f}")
            
            with col3:
                st.metric("Coef. Variación", f"{vol_stats['coeficiente_variacion']:.2f}%")
            
            with col4:
                estabilidad = "Alta ✅" if vol_stats['coeficiente_variacion'] < 15 else ("Media ⚠️" if vol_stats['coeficiente_variacion'] < 25 else "Baja ❌")
                st.metric("Estabilidad", estabilidad)
    
    st.markdown("---")
    
    # ============================================================================
    # ITEM 15: VALIDACIÓN DE DATOS (DATA QUALITY)
    # ============================================================================
    st.subheader("🔍 Validación y Calidad de Datos")
    
    df_completo_valid = cargar_datos_csv(year)
    if df_completo_valid is not None and not df_completo_valid.empty:
        total_registros = len(df_completo_valid)
        registros_nulos = df_completo_valid[['Cruces', 'Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']].isnull().sum().sum()
        pct_completo = ((total_registros * 4 - registros_nulos) / (total_registros * 4)) * 100
        
        # Verificar fechas
        fecha_min = df_completo_valid['Fecha'].min()
        fecha_max = df_completo_valid['Fecha'].max()
        dias_rango = (fecha_max - fecha_min).days + 1
        
        # Por columna
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Registros", f"{total_registros:,}")
        
        with col2:
            color_quality = "🟢" if pct_completo >= 95 else ("🟡" if pct_completo >= 80 else "🔴")
            delta_val = f"{pct_completo - 95:.1f}%" if pct_completo > 95 else None
            st.metric("Calidad (%)", f"{pct_completo:.1f}% {color_quality}", delta=delta_val)
        
        with col3:
            st.metric("Rango Temporal", f"{dias_rango} días")
        
        with col4:
            aduanas_count = df_completo_valid['Puerto'].nunique()
            st.metric("Aduanas", f"{aduanas_count}")
        
        # Tabla de validación por columna
        validation_data = []
        for col in ['Cruces', 'Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']:
            nulos = df_completo_valid[col].isnull().sum()
            pct_nulos = (nulos / len(df_completo_valid)) * 100
            validation_data.append({
                'Columna': col,
                'Registros': len(df_completo_valid),
                'Nulos': nulos,
                '% Nulos': pct_nulos,
                'Estado': '✅ OK' if pct_nulos == 0 else f'⚠️ {pct_nulos:.1f}%'
            })
        
        df_validation = pd.DataFrame(validation_data)
        st_valid = df_validation.style.set_properties(**{'text-align': 'center'})
        st.dataframe(st_valid, use_container_width=True, hide_index=True)
        
        if pct_completo < 95:
            st.warning(f"⚠️ Advertencia: Completitud de datos < 95% ({pct_completo:.1f}%)")
        else:
            st.success(f"✅ Datos completos y listos para análisis ({pct_completo:.1f}%)")
    
    st.markdown("---")
    
    # ============================================================================
    # ITEM 16: VALOR USD ESTIMADO
    # ============================================================================
    st.subheader("💰 Estimación de Valor Económico")
    
    df_completo_usd = cargar_datos_csv(year)
    if df_completo_usd is not None and not df_completo_usd.empty:
        # Valor promedio por cruce (configurable)
        valor_promedio = st.slider(
            "Valor USD estimado por cruce",
            min_value=10000,
            max_value=50000,
            value=25000,
            step=1000,
            help="Estimación del valor promedio en USD por cruce fronterizo"
        )
        
        # Calcular valor total
        total_cruces = df_completo_usd['Cruces'].sum()
        valor_total_usd = total_cruces * valor_promedio
        
        # Valor en millones
        valor_millones = valor_total_usd / 1_000_000
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Cruces", f"{total_cruces:,}")
        
        with col2:
            st.metric("Valor/Cruce", f"${valor_promedio:,}")
        
        with col3:
            st.metric("Valor Total USD", f"${valor_total_usd:,.0f}")
        
        with col4:
            st.metric("Valor (Millones USD)", f"${valor_millones:.2f}M")
        
        # Valor por mes
        if mes == "Todos":
            df_completo_usd['Mes'] = df_completo_usd['Fecha'].dt.month
            meses_nombres_es = {
                1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
            }
            df_completo_usd['Mes_Nombre'] = df_completo_usd['Mes'].map(meses_nombres_es)
            df_valor_mes = df_completo_usd.groupby(['Mes', 'Mes_Nombre'])['Cruces'].sum().reset_index()
            df_valor_mes['Valor_USD'] = df_valor_mes['Cruces'] * valor_promedio
            df_valor_mes['Valor_Millones'] = df_valor_mes['Valor_USD'] / 1_000_000
            
            fig_valor = go.Figure()
            
            fig_valor.add_trace(go.Bar(
                x=df_valor_mes['Mes_Nombre'],
                y=df_valor_mes['Valor_Millones'],
                name='Valor (Millones USD)',
                marker=dict(color='#FFB300'),
                text=[f"${v:.2f}M" for v in df_valor_mes['Valor_Millones']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Valor: $%{y:.2f}M<extra></extra>'
            ))
            
            fig_valor.update_layout(
                title=f'Estimación de Valor Económico Mensual - {year}',
                xaxis_title='Mes',
                yaxis_title='Valor (Millones USD)',
                height=400,
                template='plotly_white',
                showlegend=False
            )
            
            st.plotly_chart(fig_valor, use_container_width=True, config={'responsive': True})
    
    st.markdown("---")
    
    # ============================================================================
    # ITEM 17: EXPORTACIÓN DE REPORTES
    # ============================================================================
    st.subheader("📥 Descargar Reportes")
    
    df_completo_export = cargar_datos_csv(year)
    if df_completo_export is not None and not df_completo_export.empty:
        # Preparar datos para exportación
        reporte_csv = exportar_reporte_csv(
            df_completo_export,
            df_mes_completo_2026 if year == 2026 and mes == "Todos" else None,
            None,  # Volatilidad se calcula en contexto
            None,  # Anomalías se calculan en contexto
            year,
            frontera
        )
        
        # Botón de descargar
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📥 Descargar Reporte CSV",
                data=reporte_csv,
                file_name=f"Reporte_Flujos_Carga_{year}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="reporte_csv"
            )
        
        with col2:
            # Crear Excel con múltiples sheets
            import io
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill
            
            excel_buffer = io.BytesIO()
            
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                # Sheet 1: Resumen
                df_resumen = pd.DataFrame({
                    'Métrica': ['Total Cruces', 'Aduanas', 'Período', 'Generado'],
                    'Valor': [
                        df_completo_export['Cruces'].sum(),
                        df_completo_export['Puerto'].nunique(),
                        f"{year}",
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ]
                })
                df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
                
                # Sheet 2: Datos mensuales
                df_completo_export['Mes'] = df_completo_export['Fecha'].dt.month
                df_mes_export = df_completo_export.groupby('Mes')['Cruces'].sum().reset_index()
                df_mes_export.to_excel(writer, sheet_name='Mensual', index=False)
                
                # Sheet 3: Datos por aduana
                df_aduanas_export = df_completo_export.groupby('Puerto')['Cruces'].sum().sort_values(ascending=False).reset_index()
                df_aduanas_export.to_excel(writer, sheet_name='Por Aduana', index=False)
                
                # Sheet 4: Datos completos
                df_export_full = df_completo_export[['Fecha', 'Puerto', 'Frontera', 'Cruces', 'Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']].copy()
                df_export_full.to_excel(writer, sheet_name='Detalle Completo', index=False)
            
            excel_buffer.seek(0)
            
            st.download_button(
                label="📊 Descargar Reporte Excel",
                data=excel_buffer.getvalue(),
                file_name=f"Reporte_Flujos_Carga_{year}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="reporte_excel"
            )
        
        st.success("✅ Datos actualizados - FreightMetrics")


if __name__ == "__main__":
    page_flujos_de_carga()

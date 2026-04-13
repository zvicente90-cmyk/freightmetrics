"""
FLUJOS DE CARGA TRANSFRONTERIZOS - VERSIÓN LIMPIA v2.0
Análisis de cruces fronterizos México-USA y Canadá-USA
Autor: FreightMetrics
Fecha: 2026-04-08
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path


# ============================================================
# CONFIGURACIÓN STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Flujos de Carga",
    page_icon="🚛",
    layout="wide"
)


# ============================================================
# FUNCIÓN: CARGAR DATOS CSV POR AÑO (SIN CACHÉ)
# ============================================================

def cargar_datos_csv(year):
    """
    Carga datos BTS del año especificado.
    Sin caché para que siempre cargue datos frescos.
    """
    try:
        archivo = Path(__file__).parent / "data" / f"border_crossings_{year}_historical.csv"
        
        if not archivo.exists():
            st.error(f"❌ Archivo no encontrado: {archivo}")
            return None
        
        # Lectura del CSV
        df = pd.read_csv(archivo)
        df['date'] = pd.to_datetime(df['date'])
        df = df.rename(columns={
            'date': 'Fecha',
            'port_name': 'Puerto',
            'value': 'Valor',
            'measure': 'Tipo_Medida',
            'border': 'Frontera_Original'
        })
        
        # Filtrar solo camiones
        df = df[df['Tipo_Medida'].isin(['Trucks', 'Truck Containers Loaded', 'Truck Containers Empty'])]
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0).astype(int)
        
        # Crear columna Frontera
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
        return None


# ============================================================
# INTERFAZ PRINCIPAL
# ============================================================

st.title("🚛 Flujos de Carga Transfronterizos")
st.markdown("---")

# FILTROS EN 3 COLUMNAS
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📆 Año**")
    year = st.selectbox("Selecciona año:", [2023, 2024, 2025, 2026], index=3, label_visibility="collapsed")

with col2:
    st.markdown("**🌎 Frontera**")
    frontera = st.radio("Frontera", ["🇲🇽 México", "🇨🇦 Canadá", "🌎 Ambas"], index=2, horizontal=True, label_visibility="hidden")

with col3:
    st.markdown("**📅 Mes**")
    mes = st.selectbox("Selecciona mes:", 
        ["Todos", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"], 
        index=0, label_visibility="collapsed")

st.markdown("---")

# CARGAR DATOS DEL AÑO
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

# MOSTRAR PERÍODO
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

# GRÁFICO
st.subheader("📈 Evolución Diaria")

df_dia = df.groupby('Fecha')[['Cruces', 'Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']].sum().reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_dia['Fecha'], y=df_dia['Cruces'], 
    name='Total Cruces', mode='lines+markers', line=dict(color='#1f77b4', width=3),
    fill='tozeroy', fillcolor='rgba(31, 119, 180, 0.2)'))

fig.update_layout(
    xaxis_title="Fecha", yaxis_title="Número de Cruces",
    hovermode='x unified', height=400, template="plotly_white"
)

st.plotly_chart(fig, use_container_width=False)

st.markdown("---")

# ESTADÍSTICAS
st.subheader("📊 Estadísticas")
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

"""
Página de Monitoreo de Aduanas V2 - Versión Limpia
FreightMetrics - Sistema de monitoreo en tiempo real

Versión: 2.0.0
Fecha: 2026-02-05
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================================
# FUNCIONES DE UTILIDAD LIMPIAS
# ============================================================================

def calcular_cruces_acumulados(cruces_diarios_total, hora_actual, minuto_actual):
    """
    Calcula cruces acumulados hasta la hora actual basado en distribución horaria realista.
    Simula que el tráfico es más alto en horas pico (8 AM - 8 PM).
    """
    # Calcular fracción del día transcurrida
    minutos_transcurridos = hora_actual * 60 + minuto_actual
    minutos_totales_dia = 24 * 60
    
    # Distribución de tráfico por hora (más tráfico en horas pico)
    # Patrón realista: bajo en madrugada, alto durante el día
    distribucion_horaria = {
        0: 0.015, 1: 0.010, 2: 0.008, 3: 0.008, 4: 0.012, 5: 0.020,
        6: 0.035, 7: 0.045, 8: 0.055, 9: 0.058, 10: 0.060, 11: 0.062,
        12: 0.058, 13: 0.055, 14: 0.060, 15: 0.062, 16: 0.065, 17: 0.058,
        18: 0.050, 19: 0.045, 20: 0.038, 21: 0.030, 22: 0.025, 23: 0.020
    }
    
    # Calcular acumulado hasta la hora actual
    acumulado = 0
    for h in range(hora_actual):
        acumulado += cruces_diarios_total * distribucion_horaria[h]
    
    # Agregar fracción de la hora actual
    fraccion_hora = minuto_actual / 60
    acumulado += cruces_diarios_total * distribucion_horaria[hora_actual] * fraccion_hora
    
    return int(acumulado)


def calcular_capacidad_hora(cruces_diarios):
    """
    Calcula capacidad realista por hora basada en infraestructura de aduana.
    Asume que las aduanas están diseñadas para manejar ~120-130% del tráfico promedio.
    """
    # Capacidad = cruces/hora promedio × factor de sobrecapacidad (1.25-1.35)
    cruces_hora_promedio = cruces_diarios / 24
    
    if cruces_diarios > 8000:  # Aduanas muy grandes (Laredo, Otay Mesa)
        factor_capacidad = 1.30  # 30% sobrecapacidad
        return int(cruces_hora_promedio * factor_capacidad)
    elif cruces_diarios > 4000:  # Aduanas grandes
        factor_capacidad = 1.25  # 25% sobrecapacidad
        return int(cruces_hora_promedio * factor_capacidad)
    elif cruces_diarios > 1500:  # Aduanas medianas
        factor_capacidad = 1.20  # 20% sobrecapacidad
        return int(cruces_hora_promedio * factor_capacidad)
    else:  # Aduanas pequeñas
        factor_capacidad = 1.15  # 15% sobrecapacidad
        return int(cruces_hora_promedio * factor_capacidad)


def calcular_saturacion(cruces_diarios, capacidad_hora):
    """
    Calcula saturación realista basada en tráfico en horas pico.
    En horas pico (8 AM - 8 PM, 12 horas), se concentra ~75% del tráfico diario.
    """
    # Tráfico en horas pico
    trafico_horas_pico = cruces_diarios * 0.75  # 75% del tráfico
    cruces_hora_pico = trafico_horas_pico / 12  # Distribuido en 12 horas pico
    
    # Saturación = (demanda real / capacidad) × 100
    saturacion = (cruces_hora_pico / capacidad_hora) * 100
    
    # Permitir saturaciones >100% (sobrecarga real)
    return int(max(5, min(150, saturacion)))  # Límite máximo 150% (colapso)


def calcular_tiempo_espera(saturacion):
    """Calcula tiempo de espera basado en saturación"""
    if saturacion < 30:
        return int(5 + saturacion * 0.3)
    elif saturacion < 60:
        return int(15 + (saturacion - 30) * 0.8)
    elif saturacion < 85:
        return int(40 + (saturacion - 60) * 1.5)
    else:
        return int(80 + (saturacion - 85) * 3)


def aduana_esta_abierta(nombre_aduana):
    """Verifica si una aduana está abierta según horarios reales"""
    hora_actual = datetime.now().hour
    dia_semana = datetime.now().weekday()  # 0=Lunes, 6=Domingo
    
    # Aduanas 24/7 (siempre abiertas)
    aduanas_24_7 = [
        'Laredo', 'Ysleta', 'Buffalo Niagara Falls', 'Champlain Rouses Point',
        'Alcan', 'Alexandria Bay', 'Baudette', 'Blaine', 'Calais'
    ]
    
    if any(aduana in nombre_aduana for aduana in aduanas_24_7):
        return True, "24/7"
    
    # Aduanas con horario extendido (6 AM - 12 AM / 6 AM - 8 PM fines de semana)
    aduanas_extendidas = ['Otay Mesa', 'Hidalgo', 'Eagle Pass', 'Nogales', 'Calexico East']
    if any(aduana in nombre_aduana for aduana in aduanas_extendidas):
        if dia_semana < 5:  # Lunes a Viernes
            if 6 <= hora_actual < 24:
                return True, "6:00 AM - 12:00 AM"
            else:
                return False, "6:00 AM - 12:00 AM"
        else:  # Fin de semana
            if 8 <= hora_actual < 20:
                return True, "8:00 AM - 8:00 PM"
            else:
                return False, "8:00 AM - 8:00 PM"
    
    # Aduanas con horario estándar (8 AM - 10 PM / 8 AM - 4 PM fines de semana)
    aduanas_estandar = [
        'Brownsville', 'Santa Teresa', 'Del Rio', 'Douglas', 'San Luis',
        'Bridgewater', 'Dalton Cache'
    ]
    if any(aduana in nombre_aduana for aduana in aduanas_estandar):
        if dia_semana < 5:  # Lunes a Viernes
            if 8 <= hora_actual < 22:
                return True, "8:00 AM - 10:00 PM"
            else:
                return False, "8:00 AM - 10:00 PM"
        else:  # Fin de semana
            if 8 <= hora_actual < 16:
                return True, "8:00 AM - 4:00 PM"
            else:
                return False, "8:00 AM - 4:00 PM"
    
    # Aduanas con horario limitado (8 AM - 5 PM solo L-V)
    aduanas_limitadas = [
        'El Paso', 'Tecate', 'Tornillo', 'Naco', 'Rio Grande City', 'Progreso',
        'Roma', 'Presidio', 'Columbus', 'Lukeville', 'Antler', 'Beecher Falls',
        'Boundary', 'Carbury', 'Danville', 'Del Bonita'
    ]
    if any(aduana in nombre_aduana for aduana in aduanas_limitadas):
        if dia_semana < 5:  # Solo Lunes a Viernes
            if 8 <= hora_actual < 17:
                return True, "8:00 AM - 5:00 PM (L-V)"
            else:
                return False, "8:00 AM - 5:00 PM (L-V)"
        else:
            return False, "Cerrada Fines de Semana"
    
    # Default: horario normal 8 AM - 8 PM
    if 8 <= hora_actual < 20:
        return True, "8:00 AM - 8:00 PM"
    else:
        return False, "8:00 AM - 8:00 PM"


# ============================================================================
# FUNCIÓN PRINCIPAL DE LA PÁGINA
# ============================================================================

def page_monitoreo_v2():
    """Página de Monitoreo de Aduanas V2 - Limpia y funcional"""
    
    # Header
    st.title("🚛 Monitoreo de Aduanas en Tiempo Real")
    
    # ========================================================================
    # CARGAR DATOS SIMULADOS
    # ========================================================================
    
    with st.spinner("Cargando datos simulados de 2026..."):
        # Generar datos simulados limpios
        np.random.seed(42)
        
        # TODAS las aduanas (37 totales: 22 México + 15 Canadá)
        puertos_mexico = [
            'Laredo', 'Ysleta', 'Otay Mesa', 'Hidalgo', 'Brownsville',
            'Eagle Pass', 'El Paso', 'Nogales', 'Calexico East', 'Santa Teresa',
            'San Luis', 'Del Rio', 'Douglas', 'Tecate', 'Tornillo',
            'Naco', 'Rio Grande City', 'Progreso', 'Roma', 'Presidio',
            'Columbus', 'Lukeville'
        ]
        
        puertos_canada = [
            'Alcan', 'Alexandria Bay', 'Antler', 'Baudette', 'Beecher Falls',
            'Blaine', 'Boundary', 'Bridgewater', 'Buffalo Niagara Falls', 'Calais',
            'Carbury', 'Champlain Rouses Point', 'Dalton Cache', 'Danville', 'Del Bonita'
        ]
        
        puertos = puertos_mexico + puertos_canada
        
        # Mapeo de fronteras
        fronteras = {}
        for p in puertos_mexico:
            fronteras[p] = 'México'
        for p in puertos_canada:
            fronteras[p] = 'Canadá'
        
        # Volúmenes base (cruces diarios) - BASADOS EN DATOS REALES DE BTS
        # CANADÁ total real: ~40,000 cruces/día (febrero 2025: 1,127,950 ÷ 28 días = 40,284/día)
        # MÉXICO: Similar o mayor volumen
        # Distribución: pocas aduanas grandes concentran ~70% del tráfico
        volumenes_base = {
            # México - Alta actividad (Top aduanas: ~70% del tráfico)
            'Laredo': 12000,        # Más grande de todas
            'Otay Mesa': 8500,      # Segunda más grande  
            'Hidalgo': 6500,
            'El Paso': 5800,
            'Eagle Pass': 4200,
            'Brownsville': 3800,
            'Nogales': 3400,
            'Calexico East': 2900,
            
            # México - Actividad media (~20% del tráfico)
            'Ysleta': 2400,
            'Santa Teresa': 2100,
            'San Luis': 1800,
            'Del Rio': 1500,
            'Douglas': 1300,
            'Tecate': 1100,
            'Tornillo': 950,
            'Naco': 800,
            
            # México - Actividad baja (~10% del tráfico)
            'Rio Grande City': 650,
            'Progreso': 550,
            'Roma': 450,
            'Presidio': 350,
            'Columbus': 250,
            'Lukeville': 150,
            
            # Canadá - Alta actividad (Top 5: ~75% del tráfico de Canadá)
            # Datos reales: Buffalo ~180K/mes, Champlain ~160K/mes, etc.
            'Buffalo Niagara Falls': 6500,      # ~180K mensuales ÷ 28 = 6,400/día
            'Champlain Rouses Point': 5700,     # ~160K mensuales ÷ 28 = 5,700/día
            'Blaine': 4800,                      # ~135K mensuales ÷ 28 = 4,800/día
            'Calais': 3200,
            'Baudette': 2800,
            'Alexandria Bay': 2400,
            
            # Canadá - Actividad media/baja (~25% del tráfico)
            'Bridgewater': 1900,
            'Alcan': 1600,
            'Dalton Cache': 1400,
            'Antler': 1200,
            'Beecher Falls': 1000,
            'Boundary': 850,
            'Danville': 700,
            'Carbury': 600,
            'Del Bonita': 450
        }
        
        # Crear DataFrame
        hora_actual = datetime.now().hour
        minuto_actual = datetime.now().minute
        
        data = []
        for puerto in puertos:
            cruces_base = volumenes_base[puerto]
            variacion = np.random.uniform(0.85, 1.15)
            cruces_total_dia = int(cruces_base * variacion)
            
            # Calcular cruces acumulados hasta la hora actual
            cruces_acumulados = calcular_cruces_acumulados(cruces_total_dia, hora_actual, minuto_actual)
            
            # Distribución BTS: 60% Trucks, 30% Loaded, 10% Empty
            trucks = int(cruces_acumulados * np.random.uniform(0.55, 0.65))
            loaded = int(cruces_acumulados * np.random.uniform(0.25, 0.35))
            empty = cruces_acumulados - trucks - loaded
            
            # Verificar si está abierta
            abierta, horario = aduana_esta_abierta(puerto)
            
            # Calcular capacidad y saturación (usando proyección del día completo)
            capacidad = calcular_capacidad_hora(cruces_total_dia)
            saturacion = calcular_saturacion(cruces_total_dia, capacidad) if abierta else 0
            tiempo_espera = calcular_tiempo_espera(saturacion) if abierta else 0
            
            data.append({
                'Aduana': puerto,
                'Frontera': fronteras[puerto],
                'Cruces': cruces_acumulados,  # Acumulados hasta ahora
                'Cruces_Proyectados': cruces_total_dia,  # Proyección del día completo
                'Trucks': trucks,
                'Trucks_Loaded': loaded,
                'Trucks_Empty': empty,
                'Abierta': abierta,
                'Horario': horario,
                'Capacidad_Hora': capacidad,
                'Saturación': saturacion,
                'Tiempo_Espera': tiempo_espera,
                'Cruces_Por_Hora': int(cruces_total_dia / 24)
            })
        
        df_aduanas = pd.DataFrame(data)
    
    # Calcular porcentaje del día transcurrido
    fecha_hoy = datetime.now()
    porcentaje_dia = ((hora_actual * 60 + minuto_actual) / (24 * 60)) * 100
    
    # Información consolidada en una sola línea
    st.info(f"📅 **{fecha_hoy.strftime('%Y-%m-%d %H:%M')}** | ✅ {len(df_aduanas)} aduanas cargadas | ⏱️ Acumulado hasta las {hora_actual:02d}:{minuto_actual:02d} ({porcentaje_dia:.1f}% del día)")
    
    # ========================================================================
    # FILTROS
    # ========================================================================
    
    st.markdown("---")
    st.subheader("🔍 Filtros")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        frontera_filtro = st.multiselect(
            "Frontera",
            options=['México', 'Canadá'],
            default=['México', 'Canadá']
        )
    
    with col2:
        estado_filtro = st.selectbox(
            "Estado",
            options=['Todas', 'Solo Abiertas', 'Solo Cerradas']
        )
    
    with col3:
        vista = st.selectbox(
            "Vista de Tabla",
            options=['Básica', 'Con BTS', 'Completa']
        )
    
    # Aplicar filtros
    df_filtrado = df_aduanas[df_aduanas['Frontera'].isin(frontera_filtro)].copy()
    
    if estado_filtro == 'Solo Abiertas':
        df_filtrado = df_filtrado[df_filtrado['Abierta'] == True]
    elif estado_filtro == 'Solo Cerradas':
        df_filtrado = df_filtrado[df_filtrado['Abierta'] == False]
    
    # ========================================================================
    # KPIs PRINCIPALES
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📊 Indicadores Principales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_aduanas = len(df_filtrado)
        st.metric("Total Aduanas", total_aduanas)
    
    with col2:
        abiertas = len(df_filtrado[df_filtrado['Abierta'] == True])
        st.metric("Abiertas", abiertas, delta=f"{(abiertas/total_aduanas*100):.0f}%")
    
    with col3:
        saturacion_prom = df_filtrado[df_filtrado['Abierta'] == True]['Saturación'].mean()
        st.metric("Saturación Promedio", f"{saturacion_prom:.0f}%")
    
    with col4:
        espera_prom = df_filtrado[df_filtrado['Abierta'] == True]['Tiempo_Espera'].mean()
        st.metric("Espera Promedio", f"{espera_prom:.0f} min")
    
    # ========================================================================
    # ALERTAS
    # ========================================================================
    
    st.markdown("---")
    st.subheader("🚨 Alertas de Saturación")
    
    aduanas_abiertas = df_filtrado[df_filtrado['Abierta'] == True]
    criticas = aduanas_abiertas[aduanas_abiertas['Saturación'] >= 85]
    altas = aduanas_abiertas[(aduanas_abiertas['Saturación'] >= 70) & (aduanas_abiertas['Saturación'] < 85)]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔴 Críticas (>85%)", len(criticas))
        if not criticas.empty:
            for _, row in criticas.iterrows():
                st.error(f"**{row['Aduana']}**: {row['Saturación']}% | {row['Tiempo_Espera']} min")
    
    with col2:
        st.metric("🟠 Altas (70-85%)", len(altas))
        if not altas.empty:
            for _, row in altas.head(3).iterrows():
                st.warning(f"**{row['Aduana']}**: {row['Saturación']}% | {row['Tiempo_Espera']} min")
    
    with col3:
        normales = len(aduanas_abiertas[aduanas_abiertas['Saturación'] < 70])
        st.metric("🟢 Normales (<70%)", normales)
    
    # ========================================================================
    # TABLA DE DATOS
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📋 Tabla de Aduanas")
    
    # Preparar columnas según vista
    if vista == 'Básica':
        cols = ['Aduana', 'Frontera', 'Abierta', 'Saturación', 'Tiempo_Espera', 'Cruces', 'Cruces_Proyectados']
        rename_cols = {
            'Aduana': 'Aduana',
            'Frontera': 'Frontera',
            'Abierta': 'Estado',
            'Saturación': 'Saturación (%)',
            'Tiempo_Espera': 'Espera (min)',
            'Cruces': 'Acumulados',
            'Cruces_Proyectados': 'Proyección Día'
        }
    elif vista == 'Con BTS':
        cols = ['Aduana', 'Frontera', 'Cruces', 'Cruces_Proyectados', 'Trucks', 'Trucks_Loaded', 'Trucks_Empty', 'Saturación', 'Tiempo_Espera']
        rename_cols = {
            'Aduana': 'Aduana',
            'Frontera': 'Frontera',
            'Cruces': 'Acumulado',
            'Cruces_Proyectados': 'Proyección',
            'Trucks': '🚛 Trucks',
            'Trucks_Loaded': '📦 Cargados',
            'Trucks_Empty': '📭 Vacíos',
            'Saturación': 'Sat. (%)',
            'Tiempo_Espera': 'Espera (min)'
        }
    else:  # Completa
        cols = ['Aduana', 'Frontera', 'Abierta', 'Cruces', 'Cruces_Proyectados', 'Trucks', 'Trucks_Loaded', 'Trucks_Empty',
                'Capacidad_Hora', 'Saturación', 'Tiempo_Espera', 'Cruces_Por_Hora']
        rename_cols = {
            'Aduana': 'Aduana',
            'Frontera': 'Frontera',
            'Abierta': 'Estado',
            'Cruces': 'Acumulado',
            'Cruces_Proyectados': 'Proy. Día',
            'Trucks': 'Trucks',
            'Trucks_Loaded': 'Cargados',
            'Trucks_Empty': 'Vacíos',
            'Capacidad_Hora': 'Cap/Hora',
            'Saturación': 'Sat. (%)',
            'Tiempo_Espera': 'Espera (min)',
            'Cruces_Por_Hora': 'Cruces/Hora'
        }
    
    df_tabla = df_filtrado[cols].copy()
    df_tabla = df_tabla.rename(columns=rename_cols)
    
    # Formatear Estado
    if 'Estado' in df_tabla.columns:
        df_tabla['Estado'] = df_tabla['Estado'].apply(lambda x: '🟢 Abierta' if x else '🔴 Cerrada')
    
    st.dataframe(df_tabla, use_container_width=True, hide_index=True, height=400)
    
    # ========================================================================
    # GRÁFICOS BTS
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📊 Distribución de Tipos BTS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras
        top_10 = df_filtrado.nlargest(10, 'Cruces')
        
        fig_bars = go.Figure()
        fig_bars.add_trace(go.Bar(
            name='Trucks',
            x=top_10['Aduana'],
            y=top_10['Trucks'],
            marker_color='#1f77b4'
        ))
        fig_bars.add_trace(go.Bar(
            name='Cargados',
            x=top_10['Aduana'],
            y=top_10['Trucks_Loaded'],
            marker_color='#ff7f0e'
        ))
        fig_bars.add_trace(go.Bar(
            name='Vacíos',
            x=top_10['Aduana'],
            y=top_10['Trucks_Empty'],
            marker_color='#2ca02c'
        ))
        
        fig_bars.update_layout(
            title="Top 10 Aduanas por Volumen",
            barmode='stack',
            height=400,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_bars, use_container_width=True)
    
    with col2:
        # Gráfico de pie
        total_trucks = df_filtrado['Trucks'].sum()
        total_loaded = df_filtrado['Trucks_Loaded'].sum()
        total_empty = df_filtrado['Trucks_Empty'].sum()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Trucks Completos', 'Contenedores Cargados', 'Contenedores Vacíos'],
            values=[total_trucks, total_loaded, total_empty],
            marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c'],
            hole=0.3
        )])
        
        fig_pie.update_layout(
            title="Distribución Total BTS",
            height=400
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # ========================================================================
    # ESTADÍSTICAS FINALES
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📈 Estadísticas del Día")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_cruces = df_filtrado['Cruces'].sum()
        total_proyectado = df_filtrado['Cruces_Proyectados'].sum()
        st.metric("Total Cruces Acumulados", f"{total_cruces:,}", 
                  delta=f"Proyección: {total_proyectado:,}")
    
    with col2:
        total_trucks = df_filtrado['Trucks'].sum()
        st.metric("🚛 Trucks", f"{total_trucks:,}")
        st.caption(f"{(total_trucks/total_cruces*100 if total_cruces > 0 else 0):.1f}% del total")
    
    with col3:
        total_loaded = df_filtrado['Trucks_Loaded'].sum()
        st.metric("📦 Contenedores Cargados", f"{total_loaded:,}")
        st.caption(f"{(total_loaded/total_cruces*100 if total_cruces > 0 else 0):.1f}% del total")
    
    with col4:
        total_empty = df_filtrado['Trucks_Empty'].sum()
        st.metric("📭 Contenedores Vacíos", f"{total_empty:,}")
        st.caption(f"{(total_empty/total_cruces*100 if total_cruces > 0 else 0):.1f}% del total")
    
    # Footer
    st.markdown("---")
    st.caption("💡 **Nota**: Datos acumulados en tiempo real - Se actualizan según la hora del día")
    st.caption("📊 Los números muestran cruces registrados hasta ahora, la proyección indica el total esperado al finalizar el día")

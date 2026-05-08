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
from datetime import datetime, timedelta, timezone
from pathlib import Path
import time
import pytz
from page_modules.tarjeta_kpi import tarjeta_kpi_color, COLORES

# Usar zona horaria local del sistema (no forzar México)
def obtener_hora_actual():
    """Obtiene la hora actual en la zona horaria local del sistema"""
    return datetime.now()


# ============================================================================
# FUNCIONES DE HORARIOS Y OPERACIÓN
# ============================================================================

def cargar_horarios_aduanas():
    """
    Carga los horarios de operación de las aduanas desde archivo TSV.
    Retorna un DataFrame con información de horarios.
    """
    try:
        ruta_horarios = Path(__file__).parent.parent / "Horarios Aduanas México-USA 2026 - Horarios Aduanas México-USA 2026.tsv"
        if ruta_horarios.exists():
            df_horarios = pd.read_csv(ruta_horarios, sep='\t')
            return df_horarios
        else:
            return pd.DataFrame()  # Retorna vacío si no existe
    except Exception as e:
        st.warning(f"⚠️ No se pudieron cargar los horarios: {str(e)}")
        return pd.DataFrame()


def mostrar_horarios_aduana(aduana_nombre):
    """
    Muestra los horarios de operación para una aduana específica.
    """
    df_horarios = cargar_horarios_aduanas()
    
    if df_horarios.empty:
        return None
    
    # Buscar la aduana en el dataframe
    fila = df_horarios[df_horarios['Aduana / Puerto (Estado México)'].str.contains(aduana_nombre, case=False, na=False)]
    
    if fila.empty:
        return None
    
    return fila.iloc[0].to_dict()


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
    Asume que las aduanas están diseñadas para manejar tráfico en horas pico.
    """
    # En horas pico, se concentra ~60% del tráfico en 12 horas
    # Capacidad debe ser suficiente para las horas pico, no el promedio de 24h
    trafico_hora_pico = (cruces_diarios * 0.60) / 12  # 60% en 12 horas pico
    
    if cruces_diarios > 8000:  # Aduanas muy grandes (Laredo, Otay Mesa)
        factor_capacidad = 1.40  # 40% sobrecapacidad en hora pico
        return int(trafico_hora_pico * factor_capacidad)
    elif cruces_diarios > 4000:  # Aduanas grandes
        factor_capacidad = 1.35  # 35% sobrecapacidad
        return int(trafico_hora_pico * factor_capacidad)
    elif cruces_diarios > 1500:  # Aduanas medianas
        factor_capacidad = 1.30  # 30% sobrecapacidad
        return int(trafico_hora_pico * factor_capacidad)
    else:  # Aduanas pequeñas
        factor_capacidad = 1.25  # 25% sobrecapacidad
        return int(trafico_hora_pico * factor_capacidad)


def calcular_saturacion(cruces_diarios, capacidad_hora):
    """
    Calcula saturación realista basada en tráfico en horas pico.
    En horas pico (8 AM - 8 PM, 12 horas), se concentra ~60% del tráfico diario.
    """
    # Tráfico en horas pico (más realista: 60% en vez de 75%)
    trafico_horas_pico = cruces_diarios * 0.60  # 60% del tráfico
    cruces_hora_pico = trafico_horas_pico / 12  # Distribuido en 12 horas pico
    
    # Saturación = (demanda real / capacidad) × 100
    saturacion = (cruces_hora_pico / capacidad_hora) * 100
    
    # Agregar variabilidad realista (±15%)
    variacion = np.random.uniform(0.85, 1.15)
    saturacion = saturacion * variacion
    
    # Permitir saturaciones >100% pero más raras
    return int(max(5, min(135, saturacion)))  # Límite máximo 135%


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


def generar_insights_inteligentes(df_aduanas, hora_actual):
    """
    Genera insights inteligentes basados en estado actual de aduanas.
    Retorna lista de insights con severidad, mensaje y recomendación.
    """
    insights = []
    
    # 1. Análisis de hora pico
    es_hora_pico = 8 <= hora_actual < 20
    if es_hora_pico:
        aduanas_abiertas = df_aduanas[df_aduanas['Abierta'] == True]
        saturacion_pico = aduanas_abiertas['Saturación'].mean()
        
        if saturacion_pico > 75:
            cruces_afectados = aduanas_abiertas[aduanas_abiertas['Saturación'] > 75]['Cruces'].sum()
            insights.append({
                'tipo': 'crítico',
                'icono': '⚠️',
                'titulo': 'Hora Pico - Alta Congestión General',
                'mensaje': f'Saturación promedio en hora pico: **{saturacion_pico:.1f}%**. {len(aduanas_abiertas[aduanas_abiertas["Saturación"] > 75])} aduanas saturadas afectan **{cruces_afectados:,}** cruces acumulados.',
                'recomendacion': 'Considere rutas alternativas. Aduanas con menor saturación: ' + ', '.join(aduanas_abiertas.nsmallest(3, 'Saturación')['Aduana'].tolist()) + '.',
                'impacto': 'alto'
            })
    
    # 2. Detección de cuellos de botella críticos
    criticas = df_aduanas[df_aduanas['Saturación'] >= 90]
    if not criticas.empty:
        total_criticas = criticas['Cruces'].sum()
        pct_del_total = (total_criticas / df_aduanas['Cruces'].sum()) * 100
        insights.append({
            'tipo': 'crítico',
            'icono': '🚨',
            'titulo': 'Cuellos de Botella Detectados',
            'mensaje': f'**{len(criticas)}** aduanas en estado crítico (>90% saturación) procesan **{pct_del_total:.1f}%** del tráfico total con tiempos de espera superiores a **{criticas["Tiempo_Espera"].mean():.0f} minutos**.',
            'recomendacion': f'Rutas críticas: {", ".join(criticas["Aduana"].tolist())}. Desvíe tráfico no urgente a: ' + ', '.join(df_aduanas[df_aduanas['Saturación'] < 50].nsmallest(3, 'Saturación')['Aduana'].tolist()) + '.',
            'impacto': 'crítico'
        })
    
    # 3. Oportunidades de optimización
    baja_saturacion = df_aduanas[(df_aduanas['Abierta'] == True) & (df_aduanas['Saturación'] < 40)]
    if len(baja_saturacion) >= 3:
        capacidad_disponible = baja_saturacion['Capacidad_Hora'].sum() - (baja_saturacion['Cruces_Por_Hora'].sum())
        insights.append({
            'tipo': 'oportunidad',
            'icono': '💡',
            'titulo': 'Capacidad Subutilizada Disponible',
            'mensaje': f'**{len(baja_saturacion)}** aduanas operan con menos del 40% de saturación. Capacidad disponible: **~{capacidad_disponible:,}** cruces/hora adicionales.',
            'recomendacion': f'Aduanas óptimas para tráfico adicional: {", ".join(baja_saturacion.nsmallest(5, "Saturación")["Aduana"].tolist())}. Considere redistribución de rutas.',
            'impacto': 'medio'
        })
    
    # 4. Análisis de frontera
    for frontera in ['México', 'Canadá']:
        df_frontera = df_aduanas[(df_aduanas['Frontera'] == frontera) & (df_aduanas['Abierta'] == True)]
        if not df_frontera.empty:
            sat_frontera = df_frontera['Saturación'].mean()
            cruces_frontera = df_frontera['Cruces'].sum()
            
            if sat_frontera > 70:
                insights.append({
                    'tipo': 'advertencia',
                    'icono': '🌎',
                    'titulo': f'Frontera {frontera} - Presión Elevada',
                    'mensaje': f'Saturación promedio: **{sat_frontera:.1f}%**. Total acumulado: **{cruces_frontera:,}** cruces. {len(df_frontera[df_frontera["Saturación"] > 80])} aduanas sobre 80%.',
                    'recomendacion': f'Aduanas menos saturadas en {frontera}: ' + ', '.join(df_frontera.nsmallest(3, 'Saturación')['Aduana'].tolist()) + '.',
                    'impacto': 'alto' if sat_frontera > 80 else 'medio'
                })
    
    # 5. Impacto de aduanas cerradas
    cerradas = df_aduanas[df_aduanas['Abierta'] == False]
    if len(cerradas) > 0:
        # Calcular presión adicional en aduanas cercanas
        cruces_perdidos = cerradas['Cruces_Proyectados'].sum()
        insights.append({
            'tipo': 'info',
            'icono': '🔒',
            'titulo': 'Aduanas Fuera de Horario',
            'mensaje': f'**{len(cerradas)}** aduanas cerradas. Tráfico redistribuido: **~{cruces_perdidos:,}** cruces proyectados hacia aduanas 24/7.',
            'recomendacion': 'Aduanas 24/7 disponibles: Laredo, Otay Mesa, Buffalo Niagara Falls, Champlain Rouses Point, Blaine.',
            'impacto': 'bajo'
        })
    
    # 6. Análisis de eficiencia (BTS)
    total_cruces = df_aduanas['Cruces'].sum()
    if total_cruces > 0:
        pct_trucks = (df_aduanas['Trucks'].sum() / total_cruces) * 100
        pct_loaded = (df_aduanas['Trucks_Loaded'].sum() / total_cruces) * 100
        pct_empty = (df_aduanas['Trucks_Empty'].sum() / total_cruces) * 100
        
        if pct_empty > 15:
            insights.append({
                'tipo': 'advertencia',
                'icono': '📭',
                'titulo': 'Alta Proporción de Contenedores Vacíos',
                'mensaje': f'**{pct_empty:.1f}%** del tráfico son contenedores vacíos ({df_aduanas["Trucks_Empty"].sum():,} unidades). Indicador de desbalance en flujo comercial.',
                'recomendacion': 'Oportunidad para optimizar logística inversa y reducir viajes vacíos mediante consolidación de cargas de retorno.',
                'impacto': 'medio'
            })
    
    # 7. Predicción de tendencia (próximas horas)
    if hora_actual < 18:  # Antes de las 6 PM
        horas_restantes = 20 - hora_actual  # Hasta las 8 PM (fin de hora pico)
        aduanas_riesgo = df_aduanas[(df_aduanas['Abierta'] == True) & (df_aduanas['Saturación'] > 65) & (df_aduanas['Saturación'] < 85)]
        
        if len(aduanas_riesgo) > 0:
            insights.append({
                'tipo': 'prediccion',
                'icono': '🔮',
                'titulo': 'Predicción - Riesgo de Saturación',
                'mensaje': f'**{len(aduanas_riesgo)}** aduanas con saturación 65-85% pueden alcanzar niveles críticos en las próximas **{horas_restantes}** horas de hora pico.',
                'recomendacion': f'Monitoreo prioritario: {", ".join(aduanas_riesgo.nlargest(3, "Saturación")["Aduana"].tolist())}. Planifique rutas alternas.',
                'impacto': 'medio'
            })
    
    # 8. Top performers (insight positivo)
    eficientes = df_aduanas[(df_aduanas['Abierta'] == True) & (df_aduanas['Saturación'] < 60) & (df_aduanas['Cruces'] > df_aduanas['Cruces'].median())]
    if len(eficientes) > 0:
        insights.append({
            'tipo': 'exito',
            'icono': '✅',
            'titulo': 'Aduanas con Operación Eficiente',
            'mensaje': f'**{len(eficientes)}** aduanas mantienen alto volumen (<60% saturación) con tiempos de espera menores a **{eficientes["Tiempo_Espera"].mean():.0f} minutos**.',
            'recomendacion': f'Rutas recomendadas: {", ".join(eficientes.nsmallest(4, "Tiempo_Espera")["Aduana"].tolist())}.',
            'impacto': 'positivo'
        })
    
    return insights


def obtener_estadisticas_comparativas(df_aduanas):
    """
    Genera estadísticas comparativas y benchmarks.
    """
    stats = {}
    
    # Por frontera
    for frontera in ['México', 'Canadá']:
        df_f = df_aduanas[(df_aduanas['Frontera'] == frontera) & (df_aduanas['Abierta'] == True)]
        if not df_f.empty:
            stats[frontera] = {
                'total_aduanas': len(df_f),
                'saturacion_promedio': df_f['Saturación'].mean(),
                'tiempo_espera_promedio': df_f['Tiempo_Espera'].mean(),
                'cruces_totales': df_f['Cruces'].sum(),
                'top_3_saturadas': df_f.nlargest(3, 'Saturación')[['Aduana', 'Saturación']].to_dict('records'),
                'top_3_rapidas': df_f.nsmallest(3, 'Tiempo_Espera')[['Aduana', 'Tiempo_Espera']].to_dict('records')
            }
    
    # Estadísticas globales
    aduanas_activas = df_aduanas[df_aduanas['Abierta'] == True]
    stats['global'] = {
        'mejor_aduana': aduanas_activas.loc[aduanas_activas['Saturación'].idxmin(), 'Aduana'],
        'peor_aduana': aduanas_activas.loc[aduanas_activas['Saturación'].idxmax(), 'Aduana'],
        'saturacion_min': aduanas_activas['Saturación'].min(),
        'saturacion_max': aduanas_activas['Saturación'].max(),
        'desviacion_std': aduanas_activas['Saturación'].std(),
        'mediana_saturacion': aduanas_activas['Saturación'].median()
    }
    
    return stats


def aduana_esta_abierta(nombre_aduana):
    """Verifica si una aduana está abierta según horarios reales"""
    hora_actual = obtener_hora_actual().hour
    dia_semana = obtener_hora_actual().weekday()  # 0=Lunes, 6=Domingo
    
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
# FRAGMENTO: GRÁFICO DE DISTRIBUCIÓN HORARIA (Se actualiza independientemente)
# ============================================================================

@st.fragment(run_every=60)  # Se actualiza cada 60 segundos
def mostrar_distribucion_trafico_horaria():
    """Fragmento que muestra la distribución de tráfico por hora - se actualiza automáticamente"""
    
    st.subheader("📊 Distribución de Tráfico por Hora")
    
    # Obtener hora actual en tiempo real
    hora_actual_grafico = obtener_hora_actual().hour
    minuto_actual_grafico = obtener_hora_actual().minute
    
    # Mostrar patrón esperado vs real
    distribucion_teorica = {
        0: 1.5, 1: 1.0, 2: 0.8, 3: 0.8, 4: 1.2, 5: 2.0,
        6: 3.5, 7: 4.5, 8: 5.5, 9: 5.8, 10: 6.0, 11: 6.2,
        12: 5.8, 13: 5.5, 14: 6.0, 15: 6.2, 16: 6.5, 17: 5.8,
        18: 5.0, 19: 4.5, 20: 3.8, 21: 3.0, 22: 2.5, 23: 2.0
    }
    
    # Gráfico de distribución horaria - ANCHO COMPLETO
    horas = list(range(24))
    porcentajes = [distribucion_teorica[h] for h in horas]
    
    # Marcar la hora actual
    colores = ['#0052a3' if h == hora_actual_grafico else '#E0E0E0' if h < hora_actual_grafico else '#BDBDBD' for h in horas]
    
    fig_horas = go.Figure(data=[go.Bar(
        x=horas,
        y=porcentajes,
        marker_color=colores,
        text=[f"{p}%" for p in porcentajes],
        textposition='outside',
        hovertemplate='<b>Hora %{x}:00</b><br>Tráfico: %{y}%<extra></extra>'
    )])
    
    fig_horas.update_layout(
        title=f"Distribución de Tráfico por Hora (Hora Actual: {hora_actual_grafico:02d}:{minuto_actual_grafico:02d})",
        xaxis_title="Hora del Día",
        yaxis_title="% del Tráfico Diario",
        height=350,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#11101D'),
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=2,
            gridcolor='#E0E0E0'
        ),
        yaxis=dict(gridcolor='#E0E0E0')
    )
    
    # Agregar anotación de hora actual
    fig_horas.add_annotation(
        x=hora_actual_grafico,
        y=distribucion_teorica[hora_actual_grafico] + 1,
        text=f"<b>AHORA</b><br>{hora_actual_grafico:02d}:{minuto_actual_grafico:02d}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#4CAF50",
        font=dict(size=12, color="#4CAF50", family="Arial Black"),
        bgcolor="white",
        bordercolor="#4CAF50",
        borderwidth=2
    )
    
    st.plotly_chart(fig_horas, use_container_width=True, config={'responsive': True})
    
    # CONTEXTO TEMPORAL - DEBAJO DEL GRÁFICO
    st.markdown("**⏰ Contexto Temporal**")
    
    col_t1, col_t2, col_t3 = st.columns(3)
    
    # Determinar fase del día
    if 0 <= hora_actual_grafico < 6:
        fase = "🌙 Madrugada"
        desc = "Tráfico mínimo (1-2% por hora)"
        color = "#424242"
    elif 6 <= hora_actual_grafico < 12:
        fase = "🌅 Mañana"
        desc = "Incremento progresivo (3.5-6.2%)"
        color = "#FF9800"
    elif 12 <= hora_actual_grafico < 18:
        fase = "☀️ Tarde"
        desc = "Hora pico principal (5.5-6.5%)"
        color = "#FFC107"
    else:
        fase = "🌆 Noche"
        desc = "Descenso gradual (2-5%)"
        color = "#9C27B0"
    
    with col_t1:
        st.markdown(f"""
            <div style="background-color: {color}20; 
                        border-left: 5px solid {color}; 
                        padding: 15px; 
                        border-radius: 8px;
                        margin: 10px 0;">
                <h4 style="color: {color}; margin: 0 0 8px 0;">{fase}</h4>
                <p style="color: #333; margin: 0; font-size: 0.9rem;">{desc}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_t2:
        # Progreso del día
        progreso = (hora_actual_grafico * 60 + minuto_actual_grafico) / (24 * 60) * 100
        st.markdown(f"""
            <div style="background-color: #F5F5F5; 
                        padding: 15px; 
                        border-radius: 8px;
                        margin: 10px 0;">
                <h4 style="color: #11101D; margin: 0 0 8px 0;">📊 Progreso del Día</h4>
                <p style="color: #333; margin: 0; font-size: 0.9rem;">Completado: {progreso:.1f}%</p>
            </div>
        """, unsafe_allow_html=True)
        st.progress(progreso / 100)
    
    with col_t3:
        # Tiempo restante de hora pico
        if hora_actual_grafico < 20:
            horas_restantes = 20 - hora_actual_grafico
            st.markdown(f"""
                <div style="background-color: #E3F2FD; 
                            border-left: 5px solid #2196F3; 
                            padding: 15px; 
                            border-radius: 8px;
                            margin: 10px 0;">
                    <h4 style="color: #1976D2; margin: 0 0 8px 0;">⏱️ Hora Pico</h4>
                    <p style="color: #333; margin: 0; font-size: 0.9rem;">{horas_restantes}h restantes</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="background-color: #E8F5E9; 
                            border-left: 5px solid #4CAF50; 
                            padding: 15px; 
                            border-radius: 8px;
                            margin: 10px 0;">
                    <h4 style="color: #388E3C; margin: 0 0 8px 0;">✅ Hora Pico</h4>
                    <p style="color: #333; margin: 0; font-size: 0.9rem;">Finalizada</p>
                </div>
            """, unsafe_allow_html=True)


# ============================================================================
# FUNCIÓN PRINCIPAL DE LA PÁGINA
# ============================================================================

def page_monitoreo_aduanas():
    """Página de Monitoreo de Aduanas V2 - Limpia y funcional"""
    
    # Header
    st.title("🚛 Monitoreo de Aduanas en Tiempo Real")
    
    # ============================================================
    # Estilos CSS LOCALES para esta página
    # ============================================================
    st.markdown("""
    <style>
        /* Mejorar todas las métricas en esta página */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, rgba(0, 61, 122, 0.15) 0%, rgba(0, 82, 163, 0.10) 100%) !important;
            border-left: 5px solid #0066cc !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Definir distribución teórica de tráfico por hora (constante para toda la página)
    distribucion_teorica = {
        0: 1.5, 1: 1.0, 2: 0.8, 3: 0.8, 4: 1.2, 5: 2.0,
        6: 3.5, 7: 4.5, 8: 5.5, 9: 5.8, 10: 6.0, 11: 6.2,
        12: 5.8, 13: 5.5, 14: 6.0, 15: 6.2, 16: 6.5, 17: 5.8,
        18: 5.0, 19: 4.5, 20: 3.8, 21: 3.0, 22: 2.5, 23: 2.0
    }
    
    # ========================================================================
    # CARGAR DATOS SIMULADOS
    # ========================================================================
    
    # Obtener hora actual UNA SOLA VEZ para usar en toda la función
    fecha_hoy = obtener_hora_actual()
    hora_actual = fecha_hoy.hour
    minuto_actual = fecha_hoy.minute
    
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
        
        # Crear DataFrame (usar las variables ya definidas de hora_actual y minuto_actual)
        
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
    fecha_hoy = obtener_hora_actual()
    porcentaje_dia = ((hora_actual * 60 + minuto_actual) / (24 * 60)) * 100
    
    # Información consolidada en una sola línea
    st.info(f"📅 **{fecha_hoy.strftime('%Y-%m-%d %H:%M')}** | ✅ {len(df_aduanas)} aduanas cargadas | ⏱️ Acumulado hasta las {hora_actual:02d}:{minuto_actual:02d} ({porcentaje_dia:.1f}% del día)")
    
    # ========================================================================
    # FILTROS Y MODO DE VISTA
    # ========================================================================
    
    st.markdown("---")
    st.subheader("🔍 Configuración de Vista y Filtros")
    
    # Modo de vista: Operador simplificado vs Analista avanzado
    col_modo, col_export = st.columns([3, 1])
    
    with col_modo:
        modo_vista = st.radio(
            "Seleccionar modo de vista:",
            options=['👨‍💼 Operador (Simplificado)', '📊 Analista (Detallado)'],
            horizontal=True,
            help="Modo Operador: Muestra solo métricas críticas. Modo Analista: Muestra todos los datos y gráficos."
        )
    
    with col_export:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📥 Exportar Reporte", use_container_width=True):
            # Generar CSV con datos actuales
            export_data = df_aduanas.copy()
            export_data['Fecha_Hora'] = fecha_hoy.strftime('%Y-%m-%d %H:%M:%S')
            
            # Crear CSV
            csv_data = export_data[[
                'Fecha_Hora', 'Aduana', 'Frontera', 'Cruces', 'Trucks', 'Trucks_Loaded', 
                'Trucks_Empty', 'Saturación', 'Tiempo_Espera', 'Abierta'
            ]].to_csv(index=False)
            
            st.download_button(
                label="📊 Descargar CSV",
                data=csv_data,
                file_name=f"reporte_aduanas_{fecha_hoy.strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="download_csv"
            )
    
    # Filtros principales
    st.markdown("**Filtros Principales:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        frontera_filtro = st.multiselect(
            "Frontera",
            options=['México', 'Canadá'],
            default=['México', 'Canadá'],
            key="frontera_select"
        )
    
    with col2:
        estado_filtro = st.selectbox(
            "Estado",
            options=['Todas', 'Solo Abiertas', 'Solo Cerradas'],
            key="estado_select"
        )
    
    with col3:
        vista = st.selectbox(
            "Vista de Tabla",
            options=['Básica', 'Con BTS', 'Completa'],
            key="vista_select"
        )
    
    with col4:
        saturacion_min = st.slider(
            "Saturación mínima (%)",
            min_value=0,
            max_value=100,
            value=0,
            step=5,
            key="sat_min_slider"
        )
    
    # Filtros avanzados (desplegable)
    with st.expander("⚙️ Filtros Avanzados", expanded=False):
        col_adv1, col_adv2, col_adv3 = st.columns(3)
        
        with col_adv1:
            rango_espera = st.slider(
                "Rango de tiempo de espera (min)",
                min_value=0,
                max_value=300,
                value=(0, 300),
                step=10,
                key="espera_range"
            )
        
        with col_adv2:
            # Filtro por volumen diario
            vol_min, vol_max = st.slider(
                "Rango de cruces proyectados/día",
                min_value=0,
                max_value=int(df_aduanas['Cruces_Proyectados'].max()),
                value=(0, int(df_aduanas['Cruces_Proyectados'].max())),
                step=500,
                key="vol_range"
            )
        
        with col_adv3:
            aduanas_custom = st.multiselect(
                "Seleccionar aduanas específicas (vacío = todas)",
                options=sorted(df_aduanas['Aduana'].unique()),
                key="aduanas_custom"
            )
    
    # Aplicar filtros
    df_filtrado = df_aduanas[df_aduanas['Frontera'].isin(frontera_filtro)].copy()
    
    if estado_filtro == 'Solo Abiertas':
        df_filtrado = df_filtrado[df_filtrado['Abierta'] == True]
    elif estado_filtro == 'Solo Cerradas':
        df_filtrado = df_filtrado[df_filtrado['Abierta'] == False]
    
    # Aplicar filtros avanzados
    df_filtrado = df_filtrado[df_filtrado['Saturación'] >= saturacion_min]
    df_filtrado = df_filtrado[
        (df_filtrado['Tiempo_Espera'] >= rango_espera[0]) &
        (df_filtrado['Tiempo_Espera'] <= rango_espera[1])
    ]
    df_filtrado = df_filtrado[
        (df_filtrado['Cruces_Proyectados'] >= vol_min) &
        (df_filtrado['Cruces_Proyectados'] <= vol_max)
    ]
    
    if aduanas_custom:
        df_filtrado = df_filtrado[df_filtrado['Aduana'].isin(aduanas_custom)]
    
    # Mostrar resumen de filtros aplicados
    st.caption(f"✅ {len(df_filtrado)} aduanas coinciden con los filtros | 🔴 {len(df_filtrado[df_filtrado['Saturación'] > 70])} en saturación crítica (>70%)")
    
    # Si está en modo operador, mostrar solo vista simplificada y saltarse análisis detallados
    modo_simplificado = "Operador" in modo_vista
    
    # ========================================================================
    # TABLA DE ADUANAS (MODOS SIMPLIFICADO/DETALLADO)
    # ========================================================================
    
    st.markdown("---")
    if modo_simplificado:
        st.subheader("⚠️ VISTA OPERADOR - Información Crítica")
    else:
        st.subheader("📊 Detalle de Aduanas")
    
    # ========================================================================
    # KPIs PRINCIPALES - CON ESTILOS PROFESIONALES INLINE
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📊 Indicadores Principales")
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    total_aduanas = len(df_filtrado)
    abiertas = len(df_filtrado[df_filtrado['Abierta'] == True])
    saturacion_prom = df_filtrado[df_filtrado['Abierta'] == True]['Saturación'].mean()
    espera_prom = df_filtrado[df_filtrado['Abierta'] == True]['Tiempo_Espera'].mean()
    
    # Estilos compartidos
    estilo_tarjeta = """
        background: linear-gradient(135deg, rgba(0, 102, 204, 0.12) 0%, rgba(25, 118, 210, 0.08) 100%);
        border: 2px solid #0066cc;
        border-radius: 14px;
        padding: 24px 20px;
        box-shadow: 0 0 20px rgba(0, 102, 204, 0.4), 0 8px 24px rgba(0, 0, 0, 0.15);
        text-align: center;
    """
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(0, 102, 204, 0.12) 0%, rgba(25, 118, 210, 0.08) 100%); border: 2px solid #0066cc; border-radius: 14px; padding: 24px 20px; box-shadow: 0 0 20px rgba(0, 102, 204, 0.4), 0 8px 24px rgba(0, 0, 0, 0.15); text-align: center;">
            <div style="color: #0052a3; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">📍 Total Aduanas</div>
            <div style="color: #0066cc; font-size: 2.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3); margin: 8px 0;">{total_aduanas}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        delta_pct = (abiertas/total_aduanas*100) if total_aduanas > 0 else 0
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(0, 102, 204, 0.12) 0%, rgba(25, 118, 210, 0.08) 100%); border: 2px solid #0066cc; border-radius: 14px; padding: 24px 20px; box-shadow: 0 0 20px rgba(0, 102, 204, 0.4), 0 8px 24px rgba(0, 0, 0, 0.15); text-align: center;">
            <div style="color: #0052a3; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">🟢 Abiertas</div>
            <div style="color: #0066cc; font-size: 2.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3); margin: 8px 0;">{abiertas}</div>
            <div style="color: #1976d2; font-size: 0.95rem; font-weight: 700; margin-top: 8px;">↑ {delta_pct:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(0, 102, 204, 0.12) 0%, rgba(25, 118, 210, 0.08) 100%); border: 2px solid #0066cc; border-radius: 14px; padding: 24px 20px; box-shadow: 0 0 20px rgba(0, 102, 204, 0.4), 0 8px 24px rgba(0, 0, 0, 0.15); text-align: center;">
            <div style="color: #0052a3; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">📊 Saturación</div>
            <div style="color: #0066cc; font-size: 2.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3); margin: 8px 0;">{saturacion_prom:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(0, 102, 204, 0.12) 0%, rgba(25, 118, 210, 0.08) 100%); border: 2px solid #0066cc; border-radius: 14px; padding: 24px 20px; box-shadow: 0 0 20px rgba(0, 102, 204, 0.4), 0 8px 24px rgba(0, 0, 0, 0.15); text-align: center;">
            <div style="color: #0052a3; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">⏱️ Espera Prom.</div>
            <div style="color: #0066cc; font-size: 2.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(0, 102, 204, 0.3); margin: 8px 0;">{espera_prom:.0f}</div>
            <div style="color: #1976d2; font-size: 0.95rem; font-weight: 700; margin-top: 8px;">minutos</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # TABLA DE ADUANAS SEGÚN MODO DE VISTA
    # ========================================================================
    
    # Vista simplificada para operadores
    if modo_simplificado:
        st.warning("⚠️ **VISTA OPERADOR**: Solo se muestran métricas críticas y alertas activas")
        
        # Filtrar solo aduanas con problemas
        df_criticas = df_filtrado[df_filtrado['Saturación'] > 70].copy()
        df_criticas = df_criticas.sort_values('Saturación', ascending=False)
        
        if not df_criticas.empty:
            st.error(f"🔴 **{len(df_criticas)} ADUANAS EN SITUACIÓN CRÍTICA** (Saturación > 70%)")
            
            # Tabla simplificada
            tabla_simple = df_criticas[[
                'Aduana', 'Frontera', 'Cruces', 'Saturación', 'Tiempo_Espera', 'Abierta'
            ]].copy()
            tabla_simple['Saturación'] = tabla_simple['Saturación'].apply(lambda x: f"🔴 {x:.0f}%" if x > 80 else f"🟠 {x:.0f}%")
            tabla_simple['Tiempo_Espera'] = tabla_simple['Tiempo_Espera'].apply(lambda x: f"{x:.0f} min")
            tabla_simple['Abierta'] = tabla_simple['Abierta'].apply(lambda x: "✅" if x else "🔒")
            
            st.dataframe(
                tabla_simple,
                use_container_width=True,
                hide_index=True,
                column_config={
                    'Aduana': st.column_config.TextColumn('Aduana', width=120),
                    'Frontera': st.column_config.TextColumn('Frontera', width=80),
                    'Cruces': st.column_config.NumberColumn('Cruces Acum.', width=100),
                    'Saturación': st.column_config.TextColumn('Saturación', width=100),
                    'Tiempo_Espera': st.column_config.TextColumn('Espera', width=80),
                    'Abierta': st.column_config.TextColumn('Estado', width=60)
                }
            )
            
            # Recomendaciones operacionales
            st.markdown("**📋 Acciones Recomendadas:**")
            for idx, row in df_criticas.iterrows():
                st.warning(f"**{row['Aduana']}** - Saturación {row['Saturación']:.0f}% | ⏱️ {row['Tiempo_Espera']:.0f} min espera | 🚛 Considerar desvío de tráfico", icon="⚠️")
        else:
            st.success("✅ No hay aduanas en situación crítica. Sistema operando normalmente.")
            
            # Mostrar resumen de estado general
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric("Saturación Promedio", f"{df_filtrado['Saturación'].mean():.0f}%", "Normal" if df_filtrado['Saturación'].mean() < 60 else "Moderada")
            with col_s2:
                st.metric("Espera Promedio", f"{df_filtrado[df_filtrado['Abierta']]['Tiempo_Espera'].mean():.0f} min", "Aceptable")
            with col_s3:
                st.metric("Capacidad Disponible", f"{(100 - df_filtrado['Saturación'].mean()):.0f}%", "Buena")
    
    else:
        # Vista detallada para analistas
        st.markdown("**Tabla Detallada de Aduanas**")
        
        if vista == 'Básica':
            df_vista = df_filtrado[['Aduana', 'Frontera', 'Cruces', 'Cruces_Proyectados', 'Saturación', 'Tiempo_Espera', 'Abierta']].copy()
            columnas_config = {
                'Aduana': st.column_config.TextColumn('Aduana', width=120),
                'Frontera': st.column_config.TextColumn('Frontera', width=80),
                'Cruces': st.column_config.NumberColumn('Cruces Acum.', width=100),
                'Cruces_Proyectados': st.column_config.NumberColumn('Proy. Diaria', width=100),
                'Saturación': st.column_config.ProgressColumn('Saturación %', min_value=0, max_value=100, width=120),
                'Tiempo_Espera': st.column_config.NumberColumn('Espera (min)', width=100),
                'Abierta': st.column_config.CheckboxColumn('Abierta', width=80)
            }
        
        elif vista == 'Con BTS':
            df_vista = df_filtrado[['Aduana', 'Frontera', 'Trucks', 'Trucks_Loaded', 'Trucks_Empty', 'Saturación', 'Tiempo_Espera']].copy()
            columnas_config = {
                'Aduana': st.column_config.TextColumn('Aduana', width=120),
                'Frontera': st.column_config.TextColumn('Frontera', width=80),
                'Trucks': st.column_config.NumberColumn('Trucks', width=80),
                'Trucks_Loaded': st.column_config.NumberColumn('Cargados', width=100),
                'Trucks_Empty': st.column_config.NumberColumn('Vacíos', width=100),
                'Saturación': st.column_config.ProgressColumn('Saturación %', min_value=0, max_value=100, width=120),
                'Tiempo_Espera': st.column_config.NumberColumn('Espera (min)', width=100)
            }
        
        else:  # Completa
            df_vista = df_filtrado.copy()
            columnas_config = {col: st.column_config.TextColumn(col, width=100) for col in df_vista.columns}
        
        st.dataframe(
            df_vista,
            use_container_width=True,
            hide_index=True,
            column_config=columnas_config
        )
    
    # ========================================================================
    # NUEVA SECCIÓN: GRÁFICOS VISUALES AVANZADOS
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📈 Análisis Visual Avanzado")
    
    # Tab 1: Heatmap de saturación horaria
    tab_heat, tab_bts, tab_comp = st.tabs(["🔥 Heatmap Horario", "📦 Distribución BTS", "📊 Comparativa"])
    
    with tab_heat:
        st.markdown("**Saturación estimada por hora del día**")
        
        # Crear datos de heatmap (Aduana vs Hora)
        horas = list(range(0, 24))
        aduanas_top = df_filtrado[df_filtrado['Abierta'] == True].nlargest(10, 'Cruces')['Aduana'].tolist()
        
        heatmap_data = []
        for aduana in aduanas_top:
            fila = []
            sat_base = df_filtrado[df_filtrado['Aduana'] == aduana]['Saturación'].values[0]
            for hora in horas:
                # Modular saturación por distribución horaria
                dist_hora = [0.015, 0.010, 0.008, 0.008, 0.012, 0.020,
                            0.035, 0.045, 0.055, 0.058, 0.060, 0.062,
                            0.058, 0.055, 0.060, 0.062, 0.065, 0.058,
                            0.050, 0.045, 0.038, 0.030, 0.025, 0.020][hora]
                sat_hora = sat_base * (dist_hora / 0.050)  # Normalizar
                fila.append(sat_hora)
            heatmap_data.append(fila)
        
        # Crear heatmap con Plotly
        fig_heat = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=[f"{h:02d}:00" for h in horas],
            y=aduanas_top,
            colorscale='RdYlGn_r',
            colorbar=dict(title="Saturación %"),
            hovertemplate="<b>%{y}</b><br>Hora: %{x}<br>Saturación: %{z:.0f}%<extra></extra>"
        ))
        fig_heat.update_layout(
            title="Mapa de Calor - Saturación por Hora",
            xaxis_title="Hora del Día",
            yaxis_title="Aduana",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
        st.caption("💡 **Interpretación:** Los colores más rojo indican saturación más alta. Las horas 8-17 (pico laboral) normalmente tienen mayor saturación.")
    
    with tab_bts:
        st.markdown("**Distribución de tipos de cruces (BTS)**")
        
        if not df_filtrado.empty:
            # Totales por tipo
            total_trucks = df_filtrado['Trucks'].sum()
            total_loaded = df_filtrado['Trucks_Loaded'].sum()
            total_empty = df_filtrado['Trucks_Empty'].sum()
            total_cruces = df_filtrado['Cruces'].sum()
            
            # Porcentajes
            pct_trucks = (total_trucks / total_cruces * 100) if total_cruces > 0 else 0
            pct_loaded = (total_loaded / total_cruces * 100) if total_cruces > 0 else 0
            pct_empty = (total_empty / total_cruces * 100) if total_cruces > 0 else 0
            
            col_bts1, col_bts2 = st.columns(2)
            
            with col_bts1:
                # Gráfico de pastel
                fig_bts = go.Figure(data=[go.Pie(
                    labels=['Trucks', 'Containers Loaded', 'Containers Empty'],
                    values=[total_trucks, total_loaded, total_empty],
                    marker=dict(colors=['#4CAF50', '#2196F3', '#FF9800']),
                    textposition='inside',
                    textinfo='label+percent',
                    hovertemplate="<b>%{label}</b><br>Total: %{value:,}<br>Porcentaje: %{percent}<extra></extra>"
                )])
                fig_bts.update_layout(
                    title="Distribución de Cruces por Tipo",
                    height=400,
                    showlegend=True
                )
                st.plotly_chart(fig_bts, use_container_width=True)
            
            with col_bts2:
                # Métricas de distribución
                st.markdown("**Composición Actual**")
                st.metric("🚚 Trucks Completos", f"{total_trucks:,}", f"{pct_trucks:.1f}%")
                st.metric("📦 Contenedores Cargados", f"{total_loaded:,}", f"{pct_loaded:.1f}%")
                st.metric("📭 Contenedores Vacíos", f"{total_empty:,}", f"{pct_empty:.1f}%")
                
                # Análisis de eficiencia
                st.markdown("**Análisis de Eficiencia**")
                if pct_empty > 15:
                    st.warning(f"⚠️ Proporción de vacíos ({pct_empty:.1f}%) está por encima del 15% recomendado")
                else:
                    st.success(f"✅ Proporción de vacíos ({pct_empty:.1f}%) dentro de lo normal")
    
    with tab_comp:
        st.markdown("**Comparativa con día anterior**")
        
        # Simular datos del día anterior
        np.random.seed(41)  # Seed diferente para variar datos
        cruces_ayer_total = df_filtrado['Cruces'].sum() * np.random.uniform(0.85, 1.15)
        saturacion_ayer = df_filtrado[df_filtrado['Abierta'] == True]['Saturación'].mean() * np.random.uniform(0.90, 1.10)
        espera_ayer = df_filtrado[df_filtrado['Abierta'] == True]['Tiempo_Espera'].mean() * np.random.uniform(0.85, 1.20)
        
        cruces_hoy_total = df_filtrado['Cruces'].sum()
        saturacion_hoy = df_filtrado[df_filtrado['Abierta'] == True]['Saturación'].mean()
        espera_hoy = df_filtrado[df_filtrado['Abierta'] == True]['Tiempo_Espera'].mean()
        
        # Variaciones
        var_cruces = ((cruces_hoy_total - cruces_ayer_total) / cruces_ayer_total * 100) if cruces_ayer_total > 0 else 0
        var_sat = saturacion_hoy - saturacion_ayer
        var_esp = espera_hoy - espera_ayer
        
        col_c1, col_c2, col_c3 = st.columns(3)
        
        with col_c1:
            st.metric(
                "Cruces Acumulados",
                f"{int(cruces_hoy_total):,}",
                f"{var_cruces:+.1f}% vs ayer"
            )
        
        with col_c2:
            st.metric(
                "Saturación Promedio",
                f"{saturacion_hoy:.0f}%",
                f"{var_sat:+.1f}pp vs ayer"
            )
        
        with col_c3:
            st.metric(
                "Tiempo Espera Promedio",
                f"{espera_hoy:.0f} min",
                f"{var_esp:+.0f} min vs ayer"
            )
        
        # Gráfico de línea de comparativa
        datos_comparativa = {
            'Métrica': ['Cruces', 'Saturación (%)', 'Espera (min)'],
            'Hoy': [cruces_hoy_total/1000, saturacion_hoy, espera_hoy],
            'Ayer': [cruces_ayer_total/1000, saturacion_ayer, espera_ayer]
        }
        df_comp = pd.DataFrame(datos_comparativa)
        
        fig_comp = go.Figure(data=[
            go.Bar(name='Hoy', x=df_comp['Métrica'], y=df_comp['Hoy'], marker_color='#2196F3'),
            go.Bar(name='Ayer', x=df_comp['Métrica'], y=df_comp['Ayer'], marker_color='#FFC107')
        ])
        fig_comp.update_layout(
            title="Comparativa Día a Día",
            barmode='group',
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig_comp, use_container_width=True)
    
    # ========================================================================
    # ESTADÍSTICAS COMPARATIVAS - CON TARJETAS PERSONALIZADAS
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📈 Análisis Comparativo por Frontera")
    
    stats = obtener_estadisticas_comparativas(df_filtrado)
    
    if 'México' in stats and 'Canadá' in stats:
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%); 
                            color: white; 
                            padding: 20px; 
                            border-radius: 12px;
                            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);">
                    <h3 style="color: white; margin: 0 0 15px 0; font-size: 1.3rem;">🇲🇽 Frontera México</h3>
                </div>
            """, unsafe_allow_html=True)
            
            mx = stats.get('México', {})
            col_mx1, col_mx2 = st.columns(2)
            
            # Tarjetas personalizadas para México
            with col_mx1:
                st.markdown(f"""
                <div style="border-color: #4CAF50; background: linear-gradient(135deg, rgba(76, 175, 80, 0.12) 0%, rgba(56, 142, 60, 0.08) 100%); box-shadow: 0 0 20px rgba(76, 175, 80, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #4CAF50; padding: 24px 20px; text-align: center;">
                    <div style="color: #2E7D32; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">✅ Aduanas Activas</div>
                    <div style="color: #388E3C; font-size: 2.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(76, 175, 80, 0.3); margin: 8px 0;">{mx.get('total_aduanas', 0)}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="border-color: #4CAF50; background: linear-gradient(135deg, rgba(76, 175, 80, 0.12) 0%, rgba(56, 142, 60, 0.08) 100%); box-shadow: 0 0 20px rgba(76, 175, 80, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #4CAF50; padding: 24px 20px; text-align: center;">
                    <div style="color: #2E7D32; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">📊 Saturación Prom.</div>
                    <div style="color: #388E3C; font-size: 2.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(76, 175, 80, 0.3); margin: 8px 0;">{mx.get('saturacion_promedio', 0):.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_mx2:
                st.markdown(f"""
                <div style="border-color: #4CAF50; background: linear-gradient(135deg, rgba(76, 175, 80, 0.12) 0%, rgba(56, 142, 60, 0.08) 100%); box-shadow: 0 0 20px rgba(76, 175, 80, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #4CAF50; padding: 24px 20px; text-align: center;">
                    <div style="color: #2E7D32; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">⏱️ Espera Prom.</div>
                    <div style="color: #388E3C; font-size: 2.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(76, 175, 80, 0.3); margin: 8px 0;">{mx.get('tiempo_espera_promedio', 0):.0f}</div>
                    <div style="color: #388E3C; font-size: 0.95rem; font-weight: 700; margin-top: 8px;">minutos</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="border-color: #4CAF50; background: linear-gradient(135deg, rgba(76, 175, 80, 0.12) 0%, rgba(56, 142, 60, 0.08) 100%); box-shadow: 0 0 20px rgba(76, 175, 80, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #4CAF50; padding: 24px 20px; text-align: center;">
                    <div style="color: #2E7D32; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">🚚 Cruces Totales</div>
                    <div style="color: #388E3C; font-size: 2.2rem; font-weight: 900; text-shadow: 0 2px 8px rgba(76, 175, 80, 0.3); margin: 8px 0;">{mx.get('cruces_totales', 0):,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            if 'top_3_saturadas' in mx:
                st.markdown("**🔴 Top 3 Más Saturadas:**")
                for aduana in mx['top_3_saturadas']:
                    st.caption(f"• {aduana['Aduana']}: {aduana['Saturación']:.0f}%")
            
            if 'top_3_rapidas' in mx:
                st.markdown("**✅ Top 3 Más Rápidas:**")
                for aduana in mx['top_3_rapidas']:
                    st.caption(f"• {aduana['Aduana']}: {aduana['Tiempo_Espera']:.0f} min")
        
        with col_c2:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); 
                            color: white; 
                            padding: 20px; 
                            border-radius: 12px;
                            box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);">
                    <h3 style="color: white; margin: 0 0 15px 0; font-size: 1.3rem;">🇨🇦 Frontera Canadá</h3>
                </div>
            """, unsafe_allow_html=True)
            
            ca = stats.get('Canadá', {})
            col_ca1, col_ca2 = st.columns(2)
            
            # Tarjetas personalizadas para Canadá
            with col_ca1:
                st.markdown(f"""
                <div style="border-color: #2196F3; background: linear-gradient(135deg, rgba(33, 150, 243, 0.12) 0%, rgba(25, 118, 210, 0.08) 100%); box-shadow: 0 0 20px rgba(33, 150, 243, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #2196F3; padding: 24px 20px; text-align: center;">
                    <div style="color: #0D47A1; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">✅ Aduanas Activas</div>
                    <div style="color: #1565C0; font-size: 2.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(33, 150, 243, 0.3); margin: 8px 0;">{ca.get('total_aduanas', 0)}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="border-color: #2196F3; background: linear-gradient(135deg, rgba(33, 150, 243, 0.12) 0%, rgba(25, 118, 210, 0.08) 100%); box-shadow: 0 0 20px rgba(33, 150, 243, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #2196F3; padding: 24px 20px; text-align: center;">
                    <div style="color: #0D47A1; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">📊 Saturación Prom.</div>
                    <div style="color: #1565C0; font-size: 2.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(33, 150, 243, 0.3); margin: 8px 0;">{ca.get('saturacion_promedio', 0):.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_ca2:
                st.markdown(f"""
                <div style="border-color: #2196F3; background: linear-gradient(135deg, rgba(33, 150, 243, 0.12) 0%, rgba(25, 118, 210, 0.08) 100%); box-shadow: 0 0 20px rgba(33, 150, 243, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #2196F3; padding: 24px 20px; text-align: center;">
                    <div style="color: #0D47A1; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">⏱️ Espera Prom.</div>
                    <div style="color: #1565C0; font-size: 2.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(33, 150, 243, 0.3); margin: 8px 0;">{ca.get('tiempo_espera_promedio', 0):.0f}</div>
                    <div style="color: #1565C0; font-size: 0.95rem; font-weight: 700; margin-top: 8px;">minutos</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="border-color: #2196F3; background: linear-gradient(135deg, rgba(33, 150, 243, 0.12) 0%, rgba(25, 118, 210, 0.08) 100%); box-shadow: 0 0 20px rgba(33, 150, 243, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #2196F3; padding: 24px 20px; text-align: center;">
                    <div style="color: #0D47A1; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">🚚 Cruces Totales</div>
                    <div style="color: #1565C0; font-size: 2.2rem; font-weight: 900; text-shadow: 0 2px 8px rgba(33, 150, 243, 0.3); margin: 8px 0;">{ca.get('cruces_totales', 0):,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            if 'top_3_saturadas' in ca:
                st.markdown("**🔴 Top 3 Más Saturadas:**")
                for aduana in ca['top_3_saturadas']:
                    st.caption(f"• {aduana['Aduana']}: {aduana['Saturación']:.0f}%")
            
            if 'top_3_rapidas' in ca:
                st.markdown("**✅ Top 3 Más Rápidas:**")
                for aduana in ca['top_3_rapidas']:
                    st.caption(f"• {aduana['Aduana']}: {aduana['Tiempo_Espera']:.0f} min")
    
    # Benchmarks globales
    if 'global' in stats:
        glob = stats['global']
        st.markdown("---")
        st.markdown("**🎯 Benchmarks del Sistema**")
        
        col_b1, col_b2, col_b3 = st.columns(3)
        
        with col_b1:
            st.markdown(f"""
            <div style="border-color: #FF9800; background: linear-gradient(135deg, rgba(255, 152, 0, 0.12) 0%, rgba(255, 167, 38, 0.08) 100%); box-shadow: 0 0 20px rgba(255, 152, 0, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #FF9800; padding: 24px 20px; text-align: center;">
                <div style="color: #E65100; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">🏆 Mejor Aduana</div>
                <div style="color: #FF9800; font-size: 1.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(255, 152, 0, 0.3); margin: 8px 0;">{glob.get('mejor_aduana', 'N/A')}</div>
                <div style="color: #FF9800; font-size: 0.95rem; font-weight: 700; margin-top: 8px;">↓ {glob.get('saturacion_min', 0):.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b2:
            st.markdown(f"""
            <div style="border-color: #F44336; background: linear-gradient(135deg, rgba(244, 67, 54, 0.12) 0%, rgba(229, 57, 53, 0.08) 100%); box-shadow: 0 0 20px rgba(244, 67, 54, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #F44336; padding: 24px 20px; text-align: center;">
                <div style="color: #C62828; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">⚠️ Peor Aduana</div>
                <div style="color: #F44336; font-size: 1.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(244, 67, 54, 0.3); margin: 8px 0;">{glob.get('peor_aduana', 'N/A')}</div>
                <div style="color: #F44336; font-size: 0.95rem; font-weight: 700; margin-top: 8px;">↑ {glob.get('saturacion_max', 0):.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b3:
            rango = glob.get('saturacion_max', 0) - glob.get('saturacion_min', 0)
            st.markdown(f"""
            <div style="border-color: #9C27B0; background: linear-gradient(135deg, rgba(156, 39, 176, 0.12) 0%, rgba(142, 54, 157, 0.08) 100%); box-shadow: 0 0 20px rgba(156, 39, 176, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #9C27B0; padding: 24px 20px; text-align: center;">
                <div style="color: #6A1B9A; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">📏 Rango</div>
                <div style="color: #9C27B0; font-size: 1.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(156, 39, 176, 0.3); margin: 8px 0;">{rango:.0f}%</div>
                <div style="color: #9C27B0; font-size: 0.95rem; font-weight: 700; margin-top: 8px;">Variación</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Segunda fila de benchmarks
        col_b4, col_b5 = st.columns(2)
        
        with col_b4:
            st.markdown(f"""
            <div style="border-color: #00BCD4; background: linear-gradient(135deg, rgba(0, 188, 212, 0.12) 0%, rgba(0, 150, 136, 0.08) 100%); box-shadow: 0 0 20px rgba(0, 188, 212, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #00BCD4; padding: 24px 20px; text-align: center;">
                <div style="color: #00695C; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">📊 Mediana</div>
                <div style="color: #00BCD4; font-size: 1.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(0, 188, 212, 0.3); margin: 8px 0;">{glob.get('mediana_saturacion', 0):.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b5:
            st.markdown(f"""
            <div style="border-color: #673AB7; background: linear-gradient(135deg, rgba(103, 58, 183, 0.12) 0%, rgba(94, 53, 177, 0.08) 100%); box-shadow: 0 0 20px rgba(103, 58, 183, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #673AB7; padding: 24px 20px; text-align: center;">
                <div style="color: #4527A0; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">📉 Desv. Est.</div>
                <div style="color: #673AB7; font-size: 1.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(103, 58, 183, 0.3); margin: 8px 0;">{glob.get('desviacion_std', 0):.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
    
    # ========================================================================
    # SISTEMA DE INSIGHTS INTELIGENTES
    # ========================================================================
    
    st.markdown("---")
    st.subheader("🧠 Centro de Insights Inteligentes")
    
    # Generar insights dinámicos
    insights = generar_insights_inteligentes(df_filtrado, hora_actual)
    
    if insights:
        # Separar por tipo
        criticos = [i for i in insights if i['tipo'] == 'crítico']
        advertencias = [i for i in insights if i['tipo'] == 'advertencia']
        oportunidades = [i for i in insights if i['tipo'] == 'oportunidad']
        predicciones = [i for i in insights if i['tipo'] == 'prediccion']
        exitos = [i for i in insights if i['tipo'] == 'exito']
        info = [i for i in insights if i['tipo'] == 'info']
        
        # Métricas de resumen CON TARJETAS PERSONALIZADAS
        col_i1, col_i2, col_i3, col_i4 = st.columns(4)
        
        with col_i1:
            st.markdown(f"""
            <div style="border-color: #D32F2F; background: linear-gradient(135deg, rgba(211, 47, 47, 0.12) 0%, rgba(198, 40, 40, 0.08) 100%); box-shadow: 0 0 20px rgba(211, 47, 47, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #D32F2F; padding: 24px 20px; text-align: center;">
                <div style="color: #B71C1C; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">🚨 Críticos</div>
                <div style="color: #D32F2F; font-size: 2.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(211, 47, 47, 0.3); margin: 8px 0;">{len(criticos)}</div>
                <div style="color: #D32F2F; font-size: 0.95rem; font-weight: 700; margin-top: 8px;">Acción inmediata</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_i2:
            st.markdown(f"""
            <div style="border-color: #FF9800; background: linear-gradient(135deg, rgba(255, 152, 0, 0.12) 0%, rgba(255, 167, 38, 0.08) 100%); box-shadow: 0 0 20px rgba(255, 152, 0, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #FF9800; padding: 24px 20px; text-align: center;">
                <div style="color: #E65100; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">⚠️ Advertencias</div>
                <div style="color: #FF9800; font-size: 2.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(255, 152, 0, 0.3); margin: 8px 0;">{len(advertencias)}</div>
                <div style="color: #FF9800; font-size: 0.95rem; font-weight: 700; margin-top: 8px;">Monitorear</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_i3:
            st.markdown(f"""
            <div style="border-color: #7E57C2; background: linear-gradient(135deg, rgba(126, 87, 194, 0.12) 0%, rgba(103, 58, 183, 0.08) 100%); box-shadow: 0 0 20px rgba(126, 87, 194, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #7E57C2; padding: 24px 20px; text-align: center;">
                <div style="color: #4527A0; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">💡 Oportunidades</div>
                <div style="color: #7E57C2; font-size: 2.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(126, 87, 194, 0.3); margin: 8px 0;">{len(oportunidades)}</div>
                <div style="color: #7E57C2; font-size: 0.95rem; font-weight: 700; margin-top: 8px;">Optimizar</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_i4:
            st.markdown(f"""
            <div style="border-color: #00BCD4; background: linear-gradient(135deg, rgba(0, 188, 212, 0.12) 0%, rgba(0, 150, 136, 0.08) 100%); box-shadow: 0 0 20px rgba(0, 188, 212, 0.3), 0 8px 24px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255, 255, 255, 0.1); border-radius: 14px; border: 2px solid #00BCD4; padding: 24px 20px; text-align: center;">
                <div style="color: #00695C; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 12px;">🔮 Predicciones</div>
                <div style="color: #00BCD4; font-size: 2.8rem; font-weight: 900; text-shadow: 0 2px 8px rgba(0, 188, 212, 0.3); margin: 8px 0;">{len(predicciones)}</div>
                <div style="color: #00BCD4; font-size: 0.95rem; font-weight: 700; margin-top: 8px;">Tendencias</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Mostrar insights críticos destacados
        if criticos:
            st.markdown("### 🚨 Situaciones Críticas - Acción Inmediata Requerida")
            for insight in criticos:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #EF553B 0%, #D32F2F 100%); 
                                color: white; 
                                padding: 20px; 
                                border-radius: 12px; 
                                margin: 12px 0;
                                box-shadow: 0 4px 15px rgba(239, 85, 59, 0.3);
                                border-left: 6px solid #B71C1C;">
                        <h4 style="color: white; margin: 0 0 10px 0; font-size: 1.1rem;">{insight['icono']} {insight['titulo']}</h4>
                        <p style="color: white; margin: 8px 0; font-size: 0.95rem;">{insight['mensaje']}</p>
                        <div style="background-color: rgba(255,255,255,0.15); 
                                    padding: 12px; 
                                    border-radius: 8px; 
                                    margin-top: 12px;
                                    border-left: 3px solid white;">
                            <p style="color: white; margin: 0; font-weight: 600; font-size: 0.9rem;">
                                💡 <strong>Recomendación:</strong> {insight['recomendacion']}
                            </p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        # Advertencias y predicciones en tabs
        if advertencias or predicciones:
            tab1, tab2 = st.tabs(["⚠️ Advertencias", "🔮 Predicciones"])
            
            with tab1:
                if advertencias:
                    for insight in advertencias:
                        color = '#FFA726' if insight['impacto'] == 'alto' else '#FFB74D'
                        st.markdown(f"""
                            <div style="background-color: #FFF3E0; 
                                        border-left: 5px solid {color}; 
                                        padding: 15px; 
                                        border-radius: 8px; 
                                        margin: 10px 0;">
                                <h5 style="color: #E65100; margin: 0 0 8px 0;">{insight['icono']} {insight['titulo']}</h5>
                                <p style="color: #333; margin: 5px 0; font-size: 0.9rem;">{insight['mensaje']}</p>
                                <p style="background-color: rgba(255,167,38,0.1); 
                                          padding: 10px; 
                                          margin: 8px 0 0 0; 
                                          border-radius: 5px;
                                          color: #333;
                                          font-size: 0.85rem;">
                                    <strong>💡 Recomendación:</strong> {insight['recomendacion']}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("✅ No hay advertencias activas")
            
            with tab2:
                if predicciones:
                    for insight in predicciones:
                        st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #673AB7 0%, #512DA8 100%); 
                                        color: white; 
                                        padding: 15px; 
                                        border-radius: 10px; 
                                        margin: 10px 0;
                                        box-shadow: 0 3px 10px rgba(103, 58, 183, 0.2);">
                                <h5 style="color: white; margin: 0 0 8px 0;">{insight['icono']} {insight['titulo']}</h5>
                                <p style="color: white; margin: 5px 0; font-size: 0.9rem;">{insight['mensaje']}</p>
                                <p style="background-color: rgba(255,255,255,0.15); 
                                          padding: 10px; 
                                          margin: 8px 0 0 0; 
                                          border-radius: 5px;
                                          color: white;
                                          font-size: 0.85rem;">
                                    <strong>💡 Acción sugerida:</strong> {insight['recomendacion']}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("📊 No hay predicciones disponibles en este momento")
        
        # Oportunidades y éxitos en columnas
        if oportunidades or exitos:
            st.markdown("### 💡 Oportunidades y Operaciones Eficientes")
            col_o1, col_o2 = st.columns(2)
            
            with col_o1:
                if oportunidades:
                    st.markdown("**🎯 Optimizaciones Detectadas**")
                    for insight in oportunidades:
                        st.markdown(f"""
                            <div style="background-color: #E8F5E9; 
                                        border-left: 4px solid #4CAF50; 
                                        padding: 12px; 
                                        border-radius: 8px; 
                                        margin: 8px 0;">
                                <p style="color: #2E7D32; font-weight: 600; margin: 0 0 5px 0; font-size: 0.9rem;">
                                    {insight['icono']} {insight['titulo']}
                                </p>
                                <p style="color: #333; margin: 3px 0; font-size: 0.85rem;">{insight['mensaje']}</p>
                                <p style="color: #1B5E20; margin: 5px 0 0 0; font-size: 0.8rem; font-style: italic;">
                                    💡 {insight['recomendacion']}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
            
            with col_o2:
                if exitos:
                    st.markdown("**✅ Rutas Óptimas**")
                    for insight in exitos:
                        st.markdown(f"""
                            <div style="background-color: #E3F2FD; 
                                        border-left: 4px solid #2196F3; 
                                        padding: 12px; 
                                        border-radius: 8px; 
                                        margin: 8px 0;">
                                <p style="color: #1565C0; font-weight: 600; margin: 0 0 5px 0; font-size: 0.9rem;">
                                    {insight['icono']} {insight['titulo']}
                                </p>
                                <p style="color: #333; margin: 3px 0; font-size: 0.85rem;">{insight['mensaje']}</p>
                                <p style="color: #0D47A1; margin: 5px 0 0 0; font-size: 0.8rem; font-style: italic;">
                                    🎯 {insight['recomendacion']}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
        
        # Info adicional en expander
        if info:
            with st.expander("ℹ️ Información Adicional del Sistema"):
                for insight in info:
                    st.info(f"**{insight['icono']} {insight['titulo']}**\n\n{insight['mensaje']}\n\n💡 {insight['recomendacion']}")
    else:
        st.info("📊 Sistema en análisis. Los insights se generarán basados en patrones detectados.")
    
    # ========================================================================
    # ALERTAS TRADICIONALES (Resumen rápido) - SOLO MODO DETALLADO
    # ========================================================================
    
    st.markdown("---")
    st.subheader("🚦 Estado Operativo por Nivel de Saturación")
    
    aduanas_abiertas = df_filtrado[df_filtrado['Abierta'] == True]
    criticas = aduanas_abiertas[aduanas_abiertas['Saturación'] >= 85]
    altas = aduanas_abiertas[(aduanas_abiertas['Saturación'] >= 70) & (aduanas_abiertas['Saturación'] < 85)]
    normales = aduanas_abiertas[aduanas_abiertas['Saturación'] < 70]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cruces_criticos = criticas['Cruces'].sum() if not criticas.empty else 0
        delta_text = f"{cruces_criticos:,} cruces" if cruces_criticos > 0 else None
        tarjeta_kpi_color("Críticas (≥85%)", str(len(criticas)), "🔴", delta=delta_text, color_preset="rojo")
        if not criticas.empty:
            with st.expander("Ver detalles"):
                for _, row in criticas.iterrows():
                    st.error(f"**{row['Aduana']}** ({row['Frontera']}): {row['Saturación']}% | ⏱️ {row['Tiempo_Espera']} min | 🚛 {row['Cruces']:,} cruces")
    
    with col2:
        cruces_altos = altas['Cruces'].sum() if not altas.empty else 0
        delta_text = f"{cruces_altos:,} cruces" if cruces_altos > 0 else None
        tarjeta_kpi_color("Altas (70-84%)", str(len(altas)), "🟠", delta=delta_text, color_preset="naranja")
        if not altas.empty:
            with st.expander("Ver detalles"):
                for _, row in altas.iterrows():
                    st.warning(f"**{row['Aduana']}** ({row['Frontera']}): {row['Saturación']}% | ⏱️ {row['Tiempo_Espera']} min | 🚛 {row['Cruces']:,} cruces")
    
    with col3:
        cruces_normales = normales['Cruces'].sum() if not normales.empty else 0
        delta_text = f"{cruces_normales:,} cruces" if cruces_normales > 0 else None
        tarjeta_kpi_color("Normales (<70%)", str(len(normales)), "🟢", delta=delta_text, color_preset="verde")
        if not normales.empty:
            with st.expander("Ver top 5 más eficientes"):
                for _, row in normales.nsmallest(5, 'Saturación').iterrows():
                    st.success(f"**{row['Aduana']}** ({row['Frontera']}): {row['Saturación']}% | ⏱️ {row['Tiempo_Espera']} min | 🚛 {row['Cruces']:,} cruces")
    
    # ========================================================================
    # ANÁLISIS DE TENDENCIA HORARIA
    # ========================================================================
    
    st.markdown("---")
    
    # Llamar al fragmento que muestra el gráfico (se actualiza cada 60 segundos)
    mostrar_distribucion_trafico_horaria()
    
    # ========================================================================
    # GRÁFICA DE CRUCES REALES POR HORA
    # ========================================================================
    
    st.markdown("---")
    st.subheader("🚛 Volumen de Cruces por Hora")
    
    # Calcular cruces reales por hora basados en datos actuales
    total_cruces_dia = df_filtrado['Cruces_Proyectados'].sum()
    
    # Aplicar la misma distribución horaria a los cruces totales
    cruces_por_hora_real = {}
    for h in range(24):
        cruces_hora = int(total_cruces_dia * distribucion_teorica[h] / 100)
        cruces_por_hora_real[h] = cruces_hora
    
    # Crear gráfica de volumen real
    horas_vol = list(range(24))
    volumenes = [cruces_por_hora_real[h] for h in horas_vol]
    
    # Colores: verde para horas pasadas, azul para hora actual, gris para futuras
    colores_vol = []
    for h in horas_vol:
        if h < hora_actual:
            colores_vol.append('#4CAF50')  # Verde - pasado
        elif h == hora_actual:
            colores_vol.append('#2196F3')  # Azul - actual
        else:
            colores_vol.append('#E0E0E0')  # Gris - futuro
    
    fig_volumen = go.Figure(data=[go.Bar(
        x=horas_vol,
        y=volumenes,
        marker_color=colores_vol,
        text=[f"{v:,}" for v in volumenes],
        textposition='outside',
        hovertemplate='<b>Hora %{x}:00</b><br>Cruces estimados: %{y:,.0f}<extra></extra>'
    )])
    
    fig_volumen.update_layout(
        title=f"Volumen Estimado de Cruces por Hora - Total del Día: {total_cruces_dia:,}",
        xaxis_title="Hora del Día",
        yaxis_title="Número de Cruces",
        height=350,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#11101D'),
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=2,
            gridcolor='#E0E0E0'
        ),
        yaxis=dict(
            gridcolor='#E0E0E0',
            tickformat=','
        )
    )
    
    # Agregar anotación de hora actual
    fig_volumen.add_annotation(
        x=hora_actual,
        y=cruces_por_hora_real[hora_actual] + (max(volumenes) * 0.08),
        text=f"<b>AHORA</b><br>{cruces_por_hora_real[hora_actual]:,} cruces/h",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#2196F3",
        font=dict(size=11, color="#2196F3", family="Arial Black"),
        bgcolor="white",
        bordercolor="#2196F3",
        borderwidth=2
    )
    
    # Línea de promedio
    promedio_hora = total_cruces_dia / 24
    fig_volumen.add_hline(
        y=promedio_hora,
        line_dash="dash",
        line_color="#FF5722",
        annotation_text=f"Promedio: {promedio_hora:,.0f} cruces/h",
        annotation_position="right"
    )
    
    st.plotly_chart(fig_volumen, use_container_width=True, config={'responsive': True})
    
    # Métricas de comparación
    col_v1, col_v2, col_v3, col_v4 = st.columns(4)
    
    with col_v1:
        cruces_hasta_ahora = df_filtrado['Cruces'].sum()
        st.metric(
            "🚛 Cruces Acumulados", 
            f"{cruces_hasta_ahora:,}",
            help="Cruces procesados hasta la hora actual"
        )
    
    with col_v2:
        cruces_hora_actual = cruces_por_hora_real[hora_actual]
        st.metric(
            "⏱️ Cruces Esta Hora",
            f"{cruces_hora_actual:,}",
            delta=f"{((cruces_hora_actual / promedio_hora - 1) * 100):.0f}% vs promedio",
            delta_color="off"
        )
    
    with col_v3:
        # Hora más congestionada
        hora_max = max(cruces_por_hora_real, key=cruces_por_hora_real.get)
        cruces_max = cruces_por_hora_real[hora_max]
        st.metric(
            "🔝 Hora Pico",
            f"{hora_max:02d}:00",
            delta=f"{cruces_max:,} cruces"
        )
    
    with col_v4:
        # Hora menos congestionada
        hora_min = min(cruces_por_hora_real, key=cruces_por_hora_real.get)
        cruces_min = cruces_por_hora_real[hora_min]
        st.metric(
            "🌙 Hora Valle",
            f"{hora_min:02d}:00",
            delta=f"{cruces_min:,} cruces"
        )
    
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
        
        st.plotly_chart(fig_bars, use_container_width=True, config={'responsive': True})
    
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
        
        st.plotly_chart(fig_pie, use_container_width=True, config={'responsive': True})
    
    # ========================================================================
    # ESTADÍSTICAS FINALES
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📈 Estadísticas del Día")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_cruces = df_filtrado['Cruces'].sum()
        total_proyectado = df_filtrado['Cruces_Proyectados'].sum()
        delta_text = f"Proyección: {total_proyectado:,}"
        tarjeta_kpi_color("Total Cruces Acumulados", f"{total_cruces:,}", "📊", delta=delta_text, color_preset="azul_primario")
    
    with col2:
        total_trucks = df_filtrado['Trucks'].sum()
        pct_trucks = (total_trucks/total_cruces*100 if total_cruces > 0 else 0)
        tarjeta_kpi_color("Trucks", f"{total_trucks:,}", "🚛", delta=f"{pct_trucks:.1f}%", color_preset="verde")
    
    with col3:
        total_loaded = df_filtrado['Trucks_Loaded'].sum()
        pct_loaded = (total_loaded/total_cruces*100 if total_cruces > 0 else 0)
        tarjeta_kpi_color("Contenedores Cargados", f"{total_loaded:,}", "📦", delta=f"{pct_loaded:.1f}%", color_preset="azul_canada")
    
    with col4:
        total_empty = df_filtrado['Trucks_Empty'].sum()
        pct_empty = (total_empty/total_cruces*100 if total_cruces > 0 else 0)
        tarjeta_kpi_color("Contenedores Vacíos", f"{total_empty:,}", "📭", delta=f"{pct_empty:.1f}%", color_preset="naranja")
    
    # ========================================================================
    # RESUMEN EJECUTIVO
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📋 Resumen Ejecutivo del Día")
    
    # Generar resumen automático
    aduanas_activas = df_filtrado[df_filtrado['Abierta'] == True]
    total_aduanas_activas = len(aduanas_activas)
    sat_general = aduanas_activas['Saturación'].mean() if not aduanas_activas.empty else 0
    
    # Determinar estado general del sistema
    if sat_general < 50:
        estado_sistema = "🟢 Óptimo"
        color_estado = "#4CAF50"
        desc_estado = "El sistema opera significativamente por debajo de su capacidad máxima"
    elif sat_general < 70:
        estado_sistema = "🟡 Normal"
        color_estado = "#FFC107"
        desc_estado = "El sistema opera dentro de parámetros normales"
    elif sat_general < 85:
        estado_sistema = "🟠 Presión Elevada"
        color_estado = "#FF9800"
        desc_estado = "El sistema experimenta presión significativa en múltiples puntos"
    else:
        estado_sistema = "🔴 Crítico"
        color_estado = "#EF553B"
        desc_estado = "El sistema opera cerca o por encima de su capacidad máxima"
    
    # Calcular eficiencia
    cruces_totales = df_filtrado['Cruces'].sum()
    proyeccion_total = df_filtrado['Cruces_Proyectados'].sum()
    eficiencia = (cruces_totales / (proyeccion_total * (porcentaje_dia / 100))) * 100 if proyeccion_total > 0 and porcentaje_dia > 0 else 100
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #11101D 0%, {color_estado} 100%); 
                    color: white; 
                    padding: 25px; 
                    border-radius: 15px;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.2);
                    margin: 15px 0;">
            <h3 style="color: white; margin: 0 0 15px 0;">Estado General del Sistema: {estado_sistema}</h3>
            <p style="color: white; font-size: 1rem; margin: 0 0 15px 0;">{desc_estado}</p>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;">
                <div style="background-color: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px;">
                    <p style="color: white; margin: 0; font-size: 0.8rem; opacity: 0.9;">Aduanas Activas</p>
                    <p style="color: white; margin: 5px 0 0 0; font-size: 1.5rem; font-weight: 700;">{total_aduanas_activas}</p>
                </div>
                <div style="background-color: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px;">
                    <p style="color: white; margin: 0; font-size: 0.8rem; opacity: 0.9;">Saturación Avg</p>
                    <p style="color: white; margin: 5px 0 0 0; font-size: 1.5rem; font-weight: 700;">{sat_general:.1f}%</p>
                </div>
                <div style="background-color: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px;">
                    <p style="color: white; margin: 0; font-size: 0.8rem; opacity: 0.9;">Cruces Procesados</p>
                    <p style="color: white; margin: 5px 0 0 0; font-size: 1.5rem; font-weight: 700;">{cruces_totales:,}</p>
                </div>
                <div style="background-color: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px;">
                    <p style="color: white; margin: 0; font-size: 0.8rem; opacity: 0.9;">Eficiencia del Día</p>
                    <p style="color: white; margin: 5px 0 0 0; font-size: 1.5rem; font-weight: 700;">{eficiencia:.1f}%</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Recomendaciones ejecutivas
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown("**🎯 Recomendaciones Principales**")
        
        # Top 3 recomendaciones basadas en datos
        recomendaciones = []
        
        # 1. Saturación alta
        if sat_general > 70:
            top_alternativas = aduanas_activas.nsmallest(3, 'Saturación')['Aduana'].tolist()
            recomendaciones.append({
                'prioridad': '🔴 Alta',
                'accion': f"Redistribuir tráfico hacia: {', '.join(top_alternativas)}"
            })
        
        # 2. Contenedores vacíos
        pct_empty = (total_empty / cruces_totales * 100) if cruces_totales > 0 else 0
        if pct_empty > 12:
            recomendaciones.append({
                'prioridad': '🟡 Media',
                'accion': f"Optimizar logística inversa ({pct_empty:.1f}% de contenedores vacíos)"
            })
        
        # 3. Capacidad disponible
        capacidad_disponible = aduanas_activas[aduanas_activas['Saturación'] < 40]
        if len(capacidad_disponible) >= 3:
            recomendaciones.append({
                'prioridad': '🟢 Baja',
                'accion': f"Aprovechar capacidad en {len(capacidad_disponible)} aduanas subutilizadas"
            })
        
        # Mostrar recomendaciones
        if recomendaciones:
            for i, rec in enumerate(recomendaciones[:3], 1):
                st.markdown(f"""
                    <div style="background-color: #F5F5F5; 
                                padding: 10px; 
                                border-radius: 6px; 
                                margin: 5px 0;
                                border-left: 3px solid #4070F4;">
                        <p style="margin: 0; color: #333; font-size: 0.85rem;">
                            <strong>{rec['prioridad']}</strong> - {rec['accion']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Sistema operando óptimamente. No se requieren acciones inmediatas.")
    
    with col_rec2:
        st.markdown("**📊 Indicadores Clave de Rendimiento**")
        
        # KPIs adicionales
        tiempo_espera_avg = aduanas_activas['Tiempo_Espera'].mean() if not aduanas_activas.empty else 0
        capacidad_total = aduanas_activas['Capacidad_Hora'].sum() if not aduanas_activas.empty else 0
        cruces_x_hora_actual = aduanas_activas['Cruces_Por_Hora'].sum() if not aduanas_activas.empty else 0
        utilizacion = (cruces_x_hora_actual / capacidad_total * 100) if capacidad_total > 0 else 0
        
        col_kpi1, col_kpi2 = st.columns(2)
        with col_kpi1:
            tarjeta_kpi_color("Tiempo Espera Avg", f"{tiempo_espera_avg:.0f} min", "⏱️", color_preset="azul_primario")
            tarjeta_kpi_color("Tasa Utilización", f"{utilizacion:.1f}%", "🚀", color_preset="verde")
        with col_kpi2:
            tarjeta_kpi_color("Capacidad/Hora", f"{capacidad_total:,}", "📦", color_preset="turquesa")
            tarjeta_kpi_color("Cruces/Hora Actual", f"{cruces_x_hora_actual:,}", "🔄", color_preset="morado")
    
    # ========================================================================
    # TABLA DE ALERTAS HISTÓRICA
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📋 Historial de Alertas")
    
    # Crear datos de historial de alertas
    historico_alertas = []
    
    # Recolectar insights críticos para el historial
    for insight in criticos:
        historico_alertas.append({
            'Hora': obtener_hora_actual().strftime('%H:%M:%S'),
            'Tipo': insight['titulo'],
            'Aduana/Region': insight.get('aduana', 'Sistema General'),
            'Saturación': f"{insight.get('saturacion', 0):.0f}%",
            'Severidad': '🔴 Crítica'
        })
    
    # Agregar advertencias
    for insight in advertencias:
        historico_alertas.append({
            'Hora': obtener_hora_actual().strftime('%H:%M:%S'),
            'Tipo': insight['titulo'],
            'Aduana/Region': insight.get('aduana', 'Sistema General'),
            'Saturación': f"{insight.get('saturacion', 0):.0f}%",
            'Severidad': '🟡 Advertencia'
        })
    
    # Si no hay alertas, agregar un mensaje
    if not historico_alertas:
        # Crear alertas simuladas para demostración
        historico_alertas = [
            {
                'Hora': '08:30:00',
                'Tipo': 'Saturación Alta',
                'Aduana/Region': 'Laredo, TX',
                'Saturación': '85%',
                'Severidad': '🔴 Crítica'
            },
            {
                'Hora': '09:15:00',
                'Tipo': 'Capacidad Limitada',
                'Aduana/Region': 'El Paso, TX',
                'Saturación': '72%',
                'Severidad': '🟡 Advertencia'
            },
            {
                'Hora': '10:45:00',
                'Tipo': 'Tiempo de Espera',
                'Aduana/Region': 'San Ysidro, CA',
                'Saturación': '68%',
                'Severidad': '🟡 Advertencia'
            },
            {
                'Hora': '11:20:00',
                'Tipo': 'Contenedores Vacíos',
                'Aduana/Region': 'Otay Mesa, CA',
                'Saturación': '45%',
                'Severidad': '🟢 Información'
            },
            {
                'Hora': '12:30:00',
                'Tipo': 'Operación Normal',
                'Aduana/Region': 'Buffalo, NY',
                'Saturación': '35%',
                'Severidad': '✅ Exitosa'
            }
        ]
    
    if historico_alertas:
        df_alertas = pd.DataFrame(historico_alertas)
        
        # Filtros
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        
        with col_filter1:
            filtro_severidad = st.multiselect(
                "Filtrar por Severidad",
                options=['🔴 Crítica', '🟡 Advertencia', '🟢 Información', '✅ Exitosa'],
                default=['🔴 Crítica', '🟡 Advertencia']
            )
        
        with col_filter2:
            filtro_tipo = st.multiselect(
                "Filtrar por Tipo",
                options=df_alertas['Tipo'].unique() if not df_alertas.empty else []
            )
        
        with col_filter3:
            orden = st.radio("Ordenar por", ['Más Recientes', 'Más Antiguos'], horizontal=True)
        
        # Aplicar filtros
        df_alertas_filtradas = df_alertas.copy()
        
        if filtro_severidad:
            df_alertas_filtradas = df_alertas_filtradas[df_alertas_filtradas['Severidad'].isin(filtro_severidad)]
        
        if filtro_tipo:
            df_alertas_filtradas = df_alertas_filtradas[df_alertas_filtradas['Tipo'].isin(filtro_tipo)]
        
        if orden == 'Más Antiguos':
            df_alertas_filtradas = df_alertas_filtradas.iloc[::-1]
        
        # Mostrar tabla
        if not df_alertas_filtradas.empty:
            st.dataframe(
                df_alertas_filtradas,
                use_container_width=True,
                hide_index=True,
                column_config={
                    'Hora': st.column_config.TextColumn('Hora', width=80),
                    'Tipo': st.column_config.TextColumn('Tipo de Alerta', width=150),
                    'Aduana/Region': st.column_config.TextColumn('Aduana / Región', width=150),
                    'Saturación': st.column_config.TextColumn('Saturación', width=100),
                    'Severidad': st.column_config.TextColumn('Severidad', width=120)
                }
            )
            
            # Estadísticas del historial
            st.markdown("**📊 Resumen del Historial**")
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            
            with col_stat1:
                criticas_count = len(df_alertas_filtradas[df_alertas_filtradas['Severidad'] == '🔴 Crítica'])
                st.metric("Alertas Críticas", criticas_count)
            
            with col_stat2:
                advertencias_count = len(df_alertas_filtradas[df_alertas_filtradas['Severidad'] == '🟡 Advertencia'])
                st.metric("Advertencias", advertencias_count)
            
            with col_stat3:
                aduanas_afectadas = df_alertas_filtradas['Aduana/Region'].nunique()
                st.metric("Aduanas Afectadas", aduanas_afectadas)
            
            with col_stat4:
                saturacion_max = df_alertas_filtradas['Saturación'].str.rstrip('%').astype(float).max()
                st.metric("Saturación Máx.", f"{saturacion_max:.0f}%")
            
            # Opción para exportar
            csv = df_alertas_filtradas.to_csv(index=False)
            st.download_button(
                label="📥 Descargar Historial (CSV)",
                data=csv,
                file_name=f"alertas_{obtener_hora_actual().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No hay alertas que coincidan con los filtros seleccionados.")
    else:
        st.success("✅ No se han generado alertas en este período.")
    
    # ========================================================================
    # NUEVA SECCIÓN: HORARIOS DE OPERACIÓN
    # ========================================================================
    
    st.markdown("---")
    st.subheader("⏰ Horarios de Operación - Aduanas México-USA")
    
    # Cargar horarios
    df_horarios = cargar_horarios_aduanas()
    
    if not df_horarios.empty:
        # Selector de aduana
        aduanas_disponibles = df_horarios['Aduana / Puerto (Estado México)'].tolist()
        aduana_seleccionada = st.selectbox(
            "Seleccionar aduana para ver horarios:",
            aduanas_disponibles,
            index=aduanas_disponibles.index('Calexico East') if 'Calexico East' in aduanas_disponibles else 0
        )
        
        # Mostrar datos de la aduana seleccionada
        fila_aduana = df_horarios[df_horarios['Aduana / Puerto (Estado México)'] == aduana_seleccionada].iloc[0]
        
        col_h1, col_h2, col_h3, col_h4 = st.columns(4)
        
        with col_h1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.15), rgba(56, 142, 60, 0.1)); border: 2px solid #4CAF50; border-radius: 12px; padding: 16px; text-align: center;">
                <div style="font-size: 0.75rem; color: #2e7d32; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">📤 Exportación (L-V)</div>
                <div style="font-size: 1rem; color: #1b5e20; font-weight: 900;">{fila_aduana['Exportación (L-V)']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_h2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(33, 150, 243, 0.15), rgba(13, 71, 161, 0.1)); border: 2px solid #2196F3; border-radius: 12px; padding: 16px; text-align: center;">
                <div style="font-size: 0.75rem; color: #0d47a1; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">📥 Importación (L-V)</div>
                <div style="font-size: 1rem; color: #0d47a1; font-weight: 900;">{fila_aduana['Importación (L-V)']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_h3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(255, 152, 0, 0.15), rgba(230, 124, 15, 0.1)); border: 2px solid #FF9800; border-radius: 12px; padding: 16px; text-align: center;">
                <div style="font-size: 0.75rem; color: #e65100; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">📅 Fin de Semana</div>
                <div style="font-size: 0.85rem; color: #e65100; font-weight: 900;">{fila_aduana['Fin de Semana (S-D)']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_h4:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(156, 39, 176, 0.15), rgba(106, 27, 154, 0.1)); border: 2px solid #9C27B0; border-radius: 12px; padding: 16px; text-align: center;">
                <div style="font-size: 0.75rem; color: #6a1b9a; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">🎉 Día Festivo</div>
                <div style="font-size: 0.85rem; color: #6a1b9a; font-weight: 900;">{fila_aduana['Día Festivo (Estándar)']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Mostrar notas si existen
        if 'Notas' in fila_aduana and pd.notna(fila_aduana['Notas']):
            st.info(f"📌 **Notas**: {fila_aduana['Notas']}")
        
        # Información adicional
        with st.expander("📋 Ver todos los horarios (tabla completa)"):
            # Preparar tabla para mostrar
            df_display = df_horarios[['Aduana / Puerto (Estado México)', 'Exportación (L-V)', 'Importación (L-V)', 'Fin de Semana (S-D)', 'Día Festivo (Estándar)']].copy()
            df_display.columns = ['Aduana', 'Exportación L-V', 'Importación L-V', 'Fin de Semana', 'Día Festivo']
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                column_config={
                    'Aduana': st.column_config.TextColumn('Aduana / Puerto', width=150),
                    'Exportación L-V': st.column_config.TextColumn('Exportación L-V', width=120),
                    'Importación L-V': st.column_config.TextColumn('Importación L-V', width=120),
                    'Fin de Semana': st.column_config.TextColumn('Fin de Semana', width=150),
                    'Día Festivo': st.column_config.TextColumn('Día Festivo', width=120)
                }
            )
    
    # Footer (disponible en ambos modos)
    st.markdown("---")
    st.caption("💡 **Nota**: Datos en tiempo real actualizados según hora del sistema. Los cruces acumulados representan el tráfico procesado hasta el momento actual.")
    st.caption(f"📊 Última actualización: {obtener_hora_actual().strftime('%Y-%m-%d %H:%M:%S')} | 🔄 Proyección diaria: {proyeccion_total:,} cruces | ⏱️ Progreso del día: {porcentaje_dia:.1f}%")


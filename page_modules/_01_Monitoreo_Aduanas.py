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
import time


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
# FRAGMENTO: GRÁFICO DE DISTRIBUCIÓN HORARIA (Se actualiza independientemente)
# ============================================================================

@st.fragment(run_every=60)  # Se actualiza cada 60 segundos
def mostrar_distribucion_trafico_horaria():
    """Fragmento que muestra la distribución de tráfico por hora - se actualiza automáticamente"""
    
    st.subheader("📊 Distribución de Tráfico por Hora")
    
    # Obtener hora actual en tiempo real
    hora_actual_grafico = datetime.now().hour
    minuto_actual_grafico = datetime.now().minute
    
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
            <div style='background-color: {color}20; 
                        border-left: 5px solid {color}; 
                        padding: 15px; 
                        border-radius: 8px;
                        margin: 10px 0;'>
                <h4 style='color: {color}; margin: 0 0 8px 0;'>{fase}</h4>
                <p style='color: #333; margin: 0; font-size: 0.9rem;'>{desc}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_t2:
        # Progreso del día
        progreso = (hora_actual_grafico * 60 + minuto_actual_grafico) / (24 * 60) * 100
        st.markdown(f"""
            <div style='background-color: #F5F5F5; 
                        padding: 15px; 
                        border-radius: 8px;
                        margin: 10px 0;'>
                <h4 style='color: #11101D; margin: 0 0 8px 0;'>📊 Progreso del Día</h4>
                <p style='color: #333; margin: 0; font-size: 0.9rem;'>Completado: {progreso:.1f}%</p>
            </div>
        """, unsafe_allow_html=True)
        st.progress(progreso / 100)
    
    with col_t3:
        # Tiempo restante de hora pico
        if hora_actual_grafico < 20:
            horas_restantes = 20 - hora_actual_grafico
            st.markdown(f"""
                <div style='background-color: #E3F2FD; 
                            border-left: 5px solid #2196F3; 
                            padding: 15px; 
                            border-radius: 8px;
                            margin: 10px 0;'>
                    <h4 style='color: #1976D2; margin: 0 0 8px 0;'>⏱️ Hora Pico</h4>
                    <p style='color: #333; margin: 0; font-size: 0.9rem;'>{horas_restantes}h restantes</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='background-color: #E8F5E9; 
                            border-left: 5px solid #4CAF50; 
                            padding: 15px; 
                            border-radius: 8px;
                            margin: 10px 0;'>
                    <h4 style='color: #388E3C; margin: 0 0 8px 0;'>✅ Hora Pico</h4>
                    <p style='color: #333; margin: 0; font-size: 0.9rem;'>Finalizada</p>
                </div>
            """, unsafe_allow_html=True)


# ============================================================================
# FUNCIÓN PRINCIPAL DE LA PÁGINA
# ============================================================================

def page_monitoreo_aduanas():
    """Página de Monitoreo de Aduanas V2 - Limpia y funcional"""
    
    # Header
    st.title("🚛 Monitoreo de Aduanas en Tiempo Real")
    
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
    fecha_hoy = datetime.now()
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
    # ESTADÍSTICAS COMPARATIVAS
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📈 Análisis Comparativo por Frontera")
    
    stats = obtener_estadisticas_comparativas(df_filtrado)
    
    if 'México' in stats and 'Canadá' in stats:
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%); 
                            color: white; 
                            padding: 20px; 
                            border-radius: 12px;
                            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);'>
                    <h3 style='color: white; margin: 0 0 15px 0; font-size: 1.3rem;'>🇲🇽 Frontera México</h3>
                </div>
            """, unsafe_allow_html=True)
            
            mx = stats.get('México', {})
            col_mx1, col_mx2 = st.columns(2)
            with col_mx1:
                st.metric("Aduanas Activas", mx.get('total_aduanas', 0))
                st.metric("Saturación Avg", f"{mx.get('saturacion_promedio', 0):.1f}%")
            with col_mx2:
                st.metric("Espera Avg", f"{mx.get('tiempo_espera_promedio', 0):.0f} min")
                st.metric("Cruces Totales", f"{mx.get('cruces_totales', 0):,}")
            
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
                <div style='background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); 
                            color: white; 
                            padding: 20px; 
                            border-radius: 12px;
                            box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);'>
                    <h3 style='color: white; margin: 0 0 15px 0; font-size: 1.3rem;'>🇨🇦 Frontera Canadá</h3>
                </div>
            """, unsafe_allow_html=True)
            
            ca = stats.get('Canadá', {})
            col_ca1, col_ca2 = st.columns(2)
            with col_ca1:
                st.metric("Aduanas Activas", ca.get('total_aduanas', 0))
                st.metric("Saturación Avg", f"{ca.get('saturacion_promedio', 0):.1f}%")
            with col_ca2:
                st.metric("Espera Avg", f"{ca.get('tiempo_espera_promedio', 0):.0f} min")
                st.metric("Cruces Totales", f"{ca.get('cruces_totales', 0):,}")
            
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
        col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
        
        with col_b1:
            st.metric("🏆 Mejor Aduana", glob.get('mejor_aduana', 'N/A'), 
                      delta=f"{glob.get('saturacion_min', 0):.0f}%", delta_color="inverse")
        with col_b2:
            st.metric("⚠️ Peor Aduana", glob.get('peor_aduana', 'N/A'),
                      delta=f"{glob.get('saturacion_max', 0):.0f}%", delta_color="off")
        with col_b3:
            st.metric("📊 Mediana", f"{glob.get('mediana_saturacion', 0):.0f}%")
        with col_b4:
            st.metric("📉 Desv. Estándar", f"{glob.get('desviacion_std', 0):.1f}%")
        with col_b5:
            rango = glob.get('saturacion_max', 0) - glob.get('saturacion_min', 0)
            st.metric("📏 Rango", f"{rango:.0f}%")
    
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
        
        # Métricas de resumen
        col_i1, col_i2, col_i3, col_i4 = st.columns(4)
        with col_i1:
            st.metric("🚨 Críticos", len(criticos), help="Situaciones que requieren acción inmediata")
        with col_i2:
            st.metric("⚠️ Advertencias", len(advertencias), help="Situaciones que requieren monitoreo")
        with col_i3:
            st.metric("💡 Oportunidades", len(oportunidades), help="Áreas de optimización detectadas")
        with col_i4:
            st.metric("🔮 Predicciones", len(predicciones), help="Tendencias anticipadas")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Mostrar insights críticos destacados
        if criticos:
            st.markdown("### 🚨 Situaciones Críticas - Acción Inmediata Requerida")
            for insight in criticos:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #EF553B 0%, #D32F2F 100%); 
                                color: white; 
                                padding: 20px; 
                                border-radius: 12px; 
                                margin: 12px 0;
                                box-shadow: 0 4px 15px rgba(239, 85, 59, 0.3);
                                border-left: 6px solid #B71C1C;'>
                        <h4 style='color: white; margin: 0 0 10px 0; font-size: 1.1rem;'>{insight['icono']} {insight['titulo']}</h4>
                        <p style='color: white; margin: 8px 0; font-size: 0.95rem;'>{insight['mensaje']}</p>
                        <div style='background-color: rgba(255,255,255,0.15); 
                                    padding: 12px; 
                                    border-radius: 8px; 
                                    margin-top: 12px;
                                    border-left: 3px solid white;'>
                            <p style='color: white; margin: 0; font-weight: 600; font-size: 0.9rem;'>
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
                            <div style='background-color: #FFF3E0; 
                                        border-left: 5px solid {color}; 
                                        padding: 15px; 
                                        border-radius: 8px; 
                                        margin: 10px 0;'>
                                <h5 style='color: #E65100; margin: 0 0 8px 0;'>{insight['icono']} {insight['titulo']}</h5>
                                <p style='color: #333; margin: 5px 0; font-size: 0.9rem;'>{insight['mensaje']}</p>
                                <p style='background-color: rgba(255,167,38,0.1); 
                                          padding: 10px; 
                                          margin: 8px 0 0 0; 
                                          border-radius: 5px;
                                          color: #333;
                                          font-size: 0.85rem;'>
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
                            <div style='background: linear-gradient(135deg, #673AB7 0%, #512DA8 100%); 
                                        color: white; 
                                        padding: 15px; 
                                        border-radius: 10px; 
                                        margin: 10px 0;
                                        box-shadow: 0 3px 10px rgba(103, 58, 183, 0.2);'>
                                <h5 style='color: white; margin: 0 0 8px 0;'>{insight['icono']} {insight['titulo']}</h5>
                                <p style='color: white; margin: 5px 0; font-size: 0.9rem;'>{insight['mensaje']}</p>
                                <p style='background-color: rgba(255,255,255,0.15); 
                                          padding: 10px; 
                                          margin: 8px 0 0 0; 
                                          border-radius: 5px;
                                          color: white;
                                          font-size: 0.85rem;'>
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
                            <div style='background-color: #E8F5E9; 
                                        border-left: 4px solid #4CAF50; 
                                        padding: 12px; 
                                        border-radius: 8px; 
                                        margin: 8px 0;'>
                                <p style='color: #2E7D32; font-weight: 600; margin: 0 0 5px 0; font-size: 0.9rem;'>
                                    {insight['icono']} {insight['titulo']}
                                </p>
                                <p style='color: #333; margin: 3px 0; font-size: 0.85rem;'>{insight['mensaje']}</p>
                                <p style='color: #1B5E20; margin: 5px 0 0 0; font-size: 0.8rem; font-style: italic;'>
                                    💡 {insight['recomendacion']}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
            
            with col_o2:
                if exitos:
                    st.markdown("**✅ Rutas Óptimas**")
                    for insight in exitos:
                        st.markdown(f"""
                            <div style='background-color: #E3F2FD; 
                                        border-left: 4px solid #2196F3; 
                                        padding: 12px; 
                                        border-radius: 8px; 
                                        margin: 8px 0;'>
                                <p style='color: #1565C0; font-weight: 600; margin: 0 0 5px 0; font-size: 0.9rem;'>
                                    {insight['icono']} {insight['titulo']}
                                </p>
                                <p style='color: #333; margin: 3px 0; font-size: 0.85rem;'>{insight['mensaje']}</p>
                                <p style='color: #0D47A1; margin: 5px 0 0 0; font-size: 0.8rem; font-style: italic;'>
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
    # ALERTAS TRADICIONALES (Resumen rápido)
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
        st.metric("🔴 Críticas (≥85%)", len(criticas), 
                  delta=f"{cruces_criticos:,} cruces" if cruces_criticos > 0 else None,
                  delta_color="inverse")
        if not criticas.empty:
            with st.expander("Ver detalles"):
                for _, row in criticas.iterrows():
                    st.error(f"**{row['Aduana']}** ({row['Frontera']}): {row['Saturación']}% | ⏱️ {row['Tiempo_Espera']} min | 🚛 {row['Cruces']:,} cruces")
    
    with col2:
        cruces_altos = altas['Cruces'].sum() if not altas.empty else 0
        st.metric("🟠 Altas (70-84%)", len(altas),
                  delta=f"{cruces_altos:,} cruces" if cruces_altos > 0 else None,
                  delta_color="off")
        if not altas.empty:
            with st.expander("Ver detalles"):
                for _, row in altas.iterrows():
                    st.warning(f"**{row['Aduana']}** ({row['Frontera']}): {row['Saturación']}% | ⏱️ {row['Tiempo_Espera']} min | 🚛 {row['Cruces']:,} cruces")
    
    with col3:
        cruces_normales = normales['Cruces'].sum() if not normales.empty else 0
        st.metric("🟢 Normales (<70%)", len(normales),
                  delta=f"{cruces_normales:,} cruces" if cruces_normales > 0 else None,
                  delta_color="normal")
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
        <div style='background: linear-gradient(135deg, #11101D 0%, {color_estado} 100%); 
                    color: white; 
                    padding: 25px; 
                    border-radius: 15px;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.2);
                    margin: 15px 0;'>
            <h3 style='color: white; margin: 0 0 15px 0;'>Estado General del Sistema: {estado_sistema}</h3>
            <p style='color: white; font-size: 1rem; margin: 0 0 15px 0;'>{desc_estado}</p>
            <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;'>
                <div style='background-color: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px;'>
                    <p style='color: white; margin: 0; font-size: 0.8rem; opacity: 0.9;'>Aduanas Activas</p>
                    <p style='color: white; margin: 5px 0 0 0; font-size: 1.5rem; font-weight: 700;'>{total_aduanas_activas}</p>
                </div>
                <div style='background-color: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px;'>
                    <p style='color: white; margin: 0; font-size: 0.8rem; opacity: 0.9;'>Saturación Avg</p>
                    <p style='color: white; margin: 5px 0 0 0; font-size: 1.5rem; font-weight: 700;'>{sat_general:.1f}%</p>
                </div>
                <div style='background-color: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px;'>
                    <p style='color: white; margin: 0; font-size: 0.8rem; opacity: 0.9;'>Cruces Procesados</p>
                    <p style='color: white; margin: 5px 0 0 0; font-size: 1.5rem; font-weight: 700;'>{cruces_totales:,}</p>
                </div>
                <div style='background-color: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px;'>
                    <p style='color: white; margin: 0; font-size: 0.8rem; opacity: 0.9;'>Eficiencia del Día</p>
                    <p style='color: white; margin: 5px 0 0 0; font-size: 1.5rem; font-weight: 700;'>{eficiencia:.1f}%</p>
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
                    <div style='background-color: #F5F5F5; 
                                padding: 10px; 
                                border-radius: 6px; 
                                margin: 5px 0;
                                border-left: 3px solid #4070F4;'>
                        <p style='margin: 0; color: #333; font-size: 0.85rem;'>
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
            st.metric("⏱️ Tiempo Espera Avg", f"{tiempo_espera_avg:.0f} min")
            st.metric("🚀 Tasa Utilización", f"{utilizacion:.1f}%")
        with col_kpi2:
            st.metric("📦 Capacidad/Hora", f"{capacidad_total:,}")
            st.metric("🔄 Cruces/Hora Actual", f"{cruces_x_hora_actual:,}")
    
    # Footer
    st.markdown("---")
    st.caption("💡 **Nota**: Datos en tiempo real actualizados según hora del sistema. Los cruces acumulados representan el tráfico procesado hasta el momento actual.")
    st.caption(f"📊 Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 🔄 Proyección diaria: {proyeccion_total:,} cruces | ⏱️ Progreso del día: {porcentaje_dia:.1f}%")


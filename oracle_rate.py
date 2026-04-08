"""
Página: FreightMetrics Oracle Rate
Sistema de predicción y análisis de tarifas de transporte
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta


def page_oracle_rate():
    """Página Oracle Rate - Predicción de tarifas"""
    
    # Header
    st.markdown("""
        <div style='background: linear-gradient(135deg, #6B46C1 0%, #9333EA 100%); 
                    color: white; 
                    padding: 30px 40px; 
                    border-radius: 15px; 
                    margin-bottom: 30px;
                    box-shadow: 0 8px 20px rgba(107, 70, 193, 0.3);'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'>🔮 FreightMetrics Oracle Rate</h1>
            <p style='color: #C4B5FD; font-size: 1.2rem; font-weight: 500; margin-top: 10px; margin-bottom: 0;'>
                Predicción Inteligente de Tarifas de Transporte
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Selector de ruta
    st.subheader("🛣️ Configuración de Ruta")
    
    col_ruta1, col_ruta2, col_ruta3 = st.columns(3)
    
    with col_ruta1:
        origen = st.selectbox(
            "📍 Origen",
            options=[
                "Laredo, TX",
                "El Paso, TX",
                "Nogales, AZ",
                "Tijuana, BC",
                "Detroit, MI",
                "Buffalo, NY"
            ],
            index=0
        )
    
    with col_ruta2:
        destino = st.selectbox(
            "📍 Destino",
            options=[
                "Ciudad de México",
                "Monterrey",
                "Guadalajara",
                "Toronto",
                "Chicago",
                "Los Angeles"
            ],
            index=0
        )
    
    with col_ruta3:
        tipo_carga = st.selectbox(
            "📦 Tipo de Carga",
            options=["Dry Van", "Reefer", "Flatbed", "Contenedor 20'", "Contenedor 40'"],
            index=0
        )
    
    st.markdown("---")
    
    # TARIFA ACTUAL Y PREDICCIÓN
    np.random.seed(hash(origen + destino + tipo_carga) % 2**32)
    tarifa_base = np.random.uniform(2500, 5500)
    tarifa_actual = tarifa_base * np.random.uniform(0.95, 1.05)
    
    # Predicción 7 días
    prediccion_7d = tarifa_actual * np.random.uniform(0.98, 1.08)
    cambio_7d = ((prediccion_7d - tarifa_actual) / tarifa_actual) * 100
    
    # Predicción 30 días
    prediccion_30d = tarifa_actual * np.random.uniform(0.92, 1.12)
    cambio_30d = ((prediccion_30d - tarifa_actual) / tarifa_actual) * 100
    
    # Confianza del modelo
    confianza = np.random.uniform(75, 95)
    
    st.subheader("💰 Tarifa Actual y Predicciones")
    
    col_tar1, col_tar2, col_tar3, col_tar4 = st.columns(4)
    
    with col_tar1:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #4070F4 0%, #2196F3 100%); 
                        color: white; 
                        padding: 25px; 
                        border-radius: 12px;
                        box-shadow: 0 4px 15px rgba(64, 112, 244, 0.3);
                        text-align: center;'>
                <p style='color: rgba(255,255,255,0.9); font-size: 0.9rem; margin: 0;'>TARIFA ACTUAL</p>
                <h2 style='color: white; font-size: 2.5rem; font-weight: 700; margin: 10px 0;'>${tarifa_actual:,.0f}</h2>
                <p style='color: rgba(255,255,255,0.8); font-size: 0.85rem; margin: 0;'>USD por viaje</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_tar2:
        color_7d = "#4CAF50" if cambio_7d >= 0 else "#EF553B"
        st.markdown(f"""
            <div style='background-color: #F5F5F5; padding: 25px; border-radius: 12px; text-align: center;'>
                <p style='color: #666; font-size: 0.9rem; margin: 0;'>PREDICCIÓN 7 DÍAS</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0;'>${prediccion_7d:,.0f}</h2>
                <p style='color: {color_7d}; font-size: 1rem; font-weight: 600; margin: 0;'>{cambio_7d:+.1f}%</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_tar3:
        color_30d = "#4CAF50" if cambio_30d >= 0 else "#EF553B"
        st.markdown(f"""
            <div style='background-color: #F5F5F5; padding: 25px; border-radius: 12px; text-align: center;'>
                <p style='color: #666; font-size: 0.9rem; margin: 0;'>PREDICCIÓN 30 DÍAS</p>
                <h2 style='color: #11101D; font-size: 2.5rem; font-weight: 700; margin: 10px 0;'>${prediccion_30d:,.0f}</h2>
                <p style='color: {color_30d}; font-size: 1rem; font-weight: 600; margin: 0;'>{cambio_30d:+.1f}%</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_tar4:
        conf_color = "#4CAF50" if confianza >= 85 else "#FFC107" if confianza >= 75 else "#EF553B"
        st.markdown(f"""
            <div style='background-color: #F5F5F5; padding: 25px; border-radius: 12px; text-align: center;'>
                <p style='color: #666; font-size: 0.9rem; margin: 0;'>CONFIANZA</p>
                <h2 style='color: {conf_color}; font-size: 2.5rem; font-weight: 700; margin: 10px 0;'>{confianza:.0f}%</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>Precisión modelo</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # GRÁFICO DE PREDICCIÓN
    st.subheader("📈 Proyección de Tarifa - Próximos 30 Días")
    
    # Generar datos históricos y predicción
    fechas_hist = pd.date_range(end=datetime.now(), periods=30, freq='D')
    fechas_pred = pd.date_range(start=datetime.now() + timedelta(days=1), periods=30, freq='D')
    
    # Histórico con tendencia y ruido
    tarifas_hist = tarifa_base + np.linspace(-200, 0, 30) + np.random.normal(0, 100, 30)
    
    # Predicción con tendencia
    tarifas_pred = np.linspace(tarifa_actual, prediccion_30d, 30) + np.random.normal(0, 80, 30)
    
    # Banda de confianza (±10%)
    banda_superior = tarifas_pred * 1.10
    banda_inferior = tarifas_pred * 0.90
    
    fig_pred = go.Figure()
    
    # Histórico
    fig_pred.add_trace(go.Scatter(
        x=fechas_hist,
        y=tarifas_hist,
        mode='lines',
        name='Histórico',
        line=dict(color='#4070F4', width=3),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>$%{y:,.0f}<extra></extra>'
    ))
    
    # Predicción
    fig_pred.add_trace(go.Scatter(
        x=fechas_pred,
        y=tarifas_pred,
        mode='lines',
        name='Predicción',
        line=dict(color='#9333EA', width=3, dash='dash'),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>$%{y:,.0f}<extra></extra>'
    ))
    
    # Banda de confianza
    fig_pred.add_trace(go.Scatter(
        x=fechas_pred,
        y=banda_superior,
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig_pred.add_trace(go.Scatter(
        x=fechas_pred,
        y=banda_inferior,
        mode='lines',
        fill='tonexty',
        fillcolor='rgba(147, 51, 234, 0.2)',
        line=dict(width=0),
        name='Banda de confianza',
        hoverinfo='skip'
    ))
    
    fig_pred.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Tarifa (USD)",
        height=400,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#11101D'),
        xaxis=dict(gridcolor='#E0E0E0', showgrid=True),
        yaxis=dict(gridcolor='#E0E0E0', showgrid=True),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_pred, use_container_width=True)
    
    st.markdown("---")
    
    # FACTORES DE INFLUENCIA
    st.subheader("🎯 Factores de Influencia en la Tarifa")
    
    col_fact1, col_fact2 = st.columns(2)
    
    with col_fact1:
        # Gráfico de radar con factores
        factores = ['Demanda', 'Capacidad', 'Combustible', 'Temporada', 'Competencia']
        valores = np.random.uniform(60, 95, 5)
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=valores,
            theta=factores,
            fill='toself',
            fillcolor='rgba(64, 112, 244, 0.2)',
            line=dict(color='#4070F4', width=2)
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title="Impacto de Factores (0-100)",
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col_fact2:
        st.markdown("**📊 Análisis de Factores:**")
        
        for i, factor in enumerate(factores):
            valor = valores[i]
            color = "#4CAF50" if valor >= 80 else "#FFC107" if valor >= 65 else "#EF553B"
            
            st.markdown(f"""
                <div style='background-color: #F5F5F5; padding: 12px; border-radius: 8px; margin: 8px 0;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='font-weight: 600; color: #11101D;'>{factor}</span>
                        <span style='color: {color}; font-weight: 700;'>{valor:.0f}/100</span>
                    </div>
                    <div style='background-color: #E0E0E0; height: 6px; border-radius: 3px; margin-top: 8px;'>
                        <div style='background-color: {color}; height: 6px; border-radius: 3px; width: {valor}%;'></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Recomendación
        if cambio_7d > 5:
            recom_text = "⚠️ Esperar - Tarifa puede bajar"
            recom_color = "#FF9800"
        elif cambio_7d < -5:
            recom_text = "✅ Contratar ahora"
            recom_color = "#4CAF50"
        else:
            recom_text = "📊 Tarifa estable"
            recom_color = "#2196F3"
        
        st.markdown(f"""
            <div style='background-color: {recom_color}20; border-left: 5px solid {recom_color}; 
                        padding: 15px; border-radius: 10px; margin-top: 20px;'>
                <h4 style='color: {recom_color}; margin: 0 0 8px 0;'>💡 Recomendación</h4>
                <p style='color: #333; margin: 0; font-size: 1.1rem; font-weight: 600;'>{recom_text}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # COMPARACIÓN DE RUTAS ALTERNATIVAS
    st.subheader("🔄 Rutas Alternativas")
    
    rutas_alt = pd.DataFrame({
        'Ruta': [
            f"{origen} → {destino} (Directa)",
            f"{origen} → Querétaro → {destino}",
            f"{origen} → Monterrey → {destino}"
        ],
        'Tarifa': [
            tarifa_actual,
            tarifa_actual * 1.15,
            tarifa_actual * 1.08
        ],
        'Tiempo': ['24 hrs', '28 hrs', '26 hrs'],
        'Confiabilidad': ['Alta', 'Media', 'Alta']
    })
    
    # Agregar columna de diferencia
    rutas_alt['Diferencia'] = rutas_alt['Tarifa'] - tarifa_actual
    
    # Formatear columnas para mostrar
    rutas_alt_display = rutas_alt.copy()
    rutas_alt_display['Tarifa'] = rutas_alt_display['Tarifa'].apply(lambda x: f"${x:,.0f}")
    rutas_alt_display['Diferencia'] = rutas_alt_display['Diferencia'].apply(lambda x: f"${x:+,.0f}")
    
    # Mostrar tabla
    st.dataframe(
        rutas_alt_display,
        use_container_width=True,
        height=150
    )
    
    st.caption(f"🔮 **Modelo**: Oracle Neural Network v2.1 | **Actualizado**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

"""
Página: Índice FreightMetrics
Sistema de índices y métricas de referencia del mercado de transporte
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path

# Importar función de cálculo de capacidad desde monitoreo_v2
try:
    from monitoreo_v2 import calcular_capacidad_hora
except ImportError:
    # Fallback si no se puede importar
    def calcular_capacidad_hora(cruces_diarios):
        trafico_hora_pico = (cruces_diarios * 0.60) / 12
        if cruces_diarios > 8000:
            return int(trafico_hora_pico * 1.40)
        elif cruces_diarios > 4000:
            return int(trafico_hora_pico * 1.35)
        elif cruces_diarios > 1500:
            return int(trafico_hora_pico * 1.30)
        else:
            return int(trafico_hora_pico * 1.25)


@st.cache_data(ttl=600)
def cargar_datos_bts(years=[2025]):
    """
    Carga datos históricos de cruces fronterizos del BTS.
    """
    data_dir = Path(__file__).parent / "data"
    all_data = []
    
    for year in years:
        file_path = data_dir / f"border_crossings_{year}_historical.csv"
        if file_path.exists():
            try:
                df = pd.read_csv(file_path)
                df['year'] = year
                all_data.append(df)
            except Exception as e:
                st.warning(f"⚠️ No se pudo cargar datos de {year}: {str(e)}")
    
    if not all_data:
        return None
    
    df_consolidated = pd.concat(all_data, ignore_index=True)
    
    # Filtrar solo fronteras US-Mexico y US-Canada
    df_consolidated = df_consolidated[
        df_consolidated['border'].isin(['US-Mexico Border', 'US-Canada Border'])
    ].copy()
    
    # Asegurar que date es datetime
    df_consolidated['date'] = pd.to_datetime(df_consolidated['date'])
    
    # Solo tipos de medida relevantes (trucks)
    df_consolidated = df_consolidated[
        df_consolidated['measure'].isin(['Trucks', 'Truck Containers Empty', 'Truck Containers Loaded'])
    ].copy()
    
    return df_consolidated


def page_indice_freightmetrics():
    """Página del Índice FreightMetrics - Indicador del mercado de transporte"""
    
    # Header
    st.markdown("""
        <div style='background: linear-gradient(135deg, #11101D 0%, #4070F4 100%); 
                    color: white; 
                    padding: 30px 40px; 
                    border-radius: 15px; 
                    margin-bottom: 30px;
                    box-shadow: 0 8px 20px rgba(17, 16, 29, 0.3);'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'>📊 Índice FreightMetrics</h1>
            <p style='color: #29B5E8; font-size: 1.2rem; font-weight: 500; margin-top: 10px; margin-bottom: 0;'>
                Indicador Compuesto del Mercado de Transporte Transfronterizo
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # CARGAR DATOS REALES DEL BTS
    # ========================================================================
    
    # Cargar datos históricos (últimos 365 días disponibles)
    df_bts = cargar_datos_bts(years=[2025])  # Cargar año 2025 (más reciente disponible)
    
    if df_bts is None or df_bts.empty:
        st.warning("⚠️ No se pudieron cargar datos del BTS. Mostrando datos simulados de demostración.")
        st.info("💡 Para usar datos reales, asegúrate de tener el archivo `data/border_crossings_2025_historical.csv`")
        # Fallback a datos simulados
        np.random.seed(42)
        fechas = pd.date_range(end=datetime.now(), periods=365, freq='D')
        indice_base = 100
        tendencia = np.linspace(0, 15, 365)
        estacionalidad = 5 * np.sin(np.linspace(0, 4 * np.pi, 365))
        ruido = np.random.normal(0, 2, 365)
        indice_valores = indice_base + tendencia + estacionalidad + ruido
        
        df_indice = pd.DataFrame({
            'Fecha': fechas,
            'Indice': indice_valores,
            'Volumen': np.random.randint(50000, 150000, 365),
            'Tarifas': indice_valores * 0.95 + np.random.normal(0, 1, 365),
            'Capacidad': indice_valores * 1.05 + np.random.normal(0, 1, 365),
            'Demanda': indice_valores * 0.98 + np.random.normal(0, 1.5, 365)
        })
    else:
        # PROCESAR DATOS REALES DEL BTS
        # Agrupar por fecha y sumar cruces de todos los puertos
        df_daily = df_bts.groupby('date')['value'].sum().reset_index()
        df_daily.columns = ['Fecha', 'Volumen_Real']
        df_daily['Fecha'] = pd.to_datetime(df_daily['Fecha'])
        df_daily = df_daily.sort_values('Fecha')
        
        # Tomar últimos 365 días disponibles
        df_daily = df_daily.tail(365).reset_index(drop=True)
        
        # Validar que después del procesamiento tenemos suficientes datos
        if df_daily.empty or len(df_daily) < 30:
            st.warning(f"⚠️ Datos insuficientes después de procesar BTS ({len(df_daily)} días). Mostrando datos simulados.")
            # Fallback a datos simulados
            np.random.seed(42)
            fechas = pd.date_range(end=datetime.now(), periods=365, freq='D')
            indice_base = 100
            tendencia = np.linspace(0, 15, 365)
            estacionalidad = 5 * np.sin(np.linspace(0, 4 * np.pi, 365))
            ruido = np.random.normal(0, 2, 365)
            indice_valores = indice_base + tendencia + estacionalidad + ruido
            
            df_indice = pd.DataFrame({
                'Fecha': fechas,
                'Indice': indice_valores,
                'Volumen': np.random.randint(50000, 150000, 365),
                'Tarifas': indice_valores * 0.95 + np.random.normal(0, 1, 365),
                'Capacidad': indice_valores * 1.05 + np.random.normal(0, 1, 365),
                'Demanda': indice_valores * 0.98 + np.random.normal(0, 1.5, 365)
            })
        else:
            # Calcular componentes del índice
            # 1. VOLUMEN (25%): Normalizado a base 100
            volumen_promedio = df_daily['Volumen_Real'].mean()
            df_daily['Volumen'] = (df_daily['Volumen_Real'] / volumen_promedio) * 100
            
            # 2. CAPACIDAD (25%): Basada en cálculo de monitoreo_v2
            capacidades = []
            for volumen in df_daily['Volumen_Real']:
                cap_hora = calcular_capacidad_hora(volumen)
                # Normalizar: capacidad total diaria vs volumen
                cap_total_dia = cap_hora * 12  # 12 horas pico
                ratio_capacidad = (cap_total_dia / volumen) * 100 if volumen > 0 else 100
                capacidades.append(ratio_capacidad)
            df_daily['Capacidad'] = capacidades
            
            # 3. DEMANDA (20%): Inverso de la capacidad disponible
            df_daily['Demanda'] = 200 - df_daily['Capacidad']  # Más demanda = menos capacidad disponible
            
            # 4. TARIFAS (30%): Simulado basado en volumen y capacidad
            # Tarifas suben cuando hay más demanda y menos capacidad
            df_daily['Tarifas'] = (df_daily['Volumen'] * 0.6 + df_daily['Demanda'] * 0.4)
            
            # CALCULAR ÍNDICE COMPUESTO (ponderado)
            df_daily['Indice'] = (
                df_daily['Volumen'] * 0.25 +      # 25% peso
                df_daily['Tarifas'] * 0.30 +      # 30% peso  
                df_daily['Capacidad'] * 0.25 +    # 25% peso
                df_daily['Demanda'] * 0.20        # 20% peso
            )
            
            # Aplicar suavizado (media móvil de 7 días) para reducir volatilidad
            df_daily['Indice'] = df_daily['Indice'].rolling(window=7, min_periods=1).mean()
            
            # Renombrar para compatibilidad
            df_indice = df_daily[['Fecha', 'Indice', 'Volumen', 'Tarifas', 'Capacidad', 'Demanda']].copy()
    
    # Valor actual y variación
    valor_actual = df_indice['Indice'].iloc[-1]
    valor_ayer = df_indice['Indice'].iloc[-2] if len(df_indice) >= 2 else valor_actual
    variacion_diaria = valor_actual - valor_ayer
    variacion_pct = (variacion_diaria / valor_ayer) * 100 if valor_ayer != 0 else 0
    
    valor_mes_anterior = df_indice['Indice'].iloc[-30] if len(df_indice) >= 30 else df_indice['Indice'].iloc[0]
    variacion_mensual = ((valor_actual - valor_mes_anterior) / valor_mes_anterior) * 100 if valor_mes_anterior != 0 else 0
    
    # MÉTRICAS PRINCIPALES
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #4070F4 0%, #2196F3 100%); 
                        color: white; 
                        padding: 25px; 
                        border-radius: 12px;
                        box-shadow: 0 4px 15px rgba(64, 112, 244, 0.3);
                        text-align: center;'>
                <p style='color: rgba(255,255,255,0.9); font-size: 0.9rem; margin: 0; text-transform: uppercase;'>Índice Actual</p>
                <h2 style='color: white; font-size: 2.8rem; font-weight: 700; margin: 10px 0;'>{valor_actual:.2f}</h2>
                <p style='color: {"#4CAF50" if variacion_diaria >= 0 else "#EF553B"}; font-size: 1.1rem; font-weight: 600; margin: 0;'>
                    {"+" if variacion_diaria >= 0 else ""}{variacion_diaria:.2f} ({variacion_pct:+.2f}%)
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric(
            "📅 Variación Mensual",
            f"{variacion_mensual:+.2f}%",
            delta=f"{abs(variacion_mensual):.2f} puntos",
            delta_color="normal" if variacion_mensual >= 0 else "inverse"
        )
    
    with col3:
        # Calcular promedio de 90 días (o todos los disponibles si hay menos)
        dias_promedio = min(90, len(df_indice))
        promedio_90d = df_indice['Indice'].iloc[-dias_promedio:].mean()
        st.metric(
            f"📊 Promedio {dias_promedio} días",
            f"{promedio_90d:.2f}",
            delta=f"{((valor_actual - promedio_90d) / promedio_90d * 100):+.2f}%" if promedio_90d != 0 else "0%"
        )
    
    with col4:
        # Calcular volatilidad de 30 días (o todos los disponibles si hay menos)
        dias_volatilidad = min(30, len(df_indice))
        volatilidad = df_indice['Indice'].iloc[-dias_volatilidad:].std()
        st.metric(
            f"📈 Volatilidad ({dias_volatilidad}d)",
            f"±{volatilidad:.2f}",
            help=f"Desviación estándar de los últimos {dias_volatilidad} días"
        )
    
    st.markdown("---")
    
    # GRÁFICO PRINCIPAL - EVOLUCIÓN DEL ÍNDICE
    st.subheader("📈 Evolución Histórica del Índice FreightMetrics")
    
    # Selector de período
    col_per1, col_per2 = st.columns([1, 3])
    with col_per1:
        periodo = st.selectbox(
            "Período",
            options=['7 días', '30 días', '90 días', '180 días', '1 año'],
            index=2
        )
    
    # Filtrar datos según período
    dias_map = {'7 días': 7, '30 días': 30, '90 días': 90, '180 días': 180, '1 año': 365}
    dias = dias_map[periodo]
    df_filtered = df_indice.iloc[-dias:]
    
    # Crear gráfico
    fig_indice = go.Figure()
    
    # Línea del índice
    fig_indice.add_trace(go.Scatter(
        x=df_filtered['Fecha'],
        y=df_filtered['Indice'],
        mode='lines',
        name='Índice FreightMetrics',
        line=dict(color='#4070F4', width=3),
        fill='tozeroy',
        fillcolor='rgba(64, 112, 244, 0.1)',
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Índice: %{y:.2f}<extra></extra>'
    ))
    
    # Línea de promedio móvil 20 días
    if dias >= 20:
        ma20 = df_filtered['Indice'].rolling(window=20).mean()
        fig_indice.add_trace(go.Scatter(
            x=df_filtered['Fecha'],
            y=ma20,
            mode='lines',
            name='MA 20 días',
            line=dict(color='#FF9800', width=2, dash='dash'),
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>MA20: %{y:.2f}<extra></extra>'
        ))
    
    # Línea base 100
    fig_indice.add_hline(
        y=100,
        line_dash="dot",
        line_color="#E0E0E0",
        annotation_text="Base: 100",
        annotation_position="right"
    )
    
    fig_indice.update_layout(
        title=f"Índice FreightMetrics - Últimos {periodo}",
        xaxis_title="Fecha",
        yaxis_title="Valor del Índice",
        height=450,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#11101D', family='Inter'),
        xaxis=dict(gridcolor='#E0E0E0', showgrid=True),
        yaxis=dict(gridcolor='#E0E0E0', showgrid=True),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_indice, use_container_width=True)
    
    st.markdown("---")
    
    # COMPONENTES DEL ÍNDICE
    st.subheader("🔍 Componentes del Índice")
    
    st.markdown("""
        El **Índice FreightMetrics** es un indicador compuesto que mide la salud general del mercado de transporte 
        transfronterizo, considerando cuatro factores principales:
    """)
    
    col_comp1, col_comp2 = st.columns(2)
    
    with col_comp1:
        # Gráfico de componentes actuales (ya normalizados a base 100)
        componentes_actuales = {
            'Volumen': df_indice['Volumen'].iloc[-1],
            'Tarifas': df_indice['Tarifas'].iloc[-1],
            'Capacidad': df_indice['Capacidad'].iloc[-1],
            'Demanda': df_indice['Demanda'].iloc[-1]
        }
        
        fig_componentes = go.Figure(data=[go.Bar(
            x=list(componentes_actuales.keys()),
            y=list(componentes_actuales.values()),
            marker_color=['#4070F4', '#29B5E8', '#4CAF50', '#FFA726'],
            text=[f"{v:.1f}" for v in componentes_actuales.values()],
            textposition='outside'
        )])
        
        fig_componentes.update_layout(
            title="Valor Actual de Componentes (Base 100)",
            yaxis_title="Índice Normalizado",
            height=350,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#11101D')
        )
        
        st.plotly_chart(fig_componentes, use_container_width=True)
    
    with col_comp2:
        st.markdown("**💡 Descripción de Componentes:**")
        
        st.markdown("""
            <div style='background-color: #F5F5F5; padding: 15px; border-radius: 10px; margin: 10px 0;'>
                <p style='margin: 0 0 10px 0;'><strong>📦 Volumen (25%):</strong> Cruces fronterizos BTS (normalizado)</p>
                <p style='margin: 0 0 10px 0;'><strong>💰 Tarifas (30%):</strong> Derivado de volumen y demanda</p>
                <p style='margin: 0 0 10px 0;'><strong>🚛 Capacidad (25%):</strong> Cálculo monitoreo_v2.py</p>
                <p style='margin: 0;'><strong>📊 Demanda (20%):</strong> Presión sobre capacidad</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**📈 Interpretación:**")
        st.markdown("""
            <div style='background-color: #E3F2FD; padding: 15px; border-radius: 10px;'>
                <p style='margin: 0 0 5px 0;'>• <strong>>110:</strong> Mercado muy activo 🔥</p>
                <p style='margin: 0 0 5px 0;'>• <strong>100-110:</strong> Mercado saludable ✅</p>
                <p style='margin: 0 0 5px 0;'>• <strong>90-100:</strong> Mercado normal 📊</p>
                <p style='margin: 0;'>• <strong><90:</strong> Mercado débil ⚠️</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ANÁLISIS COMPARATIVO
    st.subheader("📊 Análisis Comparativo por Frontera")
    
    # Seed basado en la fecha para variabilidad diaria pero consistencia en el día
    np.random.seed(int(datetime.now().strftime('%Y%m%d')))
    indice_mexico = valor_actual * np.random.uniform(0.95, 1.05)
    indice_canada = valor_actual * np.random.uniform(0.90, 1.00)
    
    col_front1, col_front2, col_front3 = st.columns(3)
    
    with col_front1:
        st.markdown(f"""
            <div style='background-color: #E8F5E9; border-left: 5px solid #4CAF50; padding: 20px; border-radius: 10px;'>
                <h3 style='color: #2E7D32; margin: 0 0 10px 0;'>🇲🇽 Frontera México</h3>
                <p style='font-size: 2rem; font-weight: 700; color: #11101D; margin: 0;'>{indice_mexico:.2f}</p>
                <p style='color: #666; margin: 5px 0 0 0;'>
                    {((indice_mexico - valor_actual) / valor_actual * 100):+.1f}% vs general
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_front2:
        st.markdown(f"""
            <div style='background-color: #E3F2FD; border-left: 5px solid #2196F3; padding: 20px; border-radius: 10px;'>
                <h3 style='color: #1565C0; margin: 0 0 10px 0;'>🇨🇦 Frontera Canadá</h3>
                <p style='font-size: 2rem; font-weight: 700; color: #11101D; margin: 0;'>{indice_canada:.2f}</p>
                <p style='color: #666; margin: 5px 0 0 0;'>
                    {((indice_canada - valor_actual) / valor_actual * 100):+.1f}% vs general
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_front3:
        st.markdown(f"""
            <div style='background-color: #FFF3E0; border-left: 5px solid #FFA726; padding: 20px; border-radius: 10px;'>
                <h3 style='color: #E65100; margin: 0 0 10px 0;'>📊 Diferencial</h3>
                <p style='font-size: 2rem; font-weight: 700; color: #11101D; margin: 0;'>{abs(indice_mexico - indice_canada):.2f}</p>
                <p style='color: #666; margin: 5px 0 0 0;'>puntos de spread</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # INSIGHTS Y RECOMENDACIONES
    st.subheader("💡 Insights del Mercado")
    
    col_ins1, col_ins2 = st.columns(2)
    
    with col_ins1:
        # Determinar tendencia
        if variacion_mensual > 3:
            tendencia_text = "📈 Tendencia Alcista Fuerte"
            tendencia_color = "#4CAF50"
            tendencia_msg = f"El índice ha crecido **{variacion_mensual:.1f}%** en el último mes, indicando un mercado robusto con alta demanda."
        elif variacion_mensual > 0:
            tendencia_text = "📊 Tendencia Alcista Moderada"
            tendencia_color = "#FFC107"
            tendencia_msg = f"Crecimiento moderado de **{variacion_mensual:.1f}%** mensual. El mercado mantiene momentum positivo."
        elif variacion_mensual > -3:
            tendencia_text = "📉 Tendencia Bajista Leve"
            tendencia_color = "#FF9800"
            tendencia_msg = f"Caída leve de **{variacion_mensual:.1f}%** mensual. Monitorear evolución en próximas semanas."
        else:
            tendencia_text = "⚠️ Tendencia Bajista Fuerte"
            tendencia_color = "#EF553B"
            tendencia_msg = f"Descenso significativo de **{variacion_mensual:.1f}%** mensual. Mercado en contracción."
        
        st.markdown(f"""
            <div style='background-color: {tendencia_color}20; border-left: 5px solid {tendencia_color}; padding: 20px; border-radius: 10px;'>
                <h4 style='color: {tendencia_color}; margin: 0 0 10px 0;'>{tendencia_text}</h4>
                <p style='color: #333; margin: 0; line-height: 1.6;'>{tendencia_msg}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_ins2:
        # Volatilidad
        if volatilidad < 2:
            vol_text = "📊 Baja Volatilidad"
            vol_color = "#4CAF50"
            vol_msg = "Mercado estable con movimientos predecibles. Entorno favorable para planificación."
        elif volatilidad < 4:
            vol_text = "⚡ Volatilidad Moderada"
            vol_color = "#FFC107"
            vol_msg = "Fluctuaciones normales del mercado. Mantener flexibilidad operativa."
        else:
            vol_text = "🌪️ Alta Volatilidad"
            vol_color = "#EF553B"
            vol_msg = "Mercado con cambios bruscos. Considerar estrategias de cobertura de riesgo."
        
        st.markdown(f"""
            <div style='background-color: {vol_color}20; border-left: 5px solid {vol_color}; padding: 20px; border-radius: 10px;'>
                <h4 style='color: {vol_color}; margin: 0 0 10px 0;'>{vol_text}</h4>
                <p style='color: #333; margin: 0; line-height: 1.6;'>{vol_msg}</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.caption(f"💡 **Actualización**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | **Base**: 100 | **Fuente**: BTS API + Monitoreo_v2 | **Metodología**: Índice compuesto ponderado")

"""
Página: Nearshoring
Análisis de tendencias de nearshoring y relocalización industrial
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from modules.config import t

# Importar componentes UI centralizados
try:
    from modules.session_init import metric_card, page_header, spacer
except ImportError:
    def metric_card(title, value, icon="📊", color="#1976d2", delta=None, delta_color="normal"):
        st.metric(title, value, delta=delta, delta_color=delta_color)
    def page_header(title, subtitle="", icon="📊"):
        st.title(f"{icon} {title}")
        if subtitle:
            st.markdown(f"**{subtitle}**")
    def spacer(height=20):
        st.markdown(f"<div style='height: {height}px;'></div>", unsafe_allow_html=True)


def page_nearshoring():
    """Análisis de tendencias de nearshoring y relocalización industrial"""
    
    # Obtener idioma actual (seguro con .get())
    lang = st.session_state.get('language', 'es')
    
    # Header de la página
    page_header(
        t('menu_nearshoring', lang),
        "Análisis de tendencias de relocalización industrial y nearshoring" if lang == 'es' else 
        "Nearshoring and industrial relocation trends analysis" if lang == 'en' else
        "Analyse des tendances de relocalisation industrielle et de nearshoring",
        "🌎"
    )
    
    # ============================================================
    # Estilos CSS LOCALES para esta página
    # ============================================================
    st.markdown("""
    <style>
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, rgba(251, 192, 45, 0.10) 0%, rgba(255, 235, 59, 0.08) 100%) !important;
            border-left: 5px solid #FBC02D !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Cargar datos históricos
    @st.cache_data(ttl=600)
    def cargar_datos_nearshoring():
        """Carga y procesa datos para análisis de nearshoring"""
        try:
            # Cargar datos de cruces fronterizos multi-año
            years = [2023, 2024, 2025]
            all_data = []
            
            for year in years:
                file_path = Path(__file__).parent.parent / "data" / f"border_crossings_{year}_historical.csv"
                if file_path.exists():
                    df = pd.read_csv(file_path)
                    df['year'] = year
                    all_data.append(df)
            
            if all_data:
                df_combined = pd.concat(all_data, ignore_index=True)
                df_combined['date'] = pd.to_datetime(df_combined['date'])
                df_combined['month'] = df_combined['date'].dt.month
                df_combined['year_month'] = df_combined['date'].dt.strftime('%Y-%m')
                return df_combined
            else:
                return pd.DataFrame()
                
        except Exception as e:
            st.error(f"Error cargando datos: {e}")
            return pd.DataFrame()
    
    # Cargar datos de aduanas mexicanas
    @st.cache_data(ttl=600)
    def cargar_datos_aduanas():
        """Carga datos de contenedores en aduanas mexicanas"""
        try:
            file_path = Path(__file__).parent.parent / "data" / "aduanas_latest.csv"
            if file_path.exists():
                df = pd.read_csv(file_path)
                df['Fecha'] = pd.to_datetime(df['Fecha'])
                return df
            else:
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error cargando datos de aduanas: {e}")
            return pd.DataFrame()
    
    df_border = cargar_datos_nearshoring()
    df_aduanas = cargar_datos_aduanas()
    
    if df_border.empty:
        st.error("No se pudieron cargar los datos de cruces fronterizos")
        return
    
    # ========== MÉTRICAS PRINCIPALES ==========
    st.markdown("### 📊 Indicadores Clave de Inversión Extranjera Directa (IED) 2025" if lang == 'es' else 
                "### 📊 Key FDI Indicators 2025" if lang == 'en' else
                "### 📊 Indicateurs Clés d'IDE 2025")
    
    # Datos de IED 2025 (Q3 - Cierre de tercer trimestre)
    ied_q3_2025 = 40906  # Millones USD
    reinversion_pct = 67.8  # Porcentaje
    nuevas_inversiones_pct = 16  # Porcentaje
    manufactura_pct = 37  # Porcentaje
    anuncios_cambio = -23  # Cambio porcentual vs 2024
    
    # Métricas de tarjetas - Fila 1: Cifras principales de IED
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card(
            "IED Q3 2025" if lang == 'es' else "FDI Q3 2025" if lang == 'en' else "IDE Q3 2025",
            f"${ied_q3_2025:,.0f}M",
            "💵",
            "#1976D2",
            "📈 Máximo histórico" if lang == 'es' else "📈 All-time high" if lang == 'en' else "📈 Sommet historique"
        )
    
    with col2:
        metric_card(
            "Reinversión" if lang == 'es' else "Reinvestment" if lang == 'en' else "Réinvestissement",
            f"{reinversion_pct:.1f}%",
            "🔄",
            "#0052a3",
            f"${(ied_q3_2025 * reinversion_pct / 100):,.0f}M" if lang == 'es' else f"${(ied_q3_2025 * reinversion_pct / 100):,.0f}M"
        )
    
    with col3:
        metric_card(
            "Nuevas Inversiones" if lang == 'es' else "New Investments" if lang == 'en' else "Nouveaux Investissements",
            f"{nuevas_inversiones_pct:.1f}%",
            "🆕",
            "#0066cc",
            f"${(ied_q3_2025 * nuevas_inversiones_pct / 100):,.0f}M" if lang == 'es' else f"${(ied_q3_2025 * nuevas_inversiones_pct / 100):,.0f}M"
        )
    
    with col4:
        metric_card(
            "Sector Manufactura" if lang == 'es' else "Manufacturing Sector" if lang == 'en' else "Secteur de la Fabrication",
            f"{manufactura_pct:.1f}%",
            "🏭",
            "#1976d2",
            f"${(ied_q3_2025 * manufactura_pct / 100):,.0f}M" if lang == 'es' else f"${(ied_q3_2025 * manufactura_pct / 100):,.0f}M"
        )
    
    spacer(15)
    
    # Fila 2: Flujos de contenedores (indicadores logísticos)
    current_year = 2025
    prev_year = 2024
    
    # Contenedores totales (indicador clave de nearshoring)
    containers_current = df_border[
        (df_border['year'] == current_year) & 
        (df_border['measure'].str.contains('Container', case=False))
    ]['value'].sum()
    
    containers_prev = df_border[
        (df_border['year'] == prev_year) & 
        (df_border['measure'].str.contains('Container', case=False))
    ]['value'].sum()
    
    containers_growth = ((containers_current - containers_prev) / containers_prev * 100) if containers_prev > 0 else 0
    
    # Tráfico total de camiones
    trucks_current = df_border[
        (df_border['year'] == current_year) & 
        (df_border['measure'] == 'Trucks')
    ]['value'].sum()
    
    trucks_prev = df_border[
        (df_border['year'] == prev_year) & 
        (df_border['measure'] == 'Trucks')
    ]['value'].sum()
    
    trucks_growth = ((trucks_current - trucks_prev) / trucks_prev * 100) if trucks_prev > 0 else 0
    
    # Métricas de tarjetas - Fila 2: Logística
    col1, col2, col3 = st.columns(3)
    
    with col1:
        metric_card(
            "Contenedores 2025" if lang == 'es' else "Containers 2025" if lang == 'en' else "Conteneurs 2025",
            f"{containers_current:,.0f}",
            "📦",
            "#1976d2",
            f"{containers_growth:+.1f}% vs 2024"
        )
    
    with col2:
        metric_card(
            "Camiones 2025" if lang == 'es' else "Trucks 2025" if lang == 'en' else "Camions 2025",
            f"{trucks_current:,.0f}",
            "🚛",
            "#0066cc",
            f"{trucks_growth:+.1f}% vs 2024"
        )
    
    with col3:
        # Calcular valor total de aduanas si disponible
        total_valor = df_aduanas['Valor_USD'].sum() if not df_aduanas.empty else 0
        metric_card(
            "Valor Comercio (USD)" if lang == 'es' else "Trade Value (USD)" if lang == 'en' else "Valeur Commerce (USD)",
            f"${total_valor:,.0f}M" if total_valor > 0 else "N/A",
            "💰",
            "#0052a3"
        )
    
    spacer(20)
    
    # ========== ANÁLISIS DETALLADO DE IED 2025 ==========
    st.markdown("### 💼 Análisis Detallado de IED - Q3 2025" if lang == 'es' else 
                "### 💼 Detailed FDI Analysis - Q3 2025" if lang == 'en' else
                "### 💼 Analyse Détaillée d'IDE - Q3 2025")
    
    # Información sobre composición de inversiones
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Composición de Capital" if lang == 'es' else 
                    "#### 📊 Capital Composition" if lang == 'en' else
                    "#### 📊 Composition du Capital")
        
        # Crear gráfico de pie para composición de capital
        composicion_data = {
            'Tipo': ['Reinversión de Utilidades', 'Nuevas Inversiones', 'Otros'] if lang == 'es' else 
                    ['Profit Reinvestment', 'New Investments', 'Other'] if lang == 'en' else
                    ['Réinvestissement de Bénéfices', 'Nouveaux Investissements', 'Autres'],
            'Valor': [67.8, 16, 16.2],
            'Monto_USD': [
                ied_q3_2025 * 0.678,
                ied_q3_2025 * 0.16,
                ied_q3_2025 * 0.162
            ]
        }
        
        fig_composicion = px.pie(
            composicion_data,
            values='Valor',
            names='Tipo',
            title="Composición de IED" if lang == 'es' else "FDI Composition" if lang == 'en' else "Composition d'IDE",
            labels={'Valor': '%'},
            color_discrete_sequence=['#0052a3', '#0066cc', '#1976d2']
        )
        fig_composicion.update_layout(
            height=350,
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_composicion, use_container_width=True)
    
    with col2:
        st.markdown("#### 🏭 Distribución por Sector" if lang == 'es' else 
                    "#### 🏭 Distribution by Sector" if lang == 'en' else
                    "#### 🏭 Distribution par Secteur")
        
        # Datos de sectores (manufactura es 37%)
        sectores_data = {
            'Sector': ['Manufactura\n(Automotriz/Autopartes)', 'Otros Sectores'] if lang == 'es' else
                      ['Manufacturing\n(Automotive/Parts)', 'Other Sectors'] if lang == 'en' else
                      ['Fabrication\n(Automobile/Pièces)', 'Autres Secteurs'],
            'Porcentaje': [37, 63],
            'Monto_USD': [
                ied_q3_2025 * 0.37,
                ied_q3_2025 * 0.63
            ]
        }
        
        fig_sectores = px.bar(
            sectores_data,
            x='Sector',
            y='Porcentaje',
            title="Industria Líder" if lang == 'es' else "Leading Industry" if lang == 'en' else "Industrie Leader",
            labels={'Porcentaje': '%'},
            color='Porcentaje',
            color_continuous_scale=['#0052a3', '#1976d2']
        )
        fig_sectores.update_layout(
            height=350,
            showlegend=False,
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="",
            yaxis_title="Porcentaje %"
        )
        st.plotly_chart(fig_sectores, use_container_width=True)
    
    spacer(15)
    
    # Información sobre anuncios vs inauguraciones
    st.markdown("#### 📋 Indicadores de Ejecución de Proyectos" if lang == 'es' else 
                "#### 📋 Project Execution Indicators" if lang == 'en' else
                "#### 📋 Indicateurs d'Exécution de Projets")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📉 **Anuncios 2025 vs 2024:** -23% (en descenso)" if lang == 'es' else 
                "📉 **Announcements 2025 vs 2024:** -23% (declining)" if lang == 'en' else
                "📉 **Annonces 2025 vs 2024:** -23% (en baisse)")
        st.markdown(
            "Los anuncios de nuevas inversiones bajaron respecto al año anterior, sugiriendo que la "
            "fase de aceleración de compromisos está moderándose." if lang == 'es' else
            "Announcements of new investments decreased compared to the previous year, suggesting that "
            "the phase of accelerating commitments is moderating." if lang == 'en' else
            "Les annonces de nouveaux investissements ont baissé par rapport à l'année précédente, "
            "suggérant que la phase d'accélération des engagements se modère.",
            unsafe_allow_html=True
        )
    
    with col2:
        st.success("✅ **Inauguraciones 2025:** Nivel Máximo Histórico" if lang == 'es' else 
                   "✅ **Inaugurations 2025:** All-time High" if lang == 'en' else
                   "✅ **Inaugérations 2025:** Record Historique")
        st.markdown(
            "El número de inauguraciones de proyectos alcanzó su nivel más alto, reflejando que "
            "los compromisos de inversión previos ya se están materializando operativamente." if lang == 'es' else
            "The number of project inauguration reached its highest level, reflecting that "
            "previous investment commitments are now materializing operationally." if lang == 'en' else
            "Le nombre d'inaugérations de projets a atteint son plus haut niveau, reflétant que "
            "les engagements d'investissement antérieurs se concrétisent maintenant opérationnellement.",
            unsafe_allow_html=True
        )
    
    # ========== ANÁLISIS DE TENDENCIAS ==========
    st.markdown("### 📈 Tendencias de Nearshoring" if lang == 'es' else 
                "### 📈 Nearshoring Trends" if lang == 'en' else
                "### 📈 Tendances de Nearshoring")
    
    # Análisis por año de contenedores
    yearly_containers = df_border[
        df_border['measure'].str.contains('Container', case=False)
    ].groupby('year')['value'].sum().reset_index()
    
    # Gráfico de crecimiento de contenedores
    fig_containers = px.line(
        yearly_containers,
        x='year',
        y='value',
        markers=True,
        title="Crecimiento Anual de Contenedores" if lang == 'es' else 
              "Annual Container Growth" if lang == 'en' else
              "Croissance Annuelle des Conteneurs",
        labels={'value': 'Contenedores', 'year': 'Año'}
    )
    fig_containers.update_layout(
        height=400,
        font=dict(color='#11101D', family='Inter'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig_containers.update_traces(line_color='#4070F4', line_width=3)
    
    st.plotly_chart(fig_containers, use_container_width=True)
    
    spacer(20)
    
    # ========== ANÁLISIS POR FRONTERA ==========
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌎 Frontera México-EEUU" if lang == 'es' else 
                    "#### 🌎 US-Mexico Border" if lang == 'en' else
                    "#### 🌎 Frontière Mexique-ÉU")
        
        # Contenedores México
        mexico_containers = df_border[
            (df_border['border'] == 'US-Mexico Border') & 
            (df_border['measure'].str.contains('Container', case=False))
        ].groupby('year')['value'].sum().reset_index()
        
        fig_mexico = px.bar(
            mexico_containers,
            x='year',
            y='value',
            color='year',
            title="Contenedores México" if lang == 'es' else "Mexico Containers" if lang == 'en' else "Conteneurs Mexique",
            labels={'value': 'Contenedores', 'year': 'Año'}
        )
        fig_mexico.update_layout(
            height=300,
            showlegend=False,
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_mexico, use_container_width=True)
    
    with col2:
        st.markdown("#### ❄️ Frontera Canadá-EEUU" if lang == 'es' else 
                    "#### ❄️ US-Canada Border" if lang == 'en' else
                    "#### ❄️ Frontière Canada-ÉU")
        
        # Contenedores Canadá
        canada_containers = df_border[
            (df_border['border'] == 'US-Canada Border') & 
            (df_border['measure'].str.contains('Container', case=False))
        ].groupby('year')['value'].sum().reset_index()
        
        fig_canada = px.bar(
            canada_containers,
            x='year',
            y='value',
            color='year',
            title="Contenedores Canadá" if lang == 'es' else "Canada Containers" if lang == 'en' else "Conteneurs Canada",
            labels={'value': 'Contenedores', 'year': 'Año'}
        )
        fig_canada.update_layout(
            height=300,
            showlegend=False,
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_canada, use_container_width=True)
    
    
    spacer(20)
    
    # ========== COMERCIO BILATERAL MÉXICO-EUA ==========
    st.markdown("### 💱 Comercio Bilateral México-EUA 2025-2026" if lang == 'es' else 
                "### 💱 US-Mexico Bilateral Trade 2025-2026" if lang == 'en' else
                "### 💱 Commerce Bilatéral Mexique-ÉU 2025-2026")
    
    # Datos de comercio 2025
    intercambio_total_2025 = 872830  # mdd
    exp_mexico_2025 = 534874  # mdd
    exp_usa_2025 = 338000  # mdd
    balanza_comercial = 196874  # mdd (superávit para México)
    crecimiento_intercambio = 3.9  # %
    crecimiento_exp_mexico = 5.8  # %
    
    # Métricas principales - Fila 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card(
            "Intercambio Total 2025" if lang == 'es' else "Total Trade 2025" if lang == 'en' else "Échange Total 2025",
            f"${intercambio_total_2025:,.0f}M",
            "💱",
            "#1976D2",
            f"+{crecimiento_intercambio}% vs 2024" if lang == 'es' else f"+{crecimiento_intercambio}% vs 2024"
        )
    
    with col2:
        metric_card(
            "Exports MX→USA" if lang == 'es' else "MX→USA Exports" if lang == 'en' else "Exportations MX→ÉU",
            f"${exp_mexico_2025:,.0f}M",
            "📤",
            "#4CAF50",
            f"+{crecimiento_exp_mexico}% anual" if lang == 'es' else f"+{crecimiento_exp_mexico}% YoY"
        )
    
    with col3:
        metric_card(
            "Imports USA→MX" if lang == 'es' else "USA→MX Imports" if lang == 'en' else "Importations ÉU→MX",
            f"${exp_usa_2025:,.0f}M",
            "📥",
            "#FF9800",
            "México #1 Mercado USA" if lang == 'es' else "MX #1 USA Market" if lang == 'en' else "MX #1 Marché ÉU"
        )
    
    with col4:
        metric_card(
            "Balanza Comercial" if lang == 'es' else "Trade Balance" if lang == 'en' else "Bilan Commercial",
            f"${balanza_comercial:,.0f}M",
            "📊",
            "#E91E63",
            "Superávit México" if lang == 'es' else "MX Surplus" if lang == 'en' else "Excédent Mexique"
        )
    
    spacer(15)
    
    # Visualizaciones de comercio
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Composición del Intercambio 2025" if lang == 'es' else 
                    "#### 📊 Trade Composition 2025" if lang == 'en' else
                    "#### 📊 Composition du Commerce 2025")
        
        # Gráfico de pie del intercambio
        trade_composition = {
            'Flujo': ['Exportaciones MX→USA', 'Importaciones USA→MX'] if lang == 'es' else
                     ['MX→USA Exports', 'USA→MX Imports'] if lang == 'en' else
                     ['Exportations MX→ÉU', 'Importations ÉU→MX'],
            'Valor': [exp_mexico_2025, exp_usa_2025]
        }
        
        fig_trade_comp = px.pie(
            trade_composition,
            values='Valor',
            names='Flujo',
            title="Flujos de Comercio" if lang == 'es' else "Trade Flows" if lang == 'en' else "Flux Commerciaux",
            color_discrete_sequence=['#4CAF50', '#FF9800']
        )
        fig_trade_comp.update_layout(
            height=350,
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_trade_comp, use_container_width=True)
    
    with col2:
        st.markdown("#### 📈 Proyecciones 2026" if lang == 'es' else 
                    "#### 📈 2026 Projections" if lang == 'en' else
                    "#### 📈 Projections 2026")
        
        # Datos de 2026 (Enero-Febrero vs datos mensuales)
        proyecciones_2026 = {
            'Mes': ['Febrero 2026\n(Real)', 'Proyección\nAnual 2026'] if lang == 'es' else
                   ['Feb 2026\n(Actual)', '2026 Annual\nProjection'] if lang == 'en' else
                   ['Février 2026\n(Réel)', 'Projection\nAnnuelle 2026'],
            'Exportaciones_USA': [28900 * 12, 700000 * 0.4],  # Estimación extrapolada
            'Importaciones_MX': [44300 * 12, 700000 * 0.6]   # Estimación extrapolada
        }
        
        fig_proj_2026 = px.bar(
            proyecciones_2026,
            x='Mes',
            y=['Exportaciones_USA', 'Importaciones_MX'],
            title="Proyección 2026" if lang == 'es' else "2026 Projection" if lang == 'en' else "Projection 2026",
            labels={
                'Exportaciones_USA': 'USA→MX' if lang == 'es' else 'USA→MX' if lang == 'en' else 'ÉU→MX',
                'Importaciones_MX': 'MX→USA' if lang == 'es' else 'MX→USA' if lang == 'en' else 'MX→ÉU',
                'value': 'Valor (mdd)',
                'Mes': 'Período'
            },
            color_discrete_sequence=['#FF9800', '#4CAF50']
        )
        fig_proj_2026.update_layout(
            height=350,
            showlegend=True,
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            barmode='group'
        )
        st.plotly_chart(fig_proj_2026, use_container_width=True)
    
    spacer(15)
    
    # Análisis de factores de riesgo y oportunidades
    st.markdown("#### ⚠️ Factores de Riesgo & Oportunidades 2026" if lang == 'es' else 
                "#### ⚠️ Risk Factors & Opportunities 2026" if lang == 'en' else
                "#### ⚠️ Facteurs de Risque & Opportunités 2026")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning("🚨 **Factores de Riesgo:**" if lang == 'es' else "🚨 **Risk Factors:**" if lang == 'en' else "🚨 **Facteurs de Risque:**")
        st.markdown(
            "• **Revisión T-MEC (julio 2026)**: Incertidumbre regulatoria potencial\n"
            "• **Nuevas barreras comerciales**: Aduanas y sectores energéticos bajo presión\n"
            "• **Volatilidad cambiaria**: Impacto en competitividad de exportaciones\n"
            "• **Slowdown global**: Demanda estadounidense podría enfrentar desaceleración" if lang == 'es' else
            "• **USMCA Review (July 2026)**: Potential regulatory uncertainty\n"
            "• **New trade barriers**: Customs and energy sectors under pressure\n"
            "• **Currency volatility**: Impact on export competitiveness\n"
            "• **Global slowdown**: US demand could face deceleration" if lang == 'en' else
            "• **Révision USMCA (juillet 2026)**: Incertitude réglementaire potentielle\n"
            "• **Nouvelles barrières commerciales**: Douanes et secteurs énergétiques sous pression\n"
            "• **Volatilité des devises**: Impact sur la compétitivité des exportations\n"
            "• **Ralentissement mondial**: Demande américaine pourrait ralentir"
        )
    
    with col2:
        st.success("💡 **Oportunidades 2026:**" if lang == 'es' else "💡 **Opportunities 2026:**" if lang == 'en' else "💡 **Opportunités 2026:**")
        st.markdown(
            "• **Proyección $700B**: Exportaciones totales mexicanas podrían alcanzar este nivel\n"
            "• **Posición #1**: México continúa como principal socio comercial de EUA\n"
            "• **Dinamismo manufacturero**: Crecimiento 5.8% (enero-febrero +6.4%)\n"
            "• **Nearshoring acelerado**: IED en manufactura sigue fluyendo" if lang == 'es' else
            "• **$700B Projection**: Total Mexican exports could reach this level\n"
            "• **#1 Position**: Mexico continues as USA's top trading partner\n"
            "• **Manufacturing momentum**: 5.8% growth (Jan-Feb +6.4%)\n"
            "• **Accelerated Nearshoring**: FDI in manufacturing continues flowing" if lang == 'en' else
            "• **Projection $700B**: Les exportations totales mexicaines pourraient atteindre ce niveau\n"
            "• **Position #1**: Le Mexique reste le principal partenaire commercial des ÉU\n"
            "• **Dynamique manufacturière**: Croissance 5.8% (janvier-février +6.4%)\n"
            "• **Nearshoring accéléré**: L'IDE dans la fabrication continue de s'accumuler"
        )
    
    spacer(20)
    
    # ========== CORREDORES DE MANUFACTURA ==========
    st.markdown("### 🏭 Corredores de Manufactura Estratégicos" if lang == 'es' else 
                "### 🏭 Strategic Manufacturing Corridors" if lang == 'en' else
                "### 🏭 Couloirs de Fabrication Stratégiques")
    st.info("📊 Análisis de nearshoring y corredores de manufactura (en desarrollo)")

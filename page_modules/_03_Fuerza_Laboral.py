"""
Página: Fuerza Laboral
Análisis del sector autotransporte, permisionarios, operadores y parque vehicular
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from modules.config import t, SEGMENTACION_FUERZA_LABORAL, DATOS_REGIONALES_FRONTERIZOS

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def obtener_datos_fuerza_laboral():
    """Obtiene datos de segmentación de empresas y operadores"""
    df_segmentos = pd.DataFrame(SEGMENTACION_FUERZA_LABORAL)
    
    cruce_data = pd.DataFrame({
        'Segmento': ['Hombre-Camión', 'Pequeña', 'Mediana', 'Grande'],
        'Operan solo MX': [98, 70, 40, 15],
        'Operan MC (Cruce)': [2, 30, 60, 85]
    })
    
    return df_segmentos, cruce_data


def obtener_datos_fuerza_laboral_regional():
    """Obtiene datos regionales de fuerza laboral por estado fronterizo"""
    return pd.DataFrame(DATOS_REGIONALES_FRONTERIZOS)


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

def page_fuerza_laboral():
    """Página de análisis de Fuerza Laboral en sector autotransporte"""
    
    lang = st.session_state.get('language', 'es')
    
    # Títulos según idioma
    if lang == 'es':
        titulo = "👥 Fuerza Laboral - Sector Autotransporte"
        subtitulo = "Análisis de permisionarios, operadores y capacidad operativa"
    elif lang == 'en':
        titulo = "👥 Workforce - Freight Transport Sector"
        subtitulo = "Analysis of operators, drivers and operational capacity"
    else:  # fr
        titulo = "👥 Force de Travail - Secteur du Transport Routier"
        subtitulo = "Analyse des opérateurs, conducteurs et capacité opérationnelle"
    
    # Título con estilo corporativo
    st.markdown(f"<h1 style='color: #11101D; font-weight: 700; margin-bottom: 0;'>{titulo}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #4070F4; font-size: 1.1rem; font-weight: 500; margin-top: 5px;'>{subtitulo}</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # SECCIÓN 1: INDICADORES PRINCIPALES
    if lang == 'es':
        sec1_title = "📊 Indicadores Principales 2024"
    elif lang == 'en':
        sec1_title = "📊 Main Indicators 2024"
    else:
        sec1_title = "📊 Indicateurs Principaux 2024"
    
    st.subheader(sec1_title)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Permisionarios" if lang == 'es' else "Total Operators" if lang == 'en' else "Total Opérateurs",
            value="198,500",
            delta="SICT 2024" if lang == 'es' else "SICT 2024" if lang == 'en' else "SICT 2024"
        )
    
    with col2:
        st.metric(
            label="Parque Vehicular" if lang == 'es' else "Vehicle Fleet" if lang == 'en' else "Parc Automobile",
            value="630,000",
            delta="Unidades activas" if lang == 'es' else "Active units" if lang == 'en' else "Unités actives"
        )
    
    with col3:
        st.metric(
            label="Déficit Operadores" if lang == 'es' else "Operator Deficit" if lang == 'en' else "Déficit Opérateurs",
            value="99,000",
            delta="Acumulado 2024" if lang == 'es' else "Accumulated 2024" if lang == 'en' else "Accumulé 2024",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="Ratio Operadores/Empresa" if lang == 'es' else "Operators/Company Ratio" if lang == 'en' else "Ratio Opérateurs/Entreprise",
            value="3.18",
            delta="Promedio nacional" if lang == 'es' else "National average" if lang == 'en' else "Moyenne nationale"
        )
    
    st.markdown("---")
    
    # SECCIÓN 2: SEGMENTACIÓN DE EMPRESAS
    if lang == 'es':
        sec2_title = "🏢 Segmentación de Empresas por Tamaño"
    elif lang == 'en':
        sec2_title = "🏢 Company Segmentation by Size"
    else:
        sec2_title = "🏢 Segmentation Entreprises par Taille"
    
    st.subheader(sec2_title)
    
    df_segmentos, _ = obtener_datos_fuerza_laboral()
    
    col_seg1, col_seg2 = st.columns([2, 1])
    
    with col_seg1:
        # Gráfico de barras de segmentación
        if lang == 'es':
            col_label = 'Número de Empresas'
        elif lang == 'en':
            col_label = 'Number of Companies'
        else:
            col_label = 'Nombre d\'Entreprises'
        
        fig_seg = px.bar(
            df_segmentos,
            x='Segmento',
            y=col_label,
            color='Segmento',
            text=col_label,
            title=sec2_title,
            labels={'Segmento': 'Segmento' if lang == 'es' else 'Segment' if lang == 'en' else 'Segment'},
            color_discrete_sequence=['#EF553B', '#FFA726', '#4070F4', '#4CAF50']
        )
        
        fig_seg.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_seg.update_layout(
            showlegend=False,
            height=400,
            hovermode='x unified',
            template='plotly_white'
        )
        
        st.plotly_chart(fig_seg, use_container_width=True)
    
    with col_seg2:
        st.markdown("**Análisis Clave** " + ("" if lang != 'es' else "(ES)") + ("" if lang != 'en' else "(EN)"))
        
        if lang == 'es':
            st.markdown("""
            - **Pequeñas**: 163,200 (82.2%)
            - Parque: 1-5 unidades
            - Mayor atomización del sector
            
            - **Medianas**: 29,800 (15%)
            - Parque: 6-30 unidades
            - Mercado consolidado
            
            - **Grandes**: 5,500 (2.8%)
            - Parque: 31+ unidades
            - Cobertura nacional
            """)
        elif lang == 'en':
            st.markdown("""
            - **Small**: 163,200 (82.2%)
            - Fleet: 1-5 units
            - Highly fragmented
            
            - **Medium**: 29,800 (15%)
            - Fleet: 6-30 units
            - Consolidated market
            
            - **Large**: 5,500 (2.8%)
            - Fleet: 31+ units
            - National coverage
            """)
        else:
            st.markdown("""
            - **Petites**: 163,200 (82.2%)
            - Parc: 1-5 unités
            - Très fragmenté
            
            - **Moyennes**: 29,800 (15%)
            - Parc: 6-30 unités
            - Marché consolidé
            
            - **Grandes**: 5,500 (2.8%)
            - Parc: 31+ unités
            - Couverture nationale
            """)
    
    st.markdown("---")
    
    # SECCIÓN 3: DISTRIBUCIÓN GEOGRAFICA
    if lang == 'es':
        sec3_title = "🌎 Distribución Geográfica - Frontera México-USA"
    elif lang == 'en':
        sec3_title = "🌎 Geographic Distribution - Mexico-USA Border"
    else:
        sec3_title = "🌎 Distribution Géographique - Frontière Mexique-USA"
    
    st.subheader(sec3_title)
    
    df_regional = obtener_datos_fuerza_laboral_regional()
    
    # Métricas por región
    col_r1, col_r2, col_r3, col_r4, col_r5, col_r6 = st.columns(6)
    
    cols_regios = [col_r1, col_r2, col_r3, col_r4, col_r5, col_r6]
    
    for idx, (col_idx, (_, row)) in enumerate(zip(cols_regios, df_regional.iterrows())):
        with col_idx:
            region = row['Region']
            parque = row['Parque_Vehicular']
            permisionarios = row['Permisionarios']
            
            if lang == 'es':
                st.metric(label=region, value=f"{parque:,}", delta=f"{permisionarios:,} empresas")
            elif lang == 'en':
                st.metric(label=region, value=f"{parque:,}", delta=f"{permisionarios:,} companies")
            else:
                st.metric(label=region, value=f"{parque:,}", delta=f"{permisionarios:,} entreprises")
    
    # Gráfico de barras comparativo
    st.markdown("")
    
    col_map1, col_map2 = st.columns([1.2, 1])
    
    with col_map1:
        # Gráfico de dispersión: Parque Vehicular vs Permisionarios
        fig_scatter = px.scatter(
            df_regional,
            x='Permisionarios',
            y='Parque_Vehicular',
            size='Empresas_con_MC',
            color='Region',
            hover_data={'Aduanas_Principales': True},
            labels={
                'Permisionarios': 'Permisionarios' if lang == 'es' else 'Operators' if lang == 'en' else 'Opérateurs',
                'Parque_Vehicular': 'Parque Vehicular' if lang == 'es' else 'Vehicle Fleet' if lang == 'en' else 'Parc Automobile'
            },
            title="Relación Permisionarios vs Parque Vehicular por Región" if lang == 'es' else (
                "Operators vs Vehicle Fleet by Region" if lang == 'en' else 
                "Relation Opérateurs vs Parc par Région"
            )
        )
        
        fig_scatter.update_layout(
            height=400,
            template='plotly_white',
            showlegend=True
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col_map2:
        # Ranking de regiones por parque vehicular
        df_sorted = df_regional.sort_values('Parque_Vehicular', ascending=True)
        
        fig_bar = px.bar(
            df_sorted,
            x='Parque_Vehicular',
            y='Region',
            orientation='h',
            color='Parque_Vehicular',
            text='Parque_Vehicular',
            title="Top Regiones por Parque" if lang == 'es' else (
                "Top Regions by Fleet" if lang == 'en' else 
                "Top Régions par Parc"
            ),
            color_continuous_scale='Blues'
        )
        
        fig_bar.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig_bar.update_layout(
            height=400,
            showlegend=False,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    # SECCIÓN 4: CAPACIDAD DE CRUCE FRONTERIZO
    if lang == 'es':
        sec4_title = "🚚 Capacidad de Cruce Fronterizo (MC)"
    elif lang == 'en':
        sec4_title = "🚚 Cross-Border Crossing Capacity (MC)"
    else:
        sec4_title = "🚚 Capacité de Passage Frontalier (MC)"
    
    st.subheader(sec4_title)
    
    col_cap1, col_cap2 = st.columns(2)
    
    with col_cap1:
        # Gráfico de columnas apiladas
        df_mc = df_regional[['Region', 'Permisionarios', 'Empresas_con_MC']].copy()
        df_mc['Sin MC'] = df_mc['Permisionarios'] - df_mc['Empresas_con_MC']
        df_mc = df_mc[['Region', 'Empresas_con_MC', 'Sin MC']]
        
        fig_stack = go.Figure()
        
        fig_stack.add_trace(go.Bar(
            x=df_mc['Region'],
            y=df_mc['Empresas_con_MC'],
            name='Con MC' if lang == 'es' else ('With MC' if lang == 'en' else 'Avec MC'),
            marker_color='#4CAF50'
        ))
        
        fig_stack.add_trace(go.Bar(
            x=df_mc['Region'],
            y=df_mc['Sin MC'],
            name='Sin MC' if lang == 'es' else ('Without MC' if lang == 'en' else 'Sans MC'),
            marker_color='#E0E0E0'
        ))
        
        fig_stack.update_layout(
            barmode='stack',
            height=400,
            title="Empresas con Autorización para Cruzar Frontera (MC)" if lang == 'es' else (
                "Companies Authorized to Cross Border (MC)" if lang == 'en' else 
                "Entreprises Autorisées à Traverser Frontière (MC)"
            ),
            xaxis_title='Región' if lang == 'es' else ('Region' if lang == 'en' else 'Région'),
            yaxis_title='Número de Empresas' if lang == 'es' else ('Number of Companies' if lang == 'en' else 'Nombre Entreprises'),
            template='plotly_white',
            showlegend=True
        )
        
        st.plotly_chart(fig_stack, use_container_width=True)
    
    with col_cap2:
        # Tabla de capacidad
        df_cap = df_regional[['Region', 'Permisionarios', 'Empresas_con_MC', '% MC']].copy()
        
        if lang == 'es':
            df_cap.columns = ['Región', 'Total Empresas', 'Con MC', '% MC']
        elif lang == 'en':
            df_cap.columns = ['Region', 'Total Companies', 'With MC', '% MC']
        else:
            df_cap.columns = ['Région', 'Total Entreprises', 'Avec MC', '% MC']
        
        st.dataframe(df_cap, hide_index=True, use_container_width=True, height=400)
    
    st.markdown("---")
    
    # SECCIÓN 5: ALERTAS Y OPORTUNIDADES
    if lang == 'es':
        sec5_title = "⚠️ Alertas y Oportunidades"
    elif lang == 'en':
        sec5_title = "⚠️ Alerts and Opportunities"
    else:
        sec5_title = "⚠️ Alertes et Opportunités"
    
    st.subheader(sec5_title)
    
    col_alert1, col_alert2 = st.columns(2)
    
    with col_alert1:
        if lang == 'es':
            st.warning("""
            **🔴 Déficit Crítico de Operadores**
            
            - Déficit acumulado 2024: 99,000 operadores
            - Representan el 15.7% del parque vehicular
            - Impacto: Capacidad ociosa, reducción de competitividad
            
            **Recomendaciones:**
            1. Programas de capacitación vía IUSAC/IFT
            2. Mejora salarial competitiva
            3. Beneficios de retención
            """)
        elif lang == 'en':
            st.warning("""
            **🔴 Critical Operator Deficit**
            
            - Accumulated deficit 2024: 99,000 operators
            - Represents 15.7% of vehicle fleet
            - Impact: Idle capacity, reduced competitiveness
            
            **Recommendations:**
            1. Training programs via IUSAC/IFT
            2. Competitive wage improvement
            3. Retention benefits
            """)
        else:
            st.warning("""
            **🔴 Déficit Critique d'Opérateurs**
            
            - Déficit accumulé 2024: 99,000 opérateurs
            - Représente 15.7% du parc automobile
            - Impact: Capacité oisive, compétitivité réduite
            
            **Recommandations:**
            1. Programmes de formation via IUSAC/IFT
            2. Amélioration salariale compétitive
            3. Avantages de rétention
            """)
    
    with col_alert2:
        if lang == 'es':
            st.success("""
            **✅ Oportunidades de Consolidación**
            
            - 82.2% son "hombre-camión" (1-5 unidades)
            - Fragmentación representa oportunidad de consolidación
            - Potencial: Crear 2,000-3,000 empresas medianas
            
            **Estrategias:**
            1. Incentivos fiscales para fusiones
            2. Créditos para modernización
            3. Certificaciones colectivas (Green Corridor)
            """)
        elif lang == 'en':
            st.success("""
            **✅ Consolidation Opportunities**
            
            - 82.2% are "single-truck" operators (1-5 units)
            - Fragmentation represents consolidation opportunity
            - Potential: Create 2,000-3,000 mid-size companies
            
            **Strategies:**
            1. Tax incentives for mergers
            2. Credits for modernization
            3. Collective certifications (Green Corridor)
            """)
        else:
            st.success("""
            **✅ Opportunités de Consolidation**
            
            - 82.2% sont des "camionneurs indépendants" (1-5 unités)
            - Fragmentation = opportunité de consolidation
            - Potentiel: Créer 2,000-3,000 entreprises moyennes
            
            **Stratégies:**
            1. Incitations fiscales pour fusions
            2. Crédits pour modernisation
            3. Certifications collectives (Green Corridor)
            """)
    
    st.markdown("---")
    
    # Pie de página
    if lang == 'es':
        footer = "📊 Datos basados en SICT 2024 | Fuentes: SCT, IUSAC, IRU"
    elif lang == 'en':
        footer = "📊 Data based on SICT 2024 | Sources: SCT, IUSAC, IRU"
    else:
        footer = "📊 Données basées sur SICT 2024 | Sources: SCT, IUSAC, IRU"
    
    st.caption(footer)

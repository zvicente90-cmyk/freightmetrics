import streamlit as st
import pandas as pd
import plotly.express as px
from monitor_helpers import obtener_datos_fuerza_laboral, obtener_datos_fuerza_laboral_regional


def page_fuerza_laboral():
    # Título con diseño NEON cyberpunk  
    st.markdown("<h1 style='color: #00D4FF; font-weight: 700; margin-bottom: 0; text-shadow: 0 0 10px #00D4FF;'>👥 Segmentación de Empresas y Operadores</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00D4FF; font-size: 1.1rem; font-weight: 500; margin-top: 5px; margin-bottom: 20px; opacity: 0.9;'>Clasificación por tamaño de flota y capacidad operativa del sector autotransporte</p>", unsafe_allow_html=True)
    
    # Métricas Clave con tema NEON
    st.markdown("""
        <div style='background: linear-gradient(135deg, #0D1B2A 0%, #1a2a3d 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 15px 0;
                    border: 2px solid #00D4FF;
                    box-shadow: 0 0 20px rgba(0, 212, 255, 0.3), inset 0 0 20px rgba(0, 212, 255, 0.05);'>
            <h3 style='color: #00D4FF; margin: 0; font-size: 1.1rem; font-weight: 700; text-shadow: 0 0 10px #00D4FF;'>📊 Datos del Sector Autotransporte en México</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown("""
            <div style='background-color: #0D1B2A; 
                        border-left: 4px solid #00D4FF;
                        border: 1px solid #00D4FF;
                        padding: 20px; 
                        border-radius: 8px;
                        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
                        margin: 10px 0;'>
                <p style='color: #00D4FF; font-size: 0.85rem; font-weight: 700; margin: 0; text-transform: uppercase; letter-spacing: 1px;'>Total Permisionarios</p>
                <h2 style='color: #FFFFFF; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0; text-shadow: 0 0 10px #00D4FF;'>~198,500</h2>
                <p style='color: #00D4FF; font-size: 0.85rem; margin: 0; opacity: 0.8;'>🏢 Permisionarios federales (SICT)</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown("""
            <div style='background-color: #0D1B2A; 
                        border-left: 4px solid #00D4FF;
                        border: 1px solid #00D4FF;
                        padding: 20px; 
                        border-radius: 8px;
                        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
                        margin: 10px 0;'>
                <p style='color: #00D4FF; font-size: 0.85rem; font-weight: 700; margin: 0; text-transform: uppercase; letter-spacing: 1px;'>Parque Vehicular</p>
                <h2 style='color: #FFFFFF; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0; text-shadow: 0 0 10px #00D4FF;'>~630,000</h2>
                <p style='color: #00D4FF; font-size: 0.85rem; margin: 0; opacity: 0.8;'>🚛 Unidades motrices en operación</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown("""
            <div style='background-color: #0D1B2A; 
                        border-left: 4px solid #FF3366;
                        border: 1px solid #FF3366;
                        padding: 20px; 
                        border-radius: 8px;
                        box-shadow: 0 0 15px rgba(255, 51, 102, 0.2);
                        margin: 10px 0;'>
                <p style='color: #FF3366; font-size: 0.85rem; font-weight: 700; margin: 0; text-transform: uppercase; letter-spacing: 1px;'>Déficit de Operadores</p>
                <h2 style='color: #FF3366; font-size: 2.2rem; font-weight: 700; margin: 10px 0 5px 0; text-shadow: 0 0 10px #FF3366;'>~99,000</h2>
                <p style='color: #FF3366; font-size: 0.85rem; margin: 0; opacity: 0.9;'>⚠️ Vacantes según IRU 2024 (+76.7% vs 2023)</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

    # DATOS DE SEGMENTACIÓN (desde helpers)
    df_segmentos, cruce_data = obtener_datos_fuerza_laboral()

    st.markdown("---")

    # GRÁFICO DE DONAS - PARTICIPACIÓN DE MERCADO
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.markdown("<h3 style='color: #00D4FF; font-weight: 700; text-shadow: 0 0 10px #00D4FF;'>🎯 Participación de Mercado</h3>", unsafe_allow_html=True)
        fig_pie = px.pie(
            df_segmentos, 
            values='Número de Empresas', 
            names='Segmento',
            hole=0.4,
            color_discrete_sequence=['#00D4FF', '#FF3366', '#00D4FF', '#FF3366'],
            title='Distribución Porcentual de Empresas'
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='#FFFFFF', size=12))
        fig_pie.update_layout(
            height=400,
            title_font_color='#00D4FF',
            title_font_size=16,
            title_font_family='Inter',
            font=dict(color='#FFFFFF', size=12, family='Inter'),
            plot_bgcolor='#0D1B2A',
            paper_bgcolor='#0D1B2A'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col4:
        st.markdown("<h3 style='color: #00D4FF; font-weight: 700; text-shadow: 0 0 10px #00D4FF;'>⚡ Eficiencia Operativa</h3>", unsafe_allow_html=True)
        df_segmentos['Operadores/Empresa'] = (df_segmentos['Total Operadores'] / df_segmentos['Número de Empresas']).round(1)
        
        fig_eficiencia = px.bar(
            df_segmentos,
            x='Segmento',
            y='Operadores/Empresa',
            color='Operadores/Empresa',
            color_continuous_scale=[[0, '#00D4FF'], [1, '#FF3366']],
            text='Operadores/Empresa',
            labels={'Operadores/Empresa': 'Operadores promedio'},
            title='Promedio de Operadores por Empresa'
        )
        fig_eficiencia.update_traces(texttemplate='%{text:.1f}', textposition='outside', textfont=dict(color='#00D4FF', size=12))
        fig_eficiencia.update_layout(
            showlegend=False, 
            height=400,
            title_font_color='#00D4FF',
            title_font_size=16,
            title_font_family='Inter',
            font=dict(color='#FFFFFF', size=12, family='Inter'),
            plot_bgcolor='#0D1B2A',
            paper_bgcolor='#0D1B2A',
            yaxis=dict(gridcolor='rgba(0, 212, 255, 0.1)')
        )
        st.plotly_chart(fig_eficiencia, use_container_width=True)

    st.markdown("---")

    # TABLA COMPARATIVA - Tema oscuro
    st.markdown("""
        <div style='background: linear-gradient(135deg, #0D1B2A 0%, #1a3a4d 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0 15px 0;
                    border: 1px solid #00D4FF;
                    box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);'>
            <h3 style='color: #00D4FF; margin: 0; font-size: 1.1rem; font-weight: 600; text-shadow: 0 0 10px #00D4FF;'>📊 Datos Comparativos por Segmento</h3>
        </div>
    """, unsafe_allow_html=True)
    
    columnas_mostrar = ['Segmento', 'Rango Unidades', 'Número de Empresas', 'Total Operadores', 'Participación Mercado']
    st.dataframe(
        df_segmentos[columnas_mostrar].style.format({
            'Número de Empresas': '{:,.0f}',
            'Total Operadores': '{:,.0f}'
        }).set_properties(**{
            'background-color': '#1a2a3d',
            'color': '#00D4FF',
            'border-color': '#00D4FF',
            'font-family': 'Inter'
        }).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#0D1B2A'), ('color', '#00D4FF'), ('font-weight', '600'), ('border', '1px solid #00D4FF')]},
            {'selector': 'td', 'props': [('text-align', 'center'), ('border', '1px solid #00D4FF')]}
        ]),
        use_container_width=True, 
        hide_index=True
    )

    st.markdown("---")

    # INSIGHT Y ESTADOS
    st.markdown("""
        <div style='background-color: #0D1B2A; 
                    border-left: 5px solid #00D4FF;
                    border: 1px solid #00D4FF;
                    padding: 15px 20px; 
                    border-radius: 8px;
                    margin: 20px 0;
                    box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);'>
            <p style='color: #00D4FF; font-size: 0.95rem; margin: 0; line-height: 1.6;'>
                💡 <strong>Insight:</strong> A mayor tamaño de empresa, mayor es la probabilidad de contar con flota dedicada al cruce internacional (Permiso MC).
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ESTADOS CON EMPRESAS DE CRUCE
    st.markdown("<h2 style='color: #00D4FF; font-weight: 700; margin-bottom: 5px; text-shadow: 0 0 10px #00D4FF;'>🌎 Estados con Mayor Actividad de Cruce Fronterizo</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #CCCCCC; font-size: 1rem; margin-bottom: 20px;'>Distribución de empresas con permiso MC (Modalidad de Cruce) por entidad federativa.</p>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background-color: #0D1B2A; 
                    padding: 12px 20px; 
                    border-radius: 10px;
                    border: 1px solid #00D4FF;
                    box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
                    margin: 15px 0;'>
            <p style='color: #00D4FF; font-size: 0.9rem; font-weight: 600; margin: 0;'>🔍 Filtros de Búsqueda</p>
        </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f1:
        año_seleccionado = st.selectbox("📅 Año:", [2026, 2025, 2024, 2023, 2022], index=0)
    with col_f2:
        estados_disponibles = ['Todos los estados', 'Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche', 
                               'Chiapas', 'Chihuahua', 'Ciudad de México', 'Coahuila', 'Colima', 'Durango', 
                               'Estado de México', 'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco', 'Michoacán', 
                               'Morelos', 'Nayarit', 'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo', 
                               'San Luis Potosí', 'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 
                               'Veracruz', 'Yucatán', 'Zacatecas']
        estados_filtro = st.multiselect("🗺️ Filtrar por Estados:", estados_disponibles, default=['Todos los estados'])
    with col_f3:
        top_n = st.slider("Top N estados:", min_value=5, max_value=32, value=10, step=1)

    factor_año = 1.0 if año_seleccionado == 2026 else 0.95 if año_seleccionado == 2025 else 0.90 if año_seleccionado == 2024 else 0.85 if año_seleccionado == 2023 else 0.80
    
    estados_cruce_completo = pd.DataFrame({
        'Estado': ['Tamaulipas', 'Nuevo León', 'Baja California', 'Chihuahua', 'Jalisco', 'Sonora', 
                   'Estado de México', 'Coahuila', 'Guanajuato', 'Veracruz', 'Querétaro', 'Puebla',
                   'Sinaloa', 'San Luis Potosí', 'Aguascalientes', 'Durango', 'Michoacán', 'Hidalgo',
                   'Morelos', 'Chiapas', 'Yucatán', 'Tabasco', 'Quintana Roo', 'Oaxaca', 'Guerrero',
                   'Nayarit', 'Zacatecas', 'Colima', 'Tlaxcala', 'Campeche', 'Baja California Sur', 'Ciudad de México'],
        'Empresas MC': [6100, 5200, 3500, 2800, 2100, 1800, 1650, 1500, 1420, 1380, 1250, 1150,
                        980, 850, 720, 650, 580, 520, 450, 380, 350, 320, 280, 240, 210,
                        180, 150, 120, 95, 70, 55, 850],
        'Total Empresas Estado': [18500, 22000, 12500, 11000, 15000, 9500, 38000, 9500, 12000, 14000, 9000, 16000,
                                  8200, 7500, 2100, 3200, 6500, 4800, 2100, 3100, 3500, 3100, 1800, 2800, 2500,
                                  1400, 2200, 1500, 2800, 1200, 800, 25000]
    })

    estados_cruce_completo['Empresas MC'] = (estados_cruce_completo['Empresas MC'] * factor_año).round(0).astype(int)
    estados_cruce_completo['Total Empresas Estado'] = (estados_cruce_completo['Total Empresas Estado'] * factor_año).round(0).astype(int)
    
    estados_cruce_completo['Porcentaje MC (%)'] = ((estados_cruce_completo['Empresas MC'] / estados_cruce_completo['Total Empresas Estado']) * 100).round(1)
    estados_cruce_completo['Porcentaje Nacional (%)'] = ((estados_cruce_completo['Empresas MC'] / estados_cruce_completo['Empresas MC'].sum()) * 100).round(1)
    estados_cruce_completo['Año'] = año_seleccionado
    
    if 'Todos los estados' not in estados_filtro and len(estados_filtro) > 0:
        estados_cruce = estados_cruce_completo[estados_cruce_completo['Estado'].isin(estados_filtro)].copy()
    else:
        estados_cruce = estados_cruce_completo.copy()
    
    estados_cruce = estados_cruce.sort_values('Empresas MC', ascending=False).head(top_n)
    
    col_e1, col_e2 = st.columns([1.2, 1])
    
    with col_e1:
        fig_estados_mc = px.bar(
            estados_cruce.sort_values('Empresas MC', ascending=True),
            y='Estado',
            x='Empresas MC',
            orientation='h',
            color='Empresas MC',
            color_continuous_scale=[[0, '#00D4FF'], [1, '#FF3366']],
            text='Empresas MC',
            labels={'Empresas MC': 'Empresas con Permiso MC'},
            title='Empresas con Permiso de Cruce por Estado'
        )
        fig_estados_mc.update_traces(texttemplate='%{text:,.0f}', textposition='outside', textfont=dict(color='#00D4FF', size=12))
        fig_estados_mc.update_layout(
            showlegend=False, 
            height=400,
            title_font_color='#00D4FF',
            title_font_size=16,
            title_font_family='Inter',
            font=dict(color='#FFFFFF', size=12, family='Inter'),
            plot_bgcolor='#0D1B2A',
            paper_bgcolor='#0D1B2A',
            yaxis=dict(gridcolor='rgba(0, 212, 255, 0.1)')
        )
        st.plotly_chart(fig_estados_mc, use_container_width=True)
    
    with col_e2:
        fig_dona_estados = px.pie(
            estados_cruce,
            values='Empresas MC',
            names='Estado',
            hole=0.5,
            color_discrete_sequence=['#00D4FF', '#FF3366', '#FF6699', '#00AADD', '#FF1133', '#00DDFF', '#FF5588', '#00BBEE', '#FF3366', '#00D4FF'],
            title='Participación Nacional'
        )
        fig_dona_estados.update_traces(textposition='inside', textinfo='percent', textfont=dict(color='#FFFFFF', size=12))
        fig_dona_estados.update_layout(
            height=400, 
            showlegend=True,
            title_font_color='#00D4FF',
            title_font_size=16,
            title_font_family='Inter',
            font=dict(color='#FFFFFF', size=12, family='Inter'),
            plot_bgcolor='#0D1B2A',
            paper_bgcolor='#0D1B2A'
        )
        st.plotly_chart(fig_dona_estados, use_container_width=True)

    st.markdown("<h3 style='color: #00D4FF; font-weight: 700; margin-top: 30px; text-shadow: 0 0 10px #00D4FF;'>📊 Penetración del Permiso MC por Estado</h3>", unsafe_allow_html=True)
    fig_penetracion = px.bar(
        estados_cruce.sort_values('Porcentaje MC (%)', ascending=False),
        x='Estado',
        y='Porcentaje MC (%)',
        color='Porcentaje MC (%)',
        color_continuous_scale=[[0, '#00D4FF'], [1, '#FF3366']],
        text='Porcentaje MC (%)',
        labels={'Porcentaje MC (%)': '% Empresas con MC'},
        title='Porcentaje de Empresas con Permiso MC respecto al Total Estatal'
    )
    fig_penetracion.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont=dict(color='#00D4FF', size=12))
    fig_penetracion.update_layout(
        showlegend=False, 
        height=400, 
        xaxis_tickangle=-45,
        title_font_color='#00D4FF',
        title_font_size=16,
        title_font_family='Inter',
        font=dict(color='#FFFFFF', size=12, family='Inter'),
        plot_bgcolor='#0D1B2A',
        paper_bgcolor='#0D1B2A',
        yaxis=dict(gridcolor='rgba(0, 212, 255, 0.1)')
    )
    st.plotly_chart(fig_penetracion, use_container_width=True)

    st.markdown("---")

    # ANÁLISIS DE PRODUCTIVIDAD
    st.markdown("<h2 style='color: #00D4FF; font-weight: 700; margin-bottom: 5px; text-shadow: 0 0 10px #00D4FF;'>📊 Análisis de Productividad por Región y Tipo de Empresa</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #CCCCCC; font-size: 1rem; margin-bottom: 20px;'>Evaluación de eficiencia operativa y capacidad productiva del sector</p>", unsafe_allow_html=True)
    
    regiones_data = pd.DataFrame({
        'Región': ['Norte', 'Centro', 'Sur'],
        'Estados': ['Tamaulipas, Nuevo León, Coahuila, Chihuahua, Sonora, Baja California', 
                   'Estado de México, Jalisco, Guanajuato, Querétaro, Puebla, Veracruz',
                   'Chiapas, Oaxaca, Tabasco, Yucatán, Quintana Roo, Campeche'],
        'Total Empresas': [68500, 95000, 12800],
        'Total Operadores': [287000, 285000, 58000],
        'Parque Vehicular': [325000, 260000, 45000],
        'PIB Transporte (miles MDP)': [185.5, 245.3, 42.8],
    })
    regiones_data['Operadores/Empresa'] = (regiones_data['Total Operadores'] / regiones_data['Total Empresas']).round(2)
    regiones_data['Unidades/Empresa'] = (regiones_data['Parque Vehicular'] / regiones_data['Total Empresas']).round(2)
    regiones_data['Operadores/Unidad'] = (regiones_data['Total Operadores'] / regiones_data['Parque Vehicular']).round(2)
    regiones_data['Ingreso per Operador (pesos)'] = (regiones_data['PIB Transporte (miles MDP)'] * 1_000_000_000 / regiones_data['Total Operadores']).round(0)

    st.markdown("<h3 style='color: #00D4FF; font-weight: 700; margin-top: 20px; text-shadow: 0 0 10px #00D4FF;'>🌎 Indicadores por Región Geográfica</h3>", unsafe_allow_html=True)
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        st.markdown(f"""
            <div style='background-color: #0D1B2A; 
                        border-left: 5px solid #00D4FF;
                        border: 1px solid #00D4FF;
                        padding: 20px; 
                        border-radius: 8px;
                        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
                        margin: 10px 0;'>
                <p style='color: #00D4FF; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>🔵 Región Norte</p>
                <h2 style='color: #FFFFFF; font-size: 2rem; font-weight: 700; margin: 10px 0 5px 0; text-shadow: 0 0 10px #00D4FF;'>{regiones_data.loc[regiones_data['Región'] == 'Norte', 'Total Empresas'].values[0]:,.0f}</h2>
                <p style='color: #CCCCCC; font-size: 0.85rem; margin: 5px 0;'>Empresas registradas</p>
                <p style='color: #00D4FF; font-size: 0.9rem; font-weight: 600; margin: 10px 0 5px 0;'>{regiones_data.loc[regiones_data['Región'] == 'Norte', 'Operadores/Empresa'].values[0]:.2f} operadores/empresa</p>
                <p style='color: #CCCCCC; font-size: 0.8rem; margin: 0;'>Ingreso: ${regiones_data.loc[regiones_data['Región'] == 'Norte', 'Ingreso per Operador (pesos)'].values[0]:,.0f}/operador</p>
            </div>
        """, unsafe_allow_html=True)
    with col_r2:
        st.markdown(f"""
            <div style='background-color: #0D1B2A; 
                        border-left: 5px solid #00D4FF;
                        border: 1px solid #00D4FF;
                        padding: 20px; 
                        border-radius: 8px;
                        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
                        margin: 10px 0;'>
                <p style='color: #00D4FF; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>🟢 Región Centro</p>
                <h2 style='color: #FFFFFF; font-size: 2rem; font-weight: 700; margin: 10px 0 5px 0; text-shadow: 0 0 10px #00D4FF;'>{regiones_data.loc[regiones_data['Región'] == 'Centro', 'Total Empresas'].values[0]:,.0f}</h2>
                <p style='color: #CCCCCC; font-size: 0.85rem; margin: 5px 0;'>Empresas registradas</p>
                <p style='color: #00D4FF; font-size: 0.9rem; font-weight: 600; margin: 10px 0 5px 0;'>{regiones_data.loc[regiones_data['Región'] == 'Centro', 'Operadores/Empresa'].values[0]:.2f} operadores/empresa</p>
                <p style='color: #CCCCCC; font-size: 0.8rem; margin: 0;'>Ingreso: ${regiones_data.loc[regiones_data['Región'] == 'Centro', 'Ingreso per Operador (pesos)'].values[0]:,.0f}/operador</p>
            </div>
        """, unsafe_allow_html=True)
    with col_r3:
        st.markdown(f"""
            <div style='background-color: #0D1B2A; 
                        border-left: 5px solid #FF3366;
                        border: 1px solid #FF3366;
                        padding: 20px; 
                        border-radius: 8px;
                        box-shadow: 0 0 15px rgba(255, 51, 102, 0.2);
                        margin: 10px 0;'>
                <p style='color: #FF3366; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>🟡 Región Sur</p>
                <h2 style='color: #FFFFFF; font-size: 2rem; font-weight: 700; margin: 10px 0 5px 0; text-shadow: 0 0 10px #FF3366;'>{regiones_data.loc[regiones_data['Región'] == 'Sur', 'Total Empresas'].values[0]:,.0f}</h2>
                <p style='color: #CCCCCC; font-size: 0.85rem; margin: 5px 0;'>Empresas registradas</p>
                <p style='color: #00D4FF; font-size: 0.9rem; font-weight: 600; margin: 10px 0 5px 0;'>{regiones_data.loc[regiones_data['Región'] == 'Sur', 'Operadores/Empresa'].values[0]:.2f} operadores/empresa</p>
                <p style='color: #CCCCCC; font-size: 0.8rem; margin: 0;'>Ingreso: ${regiones_data.loc[regiones_data['Región'] == 'Sur', 'Ingreso per Operador (pesos)'].values[0]:,.0f}/operador</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Tabla resumen por región
    region_stats = pd.DataFrame({
        'Region': ['Norte', 'Centro', 'Sur'],
        'Empresas_Reg': [68500, 95000, 12800],
        'Parque_Vehicular': [325000, 260000, 45000],
        'Vacantes_Reportadas': [28700, 28500, 5800]
    })
    region_stats['Capacidad_Ociosa_%_Ponderada'] = ((region_stats['Vacantes_Reportadas'] / region_stats['Parque_Vehicular']) * 100).round(1)

    st.dataframe(region_stats.style.format({
        'Empresas_Reg': '{:,.0f}',
        'Parque_Vehicular': '{:,.0f}',
        'Vacantes_Reportadas': '{:,.0f}',
        'Capacidad_Ociosa_%_Ponderada': '{:.1f}%'
    }).set_properties(**{
        'background-color': '#1a2a3d',
        'color': '#00D4FF',
        'font-family': 'Inter'
    }).set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#0D1B2A'), ('color', '#00D4FF'), ('font-weight', '600'), ('border', '1px solid #00D4FF')]},
        {'selector': 'td', 'props': [('text-align', 'center'), ('border', '1px solid #00D4FF')]}
    ]), use_container_width=True)

    st.markdown("---")

    # ANÁLISIS IRU 2024 - DIFICULTADES EMPRESARIALES
    st.markdown("""
        <div style='background: linear-gradient(135deg, #0D1B2A 0%, #1a2a4d 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0 15px 0;
                    border: 1px solid #FF3366;
                    box-shadow: 0 0 20px rgba(255, 51, 102, 0.2);'>
            <h3 style='color: #FF3366; margin: 0; font-size: 1.1rem; font-weight: 600; text-shadow: 0 0 10px #FF3366;'>📊 Informe IRU 2024: Análisis de Dificultades Empresariales</h3>
        </div>
    """, unsafe_allow_html=True)

    col_iru1, col_iru2, col_iru3 = st.columns(3)
    
    with col_iru1:
        st.markdown("""
            <div style='background-color: #0D1B2A; 
                        border-left: 5px solid #FF3366;
                        border: 1px solid #FF3366;
                        padding: 20px; 
                        border-radius: 8px;
                        box-shadow: 0 0 15px rgba(255, 51, 102, 0.2);
                        margin: 10px 0;'>
                <p style='color: #FF3366; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>🔴 Dificultades Graves/Muy Graves</p>
                <h2 style='color: #FF3366; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0; text-shadow: 0 0 10px #FF3366;'>67%</h2>
                <p style='color: #CCCCCC; font-size: 0.85rem; margin: 5px 0;'>De empresas mexicanas</p>
                <p style='color: #AAAAAA; font-size: 0.8rem; margin: 0;'>📉 Mejoró desde 78% en 2023</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_iru2:
        st.markdown("""
            <div style='background-color: #0D1B2A; 
                        border-left: 5px solid #FFA500;
                        border: 1px solid #FFA500;
                        padding: 20px; 
                        border-radius: 8px;
                        box-shadow: 0 0 15px rgba(255, 165, 0, 0.2);
                        margin: 10px 0;'>
                <p style='color: #FFA500; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>🟠 Dificultades Moderadas</p>
                <h2 style='color: #FFA500; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>27%</h2>
                <p style='color: #CCCCCC; font-size: 0.85rem; margin: 5px 0;'>De empresas mexicanas</p>
                <p style='color: #AAAAAA; font-size: 0.8rem; margin: 0;'>Situación manejable pero compleja</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_iru3:
        st.markdown("""
            <div style='background-color: #0D1B2A; 
                        border-left: 5px solid #00AA77;
                        border: 1px solid #00AA77;
                        padding: 20px; 
                        border-radius: 8px;
                        box-shadow: 0 0 15px rgba(0, 170, 119, 0.2);
                        margin: 10px 0;'>
                <p style='color: #00AA77; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>🟢 Sin Problemas/Bajo Nivel</p>
                <h2 style='color: #00AA77; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0; text-shadow: 0 0 10px #00AA77;'>6%</h2>
                <p style='color: #CCCCCC; font-size: 0.85rem; margin: 5px 0;'>De empresas mexicanas</p>
                <p style='color: #AAAAAA; font-size: 0.8rem; margin: 0;'>Operaciones sin presión crítica</p>
            </div>
        """, unsafe_allow_html=True)

    # Gráfico de dificultades
    dificultades_data = pd.DataFrame({
        'Nivel de Dificultad': ['Graves/Muy Graves', 'Moderadas', 'Bajo/Sin Problemas'],
        'Porcentaje': [67, 27, 6],
        'Color': ['#FF3366', '#FFA500', '#00AA77']
    })

    fig_dificultades = px.pie(
        dificultades_data,
        values='Porcentaje',
        names='Nivel de Dificultad',
        color='Nivel de Dificultad',
        color_discrete_map={'Graves/Muy Graves': '#FF3366', 'Moderadas': '#FFA500', 'Bajo/Sin Problemas': '#00AA77'},
        title='Distribución de Empresas por Nivel de Dificultad (IRU 2024)'
    )
    fig_dificultades.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='#FFFFFF', size=12))
    fig_dificultades.update_layout(
        height=400,
        title_font_color='#00D4FF',
        title_font_size=16,
        title_font_family='Inter',
        font=dict(color='#FFFFFF', size=12, family='Inter'),
        plot_bgcolor='#0D1B2A',
        paper_bgcolor='#0D1B2A'
    )
    st.plotly_chart(fig_dificultades, use_container_width=True)

    st.markdown("---")

    # ANÁLISIS DE BRECHA DE EDAD Y PARIDAD DE GÉNERO
    st.markdown("""
        <div style='background: linear-gradient(135deg, #0D1B2A 0%, #1a3a4d 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0 15px 0;
                    border: 1px solid #00D4FF;
                    box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);'>
            <h3 style='color: #00D4FF; margin: 0; font-size: 1.1rem; font-weight: 600; text-shadow: 0 0 10px #00D4FF;'>👥 Análisis Demográfico: Edad y Género</h3>
        </div>
    """, unsafe_allow_html=True)

    col_demo1, col_demo2 = st.columns([1, 1])
    
    with col_demo1:
        st.markdown("""
            <div style='background-color: #0D1B2A; 
                        border-left: 5px solid #00D4FF;
                        border: 1px solid #00D4FF;
                        padding: 20px; 
                        border-radius: 8px;
                        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
                        margin: 10px 0;'>
                <p style='color: #00D4FF; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>🧑 Brecha de Edad</p>
                <h2 style='color: #FFFFFF; font-size: 2rem; font-weight: 700; margin: 10px 0 5px 0; text-shadow: 0 0 10px #00D4FF;'>10.2%</h2>
                <p style='color: #CCCCCC; font-size: 0.85rem; margin: 5px 0;'>Operadores menores de 25 años</p>
                <p style='color: #FF3366; font-size: 0.9rem; font-weight: 600; margin: 10px 0 0 0;'>⚠️ Crisis demográfica en curso</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_demo2:
        st.markdown("""
            <div style='background-color: #0D1B2A; 
                        border-left: 5px solid #FF3366;
                        border: 1px solid #FF3366;
                        padding: 20px; 
                        border-radius: 8px;
                        box-shadow: 0 0 15px rgba(255, 51, 102, 0.2);
                        margin: 10px 0;'>
                <p style='color: #FF3366; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>👩 Paridad de Género</p>
                <h2 style='color: #FFFFFF; font-size: 2rem; font-weight: 700; margin: 10px 0 5px 0; text-shadow: 0 0 10px #FF3366;'>1.9%</h2>
                <p style='color: #CCCCCC; font-size: 0.85rem; margin: 5px 0;'>Operadoras (puestos ocupados)</p>
                <p style='color: #CCCCCC; font-size: 0.85rem; margin: 10px 0 0 0;'>Vs 40.6% mujeres en plantilla general</p>
            </div>
        """, unsafe_allow_html=True)

    # Comparativa de crecimiento de vacantes
    vacantes_historico = pd.DataFrame({
        'Año': [2023, 2024],
        'Vacantes': [56000, 99000],
        'Incremento %': [0, 76.7],
        'Etiqueta': ['56,000<br>vacantes', '99,000<br>vacantes<br>+76.7%']
    })

    fig_vacantes_crec = px.bar(
        vacantes_historico,
        x='Año',
        y='Vacantes',
        color='Vacantes',
        color_continuous_scale=[[0, '#00D4FF'], [1, '#FF3366']],
        labels={'Vacantes': 'Vacantes de Operadores'},
        title='📈 Tendencia de Vacantes: Crecimiento de 76.7% (2023-2024)'
    )
    
    # Añadir anotaciones personalizadas  
    fig_vacantes_crec.add_annotation(
        x=2023, y=56000,
        text='<b>56,000</b><br>vacantes',
        showarrow=False,
        yshift=15,
        font=dict(color='#00D4FF', size=13),
        bgcolor='rgba(0, 212, 255, 0.15)',
        bordercolor='#00D4FF',
        borderwidth=2,
        borderpad=8
    )
    
    fig_vacantes_crec.add_annotation(
        x=2024, y=99000,
        text='<b>99,000</b><br>vacantes<br><b style="color:#FF3366">+76.7%</b>',
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor='#FF3366',
        yshift=20,
        font=dict(color='#FF3366', size=13),
        bgcolor='rgba(255, 51, 102, 0.15)',
        bordercolor='#FF3366',
        borderwidth=2,
        borderpad=8
    )
    
    fig_vacantes_crec.update_layout(
        showlegend=False,
        height=450,
        title_font_color='#00D4FF',
        title_font_size=16,
        title_font_family='Inter',
        font=dict(color='#FFFFFF', size=12, family='Inter'),
        plot_bgcolor='#0D1B2A',
        paper_bgcolor='#0D1B2A',
        yaxis_title='Vacantes de Operadores',
        xaxis=dict(tickmode='linear', tick0=2023, dtick=1),
        yaxis=dict(gridcolor='rgba(0, 212, 255, 0.1)'),
        hovermode='x unified'
    )
    st.plotly_chart(fig_vacantes_crec, use_container_width=True)

    st.markdown("---")

    # PRINCIPAL BARRERAS PARA CONTRATACIÓN
    st.markdown("""
        <div style='background: linear-gradient(135deg, #0D1B2A 0%, #1a3a4d 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0 15px 0;
                    border: 1px solid #00D4FF;
                    box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);'>
            <h3 style='color: #00D4FF; margin: 0; font-size: 1.1rem; font-weight: 600; text-shadow: 0 0 10px #00D4FF;'>🚧 Principales Barreras Identificadas (IRU 2024)</h3>
        </div>
    """, unsafe_allow_html=True)

    barreras = pd.DataFrame({
        'Barrera': [
            'Burocracia / Proceso largo para obtener licencia',
            'Falta de capacidad/disponibilidad de formación',
            'Inseguridad y crimen (robos +16% en 2024)',
            'Brecha demográfica (envejecimiento laboral)',
            'Falta de infraestructura de descanso seguro'
        ],
        'Intensidad': ['Crítica', 'Crítica', 'Muy Alta', 'Muy Alta', 'Alta'],
        'Impacto_Empresas_%': [75, 68, 52, 45, 38]
    })

    col_b1, col_b2 = st.columns([1, 1])
    
    with col_b1:
        fig_barreras = px.bar(
            barreras.sort_values('Impacto_Empresas_%'),
            x='Impacto_Empresas_%',
            y='Barrera',
            orientation='h',
            color='Impacto_Empresas_%',
            color_continuous_scale=[[0, '#00D4FF'], [0.5, '#FFA500'], [1, '#FF3366']],
            text='Impacto_Empresas_%',
            labels={'Impacto_Empresas_%': '% de Empresas Afectadas'},
            title='Impacto de Barreras en Empresas'
        )
        fig_barreras.update_traces(texttemplate='%{text:.0f}%', textposition='outside', textfont=dict(color='#00D4FF', size=12))
        fig_barreras.update_layout(
            showlegend=False,
            height=400,
            title_font_color='#00D4FF',
            title_font_size=14,
            title_font_family='Inter',
            font=dict(color='#FFFFFF', size=12, family='Inter'),
            xaxis_title='% de Empresas Afectadas',
            yaxis_title='',
            plot_bgcolor='#0D1B2A',
            paper_bgcolor='#0D1B2A',
            margin=dict(l=300),
            yaxis=dict(gridcolor='rgba(0, 212, 255, 0.1)')
        )
        st.plotly_chart(fig_barreras, use_container_width=True)
    
    with col_b2:
        st.markdown("""
            <div style='background-color: #0D1B2A; 
                        border-left: 5px solid #00D4FF;
                        border: 1px solid #00D4FF;
                        padding: 20px; 
                        border-radius: 8px;
                        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
                        margin: 10px 0;'>
                <h4 style='color: #00D4FF; margin: 0 0 15px 0; text-shadow: 0 0 10px #00D4FF;'>💡 Recomendaciones IRU 2024</h4>
                <ul style='color: #CCCCCC; font-size: 0.9rem; margin: 0; padding-left: 20px; line-height: 1.8;'>
                    <li><strong style='color: #00D4FF;'>Simplificar trámites:</strong> Agilizar obtención de licencias</li>
                    <li><strong style='color: #00D4FF;'>Capacitación:</strong> Aumentar disponibilidad de formación</li>
                    <li><strong style='color: #00D4FF;'>Seguridad:</strong> Invertir en paraderos seguros y equipados</li>
                    <li><strong style='color: #FF3366;'>Atracción juvenil:</strong> Mejorar atractivo profesional para menores de 25</li>
                    <li><strong style='color: #FF3366;'>Inclusión de género:</strong> Facilitar acceso de mujeres operadoras</li>
                    <li><strong style='color: #00D4FF;'>Educación superior:</strong> Integrar transporte en sistemas educativos</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

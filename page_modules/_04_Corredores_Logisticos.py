"""
Página: Corredores Logísticos
Análisis de corredores logísticos estratégicos con evaluación de riesgo y rentabilidad
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def page_corredores_logisticos():
    """Análisis de corredores logísticos estratégicos con evaluación de riesgo y rentabilidad"""
    
    # Inicializar contadores de keys para evitar duplicados
    if 'chart_counter_corredores' not in st.session_state:
        st.session_state.chart_counter_corredores = 0
    st.session_state.chart_counter_corredores += 1
    chart_id = st.session_state.chart_counter_corredores
    
    # Título con diseño corporativo
    st.markdown("""
        <div style='background: linear-gradient(135deg, #003d7a 0%, #0052a3 100%); 
                    color: white; 
                    padding: 30px 40px; 
                    border-radius: 15px; 
                    margin-bottom: 30px;
                    box-shadow: 0 8px 20px rgba(0, 61, 122, 0.3);'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'>🛣️ Corredores Logísticos Estratégicos</h1>
            <p style='color: #0066cc; font-size: 1.2rem; font-weight: 500; margin-top: 10px; margin-bottom: 0;'>Análisis de rutas críticas, riesgo operativo y rentabilidad</p>
        </div>
    """, unsafe_allow_html=True)
    
    # --- CONFIGURACIÓN DE PUNTOS CLAVE (Coordenadas aproximadas) ---
    puntos = {
        'Manzanillo': [19.05, -104.31],
        'Veracruz': [19.17, -96.13],
        'Lázaro Cárdenas': [17.95, -102.20],
        'Nuevo Laredo': [27.48, -99.50],
        'Tijuana': [32.51, -117.03],
        'Ciudad Juárez': [31.73, -106.48],
        'CDMX': [19.43, -99.13],  # Hub de distribución
        'Ensenada': [31.87, -116.60],
        'Mazatlán': [23.19, -106.42],
        'Matamoros': [25.87, -97.50],
        'Nogales': [31.34, -110.94],
        'Hermosillo': [29.10, -110.97],
        'Querétaro': [20.59, -100.39],
        'San Luis Potosí': [22.15, -100.98],
        'Monterrey': [25.69, -100.32],
        'Tampico': [22.27, -97.86],
        'Salina Cruz': [16.17, -95.18],
        'Coatzacoalcos': [18.13, -94.42],
        'Puebla': [19.04, -98.20],
        'Villahermosa': [17.99, -92.73],
        'Mérida': [20.97, -89.62],
        'Cancún': [21.16, -87.35]
    }
    
    # --- DEFINICIÓN DE CORREDORES ---
    corredores = [
        {"origen": "Manzanillo", "destino": "Nuevo Laredo", "nombre": "Corredor NAFTA Pacífico", "riesgo": "Medio", "rentabilidad": "Alta", "distancia_km": 1850, "tiempo_hrs": 24},
        {"origen": "Veracruz", "destino": "Nuevo Laredo", "nombre": "Corredor del Golfo", "riesgo": "Bajo", "rentabilidad": "Media", "distancia_km": 1100, "tiempo_hrs": 15},
        {"origen": "Manzanillo", "destino": "CDMX", "nombre": "Corredor Centro-Occidente", "riesgo": "Muy Alto", "rentabilidad": "Media", "distancia_km": 750, "tiempo_hrs": 10},
        {"origen": "Lázaro Cárdenas", "destino": "Nuevo Laredo", "nombre": "Corredor Intermodal", "riesgo": "Alto", "rentabilidad": "Alta", "distancia_km": 1650, "tiempo_hrs": 22},
        {"origen": "CDMX", "destino": "Tijuana", "nombre": "Corredor Noroeste", "riesgo": "Bajo", "rentabilidad": "Alta", "distancia_km": 2650, "tiempo_hrs": 35},
        {"origen": "Ensenada", "destino": "Nuevo Laredo", "nombre": "Corredor Frontera Norte", "riesgo": "Medio", "rentabilidad": "Alta", "distancia_km": 2100, "tiempo_hrs": 28},
        # --- NUEVOS CORREDORES ESTRATÉGICOS 2026 ---
        {"origen": "Mazatlán", "destino": "Matamoros", "nombre": "🔄 Corredor Transversal (Eje del Nearshoring)", "riesgo": "Alto", "rentabilidad": "Alta", "distancia_km": 1600, "tiempo_hrs": 24},
        {"origen": "CDMX", "destino": "Nogales", "nombre": "📦 Corredor del Pacífico (Exportaciones Agrícolas)", "riesgo": "Medio", "rentabilidad": "Alta", "distancia_km": 2400, "tiempo_hrs": 32},
        {"origen": "CDMX", "destino": "Nuevo Laredo", "nombre": "⭐ Corredor NAFTA Central (40% del comercio)", "riesgo": "Bajo", "rentabilidad": "Alta", "distancia_km": 1050, "tiempo_hrs": 14},
        {"origen": "Veracruz", "destino": "Monterrey", "nombre": "🌊 Corredor del Golfo (Puertos-Industria Noreste)", "riesgo": "Medio", "rentabilidad": "Media", "distancia_km": 950, "tiempo_hrs": 12},
        {"origen": "Salina Cruz", "destino": "Coatzacoalcos", "nombre": "🌉 Corredor Interoceánico (Istmo de Tehuantepec)", "riesgo": "Bajo", "rentabilidad": "Media", "distancia_km": 310, "tiempo_hrs": 6},
        {"origen": "CDMX", "destino": "Cancún", "nombre": "🏖️ Corredor Peninsular (Turismo y Petróleo)", "riesgo": "Bajo", "rentabilidad": "Media", "distancia_km": 1800, "tiempo_hrs": 24}
    ]
    
    df_corr = pd.DataFrame(corredores)
    
    # Calcular métricas
    total_corredores = len(df_corr)
    corredores_bajo_riesgo = len(df_corr[df_corr['riesgo'] == 'Bajo'])
    corredores_alta_rentabilidad = len(df_corr[df_corr['rentabilidad'] == 'Alta'])
    distancia_promedio = df_corr['distancia_km'].mean()
    
    # ============ MÉTRICAS PRINCIPALES ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #003d7a 0%, #0052a3 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(0, 61, 122, 0.2);
                    border: 1px solid #0066cc;'>
            <h3 style='color: #0066cc; margin: 0; font-size: 1.3rem; font-weight: 600;'>📊 Resumen Ejecutivo de Corredores</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
            <div style='background-color: rgba(0, 102, 204, 0.15); 
                        border-left: 5px solid #0066cc;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0, 102, 204, 0.1);
                        margin: 10px 0;'>
                <p style='color: #0066cc; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Total Corredores</p>
                <h2 style='color: #FFFFFF; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{total_corredores}</h2>
                <p style='color: #AAA; font-size: 0.85rem; margin: 0;'>🛣️ Rutas estratégicas</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
            <div style='background-color: rgba(79, 211, 143, 0.15); 
                        border-left: 5px solid #4FD38F;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(79, 211, 143, 0.1);
                        margin: 10px 0;'>
                <p style='color: #4FD38F; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Bajo Riesgo</p>
                <h2 style='color: #FFFFFF; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{corredores_bajo_riesgo}</h2>
                <p style='color: #AAA; font-size: 0.85rem; margin: 0;'>✅ Rutas seguras</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
            <div style='background-color: rgba(25, 118, 210, 0.15); 
                        border-left: 5px solid #1976d2;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(25, 118, 210, 0.1);
                        margin: 10px 0;'>
                <p style='color: #1976d2; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Alta Rentabilidad</p>
                <h2 style='color: #1976d2; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{corredores_alta_rentabilidad}</h2>
                <p style='color: #AAA; font-size: 0.85rem; margin: 0;'>💰 Rutas premium</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""
            <div style='background-color: rgba(0, 82, 163, 0.15); 
                        border-left: 5px solid #0052a3;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0, 82, 163, 0.1);
                        margin: 10px 0;'>
                <p style='color: #0052a3; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Distancia Promedio</p>
                <h2 style='color: #FFFFFF; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{distancia_promedio:,.0f}</h2>
                <p style='color: #AAA; font-size: 0.85rem; margin: 0;'>📏 Kilómetros</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ DEFINICIÓN DE ELEMENTOS (Para usar en expandibles) ============
    puertos_lista = ['Manzanillo', 'Veracruz', 'Lázaro Cárdenas', 'Ensenada', 'Salina Cruz', 'Coatzacoalcos']
    fronteras_lista = ['Nuevo Laredo', 'Tijuana', 'Ciudad Juárez', 'Nogales', 'Matamoros']
    hubs_lista = ['CDMX', 'Monterrey']
    
    # ============ INFORMACIÓN EXPANDIBLE ============
    with st.expander("📋 Catálogo de Nodos (Puertos, Fronteras, Hubs)", expanded=False):
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            st.markdown("**⚓ Puertos Marítimos:**")
            for puerto in puertos_lista:
                st.caption(f"🔵 {puerto}")
        
        with col_info2:
            st.markdown("**🚛 Cruces Fronterizos:**")
            for frontera in fronteras_lista:
                st.caption(f"🔴 {frontera}")
        
        with col_info3:
            st.markdown("**🏢 Hubs Principales:**")
            for hub in hubs_lista:
                st.caption(f"🔷 {hub}")
    
    # ============ MAPA DE RUTAS ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #003d7a 0%, #0052a3 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(0, 61, 122, 0.2);
                    border: 1px solid #0066cc;'>
            <h3 style='color: #0066cc; margin: 0; font-size: 1.3rem; font-weight: 600;'>🗺️ Mapa Interactivo de Corredores</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # ============ CONTROLES DEL MAPA (CREADOS ANTES DE DIBUJAR) ============
    st.markdown("""
        <p style='color: #AAA; font-size: 0.9rem; margin: 15px 0 10px 0;'><b>📍 Filtros de Visualización:</b></p>
    """, unsafe_allow_html=True)
    
    col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)
    
    with col_filter1:
        show_corredores = st.checkbox("Corredores", value=True, key=f'filter_corredores_{chart_id}')
    with col_filter2:
        show_puertos = st.checkbox("Puertos Marítimos", value=True, key=f'filter_puertos_{chart_id}')
    with col_filter3:
        show_fronteras = st.checkbox("Fronteras", value=True, key=f'filter_fronteras_{chart_id}')
    with col_filter4:
        show_hubs = st.checkbox("Hubs & Ciudades", value=True, key=f'filter_hubs_{chart_id}')
    
    st.markdown("<p style='color: #AAA; font-size: 0.85rem;'><b>💡 Tip:</b> Usa los filtros arriba para mostrar/ocultar categorías. La leyenda está al pie del mapa. Pasea el mouse sobre las rutas para más detalles.</p>", unsafe_allow_html=True)
    
    # 1. MAPA DE RUTAS - ESTILO SICT
    fig = go.Figure()
    
    # Clasificación de corredores (Longitudinales vs Transversales)
    corredores_longitudinales = {
        'Transpeninsular de B.C.', 'México - Nogales', 'Querétaro - Cd. Juárez',
        'México - Nuevo Laredo', 'Veracruz - Monterrey', 'Puebla - Oaxaca',
        'México - Puebla'
    }
    
    # Mapeo de colores por nivel de riesgo (Vibrantes para fondo oscuro)
    color_riesgo = {
        'Bajo': '#4FD38F',      # Verde vibrante
        'Medio': '#FFA500',     # Naranja vibrante
        'Alto': '#FF6B6B',      # Rojo vibrante
        'Muy Alto': '#FF1744'   # Rojo oscuro vibrante
    }
    
    # Clasificar puntos
    ciudades_secundarias = ['Guadalajara', 'Querétaro', 'Puebla', 'Hermosillo']
    
    # Coordenadas adicionales para ciudades secundarias
    puntos['Guadalajara'] = [20.66, -103.39]
    puntos['Culiacán'] = [24.80, -107.39]
    puntos['Reynosa'] = [26.10, -97.49]
    
    # Paleta de colores para cada corredor (más vibrante)
    colores_corredores = [
        '#00BFD6',    # Cyan brillante - Corredor 1
        '#58D9F5',    # Cyan claro - Corredor 2
        '#00D9FF',    # Cyan neon - Corredor 3
        '#00E5FF',    # Cyan ultra - Corredor 4
        '#1EE0C6',    # Turquesa - Corredor 5
        '#26ECC1',    # Turquesa claro - Corredor 6
        '#00FFCC',    # Verde cyan - Corredor 7
        '#FF006E',    # Rosa magenta - Corredor 8
        '#FF7B9C',    # Rosa claro - Corredor 9
        '#FFBE0B',    # Amarillo oro - Corredor 10
        '#FB5607',    # Naranja - Corredor 11
        '#8338EC'     # Púrpura - Corredor 12
    ]
    
    # Dibujar las rutas (Líneas) con estilos mejorados - SOLO SI SHOW_CORREDORES
    if show_corredores:
        for idx, ruta in enumerate(corredores):
            color = color_riesgo.get(ruta['riesgo'], '#4070F4')
            # Usar color único si disponible
            if idx < len(colores_corredores):
                color_unico = colores_corredores[idx]
            else:
                color_unico = color
            
            # Calcular punto medio para mostrar información
            mid_lat = (puntos[ruta['origen']][0] + puntos[ruta['destino']][0]) / 2
            mid_lon = (puntos[ruta['origen']][1] + puntos[ruta['destino']][1]) / 2
            
            # Línea de ruta: MÁS DELGADA pero más vibrante
            line_width = 4 if ruta['rentabilidad'] == 'Alta' else 3 if ruta['rentabilidad'] == 'Media' else 2.5
            
            # Diferenciación visual: usar opacidad y dash para transversales vs longitudinales
            is_transversal = ruta['nombre'].startswith('🔄') or ruta['nombre'].startswith('📦')
            dash_style = 'solid' if ruta['rentabilidad'] == 'Alta' else 'dash' if is_transversal else 'dot'
            opacity_val = 0.95 if ruta['rentabilidad'] == 'Alta' else 0.75 if ruta['rentabilidad'] == 'Media' else 0.6
            
            fig.add_trace(go.Scattergeo(
                locationmode = 'ISO-3',
                lon = [puntos[ruta['origen']][1], puntos[ruta['destino']][1]],
                lat = [puntos[ruta['origen']][0], puntos[ruta['destino']][0]],
                mode = 'lines',
                line = dict(
                    width = line_width, 
                    color = color_unico,
                    dash = dash_style
                ),
                opacity=opacity_val,
                name = f"{ruta['nombre']}",
                hoverinfo='skip',
                showlegend=False
            ))
            
            # SOMBRA del corredor (efecto de profundidad)
            fig.add_trace(go.Scattergeo(
                locationmode = 'ISO-3',
                lon = [puntos[ruta['origen']][1], puntos[ruta['destino']][1]],
                lat = [puntos[ruta['origen']][0], puntos[ruta['destino']][0]],
                mode = 'lines',
                line = dict(
                    width = line_width + 2, 
                    color = color_unico,
                    dash = dash_style
                ),
                opacity=0.15,
                hoverinfo='skip',
                showlegend=False
            ))
            
            # Número del corredor en posición media
            num_corredor = idx + 1
            fig.add_trace(go.Scattergeo(
                locationmode = 'ISO-3',
                lon = [mid_lon],
                lat = [mid_lat],
                mode = 'text',
                text = [f"<b>{num_corredor}</b>"],
                textposition = 'middle center',
                textfont = dict(size=13, color='white', family='Arial', weight='bold'),
                hoverinfo='skip',
                showlegend=False
            ))
            
            # Punto medio con información (invisible pero con hover)
            fig.add_trace(go.Scattergeo(
                locationmode = 'ISO-3',
                lon = [mid_lon],
                lat = [mid_lat],
                mode = 'markers',
                marker = dict(
                    size = 14,
                    color = color,
                    symbol = 'circle',
                    opacity = 0.7,
                    line = dict(width=2, color='white')
                ),
                name = f"{ruta['nombre']}",
                text = [f"{ruta['distancia_km']} km"],
                hovertemplate = f"<b>#{num_corredor} - {ruta['nombre']}</b><br>" +
                               f"━━━━━━━━━━━━━━━━<br>" +
                               f"📍 Origen: <b>{ruta['origen']}</b><br>" +
                               f"🎯 Destino: <b>{ruta['destino']}</b><br>" +
                               f"━━━━━━━━━━━━━━━━<br>" +
                               f"🚨 Nivel de Riesgo: <b>{ruta['riesgo']}</b><br>" +
                               f"💰 Rentabilidad: <b>{ruta['rentabilidad']}</b><br>" +
                               f"━━━━━━━━━━━━━━━━<br>" +
                               f"📏 Distancia: <b>{ruta['distancia_km']:,} km</b><br>" +
                               f"⏱️ Tiempo Estimado: <b>{ruta['tiempo_hrs']} hrs</b><br>" +
                               f"🚚 Velocidad Prom: <b>{ruta['distancia_km']/ruta['tiempo_hrs']:.0f} km/h</b><br>" +
                               "<extra></extra>",
                showlegend=True
            ))
    
    # ==================== MARCADORES DE CIUDADES ====================
    
    # Agregar marcadores de PUERTOS (Símbolos de círculo) - SOLO SI SHOW_PUERTOS
    if show_puertos:
        for puerto in puertos_lista:
            if puerto in puntos:
                fig.add_trace(go.Scattergeo(
                    locationmode = 'ISO-3',
                    lon = [puntos[puerto][1]],
                    lat = [puntos[puerto][0]],
                    mode = 'markers+text',
                    marker = dict(
                        size = 20,
                        color = '#1E88E5',  # Azul vibrante
                        symbol = 'circle',
                        line = dict(width=3, color='#29B5E8')  # Cyan border
                    ),
                    text = [puerto],
                    textposition = 'top center',
                    textfont = dict(size=9, color='#FFFFFF', family='Arial', weight='bold'),
                    name = f"⚓ {puerto}",
                    hovertemplate = f"<b>⚓ PUERTO MARÍTIMO</b><br>" +
                                   f"<b>{puerto}</b><br>" +
                                   f"━━━━━━━━━━━━━━━━<br>" +
                                   f"Tipo: Puerto de altura<br>" +
                                   f"Coordenadas: {puntos[puerto][0]:.2f}°N, {puntos[puerto][1]:.2f}°W<br>" +
                                   "<extra></extra>",
                    showlegend=True
                ))
    
    # Agregar marcadores de FRONTERAS (Símbolos de cuadrado) - SOLO SI SHOW_FRONTERAS
    if show_fronteras:
        for frontera in fronteras_lista:
            if frontera in puntos:
                fig.add_trace(go.Scattergeo(
                    locationmode = 'ISO-3',
                    lon = [puntos[frontera][1]],
                    lat = [puntos[frontera][0]],
                    mode = 'markers+text',
                    marker = dict(
                        size = 20,
                        color = '#FF6B6B',  # Rojo vibrante
                        symbol = 'square',
                        line = dict(width=3, color='#FF9999')  # Rojo claro border
                    ),
                    text = [frontera],
                    textposition = 'top center',
                    textfont = dict(size=9, color='#FFFFFF', family='Arial', weight='bold'),
                    name = f"🚛 {frontera}",
                    hovertemplate = f"<b>🚛 CRUCE FRONTERIZO</b><br>" +
                                   f"<b>{frontera}</b><br>" +
                                   f"━━━━━━━━━━━━━━━━<br>" +
                                   f"Tipo: Aduana fronteriza<br>" +
                                   f"Coordenadas: {puntos[frontera][0]:.2f}°N, {puntos[frontera][1]:.2f}°W<br>" +
                                   "<extra></extra>",
                    showlegend=True
                ))
    
    # Agregar marcadores de HUBS DE DISTRIBUCIÓN (Símbolo de diamante) - SOLO SI SHOW_HUBS
    if show_hubs:
        for hub in hubs_lista:
            if hub in puntos:
                fig.add_trace(go.Scattergeo(
                    locationmode = 'ISO-3',
                    lon = [puntos[hub][1]],
                    lat = [puntos[hub][0]],
                    mode = 'markers+text',
                    marker = dict(
                        size = 22,
                        color = '#29B5E8',  # Cyan vibrante
                        symbol = 'diamond',
                        line = dict(width=3, color='#58D9F5')  # Cyan claro border
                    ),
                    text = [hub],
                    textposition = 'top center',
                    textfont = dict(size=10, color='#000000', family='Arial', weight='bold'),
                    name = f"🏢 {hub}",
                    hovertemplate = f"<b>🏢 HUB DE DISTRIBUCIÓN PRINCIPAL</b><br>" +
                                   f"<b>{hub}</b><br>" +
                                   f"━━━━━━━━━━━━━━━━<br>" +
                                   f"Tipo: Centro de distribución estratégico<br>" +
                                   f"Coordenadas: {puntos[hub][0]:.2f}°N, {puntos[hub][1]:.2f}°W<br>" +
                                   "<extra></extra>",
                    showlegend=True
                ))
    
    # Agregar marcadores de CIUDADES SECUNDARIAS (Símbolos pequeños sin texto)
    for ciudad in ciudades_secundarias:
        if ciudad in puntos:
            fig.add_trace(go.Scattergeo(
                locationmode = 'ISO-3',
                lon = [puntos[ciudad][1]],
                lat = [puntos[ciudad][0]],
                mode = 'markers',
                marker = dict(
                    size = 10,
                    color = '#64B5F6',  # Azul claro
                    symbol = 'circle',
                    opacity = 0.8,
                    line = dict(width=1, color='#29B5E8')
                ),
                name = f"🏙️ {ciudad}",
                hovertemplate = f"<b>🏙️ CIUDAD</b><br>" +
                               f"<b>{ciudad}</b><br>" +
                               f"━━━━━━━━━━━━━━━━<br>" +
                               f"Nodo secundario de distribución<br>" +
                               f"Coordenadas: {puntos[ciudad][0]:.2f}°N, {puntos[ciudad][1]:.2f}°W<br>" +
                               "<extra></extra>",
                showlegend=False
            ))
    
    fig.update_layout(
        geo = dict(
            scope = 'north america',
            projection_type = 'mercator',
            center = dict(lat=23.6, lon=-102.5),  # Centrado en México
            showland = True,
            landcolor = "rgb(50, 70, 100)",  # Azul oscuro para tierra
            coastlinecolor = "rgb(100, 200, 255)",  # Cyan vibrante
            coastlinewidth = 2,
            showlakes = True,
            lakecolor = "rgb(40, 60, 100)",  # Azul oscuro para lagos
            showrivers = True,
            rivercolor = "rgb(80, 180, 255)",  # Azul claro para ríos
            riverwidth = 1,
            showcountries = True,
            countrycolor = "rgb(100, 150, 200)",  # Azul medio para países
            countrywidth = 1.5,
            showsubunits = True,
            subunitcolor = "rgb(70, 110, 160)",  # Azul oscuro para subdivisiones
            subunitwidth = 0.8,
            lataxis = dict(range = [14.5, 32.7]),
            lonaxis = dict(range = [-117.5, -86.5]),
            bgcolor = 'rgba(20, 35, 60, 1)',  # Azul muy oscuro (casi negro)
            resolution = 50
        ),
        margin={"r":20,"t":20,"l":20,"b":120},  # Aumentar bottom para leyenda
        height=750,
        showlegend=True,
        legend=dict(
            bgcolor='rgba(30, 45, 75, 0.95)',  # Fondo oscuro
            bordercolor='#29B5E8',  # Cyan
            borderwidth=2,
            x=0.5,
            y=-0.12,
            xanchor='center',
            yanchor='top',
            orientation='h',  # HORIZONTAL
            font=dict(size=9, color='#FFFFFF', family='Arial', weight='bold'),  # Texto blanco
            traceorder='normal',
            itemsizing='constant'
        ),
        font=dict(color='#FFFFFF', family='Arial'),  # Texto blanco
        hoverlabel=dict(
            bgcolor="rgba(30, 45, 75, 0.98)",  # Fondo oscuro
            font_size=12,
            font_family="Arial",
            font_color="#FFFFFF",  # Texto blanco
            bordercolor="#29B5E8"  # Border cyan
        ),
        paper_bgcolor='rgba(15, 25, 45, 1)'  # Fondo muy oscuro
    )
    
    # ============ APLICAR FILTROS DE VISIBILIDAD ANTES DE RENDERIZAR ============
    for i, trace in enumerate(fig.data):
        visible = True
        
        if trace.name:
            # CORREDORES: Tienen emojis como 🔄, 📦, ⭐, 🌊, 🌉, 🏖️
            if any(emoji in trace.name for emoji in ['🔄', '📦', '⭐', '🌊', '🌉', '🏖️']):
                if not show_corredores:
                    visible = False
            # NÚMEROS DE CORREDOR: <b>1</b>, <b>2</b>, etc.
            elif trace.name.startswith('<b>') and trace.name.endswith('</b>'):
                if not show_corredores:
                    visible = False
            # PUERTOS: Tienen ⚓
            elif '⚓' in trace.name:
                if not show_puertos:
                    visible = False
            # FRONTERAS: Tienen 🚛
            elif '🚛' in trace.name:
                if not show_fronteras:
                    visible = False
            # HUBS & CIUDADES: Tienen 🏢 o 🏙️
            elif '🏢' in trace.name or '🏙️' in trace.name:
                if not show_hubs:
                    visible = False
        
        fig.data[i].visible = visible
    
    st.plotly_chart(fig, use_container_width=True, config={'responsive': True}, key=f'mapa_corredores_{chart_id}')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ MATRIZ DE DECISIÓN ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>📊 Matriz de Decisión de Corredores</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h4 style='color: #11101D; font-weight: 600;'>Análisis Comparativo</h4>", unsafe_allow_html=True)
    
    # Formato de tabla
    def color_riesgo_tabla(val):
        if val == 'Muy Alto':
            return 'background-color: #FFEBEE; color: #D32F2F; font-weight: 600;'
        elif val == 'Alto':
            return 'background-color: #FFF3E0; color: #EF553B; font-weight: 600;'
        elif val == 'Medio':
            return 'background-color: #FFF8E1; color: #FFA726; font-weight: 600;'
        else:
            return 'background-color: #E8F5E9; color: #4CAF50; font-weight: 600;'
    
    def color_rentabilidad(val):
        if val == 'Alta':
            return 'background-color: #E8F5E9; color: #4CAF50; font-weight: 600;'
        elif val == 'Media':
            return 'background-color: #FFF8E1; color: #FFA726; font-weight: 600;'
        else:
            return 'background-color: #FFEBEE; color: #EF553B; font-weight: 600;'
    
    df_display = df_corr[['nombre', 'origen', 'destino', 'distancia_km', 'tiempo_hrs', 'riesgo', 'rentabilidad']].copy()
    df_display.columns = ['Corredor', 'Origen', 'Destino', 'Distancia (km)', 'Tiempo (hrs)', 'Riesgo', 'Rentabilidad']
    
    # Eliminar filas vacías
    df_display = df_display.dropna(how='all')
    df_display = df_display[df_display['Corredor'].notna()]
    
    styled_df = df_display.style.format({
        'Distancia (km)': '{:,.0f}',
        'Tiempo (hrs)': '{:.0f}'
    }).map(color_riesgo_tabla, subset=['Riesgo']).map(color_rentabilidad, subset=['Rentabilidad'])
    
    st.dataframe(styled_df, use_container_width=True, height=350)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ ANÁLISIS DE RENTABILIDAD VS RIESGO ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4070F4 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(64, 112, 244, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>📈 Análisis de Eficiencia</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_an1, col_an2 = st.columns(2)
    
    with col_an1:
        st.markdown("<h4 style='color: #11101D; font-weight: 600;'>Distancia vs Tiempo de Tránsito</h4>", unsafe_allow_html=True)
        
        fig_scatter = px.scatter(
            df_corr,
            x='distancia_km',
            y='tiempo_hrs',
            color='riesgo',
            size='distancia_km',
            hover_name='nombre',
            color_discrete_map=color_riesgo,
            labels={'distancia_km': 'Distancia (km)', 'tiempo_hrs': 'Tiempo (hrs)'}
        )
        fig_scatter.update_layout(
            height=350,
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_scatter, use_container_width=True, config={'responsive': True}, key=f'scatter_distancia_tiempo_{chart_id}')
    
    with col_an2:
        st.markdown("<h4 style='color: #11101D; font-weight: 600;'>Rentabilidad por Corredor</h4>", unsafe_allow_html=True)
        
        # Asignar valores numéricos a rentabilidad
        df_corr['rent_num'] = df_corr['rentabilidad'].map({'Alta': 3, 'Media': 2, 'Baja': 1})
        
        fig_bar = px.bar(
            df_corr.sort_values('rent_num', ascending=True),
            y='nombre',
            x='rent_num',
            orientation='h',
            color='rentabilidad',
            color_discrete_map={'Alta': '#4CAF50', 'Media': '#FFA726', 'Baja': '#EF553B'},
            labels={'rent_num': 'Nivel de Rentabilidad', 'nombre': ''}
        )
        fig_bar.update_layout(
            height=350,
            showlegend=False,
            font=dict(color='#11101D', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(tickvals=[1, 2, 3], ticktext=['Baja', 'Media', 'Alta'])
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'responsive': True}, key=f'bar_rentabilidad_{chart_id}')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ RECOMENDACIONES ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #FFA726 0%, #EF553B 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(239, 85, 59, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>💡 Recomendaciones Estratégicas</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_rec1, col_rec2 = st.columns(2)
    
    # Identificar mejores corredores
    mejor_bajo_riesgo = df_corr[(df_corr['riesgo'] == 'Bajo') & (df_corr['rentabilidad'] == 'Alta')]
    mejor_rentabilidad = df_corr[df_corr['rentabilidad'] == 'Alta'].sort_values('distancia_km').iloc[0] if len(df_corr[df_corr['rentabilidad'] == 'Alta']) > 0 else None
    
    with col_rec1:
        if not mejor_bajo_riesgo.empty:
            corredor = mejor_bajo_riesgo.iloc[0]
            st.markdown(f"""
                <div style='background-color: #E8F5E9; 
                            border-left: 4px solid #4CAF50;
                            padding: 20px; 
                            border-radius: 10px;
                            margin: 10px 0;'>
                    <h4 style='color: #11101D; margin-top: 0; font-weight: 600;'>✅ Corredor Óptimo</h4>
                    <p style='color: #333; line-height: 1.6; margin-bottom: 10px;'>
                        <strong>{corredor['nombre']}</strong><br>
                        Combina bajo riesgo con alta rentabilidad. Ideal para cargas de alto valor.
                    </p>
                    <p style='color: #666; font-size: 0.9rem; margin: 0;'>
                        📍 {corredor['origen']} → {corredor['destino']}<br>
                        🚛 {corredor['distancia_km']:,.0f} km | ⏱️ {corredor['tiempo_hrs']} hrs
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    with col_rec2:
        if mejor_rentabilidad is not None:
            st.markdown(f"""
                <div style='background-color: #FFF8E1; 
                            border-left: 4px solid #FFA726;
                            padding: 20px; 
                            border-radius: 10px;
                            margin: 10px 0;'>
                    <h4 style='color: #11101D; margin-top: 0; font-weight: 600;'>💰 Más Rentable</h4>
                    <p style='color: #333; line-height: 1.6; margin-bottom: 10px;'>
                        <strong>{mejor_rentabilidad['nombre']}</strong><br>
                        Ruta de alta rentabilidad con la menor distancia. Optimiza costos operativos.
                    </p>
                    <p style='color: #666; font-size: 0.9rem; margin: 0;'>
                        📍 {mejor_rentabilidad['origen']} → {mejor_rentabilidad['destino']}<br>
                        🚛 {mejor_rentabilidad['distancia_km']:,.0f} km | ⏱️ {mejor_rentabilidad['tiempo_hrs']} hrs
                    </p>
                </div>
            """, unsafe_allow_html=True)

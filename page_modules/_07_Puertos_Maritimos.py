"""
Página: Puertos Marítimos de México
Análisis de puertos principales y estratégicos
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime


def page_puertos_maritimos():
    """Página de Puertos Marítimos de México"""
    
    # ============ HEADER PRINCIPAL ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #003d7a 0%, #0052a3 100%); 
                    color: white; 
                    padding: 50px 60px; 
                    border-radius: 20px; 
                    margin-bottom: 40px;
                    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
                    border: 2px solid #0066cc;'>
            <h1 style='color: #FFFFFF; margin: 0; font-size: 3.5rem; font-weight: 800; letter-spacing: -1px;'>⚓ Puertos Marítimos de México</h1>
            <p style='color: #f0f7ff; font-size: 1.25rem; font-weight: 600; margin: 20px 0 0 0; line-height: 1.4;'>
                Análisis de 16 puertos principales administrados por las ASIPONA
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # ============ DESCRIPCIÓN GENERAL ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0, 102, 204, 0.15) 0%, rgba(25, 118, 210, 0.08) 100%); 
                    padding: 35px 40px; 
                    border-radius: 15px; 
                    border-left: 6px solid #0066cc;
                    margin-bottom: 50px;'>
            <p style='color: #003d7a; font-size: 1.05rem; margin: 0; line-height: 1.8; font-weight: 500;'>
                México cuenta con <strong>117 puertos y terminales</strong>, pero la actividad comercial de altura se concentra en 
                <strong>16 puertos principales</strong>. Estos puertos son estratégicos para el comercio internacional, 
                conectando a México con Asia, Europa, Sudamérica y Estados Unidos.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # ============ DATOS DE PUERTOS ============
    puertos_data = {
        'Litoral del Pacífico': [
            {
                'nombre': 'Manzanillo',
                'estado': 'Colima',
                'descripcion': 'Puerto #1 en movimiento de contenedores (TEUs). Puerta principal de mercancías desde China y Japón.',
                'especialidad': 'Contenedores, Asia-Pacífico',
                'teu_anual': 4100000,
                'emoji': '🏅'
            },
            {
                'nombre': 'Lázaro Cárdenas',
                'estado': 'Michoacán',
                'descripcion': 'Segundo puerto más importante. Mayor profundidad, capacidad para buques Post-Panamax.',
                'especialidad': 'Graneles, Contenedores Premium',
                'teu_anual': 2850000,
                'emoji': '⛴️'
            },
            {
                'nombre': 'Ensenada',
                'estado': 'Baja California',
                'descripcion': 'Estratégico para flujo de mercancías hacia California. Reducción de tiempos de tránsito.',
                'especialidad': 'Contenedores, Mercado USA',
                'teu_anual': 1200000,
                'emoji': '🚢'
            },
            {
                'nombre': 'Mazatlán',
                'estado': 'Sinaloa',
                'descripcion': 'Puerto clave para industria automotriz y turismo. Transbordadores internacionales.',
                'especialidad': 'Automotriz, Turismo',
                'teu_anual': 680000,
                'emoji': '🚗'
            },
            {
                'nombre': 'Guaymas',
                'estado': 'Sonora',
                'descripcion': 'Especializado en graneles minerales y productos agrícolas. Conexión noroeste.',
                'especialidad': 'Graneles, Minería',
                'teu_anual': 450000,
                'emoji': '⛏️'
            },
            {
                'nombre': 'Puerto Chiapas',
                'estado': 'Chiapas',
                'descripcion': 'Nodo logístico para comercio con Centroamérica. Puerta sur estratégica.',
                'especialidad': 'Centroamérica, Diverso',
                'teu_anual': 380000,
                'emoji': '🌉'
            },
            {
                'nombre': 'Salina Cruz',
                'estado': 'Oaxaca',
                'descripcion': 'Punto clave del Corredor Interoceánico del Istmo de Tehuantepec. Futuro estratégico.',
                'especialidad': 'Interoceánico, Estratégico',
                'teu_anual': 520000,
                'emoji': '🔗'
            },
            {
                'nombre': 'Topolobampo',
                'estado': 'Sinaloa',
                'descripcion': 'Manejo de hidrocarburos y graneles. Conexión crítica para noroeste mexicano.',
                'especialidad': 'Hidrocarburos, Graneles',
                'teu_anual': 280000,
                'emoji': '⛽'
            }
        ],
        'Litoral del Golfo y Caribe': [
            {
                'nombre': 'Veracruz',
                'estado': 'Veracruz',
                'descripcion': 'Puerto histórico más importante. Líder en vehículos y graneles agrícolas.',
                'especialidad': 'Vehículos, Agrícola',
                'teu_anual': 3200000,
                'emoji': '🏆'
            },
            {
                'nombre': 'Altamira',
                'estado': 'Tamaulipas',
                'descripcion': 'Especializado en fluidos, petroquímica e industria. Hub del noreste mexicano.',
                'especialidad': 'Petroquímica, Fluidos',
                'teu_anual': 1800000,
                'emoji': '🏭'
            },
            {
                'nombre': 'Tampico',
                'estado': 'Tamaulipas',
                'descripcion': 'Importante para acero y carga general. Nodo industrial complementario.',
                'especialidad': 'Acero, Carga General',
                'teu_anual': 920000,
                'emoji': '🏗️'
            },
            {
                'nombre': 'Coatzacoalcos',
                'estado': 'Veracruz',
                'descripcion': 'Segundo punto del Corredor Interoceánico. Especializado en químicos e industriales.',
                'especialidad': 'Químicos, Interoceánico',
                'teu_anual': 1100000,
                'emoji': '🧪'
            },
            {
                'nombre': 'Progreso',
                'estado': 'Yucatán',
                'descripcion': 'Puerta de entrada península yucateca. Contenedores, turismo de cruceros.',
                'especialidad': 'Turismo, Península',
                'teu_anual': 640000,
                'emoji': '⛱️'
            },
            {
                'nombre': 'Dos Bocas',
                'estado': 'Tabasco',
                'descripcion': 'Puerto eminentemente petrolero e industrial. Pivote energético nacional.',
                'especialidad': 'Petróleo, Energía',
                'teu_anual': 380000,
                'emoji': '🛢️'
            },
            {
                'nombre': 'Tuxpan',
                'estado': 'Veracruz',
                'descripcion': 'Puerto más cercano a CDMX. Clave para importación de combustibles.',
                'especialidad': 'Combustibles, CDMX',
                'teu_anual': 850000,
                'emoji': '🚆'
            },
            {
                'nombre': 'Puerto Morelos',
                'estado': 'Quintana Roo',
                'descripcion': 'Manejo de suministros para zona turística del Caribe. Logística hotelera.',
                'especialidad': 'Turismo, Caribe',
                'teu_anual': 320000,
                'emoji': '🏨'
            }
        ]
    }
    
    # ============ TABS PRINCIPALES ============
    tab1, tab2, tab3 = st.tabs([
        "🌊 Litoral del Pacífico",
        "⛵ Literales Golfo & Caribe",
        "📊 Análisis Comparativo"
    ])
    
    # ============ TAB 1: PACÍFICO ============
    with tab1:
        st.markdown("### 🌊 Puertos Estratégicos del Pacífico (Asia-Sudamérica)")
        st.markdown("**Conexión directa con Asia, Sudamérica y mercado estadounidense del Pacífico**")
        
        for puerto in puertos_data['Litoral del Pacífico']:
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"<h3 style='font-size: 3rem; margin: 0;'>{puerto['emoji']}</h3>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, rgba(100, 180, 255, 0.15) 0%, rgba(150, 200, 255, 0.08) 100%); 
                                padding: 20px; 
                                border-radius: 12px; 
                                border-left: 5px solid #4A7C9E;'>
                        <h4 style='color: #1F4E78; margin: 0 0 5px 0; font-size: 1.3rem;'>{puerto['nombre']} - {puerto['estado']}</h4>
                        <p style='color: #555; margin: 10px 0 0 0; font-size: 0.95rem; line-height: 1.6;'>
                            <strong>📍</strong> {puerto['descripcion']}
                        </p>
                        <p style='color: #666; margin: 8px 0 0 0; font-size: 0.9rem;'>
                            <strong style='color: #2C5AA0;'>{puerto['especialidad']}</strong> | 
                            Movimiento: <strong>{puerto['teu_anual']:,} TEU/año</strong>
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("")
    
    # ============ TAB 2: GOLFO Y CARIBE ============
    with tab2:
        st.markdown("### ⛵ Puertos Golfo & Caribe (USA-Europa)")
        st.markdown("**Conexión directa con EE.UU., Europa y Centroamérica**")
        
        for puerto in puertos_data['Litoral del Golfo y Caribe']:
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"<h3 style='font-size: 3rem; margin: 0;'>{puerto['emoji']}</h3>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(100, 200, 100, 0.08) 100%); 
                                padding: 20px; 
                                border-radius: 12px; 
                                border-left: 5px solid #4CAF50;'>
                        <h4 style='color: #2E7D32; margin: 0 0 5px 0; font-size: 1.3rem;'>{puerto['nombre']} - {puerto['estado']}</h4>
                        <p style='color: #555; margin: 10px 0 0 0; font-size: 0.95rem; line-height: 1.6;'>
                            <strong>📍</strong> {puerto['descripcion']}
                        </p>
                        <p style='color: #666; margin: 8px 0 0 0; font-size: 0.9rem;'>
                            <strong style='color: #2E7D32;'>{puerto['especialidad']}</strong> | 
                            Movimiento: <strong>{puerto['teu_anual']:,} TEU/año</strong>
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("")
    
    # ============ TAB 3: ANÁLISIS COMPARATIVO ============
    with tab3:
        st.markdown("### 📊 Análisis Comparativo de Puertos")
        
        # Crear dataframe consolidado
        todos_puertos = []
        for region, puertos_lista in puertos_data.items():
            for puerto in puertos_lista:
                todos_puertos.append({
                    'Puerto': puerto['nombre'],
                    'Estado': puerto['estado'],
                    'Región': region.split()[0],
                    'TEU/Año': puerto['teu_anual'],
                    'Especialidad': puerto['especialidad']
                })
        
        df_puertos = pd.DataFrame(todos_puertos)
        
        # Gráfico: Top 10 puertos por movimiento
        st.markdown("**Top 10 Puertos por Movimiento de Contenedores**")
        
        df_top10 = df_puertos.nlargest(10, 'TEU/Año')
        
        fig_top = px.bar(
            df_top10,
            x='TEU/Año',
            y='Puerto',
            orientation='h',
            color='Región',
            color_discrete_map={'Litoral': '#4A7C9E', 'Literales': '#4CAF50'},
            title='',
            labels={'TEU/Año': 'Movimiento (TEU/Año)', 'Puerto': 'Puerto'}
        )
        
        fig_top.update_layout(
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#11101D'),
            xaxis=dict(gridcolor='#E0E0E0', showgrid=True),
            yaxis=dict(gridcolor='#E0E0E0', showgrid=False)
        )
        
        st.plotly_chart(fig_top, use_container_width=True)
        
        st.markdown("---")
        
        # Tabla comparativa
        st.markdown("**Tabla de Puertos Principales**")
        
        df_display = df_puertos.sort_values('TEU/Año', ascending=False).copy()
        df_display['TEU/Año'] = df_display['TEU/Año'].apply(lambda x: f"{x:,}")
        
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
        
        # Estadísticas por región
        st.markdown("**Estadísticas por Región**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pacifico_total = sum([p['teu_anual'] for p in puertos_data['Litoral del Pacífico']])
            st.metric(
                "🌊 Pacífico (8 puertos)",
                f"{pacifico_total:,} TEU/año",
                f"{(pacifico_total/df_puertos['TEU/Año'].sum())*100:.1f}% del total"
            )
        
        with col2:
            golfo_total = sum([p['teu_anual'] for p in puertos_data['Litoral del Golfo y Caribe']])
            st.metric(
                "⛵ Golfo & Caribe (8 puertos)",
                f"{golfo_total:,} TEU/año",
                f"{(golfo_total/df_puertos['TEU/Año'].sum())*100:.1f}% del total"
            )
        
        st.info("""
        **Movimiento Total Nacional**: ~18.4 millones TEU/año
        
        Los puertos mexicanos juegan un rol crítico en la logística norteamericana, 
        siendo alternativas competitivas a puertos estadounidenses.
        """)

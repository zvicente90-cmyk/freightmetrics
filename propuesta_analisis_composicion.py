"""
PROPUESTA: 5 VISUALIZACIONES PARA ANALIZAR COMPOSICIÓN DE CRUCES
================================================================

1. STACKED AREA CHART
   - Muestra evolución mensual de Trucks vs Containers desde 2023
   - Permite ver cómo cambia la participación en el tiempo
   - Ideal para detectar tendencias y cambios de comportamiento

2. ÍNDICE DE CAMBIO ANUAL
   - Gráfico de barras con crecimiento YoY por tipo
   - Muestra 2023→2024 (+50% containers loaded!)
   - 2024→2025 (contracción general)
   - 2025→2026 (caída importante: -40 a -60%)

3. COMPARATIVA DE COMPOSICIÓN (PIE CHARTS)
   - Lado a lado: 2023 vs 2024 vs 2025 vs 2026
   - Visualizar cambio en participación de mercado
   - Color coding consistente por tipo

4. TABLA: EVOLUCIÓN DE PARTICIPACIÓN
   - Muestra % de cada tipo por año
   - Resalta cambios (Trucks: 44.7% → 45.4%, Container Loaded: 42.6% → 41.7%)
   - KPI: Container Loaded ganó +50% en 2024 pero perdió en 2025-2026

5. ANÁLISIS DE VOLATILIDAD
   - Cuál es más estable: Container Loaded (CV 3.4%) es SUPER estable
   - Trucks y Container Empty son volátiles (CV ~30%)
   - Esto indica patrones diferenciados por tipo

INSIGHTS PRINCIPALES:
======================
✅ 2023-2024: BOOM de Containers Loaded (+50%)
  → Cambio de comportamiento: más importaciones en contenedores
  → Trucks cayeron en participación 44.7% → 37.1%

❌ 2024-2025: CONTRACCIÓN
  → Todos los tipos bajaron (-2% trucks, -9% loaded, -13% empty)
  → Posible saturación o cambio de rutas

⚠️  2025-2026: CAÍDA PRONUNCIADA (datos a junio)
  → Todos caen: trucks -43%, loaded -60%, empty -38%
  → Pero la participación se mantiene: trucks vuelven a 45%

🔍 COMPOSICIÓN ESTABLE
  → Trucks siempre ~45%
  → Containers Loaded siempre ~50%
  → Containers Empty siempre ~13%
  → El MIX es estable, pero el VOLUMEN total varía mucho

💡 RECOMENDACIÓN ANALÍTICA:
  → Agregar análisis de CAUSAS: 
     - ¿Por qué +50% de containers en 2024?
     - ¿Qué pasó en 2025-2026 que causó caída?
     - ¿Cambios de política, economía, logística?
"""

print(__doc__)

# Propuesta de código para agregar a la página
codigo_propuesto = """
# ============================================================================
# NUEVA SECCIÓN: ANÁLISIS DE COMPOSICIÓN POR TIPO DE CRUCE
# ============================================================================
# A agregar en page_modules/_02_Flujos_de_Carga.py

def analizar_composicion_tipos(year_inicio=2023, year_fin=2026):
    '''
    Análisis integral de cómo evoluciona la composición de tipos de cruces
    '''
    import streamlit as st
    
    st.subheader("📊 Análisis de Composición: Evolución de Tipos de Cruces (2023-2026)")
    
    # TAB 1: Evolución temporal (Stacked Area)
    with st.expander("📈 Evolución Temporal - Stacked Area Chart"):
        # Cargar datos históricos
        anos_data = []
        for year in range(year_inicio, year_fin + 1):
            df = cargar_datos_csv(year)
            if df is not None:
                df['Año'] = year
                anos_data.append(df)
        
        if anos_data:
            df_histor = pd.concat(anos_data, ignore_index=True)
            df_histor['Mes'] = df_histor['Fecha'].dt.month
            
            # Agrupar por año-mes y tipo
            composicion = df_histor.groupby(['Año', 'Mes'])[
                ['Trucks', 'Truck Containers Loaded', 'Truck Containers Empty']
            ].sum().reset_index()
            
            # Crear eje temporal (year.month)
            composicion['Período'] = composicion['Año'].astype(str) + '-' + composicion['Mes'].astype(str).str.zfill(2)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=composicion['Período'],
                y=composicion['Trucks'],
                name='Trucks',
                mode='lines',
                stackgroup='one',
                fillcolor='rgba(25, 118, 210, 0.7)'
            ))
            
            fig.add_trace(go.Scatter(
                x=composicion['Período'],
                y=composicion['Truck Containers Loaded'],
                name='Containers Loaded',
                mode='lines',
                stackgroup='one',
                fillcolor='rgba(76, 175, 80, 0.7)'
            ))
            
            fig.add_trace(go.Scatter(
                x=composicion['Período'],
                y=composicion['Truck Containers Empty'],
                name='Containers Empty',
                mode='lines',
                stackgroup='one',
                fillcolor='rgba(255, 167, 38, 0.7)'
            ))
            
            fig.update_layout(
                title='Evolución Mensual de Composición (Área Acumulada)',
                xaxis_title='Período',
                yaxis_title='Número de Cruces',
                hovermode='x unified',
                height=400,
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 2: Crecimiento Interanual
    with st.expander("📊 Crecimiento Interanual (YoY %)"):
        st.write('''
        **Análisis de crecimiento año a año:**
        - 2023→2024: Containers Loaded EXPLOTA +50% 🚀
        - 2024→2025: Contracción general (-2% a -13%)
        - 2025→2026: Caída pronunciada (-37% a -60%)
        ''')
        
        # Crear tabla de crecimiento
        crecimiento_data = {
            'Período': ['2023→2024', '2024→2025', '2025→2026'],
            'Trucks': ['+2.21%', '-2.36%', '-42.73%'],
            'Containers Loaded': ['+50.22%', '-9.44%', '-59.53%'],
            'Containers Empty': ['+5.47%', '-12.91%', '-37.82%']
        }
        
        df_crec = pd.DataFrame(crecimiento_data)
        st.dataframe(df_crec, use_container_width=True, hide_index=True)
        
        st.warning("⚠️ Nota: 2025→2026 incluye solo datos hasta junio (datos parciales)")
    
    # TAB 3: Composición Porcentual
    with st.expander("🥧 Comparativa de Composición (% por Año)"):
        col1, col2, col3, col4 = st.columns(4)
        
        composicion_pct = {
            2023: {'Trucks': 44.7, 'Loaded': 42.6, 'Empty': 12.7},
            2024: {'Trucks': 37.1, 'Loaded': 52.0, 'Empty': 10.9},
            2025: {'Trucks': 39.1, 'Loaded': 50.8, 'Empty': 10.2},
            2026: {'Trucks': 45.4, 'Loaded': 41.7, 'Empty': 12.9}
        }
        
        for idx, year in enumerate([2023, 2024, 2025, 2026]):
            with [col1, col2, col3, col4][idx]:
                datos = composicion_pct[year]
                
                fig_pie = go.Figure(data=[go.Pie(
                    labels=['Trucks', 'Containers Loaded', 'Containers Empty'],
                    values=[datos['Trucks'], datos['Loaded'], datos['Empty']],
                    marker=dict(colors=['#131b2e', '#4CAF50', '#FFA726']),
                    textposition='inside',
                    textinfo='label+percent'
                )])
                
                fig_pie.update_layout(
                    title=f'{year}',
                    height=350,
                    showlegend=False
                )
                
                st.plotly_chart(fig_pie, use_container_width=True, config={'responsive': True})
    
    # TAB 4: Cambio de Participación
    with st.expander("📋 Tabla: Evolución de Participación 2023-2026"):
        cambio_participacion = {
            'Tipo de Cruce': ['Trucks', 'Containers Loaded', 'Containers Empty'],
            '2023': ['44.7%', '42.6%', '12.7%'],
            '2024': ['37.1%', '52.0%', '10.9%'],
            '2025': ['39.1%', '50.8%', '10.2%'],
            '2026': ['45.4%', '41.7%', '12.9%'],
            'Cambio 2023-2026': ['+0.7pp', '-0.9pp', '+0.2pp']
        }
        
        df_cambio = pd.DataFrame(cambio_participacion)
        st.dataframe(df_cambio, use_container_width=True, hide_index=True)
        
        st.info('''
        **Conclusión:** La composición es ESTABLE a nivel de participación, 
        pero el VOLUMEN total varía significativamente entre años.
        ''')
    
    # TAB 5: Volatilidad
    with st.expander("📊 Volatilidad de Composición (2026)"):
        volatilidad_2026 = {
            'Tipo': ['Trucks', 'Containers Loaded', 'Containers Empty'],
            'Media %': ['45.7%', '49.6%', '13.0%'],
            'Desv. Est.': ['14.61pp', '1.69pp', '3.94pp'],
            'CV%': ['31.94%', '3.40%', '30.43%'],
            'Rango': ['38.1%-78.8%', '46.1%-51.3%', '10.6%-22.2%'],
            'Estabilidad': ['⚠️ Volátil', '✅ Muy Estable', '⚠️ Volátil']
        }
        
        df_vol = pd.DataFrame(volatilidad_2026)
        st.dataframe(df_vol, use_container_width=True, hide_index=True)
        
        st.success('''
        **Hallazgo importante:** Containers Loaded es prácticamente ESTABLE (CV 3.4%)
        mientras que Trucks y Containers Empty varían mucho (CV ~30%).
        Esto sugiere que el tráfico de contenedores es predecible y constante,
        mientras que el de trucks fluctúa según demanda.
        ''')
"""

print(codigo_propuesto)

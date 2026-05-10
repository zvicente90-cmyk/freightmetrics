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
    """Página Oracle Rate - Sistema de Cálculo Actuarial"""
    
    # ============ HEADER PRINCIPAL ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%); 
                    color: white; 
                    padding: 50px 60px; 
                    border-radius: 20px; 
                    margin-bottom: 40px;
                    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
                    border: 2px solid #4A7C9E;'>
            <h1 style='color: #FFFFFF; margin: 0; font-size: 3.5rem; font-weight: 800; letter-spacing: -1px;'>FreightMetrics Oracle Rate</h1>
            <p style='color: #B0C4DE; font-size: 1.25rem; font-weight: 600; margin: 20px 0 0 0; line-height: 1.4;'>
                La primera plataforma en México en desarrollar el Sistema Actuarial de Cálculo para Tarifas Spot de Autotransporte
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # ============ DESCRIPCIÓN GENERAL ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(74, 124, 158, 0.15) 0%, rgba(100, 150, 180, 0.08) 100%); 
                    padding: 35px 40px; 
                    border-radius: 15px; 
                    border-left: 6px solid #4A7C9E;
                    margin-bottom: 50px;'>
            <p style='color: #2C3E50; font-size: 1.05rem; margin: 0; line-height: 1.8; font-weight: 500;'>
                FreightMetrics redefine el estándar logístico en México. Somos la tecnología pionera que transforma la 
                <strong>Matriz de Costos de la SCT</strong> en una herramienta predictiva en tiempo real. Nuestro algoritmo procesa y 
                audita variables macroeconómicas oficiales para determinar el <strong>costo operativo real por kilómetro (CPK)</strong>, 
                integrando de forma única:
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # ============ TRES PILARES PRINCIPALES ============
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255, 165, 0, 0.15) 0%, rgba(255, 140, 0, 0.08) 100%); 
                        padding: 30px; 
                        border-radius: 15px; 
                        border-left: 5px solid #FFA500;
                        height: 100%;
                        box-shadow: 0 4px 15px rgba(255, 165, 0, 0.1);'>
                <h3 style='color: #FF8C00; margin: 0 0 15px 0; font-size: 1.3rem; font-weight: 700;'>⚡ Variación Energética</h3>
                <p style='color: #444; font-size: 1rem; margin: 0; line-height: 1.6; font-weight: 500;'>
                    Indexado diario con los precios regionales de la <strong>CRE</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(100, 200, 255, 0.15) 0%, rgba(100, 150, 200, 0.08) 100%); 
                        padding: 30px; 
                        border-radius: 15px; 
                        border-left: 5px solid #4A7C9E;
                        height: 100%;
                        box-shadow: 0 4px 15px rgba(74, 124, 158, 0.1);'>
                <h3 style='color: #2C5AA0; margin: 0 0 15px 0; font-size: 1.3rem; font-weight: 700;'>📊 Inflación Sectorial</h3>
                <p style='color: #444; font-size: 1rem; margin: 0; line-height: 1.6; font-weight: 500;'>
                    Ajuste dinámico basado en el <strong>INPP del INEGI (Rubro 611)</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(76, 175, 80, 0.08) 100%); 
                        padding: 30px; 
                        border-radius: 15px; 
                        border-left: 5px solid #4CAF50;
                        height: 100%;
                        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.1);'>
                <h3 style='color: #2E7D32; margin: 0 0 15px 0; font-size: 1.3rem; font-weight: 700;'>🛡️ Riesgo Logístico</h3>
                <p style='color: #444; font-size: 1rem; margin: 0; line-height: 1.6; font-weight: 500;'>
                    Evaluación de seguridad por corredor y nodo industrial <strong>2026</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============ BOTÓN LLAMATIVO DE REDIRECCIÓN ============
    st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; margin: 60px 0;'>
            <a href='https://freightmetrics-oracle-rate.streamlit.app/' target='_blank' style='text-decoration: none;'>
                <button style='background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%); 
                            color: white; 
                            padding: 20px 50px; 
                            border-radius: 50px; 
                            font-size: 1.1rem; 
                            font-weight: 700;
                            box-shadow: 0 8px 25px rgba(255, 107, 107, 0.35);
                            transition: all 0.3s ease;
                            cursor: pointer;
                            border: 2px solid #FF6B6B;
                            letter-spacing: 0.5px;'>
                    🚀 ACCEDER A ORACLE RATE COMPLETO
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    # ============ INFORMACIÓN ADICIONAL ============
    st.markdown("""
        <div style='background: rgba(74, 124, 158, 0.08); 
                    padding: 30px 40px; 
                    border-radius: 15px; 
                    margin-top: 60px;
                    border-left: 6px solid #FF6B6B;'>
            <h3 style='color: #FF6B6B; margin: 0 0 20px 0;'>ℹ️ Sobre Oracle Rate Completo</h3>
            <p style='color: #555; font-size: 1rem; margin: 10px 0; line-height: 1.7;'>
                La versión completa en Streamlit Cloud incluye:
            </p>
            <ul style='color: #555; font-size: 0.95rem; margin: 15px 0; line-height: 1.8;'>
                <li><strong>🔄 Actualizaciones en tiempo real</strong> de tasas de cambio, energía e inflación</li>
                <li><strong>📈 Gráficos interactivos</strong> con análisis histórico de precios</li>
                <li><strong>🧮 Calculadora de CPK</strong> personalizada por ruta y corredor</li>
                <li><strong>📊 Dashboard ejecutivo</strong> con KPIs de mercado</li>
                <li><strong>🔐 Seguridad robusta</strong> y auditoría de cambios</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

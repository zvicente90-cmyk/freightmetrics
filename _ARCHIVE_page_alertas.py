"""
ARCHIVO ARCHIVADO - page_alertas.py
Página de centro de notificaciones operativas (no utilizada actualmente)
Archivada el: 2026-04-08
Razón: Funcionalidad reemplazada por sistema de alertas mejorado en page_monitoreo_aduanas
"""

import streamlit as st

def page_alertas():
    """Centro de Notificaciones Operativas - DEPRECATED"""
    st.title("⚠️ Centro de Notificaciones Operativas")
    st.markdown("---")
    
    # Nota: Esta función usa variables globales que no están disponibles en contexto
    # Para restaurar: necesita df_mapa como variable global
    try:
        alertas_criticas = df_mapa[df_mapa["Saturacion"] > 80]
        alertas_preventivas = df_mapa[(df_mapa["Saturacion"] > 60) & (df_mapa["Saturacion"] <= 80)]

        if not alertas_criticas.empty or not alertas_preventivas.empty:
            col_a, col_b = st.columns(2)
            
            with col_a:
                for _, row in alertas_criticas.iterrows():
                    st.error(f"**CRÍTICO:** Puerto de {row['Puerto']} al {row['Saturacion']}%")
                    try:
                        st.toast(f"¡Acción requerida en {row['Puerto']}!", icon='🔥')
                    except:
                        pass
            
            with col_b:
                for _, row in alertas_preventivas.iterrows():
                    st.warning(f"**PREVENTIVO:** {row['Puerto']} aumentando carga ({row['Saturacion']}%)")
        else:
            st.success("✅ Operación Fluida: No se detectan cuellos de botella en la red.")
    except NameError:
        st.error("❌ Datos no disponibles. Esta página fue archivada.")

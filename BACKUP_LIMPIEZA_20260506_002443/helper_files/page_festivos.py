"""
PÁGINA DE DÍAS FESTIVOS 2026 - MÉXICO Y EEUU
Muestra horarios de aduanas en días festivos con impacto por frontera
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import numpy as np

# ============================================================================
# ESTILOS CSS PERSONALIZADOS - SELECTBOX CON COLOR
# ============================================================================

st.markdown("""
<style>
/* ============ RADIO BUTTONS - SIN RECUADRO EN TODO LADO ============ */

/* OBJETIVO: Remover TODOS los backgrounds grises de radio buttons */

/* 1. RADIO BUTTONS SELECCIONADOS - CRÍTICO */
[data-testid="stRadio"] [aria-checked="true"],
[data-testid="stRadio"] input[type="radio"]:checked,
[data-testid="stRadio"] input[type="radio"]:checked + label,
[data-testid="stRadio"] label:has(input:checked) {
    background-color: transparent !important;
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

/* 2. RADIO BUTTONS NO SELECCIONADOS */
[data-testid="stRadio"] [aria-checked="false"],
[data-testid="stRadio"] input[type="radio"]:not(:checked),
[data-testid="stRadio"] input[type="radio"]:not(:checked) + label {
    background-color: transparent !important;
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

/* 3. TODO DENTRO DE RADIO - SIN EXCEPCIÓN */
[data-testid="stRadio"] *, 
[data-testid="stRadio"] *::before,
[data-testid="stRadio"] *::after {
    background-color: transparent !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

/* 4. RADIO GENERAL */
[data-testid="stRadio"] {
    background-color: transparent !important;
    border: none !important;
}

[data-testid="stRadio"] label {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #ffffff !important;
}

[data-testid="stRadio"] input[type="radio"] {
    accent-color: #1f77b4 !important;
}

/* 5. DIVS ANIDADOS - REMOVER PADDING/MARGIN */
[data-testid="stRadio"] div {
    background-color: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

[data-testid="stRadio"] div div {
    background-color: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

[data-testid="stRadio"] div div div {
    background-color: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

[data-testid="stRadio"] div div div div {
    background-color: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* 6. RADIOGROUP CONTENEDOR */
div[role="radiogroup"] {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

div[role="radiogroup"] * {
    background-color: transparent !important;
    border: none !important;
}

div[role="radiogroup"] label {
    background-color: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* 7. LABELS GLOBALES */
label {
    background-color: transparent !important;
    border: none !important;
}

label span {
    background-color: transparent !important;
}

/* ============ SELECTBOX - TRANSPARENTE CON TEMA ============ */
div[data-testid="stSelectbox"] > div {
    background-color: transparent !important;
}

div[data-testid="stSelectbox"] > div > div {
    background-color: transparent !important;
}

/* ============ EXPANDABLE SECTIONS ============ */
[data-testid="stExpander"] {
    background-color: #1e1e2e !important;
    border: 1px solid #3d3d54 !important;
    border-radius: 6px !important;
}

[data-testid="stExpander"] summary {
    background-color: #1e1e2e !important;
    color: #ffffff !important;
}

[data-testid="stExpander"] summary:hover {
    background-color: #1e1e2e !important;
    color: #ffffff !important;
}

[data-testid="stExpander"] summary * {
    color: #ffffff !important;
}

[data-testid="stExpanderDetails"] {
    background-color: #1e1e2e !important;
    color: #ffffff !important;
}

details > summary {
    background-color: #1e1e2e !important;
    color: #ffffff !important;
    padding: 10px;
    border-radius: 5px;
}

details > summary:hover {
    background-color: #1e1e2e !important;
    color: #ffffff !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================================
# CONFIGURACIÓN DE DÍAS FESTIVOS 2026
# ============================================================================

FESTIVOS_MEXICO_2026 = {
    "01-01": {"nombre": "Año Nuevo", "color": "red", "tipo": "nacional"},
    "02-05": {"nombre": "Constitución", "color": "orange", "tipo": "nacional"},
    "03-17": {"nombre": "Benito Juárez", "color": "orange", "tipo": "nacional"},
    "05-01": {"nombre": "Día del Trabajo", "color": "red", "tipo": "nacional"},
    "09-16": {"nombre": "Independencia", "color": "red", "tipo": "nacional"},
    "11-02": {"nombre": "Día de Muertos", "color": "purple", "tipo": "cultural"},
    "11-19": {"nombre": "Revolución Mexicana", "color": "orange", "tipo": "nacional"},
    "12-25": {"nombre": "Navidad", "color": "red", "tipo": "nacional"},
}

FESTIVOS_EEUU_2026 = {
    "01-01": {"nombre": "New Year's Day", "color": "red", "tipo": "nacional"},
    "01-19": {"nombre": "MLK Jr. Day", "color": "blue", "tipo": "nacional"},
    "02-16": {"nombre": "Presidents Day", "color": "blue", "tipo": "nacional"},
    "05-25": {"nombre": "Memorial Day", "color": "blue", "tipo": "nacional"},
    "07-04": {"nombre": "Independence Day", "color": "red", "tipo": "nacional"},
    "09-07": {"nombre": "Labor Day", "color": "blue", "tipo": "nacional"},
    "10-12": {"nombre": "Columbus Day", "color": "blue", "tipo": "nacional"},
    "11-11": {"nombre": "Veterans Day", "color": "blue", "tipo": "nacional"},
    "11-26": {"nombre": "Thanksgiving", "color": "orange", "tipo": "nacional"},
    "12-25": {"nombre": "Christmas", "color": "red", "tipo": "nacional"},
}

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

@st.cache_data
def cargar_horarios_aduanas():
    """Carga horarios oficiales del TSV"""
    try:
        ruta_tsv = Path(__file__).parent / "Horarios de Aduanas en Días Festivos - Horarios de Aduanas en Días Festivos.tsv"
        df = pd.read_csv(ruta_tsv, sep='\t', encoding='utf-8')
        return df
    except Exception as e:
        st.error(f"Error cargando horarios: {e}")
        return None

def parsear_hora(hora_str):
    """Convierte '06:00 – 19:00' a (6, 19)"""
    if not hora_str or 'Cerrado' in hora_str or 'CERRADO' in hora_str:
        return None
    try:
        if '–' in hora_str:
            partes = hora_str.split('–')
            apertura = int(partes[0].strip().split(':')[0])
            cierre = int(partes[1].strip().split(':')[0])
            return (apertura, cierre)
    except:
        pass
    return None

def obtener_estado_aduana_festivo(aduana_exp, aduana_imp, aduana_fest):
    """Determina el estado de una aduana en día festivo"""
    if 'CERRADO' in aduana_fest or 'Cerrado' in aduana_fest:
        return "🔴 CERRADA", "CERRADO"
    
    exp_horas = parsear_hora(aduana_exp)
    fest_horas = parsear_hora(aduana_fest)
    
    if exp_horas and fest_horas:
        if fest_horas[1] - fest_horas[0] < exp_horas[1] - exp_horas[0]:
            return "🟡 REDUCIDA", aduana_fest
        else:
            return "🟢 NORMAL", aduana_fest
    
    return "⚠️ VERIFICAR", aduana_fest

# ============================================================================
# PÁGINA PRINCIPAL
# ============================================================================

def page_festivos():
    """Página de Días Festivos 2026"""
    
    # Título con gradiente
    st.markdown("""
        <h1 style="background: linear-gradient(135deg, #2d3748 0%, #374151 100%); 
                   -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent; 
                   background-clip: text;
                   font-size: 2.5em;
                   margin: 0;
                   padding: 0;">
            📅 Horarios Aduanas en Días Festivos 2026
        </h1>
    """, unsafe_allow_html=True)
    
    # Cargar datos
    df_horarios = cargar_horarios_aduanas()
    if df_horarios is None:
        return
    
    # ========================================================================
    # TAB 1: COMPARACIÓN DE FESTIVOS
    # ========================================================================
    tab1, tab2, tab3 = st.tabs(["📊 Comparación Festivos", "🚨 Impacto por Aduana", "🔍 Búsqueda Rápida"])
    
    with tab1:
        st.subheader("Días Festivos 2026 - México vs EEUU")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🇲🇽 MÉXICO")
            for fecha, info in sorted(FESTIVOS_MEXICO_2026.items()):
                estado_icon = "🔴" if info["tipo"] == "nacional" else "💜"
                st.markdown(f"{estado_icon} **{info['nombre']}** - {fecha}")
        
        with col2:
            st.markdown("### 🇺🇸 EEUU")
            for fecha, info in sorted(FESTIVOS_EEUU_2026.items()):
                estado_icon = "🔵" if info["tipo"] == "nacional" else "⚪"
                st.markdown(f"{estado_icon} **{info['nombre']}** - {fecha}")
        
        st.divider()
        
        # Fechas coincidentes
        fechas_mex = set(FESTIVOS_MEXICO_2026.keys())
        fechas_usa = set(FESTIVOS_EEUU_2026.keys())
        coincidentes = fechas_mex & fechas_usa
        
        st.markdown("### 🔗 Festivos Coincidentes (Mayor Impacto)")
        if coincidentes:
            cols = st.columns(len(coincidentes))
            for idx, fecha in enumerate(sorted(coincidentes)):
                with cols[idx]:
                    mex_nombre = FESTIVOS_MEXICO_2026[fecha]['nombre']
                    usa_nombre = FESTIVOS_EEUU_2026[fecha]['nombre']
                    st.info(f"**{fecha}**\n\n{mex_nombre}\n\n{usa_nombre}")
        else:
            st.info("No hay festivos coincidentes en 2026")
    
    # ========================================================================
    # TAB 2: IMPACTO POR ADUANA
    # ========================================================================
    with tab2:
        st.subheader("Impacto de Días Festivos en Aduanas")
        
        # Preparar opciones de fechas
        todas_fechas = sorted(list(FESTIVOS_MEXICO_2026.keys()) + list(FESTIVOS_EEUU_2026.keys()))
        opciones = {}
        for fecha in todas_fechas:
            nombre = FESTIVOS_MEXICO_2026.get(fecha, FESTIVOS_EEUU_2026.get(fecha, {})).get('nombre', 'Festivo')
            opciones[f"{fecha} - {nombre}"] = fecha
        opciones_list = list(opciones.keys())
        
        # Fila superior: título + operación
        col_titulo, col_op = st.columns([3, 1])
        with col_op:
            tipo_operacion = st.segmented_control(
                "⚙️ Operación",
                ["Exportación", "Importación"],
                default="Exportación",
                key="seg_operacion"
            )
            if tipo_operacion is None:
                tipo_operacion = "Exportación"
        
        st.markdown("**📅 Seleccionar día festivo:**")
        
        # 3 columnas con st.pills (sin radio buttons - sin recuadro gris)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📌 México**")
            opciones_mex = [f for f in opciones_list if f.split(' - ')[0] in FESTIVOS_MEXICO_2026]
            sel_mex = st.pills(
                "México", opciones_mex,
                selection_mode="single",
                default=None,
                label_visibility="collapsed",
                key="pills_mex"
            )
        
        with col2:
            st.markdown("**📌 EEUU**")
            opciones_usa = [f for f in opciones_list if f.split(' - ')[0] in FESTIVOS_EEUU_2026]
            sel_usa = st.pills(
                "EEUU", opciones_usa,
                selection_mode="single",
                default=None,
                label_visibility="collapsed",
                key="pills_usa"
            )
        
        with col3:
            st.markdown("**📌 Coincidentes**")
            fechas_coinc_set = set(FESTIVOS_MEXICO_2026.keys()) & set(FESTIVOS_EEUU_2026.keys())
            opciones_coinc = [f for f in opciones_list if f.split(' - ')[0] in fechas_coinc_set]
            sel_coinc = st.pills(
                "Coinc", opciones_coinc,
                selection_mode="single",
                default=None,
                label_visibility="collapsed",
                key="pills_coinc"
            )
        
        # Determinar fecha seleccionada: la última que el usuario haya tocado
        sel_display = sel_coinc or sel_usa or sel_mex
        if sel_display is None:
            sel_display = opciones_list[0]
        fecha_sel = opciones.get(sel_display, list(opciones.values())[0])
        
        st.divider()
        
        # Tabla de aduanas con impacto festivo
        datos_tabla = []
        
        for _, row in df_horarios.iterrows():
            aduana = row['Aduana / Puerto'].strip()
            exp_lv = row['Exportación (L-V)']
            imp_lv = row['Importación (L-V)']
            fest = row['Día Festivo (Estándar)']
            
            # Elegir operación
            horario_lv = exp_lv if tipo_operacion == "Exportación" else imp_lv
            
            # Comparar
            estado, horario_fest_display = obtener_estado_aduana_festivo(exp_lv, imp_lv, fest)
            
            # Horas disponibles
            horas_norm = parsear_hora(horario_lv)
            horas_fest = parsear_hora(fest)
            
            horas_norm_str = f"{horas_norm[0]}-{horas_norm[1]}h" if horas_norm else "N/A"
            horas_fest_str = f"{horas_fest[0]}-{horas_fest[1]}h" if horas_fest else "CERRADO"
            
            datos_tabla.append({
                "Aduana": aduana,
                "Horario Normal": horas_norm_str,
                "Horario Festivo": horas_fest_str,
                "Estado": estado,
                "Impacto": "🔴 Alto" if "CERRADA" in estado else ("🟡 Medio" if "REDUCIDA" in estado else "🟢 Ninguno")
            })
        
        df_tabla = pd.DataFrame(datos_tabla)
        
        # Colorear por estado
        def colorear_estado(row):
            if "CERRADA" in row['Estado']:
                return ['background-color: #ffcccc'] * len(row)
            elif "REDUCIDA" in row['Estado']:
                return ['background-color: #fff3cd'] * len(row)
            else:
                return ['background-color: #d4edda'] * len(row)
        
        df_styled = df_tabla.style.apply(colorear_estado, axis=1)
        st.dataframe(df_styled, use_container_width=True, hide_index=True)
        
        # Resumen
        cerradas = len(df_tabla[df_tabla['Estado'].str.contains("CERRADA")])
        reducidas = len(df_tabla[df_tabla['Estado'].str.contains("REDUCIDA")])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 Cerradas", cerradas)
        with col2:
            st.metric("🟡 Reducidas", reducidas)
        with col3:
            st.metric("🟢 Sin Cambios", len(df_tabla) - cerradas - reducidas)
    
    # ========================================================================
    # TAB 3: BÚSQUEDA RÁPIDA
    # ========================================================================
    with tab3:
        st.subheader("Búsqueda Rápida de Aduana")
        
        lista_aduanas = [row['Aduana / Puerto'].strip() for _, row in df_horarios.iterrows()]
        
        # Operación con segmented_control (igual que TAB 2)
        col_a, col_b = st.columns([3, 1])
        with col_b:
            tipo_op = st.segmented_control(
                "⚙️ Operación",
                ["Exportación", "Importación"],
                default="Exportación",
                key="seg_op_tab3"
            )
            if tipo_op is None:
                tipo_op = "Exportación"
        
        st.markdown("**🏢 Seleccionar aduana:**")
        
        # Pills en 3 columnas para evitar lista larga
        n = len(lista_aduanas)
        div = (n + 2) // 3
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sel1 = st.pills("A1", lista_aduanas[:div], selection_mode="single", default=None,
                            label_visibility="collapsed", key="tab3_col1")
        with col2:
            sel2 = st.pills("A2", lista_aduanas[div:div*2], selection_mode="single", default=None,
                            label_visibility="collapsed", key="tab3_col2")
        with col3:
            sel3 = st.pills("A3", lista_aduanas[div*2:], selection_mode="single", default=None,
                            label_visibility="collapsed", key="tab3_col3")
        
        aduana_busqueda = sel1 or sel2 or sel3 or lista_aduanas[0]
        
        with col3:
            st.write("")  # Espaciado
        
        # Buscar aduana
        aduana_data = df_horarios[df_horarios['Aduana / Puerto'].str.contains(aduana_busqueda, case=False)].iloc[0]
        
        st.divider()
        
        # Card con información completa
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### 📍 {aduana_busqueda}")
            
            # Horarios
            with st.expander("📋 Horarios Completos", expanded=True):
                col_tabs = st.columns(2)
                
                with col_tabs[0]:
                    st.markdown("**Exportación (L-V)**")
                    st.markdown(f"<span style='color:#4da6ff;font-size:1.1em;'>🕐 {aduana_data['Exportación (L-V)']}</span>", unsafe_allow_html=True)
                
                with col_tabs[1]:
                    st.markdown("**Importación (L-V)**")
                    st.markdown(f"<span style='color:#4da6ff;font-size:1.1em;'>🕐 {aduana_data['Importación (L-V)']}</span>", unsafe_allow_html=True)
                
                col_tabs = st.columns(2)
                
                with col_tabs[0]:
                    st.markdown("**Fin de Semana (S-D)**")
                    st.markdown(f"<span style='color:#4da6ff;font-size:1.1em;'>🕐 {aduana_data['Fin de Semana (S-D)']}</span>", unsafe_allow_html=True)
                
                with col_tabs[1]:
                    st.markdown("**Día Festivo**")
                    st.markdown(f"<span style='color:#4da6ff;font-size:1.1em;'>🕐 {aduana_data['Día Festivo (Estándar)']}</span>", unsafe_allow_html=True)
        
        with col2:
            # Indicadores
            horario_normal = aduana_data['Exportación (L-V)'] if tipo_op == "Exportación" else aduana_data['Importación (L-V)']
            horario_festivo = aduana_data['Día Festivo (Estándar)']
            
            estado, _ = obtener_estado_aduana_festivo(
                aduana_data['Exportación (L-V)'],
                aduana_data['Importación (L-V)'],
                aduana_data['Día Festivo (Estándar)']
            )
            
            if "CERRADA" in estado:
                st.error("CERRADA EN FESTIVOS")
            elif "REDUCIDA" in estado:
                st.warning("HORARIO REDUCIDO")
            else:
                st.success("SIN CAMBIOS")
        
        # Row picker para fechas festivas específicas
        st.divider()
        st.markdown("### 📅 Estado en Fechas Específicas")
        
        todas_fechas_dict = {**FESTIVOS_MEXICO_2026, **FESTIVOS_EEUU_2026}
        opciones_fechas = {f"{f} - {todas_fechas_dict[f]['nombre']}": f for f in sorted(todas_fechas_dict.keys())}
        
        sel_fecha = st.pills(
            "📅 Seleccionar fecha festiva",
            list(opciones_fechas.keys()),
            selection_mode="single",
            default=None,
            key="tab3_fecha"
        )
        fecha_check = opciones_fechas[sel_fecha] if sel_fecha else sorted(todas_fechas_dict.keys())[0]
        
        col1, col2 = st.columns([1, 3])
        with col1:
            es_mx = "🇲🇽" if fecha_check in FESTIVOS_MEXICO_2026 else "🇺🇸"
            st.metric("País", es_mx)
        
        st.info(f"**Horario en {fecha_check}:** {aduana_data['Día Festivo (Estándar)']}")

# ============================================================================
# EJECUTAR SI SE LLAMA DIRECTAMENTE
# ============================================================================

if __name__ == "__main__":
    page_festivos()

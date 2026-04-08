"""
ARCHIVO ARCHIVADO - page_reportes.py
Página de reportes y consultas de APIs (no utilizada actualmente)
Archivada el: 2026-04-08
Razón: Funcionalidad parcialmente duplicada y APIs backend no siempre disponibles
"""

import streamlit as st
import pandas as pd
import datetime as dt
import requests
from urllib.parse import parse_qs

# Variables globales necesarias (para referencia)
# df_mapa: DataFrame de puertos
# tipo_cambio: Tipo de cambio USD/MXN
# crear_pdf: Función para generar PDFs
# api_key: API key del usuario

def page_reportes():
    """Reportes y Consultas de APIs - DEPRECATED"""
    st.title("📥 Reportes")
    st.markdown("---")
    st.warning("⚠️ Esta página fue archivada. Las funcionalidades de reportes han sido integradas en otras secciones.")
    
    # El código original comentado a continuación para referencia futura:
    """
    # Calculamos costos y mostramos tabla
    df_local = df_mapa.copy()
    df_local["Costo_Estimado_MXN"] = df_local["Operaciones"] * 5000 * tipo_cambio
    st.subheader("📑 Datos de Operación")
    st.dataframe(df_local[["Puerto", "Saturacion", "Costo_Estimado_MXN"]], use_container_width=True)

    st.markdown("---")
    pdf_data = crear_pdf(df_local, tipo_cambio)
    st.download_button(
        label="📄 Descargar PDF",
        data=pdf_data,
        file_name=f"FreightMetrics_Reporte_{dt.date.today()}.pdf",
        mime="application/pdf"
    )

    # --- CONSULTA CENSUS ---
    st.markdown("---")
    st.subheader("🌐 Consultar Census (International Trade)")
    dataset = st.selectbox("Dataset (timeseries/intltrade)", ["exports", "imports"], index=0)
    get_param = st.text_input("get (campos, separados por coma)", "ALL_VAL_MO,CTY")
    time_param = st.text_input("time (ej. 2019)", "")

    # headers para llamadas a la API
    try:
        headers = {'X-API-KEY': api_key} if api_key else None
    except Exception:
        headers = None

    params = {}
    if get_param:
        params["get"] = get_param
    if time_param:
        params["time"] = time_param

    if st.button("Consultar Census"):
        try:
            with st.spinner("Consultando Census API..."):
                resp = requests.get(f"http://127.0.0.1:8000/functions/v1/census/{dataset}", params=params, headers=headers, timeout=30)
                resp.raise_for_status()
                payload = resp.json()
                if payload.get("status") == "ok":
                    df_census = pd.DataFrame(payload.get("data", []))
                    if df_census.empty:
                        st.warning("La consulta no retornó filas.")
                    else:
                        st.subheader("Resultados Census")
                        st.dataframe(df_census, use_container_width=True)
                        # Intentar convertir columnas numéricas y plotear
                        for col in df_census.columns:
                            if df_census[col].dtype == object:
                                try:
                                    df_census[col] = pd.to_numeric(df_census[col].astype(str).str.replace(",", ""), errors='coerce')
                                except Exception:
                                    pass
                        numeric_cols = df_census.select_dtypes(include=["number"]).columns.tolist()
                        if numeric_cols:
                            st.subheader("Series numéricas")
                            st.line_chart(df_census[numeric_cols])
                else:
                    st.error(f"Error: {payload.get('detail', 'respuesta no OK')}")
        except Exception as e:
            st.error(f"Fallo al consultar Census: {e}")

    # --- CONSULTA BTS (data.bts.gov / Socrata) ---
    st.markdown("---")
    st.subheader("🌍 Consultar BTS / Socrata")
    bts_dataset = st.text_input("Dataset ID (ej. 9v9j-9z33)", "")
    bts_domain = st.text_input("Dominio (por defecto data.bts.gov)", "data.bts.gov")
    bts_qs = st.text_input("Query string (ej: $limit=100&$select=column1,column2)", "")

    if st.button("Consultar BTS"):
        if not bts_dataset:
            st.error("Ingrese un dataset ID para consultar.")
        else:
            try:
                with st.spinner("Consultando BTS / Socrata..."):
                    params_raw = parse_qs(bts_qs, keep_blank_values=True)
                    params = {k: v[0] for k, v in params_raw.items()} if params_raw else {}
                    resp = requests.get(f"http://127.0.0.1:8000/functions/v1/bts/{bts_dataset}", 
                                      params={**params, "domain": bts_domain}, headers=headers, timeout=30)
                    resp.raise_for_status()
                    payload = resp.json()
                    if payload.get("status") == "ok":
                        df_bts = pd.DataFrame(payload.get("data", []))
                        if df_bts.empty:
                            st.warning("La consulta BTS no retornó filas.")
                        else:
                            st.subheader("Resultados BTS")
                            st.dataframe(df_bts, use_container_width=True)
                            numeric_cols = df_bts.select_dtypes(include=["number"]).columns.tolist()
                            if numeric_cols:
                                st.subheader("Series numéricas")
                                st.line_chart(df_bts[numeric_cols])
                    else:
                        st.error(f"Error BTS: {payload.get('detail', 'respuesta no OK')}")
            except Exception as e:
                st.error(f"Fallo al consultar BTS: {e}")

    # --- CONSULTA SAT (páginas públicas) ---
    st.markdown("---")
    st.subheader("🧾 Consultar SAT (extraer tabla / enlaces)")
    sat_url = st.text_input("URL SAT o pública", "https://www.sat.gob.mx/portal/public/home")
    if st.button("Consultar SAT"):
        if not sat_url:
            st.error("Ingresa una URL para consultar.")
        else:
            try:
                with st.spinner("Consultando SAT..."):
                    resp = requests.get("http://127.0.0.1:8000/functions/v1/sat/fetch", 
                                      params={"url": sat_url}, headers=headers, timeout=30)
                    resp.raise_for_status()
                    payload = resp.json()
                    if payload.get("status") == "ok":
                        df_sat = pd.DataFrame(payload.get("data", []))
                        if df_sat.empty:
                            st.warning("No se encontraron tablas ni enlaces en la URL proporcionada.")
                        else:
                            st.subheader("Resultados SAT")
                            st.dataframe(df_sat, use_container_width=True)
                    else:
                        st.error(f"Error SAT: {payload.get('detail', 'respuesta no OK')}")
            except Exception as e:
                st.error(f"Fallo al consultar SAT: {e}")
    """

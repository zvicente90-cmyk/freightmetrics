"""
FreightMetrics Academy — Sección de recursos educativos y ebooks
Con guardado de leads en Supabase (sin autenticación requerida)
Módulo: page_modules/_08_Academy.py
"""

import streamlit as st
from datetime import datetime
import os
from pathlib import Path
import base64
import json


def _generate_seo_schema():
    """Genera schema.org JSON-LD para SEO"""
    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "FreightMetrics Academy",
        "description": "Plataforma de recursos educativos y ebooks gratuitos para profesionales de logística transfronteriza México-USA",
        "url": "https://freightmetrics.streamlit.app",
        "image": "https://freightmetrics.streamlit.app/logo.png",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Tijuana",
            "addressRegion": "BC",
            "addressCountry": "MX"
        },
        "sameAs": [
            "https://www.linkedin.com/company/freightmetrics",
            "https://github.com/zvicente90-cmyk/freightmetrics"
        ],
        "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "MXN",
            "price": "0",
            "offerCount": 3,
            "description": "3 ebooks gratuitos sobre logística, transporte y nearshoring"
        }
    }
    return schema


def _get_supabase_client():
    try:
        from supabase import create_client
        url = key = None
        try:
            url = st.secrets.get("SUPABASE_URL")
            key = st.secrets.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_ANON_KEY")
        except Exception:
            pass
        if not url:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        if url and key:
            return create_client(url, key)
    except ImportError:
        pass
    return None


def _guardar_lead(nombre, email, empresa, perfil, ebooks):
    client = _get_supabase_client()
    if not client:
        # Sin Supabase: simular registro exitoso para demostración
        return True, f"✅ Registro recibido. Te avisaremos cuando el recurso esté disponible."
    try:
        data = {
            "nombre":  nombre.strip(),
            "email":   email.strip().lower(),
            "empresa": empresa.strip() if empresa else None,
            "perfil":  perfil or None,
            "ebooks":  ebooks or [],
            "fuente":  "freightmetrics.streamlit.app",
        }
        resp = client.table("academy_leads").insert(data).execute()
        if resp.data:
            return True, "OK"
        return False, "Error al guardar. Intenta de nuevo."
    except Exception as e:
        err = str(e)
        if "duplicate" in err.lower() or "unique" in err.lower():
            return False, "Este email ya esta registrado."
        return False, f"Error: {err[:120]}"


def _obtener_ruta_ebook(id_ebook):
    """Retorna la ruta del PDF del ebook si existe"""
    ruta_base = Path(__file__).parent.parent / "academy" / "ebooks"
    
    # Mapeo de IDs a nombres de archivo
    archivos = {
        "hombre_camion": "FreightMetrics_Academy_Hombre_Camion_ES_EN.pdf",
        "kpis_logistica": "FreightMetrics_Academy_KPIs_Logistica_ES_EN.pdf",
        "guia_autotransporte": "FreightMetrics_Academy_Guia_Autotransporte-Programas Gubernamentales_ES_EN.pdf",
        "nearshoring_101": "FreightMetrics_Academy_Nearshoring_ES_EN.pdf",
    }
    
    nombre_archivo = archivos.get(id_ebook)
    if not nombre_archivo:
        return None
    
    ruta_completa = ruta_base / nombre_archivo
    
    if ruta_completa.exists():
        return ruta_completa
    
    return None


def _descargar_ebook(archivo_pdf_path, nombre_ebook):
    """Crea un botón de descarga para el PDF"""
    try:
        with open(archivo_pdf_path, "rb") as f:
            pdf_data = f.read()
        
        # Crear nombre de archivo para descarga
        nombre_descarga = f"{nombre_ebook}.pdf"
        
        # Botón de descarga
        st.download_button(
            label="📥 Descargar PDF",
            data=pdf_data,
            file_name=nombre_descarga,
            mime="application/pdf",
            use_container_width=True,
            key=f"download_{nombre_ebook}"
        )
        
        return True
    except Exception as e:
        st.error(f"Error al preparar descarga: {e}")
        return False


EBOOKS = [
    {
        "id": "kpis_logistica",
        "emoji": "📊",
        "titulo": "KPIs de Logistica para Directivos - Transporte México-USA",
        "subtitulo": "Metricas que importan en el transporte Mexico-USA",
        "descripcion": (
            "Domina los 25+ indicadores clave de desempenio que usan los directores de "
            "logistica mas exitosos en corredores mexicanos. Aprende a medir costo por kilometro, "
            "tiempo de transito, tasa de cumplimiento y mas con ejemplos reales de logistica "
            "transfronteriza México-USA."
        ),
        "temas": [
            "25+ KPIs esenciales de transporte",
            "Benchmarks por corredor y equipo",
            "Dashboards de monitoreo ejecutivo",
            "Integracion con datos CRE e INEGI",
        ],
        "paginas": 48, "nivel": "Intermedio", "color": "#4070F4",
        "disponible": True, "badge": "DISPONIBLE",
    },
    {
        "id": "guia_autotransporte",
        "emoji": "🚛",
        "titulo": "Guia de Apoyo al Autotransporte - Programas Gubernamentales México 2025",
        "subtitulo": "Apoyos, creditos y programas federales para transportistas",
        "descripcion": (
            "Una guia completa sobre los programas de apoyo federales y estatales "
            "para el autotransporte en Mexico. Desde SICT hasta NAFIN, descubre como "
            "acceder a financiamiento, creditos y renovar tu equipo. Incluye Plan de Apoyo Masivo "
            "y esquemas de financiamiento actualizados 2025."
        ),
        "temas": [
            "Programa de Apoyo Masivo al Autotransporte ($2,250 MDP)",
            "Creditos NAFIN para renovacion de equipo",
            "Esquemas de financiamiento FOJAL y estatales",
            "Requisitos y proceso de solicitud paso a paso",
            "Verificacion de cumplimiento NOM-012",
        ],
        "paginas": 62, "nivel": "Basico", "color": "#EF553B",
        "disponible": True, "badge": "DISPONIBLE",
    },
    {
        "id": "hombre_camion",
        "emoji": "🔧",
        "titulo": "Guia del Hombre-Camion - Renovación Equipo & Apoyos para Transportistas Independientes",
        "subtitulo": "Creditos NAFIN, Plan Masivo y financiamiento para renovación",
        "descripcion": (
            "Disenada para transportistas independientes con 1-5 unidades. "
            "Conoce el Plan de Apoyo Masivo de $2,250 millones de pesos, esquemas de "
            "financiamiento, creditos NAFIN y como aprovecharlos para renovar tu tractocamion. "
            "Incluye checklist completo y contactos SICT."
        ),
        "temas": [
            "Plan de Apoyo Masivo: $2,250 MDP explicado",
            "Creditos NAFIN: requisitos y montos 2025-2026",
            "Financiamiento para tractocamiones nuevos y seminuevos",
            "Deduccion de inversiones y beneficios fiscales",
            "Directorio de gestores y contactos SICT",
            "Checklist de documentos para solicitar apoyos",
        ],
        "paginas": 38, "nivel": "Basico", "color": "#29B5E8",
        "disponible": True, "badge": "DISPONIBLE",
    },
    {
        "id": "nearshoring_101",
        "emoji": "🏭",
        "titulo": "Nearshoring 101 para Transportistas - Logistica Industrial México",
        "subtitulo": "Como posicionar tu flota para la relocalizacion industrial",
        "descripcion": (
            "El nearshoring esta transformando la logistica en Mexico. Esta guia "
            "explica que corredores industriales crecen mas rapido y como posicionar "
            "tu empresa para capturar contratos con empresas manufactureras. Incluye mapa "
            "de parques industriales con mayor demanda en fronteras México-USA."
        ),
        "temas": [
            "Mapa de parques industriales con mayor demanda",
            "Tipos de carga mas frecuentes en nearshoring",
            "Certificaciones: C-TPAT, OEA",
            "Como cotizar rutas industriales de alto valor",
        ],
        "paginas": 44, "nivel": "Intermedio", "color": "#00CC96",
        "disponible": False, "badge": "PROXIMAMENTE",
    },
]


def _render_ebook_card(book):
    color = book["color"]
    badge = book.get("badge", "")
    badge_html = (
        f'<div style="position:absolute;top:12px;right:12px;background:{color};'
        f'color:#fff;font-size:0.65rem;font-weight:700;padding:3px 10px;'
        f'border-radius:20px;letter-spacing:0.08em;">{badge}</div>'
    ) if badge else ""

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#11101D 80%,{color}22);
        border:1px solid {color}55;border-left:4px solid {color};
        border-radius:12px;padding:1.4rem 1.5rem;margin-bottom:0.5rem;position:relative;">
        {badge_html}
        <div style="font-size:2rem;margin-bottom:0.4rem;">{book["emoji"]}</div>
        <div style="font-size:1.1rem;font-weight:700;color:#F4F7F6;margin-bottom:0.2rem;">{book["titulo"]}</div>
        <div style="font-size:0.82rem;color:#29B5E8;margin-bottom:0.7rem;">{book["subtitulo"]}</div>
        <div style="font-size:0.88rem;color:#c8d0e0;line-height:1.6;margin-bottom:0.9rem;">{book["descripcion"]}</div>
        <div style="font-size:0.75rem;color:#8899aa;">
            📄 {book["paginas"]} paginas &nbsp;·&nbsp; Nivel: {book["nivel"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📋 Temas cubiertos"):
        for tema in book["temas"]:
            st.markdown(f"✅ {tema}")
    
    # Agregar botones de lectura y descarga si el ebook está disponible
    if book.get("disponible", False):
        archivo_pdf = _obtener_ruta_ebook(book["id"])
        if archivo_pdf:
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            
            # Botón de descarga
            col_download = st.columns(1)[0]
            with col_download:
                _descargar_ebook(archivo_pdf, book["titulo"].replace(" ", "_"))
            
            # Información del archivo
            try:
                size_mb = archivo_pdf.stat().st_size / (1024 * 1024)
                st.caption(f"📄 Archivo disponible ({size_mb:.1f} MB) - Descarga para leer")
            except:
                st.caption("📄 Descarga el PDF para leer el contenido completo")
        else:
            st.info(f"ℹ️ PDF aún no disponible. Intenta más tarde.")
    
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


def _render_notify_form():
    st.markdown("---")
    st.subheader("📬 Recibe los ebooks cuando esten listos")
    st.caption("Registro gratuito. Solo te avisamos cuando el recurso este disponible.")

    if st.session_state.get("academy_registered"):
        nombre_reg = st.session_state.get("academy_nombre", "")
        st.success(f"Ya estas registrado como **{nombre_reg}**. Te avisaremos por email.")
        if st.button("Cambiar registro", key="academy_reset"):
            st.session_state["academy_registered"] = False
            st.rerun()
        return

    with st.form("academy_notify_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            nombre  = st.text_input("Nombre *", placeholder="Tu nombre completo")
            empresa = st.text_input("Empresa", placeholder="Opcional")
        with col2:
            email  = st.text_input("Email *", placeholder="tu@correo.com")
            perfil = st.selectbox("Tu perfil", [
                "Transportista independiente", "Director de Logistica",
                "Agente Aduanal", "Importador / Exportador",
                "Consultor", "Otro"
            ])

        ebooks_interes = st.multiselect(
            "Que ebooks te interesan?",
            [b["titulo"] for b in EBOOKS],
            default=[b["titulo"] for b in EBOOKS[:2]]
        )

        submitted = st.form_submit_button(
            "Registrarme - Quiero acceso anticipado",
            use_container_width=True, type="primary"
        )

        if submitted:
            if not nombre.strip():
                st.error("Por favor ingresa tu nombre.")
            elif not email.strip() or "@" not in email:
                st.error("Por favor ingresa un email valido.")
            else:
                with st.spinner("Guardando registro..."):
                    ok, msg = _guardar_lead(nombre, email, empresa, perfil, ebooks_interes)
                if ok:
                    st.session_state["academy_registered"] = True
                    st.session_state["academy_nombre"] = nombre.strip()
                    st.success(f"Listo, {nombre.strip()}! Te avisaremos a **{email.strip()}**.")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(msg)


def page_academy():
    # SEO: JSON-LD Schema
    schema = _generate_seo_schema()
    st.markdown(
        f'<script type="application/ld+json">{json.dumps(schema)}</script>',
        unsafe_allow_html=True
    )
    
    st.markdown("""
    <style>
    .academy-hero-title {
        color: #00FF00 !important;
        font-size: 2.2rem !important;
        font-weight: 900 !important;
        margin: 0 0 0.3rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:linear-gradient(135deg,#11101D,#1a1a2e);
        border:1px solid #4070F455;border-radius:16px;
        padding:2rem 2rem 1.5rem;margin-bottom:1.5rem;text-align:center;">
        <div style="font-size:3rem;margin-bottom:0.5rem;">🎓</div>
        <div class="academy-hero-title">
            FreightMetrics Academy
        </div>
        <p style="color:#29B5E8;font-size:1rem;margin:0 0 0.8rem;">
            Inteligencia logistica al alcance de todos
        </p>
        <p style="color:#c8d0e0;font-size:0.9rem;max-width:600px;margin:0 auto;line-height:1.6;">
            Recursos educativos gratuitos para transportistas, directivos y profesionales
            del comercio exterior en Mexico. Aprende sobre logistica transfronteriza México-USA,
            programas de apoyo al autotransporte, KPIs y nearshoring.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Ebooks", len(EBOOKS), "en desarrollo")
    with col2:
        st.metric("Paginas", sum(b["paginas"] for b in EBOOKS))
    with col3:
        st.metric("Enfoque", "MX-USA")
    with col4:
        st.metric("Costo", "$0 MXN")

    st.markdown("---")

    col_f1, col_f2 = st.columns([3, 1])
    with col_f1:
        st.subheader("📚 Biblioteca de Recursos - Ebooks de Logística Transfronteriza")
        st.caption(
            "Aprende sobre transporte México-USA, autotransporte, logística y nearshoring. "
            "Recursos gratuitos diseñados para transportistas, directivos y profesionales del comercio exterior."
        )
    with col_f2:
        nivel_filtro = st.selectbox("Nivel", ["Todos", "Basico", "Intermedio", "Avanzado"],
                                    label_visibility="collapsed")

    libros = EBOOKS if nivel_filtro == "Todos" else [
        b for b in EBOOKS if b["nivel"] == nivel_filtro
    ]

    if not libros:
        st.info(f"No hay ebooks de nivel '{nivel_filtro}' aun.")
    else:
        for book in libros:
            _render_ebook_card(book)

    _render_notify_form()

    st.markdown("---")
    st.markdown(
        f"<p style='text-align:center;color:#8899aa;font-size:0.78rem;'>"
        f"FreightMetrics Academy · Tijuana, BC · Mexico · {datetime.now().strftime('%B %Y')}"
        f"</p>", unsafe_allow_html=True
    )

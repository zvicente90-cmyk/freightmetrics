#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Análisis de archivos Python en el proyecto FreightMetrics
Determina cuáles están activos, cuáles son backup y cuál es su propósito
"""

import sys
import os

archivos = {
    # PÁGINAS PRINCIPALES (EN SIDEBAR)
    "pages/Inicio.py": {
        "categoria": "PÁGINA PRINCIPAL",
        "función": "page_inicio()",
        "estado": "ACTIVA",
        "ubicación": "En pages/",
        "importada_en": "app.py"
    },
    "pages/Mapa.py": {
        "categoria": "PÁGINA PRINCIPAL",
        "función": "page_mapa()",
        "estado": "ACTIVA",
        "ubicación": "En pages/",
        "nombre": "Flujos de Carga Transfronterizos"
    },
    "pages/Fuerza_Laboral.py": {
        "categoria": "PÁGINA PRINCIPAL",
        "función": "page_fuerza_laboral()",
        "estado": "ACTIVA",
        "ubicación": "En pages/",
        "nombre": "Análisis de Fuerza Laboral"
    },
    "pages/Mapa_Autotransporte.py": {
        "categoria": "PÁGINA PRINCIPAL",
        "función": "page_mapa_autotransporte()",
        "estado": "ACTIVA",
        "ubicación": "En pages/",
        "nombre": "Monitoreo de Puertos"
    },
    "pages/Corredores_Logisticos.py": {
        "categoria": "PÁGINA PRINCIPAL",
        "función": "page_corredores_logisticos()",
        "estado": "ACTIVA",
        "ubicación": "En pages/",
        "nombre": "Corredores Logísticos"
    },
    "pages/Nearshoring.py": {
        "categoria": "PÁGINA PRINCIPAL",
        "función": "page_nearshoring()",
        "estado": "ACTIVA",
        "ubicación": "En pages/",
        "nombre": "Análisis de Nearshoring"
    },
    "pages/Monitoreo_Aduanas.py": {
        "categoria": "PÁGINA PRINCIPAL",
        "función": "page_monitoreo_aduanas()",
        "estado": "ACTIVA",
        "ubicación": "En pages/",
        "nombre": "Centro de Monitoreo en Tiempo Real"
    },
    
    # PÁGINAS ADICIONALES (NO EN SIDEBAR)
    "oracle_rate.py": {
        "categoria": "PÁGINA ADICIONAL",
        "función": "page_oracle_rate()",
        "estado": "ACTIVA",
        "ubicación": "Raíz del proyecto",
        "nombre": "Predicción de Tarifas (Oracle Rate)"
    },
    "indice_freightmetrics.py": {
        "categoria": "PÁGINA ADICIONAL",
        "función": "page_indice_freightmetrics()",
        "estado": "POSIBLE (no verificado)",
        "ubicación": "Raíz",
        "nombre": "Índice FreightMetrics"
    },
    "monitoreo_v2.py": {
        "categoria": "PÁGINA ADICIONAL",
        "función": "page_monitoreo_v2()",
        "estado": "POSIBLE (versión alternativa)",
        "ubicación": "Raíz",
        "nombre": "Monitoreo V2 (versión alternativa)"
    },
    
    # ARCHIVOS BACKUP (NO ACTIVOS)
    "page_monitoreo_aduanas_backup.py": {
        "categoria": "BACKUP",
        "estado": "INACTIVO",
        "propósito": "Copia de seguridad de Monitoreo_Aduanas"
    },
    "page_reportes_backup.py": {
        "categoria": "BACKUP",
        "estado": "INACTIVO",
        "propósito": "Copia de seguridad de Reportes"
    },
    "_ARCHIVE_page_alertas.py": {
        "categoria": "ARCHIVO",
        "estado": "INACTIVO",
        "propósito": "Código archivado - Alertas"
    },
    "_ARCHIVE_page_reportes.py": {
        "categoria": "ARCHIVO",
        "estado": "INACTIVO",
        "propósito": "Código archivado - Reportes"
    },
    
    # ARCHIVOS HELPER / UTILIDADES (NO PÁGINAS)
    "monitor_helpers.py": {
        "categoria": "HELPER",
        "estado": "UTILIDAD",
        "propósito": "Funciones auxiliares para monitoreo"
    },
    "monitor_laboral.py": {
        "categoria": "HELPER",
        "estado": "UTILIDAD",
        "propósito": "Monitoreo de datos laborales"
    },
    "page_festivos.py": {
        "categoria": "HELPER",
        "estado": "UTILIDAD",
        "propósito": "Gestión de días festivos"
    },
    "flujos_de_carga.py": {
        "categoria": "HELPER",
        "estado": "UTILIDAD",
        "propósito": "Análisis de flujos de carga (puede estar duplicado con Mapa.py)"
    },
    "corredores_logisticos.py": {
        "categoria": "HELPER",
        "estado": "UTILIDAD",
        "propósito": "Análisis de corredores (puede estar duplicado con Corredores_Logisticos.py)"
    },
    "puertos_maritimos.py": {
        "categoria": "HELPER",
        "estado": "UTILIDAD",
        "propósito": "Análisis de puertos marítimos (puede estar duplicado con Mapa_Autotransporte.py)"
    },
    "mostrar_puertos_frontera.py": {
        "categoria": "SCRIPT",
        "estado": "UTILIDAD",
        "propósito": "Script para mostrar puertos fronterizos"
    },
    "monitorear_bts_2026.py": {
        "categoria": "SCRIPT",
        "estado": "UTILIDAD",
        "propósito": "Monitoreo de datos BTS para 2026"
    },
}

print("=" * 80)
print("ANÁLISIS DE ARCHIVOS PYTHON - FREIGHTMETRICS")
print("=" * 80)

# Categorías
categorias = {
    "PÁGINA PRINCIPAL": [],
    "PÁGINA ADICIONAL": [],
    "HELPER": [],
    "SCRIPT": [],
    "BACKUP": [],
    "ARCHIVO": []
}

for archivo, info in archivos.items():
    cat = info.get("categoria", "OTRO")
    if cat in categorias:
        categorias[cat].append((archivo, info))

# Mostrar por categoría
for cat, items in categorias.items():
    if items:
        print(f"\n{'=' * 80}")
        print(f"{cat} ({len(items)} archivos)")
        print(f"{'=' * 80}")
        for archivo, info in items:
            print(f"\n📄 {archivo}")
            print(f"   Estado: {info.get('estado', 'DESCONOCIDO')}")
            if info.get('función'):
                print(f"   Función: {info.get('función')}")
            if info.get('nombre'):
                print(f"   Nombre: {info.get('nombre')}")
            if info.get('propósito'):
                print(f"   Propósito: {info.get('propósito')}")
            if info.get('ubicación'):
                print(f"   Ubicación: {info.get('ubicación')}")
            if info.get('importada_en'):
                print(f"   Importada en: {info.get('importada_en')}")

print("\n" + "=" * 80)
print("RESUMEN")
print("=" * 80)
print(f"✅ PÁGINAS ACTIVAS: {len(categorias['PÁGINA PRINCIPAL'])} + {len(categorias['PÁGINA ADICIONAL'])}")
print(f"🛠️  HELPERS/SCRIPTS: {len(categorias['HELPER'])} + {len(categorias['SCRIPT'])}")
print(f"📦 BACKUP: {len(categorias['BACKUP'])}")
print(f"📁 ARCHIVADO: {len(categorias['ARCHIVO'])}")
print("=" * 80)

print("\n⚠️ DUPLICADOS POSIBLES:")
print("  - flujos_de_carga.py (¿Es helper de Mapa.py?)")
print("  - corredores_logisticos.py (¿Es helper de Corredores_Logisticos.py en pages/?)")
print("  - puertos_maritimos.py (¿Es helper de Mapa_Autotransporte.py?)")

print("\n📌 RECOMENDACIONES:")
print("  1. Los BACKUP pueden ser eliminados (tienen copia en pages/)")
print("  2. Los ARCHIVOS (_ARCHIVE_) pueden ser movidos a carpeta antigua")
print("  3. Verificar si los helpers son realmente usados o pueden ser consolidados en app.py")
print("=" * 80)

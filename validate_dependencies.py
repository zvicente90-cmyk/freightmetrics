"""
Script de validación de dependencias críticas.
Ejecutar ANTES de iniciar Streamlit.
"""

import sys
import importlib

CRITICAL_MODULES = [
    "streamlit",
    "pandas",
    "numpy",
    "folium",
    "streamlit_folium",
    "plotly",
    "requests",
]

MISSING = []

for module in CRITICAL_MODULES:
    try:
        importlib.import_module(module)
        print(f"✅ {module}")
    except ImportError:
        print(f"❌ {module} — FALTA")
        MISSING.append(module)

if MISSING:
    print(f"\n⚠️  Faltan {len(MISSING)} módulo(s):")
    for m in MISSING:
        print(f"   - {m}")
    print("\nInstalar con:")
    print(f"   pip install {' '.join(MISSING)}")
    sys.exit(1)
else:
    print("\n✅ Todas las dependencias OK")
    sys.exit(0)

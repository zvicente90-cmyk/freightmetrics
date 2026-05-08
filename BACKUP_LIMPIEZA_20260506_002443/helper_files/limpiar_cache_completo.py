#!/usr/bin/env python3
"""
Limpia la cache de Streamlit completamente para que los cambios sean visibles
"""

import os
import shutil
from pathlib import Path

print("🧹 LIMPIANDO CACHE DE STREAMLIT...")
print("=" * 60)

# Limpiar __pycache__
for root, dirs, files in os.walk("."):
    if "__pycache__" in dirs:
        cache_dir = os.path.join(root, "__pycache__")
        shutil.rmtree(cache_dir, ignore_errors=True)
        print(f"✓ Eliminado: {cache_dir}")

# Limpiar .streamlit/cache
cache_paths = [
    Path.home() / ".streamlit" / "cache",
    Path(".") / ".streamlit" / "cache",
]

for cache_path in cache_paths:
    if cache_path.exists():
        shutil.rmtree(cache_path, ignore_errors=True)
        print(f"✓ Eliminado: {cache_path}")

print("\n" + "=" * 60)
print("✅ Cache limpiada completamente")
print("\n🚀 PRÓXIMO PASO: Ejecuta")
print("   streamlit run app.py")
print("\nAbre la página en navegador y ve directamente a:")
print("   📊 Monitoreo de Aduanas")
print("\n💡 DEBERÍAS VER:")
print("   • 4 tarjetas azules profesionales (Indicadores Principales)")
print("   • Tarjetas verdes para México")  
print("   • Tarjetas azules para Canadá")
print("   • Tarjetas de colores para Benchmarks")
print("   • Estilos con bordes, sombras y degradados")

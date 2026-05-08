#!/usr/bin/env python3
"""
Script de Limpieza de Caché de Streamlit
Elimina toda la caché compilada y de Streamlit
"""

import os
import shutil
import subprocess
from pathlib import Path
import sys

def limpiar_cache():
    """Limpia toda la caché de Streamlit y Python"""
    
    print("=" * 80)
    print("🧹 LIMPIEZA DE CACHÉ DE STREAMLIT")
    print("=" * 80)
    
    proyecto_dir = Path.cwd()
    
    # Lista de directorios a limpiar
    directorios_limpiar = [
        proyecto_dir / "__pycache__",
        proyecto_dir / ".streamlit" / "cache",
        proyecto_dir / "page_modules" / "__pycache__",
        proyecto_dir / "modules" / "__pycache__",
    ]
    
    archivos_limpiar = [
        proyecto_dir / ".streamlit" / "cache.json",
    ]
    
    # Limpiar directorios
    print("\n📁 Eliminando directorios de caché...")
    for directorio in directorios_limpiar:
        if directorio.exists():
            try:
                shutil.rmtree(directorio)
                print(f"   ✅ Eliminado: {directorio.name}")
            except Exception as e:
                print(f"   ⚠️ No se pudo eliminar {directorio.name}: {e}")
        else:
            print(f"   ⏭️  No existe: {directorio.name}")
    
    # Limpiar archivos
    print("\n📄 Eliminando archivos de caché...")
    for archivo in archivos_limpiar:
        if archivo.exists():
            try:
                archivo.unlink()
                print(f"   ✅ Eliminado: {archivo.name}")
            except Exception as e:
                print(f"   ⚠️ No se pudo eliminar {archivo.name}: {e}")
    
    # Buscar y limpiar todos los __pycache__ recursivamente
    print("\n🔍 Buscando y limpiando __pycache__ recursivamente...")
    contador = 0
    for pycache_dir in proyecto_dir.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache_dir)
            contador += 1
        except Exception as e:
            pass
    
    if contador > 0:
        print(f"   ✅ Eliminados {contador} directorios __pycache__")
    else:
        print(f"   ⏭️  No se encontraron directorios __pycache__")
    
    # Buscar y eliminar archivos .pyc
    print("\n🔍 Buscando y limpiando archivos .pyc...")
    contador_pyc = 0
    for pyc_file in proyecto_dir.rglob("*.pyc"):
        try:
            pyc_file.unlink()
            contador_pyc += 1
        except Exception as e:
            pass
    
    if contador_pyc > 0:
        print(f"   ✅ Eliminados {contador_pyc} archivos .pyc")
    else:
        print(f"   ⏭️  No se encontraron archivos .pyc")
    
    # Limpiar caché de usuario de Streamlit
    print("\n🏠 Limpiando caché global de Streamlit...")
    home_streamlit = Path.home() / ".cache" / "streamlit"
    if home_streamlit.exists():
        try:
            shutil.rmtree(home_streamlit)
            print(f"   ✅ Caché global eliminada")
        except Exception as e:
            print(f"   ⚠️ No se pudo limpiar caché global: {e}")
    else:
        print(f"   ⏭️  Caché global no encontrada")
    
    print("\n" + "=" * 80)
    print("✨ LIMPIEZA COMPLETADA")
    print("=" * 80)
    print("""
🎯 PRÓXIMOS PASOS:

1. Si Streamlit está corriendo, presiona CTRL+C en la terminal para detenerlo
2. Ejecuta de nuevo:
   
   streamlit run app.py

3. En el navegador, presiona "C" para limpiar la caché del navegador
   (u obtén una nueva sesión privada)

4. Navega a "Monitoreo de Aduanas"

5. ¡Ahora deberías ver todos los cambios con las tarjetas bonitas!

═════════════════════════════════════════════════════════════════════════════

💡 TIPS ADICIONALES:

• Si aún no ves los cambios:
  1. Abre DevTools (F12 en navegador)
  2. Ve a "Network" y marca "Disable cache"
  3. Recarga la página (F5 o Ctrl+Shift+R)

• Si usas Streamlit Cloud:
  1. Haz push de los cambios a GitHub
  2. La app se recargará automáticamente
  3. Limpia la caché del navegador

═════════════════════════════════════════════════════════════════════════════
    """)

if __name__ == "__main__":
    try:
        limpiar_cache()
    except KeyboardInterrupt:
        print("\n⚠️ Limpieza cancelada por el usuario")
        sys.exit(1)

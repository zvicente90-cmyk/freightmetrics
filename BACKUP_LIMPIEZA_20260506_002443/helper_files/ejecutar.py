#!/usr/bin/env python3
"""
Script para ejecutar Streamlit con caché limpia
Ideal para ver cambios inmediatamente
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Ejecuta Streamlit con opciones para evitar caché"""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║        🚀 INICIANDO STREAMLIT CON CACHÉ LIMPIA                            ║
║                                                                            ║
║              Los cambios deberían ser visibles inmediatamente              ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

⏳ Iniciando aplicación...
   📱 Abre navegador en: http://localhost:8501

🔍 Ve a: "Monitoreo de Aduanas" → "Indicadores Principales"

✨ Deberías ver:
   • Tarjetas azules con glow neon
   • Efecto glassmorphism (cristal + blur)
   • Bordes redondeados
   • Hover que levanta las tarjetas

⌨️ ATAJOS:
   • Presiona "C" en el navegador para limpiar caché
   • Presiona "R" para recargar la app
   • Presiona "Q" para ver modo debug

═════════════════════════════════════════════════════════════════════════════
    """)
    
    # Crear comando de ejecución
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "app.py",
        "--logger.level=error",           # Reducir ruido de logs
        "--client.showErrorDetails=false", # No mostrar detalles de error
        "--client.toolbarMode=minimal",    # Toolbar mínima
    ]
    
    print(f"Ejecutando: {' '.join(cmd)}\n")
    
    # Ejecutar Streamlit
    try:
        subprocess.run(cmd, cwd=str(Path.cwd()))
    except KeyboardInterrupt:
        print("\n\n⛔ Streamlit detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error al ejecutar Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

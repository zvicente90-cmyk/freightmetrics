#!/usr/bin/env python3
"""Validar que los renombres de funciones se completaron correctamente"""

import sys

try:
    from pages._00_Inicio import page_dashboard
    print("✅ page_dashboard importado correctamente")
except Exception as e:
    print(f"❌ Error importando page_dashboard: {e}")
    sys.exit(1)

try:
    from pages._02_Mapa import page_flujos_de_carga
    print("✅ page_flujos_de_carga importado correctamente")
except Exception as e:
    print(f"❌ Error importando page_flujos_de_carga: {e}")
    sys.exit(1)

try:
    from pages._05_Mapa_Autotransporte import page_puertos_maritimos
    print("✅ page_puertos_maritimos importado correctamente")
except Exception as e:
    print(f"❌ Error importando page_puertos_maritimos: {e}")
    sys.exit(1)

print("\n✅ Todos los renombres de funciones funcionan correctamente")

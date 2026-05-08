#!/usr/bin/env python3
"""Check what columns exist in simulated 2026 data"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Simular la creación de datos como lo hace obtener_datos_cruces_consolidados
print("Simulando qué columnas tendría df_border...\n")

# Puertos de prueba
puertos_mexico = ['Nuevo Laredo III (Comercio Mundial)', 'Tijuana (Mesa de Otay)']
puertos_canada = ['Vancouver', 'Detroit']

fechas = pd.date_range('2026-01-01', '2026-01-10', freq='D')
data = []

np.random.seed(42)
for puerto in puertos_mexico:
    for fecha in fechas:
        cruces = 567
        cruces_fast = int(cruces * 0.40)
        cruces_regular = int(cruces * 0.55)
        cruces_perecederos = int(cruces * 0.05)
        cruces_total = cruces_fast + cruces_regular + cruces_perecederos
        
        trucks = int(cruces_total * 0.60)
        trucks_loaded = int(cruces_total * 0.30)
        trucks_empty = int(cruces_total * 0.10)
        
        data.append({
            'Fecha': fecha,
            'Puerto': puerto,
            'Cruces': cruces_total,
            'Cruces_FAST': cruces_fast,
            'Cruces_Regular': cruces_regular,
            'Cruces_Perecederos': cruces_perecederos,
            'Trucks': trucks,
            'Trucks_Loaded': trucks_loaded,
            'Trucks_Empty': trucks_empty,
            'Frontera': 'México'
        })

df = pd.DataFrame(data)

print("COLUMNAS EN df_border (simulado):")
print("-" * 60)
for col in sorted(df.columns):
    print(f"  ✓ {col}")

print("\n\nPRUEBA: Intentar acceder a columnas esperadas por page_mapa():")
print("-" * 60)

test_columns = [
    'Trucks',
    'Trucks_Loaded',
    'Trucks_Empty',
    'Truck Containers Loaded',
    'Truck Containers Empty',
    'Cruces',
    'Cruces_FAST'
]

for col in test_columns:
    exists = col in df.columns
    status = "✓" if exists else "✗"
    print(f"  {status} {col}")

print("\n\nPROBLEMA DETECTADO:")
print("-" * 60)
print("Las columnas 'Truck Containers Loaded/Empty' NO existen")
print("Pero el código en page_mapa() las busca en líneas 3351, 3359")
print("\nLa solución sería:")
print("1. Renombrar Trucks_Loaded → Truck Containers Loaded")
print("2. Renombrar Trucks_Empty → Truck Containers Empty")
print("3. O actualizar page_mapa() para usar Trucks_Loaded/Trucks_Empty")

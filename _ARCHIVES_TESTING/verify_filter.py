#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify that Mexico filter is working correctly for Jan-Feb 2026"""

import pandas as pd
import numpy as np
from datetime import datetime

# Simular datos como si fuera la aplicación
print("=" * 80)
print("VERIFICACION: Filtro de Mexico en Enero-Febrero 2026")
print("=" * 80)

# Simular datos básicos
puertos_mexico = ['Nuevo Laredo', 'Tijuana', 'Mexicali', 'Laredo']
puertos_canada = ['Vancouver', 'Detroit', 'Buffalo', 'Seattle']

fechas_enero = pd.date_range('2026-01-01', '2026-01-31', freq='D')
fechas_feb = pd.date_range('2026-02-01', '2026-02-28', freq='D')

data = []
np.random.seed(42)

# Datos México
for puerto in puertos_mexico:
    for fecha in fechas_enero:
        cruces = int(567 * np.random.uniform(0.85, 1.15))
        trucks = int(cruces * 0.60)
        trucks_loaded = int(cruces * 0.30)
        trucks_empty = int(cruces * 0.10)
        data.append({
            'Fecha': fecha,
            'Puerto': puerto,
            'Frontera': 'México',
            'Cruces': cruces,
            'Trucks': trucks,
            'Trucks_Loaded': trucks_loaded,
            'Trucks_Empty': trucks_empty
        })
    
    for fecha in fechas_feb:
        cruces = int(567 * np.random.uniform(0.85, 1.15))
        trucks = int(cruces * 0.60)
        trucks_loaded = int(cruces * 0.30)
        trucks_empty = int(cruces * 0.10)
        data.append({
            'Fecha': fecha,
            'Puerto': puerto,
            'Frontera': 'México',
            'Cruces': cruces,
            'Trucks': trucks,
            'Trucks_Loaded': trucks_loaded,
            'Trucks_Empty': trucks_empty
        })

# Datos Canada
for puerto in puertos_canada:
    for fecha in fechas_enero:
        cruces = int(450 * np.random.uniform(0.85, 1.15))
        trucks = int(cruces * 0.60)
        trucks_loaded = int(cruces * 0.30)
        trucks_empty = int(cruces * 0.10)
        data.append({
            'Fecha': fecha,
            'Puerto': puerto,
            'Frontera': 'Canadá',
            'Cruces': cruces,
            'Trucks': trucks,
            'Trucks_Loaded': trucks_loaded,
            'Trucks_Empty': trucks_empty
        })
    
    for fecha in fechas_feb:
        cruces = int(450 * np.random.uniform(0.85, 1.15))
        trucks = int(cruces * 0.60)
        trucks_loaded = int(cruces * 0.30)
        trucks_empty = int(cruces * 0.10)
        data.append({
            'Fecha': fecha,
            'Puerto': puerto,
            'Frontera': 'Canadá',
            'Cruces': cruces,
            'Trucks': trucks,
            'Trucks_Loaded': trucks_loaded,
            'Trucks_Empty': trucks_empty
        })

df_border = pd.DataFrame(data)

print("\n[1] DATOS INICIALES (sin filtrar):")
print("-" * 80)
print(f"Total registros: {len(df_border):,}")
print(f"Total Cruces (ambas): {df_border['Cruces'].sum():,}")

print("\n[2] APLICAR FILTRO: Solo Mexico")
print("-" * 80)

# Este es el filtro que debería aplicarse en page_mapa
border_selected = ['México']  # Lo que se establece cuando selecciona "🇲🇽 México"
df_filtrado = df_border[df_border['Frontera'].isin(border_selected)].copy()

print(f"border_selected = {border_selected}")
print(f"Registros despues filtro: {len(df_filtrado):,}")
print(f"Total Cruces (SOLO Mexico): {df_filtrado['Cruces'].sum():,}")

# Ahora filtra por fecha (enero-febrero)
fecha_inicio = pd.to_datetime('2026-01-01')
fecha_fin = pd.to_datetime('2026-02-28')
df_periodo = df_filtrado[(df_filtrado['Fecha'] >= fecha_inicio) & (df_filtrado['Fecha'] <= fecha_fin)].copy()

print("\n[3] APLICAR FILTRO: Enero-Febrero 2026")
print("-" * 80)
print(f"Rango: {fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}")
print(f"Total registros del periodo: {len(df_periodo):,}")
print(f"Total Cruces: {df_periodo['Cruces'].sum():,}")

# Calcular métricas
total_trucks = df_periodo['Trucks'].sum()
total_loaded = df_periodo['Trucks_Loaded'].sum()
total_empty = df_periodo['Trucks_Empty'].sum()
total_cruces = df_periodo['Cruces'].sum()

print("\n[4] METRICAS DEL DASHBOARD (ESPERADAS):")
print("-" * 80)
print(f"Total Cruces:      {total_cruces:>12,}")
print(f"Trucks:            {total_trucks:>12,} ({total_trucks/total_cruces*100:.1f}%)")
print(f"Containers Loaded: {total_loaded:>12,} ({total_loaded/total_cruces*100:.1f}%)")
print(f"Containers Empty:  {total_empty:>12,} ({total_empty/total_cruces*100:.1f}%)")
print(f"Suma verificacion: {total_trucks + total_loaded + total_empty:>12,}")

print("\n[5] COMPARACION CON LO QUE USUARIO REPORTA:")
print("-" * 80)
print(f"Usuario ve:        {1668428:>12,}")
print(f"Esperado (Mexico): {total_cruces:>12,}")
print(f"Diferencia:        {1668428 - total_cruces:>12,}")

if 1668428 > total_cruces and 1668428 > total_cruces * 1.8:
    print(f"\n[PROBLEMA DETECTADO]")
    print(f"El usuario sigue viendo ambas fronteras combinadas (~1.67M)")
    print(f"Esto significa que NO se está aplicando el filtro de Mexico")
    print(f"\nPosibles causas:")
    print(f"  1. Usuario no recargó la página (ctrl+F5 para limpiar caché)")
    print(f"  2. Hay un problema con session_state de Streamlit")
    print(f"  3. El filtro no se está persistiendo correctamente")
else:
    print(f"\n[OK] Los números coinciden con México filtrado")

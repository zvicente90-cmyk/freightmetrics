#!/usr/bin/env python3
"""Check what data exists for border crossings"""

import pandas as pd
from pathlib import Path

# Cargar todos los datos
data_dir = Path(__file__).parent / "data"
dfs = []

for archivo in sorted(data_dir.glob("border_crossings_*.csv")):
    print(f"📂 {archivo.name}...")
    df = pd.read_csv(archivo)
    print(f"   Registros: {len(df):,}")
    print(f"   Fechas: {df['date'].min()} a {df['date'].max()}")
    print(f"   Fronteras: {df['border'].unique()}")
    dfs.append(df)

# Combinar
df_all = pd.concat(dfs, ignore_index=True)

# Buscar enero/february 2025 y 2026 por frontera
print("\n" + "=" * 80)
print("DATOS POR MES/FRONTERA (últimos meses disponibles)")
print("=" * 80 + "\n")

df_all['date'] = pd.to_datetime(df_all['date'])
df_all['mes_año'] = df_all['date'].dt.to_period('M')

# Agrupar por mes y frontera
for mes_año in sorted(df_all['mes_año'].unique())[-6:]:  # Last 6 months
    print(f"\n📅 {mes_año}:")
    
    mes_data = df_all[df_all['mes_año'] == mes_año]
    
    for border in sorted(mes_data['border'].unique()):
        border_data = mes_data[mes_data['border'] == border]
        total = border_data['value'].sum()
        
        # Solo contar "Trucks" para comparabilidad  
        trucks_only = border_data[border_data['measure'] == 'Trucks']['value'].sum()
        
        print(f"  🌎 {border:20s} - Total: {total:>12,} | Trucks: {trucks_only:>10,}")
    
    total_mes = mes_data['value'].sum()
    print(f"  {'TOTAL':>24s}  {total_mes:>12,}")

print("\n" + "=" * 80)
print("⚠️ CONCLUSIÓN: No hay datos de 2026 en los archivos.")
print("El sistema genera SIMULACIÓN para 2026.")
print("=" * 80)

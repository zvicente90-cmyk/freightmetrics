#!/usr/bin/env python3
"""Debug script - versión sin Streamlit"""

import pandas as pd
import sys
import os

# Agregr ruta al sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Cargar funciones necesarias sin Streamlit
from pathlib import Path

def leer_csv_bts_robusto(archivo):
    """Lee CSV con manejo robusto de formatos BTS variados"""
    try:
        df = pd.read_csv(archivo)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

def debug_fronteras():
    """Analizar distribución de datos por frontera"""
    
    print("\n" + "=" * 80)
    print("DEBUGING: Verificando distribución de datos por frontera")
    print("=" * 80 + "\n")
    
    # Cargar archivos BTS directamente
    data_dir = Path(__file__).parent / "data"
    
    archivos = [
        data_dir / "border_crossings_2026_historical.csv",
        data_dir / "border_crossings_2025_historical.csv",
        data_dir / "border_crossings_2024_historical.csv",
        data_dir / "border_crossings_2023_historical.csv"
    ]
    
    dfs = []
    for archivo in archivos:
        if archivo.exists():
            try:
                print(f"📂 Cargando {archivo.name}...")
                df = pd.read_csv(archivo)
                print(f"   ✓ {len(df):,} registros")
                dfs.append(df)
            except Exception as e:
                print(f"   ✗ Error: {e}")
    
    if not dfs:
        print("❌ No se encontraron archivos CSV")
        return
    
    df_combined = pd.concat(dfs, ignore_index=True)
    print(f"\n📊 Total combinado: {len(df_combined):,} registros\n")
    
    # Ver estructura
    print("COLUMNAS:")
    for col in df_combined.columns:
        print(f"  - {col}")
    
    # Ver primeras filas
    print(f"\nPRIMERAS FILAS:")
    print(df_combined.head(3).to_string())
    
    # Analizar enero 2026
    print(f"\n" + "=" * 80)
    print("ANÁLISIS: Enero 2026")
    print("=" * 80 + "\n")
    
    # Convertir fecha a datetime
    if 'date' in df_combined.columns:
        df_combined['date'] = pd.to_datetime(df_combined['date'])
        df_enero_2026 = df_combined[
            (df_combined['date'] >= '2026-01-01') & 
            (df_combined['date'] <= '2026-01-31')
        ].copy()
    else:
        print("⚠️ Columna 'date' no encontrada")
        df_enero_2026 = pd.DataFrame()
    
    if not df_enero_2026.empty:
        print(f"Registros enero 2026: {len(df_enero_2026):,}\n")
        
        # Agrupar por frontera y medida
        if 'border' in df_enero_2026.columns and 'measure' in df_enero_2026.columns and 'value' in df_enero_2026.columns:
            print("TOTALES POR FRONTERA Y MEDIDA:")
            summary = df_enero_2026.groupby(['border', 'measure'])['value'].sum().reset_index()
            print(summary.to_string(index=False))
            
            # Comparar con la medida de cruces totales
            print("\n\nTOTAL POR FRONTERA:")
            total_frontera = df_enero_2026.groupby('border')['value'].sum().sort_values(ascending=False)
            for border, total in total_frontera.items():
                print(f"  🌎 {border}: {total:,.0f}")
            
            print(f"\n  🌍 TOTAL COMBINADO: {total_frontera.sum():,.0f}")
            print(f"\n  📊 Comparación con usuario:")
            print(f"     - Mostrado en app: 1,668,428")
            print(f"     - BTS México solamente: 840,501")
            print(f"     -Nuestro total: {total_frontera.sum():,.0f}")
        else:
            print("⚠️ Columnas 'border', 'measure', 'value' no encontradas")
    else:
        print("⚠️ No hay datos para enero 2026")

if __name__ == "__main__":
    debug_fronteras()

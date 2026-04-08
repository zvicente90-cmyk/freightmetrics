#!/usr/bin/env python3
"""Debug script para verificar distribución de datos por frontera"""

import pandas as pd
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/Users/Vicente Sanchez/Documents/VICENTE DOCKER/CODIGO PRUEBAS FREIGHTMETRICS')

# Importar la función
from app import obtener_datos_cruces_consolidados

def debug_fronteras():
    """Analizar distribución de cruces por frontera"""
    
    print("=" * 80)
    print("DEBUGING: Verificando distribución de datos por frontera")
    print("=" * 80)
    
    # Cargar datos
    df_border, _ = obtener_datos_cruces_consolidados(usar_datos_reales=True, incluir_simulacion_2026=True)
    
    print(f"\n📊 CARGA INICIAL:")
    print(f"  - Total registros: {len(df_border):,}")
    print(f"  - Fechas: {df_border['Fecha'].min()} a {df_border['Fecha'].max()}")
    print(f"  - Frontera única: {'Frontera' in df_border.columns}")
    
    if 'Frontera' in df_border.columns:
        print(f"\n🌎 FRONTERA UNIQUE VALUES:")
        print(df_border['Frontera'].unique())
        print(f"\n📈 CRUCES POR FRONTERA (TOTAL):")
        frontera_stats = df_border.groupby('Frontera')['Cruces'].agg(['sum', 'count', 'mean'])
        print(frontera_stats)
    
    # Analizar enero 2026
    print(f"\n" + "=" * 80)
    print("ANÁLISIS: Enero 2026")
    print("=" * 80)
    
    df_enero_2026 = df_border[
        (df_border['Fecha'] >= '2026-01-01') & 
        (df_border['Fecha'] <= '2026-01-31')
    ].copy()
    
    print(f"\nRecords en enero 2026: {len(df_enero_2026):,}")
    print(f"Total cruces enero 2026: {df_enero_2026['Cruces'].sum():,}")
    
    if 'Frontera' in df_enero_2026.columns:
        print(f"\n📍 ENERO 2026 POR FRONTERA:")
        frontera_enero = df_enero_2026.groupby('Frontera').agg({
            'Cruces': ['sum', 'count'],
            'Trucks': 'sum' if 'Trucks' in df_enero_2026.columns else lambda x: 0,
            'Trucks_Loaded': 'sum' if 'Trucks_Loaded' in df_enero_2026.columns else lambda x: 0,
            'Trucks_Empty': 'sum' if 'Trucks_Empty' in df_enero_2026.columns else lambda x: 0,
        }).round(0)
        print(frontera_enero)
        
        # Comparar con lo que el usuario reporta
        mexico_total = df_enero_2026[df_enero_2026['Frontera'] == 'México']['Cruces'].sum()
        canada_total = df_enero_2026[df_enero_2026['Frontera'] == 'Canadá']['Cruces'].sum()
        
        print(f"\n🇲🇽 México enero 2026: {mexico_total:,}")
        print(f"🇨🇦 Canadá enero 2026: {canada_total:,}")
        print(f"🌎 TOTAL (Ambas): {mexico_total + canada_total:,}")
        print(f"\n👤 Usuario reporta BTS México: 840,501")
        print(f"🔍 Concordancia: {abs(mexico_total - 840501) < 50000}")
        
        # Verificar si es doble conteo
        if (mexico_total + canada_total) > 1600000:
            print(f"\n⚠️  POSIBLE PROBLEMA: Total ({mexico_total + canada_total:,}) es muy alto")
            
            # Análisis de puertos
            print(f"\n📍 PUERTOS ÚNICOS EN ENERO 2026:")
            puerto_frontera = df_enero_2026.groupby('Frontera')['Puerto'].nunique()
            print(puerto_frontera)
            
            print(f"\n🏛️ PUERTOS EN MÉXICO:")
            puertos_mexico = df_enero_2026[df_enero_2026['Frontera'] == 'México']['Puerto'].unique()
            for p in sorted(puertos_mexico):
                total_p = df_enero_2026[df_enero_2026['Puerto'] == p]['Cruces'].sum()
                print(f"   - {p}: {total_p:,}")
    
    # Verificar columnas de cruces
    print(f"\n" + "=" * 80)
    print("COLUMNAS RELACIONADAS CON CRUCES:")
    print("=" * 80)
    
    columnas_cruces = [col for col in df_border.columns if 'cruz' in col.lower() or 'truck' in col.lower()]
    print(f"Columnas encontradas: {columnas_cruces}")
    
    # Verificar si hay duplicados
    print(f"\n" + "=" * 80)
    print("VERIFICAR DUPLICADOS:")
    print("=" * 80)
    
    df_test = df_enero_2026[['Fecha', 'Puerto', 'Frontera', 'Cruces']].copy()
    duplicate_rows = df_test.duplicated(subset=['Fecha', 'Puerto', 'Frontera'], keep=False)
    print(f"¿Hay duplicados (Fecha+Puerto+Frontera)?: {duplicate_rows.any()}")
    if duplicate_rows.any():
        print(f"  - Registros duplicados: {duplicate_rows.sum()}")
        print(df_test[duplicate_rows].sort_values(['Fecha', 'Puerto']))

if __name__ == "__main__":
    debug_fronteras()

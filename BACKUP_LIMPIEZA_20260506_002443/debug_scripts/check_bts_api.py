#!/usr/bin/env python3
"""Check BTS API for January 2026 data"""

import requests
import json
from datetime import datetime

# BTS API endpoint
url = "https://data.bts.gov/resource/keg4-3bc2.json"

# Query for January 2026, US-Mexico Border, Trucks
params = {
    "$select": "date, port_name, measure, value, border",
    "$where": "date >= '2026-01-01' AND date < '2026-02-01' AND border = 'US-Mexico Border'",
    "$limit": 1000
}

try:
    print("🌐 Consultando BTS API para enero 2026 (Frontera México)...")
    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ {len(data):,} registros encontrados\n")
        
        # Procesar datos
        total_por_medida = {}
        total_general = 0
        
        for record in data:
            med = record.get('measure', 'Unknown')
            val = int(record.get('value', 0))
            
            if med not in total_por_medida:
                total_por_medida[med] = 0
            
            total_por_medida[med] += val
            total_general += val
        
        print("TOTALES POR MEDIDA (enero 2026, México):")
        print("-" * 60)
        for medida, total in sorted(total_por_medida.items(), key=lambda x: -x[1]):
            pct = (total / total_general * 100) if total_general > 0 else 0
            print(f"  {medida:40s}: {total:>12,} ({pct:5.1f}%)")
        
        print("-" * 60)
        print(f"  {'TOTAL':40s}: {total_general:>12,}")
        
        print("\n📊 COMPARACIÓN:")
        print(f"  BTS actual (API):              {total_general:>12,}")
        print(f"  Usuario reporta:               {840501:>12,}")
        print(f"  App muestra (Ambas fronteras): {1668428:>12,}")
        
        if abs(total_general - 840501) < 10000:
            print("\n✓ Los números coinciden con BTS")
        elif total_general > 0:
            ratio = total_general / 840501
            print(f"\n⚠️ Discrepancia: Relación = {ratio:.2f}x")
        
        # Mostrar primeros registros
        print("\n\nPRIMEROS REGISTROS:")
        print("-" * 60)
        for i, record in enumerate(data[:5]):
            print(f"{record.get('date', 'N/A')} | {record.get('port_name', 'N/A'):25s} | {record.get('measure', 'N/A'):30s} | {record.get('value', 'N/A')}")
    
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text[:500])

except Exception as e:
    print(f"❌ Error: {e}")
    print("\nℹ️ Si BTS API no está disponible, los datos podrían ser históricos/cached")

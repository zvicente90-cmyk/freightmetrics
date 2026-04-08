#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

data_dir = Path("data")

# Check 2025 historical
arquivo_2025 = data_dir / "border_crossings_2025_historical.csv"
if arquivo_2025.exists():
    df = pd.read_csv(arquivo_2025)
    df['date'] = pd.to_datetime(df['date'])
    print(f"2025 Historical: {len(df)} registros, {df['date'].min()} a {df['date'].max()}")
else:
    print("2025 file not found")

# Check 2026 current
arquivo_2026 = data_dir / "border_crossings_2026_current.csv"
if arquivo_2026.exists():
    df = pd.read_csv(arquivo_2026)
    df['date'] = pd.to_datetime(df['date'])
    enero_feb = df[(df['date'].dt.month <= 2) & (df['date'].dt.year == 2026)]
    print(f"2026 Current: {len(df)} registros")
    print(f"  Rango: {df['date'].min()} a {df['date'].max()}")
    print(f"  Enero-Febrero 2026: {len(enero_feb)} registros")
else:
    print("2026 file not found")

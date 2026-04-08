import pandas as pd

# Cargar los archivos para ver qué fechas tienen
years = [2023, 2024, 2025, 2026]

for year in years:
    try:
        file = f"data/border_crossings_{year}_historical.csv"
        df = pd.read_csv(file)
        
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            min_date = df['date'].min()
            max_date = df['date'].max()
            unique_years = sorted(df['date'].dt.year.unique())
            print(f"✅ {year}: Min={min_date}, Max={max_date}, Años={unique_years}")
        else:
            print(f"❌ {year}: No tiene columna 'date'")
            print(f"   Columnas: {df.columns.tolist()}")
    except Exception as e:
        print(f"❌ {year}: Error - {e}")

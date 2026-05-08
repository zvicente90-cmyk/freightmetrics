#!/usr/bin/env python
import pandas as pd
from pathlib import Path

data_dir = Path('data')
archivo = data_dir / 'border_crossings_2026_historical.csv'
df = pd.read_csv(archivo)

print('Columnas del CSV:')
print(list(df.columns))

print('\nPrimeras 5 filas:')
print(df.head())

print('\nValores únicos en "measure":')
print(df['measure'].unique())

print('\nForma del DataFrame:')
print(df.shape)

# Ahora verificar cómo se ve después de pivotear
print('\n\nDespués de pivotar:')
df['date'] = pd.to_datetime(df['date'])
df['Periodo'] = df['date'].dt.strftime('%Y-%m')

df_pivot = df.groupby(['Periodo', 'measure'])['value'].sum().unstack(fill_value=0)
print(df_pivot.head())
print('\nColumnas pivotadas:')
print(list(df_pivot.columns))

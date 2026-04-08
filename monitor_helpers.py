import pandas as pd
import random


# --- DATOS DE FUERZA LABORAL ---
def obtener_datos_fuerza_laboral():
    segmentacion = {
        'Segmento': ['Hombre-Camión', 'Pequeña', 'Mediana', 'Grande'],
        'Rango Unidades': ['1 - 5', '6 - 30', '31 - 100', '101+'],
        'Número de Empresas': [163200, 29800, 4500, 1000],  # Total: ~198,500
        'Total Operadores': [196000, 227000, 125000, 82000],  # Total: ~630,000 (considerando déficit de 99k según IRU 2024)
        'Participación Mercado': ['82.2%', '15.0%', '2.3%', '0.5%']
    }
    df_segmentos = pd.DataFrame(segmentacion)

    cruce_data = pd.DataFrame({
        'Segmento': ['Hombre-Camión', 'Pequeña', 'Mediana', 'Grande'],
        'Operan solo MX': [98, 70, 40, 15],
        'Operan MC (Cruce)': [2, 30, 60, 85]
    })

    return df_segmentos, cruce_data


# --- DATOS REGIONALES DE FUERZA LABORAL POR ESTADO FRONTERIZO ---
def obtener_datos_fuerza_laboral_regional():
    """
    Retorna datos de parque vehicular, permisionarios y empresas con MC
    por región/estado fronterizo.
    """
    datos_regionales = {
        'Region': ['Baja California', 'Sonora', 'Chihuahua', 'Coahuila', 'Nuevo León', 'Tamaulipas'],
        'Estado': ['Baja California', 'Sonora', 'Chihuahua', 'Coahuila', 'Nuevo León', 'Tamaulipas'],
        'Parque_Vehicular': [37000, 28000, 85000, 62000, 95000, 48000],  # Unidades
        'Permisionarios': [12500, 9200, 28000, 20500, 31500, 16000],  # Empresas totales
        'Empresas_con_MC': [4200, 3100, 9500, 7000, 11000, 5500],  # ~33% tienen MC
        '% MC': ['33.6%', '33.7%', '33.9%', '34.1%', '34.9%', '34.4%'],
        'Aduanas_Principales': [
            'Tijuana, Mexicali',
            'Nogales, San Luis Río Colorado',
            'Cd. Juárez, Ojinaga',
            'Cd. Acuña, Piedras Negras',
            'Colombia',
            'Nuevo Laredo, Reynosa, Matamoros'
        ]
    }
    
    return pd.DataFrame(datos_regionales)

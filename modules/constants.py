"""
Módulo centralizado para constantes de la aplicación.
Evita duplicación de listas, diccionarios y datos estáticos.
"""

# ============================================================
# AÑOS Y MESES
# ============================================================

YEARS = [2023, 2024, 2025, 2026]

MONTHS = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

MONTHS_MAP = {
    'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
    'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
    'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
}

MONTHS_ENGLISH = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}

# ============================================================
# FRONTERAS Y GEOGRAFÍA
# ============================================================

BORDERS = ["México", "Canadá", "Ambas"]

# Puntos geográficos principales (puertos y ciudades fronterizas)
GEOGRAPHICAL_POINTS = {
    "Manzanillo": {"lat": 19.0522, "lon": -104.3158, "country": "MX", "type": "puerto"},
    "Veracruz": {"lat": 19.1738, "lon": -96.1342, "country": "MX", "type": "puerto"},
    "Lázaro Cárdenas": {"lat": 17.9585, "lon": -102.1891, "country": "MX", "type": "puerto"},
    "Altamira": {"lat": 22.3943, "lon": -97.9377, "country": "MX", "type": "puerto"},
    "Puerto Vallarta": {"lat": 20.6295, "lon": -105.2381, "country": "MX", "type": "puerto"},
    "Los Cabos": {"lat": 22.8898, "lon": -109.9789, "country": "MX", "type": "puerto"},
    "Topolobampo": {"lat": 25.6033, "lon": -109.0358, "country": "MX", "type": "puerto"},
    "Guaymas": {"lat": 27.9289, "lon": -110.8908, "country": "MX", "type": "puerto"},
}

# Ciudades fronterizas principales
BORDER_CITIES = {
    "México": [
        "Tijuana", "Mexicali", "Ciudad Juárez", "Nuevo Laredo", 
        "Laredo", "Reynosa", "Matamoros", "Nogales", "San Luis Potosí"
    ],
    "Canadá": [
        "Vancouver", "Calgary", "Toronto", "Montreal", "Windsor"
    ]
}

# ============================================================
# TIPOS DE TRANSPORTE Y OPERACIONES
# ============================================================

TRANSPORT_TYPES = [
    "Autotransporte",
    "Ferrocarril",
    "Marítimo",
    "Aéreo",
    "Multimodal"
]

CUSTOMS_TYPES = [
    "Inspección Postal",
    "Aduana Primaria",
    "Aduana Secundaria",
    "Centro de Verificación",
    "Puerta Aérea"
]

OPERATIONAL_STATUS = [
    "Abierto - Normal",
    "Abierto - Saturado",
    "Abierto - Crítico",
    "Cerrado - Mantenimiento",
    "Cerrado - Festivo",
    "Cerrado - Emergencia"
]

STATUS_COLORS = {
    "Abierto - Normal": "#4CAF50",
    "Abierto - Saturado": "#FFA726",
    "Abierto - Crítico": "#EF553B",
    "Cerrado - Mantenimiento": "#90CAF9",
    "Cerrado - Festivo": "#CE93D8",
    "Cerrado - Emergencia": "#666666",
}

# ============================================================
# CORREDORES LOGÍSTICOS
# ============================================================

LOGISTICS_CORRIDORS = {
    "México - Canadá": {
        "principales": ["Tijuana", "Ciudad Juárez", "Nuevo Laredo"],
        "distancia_km": 2500,
        "tiempo_dias": 5
    },
    "México - USA (Este)": {
        "principales": ["Laredo", "Brownsville", "Matamoros"],
        "distancia_km": 2000,
        "tiempo_dias": 4
    },
    "México - USA (Oeste)": {
        "principales": ["Tijuana", "Mexicali", "Nogales"],
        "distancia_km": 1800,
        "tiempo_dias": 3
    },
    "México - Guatemala": {
        "principales": ["Ciudad Tecún Umán", "La Mesilla"],
        "distancia_km": 1500,
        "tiempo_dias": 3
    },
    "México - Belice": {
        "principales": ["Chetumal"],
        "distancia_km": 400,
        "tiempo_dias": 1
    }
}

# ============================================================
# DIVISIONES ADMINISTRATIVAS
# ============================================================

MEXICAN_STATES = [
    "Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
    "Chiapas", "Chihuahua", "Ciuda de México", "Coahuila", "Colima",
    "Durango", "Estado de México", "Guanajuato", "Guerrero", "Hidalgo",
    "Jalisco", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca",
    "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa",
    "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
]

CANADIAN_PROVINCES = [
    "Alberta", "British Columbia", "Manitoba", "New Brunswick",
    "Newfoundland and Labrador", "Nova Scotia", "Ontario", "Prince Edward Island",
    "Quebec", "Saskatchewan"
]

US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"
]

# ============================================================
# PRODUCTOS Y CATEGORÍAS
# ============================================================

PRODUCT_CATEGORIES = [
    "Automotriz",
    "Electrónica",
    "Textil",
    "Agrícola",
    "Químicos",
    "Metales",
    "Alimentos",
    "Maquinaria",
    "Plásticos",
    "Otros"
]

# ============================================================
# COLORES Y ESTILOS
# ============================================================

COLOR_PALETTE = {
    "primary": "#4070F4",
    "secondary": "#29B5E8",
    "success": "#4CAF50",
    "warning": "#FFA726",
    "error": "#EF553B",
    "info": "#2196F3",
    "dark": "#2C3E50",
    "light": "#ECF0F1",
}

# ============================================================
# RANGOS Y UMBRALES
# ============================================================

SATURATION_LEVELS = {
    "baja": {"min": 0, "max": 30, "label": "Baja", "color": "#4CAF50"},
    "media": {"min": 30, "max": 70, "label": "Media", "color": "#FFA726"},
    "alta": {"min": 70, "max": 100, "label": "Alta", "color": "#EF553B"},
}

WAIT_TIME_LEVELS = {
    "corto": {"min": 0, "max": 2, "label": "Corto (< 2h)", "value": 1},
    "medio": {"min": 2, "max": 6, "label": "Medio (2-6h)", "value": 2},
    "largo": {"min": 6, "max": 12, "label": "Largo (6-12h)", "value": 3},
    "muy_largo": {"min": 12, "max": 9999, "label": "Muy Largo (> 12h)", "value": 4},
}

# ============================================================
# IDIOMAS
# ============================================================

SUPPORTED_LANGUAGES = {
    'es': 'Español',
    'en': 'English',
    'fr': 'Français'
}

DEFAULT_LANGUAGE = 'es'

"""
Configuration and Constants Module
Contains shared constants, translations, and configuration settings
"""

from datetime import datetime, timedelta

# ============================================================
# DICCIONARIO DE TRADUCCIONES MULTIIDIOMA
# ============================================================
TRANSLATIONS = {
    'es': {
        # Menú y navegación
        'menu_dashboard': 'Dashboard',
        'menu_monitoring': 'Monitoreo de Aduanas',
        'menu_flows': 'Flujos de Carga',
        'menu_corridors': 'Corredores Logísticos',
        'menu_ports': 'Puertos Marítimos',
        'menu_workforce': 'Fuerza Laboral',
        'menu_nearshoring': 'Nearshoring',
        'menu_indice': 'Índice FreightMetrics',
        'menu_oracle': 'Oracle Rate',
        
        # Botones y acciones
        'download_pdf': 'Descargar PDF',
        'apply_filters': 'Aplicar Filtros',
        'clear_filters': 'Limpiar Filtros',
        'export_data': 'Exportar Datos',
        
        # Filtros
        'filter_year': 'Año',
        'filter_border': 'Frontera',
        'filter_month': 'Mes',
        'filter_customs': 'Aduanas',
        'filter_transport': 'Transporte',
        'all_borders': 'Todas las Fronteras',
        'all_months': 'Todos los Meses',
        'all_customs': 'Todas las Aduanas',
    },
    'en': {
        # Menú y navegación
        'menu_dashboard': 'Dashboard',
        'menu_monitoring': 'Customs Monitoring',
        'menu_flows': 'Cargo Flows',
        'menu_corridors': 'Logistics Corridors',
        'menu_ports': 'Maritime Ports',
        'menu_workforce': 'Workforce',
        'menu_nearshoring': 'Nearshoring',
        'menu_indice': 'FreightMetrics Index',
        'menu_oracle': 'Oracle Rate',
        
        # Botones y acciones
        'download_pdf': 'Download PDF',
        'apply_filters': 'Apply Filters',
        'clear_filters': 'Clear Filters',
        'export_data': 'Export Data',
        
        # Filtros
        'filter_year': 'Year',
        'filter_border': 'Border',
        'filter_month': 'Month',
        'filter_customs': 'Customs',
        'filter_transport': 'Transport',
        'all_borders': 'All Borders',
        'all_months': 'All Months',
        'all_customs': 'All Customs',
    },
    'fr': {
        # Menú y navegación
        'menu_dashboard': 'Tableau de Bord',
        'menu_monitoring': 'Surveillance Douanière',
        'menu_flows': 'Flux de Fret',
        'menu_corridors': 'Corridors Logistiques',
        'menu_ports': 'Ports Maritimes',
        'menu_workforce': 'Main d\'Oeuvre',
        'menu_nearshoring': 'Nearshoring',
        'menu_indice': 'Indice FreightMetrics',
        'menu_oracle': 'Oracle Rate',
        
        # Botones y acciones
        'download_pdf': 'Télécharger PDF',
        'apply_filters': 'Appliquer Filtres',
        'clear_filters': 'Effacer Filtres',
        'export_data': 'Exporter Données',
        
        # Filtros
        'filter_year': 'Année',
        'filter_border': 'Frontière',
        'filter_month': 'Mois',
        'filter_customs': 'Douanes',
        'filter_transport': 'Transport',
        'all_borders': 'Toutes Frontières',
        'all_months': 'Tous les Mois',
        'all_customs': 'Toutes Douanes',
    }
}

# ============================================================
# FUNCIÓN PARA OBTENER TRADUCCIÓN
# ============================================================
def t(key, lang='es'):
    """
    Get translation for a key in the specified language
    
    Args:
        key (str): Translation key
        lang (str): Language code ('es', 'en', 'fr')
    
    Returns:
        str: Translated text or key if not found
    """
    if lang not in TRANSLATIONS:
        lang = 'es'
    
    return TRANSLATIONS[lang].get(key, key)


# ============================================================
# DÍAS FESTIVOS MÉXICO-USA 2025-2026
# ============================================================
DIAS_FESTIVOS_2025_2026 = [
    # 2025
    '2025-01-01',  # Año Nuevo
    '2025-02-03',  # Día de la Constitución (MX)
    '2025-02-17',  # Presidents Day (USA)
    '2025-03-17',  # Natalicio Benito Juárez (MX)
    '2025-05-01',  # Día del Trabajo (MX)
    '2025-05-26',  # Memorial Day (USA)
    '2025-07-04',  # Independence Day (USA)
    '2025-09-01',  # Labor Day (USA)
    '2025-09-16',  # Independencia México
    '2025-11-17',  # Revolución Mexicana
    '2025-11-27',  # Thanksgiving (USA)
    '2025-12-25',  # Navidad
    # 2026
    '2026-01-01',  # Año Nuevo
    '2026-02-02',  # Día de la Constitución (MX)
    '2026-02-16',  # Presidents Day (USA)
    '2026-03-16',  # Natalicio Benito Juárez (MX)
    '2026-05-01',  # Día del Trabajo (MX)
    '2026-05-25',  # Memorial Day (USA)
    '2026-07-04',  # Independence Day (USA)
    '2026-09-07',  # Labor Day (USA)
    '2026-09-16',  # Independencia México
    '2026-11-16',  # Revolución Mexicana
    '2026-11-26',  # Thanksgiving (USA)
    '2026-12-25',  # Navidad
]


# ============================================================
# PUERTOS CON VOLÚMENES BASE CONSISTENTES (cruces diarios promedio)
# ============================================================
PUERTOS_BASE = {
    'Nuevo Laredo III (Comercio Mundial)': 567,     # ~17,000 mensuales
    'Reynosa (Pharr)': 450,                         # ~13,500 mensuales
    'Laredo - Colombia': 400,                       # ~12,000 mensuales
    'Cd. Juárez (Paso del Norte/Zaragoza)': 383,   # ~11,500 mensuales
    'Tijuana (Mesa de Otay)': 350,                  # ~10,500 mensuales
    'Matamoros (Gral. Ignacio Zaragoza)': 300,     # ~9,000 mensuales
    'Nogales (Mariposa)': 250,                      # ~7,500 mensuales
    'Mexicali II (Nvo. Mexicali)': 200,            # ~6,000 mensuales
    'Piedras Negras': 167,                          # ~5,000 mensuales
    'San Luis Río Colorado': 133,                   # ~4,000 mensuales
    'Agua Prieta': 100,                             # ~3,000 mensuales
    'Cd. Acuña': 117                                # ~3,500 mensuales
}


# ============================================================
# HORARIOS DE OPERACIÓN Y ZONAS HORARIAS
# ============================================================
TIMEZONE_MAP = {
    'CST': 'America/Mexico_City',      # UTC-6 - Hora Centro
    'PST': 'America/Tijuana',           # UTC-8 - Hora Pacífico (Baja California)
    'MST': 'America/Hermosillo'         # UTC-7 - Hora Montaña (Sonora)
}

# ============================================================
# DATOS DE FUERZA LABORAL
# ============================================================
SEGMENTACION_FUERZA_LABORAL = {
    'Segmento': ['Hombre-Camión', 'Pequeña', 'Mediana', 'Grande'],
    'Rango Unidades': ['1 - 5', '6 - 30', '31 - 100', '101+'],
    'Número de Empresas': [163200, 29800, 4500, 1000],  # Total: ~198,500
    'Total Operadores': [196000, 227000, 125000, 82000],  # Total: ~630,000 (déficit 99k según IRU 2024)
    'Participación Mercado': ['82.2%', '15.0%', '2.3%', '0.5%']
}

DATOS_REGIONALES_FRONTERIZOS = {
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

# ============================================================
# UMBRALES DE ALERTAS POR DEFECTO
# ============================================================
UMBRALES_ALERTAS_DEFECTO = {
    'critico': {'saturacion': 85, 'tiempo_espera': 120},
    'alto': {'saturacion': 70, 'tiempo_espera': 90},
    'medio': {'saturacion': 60, 'tiempo_espera': 60}
}

# ============================================================
# ESTILOS CSS GLOBALES
# ============================================================
ESTILOS_GLOBALES = """
/* Fuentes y colores principales */
.stApp {
    color: #F4F7F6;
    font-family: 'Inter', sans-serif;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    color: #F4F7F6;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
}

/* Buttons con bordes suaves */
.stButton > button {
    background-color: #29B5E8;
    color: white;
    border-radius: 10px;
    font-weight: 600;
    border: none;
    padding: 10px 20px;
    box-shadow: 0 2px 10px rgba(41, 181, 232, 0.2);
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-color: #29B5E8;
    box-shadow: 0 4px 15px rgba(41, 181, 232, 0.3);
}

/* Metric cards - Fondo gris claro */
[data-testid="metric-container"] {
    background-color: #f8f9fa;
    border-radius: 12px;
    border: 1px solid #E0E0E0;
    padding: 20px;
}

/* Text area */
.stTextArea textarea {
    border-radius: 10px;
    border: 1px solid #E0E0E0;
    color: #F4F7F6;
}

/* Dataframes */
.dataframe {
    border-radius: 10px;
    background-color: white;
}

.dataframe tbody tr:hover {
    background-color: #e8f4f8;
}

/* Expanders */
.streamlit-expanderHeader {
    background-color: #131b2e !important;
    color: #F4F7F6 !important;
    border-radius: 10px;
    font-weight: 600;
    border: 1px solid #29B5E8;
}

/* Alerts - Diferentes colores según tipo */
.stAlert {
    border-radius: 10px;
    border-left: 4px solid;
}

/* Alert de error - Rojo Coral */
[data-baseweb="notification"][kind="error"],
.stAlert[data-baseweb="notification"] {
    border-left-color: #EF553B !important;
}

/* Alert de éxito - Azul Acero */
[data-baseweb="notification"][kind="success"] {
    border-left-color: #29B5E8 !important;
}

/* Alert de info - Azul Eléctrico */
[data-baseweb="notification"][kind="info"] {
    border-left-color: #29B5E8 !important;
}

/* Texto general */
p, span, div {
    color: #F4F7F6;
}

/* Links - Azul Eléctrico */
a {
    color: #29B5E8 !important;
    text-decoration: none;
    font-weight: 500;
}

a:hover {
    color: #29B5E8 !important;
    text-decoration: underline;
}

/* Contenedores de columnas - Fondo transparente */
[data-testid="column"] {
    background-color: transparent;
}

/* Cards/Containers blancos para destacar sobre Gris Nube */
.element-container {
    background-color: transparent;
}

/* Plotly charts - Fondo blanco */
.js-plotly-plot {
    background-color: #131b2e !important;
    border-radius: 10px;
    padding: 10px;
    box-shadow: 0 2px 8px rgba(17, 16, 29, 0.06);
}

/* Spinner/Loading - Azul Eléctrico */
.stSpinner > div {
    border-top-color: #29B5E8 !important;
}

/* Progress bar - Azul Eléctrico */
.stProgress > div > div {
    background-color: #29B5E8 !important;
}
"""

"""
Módulo de Horarios de Operación de Puertos
Almacena y gestiona los horarios de operación de puertos México-USA y Canadá-USA
"""

# ============================================================================
# HORARIOS DE PUERTOS MÉXICO-USA
# ============================================================================

HORARIOS_MEXICO = {
    # TEXAS
    "06480101": {  # Laredo
        "nombre": "Laredo, Texas",
        "exportacion_lv": "06:00 - 23:00",
        "importacion_lv": "06:00 - 23:00",
        "fin_semana": "06:00 - 23:00",
        "dia_festivo": "06:00 - 23:00",
        "notas": "Operación 24/7 con picos por la noche"
    },
    "06471001": {  # Brownsville
        "nombre": "Brownsville, Texas",
        "exportacion_lv": "06:00 - 22:00",
        "importacion_lv": "06:00 - 22:00",
        "fin_semana": "06:00 - 22:00",
        "dia_festivo": "06:00 - 22:00",
        "notas": ""
    },
    "06472001": {  # Rio Grande City
        "nombre": "Rio Grande City, Texas",
        "exportacion_lv": "06:00 - 20:00",
        "importacion_lv": "06:00 - 18:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": "Horario limitado"
    },
    "06473001": {  # Progreso
        "nombre": "Progreso, Texas",
        "exportacion_lv": "06:00 - 20:00",
        "importacion_lv": "06:00 - 18:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
    "06474001": {  # Roma
        "nombre": "Roma, Texas",
        "exportacion_lv": "06:00 - 20:00",
        "importacion_lv": "06:00 - 18:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
    "06481001": {  # Del Rio
        "nombre": "Del Rio, Texas",
        "exportacion_lv": "06:00 - 22:00",
        "importacion_lv": "06:00 - 22:00",
        "fin_semana": "06:00 - 22:00",
        "dia_festivo": "06:00 - 22:00",
        "notas": ""
    },
    "06500601": {  # Eagle Pass
        "nombre": "Eagle Pass, Texas",
        "exportacion_lv": "06:00 - 22:00",
        "importacion_lv": "06:00 - 22:00",
        "fin_semana": "06:00 - 22:00",
        "dia_festivo": "06:00 - 22:00",
        "notas": ""
    },
    "06483001": {  # Presidio
        "nombre": "Presidio, Texas",
        "exportacion_lv": "06:00 - 20:00",
        "importacion_lv": "06:00 - 18:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": "Horario muy limitado"
    },
    "06452401": {  # Tornillo
        "nombre": "Tornillo, Texas",
        "exportacion_lv": "06:00 - 20:00",
        "importacion_lv": "06:00 - 20:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
    "06450702": {  # Ysleta
        "nombre": "Ysleta, Texas",
        "exportacion_lv": "06:00 - 23:00",
        "importacion_lv": "06:00 - 23:00",
        "fin_semana": "06:00 - 23:00",
        "dia_festivo": "06:00 - 23:00",
        "notas": ""
    },
    "09250602": {  # Otay Mesa
        "nombre": "Otay Mesa, California",
        "exportacion_lv": "06:00 - 20:00",
        "importacion_lv": "06:00 - 20:00",
        "fin_semana": "06:00 - 19:00",
        "dia_festivo": "06:00 - 18:00",
        "notas": "Uno de los puertos más congestionados"
    },
    "09250101": {  # San Ysidro
        "nombre": "San Ysidro (Tijuana), California",
        "exportacion_lv": "06:00 - 19:00",
        "importacion_lv": "06:00 - 19:00",
        "fin_semana": "06:00 - 18:00",
        "dia_festivo": "06:00 - 17:00",
        "notas": "Puerto congestionado, múltiples carriles"
    },
    "09251202": {  # Calexico East
        "nombre": "Calexico East, California",
        "exportacion_lv": "06:00 - 20:00",
        "importacion_lv": "06:00 - 19:15",
        "fin_semana": "S: 06:00 - 16:00 / D: 06:00 - 14:00",
        "dia_festivo": "06:00 - 14:00",
        "notas": "Aduanal de México"
    },
    "09250702": {  # Tecate
        "nombre": "Tecate, California",
        "exportacion_lv": "06:00 - 20:00",
        "importacion_lv": "06:00 - 19:00",
        "fin_semana": "06:00 - 18:00",
        "dia_festivo": "06:00 - 17:00",
        "notas": ""
    },
    "06450701": {  # El Paso
        "nombre": "El Paso, Texas",
        "exportacion_lv": "06:00 - 23:00",
        "importacion_lv": "06:00 - 23:00",
        "fin_semana": "06:00 - 23:00",
        "dia_festivo": "06:00 - 23:00",
        "notas": "Uno de los principales"
    },
    "06451701": {  # Santa Teresa
        "nombre": "Santa Teresa, New Mexico",
        "exportacion_lv": "07:00 - 23:00",
        "importacion_lv": "07:00 - 23:00",
        "fin_semana": "07:00 - 23:00",
        "dia_festivo": "07:00 - 23:00",
        "notas": "Cruce comercial importante"
    },
    "07200601": {  # Nogales
        "nombre": "Nogales, Arizona",
        "exportacion_lv": "06:00 - 22:00",
        "importacion_lv": "06:00 - 22:00",
        "fin_semana": "06:00 - 22:00",
        "dia_festivo": "06:00 - 22:00",
        "notas": "Puerto importante de cruce"
    },
    "07201001": {  # Douglas
        "nombre": "Douglas, Arizona",
        "exportacion_lv": "06:00 - 22:00",
        "importacion_lv": "06:00 - 22:00",
        "fin_semana": "06:00 - 22:00",
        "dia_festivo": "06:00 - 22:00",
        "notas": ""
    },
    "07202001": {  # Naco
        "nombre": "Naco, Arizona",
        "exportacion_lv": "08:00 - 20:00",
        "importacion_lv": "08:00 - 20:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": "Horario limitado"
    },
    "07204001": {  # Lukeville
        "nombre": "Lukeville, Arizona",
        "exportacion_lv": "08:00 - 17:00",
        "importacion_lv": "08:00 - 17:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": "Cruce muy limitado"
    },
    "07150501": {  # San Luis
        "nombre": "San Luis, Arizona",
        "exportacion_lv": "07:00 - 23:00",
        "importacion_lv": "07:00 - 23:00",
        "fin_semana": "07:00 - 23:00",
        "dia_festivo": "07:00 - 23:00",
        "notas": ""
    },
}

# ============================================================================
# HORARIOS DE PUERTOS CANADÁ-USA
# ============================================================================

HORARIOS_CANADA = {
    "05200101": {  # Blaine
        "nombre": "Blaine, Washington",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto de operación 24/7"
    },
    "05220101": {  # Point Roberts
        "nombre": "Point Roberts, Washington",
        "exportacion_lv": "06:00 - 22:00",
        "importacion_lv": "06:00 - 22:00",
        "fin_semana": "06:00 - 22:00",
        "dia_festivo": "06:00 - 22:00",
        "notas": ""
    },
    "05230101": {  # Bellingham
        "nombre": "Bellingham, Washington",
        "exportacion_lv": "09:00 - 17:00",
        "importacion_lv": "09:00 - 17:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": "Solo L-V"
    },
    "05240101": {  # Sumas
        "nombre": "Sumas, Washington",
        "exportacion_lv": "08:00 - 19:00",
        "importacion_lv": "08:00 - 19:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
    "05210101": {  # Lynden
        "nombre": "Lynden, Washington",
        "exportacion_lv": "09:00 - 17:00",
        "importacion_lv": "09:00 - 17:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
    "05250101": {  # Port Angeles
        "nombre": "Port Angeles, Washington",
        "exportacion_lv": "06:00 - 22:00",
        "importacion_lv": "06:00 - 22:00",
        "fin_semana": "06:00 - 22:00",
        "dia_festivo": "06:00 - 22:00",
        "notas": ""
    },
    "04640101": {  # Sweetgrass
        "nombre": "Sweetgrass, Montana",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto de operación 24/7"
    },
    "04660101": {  # Piegan
        "nombre": "Piegan, Montana",
        "exportacion_lv": "09:00 - 17:00",
        "importacion_lv": "09:00 - 17:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
    "04670101": {  # Turner
        "nombre": "Turner, Montana",
        "exportacion_lv": "09:00 - 17:00",
        "importacion_lv": "09:00 - 17:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
    "04620101": {  # Pembina
        "nombre": "Pembina, North Dakota",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto de operación 24/7"
    },
    "04680101": {  # Portal
        "nombre": "Portal, North Dakota",
        "exportacion_lv": "08:00 - 20:00",
        "importacion_lv": "08:00 - 20:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
    "04570101": {  # Dunseith
        "nombre": "Dunseith, North Dakota",
        "exportacion_lv": "09:00 - 17:00",
        "importacion_lv": "09:00 - 17:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
    "04690101": {  # Fortuna
        "nombre": "Fortuna, North Dakota",
        "exportacion_lv": "09:00 - 17:00",
        "importacion_lv": "09:00 - 17:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
    "04600101": {  # International Falls
        "nombre": "International Falls, Minnesota",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto de operación 24/7"
    },
    "04520101": {  # Baudette
        "nombre": "Baudette, Minnesota",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto de operación 24/7"
    },
    "04700101": {  # Janesville
        "nombre": "Janesville, Minnesota",
        "exportacion_lv": "09:00 - 17:00",
        "importacion_lv": "09:00 - 17:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
    "04710101": {  # Sault Ste Marie
        "nombre": "Sault Ste Marie, Michigan",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto de operación 24/7"
    },
    "04720101": {  # Mackinac Bridge
        "nombre": "Mackinac Bridge, Michigan",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto de operación 24/7"
    },
    "01050101": {  # Buffalo Niagara Falls
        "nombre": "Buffalo-Niagara Falls, New York",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto principal, operación 24/7"
    },
    "01140101": {  # Thousand Islands Bridge
        "nombre": "Thousand Islands Bridge, New York",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto de operación 24/7"
    },
    "01110101": {  # Rainbow Bridge
        "nombre": "Rainbow Bridge, New York",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto de operación 24/7"
    },
    "01100101": {  # Ogdensburg
        "nombre": "Ogdensburg, New York",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto de operación 24/7"
    },
    "01070101": {  # Champlain Rouses Point
        "nombre": "Champlain-Rouses Point, New York",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto de operación 24/7"
    },
    "01090101": {  # Highgate Springs
        "nombre": "Highgate Springs, Vermont",
        "exportacion_lv": "08:00 - 20:00",
        "importacion_lv": "08:00 - 17:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
    "01150101": {  # Alburgh
        "nombre": "Alburgh, Vermont",
        "exportacion_lv": "08:00 - 20:00",
        "importacion_lv": "08:00 - 17:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
    "01060101": {  # Calais
        "nombre": "Calais, Maine",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto de operación 24/7"
    },
    "01160101": {  # Houlton
        "nombre": "Houlton, Maine",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto de operación 24/7"
    },
    "01170101": {  # Van Buren
        "nombre": "Van Buren, Maine",
        "exportacion_lv": "24 hrs",
        "importacion_lv": "24 hrs",
        "fin_semana": "24 hrs",
        "dia_festivo": "24 hrs",
        "notas": "Puerto de operación 24/7"
    },
    "01180101": {  # Jackman
        "nombre": "Jackman, Maine",
        "exportacion_lv": "08:00 - 20:00",
        "importacion_lv": "08:00 - 17:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
    "01190101": {  # Coburn Gore
        "nombre": "Coburn Gore, Maine",
        "exportacion_lv": "08:00 - 20:00",
        "importacion_lv": "08:00 - 17:00",
        "fin_semana": "Cerrado",
        "dia_festivo": "Cerrado",
        "notas": ""
    },
}

# Combinar todos los horarios
TODOS_HORARIOS = {**HORARIOS_MEXICO, **HORARIOS_CANADA}


def obtener_horarios_puerto(codigo_puerto: str) -> dict:
    """
    Obtiene los horarios de operación de un puerto.
    
    Args:
        codigo_puerto: Código CBP del puerto (ej: "09250602")
    
    Returns:
        Dict con horarios o None si no existe
    """
    return TODOS_HORARIOS.get(codigo_puerto, {
        "nombre": f"Puerto {codigo_puerto}",
        "exportacion_lv": "—",
        "importacion_lv": "—",
        "fin_semana": "—",
        "dia_festivo": "—",
        "notas": "Información no disponible",
    })

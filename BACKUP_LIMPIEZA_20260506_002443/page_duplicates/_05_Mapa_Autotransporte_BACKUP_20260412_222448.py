"""
Página: Puertos Marítimos
Análisis geográfico de puertos marítimos, tráfico marítimo y rastreo de contenedores
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
import os
import json
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# FUNCIONES AUXILIARES DE PUERTOS MARÍTIMOS
# ============================================================

def obtener_trafico_maritimo_aishub(bbox=None, api_key=None):
    """
    Obtiene posiciones de buques en tiempo real desde AIS Hub API (gratuita con registro)
    
    Args:
        bbox: Bounding box [min_lat, min_lon, max_lat, max_lon] para filtrar zona
        api_key: API key de AIS Hub (gratis en https://www.aishub.net/api)
    
    Returns:
        DataFrame con posiciones de buques
    """
    try:
        if not api_key:
            api_key = os.getenv('AISHUB_API_KEY', '')
        
        if not api_key:
            st.info("💡 Para datos reales de tráfico marítimo, obtén una API key gratuita en https://www.aishub.net/api")
            return generar_trafico_maritimo_simulado()
        
        if bbox is None:
            bbox = [14.0, -118.0, 32.0, -86.0]
        
        url = "http://data.aishub.net/ws.php"
        params = {
            'username': api_key,
            'format': '1',
            'output': 'json',
            'compress': '0',
            'latmin': bbox[0],
            'lonmin': bbox[1],
            'latmax': bbox[2],
            'lonmax': bbox[3]
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data and len(data) > 0 and 'ERROR' not in data[0]:
                buques = []
                for vessel in data[0]:
                    if isinstance(vessel, dict):
                        buques.append({
                            'MMSI': vessel.get('MMSI', 'N/A'),
                            'Nombre': vessel.get('NAME', 'Unknown'),
                            'Lat': float(vessel.get('LATITUDE', 0)),
                            'Lon': float(vessel.get('LONGITUDE', 0)),
                            'Velocidad': float(vessel.get('SPEED', 0)),
                            'Rumbo': float(vessel.get('COURSE', 0)),
                            'Tipo': vessel.get('TYPE', 'Unknown'),
                            'Timestamp': vessel.get('TIME', '')
                        })
                
                df = pd.DataFrame(buques)
                if not df.empty:
                    st.success(f"✅ Datos AIS Hub: {len(df)} buques en tiempo real")
                    return df
        
        st.warning("⚠️ No se pudieron obtener datos de AIS Hub. Usando datos simulados.")
        return generar_trafico_maritimo_simulado()
        
    except Exception as e:
        st.warning(f"⚠️ Error al consultar AIS Hub: {str(e)[:100]}. Usando datos simulados.")
        return generar_trafico_maritimo_simulado()


def generar_trafico_maritimo_simulado():
    """Genera datos simulados de tráfico marítimo para demostración"""
    np.random.seed(42)
    
    puertos = [
        {'nombre': 'Manzanillo', 'lat': 19.05, 'lon': -104.31},
        {'nombre': 'Veracruz', 'lat': 19.17, 'lon': -96.13},
        {'nombre': 'Lázaro Cárdenas', 'lat': 17.96, 'lon': -102.19},
        {'nombre': 'Altamira', 'lat': 22.39, 'lon': -97.94},
        {'nombre': 'Ensenada', 'lat': 31.87, 'lon': -116.60}
    ]
    
    tipos_buque = ['Portacontenedores', 'Granelero', 'Petrolero', 'Carga General', 'Ro-Ro']
    buques = []
    
    for i in range(50):
        if i < 25:
            puerto = np.random.choice(puertos)
            lat = puerto['lat'] + np.random.uniform(-0.5, 0.5)
            lon = puerto['lon'] + np.random.uniform(-0.5, 0.5)
            velocidad = np.random.uniform(0, 5)
        else:
            lat = np.random.uniform(14.0, 32.0)
            lon = np.random.uniform(-118.0, -86.0)
            velocidad = np.random.uniform(10, 22)
        
        buques.append({
            'MMSI': f'3{np.random.randint(10000000, 99999999)}',
            'Nombre': f'{np.random.choice(tipos_buque)[:3].upper()}-{1000+i}',
            'Lat': lat,
            'Lon': lon,
            'Velocidad': velocidad,
            'Rumbo': np.random.uniform(0, 360),
            'Tipo': np.random.choice(tipos_buque),
            'Timestamp': datetime.now().isoformat()
        })
    
    return pd.DataFrame(buques)


def buscar_contenedor(numero_contenedor):
    """
    Simula la búsqueda de un contenedor con información detallada de disponibilidad para retiro.
    
    Args:
        numero_contenedor: Número del contenedor (ej: MSCU1234567)
    
    Returns:
        Dict con información completa del contenedor incluyendo disponibilidad para retiro
    """
    if not numero_contenedor or len(numero_contenedor) < 11:
        return None
    
    navieras = ['Maersk', 'CMA CGM', 'MSC', 'COSCO', 'Hapag-Lloyd', 'ONE', 'Evergreen']
    estados = ['En Tránsito Marítimo', 'En Puerto - Descargando', 'En Aduana - Pendiente Liberación', 
               'Liberado por Aduana', 'Disponible para Retiro', 'En Tránsito Terrestre', 'Entregado']
    puertos = ['Manzanillo', 'Veracruz', 'Lázaro Cárdenas', 'Altamira']
    terminales = {
        'Manzanillo': ['SSA Manzanillo', 'OCUPA Manzanillo', 'TEC Manzanillo'],
        'Veracruz': ['API Veracruz', 'APIVER', 'SSA Veracruz'],
        'Lázaro Cárdenas': ['TECLAZ', 'TEC II', 'TPL'],
        'Altamira': ['OCUPA Altamira', 'TIMSA', 'ALTAMIRA Terminal']
    }
    
    hash_val = sum(ord(c) for c in numero_contenedor)
    np.random.seed(hash_val)
    
    naviera = np.random.choice(navieras)
    puerto_destino = np.random.choice(puertos)
    terminal = np.random.choice(terminales[puerto_destino])
    
    fecha_inicio = datetime.now() - timedelta(days=np.random.randint(15, 45))
    eventos = []
    
    origen = np.random.choice(['Shanghai', 'Ningbo', 'Yantian', 'Hong Kong', 'Busan'])
    eventos.append({
        'fecha': fecha_inicio,
        'ubicacion': origen,
        'evento': 'Recogida en origen',
        'detalles': 'Contenedor cargado y sellado'
    })
    
    fecha_carga = fecha_inicio + timedelta(days=2)
    buque_nombre = np.random.choice(['MSC GÜLSÜN', 'EVER GIVEN', 'CMA CGM ANTOINE DE SAINT EXUPERY', 
                                      'COSCO SHIPPING UNIVERSE', 'HMM ALGECIRAS'])
    eventos.append({
        'fecha': fecha_carga,
        'ubicacion': origen,
        'evento': 'Cargado en buque',
        'detalles': f'Buque: {buque_nombre}'
    })
    
    fecha_salida = fecha_carga + timedelta(days=1)
    eventos.append({
        'fecha': fecha_salida,
        'ubicacion': origen,
        'evento': 'Salida del puerto',
        'detalles': 'En tránsito marítimo'
    })
    
    dias_transito = np.random.randint(12, 25)
    fecha_transito = fecha_salida + timedelta(days=int(dias_transito/2))
    eventos.append({
        'fecha': fecha_transito,
        'ubicacion': f'Océano Pacífico - Rumbo a {puerto_destino}',
        'evento': 'En tránsito marítimo',
        'detalles': f'ETA estimado: {dias_transito} días'
    })
    
    fecha_llegada = fecha_salida + timedelta(days=dias_transito)
    
    estado_actual = 'En Tránsito Marítimo'
    ubicacion_actual = eventos[-1]['ubicacion']
    info_retiro = None
    
    if datetime.now() > fecha_llegada:
        eventos.append({
            'fecha': fecha_llegada,
            'ubicacion': f'{puerto_destino} - {terminal}',
            'evento': 'Llegada a puerto destino',
            'detalles': f'Descargado en terminal {terminal}'
        })
        
        fecha_descarga = fecha_llegada + timedelta(hours=np.random.randint(6, 36))
        eventos.append({
            'fecha': fecha_descarga,
            'ubicacion': f'{puerto_destino} - {terminal}',
            'evento': 'Descarga completada',
            'detalles': f'Posición en terminal: Patio {np.random.choice(["A", "B", "C"])}-{np.random.randint(1, 50)}'
        })
        
        dias_desde_llegada = (datetime.now() - fecha_llegada).days
        
        if dias_desde_llegada < 2:
            estado_actual = 'En Puerto - Descargando'
            ubicacion_actual = f'{puerto_destino} - {terminal}'
        elif dias_desde_llegada < 3:
            estado_actual = 'En Aduana - Pendiente Liberación'
            ubicacion_actual = f'{puerto_destino} - Recinto Fiscal'
            
            fecha_aduana = fecha_descarga + timedelta(hours=12)
            eventos.append({
                'fecha': fecha_aduana,
                'ubicacion': f'{puerto_destino} - Recinto Fiscal',
                'evento': 'En proceso de despacho aduanal',
                'detalles': 'Documentación bajo revisión'
            })
        else:
            fecha_liberacion = fecha_descarga + timedelta(days=2)
            eventos.append({
                'fecha': fecha_liberacion,
                'ubicacion': f'{puerto_destino} - {terminal}',
                'evento': 'Liberado por aduana',
                'detalles': 'Pedimento autorizado - Listo para retiro'
            })
            
            estado_actual = 'Disponible para Retiro'
            ubicacion_actual = f'{puerto_destino} - {terminal}'
            
            dias_en_terminal = (datetime.now() - fecha_descarga).days
            dias_libres = 7
            dias_libres_restantes = max(0, dias_libres - dias_en_terminal)
            
            if dias_libres_restantes == 0:
                dias_demora = dias_en_terminal - dias_libres
                cargo_diario = 35
                if '40' in numero_contenedor:
                    cargo_diario = 50
                cargo_demora = dias_demora * cargo_diario
            else:
                cargo_demora = 0
            
            horarios_retiro = {
                'lunes_viernes': '08:00 - 17:00',
                'sabado': '08:00 - 13:00',
                'domingo': 'Cerrado'
            }
            
            docs_requeridos = [
                'Pedimento de importación (liberado)',
                'Bill of Lading (original o telex release)',
                'Carta de encomienda del transportista',
                'RFC del importador',
                'Comprobante de pago de almacenaje (si aplica)',
                'Identificación del conductor',
                'Tarjeta de circulación del vehículo'
            ]
            
            info_terminal = {
                'nombre': terminal,
                'direccion': f'Puerto de {puerto_destino}, México',
                'telefono': f'+52 {np.random.randint(300, 999)} {np.random.randint(100, 999)} {np.random.randint(1000, 9999)}',
                'email': f'retiros@{terminal.lower().replace(" ", "")}.com.mx',
                'sistema_citas': 'TAPA' if np.random.random() > 0.5 else 'Portal de Terminal'
            }
            
            patio = np.random.choice(['A', 'B', 'C', 'D'])
            fila = np.random.randint(1, 50)
            bahia = np.random.randint(1, 20)
            posicion = f'Patio {patio}, Fila {fila}, Bahía {bahia}'
            
            info_retiro = {
                'disponible': True,
                'fecha_disponibilidad': fecha_liberacion,
                'terminal': info_terminal,
                'posicion_patio': posicion,
                'dias_libres_restantes': dias_libres_restantes,
                'cargo_demora_usd': cargo_demora,
                'requiere_cita': np.random.choice([True, False]),
                'cita_sugerida': (datetime.now() + timedelta(days=1)).replace(hour=10, minute=0),
                'horarios_retiro': horarios_retiro,
                'documentacion_requerida': docs_requeridos,
                'contacto_emergencia': info_terminal['telefono'],
                'observaciones': []
            }
            
            if cargo_demora > 0:
                info_retiro['observaciones'].append(f'⚠️ Cargo por demora: ${cargo_demora:,.2f} USD ({dias_demora} días)')
            
            if dias_libres_restantes <= 2:
                info_retiro['observaciones'].append(f'⏰ URGENTE: Solo {dias_libres_restantes} días libres restantes')
            
            if info_retiro['requiere_cita']:
                info_retiro['observaciones'].append('📅 Requiere programar cita previa para retiro')
    
    if estado_actual == 'En Tránsito Marítimo':
        eta = fecha_llegada
    elif estado_actual == 'Entregado':
        eta = None
    elif estado_actual == 'Disponible para Retiro':
        eta = datetime.now()
    else:
        if estado_actual == 'En Puerto - Descargando':
            eta = fecha_llegada + timedelta(days=3)
        else:
            eta = fecha_llegada + timedelta(days=2, hours=12)
    
    return {
        'numero': numero_contenedor.upper(),
        'naviera': naviera,
        'buque': buque_nombre if datetime.now() > fecha_carga else 'Pendiente asignación',
        'tipo': np.random.choice(['20\' Standard', '40\' Standard', '40\' High Cube', '20\' Reefer', '40\' Reefer']),
        'estado': estado_actual,
        'ubicacion_actual': ubicacion_actual,
        'origen': origen,
        'destino': puerto_destino,
        'eta': eta,
        'peso_kg': np.random.randint(8000, 28000),
        'eventos': eventos,
        'info_retiro': info_retiro,
        'ultima_actualizacion': datetime.now()
    }


class SistemaAlertasPuertos:
    def __init__(self):
        self.alertas_file = Path(__file__).parent.parent / "data" / "alertas_puertos_log.json"
        self.umbrales = {
            'critico': {'congestion': 85, 'tiempo_espera': 72, 'saturacion': 85},
            'alto': {'congestion': 70, 'tiempo_espera': 48, 'saturacion': 70},
            'medio': {'congestion': 60, 'tiempo_espera': 24, 'saturacion': 60}
        }
        self.alertas_activas = []
        self.cargar_historial()
    
    def cargar_historial(self):
        try:
            if self.alertas_file.exists():
                with open(self.alertas_file, 'r', encoding='utf-8') as f:
                    self.historial = json.load(f)
            else:
                self.historial = []
        except:
            self.historial = []
    
    def guardar_alerta(self, alerta):
        try:
            self.historial.append(alerta)
            self.historial = self.historial[-100:]
            self.alertas_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.alertas_file, 'w', encoding='utf-8') as f:
                json.dump(self.historial, f, ensure_ascii=False, indent=2)
        except Exception as e:
            pass
    
    def evaluar_puertos(self, df_puertos):
        self.alertas_activas = []
        timestamp = datetime.now().isoformat()
        
        for idx, row in df_puertos.iterrows():
            puerto = row['Puerto']
            saturacion = row.get('Saturacion', 0)
            tiempo_espera = row.get('Tiempo_Espera_hrs', 0)
            congestion = row.get('Indice_Congestion', 0)
            
            nivel = None
            mensaje = ""
            
            if saturacion >= self.umbrales['critico']['saturacion'] or \
               tiempo_espera >= self.umbrales['critico']['tiempo_espera'] or \
               congestion >= self.umbrales['critico']['congestion']:
                nivel = '🔴 CRÍTICO'
                mensaje = f"Saturación: {saturacion}% | Espera: {tiempo_espera}hrs | Congestión: {congestion}%"
            elif saturacion >= self.umbrales['alto']['saturacion'] or \
                 tiempo_espera >= self.umbrales['alto']['tiempo_espera'] or \
                 congestion >= self.umbrales['alto']['congestion']:
                nivel = '🟠 ALTO'
                mensaje = f"Saturación: {saturacion}% | Espera: {tiempo_espera}hrs | Congestión: {congestion}%"
            elif saturacion >= self.umbrales['medio']['saturacion'] or \
                 tiempo_espera >= self.umbrales['medio']['tiempo_espera'] or \
                 congestion >= self.umbrales['medio']['congestion']:
                nivel = '🟡 MEDIO'
                mensaje = f"Saturación: {saturacion}% | Espera: {tiempo_espera}hrs | Congestión: {congestion}%"
            
            if nivel:
                alerta = {
                    'timestamp': timestamp,
                    'puerto': puerto,
                    'nivel': nivel,
                    'mensaje': mensaje,
                    'saturacion': saturacion,
                    'tiempo_espera': tiempo_espera,
                    'congestion': congestion
                }
                self.alertas_activas.append(alerta)
                self.guardar_alerta(alerta)
        
        return self.alertas_activas
    
    def obtener_estadisticas_alertas(self):
        if not self.historial:
            return None
        
        ahora = datetime.now()
        alertas_24h = [a for a in self.historial 
                      if (ahora - datetime.fromisoformat(a['timestamp'])).total_seconds() < 86400]
        
        if not alertas_24h:
            return None
        
        alertas_criticas_24h = len([a for a in alertas_24h if '🔴' in a['nivel']])
        
        puertos_con_alertas = {}
        for alerta in alertas_24h:
            puerto = alerta['puerto']
            puertos_con_alertas[puerto] = puertos_con_alertas.get(puerto, 0) + 1
        
        puerto_mas_alertas = max(puertos_con_alertas.items(), key=lambda x: x[1])[0] if puertos_con_alertas else "N/A"
        
        saturaciones = [a['saturacion'] for a in alertas_24h if 'saturacion' in a]
        promedio_saturacion = sum(saturaciones) / len(saturaciones) if saturaciones else 0
        
        return {
            'total_alertas_24h': len(alertas_24h),
            'alertas_criticas_24h': alertas_criticas_24h,
            'puerto_mas_alertas': puerto_mas_alertas,
            'promedio_saturacion': promedio_saturacion
        }


def cargar_datos_puertos_reales():
    """Carga datos reales de puertos desde CSV o genera datos simulados enriquecidos"""
    try:
        csv_path = Path(__file__).parent.parent / "data" / "puertos_latest.csv"
        
        if csv_path.exists():
            df_puertos = pd.read_csv(csv_path)
            
            if 'Puerto' in df_puertos.columns:
                if 'Tiempo_Espera_hrs' not in df_puertos.columns:
                    df_puertos['Tiempo_Espera_hrs'] = df_puertos.get('Vol_Actual', df_puertos.get('Saturacion', 50)) / 5000 + np.random.uniform(12, 48, len(df_puertos))
                
                if 'Indice_Congestion' not in df_puertos.columns:
                    df_puertos['Indice_Congestion'] = df_puertos.get('Saturacion', np.random.uniform(40, 85, len(df_puertos)))
                
                if 'Buques_Esperando' not in df_puertos.columns:
                    df_puertos['Buques_Esperando'] = (df_puertos['Tiempo_Espera_hrs'] / 12).astype(int) + np.random.randint(0, 5, len(df_puertos))
                
                return df_puertos
        
        puerto_data = {
            'Puerto': ['Manzanillo', 'Veracruz', 'Lázaro Cárdenas', 'Altamira', 'Ensenada', 'Tuxpan'],
            'Vol_Actual': [320000, 110000, 180000, 95000, 75000, 45000],
            'Capacidad': [350000, 180000, 220000, 150000, 120000, 80000],
            'Operaciones': [450, 280, 320, 210, 180, 120],
            'Lat': [19.0522, 19.1738, 17.9585, 22.3943, 31.8667, 20.9577],
            'Lon': [-104.3158, -96.1342, -102.1891, -97.9377, -116.6000, -97.4054],
            'Tipo_Carga': ['Contenedores', 'Granel/General', 'Contenedores', 'Granel/Petróleo', 'Contenedores/Cruceros', 'Petróleo/Granel'],
            'Tiempo_Espera_hrs': [36, 18, 28, 24, 20, 15],
            'Indice_Congestion': [78, 52, 68, 58, 45, 35],
            'Buques_Esperando': [8, 3, 6, 5, 4, 2]
        }
        
        df_puertos = pd.DataFrame(puerto_data)
        return df_puertos
        
    except Exception as e:
        st.error(f"❌ Error al cargar datos de puertos: {e}")
        return None


def calcular_rutas_maritimas(puerto_origen):
    """Calcula rutas, costos y tiempos desde un puerto mexicano a destinos clave"""
    rutas = {
        'Manzanillo': [
            {'destino': 'Los Angeles', 'distancia_nm': 1450, 'tiempo_dias': 4, 'costo_usd': 850, 'via': 'Directa'},
            {'destino': 'Shanghai', 'distancia_nm': 6200, 'tiempo_dias': 18, 'costo_usd': 2800, 'via': 'Transpacífico'},
            {'destino': 'Houston', 'distancia_nm': 2100, 'tiempo_dias': 8, 'costo_usd': 1200, 'via': 'Canal de Panamá'},
            {'destino': 'Rotterdam', 'distancia_nm': 8500, 'tiempo_dias': 28, 'costo_usd': 3500, 'via': 'Canal de Panamá'}
        ],
        'Veracruz': [
            {'destino': 'Miami', 'distancia_nm': 1100, 'tiempo_dias': 4, 'costo_usd': 700, 'via': 'Golfo de México'},
            {'destino': 'Houston', 'distancia_nm': 850, 'tiempo_dias': 3, 'costo_usd': 600, 'via': 'Golfo de México'},
            {'destino': 'Rotterdam', 'distancia_nm': 5200, 'tiempo_dias': 18, 'costo_usd': 2200, 'via': 'Atlántico'},
            {'destino': 'Santos', 'distancia_nm': 4800, 'tiempo_dias': 16, 'costo_usd': 1900, 'via': 'Atlántico Sur'}
        ],
        'Lázaro Cárdenas': [
            {'destino': 'Los Angeles', 'distancia_nm': 1520, 'tiempo_dias': 4, 'costo_usd': 900, 'via': 'Directa'},
            {'destino': 'Shanghai', 'distancia_nm': 6350, 'tiempo_dias': 19, 'costo_usd': 2900, 'via': 'Transpacífico'},
            {'destino': 'Houston', 'distancia_nm': 2200, 'tiempo_dias': 8, 'costo_usd': 1250, 'via': 'Canal de Panamá'},
            {'destino': 'Vancouver', 'distancia_nm': 2800, 'tiempo_dias': 9, 'costo_usd': 1400, 'via': 'Costa Pacífico'}
        ],
        'Altamira': [
            {'destino': 'Houston', 'distancia_nm': 520, 'tiempo_dias': 2, 'costo_usd': 450, 'via': 'Golfo de México'},
            {'destino': 'New Orleans', 'distancia_nm': 680, 'tiempo_dias': 3, 'costo_usd': 550, 'via': 'Golfo de México'},
            {'destino': 'Miami', 'distancia_nm': 1200, 'tiempo_dias': 4, 'costo_usd': 750, 'via': 'Golfo de México'},
            {'destino': 'Rotterdam', 'distancia_nm': 5400, 'tiempo_dias': 19, 'costo_usd': 2300, 'via': 'Atlántico'}
        ],
        'Ensenada': [
            {'destino': 'Los Angeles', 'distancia_nm': 280, 'tiempo_dias': 1, 'costo_usd': 350, 'via': 'Cabotaje'},
            {'destino': 'San Francisco', 'distancia_nm': 520, 'tiempo_dias': 2, 'costo_usd': 450, 'via': 'Costa Pacífico'},
            {'destino': 'Shanghai', 'distancia_nm': 5800, 'tiempo_dias': 17, 'costo_usd': 2600, 'via': 'Transpacífico'},
            {'destino': 'Vancouver', 'distancia_nm': 1100, 'tiempo_dias': 4, 'costo_usd': 700, 'via': 'Costa Pacífico'}
        ],
        'Tuxpan': [
            {'destino': 'Houston', 'distancia_nm': 920, 'tiempo_dias': 3, 'costo_usd': 650, 'via': 'Golfo de México'},
            {'destino': 'Tampa', 'distancia_nm': 1050, 'tiempo_dias': 4, 'costo_usd': 700, 'via': 'Golfo de México'},
            {'destino': 'Miami', 'distancia_nm': 1250, 'tiempo_dias': 5, 'costo_usd': 800, 'via': 'Golfo de México'},
            {'destino': 'Rotterdam', 'distancia_nm': 5300, 'tiempo_dias': 18, 'costo_usd': 2250, 'via': 'Atlántico'}
        ]
    }
    
    return rutas.get(puerto_origen, [])


def generar_buques_tiempo_real(puerto):
    """Genera datos simulados de buques en puerto o en tránsito"""
    tipos_buque = ['Portacontenedores', 'Granelero', 'Petrolero', 'Ro-Ro', 'Carga General']
    estados = ['En Puerto', 'Aproximándose', 'En Descarga', 'En Carga', 'Saliendo']
    
    num_buques = np.random.randint(3, 12)
    buques = []
    
    for i in range(num_buques):
        tipo = np.random.choice(tipos_buque)
        estado = np.random.choice(estados)
        
        if estado == 'En Puerto':
            eta_hrs = 0
            etd_hrs = np.random.randint(6, 48)
        elif estado == 'Aproximándose':
            eta_hrs = np.random.randint(2, 24)
            etd_hrs = eta_hrs + np.random.randint(24, 72)
        elif estado == 'En Descarga' or estado == 'En Carga':
            eta_hrs = 0
            etd_hrs = np.random.randint(12, 36)
        else:
            eta_hrs = 0
            etd_hrs = np.random.randint(1, 6)
        
        buque = {
            'Nombre': f"{tipo[:3].upper()}-{1000+i}",
            'Tipo': tipo,
            'Estado': estado,
            'ETA_hrs': eta_hrs,
            'ETD_hrs': etd_hrs,
            'Carga_TEUs': np.random.randint(500, 8000) if tipo == 'Portacontenedores' else 0,
            'Bandera': np.random.choice(['Panamá', 'Liberia', 'México', 'Malta', 'Singapur'])
        }
        buques.append(buque)
    
    return pd.DataFrame(buques)


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

def page_puertos_maritimos():
    """Análisis geográfico de puertos marítimos y operaciones portuarias."""
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #F4F7F6 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 30px 40px; 
                    border-radius: 15px; 
                    margin-bottom: 30px;
                    box-shadow: 0 8px 20px rgba(17, 16, 29, 0.3);'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'>⚓ Puertos Marítimos Mexicanos</h1>
            <p style='color: #29B5E8; font-size: 1.2rem; font-weight: 500; margin-top: 10px; margin-bottom: 0;'>Análisis de capacidad, operaciones, congestión y seguimiento de buques</p>
        </div>
    """, unsafe_allow_html=True)
    
    if 'sistema_alertas_puertos' not in st.session_state:
        st.session_state.sistema_alertas_puertos = SistemaAlertasPuertos()
    
    sistema_alertas = st.session_state.sistema_alertas_puertos
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    with col_btn1:
        btn_recargar = st.button("🔄 Recargar Datos", help="Recarga datos de puertos", key="btn_recargar_puertos")
    with col_btn2:
        usar_datos_reales = st.checkbox("📊 Datos Reales", value=False, help="Alternar entre datos simulados y reales", key="check_real_puertos")
    with col_btn3:
        st.caption("📡 Monitoreo en tiempo real de puertos marítimos")
    
    df_puertos = cargar_datos_puertos_reales()
    
    if df_puertos is None or df_puertos.empty:
        st.error("❌ No se pudieron cargar datos de puertos")
        return
    
    def calcular_indice_saturacion(volumen, capacidad):
        idx = (volumen / capacidad) * 100
        if idx > 80:
            status = "Crítico"
        elif idx > 60:
            status = "Alto"
        else:
            status = "Normal"
        return round(idx, 2), status
    
    if 'Vol_Actual' not in df_puertos.columns:
        df_puertos['Vol_Actual'] = np.random.randint(50000, 300000, len(df_puertos))
    
    if 'Capacidad' not in df_puertos.columns:
        df_puertos['Capacidad'] = df_puertos['Vol_Actual'] * np.random.uniform(1.1, 1.5, len(df_puertos))
    
    if 'Operaciones' not in df_puertos.columns:
        df_puertos['Operaciones'] = np.random.randint(100, 500, len(df_puertos))
    
    if 'Lat' not in df_puertos.columns or 'Lon' not in df_puertos.columns:
        coords_default = {
            'Manzanillo': (19.0522, -104.3158),
            'Veracruz': (19.1738, -96.1342),
            'Lázaro Cárdenas': (17.9585, -102.1891),
            'Altamira': (22.3943, -97.9377),
            'Ensenada': (31.8667, -116.6000),
            'Tuxpan': (20.9577, -97.4054)
        }
        df_puertos['Lat'] = df_puertos['Puerto'].map(lambda x: coords_default.get(x, (20.0, -100.0))[0])
        df_puertos['Lon'] = df_puertos['Puerto'].map(lambda x: coords_default.get(x, (20.0, -100.0))[1])
    
    if 'Tipo_Carga' not in df_puertos.columns:
        df_puertos['Tipo_Carga'] = 'Contenedores'
    
    if 'Saturacion' not in df_puertos.columns or 'Estado' not in df_puertos.columns:
        df_puertos['Saturacion'], df_puertos['Estado'] = zip(*df_puertos.apply(
            lambda x: calcular_indice_saturacion(x['Vol_Actual'], x['Capacidad']), axis=1
        ))
    
    df_puertos['Capacidad_Disponible'] = df_puertos['Capacidad'] - df_puertos['Vol_Actual']
    
    alertas = sistema_alertas.evaluar_puertos(df_puertos)
    stats_alertas = sistema_alertas.obtener_estadisticas_alertas()
    
    st.markdown("---")
    
    # ============ SISTEMA DE ALERTAS ============
    st.subheader("🚨 Sistema de Alertas Portuarias")
    
    if alertas:
        alertas_criticas = [a for a in alertas if '🔴' in a['nivel']]
        alertas_altas = [a for a in alertas if '🟠' in a['nivel']]
        alertas_medias = [a for a in alertas if '🟡' in a['nivel']]
        
        col_alert1, col_alert2, col_alert3 = st.columns(3)
        with col_alert1:
            st.metric("🔴 Alertas Críticas", len(alertas_criticas), help="Congestión >85% o Espera >72hrs")
        with col_alert2:
            st.metric("🟠 Alertas Altas", len(alertas_altas), help="Congestión >70% o Espera >48hrs")
        with col_alert3:
            st.metric("🟡 Alertas Medias", len(alertas_medias), help="Congestión >60% o Espera >24hrs")
        
        if alertas_criticas:
            st.markdown("<div style='background-color: #EF553B; color: white; padding: 15px; border-radius: 10px; margin: 10px 0;'><h3 style='color: white; margin: 0;'>🔴 ALERTAS CRÍTICAS</h3></div>", unsafe_allow_html=True)
            for alerta in alertas_criticas:
                st.markdown(f"<div style='background-color: #ffebee; border-left: 4px solid #EF553B; padding: 12px; margin: 8px 0; border-radius: 5px;'><span style='color: #F4F7F6; font-weight: 600;'>{alerta['puerto']}</span> - <span style='color: #F4F7F6;'>{alerta['mensaje']}</span></div>", unsafe_allow_html=True)
        
        if alertas_altas:
            with st.expander(f"🟠 Ver {len(alertas_altas)} Alertas de Nivel Alto"):
                for alerta in alertas_altas:
                    st.warning(f"**{alerta['puerto']}** - {alerta['mensaje']}")
        
        if alertas_medias:
            with st.expander(f"🟡 Ver {len(alertas_medias)} Alertas de Nivel Medio"):
                for alerta in alertas_medias:
                    st.info(f"**{alerta['puerto']}** - {alerta['mensaje']}")
    else:
        st.success("✅ No hay alertas activas. Todos los puertos operan en niveles normales.")
    
    st.markdown("---")
    
    # ============ MÉTRICAS PRINCIPALES ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #29B5E8 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(41, 181, 232, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>📊 Indicadores Generales</h3>
        </div>
    """, unsafe_allow_html=True)
    
    total_volumen = df_puertos['Vol_Actual'].sum()
    total_capacidad = df_puertos['Capacidad'].sum()
    saturacion_promedio = df_puertos['Saturacion'].mean()
    puertos_criticos = len(df_puertos[df_puertos['Estado'] == 'Crítico'])
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #29B5E8;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #29B5E8; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Volumen Total</p>
                <h2 style='color: #F4F7F6; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{total_volumen:,.0f}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>📦 TEUs procesados</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid #29B5E8;
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: #29B5E8; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Capacidad Total</p>
                <h2 style='color: #F4F7F6; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{total_capacidad:,.0f}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>🏗️ TEUs disponibles</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m3:
        color_saturacion = '#EF553B' if saturacion_promedio > 80 else '#FFA726' if saturacion_promedio > 60 else '#4CAF50'
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid {color_saturacion};
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: {color_saturacion}; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Saturación Promedio</p>
                <h2 style='color: {color_saturacion}; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{saturacion_promedio:.1f}%</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>📊 Ocupación nacional</p>
            </div>
        """, unsafe_allow_html=True)
    with col_m4:
        color_critico = '#EF553B' if puertos_criticos > 0 else '#4CAF50'
        st.markdown(f"""
            <div style='background-color: white; 
                        border-left: 5px solid {color_critico};
                        padding: 20px; 
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                        margin: 10px 0;'>
                <p style='color: {color_critico}; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Puertos Críticos</p>
                <h2 style='color: {color_critico}; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{puertos_criticos}</h2>
                <p style='color: #666; font-size: 0.85rem; margin: 0;'>⚠️ Saturación > 80%</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ ANÁLISIS POR PUERTO ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #29B5E8 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(41, 181, 232, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>🏗️ Análisis Detallado por Puerto</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_tabla, col_grafico = st.columns([1, 1])
    
    with col_tabla:
        st.markdown("<h4 style='color: #F4F7F6; font-weight: 600;'>Estado Operativo</h4>", unsafe_allow_html=True)
        
        def color_estado(val):
            if val == 'Crítico':
                return 'background-color: #FFEBEE; color: #EF553B; font-weight: 600;'
            elif val == 'Alto':
                return 'background-color: #FFF3E0; color: #FFA726; font-weight: 600;'
            else:
                return 'background-color: #E8F5E9; color: #4CAF50; font-weight: 600;'
        
        df_display = df_puertos[['Puerto', 'Vol_Actual', 'Capacidad', 'Saturacion', 'Estado']].copy()
        st.dataframe(
            df_display.style.format({
                'Vol_Actual': '{:,.0f}',
                'Capacidad': '{:,.0f}',
                'Saturacion': '{:.1f}%'
            }).applymap(color_estado, subset=['Estado']),
            use_container_width=True,
            height=220
        )
    
    with col_grafico:
        st.markdown("<h4 style='color: #F4F7F6; font-weight: 600;'>Saturación por Puerto</h4>", unsafe_allow_html=True)
        
        color_map = {'Crítico': '#EF553B', 'Alto': '#FFA726', 'Normal': '#4CAF50'}
        df_puertos['Color'] = df_puertos['Estado'].map(color_map)
        
        fig_saturacion = px.bar(
            df_puertos.sort_values('Saturacion', ascending=True),
            y='Puerto',
            x='Saturacion',
            orientation='h',
            color='Estado',
            color_discrete_map=color_map,
            text='Saturacion',
            labels={'Saturacion': '% Saturación'}
        )
        fig_saturacion.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_saturacion.update_layout(
            height=250,
            showlegend=True,
            title_font_color='#F4F7F6',
            font=dict(color='#F4F7F6', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_saturacion, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ CAPACIDAD DISPONIBLE ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #29B5E8 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(41, 181, 232, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>📈 Capacidad y Utilización</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_cap1, col_cap2 = st.columns([1, 1])
    
    with col_cap1:
        st.markdown("<h4 style='color: #F4F7F6; font-weight: 600;'>Comparativa Volumen vs Capacidad</h4>", unsafe_allow_html=True)
        
        df_melt = df_puertos.melt(
            id_vars=['Puerto'],
            value_vars=['Vol_Actual', 'Capacidad'],
            var_name='Métrica',
            value_name='TEUs'
        )
        
        fig_comparativa = px.bar(
            df_melt,
            x='Puerto',
            y='TEUs',
            color='Métrica',
            barmode='group',
            color_discrete_map={'Vol_Actual': '#29B5E8', 'Capacidad': '#29B5E8'},
            labels={'TEUs': 'TEUs/mes'}
        )
        fig_comparativa.update_layout(
            height=350,
            title_font_color='#F4F7F6',
            font=dict(color='#F4F7F6', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend_title_text='',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_comparativa, use_container_width=True)
    
    with col_cap2:
        st.markdown("<h4 style='color: #F4F7F6; font-weight: 600;'>Distribución de Volumen</h4>", unsafe_allow_html=True)
        
        fig_pie = px.pie(
            df_puertos,
            values='Vol_Actual',
            names='Puerto',
            hole=0.4,
            color_discrete_sequence=['#29B5E8', '#29B5E8', '#EF553B', '#FFA726']
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            height=350,
            font=dict(color='#F4F7F6', family='Inter'),
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=False
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ MAPA GEOGRÁFICO ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #29B5E8 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(41, 181, 232, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>🗺️ Ubicación Geográfica</h3>
        </div>
    """, unsafe_allow_html=True)
    
    fig_mapa = px.scatter_mapbox(
        df_puertos,
        lat='Lat',
        lon='Lon',
        hover_name='Puerto',
        hover_data={'Saturacion': ':.1f', 'Vol_Actual': ':,.0f', 'Estado': True, 'Lat': False, 'Lon': False},
        color='Estado',
        color_discrete_map=color_map,
        size='Vol_Actual',
        size_max=30,
        zoom=4.5,
        height=500
    )
    fig_mapa.update_layout(
        mapbox_style="open-street-map",
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig_mapa, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ ANÁLISIS DE TIEMPOS DE ESPERA Y CONGESTIÓN ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #29B5E8 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(41, 181, 232, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>⏱️ Tiempos de Espera y Congestión Portuaria</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_tiempo1, col_tiempo2 = st.columns([1, 1])
    
    with col_tiempo1:
        st.markdown("<h4 style='color: #F4F7F6; font-weight: 600;'>Tiempos de Espera por Puerto</h4>", unsafe_allow_html=True)
        
        fig_espera = px.bar(
            df_puertos.sort_values('Tiempo_Espera_hrs', ascending=False),
            x='Tiempo_Espera_hrs',
            y='Puerto',
            orientation='h',
            text='Tiempo_Espera_hrs',
            labels={'Tiempo_Espera_hrs': 'Horas de Espera'},
            color='Tiempo_Espera_hrs',
            color_continuous_scale=['#4CAF50', '#FFA726', '#EF553B']
        )
        fig_espera.update_traces(texttemplate='%{text:.0f}hrs', textposition='outside')
        fig_espera.update_layout(
            height=300,
            showlegend=False,
            title_font_color='#F4F7F6',
            font=dict(color='#F4F7F6', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_espera, use_container_width=True)
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            tiempo_promedio = df_puertos['Tiempo_Espera_hrs'].mean()
            st.metric("⏰ Tiempo Promedio Espera", f"{tiempo_promedio:.1f} hrs")
        with col_t2:
            puerto_max_espera = df_puertos.loc[df_puertos['Tiempo_Espera_hrs'].idxmax(), 'Puerto']
            st.metric("🔴 Puerto con Mayor Espera", puerto_max_espera)
    
    with col_tiempo2:
        st.markdown("<h4 style='color: #F4F7F6; font-weight: 600;'>Índice de Congestión</h4>", unsafe_allow_html=True)
        
        fig_congestion = px.bar(
            df_puertos.sort_values('Indice_Congestion', ascending=False),
            x='Indice_Congestion',
            y='Puerto',
            orientation='h',
            text='Indice_Congestion',
            labels={'Indice_Congestion': '% Congestión'},
            color='Indice_Congestion',
            color_continuous_scale=['#4CAF50', '#FFA726', '#EF553B']
        )
        fig_congestion.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
        fig_congestion.update_layout(
            height=300,
            showlegend=False,
            title_font_color='#F4F7F6',
            font=dict(color='#F4F7F6', family='Inter'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_congestion, use_container_width=True)
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            congestion_promedio = df_puertos['Indice_Congestion'].mean()
            st.metric("📊 Congestión Promedio", f"{congestion_promedio:.1f}%")
        with col_c2:
            total_buques_esperando = df_puertos['Buques_Esperando'].sum()
            st.metric("🚢 Buques en Espera", f"{total_buques_esperando}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ COMPARACIÓN DE RUTAS MARÍTIMAS ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #29B5E8 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(41, 181, 232, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>🌊 Comparación de Rutas Marítimas y Costos</h3>
        </div>
    """, unsafe_allow_html=True)
    
    puerto_seleccionado = st.selectbox(
        "Selecciona el puerto de origen:",
        options=df_puertos['Puerto'].tolist(),
        key="select_puerto_rutas"
    )
    
    rutas = calcular_rutas_maritimas(puerto_seleccionado)
    
    if rutas:
        df_rutas = pd.DataFrame(rutas)
        
        col_ruta1, col_ruta2 = st.columns([1, 1])
        
        with col_ruta1:
            st.markdown(f"<h4 style='color: #F4F7F6; font-weight: 600;'>Rutas desde {puerto_seleccionado}</h4>", unsafe_allow_html=True)
            
            st.dataframe(
                df_rutas[['destino', 'distancia_nm', 'tiempo_dias', 'costo_usd', 'via']].style.format({
                    'distancia_nm': '{:,.0f} NM',
                    'tiempo_dias': '{:.0f} días',
                    'costo_usd': '${:,.0f}'
                }),
                use_container_width=True,
                height=250
            )
            
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                ruta_mas_rapida = df_rutas.loc[df_rutas['tiempo_dias'].idxmin()]
                st.metric("⚡ Ruta Más Rápida", f"{ruta_mas_rapida['destino']}", f"{ruta_mas_rapida['tiempo_dias']} días")
            with col_r2:
                ruta_mas_economica = df_rutas.loc[df_rutas['costo_usd'].idxmin()]
                st.metric("💰 Ruta Más Económica", f"{ruta_mas_economica['destino']}", f"${ruta_mas_economica['costo_usd']:,.0f}")
        
        with col_ruta2:
            st.markdown("<h4 style='color: #F4F7F6; font-weight: 600;'>Comparativa de Costos por Destino</h4>", unsafe_allow_html=True)
            
            fig_costos = px.bar(
                df_rutas.sort_values('costo_usd', ascending=True),
                y='destino',
                x='costo_usd',
                orientation='h',
                text='costo_usd',
                labels={'costo_usd': 'Costo USD', 'destino': 'Destino'},
                color='tiempo_dias',
                color_continuous_scale='Viridis'
            )
            fig_costos.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
            fig_costos.update_layout(
                height=250,
                title_font_color='#F4F7F6',
                font=dict(color='#F4F7F6', family='Inter'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=10, b=0),
                coloraxis_colorbar_title="Días"
            )
            st.plotly_chart(fig_costos, use_container_width=True)
            
            st.markdown("<h4 style='color: #F4F7F6; font-weight: 600;'>Relación Tiempo vs Costo</h4>", unsafe_allow_html=True)
            fig_scatter = px.scatter(
                df_rutas,
                x='tiempo_dias',
                y='costo_usd',
                text='destino',
                size='distancia_nm',
                color='via',
                labels={'tiempo_dias': 'Tiempo (días)', 'costo_usd': 'Costo (USD)', 'via': 'Vía'}
            )
            fig_scatter.update_traces(textposition='top center')
            fig_scatter.update_layout(
                height=300,
                title_font_color='#F4F7F6',
                font=dict(color='#F4F7F6', family='Inter'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=10, b=0)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning(f"⚠️ No hay rutas disponibles desde {puerto_seleccionado}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ SEGUIMIENTO DE BUQUES EN TIEMPO REAL ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #29B5E8 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(41, 181, 232, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>🚢 Seguimiento de Buques en Tiempo Real</h3>
        </div>
    """, unsafe_allow_html=True)
    
    puerto_seguimiento = st.selectbox(
        "Selecciona el puerto para ver buques:",
        options=df_puertos['Puerto'].tolist(),
        key="select_puerto_seguimiento"
    )
    
    df_buques = generar_buques_tiempo_real(puerto_seguimiento)
    
    st.markdown(f"<h4 style='color: #F4F7F6; font-weight: 600;'>Buques en {puerto_seguimiento}</h4>", unsafe_allow_html=True)
    
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    with col_b1:
        total_buques = len(df_buques)
        st.metric("🚢 Total Buques", total_buques)
    with col_b2:
        buques_puerto = len(df_buques[df_buques['Estado'] == 'En Puerto'])
        st.metric("⚓ En Puerto", buques_puerto)
    with col_b3:
        buques_aproximando = len(df_buques[df_buques['Estado'] == 'Aproximándose'])
        st.metric("🔵 Aproximándose", buques_aproximando)
    with col_b4:
        total_teus = df_buques['Carga_TEUs'].sum()
        st.metric("📦 Total TEUs", f"{total_teus:,.0f}")
    
    col_tabla_buques, col_grafico_buques = st.columns([2, 1])
    
    with col_tabla_buques:
        st.markdown("<p style='color: #F4F7F6; font-weight: 600; margin-top: 15px;'>Estado de Buques</p>", unsafe_allow_html=True)
        
        def color_estado_buque(val):
            if val == 'En Puerto':
                return 'background-color: #E8F5E9; color: #4CAF50; font-weight: 600;'
            elif val == 'Aproximándose':
                return 'background-color: #E3F2FD; color: #2196F3; font-weight: 600;'
            elif val == 'En Descarga' or val == 'En Carga':
                return 'background-color: #FFF3E0; color: #FFA726; font-weight: 600;'
            else:
                return 'background-color: #F3E5F5; color: #9C27B0; font-weight: 600;'
        
        st.dataframe(
            df_buques.style.format({
                'ETA_hrs': '{:.0f}hrs',
                'ETD_hrs': '{:.0f}hrs',
                'Carga_TEUs': '{:,.0f}'
            }).applymap(color_estado_buque, subset=['Estado']),
            use_container_width=True,
            height=300
        )
    
    with col_grafico_buques:
        st.markdown("<p style='color: #F4F7F6; font-weight: 600; margin-top: 15px;'>Distribución por Estado</p>", unsafe_allow_html=True)
        
        estados_count = df_buques['Estado'].value_counts().reset_index()
        estados_count.columns = ['Estado', 'Cantidad']
        
        fig_estados = px.pie(
            estados_count,
            values='Cantidad',
            names='Estado',
            hole=0.4,
            color_discrete_sequence=['#4CAF50', '#2196F3', '#FFA726', '#9C27B0', '#EF553B']
        )
        fig_estados.update_traces(textposition='inside', textinfo='percent+label')
        fig_estados.update_layout(
            height=300,
            font=dict(color='#F4F7F6', family='Inter'),
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )
        st.plotly_chart(fig_estados, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ MAPA DE TRÁFICO MARÍTIMO EN TIEMPO REAL ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #29B5E8 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(41, 181, 232, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>🌊 Mapa de Tráfico Marítimo en Tiempo Real</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background-color: #E3F2FD; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #2196F3;'>
            <p style='margin: 0; color: #1565C0;'>
                <strong>💡 Obtén datos reales:</strong> Registra tu API key gratuita en 
                <a href='https://www.aishub.net/api' target='_blank' style='color: #1565C0; text-decoration: underline;'>AIS Hub</a> 
                y configúrala en el archivo .env como AISHUB_API_KEY
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    aishub_key = st.sidebar.text_input(
        "🔑 AIS Hub API Key (opcional)",
        type="password",
        value=os.getenv('AISHUB_API_KEY', ''),
        help="Obtén tu API key gratuita en https://www.aishub.net/api"
    )
    
    df_trafico = obtener_trafico_maritimo_aishub(api_key=aishub_key)
    
    if df_trafico is not None and not df_trafico.empty:
        col_filter1, col_filter2 = st.columns([1, 1])
        with col_filter1:
            tipos_disponibles = df_trafico['Tipo'].unique().tolist()
            tipos_seleccionados = st.multiselect(
                "Filtrar por tipo de buque:",
                options=tipos_disponibles,
                default=tipos_disponibles,
                key="filter_tipo_buque"
            )
        
        with col_filter2:
            min_velocidad = st.slider(
                "Velocidad mínima (nudos):",
                min_value=0.0,
                max_value=30.0,
                value=0.0,
                step=1.0,
                key="filter_velocidad"
            )
        
        df_filtrado = df_trafico[
            (df_trafico['Tipo'].isin(tipos_seleccionados)) &
            (df_trafico['Velocidad'] >= min_velocidad)
        ]
        
        col_traf1, col_traf2, col_traf3, col_traf4 = st.columns(4)
        with col_traf1:
            st.metric("🚢 Total Buques", len(df_filtrado))
        with col_traf2:
            velocidad_promedio = df_filtrado['Velocidad'].mean()
            st.metric("⚡ Velocidad Promedio", f"{velocidad_promedio:.1f} kts")
        with col_traf3:
            buques_movimiento = len(df_filtrado[df_filtrado['Velocidad'] > 1])
            st.metric("🔵 En Movimiento", buques_movimiento)
        with col_traf4:
            buques_fondeados = len(df_filtrado[df_filtrado['Velocidad'] <= 1])
            st.metric("⚓ Fondeados/En Puerto", buques_fondeados)
        
        st.markdown("<h4 style='color: #F4F7F6; font-weight: 600; margin-top: 20px;'>Posiciones en Tiempo Real</h4>", unsafe_allow_html=True)
        
        fig_trafico = px.scatter_mapbox(
            df_filtrado,
            lat='Lat',
            lon='Lon',
            hover_name='Nombre',
            hover_data={
                'Tipo': True,
                'Velocidad': ':.1f',
                'Rumbo': ':.0f',
                'MMSI': True,
                'Lat': False,
                'Lon': False
            },
            color='Tipo',
            size='Velocidad',
            size_max=15,
            zoom=5,
            height=600,
            labels={'Velocidad': 'Velocidad (kts)', 'Rumbo': 'Rumbo (°)'}
        )
        fig_trafico.update_layout(
            mapbox_style="open-street-map",
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_trafico, use_container_width=True)
        
        with st.expander("📋 Ver tabla detallada de buques"):
            st.dataframe(
                df_filtrado[['Nombre', 'Tipo', 'Lat', 'Lon', 'Velocidad', 'Rumbo', 'MMSI']].style.format({
                    'Lat': '{:.4f}',
                    'Lon': '{:.4f}',
                    'Velocidad': '{:.1f} kts',
                    'Rumbo': '{:.0f}°'
                }),
                use_container_width=True,
                height=300
            )
    else:
        st.error("❌ No se pudieron cargar datos de tráfico marítimo")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============ RASTREO DE CONTENEDORES ============
    st.markdown("""
        <div style='background: linear-gradient(135deg, #29B5E8 0%, #29B5E8 100%); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(41, 181, 232, 0.2);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 600;'>📦 Rastreo de Contenedores</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background-color: #FFF3E0; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #FFA726;'>
            <p style='margin: 0; color: #E65100;'>
                <strong>ℹ️ Sistema de demostración:</strong> Ingresa cualquier número de contenedor (ej: MSCU1234567) 
                para ver cómo funciona el tracking.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_search, col_btn = st.columns([3, 1])
    with col_search:
        numero_contenedor = st.text_input(
            "🔍 Ingresa el número de contenedor:",
            placeholder="Ej: MSCU1234567, CMAU8901234",
            help="Formato: 4 letras + 7 números",
            key="input_contenedor"
        )
    with col_btn:
        btn_buscar = st.button("🔎 Buscar", type="primary", key="btn_buscar_contenedor", use_container_width=True)
    
    if btn_buscar and numero_contenedor:
        resultado = buscar_contenedor(numero_contenedor)
        
        if resultado:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #F4F7F6 0%, #29B5E8 100%); 
                            color: white; 
                            padding: 20px; 
                            border-radius: 10px; 
                            margin: 20px 0;
                            box-shadow: 0 4px 15px rgba(17, 16, 29, 0.2);'>
                    <h2 style='color: white; margin: 0; font-size: 1.8rem;'>📦 {resultado['numero']}</h2>
                    <p style='color: #29B5E8; margin: 5px 0 0 0; font-size: 1.1rem;'>{resultado['naviera']} | {resultado['tipo']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            col_info1, col_info2, col_info3, col_info4 = st.columns(4)
            
            with col_info1:
                color_estado = {
                    'En Tránsito Marítimo': '#2196F3',
                    'En Puerto': '#4CAF50',
                    'En Aduana': '#FFA726',
                    'En Transporte Terrestre': '#9C27B0',
                    'Entregado': '#4CAF50',
                    'Disponible para Retiro': '#00BCD4'
                }.get(resultado['estado'], '#666')
                
                st.markdown(f"""
                    <div style='background-color: white; 
                                border-left: 5px solid {color_estado};
                                padding: 15px; 
                                border-radius: 8px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                        <p style='color: #666; font-size: 0.85rem; margin: 0;'>Estado Actual</p>
                        <h3 style='color: {color_estado}; margin: 5px 0; font-size: 1.3rem;'>{resultado['estado']}</h3>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_info2:
                st.markdown(f"""
                    <div style='background-color: white; 
                                border-left: 5px solid #29B5E8;
                                padding: 15px; 
                                border-radius: 8px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                        <p style='color: #666; font-size: 0.85rem; margin: 0;'>Ubicación Actual</p>
                        <h3 style='color: #F4F7F6; margin: 5px 0; font-size: 1.1rem;'>{resultado['ubicacion_actual']}</h3>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_info3:
                eta_text = resultado['eta'].strftime('%d/%m/%Y') if resultado['eta'] else 'Entregado'
                st.markdown(f"""
                    <div style='background-color: white; 
                                border-left: 5px solid #29B5E8;
                                padding: 15px; 
                                border-radius: 8px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                        <p style='color: #666; font-size: 0.85rem; margin: 0;'>ETA Destino</p>
                        <h3 style='color: #F4F7F6; margin: 5px 0; font-size: 1.1rem;'>{eta_text}</h3>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_info4:
                st.markdown(f"""
                    <div style='background-color: white; 
                                border-left: 5px solid #9C27B0;
                                padding: 15px; 
                                border-radius: 8px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                        <p style='color: #666; font-size: 0.85rem; margin: 0;'>Peso</p>
                        <h3 style='color: #F4F7F6; margin: 5px 0; font-size: 1.1rem;'>{resultado['peso_kg']:,} kg</h3>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_ruta_info, col_timeline = st.columns([1, 2])
            
            with col_ruta_info:
                st.markdown("<h4 style='color: #F4F7F6; font-weight: 600;'>🗺️ Ruta</h4>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div style='background-color: #F4F7F6; padding: 15px; border-radius: 8px;'>
                        <p style='margin: 5px 0;'><strong>Origen:</strong> {resultado['origen']}</p>
                        <p style='margin: 5px 0;'><strong>Destino:</strong> {resultado['destino']}</p>
                        <p style='margin: 5px 0;'><strong>Última actualización:</strong><br>{resultado['ultima_actualizacion'].strftime('%d/%m/%Y %H:%M')}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_timeline:
                st.markdown("<h4 style='color: #F4F7F6; font-weight: 600;'>📅 Historial de Eventos</h4>", unsafe_allow_html=True)
                
                for evento in reversed(resultado['eventos']):
                    fecha_str = evento['fecha'].strftime('%d/%m/%Y %H:%M')
                    st.markdown(f"""
                        <div style='background-color: white; 
                                    padding: 12px; 
                                    margin: 8px 0; 
                                    border-left: 4px solid #29B5E8;
                                    border-radius: 5px;
                                    box-shadow: 0 1px 4px rgba(0,0,0,0.1);'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <div>
                                    <strong style='color: #F4F7F6;'>{evento['evento']}</strong>
                                    <p style='margin: 3px 0; color: #666; font-size: 0.9rem;'>📍 {evento['ubicacion']}</p>
                                    <p style='margin: 3px 0; color: #999; font-size: 0.85rem;'>{evento['detalles']}</p>
                                </div>
                                <span style='color: #29B5E8; font-size: 0.85rem; white-space: nowrap; margin-left: 15px;'>{fecha_str}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if resultado.get('info_retiro'):
                info = resultado['info_retiro']
                
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%); 
                                color: white; 
                                padding: 20px; 
                                border-radius: 10px; 
                                margin: 20px 0;
                                box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);'>
                        <h3 style='color: white; margin: 0; font-size: 1.5rem;'>✅ CONTENEDOR DISPONIBLE PARA RETIRO</h3>
                        <p style='color: #E8F5E9; margin: 5px 0 0 0;'>Liberado por aduana - Listo para recolección</p>
                    </div>
                """, unsafe_allow_html=True)
                
                col_ret1, col_ret2, col_ret3, col_ret4 = st.columns(4)
                
                with col_ret1:
                    color_dias = '#EF553B' if info['dias_libres_restantes'] <= 2 else '#4CAF50'
                    st.markdown(f"""
                        <div style='background-color: white; 
                                    border-left: 5px solid {color_dias};
                                    padding: 15px; 
                                    border-radius: 8px;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <p style='color: #666; font-size: 0.85rem; margin: 0;'>Días Libres Restantes</p>
                            <h2 style='color: {color_dias}; margin: 5px 0; font-size: 2rem;'>{info['dias_libres_restantes']}</h2>
                            <p style='color: #999; font-size: 0.8rem; margin: 0;'>días</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_ret2:
                    color_cargo = '#EF553B' if info['cargo_demora_usd'] > 0 else '#4CAF50'
                    st.markdown(f"""
                        <div style='background-color: white; 
                                    border-left: 5px solid {color_cargo};
                                    padding: 15px; 
                                    border-radius: 8px;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <p style='color: #666; font-size: 0.85rem; margin: 0;'>Cargo por Demora</p>
                            <h2 style='color: {color_cargo}; margin: 5px 0; font-size: 2rem;'>${info['cargo_demora_usd']:,.0f}</h2>
                            <p style='color: #999; font-size: 0.8rem; margin: 0;'>USD</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_ret3:
                    st.markdown(f"""
                        <div style='background-color: white; 
                                    border-left: 5px solid #29B5E8;
                                    padding: 15px; 
                                    border-radius: 8px;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <p style='color: #666; font-size: 0.85rem; margin: 0;'>Disponible Desde</p>
                            <h3 style='color: #F4F7F6; margin: 5px 0; font-size: 1.2rem;'>{info['fecha_disponibilidad'].strftime('%d/%m/%Y')}</h3>
                            <p style='color: #999; font-size: 0.8rem; margin: 0;'>{info['fecha_disponibilidad'].strftime('%H:%M')}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_ret4:
                    icon_cita = '📅' if info['requiere_cita'] else '✅'
                    texto_cita = 'Requiere cita' if info['requiere_cita'] else 'Sin cita previa'
                    st.markdown(f"""
                        <div style='background-color: white; 
                                    border-left: 5px solid #9C27B0;
                                    padding: 15px; 
                                    border-radius: 8px;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <p style='color: #666; font-size: 0.85rem; margin: 0;'>Sistema de Retiro</p>
                            <h3 style='color: #F4F7F6; margin: 5px 0; font-size: 1.2rem;'>{icon_cita} {texto_cita}</h3>
                            <p style='color: #999; font-size: 0.8rem; margin: 0;'>{info['terminal']['sistema_citas']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                if info['observaciones']:
                    st.markdown("<br>", unsafe_allow_html=True)
                    for obs in info['observaciones']:
                        if '⚠️' in obs or 'URGENTE' in obs:
                            st.warning(obs)
                        else:
                            st.info(obs)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                col_terminal, col_horarios = st.columns([1, 1])
                
                with col_terminal:
                    st.markdown("<h4 style='color: #F4F7F6; font-weight: 600;'>🏢 Información de la Terminal</h4>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div style='background-color: white; 
                                    padding: 20px; 
                                    border-radius: 10px;
                                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                            <p style='margin: 8px 0;'><strong>Terminal:</strong> {info['terminal']['nombre']}</p>
                            <p style='margin: 8px 0;'><strong>Dirección:</strong> {info['terminal']['direccion']}</p>
                            <p style='margin: 8px 0;'><strong>📞 Teléfono:</strong> {info['terminal']['telefono']}</p>
                            <p style='margin: 8px 0;'><strong>📧 Email:</strong> {info['terminal']['email']}</p>
                            <p style='margin: 8px 0;'><strong>📍 Posición en patio:</strong> {info['posicion_patio']}</p>
                            <p style='margin: 8px 0; padding: 10px; background-color: #E3F2FD; border-radius: 5px;'>
                                <strong>💡 Sistema de citas:</strong> {info['terminal']['sistema_citas']}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if info['requiere_cita']:
                        st.markdown(f"""
                            <div style='background-color: #FFF3E0; 
                                        padding: 15px; 
                                        border-radius: 8px; 
                                        margin-top: 15px;
                                        border-left: 4px solid #FFA726;'>
                                <p style='margin: 0;'><strong>📅 Cita sugerida:</strong></p>
                                <p style='margin: 5px 0; font-size: 1.1rem; color: #E65100;'>
                                    {info['cita_sugerida'].strftime('%d/%m/%Y a las %H:%M')}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                
                with col_horarios:
                    st.markdown("<h4 style='color: #F4F7F6; font-weight: 600;'>🕐 Horarios de Retiro</h4>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div style='background-color: white; 
                                    padding: 20px; 
                                    border-radius: 10px;
                                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                            <div style='padding: 12px; background-color: #E8F5E9; border-radius: 5px; margin-bottom: 10px;'>
                                <p style='margin: 0;'><strong>Lunes a Viernes:</strong></p>
                                <p style='margin: 5px 0; font-size: 1.2rem; color: #2E7D32;'>{info['horarios_retiro']['lunes_viernes']}</p>
                            </div>
                            <div style='padding: 12px; background-color: #E3F2FD; border-radius: 5px; margin-bottom: 10px;'>
                                <p style='margin: 0;'><strong>Sábado:</strong></p>
                                <p style='margin: 5px 0; font-size: 1.2rem; color: #131b2e;'>{info['horarios_retiro']['sabado']}</p>
                            </div>
                            <div style='padding: 12px; background-color: #FFEBEE; border-radius: 5px;'>
                                <p style='margin: 0;'><strong>Domingo:</strong></p>
                                <p style='margin: 5px 0; font-size: 1.2rem; color: #C62828;'>{info['horarios_retiro']['domingo']}</p>
                            </div>
                            <div style='margin-top: 15px; padding: 12px; background-color: #FFF9C4; border-radius: 5px;'>
                                <p style='margin: 0; color: #F57F17;'><strong>⚠️ Contacto de Emergencia:</strong></p>
                                <p style='margin: 5px 0; font-size: 1.1rem; color: #F57F17;'>{info['contacto_emergencia']}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown("<h4 style='color: #F4F7F6; font-weight: 600;'>📋 Documentación Requerida para Retiro</h4>", unsafe_allow_html=True)
                
                col_docs1, col_docs2 = st.columns(2)
                for idx, doc in enumerate(info['documentacion_requerida']):
                    col = col_docs1 if idx % 2 == 0 else col_docs2
                    with col:
                        st.markdown(f"""
                            <div style='background-color: white; 
                                        padding: 12px; 
                                        margin: 5px 0; 
                                        border-left: 4px solid #29B5E8;
                                        border-radius: 5px;
                                        box-shadow: 0 1px 4px rgba(0,0,0,0.1);'>
                                <p style='margin: 0; color: #F4F7F6;'>✓ {doc}</p>
                            </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                with col_btn1:
                    if st.button("📅 Programar Cita de Retiro", type="primary", use_container_width=True, key="btn_cita"):
                        st.success("✅ Funcionalidad de programación de citas próximamente disponible")
                with col_btn2:
                    if st.button("📄 Descargar Documentación", use_container_width=True, key="btn_docs"):
                        st.info("📄 Generando checklist de documentos...")
                with col_btn3:
                    if st.button("📧 Notificar al Transportista", use_container_width=True, key="btn_notify"):
                        st.info("📧 Sistema de notificaciones próximamente disponible")
            
            elif resultado['estado'] in ['En Aduana - Pendiente Liberación', 'En Puerto - Descargando']:
                st.markdown(f"""
                    <div style='background-color: #FFF3E0; 
                                padding: 20px; 
                                border-radius: 10px; 
                                margin: 20px 0;
                                border-left: 6px solid #FFA726;
                                box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                        <h4 style='color: #E65100; margin: 0 0 10px 0;'>⏳ Contenedor en proceso</h4>
                        <p style='margin: 5px 0; font-size: 1.1rem; color: #666;'>
                            <strong>Estado actual:</strong> {resultado['estado']}
                        </p>
                        <p style='margin: 5px 0; font-size: 1.1rem; color: #666;'>
                            <strong>Disponibilidad estimada:</strong> {resultado['eta'].strftime('%d/%m/%Y %H:%M') if resultado['eta'] else 'Calculando...'}
                        </p>
                        <p style='margin: 15px 0 0 0; padding: 12px; background-color: #FFECB3; border-radius: 5px; color: #E65100;'>
                            💡 <strong>Recomendación:</strong> Mantén tu documentación lista para agilizar el retiro una vez liberado
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Contenedor no encontrado. Verifica el número e intenta nuevamente.")

# PyTZ - Dependencia de Zonas Horarias

## 📋 Descripción

`pytz` es una librería esencial para **FreightMetrics** que proporciona soporte robusto para zonas horarias globales y conversiones de tiempo.

## 🎯 Propósito

- Manejo correcto de zonas horarias (México, Canadá, USA)
- Conversión de tiempos en operaciones aduanales
- Cálculo de horarios de operación fronteriza
- Sincronización de datos entre regiones

## 📦 Instalación

### Desde `requirements.txt`

```bash
pip install -r requirements.txt
```

**Versión recomendada:** `pytz>=2023.3`

### Instalación manual

```bash
pip install pytz>=2023.3
```

## 🔧 Uso en FreightMetrics

### Importación

```python
import pytz

# Definir zona horaria de México
TZ_MEXICO = pytz.timezone('America/Mexico_City')

# Convertir datetime a zona horaria específica
tz_mx = pytz.timezone('America/Mexico_City')
dt_converted = datetime.now(tz_mx)
```

### Ubicaciones principales de uso

| Archivo | Línea | Función |
|---------|-------|---------|
| `app.py` | 17, 1508 | Importación y conversión de timezones |
| `page_modules/_01_Monitoreo_Aduanas.py` | 16, 20 | Monitoreo de horarios aduanales |
| `page_modules/_00_Inicio.py` | 54, 57 | Dashboard inicial |
| `page_modules/_05_Puertos_Maritimos.py` | 16, 25 | Horarios de puertos |

## 🌍 Zonas horarias soportadas

```python
# Principales regiones
'America/Mexico_City'      # México
'America/Toronto'          # Canadá
'America/New_York'         # USA Este
'America/Los_Angeles'      # USA Oeste
'America/Denver'           # USA Centro
```

## ⚠️ Problemas comunes

### `ModuleNotFoundError: No module named 'pytz'`

**Causa:** Librería no instalada en el virtual environment

**Solución:**
```bash
source .venv/Scripts/activate  # Windows: .venv\Scripts\Activate
pip install pytz>=2023.3
```

### Errores de zona horaria

**Problema:** Conversión incorrecta de horas

**Solución:**
```python
# Usar timezone aware
from datetime import datetime
tz = pytz.timezone('America/Mexico_City')
now = datetime.now(tz)  # ✓ Correcto (timezone aware)
```

## 📊 Versión actual

- **Versión instalada:** v2026.1.post1
- **Estado:** ✅ Funcional
- **Última verificación:** 2026-04-13

## 🚀 Setup del proyecto

Para configurar FreightMetrics correctamente:

```bash
# 1. Clonar repositorio
git clone <repo-url>

# 2. Crear virtual environment
python -m venv .venv

# 3. Activar virtual environment
.venv\Scripts\Activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 4. Instalar dependencias (incluyendo pytz)
pip install -r requirements.txt

# 5. Ejecutar aplicación
streamlit run app.py
```

## 📚 Referencias

- Documentación oficial: https://pypi.org/project/pytz/
- Zonas horarias: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
- Python datetime: https://docs.python.org/3/library/datetime.html

## 📝 Notas de mantenimiento

- PyTZ se actualiza frecuentemente con cambios de normativa horaria
- Revisar actualizaciones mínimo 2 veces por año
- Documentar cambios en `CHANGELOG.md` si se actualiza versión

## ✅ Checklist de verificación

- [ ] `pytz` instalado en virtual environment
- [ ] `requirements.txt` contiene `pytz>=2023.3`
- [ ] Importe correctamente en `app.py`
- [ ] Conversiones de timezone funcionales
- [ ] Pruebas en aduanas México, Canadá, USA

---

**Última actualización:** 2026-04-13  
**Responsable:** FreightMetrics Development Team

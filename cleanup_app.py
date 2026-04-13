#!/usr/bin/env python3
"""
Script para limpiar app.py
"""

# Leer el archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontrar y remover líneas dañadas entre comentario y función
cleaned = []
in_monitoreo_section = False
skip_until_def = False

for i, line in enumerate(lines):
    # Detectar inicio de sección Monitoreo
    if '# Esta página ha sido movida a: pages/Monitoreo_Aduanas.py' in line:
        in_monitoreo_section = True
        cleaned.append(line)
        continue
    
    # Si detectamos líneas de código viejo (indentadas, no comentarios, dentro de la sección)
    if in_monitoreo_section and skip_until_def:
        if line.strip().startswith('def page_'):
            cleaned.append(line)
            skip_until_def = False
            in_monitoreo_section = False
        # Skip everything else
        continue
    
    # Si detectamos la línea de "===" que cierra el comentario
    if in_monitoreo_section and line.strip().startswith('# ============================================================'):
        cleaned.append(line)
        # La próxima línea vacía también
        if i+1 < len(lines) and lines[i+1].strip() == '':
            cleaned.append('\n')
        skip_until_def = True
        in_monitoreo_section = False
        # Skip next iteration since we handled the blank line
        continue
    
    if not skip_until_def:
        cleaned.append(line)

# Escribir
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(cleaned)

print("✅ Cleaned app.py")

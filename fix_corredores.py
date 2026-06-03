import re
import os

file_path = "page_modules/_04_Corredores_Logisticos.py"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix for headers and metrics cards in _04_Corredores_Logisticos.py
replacements = [
    (r"st\.markdown\(\"\"\"\s*<div style='background: linear-gradient\(135deg, #003d7a 0%, #0052a3 100%\);.*?</div>\s*\"\"\", unsafe_allow_html=True\)", 
     r"st.markdown(\"\"\"<div style='background: linear-gradient(135deg, #0b1326 0%, #1a2d4a 100%); color: white; padding: 30px 40px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 8px 20px rgba(41, 181, 232, 0.2);'><h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'>🛣️ Corredores Logísticos Estratégicos</h1><p style='color: #F4F7F6; font-size: 1.2rem; font-weight: 500; margin-top: 10px; margin-bottom: 0;'>Análisis de rutas críticas, riesgo operativo y rentabilidad</p></div>\"\"\", unsafe_allow_html=True)"),
    
    (r"st\.markdown\(\"\"\"\s*<div style='background: linear-gradient\(135deg, #003d7a 0%, #0052a3 100%\);.*? Resumen Ejecutivo de Corredores</h3>\s*</div>\s*\"\"\", unsafe_allow_html=True\)", 
     r"st.markdown(\"\"\"<div style='background: linear-gradient(135deg, #0b1326 0%, #1a2d4a 100%); color: white; padding: 15px 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 4px 12px rgba(0, 61, 122, 0.2); border: 1px solid #1a2d4a;'><h3 style='color: #F4F7F6; margin: 0; font-size: 1.3rem; font-weight: 600;'>📊 Resumen Ejecutivo de Corredores</h3></div>\"\"\", unsafe_allow_html=True)"),
    
    (r"st\.markdown\(f\"\"\"\s*<div style='background-color: rgba\(0, 102, 204, 0.15\);.*?Total Corredores.*?\s*</div>\s*\"\"\", unsafe_allow_html=True\)", 
     r"st.markdown(f\"\"\"<div style='background-color: rgba(41, 181, 232, 0.15); border-left: 5px solid #1a2d4a; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0, 102, 204, 0.1); margin: 10px 0;'> <p style='color: #F4F7F6; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Total Corredores</p> <h2 style='color: #FFFFFF; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{total_corredores}</h2> <p style='color: #AAA; font-size: 0.85rem; margin: 0;'>🛣️ Rutas estratégicas</p> </div>\"\"\", unsafe_allow_html=True)"),

    (r"st\.markdown\(f\"\"\"\s*<div style='background-color: rgba\(79, 211, 143, 0.15\);.*?Bajo Riesgo.*?\s*</div>\s*\"\"\", unsafe_allow_html=True\)", 
     r"st.markdown(f\"\"\"<div style='background-color: rgba(79, 211, 143, 0.15); border-left: 5px solid #4FD38F; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(79, 211, 143, 0.1); margin: 10px 0;'> <p style='color: #4FD38F; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Bajo Riesgo</p> <h2 style='color: #FFFFFF; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{corredores_bajo_riesgo}</h2> <p style='color: #AAA; font-size: 0.85rem; margin: 0;'>✅ Rutas seguras</p> </div>\"\"\", unsafe_allow_html=True)"),

    (r"st\.markdown\(f\"\"\"\s*<div style='background-color: rgba\(25, 118, 210, 0.15\);.*?Alta Rentabilidad.*?\s*</div>\s*\"\"\", unsafe_allow_html=True\)", 
     r"st.markdown(f\"\"\"<div style='background-color: rgba(41, 181, 232, 0.15); border-left: 5px solid #131b2e; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(25, 118, 210, 0.1); margin: 10px 0;'> <p style='color: #29B5E8; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Alta Rentabilidad</p> <h2 style='color: #29B5E8; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{corredores_alta_rentabilidad}</h2> <p style='color: #AAA; font-size: 0.85rem; margin: 0;'>💰 Rutas premium</p> </div>\"\"\", unsafe_allow_html=True)"),

    (r"st\.markdown\(f\"\"\"\s*<div style='background-color: rgba\(0, 82, 163, 0.15\);.*?Distancia Promedio.*?\s*</div>\s*\"\"\", unsafe_allow_html=True\)", 
     r"st.markdown(f\"\"\"<div style='background-color: rgba(41, 181, 232, 0.15); border-left: 5px solid #1a2d4a; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0, 82, 163, 0.1); margin: 10px 0;'> <p style='color: #29B5E8; font-size: 0.85rem; font-weight: 600; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;'>Distancia Promedio</p> <h2 style='color: #FFFFFF; font-size: 2.5rem; font-weight: 700; margin: 10px 0 5px 0;'>{distancia_promedio:,.0f}</h2> <p style='color: #AAA; font-size: 0.85rem; margin: 0;'>📏 Kilómetros</p> </div>\"\"\", unsafe_allow_html=True)"),

]

for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

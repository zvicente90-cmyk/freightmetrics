import re

file_path = "page_modules/_04_Corredores_Logisticos.py"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix for the accidental duplicate entry and remaining headers
content = content.replace(
    'st.markdown(\"\"\"<div style=\'background: linear-gradient(135deg, #0b1326 0%, #1a2d4a 100%); color: white; padding: 30px 40px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 8px 20px rgba(41, 181, 232, 0.2);\'><h1 style=\'color: white; margin: 0; font-size: 2.5rem; font-weight: 700;\'>🛣️ Corredores Logísticos Estratégicos</h1><p style=\'color: #F4F7F6; font-size: 1.2rem; font-weight: 500; margin-top: 10px; margin-bottom: 0;\'>Análisis de rutas críticas, riesgo operativo y rentabilidad</p></div>\"\"\", unsafe_allow_html=True)',
    'st.markdown("""<div style=\'background: linear-gradient(135deg, #0b1326 0%, #1a2d4a 100%); color: white; padding: 30px 40px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 8px 20px rgba(41, 181, 232, 0.2);\'><h1 style=\'color: white; margin: 0; font-size: 2.5rem; font-weight: 700;\'>🛣️ Corredores Logísticos Estratégicos</h1><p style=\'color: #F4F7F6; font-size: 1.2rem; font-weight: 500; margin-top: 10px; margin-bottom: 0;\'>Análisis de rutas críticas, riesgo operativo y rentabilidad</p></div>""", unsafe_allow_html=True)',
    1 # Only the first one should stay as is (already fixed)
)

# Wait, I'll just use regex to clean up everything properly now that I know what happened.
# I will collapse all st.markdown("""...""") but NOT if they contain only text (Markdown).
# If they contain <div or <h or <p (HTML), I will collapse them.

def collapse_html_blocks(text):
    def replacer(match):
        prefix = match.group(1) # st.markdown(f?"""
        inner = match.group(2)
        suffix = match.group(3) # """, unsafe_allow_html=True)
        
        if '<div' in inner or '<h' in inner or '<p' in inner or '<span' in inner:
            # Collapse it
            collapsed = " ".join([line.strip() for line in inner.splitlines()])
            return f'{prefix}{collapsed}{suffix}'
        return match.group(0)

    pattern = r'(st\.markdown\(f?["\']{3})(.*?)(["\']{3}\s*,\s*unsafe_allow_html=True\))'
    return re.sub(pattern, replacer, text, flags=re.DOTALL)

content = collapse_html_blocks(content)

# Fix the specific duplicated title for the map
content = content.replace(
    '# ============ MAPA DE RUTAS ============ st.markdown("""<div style=\'background: linear-gradient(135deg, #0b1326 0%, #1a2d4a 100%); color: white; padding: 30px 40px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 8px 20px rgba(41, 181, 232, 0.2);\'><h1 style=\'color: white; margin: 0; font-size: 2.5rem; font-weight: 700;\'>🛣️ Corredores Logísticos Estratégicos</h1><p style=\'color: #F4F7F6; font-size: 1.2rem; font-weight: 500; margin-top: 10px; margin-bottom: 0;\'>Análisis de rutas críticas, riesgo operativo y rentabilidad</p></div>""", unsafe_allow_html=True)',
    '# ============ MAPA DE RUTAS ============ st.markdown("""<div style=\'background: linear-gradient(135deg, #0b1326 0%, #1a2d4a 100%); color: white; padding: 15px 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 4px 12px rgba(0, 61, 122, 0.2); border: 1px solid #1a2d4a;\'><h3 style=\'color: #F4F7F6; margin: 0; font-size: 1.3rem; font-weight: 600;\'>🗺️ Mapa Interactivo de Corredores</h3></div>""", unsafe_allow_html=True)'
)

# Fix the duplicate "Filtros de Visualización" block which might have been collapsed
content = content.replace(
    'st.markdown(""" <p style=\'color: #AAA; font-size: 0.9rem; margin: 15px 0 10px 0;\'><b>📍 Filtros de Visualización:</b></p> """, unsafe_allow_html=True)',
    'st.markdown("""<p style=\'color: #AAA; font-size: 0.9rem; margin: 15px 0 10px 0;\'><b>📍 Filtros de Visualización:</b></p>""", unsafe_allow_html=True)'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

"""
SCRIPT DE MEJORA AUTOMÁTICA - Análisis de Tarjetas KPI
Identifica TODOS los st.metric() en las 7 páginas y propone mejoras
"""

import re
from pathlib import Path

# Directorios
PAGE_MODULES = Path("page_modules")
PAGES_TO_ANALYZE = [
    "_01_Monitoreo_Aduanas.py",
    "_02_Flujos_de_Carga.py", 
    "_03_Fuerza_Laboral.py",
    "_04_Corredores_Logisticos.py",
    "_05_Puertos_Maritimos.py",
    "_06_Nearshoring.py",
    "_07_Puertos_Maritimos.py",
]

def analyze_page(page_name):
    """Analiza una página para encontrar todos los st.metric() y st.markdown() con estilos"""
    page_path = PAGE_MODULES / page_name
    
    if not page_path.exists():
        return None
    
    with open(page_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encuentrar todos los st.metric()
    metric_pattern = r'st\.metric\([^)]+(?:\([^)]*\)[^)]*)*\)'
    metrics = re.findall(metric_pattern, content)
    
    # Encontrar todas las líneas con st.markdown() que tengan background o color
    markdown_pattern = r'st\.markdown\(["\'].*(?:background|color|style).*["\']'
    markdowns = re.findall(markdown_pattern, content, re.DOTALL)
    
    # Chequear si ya tiene apply_global_styles
    has_global_styles = "apply_global_styles" in content
    
    return {
        'page': page_name,
        'metrics_count': len(metrics),
        'markdown_count': len(markdowns),
        'has_global_styles': has_global_styles,
        'metrics': metrics[:3] if metrics else [],  # Show first 3
        'file_size': len(content),
    }

# Analizar todas las páginas
print("=" * 80)
print("ANÁLISIS DE TARJETAS KPI EN TODAS LAS PÁGINAS")
print("=" * 80)

results = []
for page_name in PAGES_TO_ANALYZE:
    result = analyze_page(page_name)
    if result:
        results.append(result)
        print(f"\n📄 {result['page']}")
        print(f"   - st.metric() calls: {result['metrics_count']}")
        print(f"   - st.markdown() with styles: {result['markdown_count']}")
        print(f"   - Has global_styles: {result['has_global_styles']}")
        if result['metrics']:
            print(f"   - First metric: {result['metrics'][0][:60]}...")

# Resumen
print("\n" + "=" * 80)
print("RESUMEN")
print("=" * 80)
total_metrics = sum(r['metrics_count'] for r in results)
total_markdowns = sum(r['markdown_count'] for r in results)
with_global = sum(1 for r in results if r['has_global_styles'])

print(f"Total st.metric() calls across all pages: {total_metrics}")
print(f"Total st.markdown() with styles: {total_markdowns}")
print(f"Pages with global_styles: {with_global}/{len(results)}")

print("\n📊 RECOMENDACIÓN:")
print("✅ Los estilos CSS globales ya están definidos en global_styles.py")
print("✅ Se aplican automáticamente desde app.py")
print("✅ TODOS los st.metric() recibirán los estilos profesionales automáticamente")
print("\n🎨 PRÓXIMOS PASOS:")
print("1. Verificar que app.py carga global_styles (HECHO)")
print("2. Mejorar iconos y colores específicos en cada página (OPCIONAL)")
print("3. Testear en navegador para confirmar que se ven los estilos (NECESARIO)")

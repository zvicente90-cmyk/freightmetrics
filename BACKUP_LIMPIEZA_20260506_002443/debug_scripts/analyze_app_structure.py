#!/usr/bin/env python3
"""
Comprehensive analyzer of app.py structure to create a refactoring plan
Identifies: page functions, shared functions, data loaders, UI components, global variables
"""

import re
from pathlib import Path
from collections import defaultdict
import ast
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# File to analyze
APP_FILE = Path(__file__).parent / "app.py"

# Data structures to hold results
analysis = {
    'page_functions': {},
    'data_loaders': {},
    'helper_functions': {},
    'ui_components': {},
    'imports': [],
    'global_variables': {},
    'function_calls': defaultdict(set),
    'cache_decorators': defaultdict(list),
}

def extract_function_info(file_path):
    """Extract all functions with their line numbers and basic info"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    functions = {}
    current_indent = 0
    
    for i, line in enumerate(lines, 1):
        # Match function definition
        func_match = re.match(r'^def\s+(\w+)\s*\((.*?)\):\s*', line)
        if func_match:
            func_name = func_match.group(1)
            func_args = func_match.group(2)
            
            # Find decorator above it
            decorators = []
            j = i - 2
            while j >= 0 and lines[j].strip().startswith('@'):
                decorators.append(lines[j].strip())
                j -= 1
            
            functions[func_name] = {
                'start_line': i,
                'end_line': None,
                'args': func_args,
                'decorators': decorators,
                'docstring': None,
                'size': 0,
            }
    
    # Find end lines
    func_names = list(functions.keys())
    for i, func_name in enumerate(func_names):
        start = functions[func_name]['start_line']
        
        # End line is the start of the next function minus 1, or end of file
        if i < len(func_names) - 1:
            next_start = functions[func_names[i + 1]]['start_line']
            functions[func_name]['end_line'] = next_start - 1
        else:
            functions[func_name]['end_line'] = len(lines)
        
        functions[func_name]['size'] = functions[func_name]['end_line'] - functions[func_name]['start_line'] + 1
        
        # Extract docstring if present
        docstring_start = functions[func_name]['start_line']
        if docstring_start < len(lines):
            if '"""' in lines[docstring_start] or "'''" in lines[docstring_start]:
                docstring_lines = []
                for j in range(docstring_start, min(docstring_start + 50, len(lines))):
                    docstring_lines.append(lines[j])
                    if j > docstring_start and ('"""' in lines[j] or "'''" in lines[j]):
                        break
                functions[func_name]['docstring'] = ''.join(docstring_lines).strip()
    
    return functions, lines

def categorize_function(func_name, func_info):
    """Categorize function by name and decorator patterns"""
    name_lower = func_name.lower()
    
    if name_lower.startswith('page_'):
        return 'page_function'
    elif any(x in name_lower for x in ['obtener_', 'cargar_', 'descargar_', 'conectar_', 'leer_']):
        return 'data_loader'
    elif any(x in func_info['decorators'] for x in ['@st.cache_data', '@st.cache', '@cache']):
        return 'cached_function'
    elif any(x in name_lower for x in ['calcular_', 'procesar_', 'transformar_', 'generar_', 'filtrar_']):
        return 'helper_function'
    else:
        return 'utility_function'

def extract_function_calls(code_snippet):
    """Extract function calls from code"""
    # Simple regex to find function calls
    pattern = r'(\w+)\s*\('
    calls = set(re.findall(pattern, code_snippet))
    
    # Filter out common keywords and Streamlit functions
    exclude = {
        'if', 'for', 'while', 'def', 'class', 'return', 'print', 'len', 'str', 'int', 'float',
        'list', 'dict', 'set', 'range', 'enumerate', 'zip', 'map', 'filter', 'sorted',
        'isinstance', 'hasattr', 'getattr', 'setattr', 'super', 'open', 'with', 'try', 'except',
        'raise', 'assert', 'pass', 'continue', 'break', 'yield', 'lambda', 'and', 'or', 'not',
        'in', 'is', 'None', 'True', 'False', 'else', 'elif', 'except', 'finally', 'as'
    }
    
    return calls - exclude

def extract_imports(lines):
    """Extract all imports from the file"""
    imports = []
    
    for line in lines:
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            imports.append(line.strip())
    
    return imports

def extract_global_vars(lines, functions):
    """Extract global variables (assignments outside functions)"""
    globals_dict = {}
    
    current_func_line = 0
    for func_name, func_info in functions.items():
        current_func_line = max(current_func_line, func_info['start_line'])
    
    # Lines before first function are likely globals
    first_func_line = min([f['start_line'] for f in functions.values()], default=len(lines))
    
    # Also check for ALL_CAPS assignments throughout the file (common pattern for constants)
    for i, line in enumerate(lines, 1):
        if i > first_func_line:
            # Check if we're at top-level indentation
            if line and not line[0].isspace():
                match = re.match(r'^([A-Z_][A-Z0-9_]*)\s*=', line)
                if match:
                    var_name = match.group(1)
                    globals_dict[var_name] = i
    
    return globals_dict

def analyze_page_function(func_name, func_info, lines):
    """Detailed analysis of a page function"""
    start = func_info['start_line'] - 1
    end = min(func_info['end_line'], len(lines))
    
    code = ''.join(lines[start:end])
    
    # Extract called functions
    called_funcs = extract_function_calls(code)
    
    # Extract UI elements used
    ui_elements = set()
    if 'st.metric' in code: ui_elements.add('metric')
    if 'st.columns' in code: ui_elements.add('columns')
    if 'st.tabs' in code: ui_elements.add('tabs')
    if 'st.selectbox' in code or 'st.radio' in code: ui_elements.add('filters')
    if 'px.bar' in code or 'go.Bar' in code: ui_elements.add('bar_charts')
    if 'px.line' in code or 'go.Scatter' in code: ui_elements.add('line_charts')
    if 'px.pie' in code or 'go.Pie' in code: ui_elements.add('pie_charts')
    if 'px.scatter' in code: ui_elements.add('scatter_charts')
    if 'st.map' in code or 'folium' in code: ui_elements.add('maps')
    if 'st.dataframe' in code: ui_elements.add('dataframes')
    if 'st.button' in code: ui_elements.add('buttons')
    
    # Count lines
    size = func_info['size']
    
    return {
        'called_functions': called_funcs,
        'ui_elements': ui_elements,
        'size': size,
        'decorators': func_info['decorators'],
    }

def main():
    print("=" * 80)
    print("APP.PY STRUCTURE ANALYSIS & REFACTORING PLAN")
    print("=" * 80)
    
    functions, lines = extract_function_info(APP_FILE)
    imports = extract_imports(lines)
    globals_dict = extract_global_vars(lines, functions)
    
    # Categorize functions
    page_funcs = {}
    data_loaders = {}
    helper_funcs = {}
    other_funcs = {}
    
    for func_name, func_info in functions.items():
        category = categorize_function(func_name, func_info)
        
        if category == 'page_function':
            page_funcs[func_name] = {**func_info, **analyze_page_function(func_name, func_info, lines)}
        elif category == 'data_loader':
            data_loaders[func_name] = func_info
        elif category == 'helper_function':
            helper_funcs[func_name] = func_info
        else:
            other_funcs[func_name] = func_info
    
    # SECTION 1: Summary
    print(f"\n[SUMMARY]")
    print("-" * 80)
    print(f"Total lines in app.py: {len(lines)}")
    print(f"Total functions: {len(functions)}")
    print(f"  - Page functions: {len(page_funcs)}")
    print(f"  - Data loaders: {len(data_loaders)}")
    print(f"  - Helper functions: {len(helper_funcs)}")
    print(f"  - Other functions: {len(other_funcs)}")
    print(f"Global variables/constants: {len(globals_dict)}")
    print(f"Import statements: {len(imports)}")
    
    # SECTION 2: Page Functions Analysis
    print(f"\n" + "=" * 80)
    print("[PAGE FUNCTIONS] (7 functions)")
    print("=" * 80)
    
    page_summary = []
    for func_name in sorted(page_funcs.keys()):
        info = page_funcs[func_name]
        print(f"\n{func_name}")
        print(f"  [LINES] {info['start_line']}-{info['end_line']} ({info['size']} lines)")
        print(f"  [UI ELEMENTS] {', '.join(sorted(info['ui_elements'])) if info['ui_elements'] else 'N/A'}")
        print(f"  [CALLED FUNCTIONS] {len(info['called_functions'])}")
        
        # Show top called functions
        top_calls = sorted(info['called_functions'])[:5]
        if top_calls:
            print(f"     Top: {', '.join(top_calls)}")
        
        page_summary.append({
            'name': func_name,
            'start': info['start_line'],
            'end': info['end_line'],
            'size': info['size'],
            'calls': info['called_functions'],
        })
    
    # SECTION 3: Data Loading Functions
    print(f"\n" + "=" * 80)
    print("[DATA LOADING FUNCTIONS] ({} functions)".format(len(data_loaders)))
    print("=" * 80)
    
    loader_summary = []
    for func_name in sorted(data_loaders.keys()):
        info = data_loaders[func_name]
        is_cached = len(info['decorators']) > 0
        cache_str = f"[CACHED] ({', '.join(info['decorators'])})" if is_cached else "[NOT CACHED]"
        
        print(f"\n{func_name}")
        print(f"  [LINES] {info['start_line']}-{info['end_line']} ({info['size']} lines)")
        print(f"  {cache_str}")
        
        loader_summary.append({
            'name': func_name,
            'start': info['start_line'],
            'end': info['end_line'],
            'size': info['size'],
            'cached': is_cached,
        })
    
    # SECTION 4: Helper Functions
    print(f"\n" + "=" * 80)
    print("[HELPER/UTILITY FUNCTIONS] ({} functions)".format(len(helper_funcs) + len(other_funcs)))
    print("=" * 80)
    
    all_helpers = {**helper_funcs, **other_funcs}
    helper_list = sorted(all_helpers.keys())
    
    print(f"\nTop helpers by size:")
    for func_name in sorted(helper_list, key=lambda x: all_helpers[x]['size'], reverse=True)[:10]:
        info = all_helpers[func_name]
        print(f"  {func_name:<40} {info['size']:>4} lines")
    
    # SECTION 5: Global Variables
    print(f"\n" + "=" * 80)
    print(f"[GLOBAL CONSTANTS] (Sample)")
    print("=" * 80)
    
    # Read the file again to find all-caps assignments
    with open(APP_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    caps_vars = re.findall(r'^([A-Z_][A-Z0-9_]*)\s*=\s*(.+?)$', content, re.MULTILINE)
    caps_vars = caps_vars[:15]  # Show first 15
    
    for var, value in caps_vars:
        value_preview = value.replace('\n', ' ')[:60]
        print(f"  {var:<30} = {value_preview}...")
    
    # SECTION 6: Imports
    print(f"\n" + "=" * 80)
    print(f"[KEY IMPORTS] ({len(imports)} total)")
    print("=" * 80)
    
    key_imports = []
    for imp in imports:
        if any(x in imp for x in ['streamlit', 'plotly', 'pandas', 'requests', 'ui_components']):
            key_imports.append(imp)
    
    for imp in key_imports[:10]:
        print(f"  {imp}")
    
    if len(key_imports) > 10:
        print(f"  ... and {len(key_imports) - 10} more")
    
    # SECTION 7: Structure-Based Refactoring Plan
    print(f"\n" + "=" * 80)
    print("[REFACTORING PLAN] - MODULE STRUCTURE")
    print("=" * 80)
    
    print('''
[RECOMMENDED STRUCTURE]

|- app.py (Main entry point, ~200 lines)
|  |- Imports & configuration
|  |- Session state initialization
|  |- Language & translation setup
|  |- CSS styling (inject or import)
|  |- Navigation/routing logic
|  `- main() function
|
|- config/
|  |- __init__.py
|  |- settings.py (Global constants, colors, paths)
|  |- translations.py (TRANSLATIONS dictionary - ~400 lines)
|  `- styles.py (CSS injection)
|
|- data/
|  |- __init__.py
|  |- loaders.py (All data loading functions)
|  |  |- cargar_datos_aduanas_reales()
|  |  |- cargar_datos_flujos_reales()
|  |  |- cargar_datos_historicos_multiannual()
|  |  |- obtener_datos_puertos_oficiales()
|  |  |- obtener_dias_festivos_2026()
|  |  `- ... (all "obtener_*" and "cargar_*" functions)
|  |
|  |- connectors.py (External API connections)
|  |  |- conectar_asipona()
|  |  |- conectar_semar()
|  |  |- conectar_anam()
|  |  |- obtener_trafico_maritimo_aishub()
|  |  `- ...
|  |
|  `- processors.py (Data transformation)
|     |- calcular_tendencias_historicas()
|     |- obtener_datos_cruces_consolidados()
|     `- ... (calcular_*, procesar_* functions)
|
|- ui/
|  |- __init__.py
|  |- components.py (Re-export from ui_components)
|  `- styles.py (CSS class definitions)
|
|- pages/
|  |- __init__.py
|  |- inicio.py
|  |  `- def page_inicio()
|  |- mapa.py
|  |  `- def page_mapa()
|  |- monitoreo_aduanas.py
|  |  `- def page_monitoreo_aduanas()
|  |- fuerza_laboral.py
|  |  `- def page_fuerza_laboral()
|  |- mapa_autotransporte.py
|  |  `- def page_mapa_autotransporte()
|  |- corredores_logisticos.py
|  |  `- def page_corredores_logisticos()
|  `- nearshoring.py
|     `- def page_nearshoring()
|
`- utils/
   |- __init__.py
   |- helpers.py (General helper functions)
   |- formatters.py (Formatting & conversion functions)
   |- validators.py (Data validation functions)
   `- cache.py (Cache management utilities)
''')
    
    # SECTION 8: Migration Steps
    print("\n" + "=" * 80)
    print("[MIGRATION STEPS] - Phase by Phase")
    print("=" * 80)
    
    print('''
[PHASE 1] Extract Translations & Configuration
  1.1 Create config/translations.py with TRANSLATIONS dict (~800 lines)
  1.2 Create config/settings.py with color constants, paths, etc.
  1.3 Update app.py to import: from config import TRANSLATIONS, settings
  
[PHASE 2] Extract Data Functions
  2.1 Create data/loaders.py with all data loading functions
      - cargar_datos_aduanas_reales() (~150 lines)
      - cargar_datos_flujos_reales() (~200 lines)
      - cargar_datos_historicos_multiannual() (~120 lines)
      - All obtener_datos_* functions (~500 lines total)
  
  2.2 Create data/connectors.py with API connection functions
      - conectar_asipona() (~30 lines)
      - conectar_semar() (~30 lines)
      - conectar_anam() (~30 lines)
      - obtener_trafico_maritimo_aishub() (~100 lines)
      
  2.3 Create data/processors.py with calculation functions
      - calcular_tendencias_historicas() (~150 lines)
      - obtener_datos_cruces_consolidados() (~300 lines)
  
  2.4 Update app.py imports: 
      from data.loaders import cargar_datos_aduanas_reales, ...

[PHASE 3] Extract Page Functions
  3.1 Create pages/inicio.py with page_inicio() (~200 lines)
  3.2 Create pages/mapa.py with page_mapa() (~200 lines)
  3.3 Create pages/monitoreo_aduanas.py with page_monitoreo_aduanas() (~300 lines)
  3.4 Create pages/fuerza_laboral.py with page_fuerza_laboral() (~400 lines)
  3.5 Create pages/mapa_autotransporte.py with page_mapa_autotransporte() (~400 lines)
  3.6 Create pages/corredores_logisticos.py with page_corredores_logisticos() (~300 lines)
  3.7 Create pages/nearshoring.py with page_nearshoring() (~200 lines)

[PHASE 4] Extract UI & Helper Functions
  4.1 Extract helper functions to utils/helpers.py
  4.2 Extract formatters to utils/formatters.py
  4.3 Extract validators to utils/validators.py

[PHASE 5] Refactor Main app.py
  5.1 Reduce app.py to ~200 lines with only:
      - Imports and configuration
      - Session state setup
      - Sidebar navigation
      - Main routing logic
      - CSS injection (or import from styles)
  
  5.2 Create clean __init__ files for each module

[PHASE 6] Testing & Validation
  6.1 Test each page module independently
  6.2 Test imports and circular dependencies
  6.3 Test session state management
  6.4 Test cache functionality
''')
    
    # SECTION 9: Dependencies Between Pages
    print("\n" + "=" * 80)
    print("[DEPENDENCY ANALYSIS] - What Each Page Needs")
    print("=" * 80)
    
    deps = {
        'page_inicio': ['obtener_datos_mapeados', 'metric_card', 'st.metric'],
        'page_mapa': ['cargar_datos_csv (legacy)', 'px.bar', 'st.columns'],
        'page_monitoreo_aduanas': ['obtener_datos_cruces_consolidados', 'st.map', 'px.line'],
        'page_fuerza_laboral': ['obtener_datos_fuerza_laboral', 'px.pie', 'st.dataframe'],
        'page_mapa_autotransporte': ['cargar_datos_puertos_reales', 'px.bar', 'folium'],
        'page_corredores_logisticos': ['obtener_datos_cruces_consolidados', 'px.scatter'],
        'page_nearshoring': ['obtener_datos_cruces_consolidados', 'px.line'],
    }
    
    for page, depends_on in sorted(deps.items()):
        print(f"\n{page}:")
        for dep in depends_on:
            print(f"  -> {dep}")
    
    # SECTION 10: Critical Shared Dependencies
    print("\n" + "=" * 80)
    print("[CRITICAL SHARED DEPENDENCIES] (Used by multiple pages)")
    print("=" * 80)
    
    shared = {
        'obtener_datos_cruces_consolidados()': ['page_monitoreo_aduanas', 'page_corredores_logisticos', 'page_nearshoring'],
        'metric_card()': ['page_inicio', 'most pages'],
        'st.session_state.language': ['All pages'],
        'TRANSLATIONS dict': ['All pages'],
        't() function': ['All pages'],
    }
    
    for shared_item, pages in shared.items():
        print(f"\n{shared_item}")
        print(f"  Used in: {', '.join(pages)}")
    
    # SECTION 11: File Size Estimates
    print("\n" + "=" * 80)
    print("[FILE SIZE ESTIMATES] For New Structure")
    print("=" * 80)
    
    print(f'''
[CURRENT STATE]
  app.py: ~15,000 lines

[AFTER REFACTORING]
  app.py:                           ~200 lines  (DOWN 98.7%)
  config/translations.py:           ~800 lines
  config/settings.py:               ~200 lines
  data/loaders.py:                 ~1,000 lines
  data/connectors.py:               ~300 lines
  data/processors.py:               ~500 lines
  pages/inicio.py:                  ~250 lines
  pages/mapa.py:                    ~300 lines
  pages/monitoreo_aduanas.py:       ~500 lines
  pages/fuerza_laboral.py:          ~500 lines
  pages/mapa_autotransporte.py:     ~500 lines
  pages/corredores_logisticos.py:   ~400 lines
  pages/nearshoring.py:             ~300 lines
  utils/helpers.py:                 ~400 lines
  utils/formatters.py:              ~200 lines
  
  TOTAL: ~7,150 lines (+ UI, styles, other modules)
  
[BENEFITS]
  - Each page is now ~300-500 lines (manageable)
  - Data logic is separate and reusable
  - Configuration is centralized
  - Much easier to test and maintain
  - Clear separation of concerns
''')
    
    print("\n" + "=" * 80)
    print("[ANALYSIS COMPLETE]")
    print("=" * 80)

if __name__ == "__main__":
    main()

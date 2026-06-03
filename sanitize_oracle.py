import re

def collapse_html_blocks(text):
    def replacer(match):
        prefix = match.group(1) # st.markdown(f?"""
        inner = match.group(2)
        suffix = match.group(3) # """, unsafe_allow_html=True)
        
        # Check if it looks like HTML/CSS
        if '<div' in inner or '<h' in inner or '<p' in inner or '<span' in inner or 'background:' in inner or 'padding:' in inner:
            # Collapse it: remove newlines and leading/trailing whitespace
            # Replace multiple spaces/newlines with a single space
            collapsed = re.sub(r'\s+', ' ', inner).strip()
            return f'{prefix}{collapsed}{suffix}'
        return match.group(0)

    # Regex to find st.markdown(f?"""...""", unsafe_allow_html=True)
    pattern = r'(st\.markdown\(f?["\']{3})(.*?)(["\']{3}\s*,\s*unsafe_allow_html=True\))'
    return re.sub(pattern, replacer, text, flags=re.DOTALL)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = collapse_html_blocks(content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    process_file("pages/09_Oracle_Rate.py")
    process_file("page_modules/_04_Corredores_Logisticos.py")

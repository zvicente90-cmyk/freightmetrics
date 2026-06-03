import re
import sys

def sanitize_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find st.markdown("""...""", unsafe_allow_html=True)
    # and collapse the string inside the triple quotes.
    def collapse_html(match):
        indent = match.group(1)
        prefix = match.group(2) # e.g. 'st.markdown('
        opening = match.group(3) # '"""' or "'''"
        inner_content = match.group(4)
        closing = match.group(5) # '"""' or "'''"
        suffix = match.group(6) # ', unsafe_allow_html=True)'
        
        # Collapse newlines and extra spaces inside the HTML string
        collapsed = re.sub(r'\s*\n\s*', ' ', inner_content).strip()
        # Ensure we don't accidentally escape backslashes if they were planned
        # but here we just want a single line.
        return f'{indent}{prefix}{opening}{collapsed}{closing}{suffix}'

    # This regex is a bit complex to handle potential f-strings too.
    # It looks for: (indent)(st.markdown\(f?)(["']{3})(.*?)(["']{3})(\s*,?\s*unsafe_allow_html=True\s*\))
    pattern = r'^(\s*)(st\.markdown\(f?)(["\']{3})(.*?)(["\']{3})(\s*,?\s*unsafe_allow_html=True\s*\))'
    
    new_content = re.sub(pattern, collapse_html, content, flags=re.DOTALL | re.MULTILINE)
    
    # Also clean up multiple empty lines while we're at it
    new_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', new_content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    sanitize_file(sys.argv[1])

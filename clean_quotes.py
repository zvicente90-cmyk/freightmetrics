import os

file_path = "page_modules/_04_Corredores_Logisticos.py"
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Replace \"\"\" with """ (literal backslash followed by three quotes)
    new_line = line.replace('\\\"\"\"', '\"\"\"')
    new_lines.append(new_line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

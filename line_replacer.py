import sys

def replace_lines(file_path, start_line, end_line, new_text):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Lines are 1-indexed for the user, 0-indexed for python
    lines[start_line-1:end_line] = [new_text + '\n']
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == "__main__":
    file_path = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    # Read new text from stdin to handle multi-line easily
    new_text = sys.stdin.read()
    replace_lines(file_path, start, end, new_text)

import re

unidentified_lines = []

def parse_markdown_line(line):
    line = line.rstrip()
    if line.startswith('# '):
        return {'type': 'heading1', 'content': line[2:].strip(), 'raw': line}
    elif line.startswith('## '):
        return {'type': 'heading2', 'content': line[3:].strip(), 'raw': line}
    elif line.startswith('### '):
        return {'type': 'heading3', 'content': line[4:].strip(), 'raw': line}
    elif line.startswith('#### '):
        return {'type': 'heading4', 'content': line[5:].strip(), 'raw': line}
    elif line.startswith('##### '):
        return {'type': 'heading5', 'content': line[6:].strip(), 'raw': line}
    elif line.startswith('###### '):
        return {'type': 'heading6', 'content': line[7:].strip(), 'raw': line}
    elif re.match(r'^\s*-\s+', line):
        return {'type': 'list_item', 'content': re.sub(r'^\s*-\s+', '', line).strip(), 'raw': line}
    elif re.match(r'^\s*\d+\.\s+', line):
        return {'type': 'ordered_list_item', 'content': re.sub(r'^\s*\d+\.\s+', '', line).strip(), 'raw': line}
    elif re.match(r'^!\[.*\]\((.*)\)$', line):
        match = re.match(r'^!\[.*\]\((.*)\)$', line)
        return {'type': 'image', 'content': match.group(1), 'raw': line}
    elif re.match(r'^\[.*\]\((.*)\)$', line):
        match = re.match(r'^\[.*\]\((.*)\)$', line)
        return {'type': 'link', 'content': match.group(1), 'raw': line}
    elif re.match(r'^---+$', line):
        return {'type': 'horizontal_line', 'content': '', 'raw': line}
    elif re.match(r'^\*\*\*+$', line):
        return {'type': 'horizontal_line_asterisks', 'content': '', 'raw': line}
    elif line == '':
        return {'type': 'blank_line', 'content': '', 'raw': line}
    else:
        unidentified_lines.append(line)
        return {'type': 'paragraph', 'content': line, 'raw': line}

def parse_markdown(markdown):
    lines = markdown.splitlines()
    parsed_lines = []
    skip_yaml_frontmatter = False

    for line in lines:
        if line == "---" and not skip_yaml_frontmatter:
            skip_yaml_frontmatter = True
            continue
        elif line == "---" and skip_yaml_frontmatter:
            skip_yaml_frontmatter = False
            continue
        
        if not skip_yaml_frontmatter:
            parsed_lines.append(parse_markdown_line(line))

    return parsed_lines

def parse_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    return parse_markdown(content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m markdown_parser <markdown_file_path>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    parsed_file = parse_markdown_file(filepath)
    if unidentified_lines:
        print("Unidentified lines:")
        for line in unidentified_lines:
            print(line)
    sys.exit(parsed_file)

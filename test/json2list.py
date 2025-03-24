import json

def parse_tokens(tokens, indent=0):
    markdown = ""
    prefix = "  " * indent + "- "
    for token in tokens:
        content = token.get('raw') or token.get('attrs', {}).get('url', '')
        text = f"{token['type']}: {content}" if content else token['type']
        markdown += f"{prefix}{text}\n"
        if 'children' in token:
            markdown += parse_tokens(token['children'], indent + 1)
    return markdown

def convert_json_to_markdown(json_file, md_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    markdown_content = parse_tokens(data.get('tokens', []))
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    print(f"Markdown file saved: {md_file}")

# 실행 예제
convert_json_to_markdown("flattened.json", "list.md")
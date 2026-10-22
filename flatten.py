import os
import sys
import re
import urllib.parse

def read_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

class FlattenCycleError(ValueError):
    """Raised when embedded Markdown files form a recursive cycle."""


def flatten_markdown(
    filepath,
    base_path=None,
    export_base_path=None,
    is_root=True,
    diagnostics=None,
    _stack=None,
):
    filepath = os.path.abspath(filepath)
    base_path = os.path.abspath(base_path or os.path.dirname(filepath))
    export_base_path = os.path.abspath(export_base_path or base_path)
    stack = list(_stack or [])
    canonical_path = os.path.normcase(os.path.realpath(filepath))
    if canonical_path in stack:
        chain = stack[stack.index(canonical_path):] + [canonical_path]
        raise FlattenCycleError(
            "Circular Markdown embed: " + " -> ".join(chain)
        )
    stack.append(canonical_path)

    content = read_markdown_file(filepath)
    lines = content.splitlines()
    flattened_content = []
    
    # YAML frontmatter 처리 - 하위 마크다운에서만 무시
    in_frontmatter = False
    for i, line in enumerate(lines):
        # frontmatter 시작 확인
        if i == 0 and line.strip() == '---':
            in_frontmatter = True
            if is_root:  # 최상위 마크다운인 경우 frontmatter 포함
                flattened_content.append(line)
            continue
        # frontmatter 종료 확인
        if in_frontmatter and line.strip() == '---':
            in_frontmatter = False
            if is_root:  # 최상위 마크다운인 경우 frontmatter 포함
                flattened_content.append(line)
            continue
        # frontmatter 내부 처리
        if in_frontmatter:
            if is_root:  # 최상위 마크다운인 경우 frontmatter 포함
                flattened_content.append(line)
            continue

        # Check if the line is an embedded markdown reference
        embed_match = re.match(r'^!\[.*\]\((.*\.md)\)$', line)
        if embed_match:
            embedded_path = embed_match.group(1)
            # Decode URL-encoded characters (e.g., %20 -> space)
            embedded_path = urllib.parse.unquote(embedded_path)
            embedded_full_path = os.path.abspath(os.path.join(base_path, embedded_path))
            if os.path.isfile(embedded_full_path):
                # 하위 마크다운 처리 시 is_root=False로 설정
                embedded_content = flatten_markdown(embedded_full_path, 
                                                 os.path.dirname(embedded_full_path), 
                                                 export_base_path,
                                                 is_root=False,
                                                 diagnostics=diagnostics,
                                                 _stack=stack)
                flattened_content.append(embedded_content)
            else:
                if diagnostics is not None:
                    diagnostics.append(
                        f"{filepath}:{i + 1}: Embedded Markdown not found: {embedded_path}"
                    )
                flattened_content.append(f"<!-- Embedded file not found: {embedded_path} -->")
        else:
            # Check if the line is an image reference
            image_match = re.match(r'^!\[.*\]\((.*\.(png|jpg|jpeg|gif|svg|webp))\)$', line)
            if image_match:
                image_path = image_match.group(1)
                parsed_image = urllib.parse.urlsplit(image_path)
                if parsed_image.scheme.lower() in ("http", "https"):
                    flattened_content.append(line)
                    continue
                # Decode URL-encoded characters (e.g., %20 -> space)
                image_path = urllib.parse.unquote(image_path)
                image_full_path = os.path.abspath(
                    image_path if os.path.isabs(image_path)
                    else os.path.join(base_path, image_path)
                )
                if diagnostics is not None and not os.path.isfile(image_full_path):
                    diagnostics.append(
                        f"{filepath}:{i + 1}: Image not found: {image_path}"
                    )
                # Create a new relative path from the export base path
                new_relative_path = os.path.relpath(image_full_path, export_base_path)
                # Keep URL paths portable while encoding filename characters.
                new_relative_path = urllib.parse.quote(
                    new_relative_path.replace('\\', '/'), safe='/@:+-._~'
                )
                # Reconstruct the line with the updated image path
                updated_line = re.sub(r'\(.*\.(png|jpg|jpeg|gif|svg|webp)\)', lambda m: f'({new_relative_path})', line)
                flattened_content.append(updated_line)
            else:
                flattened_content.append(line)

    return '\n'.join(flattened_content)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m markdown_flatten_embed <markdown_file_path> [--export]")
        sys.exit(1)

    mother_filepath = sys.argv[1]
    mother_base_path = os.path.dirname(mother_filepath)

    # Flatten the markdown file
    flattened_markdown = flatten_markdown(mother_filepath, mother_base_path, is_root=True)

    # Check if export flag is provided
    if len(sys.argv) > 2 and sys.argv[2] == "--export":
        # Write the final flattened markdown content to a new file
        flattened_filepath = os.path.join(mother_base_path, f"{os.path.splitext(os.path.basename(mother_filepath))[0]}_flattened.md")
        with open(flattened_filepath, 'w', encoding='utf-8') as flattened_file:
            flattened_file.write(flattened_markdown)
    else:
        # By default, return the flattened markdown as a string
        print(flattened_markdown)

import os
import re
import platform
import sys

def convert_image_paths_to_absolute(markdown_content, base_path):
    lines = markdown_content.splitlines()
    updated_lines = []

    for line in lines:
        # Check if the line is an image reference
        match = re.match(r'^!\[.*\]\((.*\.(png|jpg|jpeg|gif|bmp|svg))\)$', line)
        if match:
            relative_path = match.group(1)
            absolute_path = os.path.abspath(os.path.join(base_path, relative_path))
            # Normalize the path for different OS
            if platform.system() == "Windows":
                absolute_path = absolute_path.replace('\\', '/')
            updated_line = line.replace(relative_path, absolute_path)
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)

    return '\n'.join(updated_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m markdown_absolute_paths <markdown_file_path> [--export]")
        sys.exit(1)

    markdown_filepath = sys.argv[1]
    base_path = os.path.dirname(os.path.abspath(markdown_filepath))

    # Read the markdown file
    with open(markdown_filepath, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    # Convert image paths to absolute paths
    updated_markdown = convert_image_paths_to_absolute(markdown_content, base_path)

    # Check if export flag is provided
    if len(sys.argv) > 2 and sys.argv[2] == "--export":
        # Write the updated markdown content to a new file
        abs_filepath = os.path.join(base_path, f"{os.path.splitext(os.path.basename(markdown_filepath))[0]}_abs.md")
        with open(abs_filepath, 'w', encoding='utf-8') as abs_file:
            abs_file.write(updated_markdown)
    else:
        # By default, return the updated markdown as a string
        sys.stdout.write(updated_markdown)

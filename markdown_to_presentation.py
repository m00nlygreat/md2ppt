import os
import sys
import re

def convert_markdown_to_presentation(markdown_content):
    # Read the lines from the markdown content
    r = markdown_content.splitlines(keepends=True)
    processed = []

    # Compile regex patterns
    head_level = "##"
    p = re.compile(f'^{head_level} .+\n$')
    k = re.compile("^[#]{1,2} .+\n$")

    # Process lines to handle separators and headings
    for i, line in enumerate(r):
        if line == "---\n":
            m = p.match(r[i + 2]) if i + 2 < len(r) else None
            if not m:
                processed.append(line)
                for j in range(i, 0, -1):
                    if p.match(r[j]):
                        processed.append('\n')
                        processed.append(r[j])
                        break
            else:
                processed.append(line)
        else:
            processed.append(line)

    column_separated = []
    tail = -1

    # Process lines to add columns for content separated by "***"
    for i, line in enumerate(processed):
        if line == "***\n":
            before = []
            for j in range(i, 0, -1):
                if p.match(processed[j]) or processed[j] == "---\n":
                    break
                else:
                    if processed[j] != "***\n":
                        before.insert(0, processed[j])
                    if j != i:
                        column_separated.pop()
            column_separated.append("\n")
            column_separated.append("::: {.columns}\n")
            column_separated.append("::: {.column}\n")

            for line in before:
                column_separated.append(line)

            column_separated.append(":::\n")
            column_separated.append("::: {.column}\n")
            tail = 0
            for j in range(i, len(processed)):
                if k.match(processed[j]) or processed[j] == "---\n":
                    tail -= 2
                    break
                else:
                    tail += 1
        else:
            column_separated.append(line)
            if tail == 0:
                column_separated.append(":::\n")
                column_separated.append(":::\n")
                column_separated.append("\n")
            tail -= 1

    # Join the processed lines into final markdown content
    return ''.join(column_separated)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python markdown_to_presentation.py <markdown_file_path> [output_path]")
        sys.exit(1)

    # Get file paths
    markdown_filepath = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()

    # Read the original markdown file
    with open(markdown_filepath, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Convert markdown to presentation format
    final_markdown = convert_markdown_to_presentation(markdown_content)

    # Write the final markdown to a new file
    output_filepath = os.path.join(output_path, f"_{os.path.basename(markdown_filepath)}")
    with open(output_filepath, 'w', encoding='utf-8') as output_file:
        output_file.write(final_markdown)

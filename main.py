import os
import sys
from markdown_flatten_embed import flatten_markdown
from markdown_absolute_paths import convert_image_paths_to_absolute
from markdown_to_presentation import convert_markdown_to_presentation

def process_markdown(markdown_filepath):
    # Step 1: Flatten the markdown
    base_path = os.path.dirname(markdown_filepath)
    flattened_markdown = flatten_markdown(markdown_filepath, base_path)

    # Step 2: Convert image paths to absolute paths
    absolute_path_markdown = convert_image_paths_to_absolute(flattened_markdown, base_path)

    # Step 3: Convert column separators into presentation format
    presentation_markdown = convert_markdown_to_presentation(absolute_path_markdown)

    return presentation_markdown

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <markdown_file_path> [--export]")
        sys.exit(1)

    markdown_filepath = sys.argv[1]

    # Process the markdown file
    final_markdown = process_markdown(markdown_filepath)

    # Check if export flag is provided
    if len(sys.argv) > 2 and sys.argv[2] == "--export":
        # Write the final markdown content to a new file
        output_filepath = f"_{os.path.splitext(os.path.basename(markdown_filepath))[0]}.md"
        with open(output_filepath, 'w', encoding='utf-8') as output_file:
            output_file.write(final_markdown)
    else:
        # By default, return the final markdown as a string
        sys.stdout.write(final_markdown)
#!/usr/bin/env python3
"""
Markdown to JSON Parser

This script converts Markdown content to a structured JSON representation using mistune.
It handles YAML frontmatter and special Markdown elements like horizontal rules with
different marker types (---, ***, ___).

Usage:
    # Parse a Markdown file and print the JSON to stdout
    python markdown_to_json.py --file path/to/markdown.md
    
    # Parse a Markdown file and export to a JSON file
    python markdown_to_json.py --file path/to/markdown.md --export output.json
    
    # Parse a Markdown string and print the JSON to stdout
    python markdown_to_json.py --string "# Heading\n\nParagraph text"
    
Features:
    - Extracts and preserves YAML frontmatter
    - Distinguishes between different horizontal rule types:
      * "---" (dash): Used to create new slides
      * "***" (asterisk): Used to create column separators
      * "___" (underscore): Alternative horizontal rule
    - Maintains the original Markdown structure in JSON format
    - Compatible with json_to_slides.py for presentation creation

Requirements:
    - mistune: Markdown parser
    - pyyaml: YAML parser for frontmatter

Output Format:
    The output JSON has this structure:
    {
        "content": [ ... array of parsed markdown nodes ... ],
        "frontmatter": { ... YAML frontmatter if present ... }
    }
"""
import argparse
import json
import mistune
import sys
import re
import yaml
from pathlib import Path
from typing import Dict, Union, List, Any, Tuple


class CustomMarkdownParser(mistune.BlockParser):
    """
    Custom Markdown parser that distinguishes between different types of horizontal rules.
    
    This parser extends mistune's BlockParser to detect horizontal rule marker types:
    - "---" (dash): Typically used to create new slides
    - "***" (asterisk): Typically used to create column separators
    - "___" (underscore): Alternative horizontal rule
    
    The marker type is added to the node as 'marker_type' which downstream
    processors can use to make layout decisions.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store the original markdown text for reference
        self.original_text = ""
    
    def parse_horizontal_rule(self, m, state):
        """
        Override the horizontal rule parser to include the original marker type.
        
        Args:
            m: The regex match object
            state: The parser state
            
        Returns:
            Dict with type and marker_type
        """
        # Get the original text that matched the horizontal rule
        original_marker = m.group(0).strip()
        
        # Determine the marker type (-, *, or _)
        if '-' in original_marker:
            marker_type = 'dash'  # For ---
        elif '*' in original_marker:
            marker_type = 'asterisk'  # For ***
        elif '_' in original_marker:
            marker_type = 'underscore'  # For ___
        else:
            marker_type = 'unknown'
            
        return {'type': 'thematic_break', 'marker_type': marker_type}


def extract_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """
    Extract YAML frontmatter from markdown content if it exists.
    
    Args:
        content: Markdown content with possible frontmatter
        
    Returns:
        Tuple of (frontmatter dict, markdown content without frontmatter)
    """
    # Regex pattern for frontmatter (starts and ends with ---)
    pattern = r'^\s*---\s*\n(.*?)\n\s*---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        frontmatter_text = match.group(1)
        try:
            # Parse YAML frontmatter
            frontmatter_data = yaml.safe_load(frontmatter_text)
            # Remove frontmatter from content
            content_without_frontmatter = content[match.end():]
            return frontmatter_data, content_without_frontmatter
        except yaml.YAMLError as e:
            # If YAML parsing fails, assume it's not valid frontmatter
            print(f"Warning: Found frontmatter-like content but couldn't parse as YAML: {e}", file=sys.stderr)
            return {}, content
    else:
        # No frontmatter found
        return {}, content


def parse_markdown(markdown_content: str) -> Dict[str, Any]:
    """
    Parse markdown content using custom mistune parser and return as a dictionary.
    Handles YAML frontmatter if present.
    
    Args:
        markdown_content: Markdown text to parse
        
    Returns:
        Dictionary representation of the parsed markdown with frontmatter
    """
    # Extract frontmatter if present
    frontmatter, content_without_frontmatter = extract_frontmatter(markdown_content)
    
    # Create a custom parser that can distinguish horizontal rule types
    block_parser = CustomMarkdownParser()
    markdown_parser = mistune.Markdown(
        renderer=None,
        block=block_parser,
    )
    
    # Store the original text for reference
    block_parser.original_text = content_without_frontmatter
    
    # Parse the markdown (without frontmatter)
    parsed_data = markdown_parser(content_without_frontmatter)
    
    # Include frontmatter in the result if it exists
    result = {
        'content': parsed_data
    }
    
    if frontmatter:
        result['frontmatter'] = frontmatter
    
    return result


def read_markdown_file(file_path: str) -> str:
    """
    Read markdown content from a file.
    
    Args:
        file_path: Path to the markdown file
        
    Returns:
        Content of the markdown file as a string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)


def export_to_json(data: Dict[str, Any], output_path: str) -> None:
    """
    Export dictionary data to a JSON file.
    
    Args:
        data: Dictionary data to export
        output_path: Path where JSON file will be saved
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Successfully exported to {output_path}")
    except Exception as e:
        print(f"Error exporting to JSON: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """
    Main function to handle command-line arguments and execute the parser.
    
    Command-line arguments:
        --file, -f: Path to markdown file
        --string, -s: Markdown string to parse
        --export, -e: Export parsed data to JSON file
        --include-frontmatter: Include YAML frontmatter in output (default: True)
    
    Example usages:
        python markdown_to_json.py --file example.md
        python markdown_to_json.py --file example.md --export example.json
        python markdown_to_json.py --string "# Title\n\nContent" --export example.json
    
    Returns:
        Dictionary containing parsed Markdown data
    """
    parser = argparse.ArgumentParser(description='Parse markdown to dictionary/JSON with frontmatter handling')
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--file', '-f', help='Path to markdown file')
    input_group.add_argument('--string', '-s', help='Markdown string to parse')
    
    parser.add_argument('--export', '-e', help='Export parsed data to JSON file')
    parser.add_argument('--include-frontmatter', action='store_true', 
                       help='Include YAML frontmatter in output (default: True)')
    
    args = parser.parse_args()
    
    # Get markdown content either from file or string
    if args.file:
        markdown_content = read_markdown_file(args.file)
    else:
        markdown_content = args.string
    
    # Parse the markdown content
    parsed_data = parse_markdown(markdown_content)
    
    # Export to JSON if requested
    if args.export:
        export_to_json(parsed_data, args.export)
    else:
        # Print to stdout if not exporting
        print(json.dumps(parsed_data, indent=2))
    
    return parsed_data


# Example of how to use this module programmatically:
"""
# Import the module
from markdown_to_json import parse_markdown, export_to_json

# Parse markdown content
markdown_str = "# My Document\n\nThis is some content."
parsed_data = parse_markdown(markdown_str)

# Or parse a file
with open('document.md', 'r') as f:
    markdown_content = f.read()
parsed_data = parse_markdown(markdown_content)

# Export to JSON
export_to_json(parsed_data, 'output.json')

# Process with json_to_slides.py
# python json_to_slides.py --file output.json --export slides.json
"""

if __name__ == "__main__":
    main()
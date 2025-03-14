#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Dict, List, Any, Union, Optional


def convert_mistune_to_slide_format(markdown_data: Dict[str, Any], debug=False) -> Dict[str, Any]:
    """
    Converts mistune parsed markdown content into a structured format for PowerPoint slides.
    
    Args:
        markdown_data: Dictionary containing parsed markdown content from mistune
        debug: Enable debug printing
        
    Returns:
        Dictionary organized for PowerPoint slide creation in enhanced format
    """
    # Extract content nodes from the input data
    if 'content' in markdown_data:
        # If the input has a content field (from our previous parser)
        content_nodes = markdown_data['content']
    else:
        # Otherwise assume the input itself is the content
        content_nodes = markdown_data
    
    # Initialize presentation structure
    presentation = {
        "metadata": {
            "title": "Untitled Presentation",
            "author": "",
            "theme": "default"
        },
        "slides": []
    }
    
    # Variables to track current state
    current_slide = None
    current_title = "Untitled"
    slide_id_counter = 1
    in_second_column = False
    
    if debug:
        print(f"Total nodes to process: {len(content_nodes)}")
    
    # First pass: extract frontmatter if present
    if 'frontmatter' in markdown_data:
        frontmatter = markdown_data['frontmatter']
        if 'title' in frontmatter:
            presentation['metadata']['title'] = frontmatter['title']
        if 'author' in frontmatter:
            presentation['metadata']['author'] = frontmatter['author']
        if 'theme' in frontmatter:
            presentation['metadata']['theme'] = frontmatter['theme']
    
    # Process each node in the content
    for i, node in enumerate(content_nodes):
        if debug:
            print(f"\nProcessing node {i}: {node.get('type', 'unknown')}")
        
        # Handle heading level 2 (new slide with new title)
        if node.get('type') == 'heading' and node.get('attrs', {}).get('level') == 2:
            if debug:
                print(f"Found h2 heading - creating new slide")
            
            # If we have an existing slide, finalize it
            if current_slide:
                presentation['slides'].append(current_slide)
                slide_id_counter += 1
            
            # Get the title text
            title_text = extract_text_from_node(node)
            current_title = title_text if title_text else f"Slide {slide_id_counter}"
            
            # Create a new slide
            current_slide = {
                "id": f"slide-{slide_id_counter}",
                "title": current_title,
                "layout": "title_and_content",
                "content": []
            }
            in_second_column = False
        
        # Handle horizontal rule (thematic break)
        elif node.get('type') == 'thematic_break':
            marker_type = node.get('marker_type', 'dash')  # Default to dash
            
            if debug:
                print(f"Found horizontal rule with marker type: {marker_type}")
            
            # '---' creates a new slide with the same title
            if marker_type == 'dash':
                # If we have an existing slide, finalize it
                if current_slide:
                    presentation['slides'].append(current_slide)
                    slide_id_counter += 1
                
                # Create a new slide with the same title
                current_slide = {
                    "id": f"slide-{slide_id_counter}",
                    "title": current_title,
                    "layout": "title_and_content",
                    "content": []
                }
                in_second_column = False
            
            # '***' creates a two-column layout
            elif marker_type == 'asterisk':
                if current_slide:
                    # Convert current slide to a two-column layout if not already
                    if current_slide["layout"] != "two_content":
                        current_slide["layout"] = "two_content"
                        # Move existing content to the first column
                        existing_content = current_slide.get("content", [])
                        current_slide["columns"] = [
                            {"width": 0.5, "content": existing_content.copy()},
                            {"width": 0.5, "content": []}
                        ]
                        # Remove the old content field
                        current_slide["content"] = []
                    in_second_column = True
                else:
                    # If no current slide, create one with two columns
                    current_slide = {
                        "id": f"slide-{slide_id_counter}",
                        "title": current_title,
                        "layout": "two_content",
                        "columns": [
                            {"width": 0.5, "content": []},
                            {"width": 0.5, "content": []}
                        ],
                        "content": []
                    }
                    in_second_column = True
        
        # Skip blank lines
        elif node.get('type') == 'blank_line':
            continue
        
        # All other content nodes
        else:
            # If we don't have a slide yet, create one
            if not current_slide:
                current_slide = {
                    "id": f"slide-{slide_id_counter}",
                    "title": current_title,
                    "layout": "title_and_content",
                    "content": []
                }
                in_second_column = False
            
            # Process the node and add it to the current slide
            processed_content = process_content_node(node)
            if processed_content:
                # Add to appropriate content array based on layout
                if current_slide["layout"] == "two_content":
                    # For two-column layout
                    column_index = 1 if in_second_column else 0
                    current_slide["columns"][column_index]["content"].append(processed_content)
                else:
                    # For single-column layout
                    current_slide["content"].append(processed_content)
    
    # Add the last slide if it exists
    if current_slide:
        presentation['slides'].append(current_slide)
    
    if debug:
        print(f"\nTotal slides created: {len(presentation['slides'])}")
    
    return {"presentation": presentation}


def extract_text_from_node(node: Dict[str, Any]) -> str:
    """
    Extracts text content from a node, handling different node structures.
    
    Args:
        node: The node to extract text from
        
    Returns:
        The extracted text as a string
    """
    if 'raw' in node:
        return node['raw']
    
    if 'children' in node:
        text_parts = []
        for child in node['children']:
            if child.get('type') == 'text':
                text_parts.append(child.get('raw', ''))
            elif child.get('type') in ('strong', 'emphasis'):
                text_parts.append(extract_text_from_node(child))
            elif child.get('type') == 'softbreak':
                text_parts.append(' ')
        return ''.join(text_parts)
    
    return ""


def process_content_node(node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Processes a content node into our structured format.
    
    Args:
        node: The node to process
        
    Returns:
        A dictionary representing the processed content
    """
    node_type = node.get('type')
    
    if node_type == 'paragraph':
        return {
            "type": "paragraph",
            "spans": process_inline_content(node.get('children', []))
        }
    
    elif node_type == 'heading':
        level = node.get('attrs', {}).get('level', 1)
        if level != 2:  # H2s are handled separately as slide titles
            return {
                "type": "heading",
                "level": level,
                "spans": process_inline_content(node.get('children', []))
            }
    
    elif node_type == 'list':
        list_style = "number" if node.get('attrs', {}).get('ordered', False) else "bullet"
        return {
            "type": "list",
            "style": list_style,
            "items": process_list_items(node.get('children', []))
        }
    
    elif node_type == 'block_code':
        return {
            "type": "code",
            "language": node.get('attrs', {}).get('info', ''),
            "text": node.get('raw', ''),
            "styles": {"background": "#f0f0f0"}
        }
    
    elif node_type == 'block_quote':
        return {
            "type": "blockquote",
            "spans": process_inline_content(node.get('children', [])),
            "styles": {"color": "#666666"}
        }
    
    elif node_type == 'image':
        return {
            "type": "image",
            "path": node.get('attrs', {}).get('url', ''),
            "alt": extract_text_from_node(node),
            "caption": "",
            "width": None,
            "height": None
        }
    
    elif node_type == 'table':
        # Table processing is more complex, this is a simplified version
        return {
            "type": "table",
            "headers": [],  # Would need to extract from node
            "rows": []      # Would need to extract from node
        }
    
    # Return None for node types we don't process
    return None


def process_inline_content(children: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Processes inline content (text with formatting) into spans.
    
    Args:
        children: List of child nodes containing inline content
        
    Returns:
        List of span dictionaries with text and styles
    """
    spans = []
    
    for child in children:
        if child.get('type') == 'text':
            spans.append({
                "text": child.get('raw', ''),
                "styles": {}
            })
        
        elif child.get('type') == 'strong':
            # Bold text
            spans.append({
                "text": extract_text_from_node(child),
                "styles": {"bold": True}
            })
        
        elif child.get('type') == 'emphasis':
            # Italic text
            spans.append({
                "text": extract_text_from_node(child),
                "styles": {"italic": True}
            })
        
        elif child.get('type') == 'link':
            # Link
            spans.append({
                "text": extract_text_from_node(child),
                "styles": {"link": child.get('attrs', {}).get('url', '')}
            })
        
        elif child.get('type') == 'softbreak':
            # Soft line break (space)
            spans.append({
                "text": " ",
                "styles": {}
            })
        
        elif child.get('type') == 'hardbreak':
            # Hard line break
            spans.append({
                "text": "\n",
                "styles": {}
            })
        
        # Handle any nested inline content
        elif child.get('children'):
            nested_spans = process_inline_content(child.get('children', []))
            spans.extend(nested_spans)
    
    return spans


def process_list_items(items: List[Dict[str, Any]], level: int = 0) -> List[Dict[str, Any]]:
    """
    Processes list items into our structured format.
    
    Args:
        items: List of list item nodes
        level: Current nesting level
        
    Returns:
        List of structured list items
    """
    result = []
    
    for item in items:
        # Extract text content
        text_blocks = []
        subitems = []
        
        for child in item.get('children', []):
            if child.get('type') == 'block_text':
                # This is the main content of the list item
                text = extract_text_from_node(child)
                text_blocks.append(text)
            
            elif child.get('type') == 'list':
                # This is a nested list
                nested_items = process_list_items(child.get('children', []), level + 1)
                subitems.extend(nested_items)
        
        # Create the list item
        list_item = {
            "text": ' '.join(text_blocks),
            "level": level
        }
        
        # Add subitems if any
        if subitems:
            list_item["subitems"] = subitems
        
        result.append(list_item)
    
    return result


def main():
    parser = argparse.ArgumentParser(description='Convert markdown JSON to structured slide format')
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--file', '-f', help='Path to JSON file with parsed markdown')
    input_group.add_argument('--string', '-s', help='JSON string with parsed markdown')
    
    parser.add_argument('--export', '-e', help='Export organized data to JSON file')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    # Get input data
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                input_data = json.load(f)
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            input_data = json.loads(args.string)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON string: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Convert to our structured format
    structured_data = convert_mistune_to_slide_format(input_data, debug=args.debug)
    
    # Export to JSON if requested
    if args.export:
        try:
            with open(args.export, 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, indent=2)
            print(f"Successfully exported to {args.export}")
        except Exception as e:
            print(f"Error exporting to JSON: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Print to stdout if not exporting
        print(json.dumps(structured_data, indent=2))
    
    return structured_data


if __name__ == "__main__":
    main()
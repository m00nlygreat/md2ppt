# md2ppt Project Guidelines

## Commands
- Run main converter: `python main.py <markdown_file_path> [--export]`
- Parse markdown to JSON: `python markdown_to_json.py --file <path> [--export <output.json>]`
- Convert JSON to slides: `python json_to_slides.py --file <input.json> [--export <output.json>] [--debug]`
- Test with sample file: `python main.py test/ChatGPT\ 기초\ 사용법.md --export`

## Code Style
- **Naming**: Use snake_case for functions and variables, CamelCase for classes
- **Types**: Always include type hints using the typing module
- **Docstrings**: Use Google style format with Args and Returns sections
- **Imports**: Group standard library, third-party, and local imports
- **Error Handling**: Use try/except blocks with specific exceptions
- **Error Output**: Write error messages to stderr and use sys.exit(1)
- **Testing**: Use assertions and descriptive print statements during development

## Architecture
This project uses a pipeline of preprocessors to convert Markdown to PowerPoint:
1. Flatten embedded markdown files into one document
2. Convert relative image paths to absolute paths
3. Process markdown to presentation format with slides based on H2 headings
4. Convert markdown to JSON representation of slides
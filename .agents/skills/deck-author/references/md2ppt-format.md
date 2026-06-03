# md2ppt Format Reference

## Pipeline

The `md2ppt` CLI runs this sequence:

1. `flatten.py`: recursively expands standalone Markdown embeds such as `![](modules/01-intro.md)`.
2. `md2json.py`: parses YAML frontmatter and Markdown tokens with Mistune.
3. `json2slide.py`: converts tokens into slides, placeholders, notes, and layout names.
4. `json2pptx.py`: renders the slide JSON into a PowerPoint file with `python-pptx`.

## Root And Child Files

Only the root Markdown file should normally include YAML frontmatter:

```markdown
---
title: My Deck
author: Alice
materials:
  - starter-files.zip
  - sample-data.csv
---
```

Use `materials` only for short, direct hands-on materials used during the lesson, such as starter files, sample datasets, worksheets, templates, prompt packs, screenshots, or exercise source files. Do not include environment prerequisites such as accounts, permissions, API keys, software or package installation, device/browser requirements, network access, or login status. If there are no direct hands-on materials, use `materials: []`.

With the default built-in template selected by the `md2ppt` CLI, avoid `subtitle` in frontmatter unless the reference template's title slide has subtitle placeholder index `1`. The current default template only has a title placeholder.

The root file acts as a table of contents and composition file. It can contain `#` chapter headings and standalone child Markdown embeds:

```markdown
# Chapter 1

![](modules/01-overview.md)

# Chapter 2

![](modules/02-practice.md)
```

Child files contain the actual slides. `flatten.py` strips child frontmatter, so do not rely on metadata inside child files.

## Slide Boundaries

- `# Heading` and `## Heading` start a new slide.
- `# Heading` also creates a table-of-contents chapter.
- `## Heading` creates a module entry under the latest chapter.
- `###` through `######` become headings inside the current slide placeholder.
- `---` and `___` force a new slide.
- `***` splits the current slide into another placeholder/content area.

Example:

```markdown
## Two-part Slide

- Left side text
- More text

***

![](../attachments/diagram.png)
```

## Layout Selection

`json2slide.py` chooses a layout automatically unless `[layout]: # (...)` is present.

Automatic layout rules:

- No non-empty placeholders: `section_header`
- One non-empty placeholder: `title_and_content`
- Two shared placeholders: `two_content`
- Two placeholders where one contains a monopoly token such as image or table: `content_with_caption`

Known layout names in the default built-in template selected by the `md2ppt` CLI:

- `title_slide`
- `comparison`
- `title_and_content`
- `section_header`
- `two_content`
- `image_first`
- `two_images`
- `blank`
- `content_with_caption`
- `toc`
- `examples`

Force a layout with a standalone comment block:

```markdown
[layout]: # (two_images)
```

The converter normalizes PowerPoint layout names to uppercase enum keys, so use lowercase snake case in Markdown.

## Notes

Add speaker notes with:

```markdown
[note]: # (Mention the live demo before moving on.)
```

Current md2ppt code collects notes in slide JSON. Confirm the selected `json2pptx.py` version renders notes before relying on them in final PPTX.

## Images And Assets

Use local image files. Supported practical extensions are `png`, `jpg`, `jpeg`, `gif`, `svg`, and `webp`; `json2pptx.py` opens images with Pillow. For slide visuals authored through this skill, save the final deck-referenced asset as a transparent `.png` with an alpha channel.

Use a standalone image line:

```markdown
![](../attachments/workflow.png)
```

When a child module references an image, `flatten.py` rewrites the path relative to the root deck. This means `../attachments/workflow.png` from `modules/01-intro.md` becomes `attachments/workflow.png` in the flattened Markdown.

If a needed slide visual does not exist:

1. Use `$imagegen` to generate or edit the raster asset.
2. Move the selected project-bound output into `attachments/`.
3. Ensure the final saved asset is a transparent PNG.
4. Reference the saved relative path from the module Markdown.
5. Avoid leaving a deck-referenced image only under `$CODEX_HOME/generated_images`.

Default slide image types:

1. Concept diagram: 3-5 named elements and their relationships.
2. Process image: workflow, flowchart, sequence, or timeline.
3. System/technical structure image: architecture, data-flow, or component diagram.
4. Case/example image: representative example, before/after comparison, result mockup, or comparison cards.
5. Metaphor image: visual analogy for the deck's central message.
6. Markup image: annotation on a provided screenshot or image; ask for the source screenshot/image if it is missing.

These categories can be combined when the user request calls for a hybrid visual.

## Supported Markdown Content

- Paragraphs and inline links
- Bold with `**text**`
- Italic with `*text*`
- Inline code with backticks
- Ordered and unordered lists, including nested lists
- Block quotes with `>`
- Fenced code blocks with language info
- Pipe tables
- Standalone local images

Avoid HTML blocks, Mermaid fences, remote image URLs, footnotes, definition lists, and complex inline image/text mixtures unless the converter has been extended and tested for them.

## Conversion Commands

Direct compile from the root deck directory:

```powershell
md2ppt -i ".\deck.md" -o ".\deck.pptx" --template default
```

List built-in templates:

```powershell
md2ppt --list-templates
```

Use another built-in template by name:

```powershell
md2ppt -i ".\deck.md" -o ".\deck.pptx" --template hanyang
```

Use an external reference `.pptx` file:

```powershell
md2ppt -i ".\deck.md" -o ".\deck.pptx" --ref ".\templates\custom.pptx"
```

Save debug files when needed:

```powershell
md2ppt -i ".\deck.md" -o ".\deck.pptx" --template default --debug --debug-dir ".\debug"
```

Run direct compile from the root deck directory, or use absolute image paths, because `json2pptx.py` opens image paths relative to the current working directory. The bundled checker assumes `md2ppt` is installed on `PATH` and calls the CLI directly for compilation.

## Authoring Heuristics

- One slide should express one idea.
- Use `***` when two areas must remain visually distinct.
- Split long lists across slides instead of shrinking content.
- Prefer diagrams, screenshots, generated teaching visuals, and requested hybrid visuals over decorative imagery.
- Use tables only when there are few columns and rows.
- Keep filenames stable, ASCII when practical, and URL-encode spaces if you hand-write paths.
- Compile early when changing layout-heavy decks; placeholder behavior depends on the reference `.pptx`.

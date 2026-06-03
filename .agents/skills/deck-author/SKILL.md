---
name: deck-author
description: Create, refactor, and polish Markdown slide decks for md2ppt. Use when Codex needs to produce or edit a root deck Markdown file, embedded child Markdown modules, slide-ready assets, slide copy, language editing rules, layout or note directives, tables, code blocks, image references, or md2ppt-ready presentation source.
---

# Deck Author

## Overview

Use this skill to author Markdown that converts cleanly through [md2ppt](https://github.com/m00nlygreat/md2ppt) into PowerPoint. The converter flattens embedded Markdown, parses slides/placeholders, and renders them into a reference `.pptx` template.

This skill defines authoring rules only. Use `$deck-reviewer` when an existing deck needs a quality review or fast correction pass.

## Workflow

1. Identify the deck root, target audience, duration, and source material.
2. Before writing slide content, perform Slide Intent & Composition Planning for each slide or section.
3. Create a root Markdown file with deck-level YAML frontmatter that includes `title` and `materials`. If authoring a lesson `text.md` directly, add YAML frontmatter with `title` and `materials` there too.
4. Put lesson content in child Markdown modules under a stable folder such as `modules/`; put generated or collected visual assets under `attachments/`.
5. Before adding embedded child Markdown references to the root deck, show the proposed embed list and get user confirmation.
6. Use md2ppt grammar deliberately: `#` or `##` starts a slide, `***` splits placeholders inside the current slide, and `---` or `___` forces a new slide only when there is no new slide heading. Do not place `---` between consecutive slide headings.
7. Keep child modules free of YAML frontmatter unless there is a specific reason; `flatten.py` ignores child frontmatter.
8. Save slide image assets as transparent PNG project files and reference them with relative Markdown image paths. If a new raster visual is needed for a slide, first try to find a relevant source or reference image through internet search when that would produce a more accurate or recognizable visual; otherwise use `$imagegen`. Move the final project-bound `.png` into `attachments/` before referencing it.
   - For newly generated slide visuals, use `$imagegen` with the default `gpt-image-2` image-generation path and request a bitmap/raster result such as realistic, 3D-rendered, photographic, painterly, or other generated-image styles. Do not substitute SVGs, hand-authored vector drawings, or flat vector-style placeholder art when the slide calls for an image. Use vector/flat SVG style only when the user explicitly asks for it, such as "draw a diagram", "make an SVG", "use vector style", or a similar direct request.
   - When prompting generated slide visuals, ask for all important subjects and objects to sit fully inside the image frame with generous padding; avoid cropped heads, hands, devices, documents, UI panels, or other key elements touching the image edge. Prefer a transparent or easily removable plain background so the asset sits naturally on the slide.
   - Do not reuse the same image across multiple slides in one deck merely to fill space. Each repeated image must have a distinct instructional role, such as a progressive annotation, before/after contrast, or recap. If a slide feels visually empty, create or find a slide-specific visual instead of repeating a generic asset.
9. Before running `md2ppt`, choose and state the working directory explicitly. Default to the directory that contains the Markdown file passed to `-i`; do not run from the repository root merely because that is the current shell directory.

## File Structure

Prefer this shape:

```text
deck-title.md
modules/
  01-intro.md
  02-practice.md
attachments/
  concept-map.png
  workflow-step.png
debug/
```

Root file pattern:

```markdown
---
title: Deck Title
author: Instructor Name
materials:
  - starter-files.zip
  - sample-data.csv
  - worksheet.md
---

# Chapter Title

![](modules/01-intro.md)

# Practice

![](modules/02-practice.md)
```

Child module pattern:

```markdown
## Slide Title

- One clear idea
- Keep bullets short

***

![](../attachments/example.png)

## Next Slide Title

- Another clear idea

### Supporting Heading

Use `###` to add an in-slide heading instead of starting a new slide.
```

## Slide Intent & Composition Planning

Before writing slide content, first plan the intended role and composition of each slide. Do not start filling in body copy, bullets, charts, images, tables, or speaker notes until this planning step is complete.

For each slide, define:

1. Slide intent: what is the one thing this slide should make the audience understand, believe, decide, or feel? Express this as a single clear sentence, not a topic label.
2. Audience transition: what does the audience likely think before seeing this slide, and what should they think after seeing it? The slide should move the audience across that gap.
3. Narrative role: why does this slide exist at this point in the deck? Decide whether it sets context, makes a claim, proves a point, compares options, resolves tension, drives a decision, or performs another specific job.
4. Composition strategy: decide the necessary elements before writing them, such as the headline or takeaway, primary visual/chart/diagram/table/image, supporting evidence, annotations or callouts, and minimal explanatory text. Assign each element a job and remove any element that does not support the slide intent.
5. Content boundary: decide what this slide should not cover. If a point belongs in another slide, move it there instead of overloading the current slide.

Before drafting body content, choose the lightest format that carries the intent: bullets, table, comparison, steps, example, or image.

Only after this planning step should the slide be drafted. A slide is not a place to pour in available information; it is a deliberately designed step in the audience's reasoning.

## Slide Image Types

When planning or creating visuals, explicitly classify requested slide images using these six default types. These are defaults, not hard boundaries: if the user asks for an image that crosses categories, create the hybrid image that best serves the slide instead of forcing it into only one type.

1. Concept diagram: a simple relationship map of the core idea, usually 3-5 named elements connected by lines. Keep in-image text to element names, not explanatory sentences.
2. Process image: a workflow, flowchart, sequence, or timeline that shows the slide's steps. Prefer four or fewer steps with short labels and clear directional flow.
3. System/technical structure image: an architecture, data-flow, or component diagram. Show the main actors, interface, processing layer, storage, model, or external services as named blocks.
4. Case/example image: a representative example, before/after comparison, result mockup, or 2-3 comparison cards. Use real provided material when available; otherwise create a clearly illustrative example.
5. Metaphor image: a visual analogy for the deck's message, such as scattered inputs becoming an organized structure or multiple streams converging into one output. Prefer little or no text.
6. Markup image: annotations on a provided screenshot or image, using boxes, arrows, numbers, highlights, and short labels to point out key UI areas, issues, or comparison points. If no source screenshot or image is available, ask the user to provide one before making the markup image.

All final deck-referenced images must be transparent PNG files. Source screenshots or references may arrive in other formats, but the asset saved under `attachments/` should be a `.png` with an alpha channel; preserve opaque screenshot/photo content when needed and keep any canvas, padding, or non-image background transparent. For generated assets, keep the full subject comfortably inside the canvas and avoid edge cropping so the image can be scaled or placed on a slide without awkward cuts.

When a slide needs a concrete object, product, place, person, UI, case, or other reality-based visual, try internet image search before generating a new image. Prefer authoritative, relevant, inspectable sources over generic stock-like images. Use `$imagegen` when search does not provide a suitable source, when the slide needs a conceptual or synthetic visual, or when licensing/source constraints make direct reuse inappropriate. Save only the final deck-ready asset under `attachments/` and keep any source attribution or usage caveat in speaker notes when needed.

When using `$imagegen` for slide imagery, explicitly prompt for a generated bitmap/raster image and avoid vector-style language unless the user specifically asks for vector art, flat SVG, or a diagram-style drawing. Prefer wording such as "3D rendered scene", "photographic slide visual", "textured bitmap illustration", or "generated raster infographic" over "SVG", "flat vector", or "vector icon set". If the user's request says "image generation", do not satisfy it by drawing native SVG shapes; reserve vector/flat SVG style for explicit requests such as "draw a diagram".

Within a single deck, avoid using the same image file on more than one slide unless the repetition is intentional and pedagogically useful. Acceptable repetitions include stepwise markup of the same screenshot, a before/after pair, or a final recap that explicitly refers back to an earlier visual. Unacceptable repetitions include using the same decorative workflow, icon set, or generic illustration to make unrelated slides look less empty.

## Language And Editing

Treat language editing as part of slide design, not as a separate proofreading pass. Make slide copy concise, consistent, and presentation-ready while preserving the original meaning, evidence level, and speaker intent.

### Default Tone

Use a clear, professional, instructional tone unless the user specifies otherwise. Avoid overly casual phrasing, exaggerated marketing copy, vague motivational language, and unsupported strengthening of claims.

For Korean decks, default to compact business Korean. Use outline-style Korean and noun-ending phrases by default for slide bullets, labels, and short supporting copy. Avoid excessive honorific endings on slides unless the deck's audience or brand voice requires them.

### Slide Copy Rules

- Keep each slide centered on one message.
- Prefer short phrases over full paragraphs.
- Use parallel structure within bullet lists.
- Use bullets when they are the clearest slide format. Keep simple parallel items as one-level lists.
- Use multi-level lists when the content itself has layers, such as a main point with examples, conditions, concrete actions, cautions, short explanations, or sub-decisions.
- Do not turn every list into a multi-level list. If the items are equal-weight choices, features, materials, or steps, a flat list is usually clearer.
- If consecutive slides repeat the same bullet-list structure, convert some slides to another compact format.
- Use Markdown inline emphasis deliberately: apply `**bold**` to the key term, number, decision, contrast, or takeaway that should catch the audience's eye; use `*italic*` sparingly for nuance, labels, cited wording, or secondary emphasis.
- Use Markdown inline code for literal tokens such as commands, file paths, filenames, API names, model names, environment variables, configuration keys, code identifiers, and exact UI or CLI values.
- Keep emphasis selective. Do not bold entire bullets, stack multiple emphasis styles on the same phrase without a clear reason, or emphasize so many words that the slide loses hierarchy.
- Do not mix noun-phrase bullets and sentence-style bullets in the same list unless there is a clear reason.
- Move nuance, transitions, examples, and caveats into speaker notes instead of crowding the slide.
- Replace abstract wording with concrete nouns, verbs, numbers, or examples.
- Keep image labels, diagram labels, and chart annotations short; use element names rather than explanatory sentences.

### Korean Editing Rules

For Korean slide decks:

- Keep spacing, punctuation, and terminology consistent.
- Prefer concise business Korean over translated-English phrasing.
- Write slide-visible text as phrase-based copy by default. Use sentence-style Korean only in limited practice-step instructions where prose is necessary for clear execution, or in quoted text.
- Avoid unnecessary English loanwords when a natural Korean term is clearer.
- Preserve domain terms, product names, model names, API names, and quoted source wording.
- Normalize repeated terms into one canonical form, such as choosing one of `워크플로`, `작업 흐름`, or `프로세스`.
- Use Arabic numerals for quantities, steps, dates, and measurable values unless the deck style requires otherwise.

### Titles And Headings

Prefer slide titles that state the slide's point, not just its topic.

Weak:

- Market Overview
- 주요 기능
- 문제점

Better:

- The Market Is Fragmented Across Three Buyer Groups
- 반복 작업을 줄이는 3가지 핵심 기능
- 현재 프로세스는 검토 단계에서 병목 발생

### Editing Scope

When asked to polish, proofread, or refine a deck:

1. Fix obvious grammar, spelling, spacing, and punctuation issues.
2. Tighten long sentences into slide-ready copy.
3. Make headings and bullets structurally consistent.
4. Preserve the original meaning, evidence level, and speaker intent.
5. Flag ambiguous claims instead of silently inventing details.
6. If the target audience or tone is unclear, use the default professional instructional tone and mention the assumption.

## Authoring Rules

- Any Markdown file passed directly to `md2ppt` must start with YAML frontmatter containing `title`; otherwise the generated PPTX may have an empty or broken title slide.
- Compile from the directory that makes the deck's relative paths resolve. Usually this is the input Markdown file's folder, with commands like `md2ppt -i ".\lesson.md" -o ".\lesson.pptx" --template inno`; put debug output outside that folder with a relative path such as `--debug-dir "..\debug\lesson"` when needed.
- Before compiling a deck with embedded Markdown modules or images outside the deck folder, verify at least the referenced module paths and representative image paths with `Test-Path` from the intended working directory. If `md2ppt` reports missing images or invalid paths, treat the PPTX as not validated, fix the working directory or paths, and regenerate before reporting completion.
- Add `materials` to the root YAML frontmatter as a YAML list. Keep it to a short list of hands-on materials learners will directly use during the lesson, such as starter files, sample datasets, worksheets, templates, prompt packs, screenshots, or exercise source files.
- Exclude deck-authoring artifacts and presentation-only assets from `materials`, including child Markdown modules, slide images, diagrams, generated visual assets, reference screenshots shown only by the instructor, and files used only to compose or render the PPTX.
- Exclude environment prerequisites from `materials`, including account creation, permissions, API keys, software installation, package installation, device/browser requirements, network access, and login status. If the lesson has no direct hands-on materials, use `materials: []`.
- Before inserting standalone child Markdown embeds such as `![](modules/01-intro.md)` into the root deck, present the intended embed paths and order to the user and wait for confirmation.
- Use standalone `![](child.md)` lines for embeds. `flatten.py` only expands Markdown embeds that occupy the full line.
- Use standalone image lines. Local image files are monopoly/block-level picture elements that occupy an image placeholder; inline images are not a reliable slide content pattern.
- Do not add `***` solely because a standalone image, pipe table, chart, diagram, or code block appears. These placeholder-occupying elements can create/occupy their own placeholder without `***`; use `***` only when you intentionally need to force separate text/media regions.
- In the default Content with Caption layout, put placeholder-occupying elements such as images, tables, charts, diagrams, and code blocks in the right/back placeholder by ordering content deliberately: write the caption, bullets, or explanatory text first, then place the image/table/code block. Add `***` only when the inferred split is ambiguous or you need an explicit boundary.
- Do not put a table and an image on the same slide. Treat tables and images as conceptually equivalent explanatory formats; choose one, or split them into separate slides when both are needed.
- Treat pipe tables as monopoly/block-level elements that occupy their entire placeholder. Do not continue with body text, headings, lists, or code after a table in the same visual area; put explanatory text before the table, force a separate region with `***`, or move the additional content to another slide.
- Do not add `[layout]: # (...)` by default. md2ppt infers the layout from headings, slide breaks, and placeholder count.
- Use `[layout]: # (layout_name)` only when intentionally forcing a layout that exists in the target template and cannot be inferred automatically. Do not add internal/default layout names such as `section_header`, `title_and_content`, or `two_content` unless the target template actually contains that layout name.
- Use `[note]: # (speaker note text)` on its own line for slide notes.
- Prefer `##` for normal content slides inside modules. Use `#` when a section divider or table-of-contents chapter is intentional.
- When sketching or drafting slide headings, list consecutive `##` headings directly. Do not add `---` between them; the heading already starts the next slide. For heading-only outlines or early structure drafts, omit slide separators entirely unless the user explicitly asks for md2ppt-ready slide breaks.
- Use `---` or `___` only to force a new slide without a slide heading, or to separate two slides where the next slide intentionally starts with non-heading content.
- Keep each slide to one main message. If a slide intentionally needs separate text and media regions that md2ppt cannot infer safely from monopoly elements, split those areas with `***`.
- Use pipe tables only for small tables that can fit in one slide placeholder by themselves.
- Use fenced code blocks for code; include the language tag for syntax highlighting.

Read `references/md2ppt-format.md` when you need the full syntax, conversion pipeline, layouts, or examples.

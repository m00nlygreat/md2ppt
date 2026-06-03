---
name: deck-reviewer
description: Review and quickly improve Markdown slide decks, especially md2ppt decks. Use when Codex needs to inspect an existing deck for slide quality issues such as inconsistent Korean endings, flat or sparse text, empty or low-density slides, repeated slide patterns, duplicated visuals, weak hierarchy, or presentation-readiness problems, then make focused edits without rebuilding the whole deck.
---

# Deck Reviewer

## Overview

Use this skill to make an existing Markdown deck presentation-ready through a fast review-and-fix pass. Prioritize visible slide quality over broad rewriting: endings, hierarchy, density, variation, and obvious md2ppt rendering risks.

If the task requires creating a new deck, changing md2ppt syntax deeply, compiling PPTX, or authoring slide assets from scratch, use `$deck-author` together with this skill.

## Workflow

1. Identify the deck root and embedded Markdown modules.
2. Read enough neighboring slides to understand the deck's tone, audience, and repeated patterns.
3. Build a short issue list grouped by slide or module. Focus on issues that can be fixed immediately.
4. Edit the Markdown directly, keeping the deck's existing structure unless a structural fix is clearly needed.
5. Re-read the edited slides and confirm that the target issues are resolved.
6. Report only the meaningful changes and any remaining risks.

When reviewing embedded md2ppt decks, follow standalone Markdown embeds such as `![](modules/01-intro.md)`. Review the root deck for section flow, but make most quality edits in the module files where slide bodies live.

## Review Priorities

### 1. Ending Consistency

Inspect slide-visible text: titles, bullets, labels, callouts, and table cells.

For Korean decks:

- Prefer compact noun-ending or outline-style Korean for slide text.
- Convert accidental sentence-style prose into phrase-based slide copy.
- Watch endings such as `-합니다`, `-됩니다`, `-입니다`, `-있습니다`, `-없습니다`, `-합니다`, `-하세요`, `-합니다.` and similar polite/narrative endings.
- Allow short sentence-style Korean only for hands-on practice steps where a phrase would make the action unclear, or for direct quotes.
- Keep endings parallel inside one bullet list or table column.

For English decks:

- Keep titles and bullets parallel.
- Avoid mixing full-sentence bullets with fragment bullets unless the contrast is intentional.

Speaker notes may use natural prose.

### 2. Rich Text And Hierarchy

Fix flat Markdown that gives every line the same visual weight. Use multi-level lists when the content itself has layers; do not force nesting onto simple parallel items.

Use focused improvements:

- Add selective `**bold**` for the key term, number, decision, contrast, or takeaway.
- Use `*italic*` sparingly for nuance, labels, or cited wording.
- Use inline code for literal UI labels, filenames, commands, variables, API names, model names, and exact values.
- Convert dense or repetitive bullets into a compact table, steps, comparison, callout line, or split placeholders with `***`.
- Use list depth when the slide has a parent-child relationship: keep the main point as a parent bullet and place examples, conditions, concrete actions, cautions, or short explanations under indented child bullets.
- Keep equal-weight choices, features, materials, or steps as flat lists when nesting would make the slide feel artificial.
- Keep emphasis selective. Do not bold whole bullets or decorate most words.

### 3. Non-Empty Slides

Flag slides that look empty or monotonous by visible Markdown structure:

- **Simple one-level list**: a title followed by 3-5 bullets at the same level, with no sub-example, step, comparison, emphasis, or image.
- **No text styling**: no `**bold**`, `*italic*`, inline code, or other emphasis on key terms, numbers, UI labels, or takeaways.
- **No image/table/example**: explanatory text only, with no screenshot, example sentence, compact comparison, steps, callout, or visual asset. Watch feature-introduction slides that end as text lists.
- **Heading plus short body**: a heading with only one short line or 1-2 bullets, unless it is an intentional section transition.

Fast fixes:

- For plain bullet lists, bold only 1-2 key terms with `**bold**`.
- Restructure one-level lists into multi-level lists only when main points and supporting details are actually mixed together.
- Use inline code for UI menus, button labels, filenames, commands, and exact values.
- Add one concrete, neutral everyday example when the slide only explains a concept.
- Convert ordered actions into a 3-step numbered list.
- Use a small before/after or good/bad structure when comparison clarifies the point.
- If a relevant visual asset already exists, place it as a standalone image after the explanatory text.

Do not add generic filler or invent much new content. Every added element must support the slide's one message, action, or distinction. Do not put a table and an image on the same slide.

### 4. Repetition And Monotony

Scan consecutive slides for repeated structures:

- `title + 3 bullets` repeated across many slides.
- Same wording pattern in titles.
- Same image reused without a teaching purpose.
- Repeated table structure where a different format would clarify the point.

Use the smallest useful variation:

- Change one slide into a comparison table.
- Change one slide into a numbered workflow.
- Change one slide into an example-driven slide.
- Combine overly similar slides if the deck is clearly redundant and the user asked for deeper cleanup.
- Preserve repetition when it is an intentional practice rhythm.

### 5. Markdown And Md2ppt Fit

Avoid quality fixes that create converter problems.

- Keep one slide centered on one message.
- Use `***` only for intentional placeholder splits. Do not require `***` merely because a standalone image, pipe table, chart, diagram, or code block appears; these monopoly/block-level elements can create/occupy their own placeholder.
- Do not put a table and an image on the same slide.
- Keep standalone image and Markdown embed lines standalone.
- For the default Content with Caption layout, ensure placeholder-occupying elements such as images, tables, charts, diagrams, and code blocks come after the explanatory text so they land in the right/back placeholder: text/caption first, then the image/table/code block. Add `***` only when the inferred split is ambiguous or a forced boundary is needed.
- Do not add `---` between consecutive slide headings.
- Prefer `##` for normal module slides.
- Keep tables small enough to fit one slide placeholder.

When unsure about md2ppt syntax details, read `$deck-author` or its `references/md2ppt-format.md`.

## Editing Style

Make focused edits rather than rewriting the whole lesson.

- Preserve the existing audience level, instructional sequence, and source meaning.
- Prefer concrete, neutral everyday examples unless the user asks for domain-specific examples.
- Do not expose sensitive course context in slide examples unless it already appears and is necessary.
- Tighten long explanations into slide-ready phrases.
- Move nuance to speaker notes only when notes already exist or the user asks for note work.
- Flag ambiguous claims instead of inventing data.

## Delivery

After editing, summarize:

1. Files changed.
2. Main categories fixed, such as endings, hierarchy, sparse slides, repeated layouts, duplicated visuals.
3. Remaining risks, if any, such as slides that need a new visual asset or PPTX render verification.

If the user asked only for review, provide findings first with slide/file references and do not edit files.

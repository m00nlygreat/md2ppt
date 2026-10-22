"""Safe HTML renderer for the shared slide JSON representation."""

import html
import os
from pathlib import Path
import re
from urllib.parse import urlsplit

import mistune
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name


_SAFE_LINK_SCHEMES = {"http", "https", "mailto", "tel"}
_IMAGE_SUFFIXES = {".apng", ".avif", ".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}


def _text(value):
    return html.escape("" if value is None else str(value), quote=False)


def _attr(value):
    return html.escape("" if value is None else str(value), quote=True)


def _safe_link(url):
    url = str(url or "").strip()
    parts = urlsplit(url)
    if parts.scheme.lower() in _SAFE_LINK_SCHEMES:
        return url
    if parts.scheme or url.startswith("//"):
        return None
    if any(ord(char) < 32 for char in url):
        return None
    return url


def _render_runs(runs):
    rendered = []
    for run in runs or []:
        content = _text(run.get("text", ""))
        if run.get("monospace"):
            content = f"<code>{content}</code>"
        if run.get("bold"):
            content = f"<strong>{content}</strong>"
        if run.get("italic"):
            content = f"<em>{content}</em>"
        href = _safe_link(run.get("hyperlink"))
        if href:
            content = f'<a href="{_attr(href)}" rel="noopener noreferrer">{content}</a>'
        rendered.append(content)
    return "".join(rendered)


def _build_list_tree(items):
    root = []
    ancestors = []
    for item in items or []:
        # json2slide stores top-level list items at depth 0.
        depth = max(0, int(item.get("depth", 0) or 0)) + 1
        while len(ancestors) >= depth:
            ancestors.pop()
        node = {"item": item, "children": []}
        if depth == 1 or not ancestors:
            root.append(node)
        else:
            ancestors[-1]["children"].append(node)
        ancestors.append(node)
    return root


def _render_list_nodes(nodes):
    output = []
    index = 0
    while index < len(nodes):
        ordered = bool(nodes[index]["item"].get("ordered"))
        tag = "ol" if ordered else "ul"
        output.append(f"<{tag}>")
        while index < len(nodes) and bool(nodes[index]["item"].get("ordered")) == ordered:
            node = nodes[index]
            output.append(f"<li>{_render_runs(node['item'].get('runs', []))}")
            if node["children"]:
                output.append(_render_list_nodes(node["children"]))
            output.append("</li>")
            index += 1
        output.append(f"</{tag}>")
    return "".join(output)


def _render_code(token):
    raw = str(token.get("raw", ""))
    language = str(token.get("lang", "") or "").strip().split()[0:1]
    try:
        lexer = get_lexer_by_name(language[0]) if language else TextLexer()
    except Exception:
        lexer = TextLexer()
    highlighted = highlight(raw, lexer, HtmlFormatter(nowrap=True))
    return f'<pre class="code"><code>{highlighted}</code></pre>'


def _resolve_image(url, input_path, register_asset, diagnostics, slide_number):
    url = str(url or "").strip()
    absolute_windows_path = bool(re.match(r"^[A-Za-z]:[\\/]", url))
    parts = urlsplit(url) if not absolute_windows_path else None
    if parts and parts.scheme.lower() in {"http", "https"}:
        return url
    if (parts and parts.scheme) or url.startswith("//"):
        diagnostics.append(f"Slide {slide_number}: unsupported image URL: {url}")
        return None

    # json2slide already decoded local paths. Parsing or decoding again would
    # turn filename '#' and '%' characters into URL fragments or escapes.
    relative_path = url.replace("/", os.sep)
    if re.match(r"^[A-Za-z]:[\\/]", relative_path) or os.path.isabs(relative_path):
        image_path = Path(relative_path)
    else:
        image_path = Path(input_path).parent / relative_path
    image_path = image_path.resolve()
    if image_path.suffix.lower() not in _IMAGE_SUFFIXES:
        diagnostics.append(f"Slide {slide_number}: unsupported image file type: {url}")
        return None
    if not image_path.is_file():
        diagnostics.append(f"Slide {slide_number}: image not found: {url}")
        return None
    return register_asset(image_path)


def _render_token(token, input_path, register_asset, diagnostics, slide_number):
    token_type = token.get("type")
    if token_type == "paragraph":
        return f"<p>{_render_runs(token.get('runs', []))}</p>"
    if token_type == "heading":
        level = min(6, max(3, int(token.get("level", 3) or 3)))
        return f"<h{level}>{_render_runs(token.get('runs', []))}</h{level}>"
    if token_type == "list":
        return _render_list_nodes(_build_list_tree(token.get("children", [])))
    if token_type == "block_quote":
        return f"<blockquote>{_render_runs(token.get('runs', []))}</blockquote>"
    if token_type == "code":
        return _render_code(token)
    if token_type == "image":
        src = _resolve_image(
            token.get("url", ""), input_path, register_asset, diagnostics, slide_number
        )
        alt = token.get("alt", "")
        if not src:
            return f'<div class="missing-image" role="img" aria-label="{_attr(alt)}">Image unavailable: {_text(token.get("url", ""))}</div>'
        return f'<figure><img src="{_attr(src)}" alt="{_attr(alt)}"><figcaption>{_text(alt)}</figcaption></figure>' if alt else f'<figure><img src="{_attr(src)}" alt=""></figure>'
    if token_type == "table":
        parts = ['<div class="table-scroll"><table>']
        if token.get("head"):
            parts.append("<thead><tr>")
            for cell in token["head"]:
                align = cell.get("align", "")
                align_attr = f' data-align="{align}"' if align in {"left", "center", "right"} else ""
                parts.append(f"<th{align_attr}>{_render_runs(cell.get('runs', []))}</th>")
            parts.append("</tr></thead>")
        parts.append("<tbody>")
        for row in token.get("body", []):
            parts.append("<tr>")
            for cell in row:
                align = cell.get("align", "")
                align_attr = f' data-align="{align}"' if align in {"left", "center", "right"} else ""
                parts.append(f"<td{align_attr}>{_render_runs(cell.get('runs', []))}</td>")
            parts.append("</tr>")
        parts.append("</tbody></table></div>")
        return "".join(parts)
    return ""


def _render_placeholder(placeholder, input_path, register_asset, diagnostics, slide_number):
    return "".join(
        _render_token(token, input_path, register_asset, diagnostics, slide_number)
        for token in (placeholder or [])
    )


class _SafeNotesRenderer(mistune.HTMLRenderer):
    """Render note Markdown while escaping raw HTML and unsafe links."""

    def __init__(self):
        super().__init__(escape=True)

    def link(self, text, url, title=None):
        safe_url = _safe_link(url)
        if safe_url is None:
            return text
        title_attr = f' title="{_attr(title)}"' if title else ""
        return (
            f'<a href="{_attr(safe_url)}" rel="noopener noreferrer"{title_attr}>'
            f"{text}</a>"
        )

    def image(self, text, url, title=None):
        # Note images are not registered as slide assets. Keep their safe alt text.
        return text


def _render_notes(notes):
    renderer = _SafeNotesRenderer()
    markdown = mistune.create_markdown(renderer=renderer, plugins=["table"])
    rendered = [markdown(str(note)) for note in (notes or []) if str(note).strip()]
    if not rendered:
        return ""
    return '<aside class="notes">' + "".join(rendered) + "</aside>"


def _render_body_slide(slide, body_index, screen_index, input_path, register_asset, diagnostics):
    slide_number = body_index + 1
    title = _render_runs(slide.get("title", {}).get("runs", []))
    layout = str(slide.get("layout", "") or "")
    placeholders = slide.get("placeholders") or [[]]
    supported_layouts = {
        "section_header",
        "title_and_content",
        "two_content",
        "content_with_caption",
        "two_images",
    }
    if layout not in supported_layouts:
        if layout:
            diagnostics.append(
                f'레이아웃을 알 수 없어 기본 배치를 사용합니다 (슬라이드 {slide_number}: "{layout}").'
            )
        layout_class = "fallback"
    else:
        layout_class = re.sub(r"[^a-zA-Z0-9_-]", "-", layout)
    if slide.get("shapes"):
        shape_names = ", ".join(str(name) for name in slide["shapes"].keys())
        diagnostics.append(
            f"웹 미리보기에서 이름 있는 도형을 지원하지 않습니다 (슬라이드 {slide_number}: {shape_names})."
        )

    slots = []
    for placeholder in placeholders:
        slots.append(
            '<div class="placeholder">'
            + _render_placeholder(placeholder, input_path, register_asset, diagnostics, slide_number)
            + "</div>"
        )
    if not slots:
        slots = ['<div class="placeholder"></div>']
    slot_count = max(1, len(slots))
    slot_columns = 1 if slot_count <= 1 else 2 if slot_count <= 4 else 3
    return (
        f'<section id="slide-{screen_index + 1}" class="slide body-slide layout-{layout_class}" aria-label="Slide {slide_number}">'
        f'<div class="slide-inner">'
        f'<header class="slide-heading">{f"<h1>{title}</h1>" if title else ""}</header>'
        f'<div class="slide-content" data-layout="{_attr(layout)}" data-slot-count="{slot_count}" data-slot-columns="{slot_columns}">{"".join(slots)}</div>'
        '<p class="overflow-warning" aria-live="polite">글자를 줄여도 한 화면에 다 표시되지 않는 내용이 있습니다.</p>'
        + _render_notes(slide.get("notes", []))
        + "</div></section>"
    )


def render_presentation(result, *, no_toc=False, register_asset=None, diagnostics_out=None):
    """Render one complete presentation page from a PipelineResult."""
    if register_asset is None:
        register_asset = lambda path: "/assets/unavailable"
    slide_data = result.slide_data
    frontmatter = slide_data.get("frontmatter") or {}
    if not isinstance(frontmatter, dict):
        frontmatter = {}
    title_value = frontmatter.get("title") or Path(result.input_path).stem
    title = str(title_value)
    subtitle = str(frontmatter.get("subtitle") or "")
    author = str(frontmatter.get("author") or "")

    chapters = (slide_data.get("toc") or {}).get("chapters") or []
    include_toc = bool(chapters) and not no_toc
    body_offset = 1 + int(include_toc)
    body_slides = slide_data.get("slides") or []
    diagnostics = list(result.diagnostics)

    slides = [
        '<section id="slide-1" class="slide cover-slide" aria-label="Cover">'
        '<div class="cover-content">'
        f'<p class="eyebrow">발표 자료</p><h1>{_text(title)}</h1>'
        f'{f"<p class=\"subtitle\">{_text(subtitle)}</p>" if subtitle else ""}'
        f'{f"<p class=\"author\">{_text(author)}</p>" if author else ""}'
        '</div><p class="overflow-warning" aria-live="polite">표지 내용이 한 화면에 다 표시되지 않습니다.</p></section>'
    ]

    if include_toc:
        toc_items = []
        for chapter in chapters:
            chapter_index = chapter.get("index")
            target = body_offset + chapter_index if isinstance(chapter_index, int) else None
            if target is not None and 0 <= chapter_index < len(body_slides):
                toc_items.append(
                    f'<li><a href="#/slide-{target + 1}">{_text(chapter.get("title", ""))}</a>'
                )
                modules = []
                for module in chapter.get("modules", []):
                    module_index = module.get("index")
                    if isinstance(module_index, int) and 0 <= module_index < len(body_slides):
                        modules.append(
                            f'<li><a href="#/slide-{body_offset + module_index + 1}">{_text(module.get("title", ""))}</a></li>'
                        )
                if modules:
                    toc_items.append("<ul>" + "".join(modules) + "</ul>")
                toc_items.append("</li>")
        slides.append(
            '<section id="slide-2" class="slide toc-slide" aria-label="Contents">'
            '<div class="toc-content"><h1>목차</h1>'
            '<nav aria-label="Table of contents"><ul class="toc-list">'
            + "".join(toc_items)
            + '</ul></nav><p class="overflow-warning" aria-live="polite">목차가 한 화면에 다 표시되지 않습니다.</p></div></section>'
        )

    for index, slide in enumerate(body_slides):
        slides.append(
            _render_body_slide(
                slide,
                index,
                body_offset + index,
                result.input_path,
                register_asset,
                diagnostics,
            )
        )

    unique_diagnostics = list(dict.fromkeys(diagnostics))
    warning_list = "".join(f"<li>{_text(message)}</li>" for message in unique_diagnostics)
    if diagnostics_out is not None:
        diagnostics_out.extend(unique_diagnostics)
    warnings_html = (
        f'<details class="diagnostics"><summary>문서 점검 · {len(unique_diagnostics)}건</summary><ul>{warning_list}</ul></details>'
        if warning_list
        else '<details class="diagnostics" hidden></details>'
    )
    escaped_title = _text(title)
    return (
        "<!doctype html><html lang=\"ko\"><head><meta charset=\"utf-8\">"
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{escaped_title}</title>"
        '<link rel="stylesheet" href="/assets/vendor/reveal/dist/reveal.css">'
        '<link rel="stylesheet" href="/assets/theme.css">'
        "</head><body>"
        '<main id="presentation" aria-label="Presentation">'
        '<div id="reveal" class="reveal"><div class="slides">'
        + "".join(slides)
        + "</div>"
        '<nav class="presentation-tools" aria-label="발표 도구">'
        '<button id="fullscreen" type="button">전체 화면</button>'
        '<button id="speaker-view" type="button">발표자 화면</button>'
        "</nav>"
        '<p id="player-status" class="sr-only" aria-live="polite"></p>'
        "</div>"
        + warnings_html
        + "</main>"
        '<script src="/assets/vendor/reveal/dist/reveal.js" defer></script>'
        '<script src="/assets/vendor/reveal/dist/plugin/notes.js" defer></script>'
        '<script src="/assets/player.js" defer></script></body></html>'
    )

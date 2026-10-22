"""Shared Markdown-to-slide-JSON pipeline used by PPTX and web output."""

from dataclasses import dataclass
import json
import os

from flatten import flatten_markdown
from json2slide import process_json
from md2json import process_markdown


@dataclass
class PipelineResult:
    input_path: str
    flattened_markdown: str
    markdown_data: dict
    slide_data: dict
    diagnostics: list[str]


def _save_debug_data(data, filename):
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as output:
        if isinstance(data, str):
            output.write(data)
        else:
            json.dump(data, output, ensure_ascii=False, indent=4)
    print(f"Debug data saved to {filename}")


def build_slide_data(input_path, *, debug=False, debug_dir="debug", verbose=False):
    """Flatten and parse an input document into the shared slide JSON format."""
    input_path = os.path.abspath(os.fspath(input_path))
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input Markdown file not found: {input_path}")

    diagnostics = []
    if verbose:
        print(f"Flattening Markdown file: {input_path}")
    flattened = flatten_markdown(input_path, is_root=True, diagnostics=diagnostics)
    if debug:
        _save_debug_data(
            flattened,
            os.path.join(debug_dir, "0_flattened.md"),
        )

    if verbose:
        print("Converting Markdown to JSON...")
    markdown_data = process_markdown(flattened)
    if debug:
        _save_debug_data(
            markdown_data,
            os.path.join(debug_dir, "1_markdown_to_json.json"),
        )

    if verbose:
        print("Converting JSON to slide format...")
    slide_data = process_json(markdown_data)
    if debug:
        _save_debug_data(
            slide_data,
            os.path.join(debug_dir, "2_json_to_slide.json"),
        )

    return PipelineResult(
        input_path=input_path,
        flattened_markdown=flattened,
        markdown_data=markdown_data,
        slide_data=slide_data,
        diagnostics=diagnostics,
    )

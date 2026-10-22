#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from contextlib import nullcontext
import os
import sys

from json2pptx import main as json2pptx_main
from md2ppt.pipeline import build_slide_data
from md2ppt.templates import list_templates, template_path


def _pptx_main(argv=None):
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to PowerPoint presentations.",
        epilog="Run `md2ppt serve --help` for browser presentation options.",
    )
    parser.add_argument("-i", "--input", help="Input Markdown file path")
    parser.add_argument("-o", "--output", help="Output PPTX file path (default: {input_filename}.pptx)")
    parser.add_argument("-d", "--debug", action="store_true", help="Save intermediate processing results to files")
    parser.add_argument("--debug-dir", default="debug", help="Directory to save debug files (default: 'debug')")
    parser.add_argument("-t", "--template", default="default", help="Built-in template name (default: default)")
    parser.add_argument("--list-templates", action="store_true", help="List built-in templates and exit")
    parser.add_argument("-r", "--ref", help="Reference PPTX file path for styling. Overrides --template.")
    parser.add_argument("--no-toc", action="store_true", help="Skip generating the table of contents slide")
    args = parser.parse_args(argv)

    if args.list_templates:
        for template in list_templates():
            print(template)
        return 0

    if not args.input:
        parser.error("the following arguments are required: -i/--input")

    output_file = args.output or f"{os.path.splitext(args.input)[0]}.pptx"
    try:
        result = build_slide_data(
            args.input,
            debug=args.debug,
            debug_dir=args.debug_dir,
            verbose=True,
        )
        print("Converting slide format to PPTX...")
        ref_context = (
            nullcontext(os.path.abspath(args.ref))
            if args.ref
            else template_path(args.template)
        )
        with ref_context as ref_path:
            os.environ["JSON2PPTX_REF"] = str(ref_path) if ref_path else ""
            os.environ["JSON2PPTX_OUTPUT"] = output_file
            os.environ["JSON2PPTX_RETURN_PPTX"] = "1"
            os.environ["JSON2PPTX_TOC"] = "0" if args.no_toc else "1"
            pptx_obj = json2pptx_main(data=result.slide_data)
            print(f"Saving PPTX file: {output_file}")
            pptx_obj.save(output_file)
        print(f"Successfully converted {args.input} to {output_file}")
        return 0
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] == "serve":
        from md2ppt.web.server import serve_main

        return serve_main(args[1:])
    return _pptx_main(args)


if __name__ == "__main__":
    sys.exit(main())

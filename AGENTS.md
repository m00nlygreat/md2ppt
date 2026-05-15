# Agent Notes

## Packaging Templates

- Built-in PowerPoint templates should live inside the Python project package, not as loose root-level files.
- Include bundled templates as package data, for example `refs/*.pptx` under the package directory.
- Users should not need to know installed package paths. Expose built-in templates by name through CLI options such as `--template default` and `--list-templates`.
- Keep `--ref` for explicit user-provided `.pptx` template paths outside the package.
- If the code is moved under an `md2ppt/` package directory, update the console script entry point to `md2ppt.main:main`.

from contextlib import contextmanager
from importlib.resources import as_file, files


TEMPLATE_EXTENSION = ".pptx"
TEMPLATE_DIR = "refs"


def _templates_dir():
    return files("md2ppt").joinpath(TEMPLATE_DIR)


def list_templates():
    return sorted(
        resource.name.removesuffix(TEMPLATE_EXTENSION)
        for resource in _templates_dir().iterdir()
        if resource.is_file() and resource.name.endswith(TEMPLATE_EXTENSION)
    )


def template_resource(name):
    template_name = name.removesuffix(TEMPLATE_EXTENSION)
    templates = list_templates()
    if template_name not in templates:
        available = ", ".join(templates) or "none"
        raise ValueError(f"Unknown template '{name}'. Available templates: {available}")
    return _templates_dir().joinpath(f"{template_name}{TEMPLATE_EXTENSION}")


@contextmanager
def template_path(name):
    with as_file(template_resource(name)) as path:
        yield path

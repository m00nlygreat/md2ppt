"""Setuptools build hook for the canonical root-level default theme."""

from pathlib import Path

from setuptools.command.build_py import build_py

PROJECT_ROOT = Path(__file__).resolve().parent


class BuildPyWithDefaultTheme(build_py):
    """Copy styles/default.css into the importable md2ppt package resource."""

    def run(self):
        super().run()
        source = PROJECT_ROOT / "styles" / "default.css"
        if not source.is_file():
            raise FileNotFoundError(f"Built-in theme source was not found: {source}")
        destination = Path(self.build_lib) / "md2ppt" / "styles" / "default.css"
        self.mkpath(str(destination.parent))
        self.copy_file(str(source), str(destination))

    def get_outputs(self, include_bytecode=1):
        outputs = super().get_outputs(include_bytecode)
        theme_output = str(Path(self.build_lib) / "md2ppt" / "styles" / "default.css")
        if theme_output not in outputs:
            outputs.append(theme_output)
        return outputs

"""Threaded local HTTP server for browser-based presentations."""

import argparse
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import mimetypes
import os
from pathlib import Path
import re
import socket
import sys
from threading import RLock
from urllib.parse import urlsplit
from importlib.resources import files

from md2ppt.pipeline import build_slide_data
from .render import render_presentation


_ASSET_ID = re.compile(r"^[0-9a-f]{64}$")
_REVEAL_RESOURCES = {
    "/assets/vendor/reveal/dist/reveal.js": ("dist/reveal.js", "text/javascript; charset=utf-8"),
    "/assets/vendor/reveal/dist/reveal.css": ("dist/reveal.css", "text/css; charset=utf-8"),
    "/assets/vendor/reveal/dist/plugin/notes.js": (
        "dist/plugin/notes.js",
        "text/javascript; charset=utf-8",
    ),
}
_REVEAL_REQUIRED_FILES = (
    "dist/reveal.js",
    "dist/reveal.css",
    "dist/plugin/notes.js",
    "LICENSE",
    "metadata.json",
)
_NOTES_SCRIPT_CSP_HASH = "'sha256-GzCveToXhSIzS3M5eQeRm3McVRB7cYneYKwTkzA3wDk='"
_CSP_COMMON = (
    "default-src 'none'; img-src 'self' http: https:; style-src 'self' 'unsafe-inline'; "
    "font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; "
)
_CSP = _CSP_COMMON + "script-src 'self'; frame-src 'none'; frame-ancestors 'none'"
_PRESENTATION_CSP = (
    _CSP_COMMON
    + f"script-src 'self' {_NOTES_SCRIPT_CSP_HASH}; frame-src 'self'; frame-ancestors 'self'"
)


def _reveal_resource(relative_path):
    return files("md2ppt.web").joinpath(
        "assets", "vendor", "reveal", *relative_path.split("/")
    )


def _verify_reveal_resources():
    missing = []
    for relative_path in _REVEAL_REQUIRED_FILES:
        resource = _reveal_resource(relative_path)
        try:
            exists = resource.is_file()
        except (OSError, TypeError):
            exists = False
        if not exists:
            missing.append(f"{relative_path} ({resource})")
    if missing:
        required = ", ".join(missing)
        raise FileNotFoundError(
            "Reveal.js 6.0.2 packaged resources are missing: "
            f"{required}. Reinstall md2ppt with its complete package data."
        )


def _default_theme_reference():
    source_path = Path(__file__).resolve().parents[2] / "styles" / "default.css"
    if source_path.is_file():
        return source_path
    return Path(__file__).resolve().parent.parent / "styles" / "default.css"


def _read_default_theme():
    resource = files("md2ppt").joinpath("styles", "default.css")
    try:
        return resource.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        source_path = Path(__file__).resolve().parents[2] / "styles" / "default.css"
        try:
            return source_path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as error:
            raise OSError(f"기본 테마 CSS를 읽을 수 없습니다 ({source_path}): {error}") from error


def _resolve_theme_path(theme):
    requested = Path(os.path.expanduser(os.fspath(theme)))
    try:
        path = requested.resolve()
    except (OSError, RuntimeError) as error:
        raise OSError(f"테마 경로를 확인할 수 없습니다 ({requested}): {error}") from error
    if not path.exists():
        raise FileNotFoundError(f"테마 CSS 파일이 없습니다: {path}")
    if path.is_dir():
        raise IsADirectoryError(f"테마 경로가 디렉터리입니다: {path}")
    if path.suffix.lower() != ".css":
        raise ValueError(f"테마 파일은 .css 확장자여야 합니다: {path}")
    if not path.is_file():
        raise ValueError(f"테마 경로가 일반 파일이 아닙니다: {path}")
    try:
        path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        raise OSError(f"테마 CSS를 읽을 수 없습니다 ({path}): {error}") from error
    return path


class PresentationHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False

    def __init__(self, address, input_path, no_toc=False, theme_path=None):
        self.input_path = os.path.abspath(os.fspath(input_path))
        self.no_toc = no_toc
        self.theme_path = _resolve_theme_path(theme_path) if theme_path is not None else None
        if self.theme_path is None:
            _read_default_theme()
        _verify_reveal_resources()
        self.asset_registry = {}
        self.asset_registry_lock = RLock()
        super().__init__(address, PresentationRequestHandler)


class PresentationRequestHandler(BaseHTTPRequestHandler):
    server_version = "md2ppt"
    sys_version = ""

    def log_message(self, format_string, *args):
        # Keep the terminal focused on useful warnings and startup information.
        return

    def _send(self, status, body, content_type, *, extra_headers=None, content_security_policy=_CSP):
        body = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", content_security_policy)
        if extra_headers:
            for name, value in extra_headers.items():
                self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def _error_page(self, message):
        import html

        escaped = html.escape(str(message))
        return (
            "<!doctype html><html lang=\"ko\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>md2ppt 문서 오류</title>"
            "<link rel=\"stylesheet\" href=\"/assets/theme.css\"></head>"
            "<body class=\"error-page\">"
            "<h1>발표 자료를 표시할 수 없습니다</h1>"
            f"<pre class=\"error-details\">{escaped}</pre>"
            "<p>Markdown 원본을 수정한 뒤 페이지를 새로고침하세요.</p></body></html>"
        )

    def _serve_presentation(self):
        result = build_slide_data(self.server.input_path)
        asset_map = {}

        def register_asset(image_path):
            resolved = Path(image_path).resolve()
            asset_id = sha256(os.path.normcase(str(resolved)).encode("utf-8")).hexdigest()
            asset_map[asset_id] = resolved
            return f"/assets/{asset_id}"

        page = render_presentation(
            result,
            no_toc=self.server.no_toc,
            register_asset=register_asset,
        )
        with self.server.asset_registry_lock:
            self.server.asset_registry.update(asset_map)
        self._send(
            200,
            page,
            "text/html; charset=utf-8",
            content_security_policy=_PRESENTATION_CSP,
        )

    def _serve_asset(self, path):
        if path == "/assets/player.js":
            resource = files("md2ppt.web").joinpath("assets", "player.js")
            self._send(200, resource.read_bytes(), "text/javascript; charset=utf-8")
            return

        reveal_asset = _REVEAL_RESOURCES.get(path)
        if reveal_asset is not None:
            relative_path, content_type = reveal_asset
            resource = _reveal_resource(relative_path)
            try:
                body = resource.read_bytes()
            except OSError:
                self._send(404, "Not found", "text/plain; charset=utf-8")
                return
            self._send(200, body, content_type)
            return

        asset_id = path.removeprefix("/assets/")
        if not _ASSET_ID.fullmatch(asset_id):
            self._send(404, "Not found", "text/plain; charset=utf-8")
            return
        with self.server.asset_registry_lock:
            image_path = self.server.asset_registry.get(asset_id)
        if image_path is None or not image_path.is_file():
            self._send(404, "Not found", "text/plain; charset=utf-8")
            return
        try:
            body = image_path.read_bytes()
        except OSError:
            self._send(404, "Not found", "text/plain; charset=utf-8")
            return
        content_type = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
        self._send(200, body, content_type)

    def _serve_theme(self):
        theme_label = self.server.theme_path or _default_theme_reference()
        try:
            css = (
                self.server.theme_path.read_text(encoding="utf-8-sig")
                if self.server.theme_path is not None
                else _read_default_theme()
            )
        except (OSError, UnicodeError) as error:
            print(f"Error: Could not read theme CSS {theme_label}: {error}", file=sys.stderr, flush=True)
            self._send(500, "Could not read the selected theme CSS.", "text/plain; charset=utf-8")
            return
        self._send(200, css, "text/css; charset=utf-8")

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/":
            try:
                self._serve_presentation()
            except Exception as error:
                self._send(500, self._error_page(error), "text/html; charset=utf-8")
            return
        if path == "/assets/theme.css":
            self._serve_theme()
            return
        if path.startswith("/assets/"):
            self._serve_asset(path)
            return
        self._send(404, "Not found", "text/plain; charset=utf-8")


def _valid_port(value):
    try:
        port = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("port must be an integer") from error
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 1 and 65535")
    return port


def serve_main(argv=None):
    parser = argparse.ArgumentParser(description="Present a Markdown file in a local browser.")
    parser.add_argument("-i", "--input", required=True, help="Input Markdown file path")
    parser.add_argument("--host", default="127.0.0.1", help="Interface to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=_valid_port, default=3000, help="Port to use (default: 3000)")
    parser.add_argument("--no-toc", action="store_true", help="Skip the web table of contents slide")
    parser.add_argument(
        "--theme",
        help="Replace the built-in presentation theme with a complete local CSS file",
    )
    args = parser.parse_args(argv)

    input_path = os.path.abspath(args.input)
    try:
        _verify_reveal_resources()
        # Preflight makes bad input and embed cycles fail before the server starts.
        result = build_slide_data(input_path)
        server_class = PresentationHTTPServer
        if ":" in args.host:
            server_class = type(
                "IPv6PresentationHTTPServer",
                (PresentationHTTPServer,),
                {"address_family": socket.AF_INET6},
            )
        server = server_class(
            (args.host, args.port),
            input_path,
            no_toc=args.no_toc,
            theme_path=args.theme,
        )
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    render_diagnostics = []
    render_presentation(
        result,
        no_toc=args.no_toc,
        diagnostics_out=render_diagnostics,
    )
    for diagnostic in dict.fromkeys(render_diagnostics):
        print(f"Warning: {diagnostic}", file=sys.stderr)
    host, port = server.server_address[:2]
    display_host = f"[{host}]" if ":" in host else host
    print(f"Serving {input_path}", flush=True)
    print(f"Open http://{display_host}:{port}/ (press Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping web presentation server.")
    finally:
        server.server_close()
    return 0

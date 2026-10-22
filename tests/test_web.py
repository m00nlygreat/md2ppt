import re
from pathlib import Path
import contextlib
import io
import os
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.parse import quote, unquote
from urllib.request import urlopen

from flatten import FlattenCycleError
from md2ppt.pipeline import build_slide_data
from md2ppt.web.render import render_presentation
from md2ppt.web.server import PresentationHTTPServer, serve_main


class WebPresentationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="md2ppt-web-")
        self.root = Path(self.temp.name) / "강의 자료"
        self.root.mkdir()
        (self.root / "sub").mkdir()
        (self.root / "images").mkdir()
        (self.root / "images" / "테스트 파일.png").write_bytes(b"fake-png-data")
        (self.root / "images" / "벡터.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg"><text>svg</text></svg>',
            encoding="utf-8",
        )
        (self.root / "sub" / "하위 문서.md").write_text(
            "# 하위 내용\n\n하위 문서에 있는 이미지:\n\n![](../images/테스트 파일.png)\n",
            encoding="utf-8",
        )
        self.document = self.root / "발표 자료.md"
        self.document.write_text(
            """---
title: "<script>alert(1)</script> 보안 발표"
subtitle: 요약 부제
author: 발표자
---
# 첫 장

[note]: # (발표자 **비공개** [위험 링크](javascript:alert(1)) <script>alert(2)</script>)

본문 **굵게**, *기울임*, `코드`, [안전한 링크](https://example.com), [위험한 링크](javascript:alert(1)). `<img src=x onerror=alert(1)>`

![](images/테스트 파일.png)

![없는 이미지](images/없는 파일.png)

![벡터 이미지](images/벡터.svg)

![](sub/하위 문서.md)

![](sub/없는 문서.md)

***

# 둘째 장

[note]: # (두 번째 발표 노트)

[layout]: # (two_images)

| 항목 | 값 |
| --- | ---: |
| 한글 | 표 |

```python
print("안녕")
```

- 바깥 항목
  - 안쪽 항목
""",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_common_pipeline_flattens_nested_embed_and_tracks_missing_files(self):
        result = build_slide_data(self.document)
        self.assertEqual(Path(result.input_path), self.document.resolve())
        self.assertIn("images/테스트 파일.png", unquote(result.flattened_markdown))
        self.assertTrue(any("없는 파일.png" in item for item in result.diagnostics))
        self.assertTrue(any("없는 문서.md" in item for item in result.diagnostics))
        self.assertGreaterEqual(len(result.slide_data["slides"]), 2)
        self.assertIn(
            "two_images",
            [slide["layout"] for slide in result.slide_data["slides"]],
        )
        self.assertIn("하위 내용", result.flattened_markdown)

    def test_cycle_is_reported_as_an_error(self):
        (self.root / "a.md").write_text("![b](b.md)\n", encoding="utf-8")
        (self.root / "b.md").write_text("![a](a.md)\n", encoding="utf-8")
        with self.assertRaises(FlattenCycleError):
            build_slide_data(self.root / "a.md")

    def test_empty_slides_are_removed_but_explicit_layout_and_toc_index_survive(self):
        document = self.root / "빈 슬라이드.md"
        document.write_text(
            "# 시작\n\n본문\n\n---\n\n---\n\n[layout]: # (two_images)\n",
            encoding="utf-8",
        )
        result = build_slide_data(document)
        slides = result.slide_data["slides"]
        self.assertEqual(len(slides), 2)
        self.assertEqual(slides[1]["layout"], "two_images")
        self.assertFalse(any(slides[1]["placeholders"]))
        self.assertEqual(result.slide_data["toc"]["chapters"][0]["index"], 0)
        html = render_presentation(result)
        self.assertIn('id="slide-4" class="slide body-slide layout-two_images"', html)

    def test_renderer_escapes_text_and_rejects_dangerous_links(self):
        result = build_slide_data(self.document)
        html = render_presentation(result, no_toc=False)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertNotIn("<img src=x onerror=alert(1)>", html)
        self.assertIn("&lt;img src=x onerror=alert(1)&gt;", html)
        self.assertIn('href="https://example.com"', html)
        self.assertNotIn('href="javascript:', html)
        self.assertIn('href="#/slide-3"', html)
        self.assertIn("문서 점검", html)
        self.assertIn("class=\"code\"", html)
        self.assertIn("안쪽 항목", html)
        self.assertIn("<table>", html)
        self.assertIn('data-align="right"', html)
        self.assertNotIn(" style=", html)
        self.assertEqual(html.count('<aside class="notes">'), 2)
        self.assertIn("발표자 <strong>비공개</strong>", html)
        self.assertIn("&lt;script&gt;alert(2)&lt;/script&gt;", html)
        self.assertNotIn('href="javascript:', html)
        self.assertLess(html.index("발표자 <strong>비공개</strong>"), html.index("두 번째 발표 노트"))
        self.assertEqual(html.count('<section id="slide-'), 5)
        self.assertIn('<div id="reveal" class="reveal"', html)
        self.assertIn('<div class="slides">', html)
        self.assertNotIn('class="stage"', html)

    def test_no_toc_removes_contents_slide_and_remaps_body_position(self):
        result = build_slide_data(self.document)
        html = render_presentation(result, no_toc=True)
        self.assertNotIn('aria-label="Contents"', html)
        self.assertIn('id="slide-2" class="slide body-slide', html)

    def test_renderer_preserves_image_filename_characters_and_remote_urls(self):
        filenames = ("해시#파일.png", "공백%20파일.png", "사진%23파일.png")
        image_paths = [self.root / "images" / name for name in filenames]
        for path in image_paths:
            path.write_bytes(b"fake-png-data")
        remote_url = "https://example.com/image%23name%20space.png?x=a%26b&y=ok"
        self.document.write_text(
            "# 이미지\n\n"
            + "\n\n".join(f"![](images/{quote(name, safe='')})" for name in filenames)
            + f"\n\n![]({remote_url})\n",
            encoding="utf-8",
        )
        registered = []
        diagnostics = []
        html = render_presentation(
            build_slide_data(self.document),
            register_asset=lambda path: registered.append(path) or "/assets/test-image",
            diagnostics_out=diagnostics,
        )
        self.assertEqual(registered, image_paths)
        self.assertEqual(diagnostics, [])
        self.assertIn('src="' + remote_url.replace("&", "&amp;") + '"', html)

    def test_unknown_layout_uses_grid_and_preserves_each_placeholder(self):
        result = build_slide_data(self.document)
        slide = max(result.slide_data["slides"], key=lambda item: len(item["placeholders"]))
        expected_slots = len(slide["placeholders"])
        slide["layout"] = "future_custom_layout"
        slide["shapes"] = {"web-warning": {"runs": [{"text": "not rendered"}]}}
        diagnostics = []
        html = render_presentation(result, diagnostics_out=diagnostics)
        fallback = re.search(
            r'<section id="slide-\d+" class="slide body-slide layout-fallback".*?</section>',
            html,
            re.DOTALL,
        )
        self.assertIsNotNone(fallback)
        self.assertEqual(fallback.group(0).count('class="placeholder"'), expected_slots)
        self.assertIn("future_custom_layout", html)
        self.assertIn("이름 있는 도형을 지원하지 않습니다", html)
        self.assertTrue(any("future_custom_layout" in item for item in diagnostics))
        self.assertTrue(any("이름 있는 도형을 지원하지 않습니다" in item for item in diagnostics))

    def test_http_server_serves_only_registered_assets_and_bundled_files(self):
        server = PresentationHTTPServer(("127.0.0.1", 0), self.document)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_address[1]}"
        try:
            with urlopen(base + "/") as response:
                page = response.read().decode("utf-8")
                self.assertEqual(response.headers["Cache-Control"].split(",")[0], "no-store")
                csp = response.headers["Content-Security-Policy"]
                self.assertIn("frame-src 'self'", csp)
                self.assertIn("frame-ancestors 'self'", csp)
                self.assertIn("'sha256-GzCveToXhSIzS3M5eQeRm3McVRB7cYneYKwTkzA3wDk='", csp)
                script_policy = csp.split("script-src", 1)[1].split(";", 1)[0]
                self.assertNotIn("'unsafe-inline'", script_policy)
                self.assertNotIn("'unsafe-eval'", csp)
            self.document.write_text(
                self.document.read_text(encoding="utf-8").replace("# 첫 장", "# 새로 고친 장"),
                encoding="utf-8",
            )
            (self.root / "sub" / "하위 문서.md").write_text(
                "# 하위 내용 변경\n\n새 embed 내용\n\n![](../images/테스트 파일.png)\n",
                encoding="utf-8",
            )
            (self.root / "images" / "테스트 파일.png").write_bytes(b"updated-png-data")
            with urlopen(base + "/") as response:
                refreshed_page = response.read().decode("utf-8")
            self.assertIn("새로 고친 장", refreshed_page)
            self.assertIn("하위 내용 변경", refreshed_page)
            match = re.search(r'src="(/assets/[0-9a-f]{64})"', page)
            self.assertIsNotNone(match)
            with urlopen(base + match.group(1)) as response:
                self.assertEqual(response.headers["Content-Type"], "image/png")
                self.assertEqual(response.headers["Cache-Control"].split(",")[0], "no-store")
                self.assertEqual(response.read(), b"updated-png-data")
            with server.asset_registry_lock:
                svg_id = next(
                    asset_id
                    for asset_id, path in server.asset_registry.items()
                    if path.suffix.lower() == ".svg"
                )
            with urlopen(base + "/assets/" + svg_id) as response:
                self.assertEqual(response.headers["Content-Type"], "image/svg+xml")
                self.assertIn(b"<svg", response.read())
            with urlopen(base + "/assets/theme.css") as response:
                self.assertEqual(response.headers["Content-Type"], "text/css; charset=utf-8")
                self.assertIn(b"--stage-width: 1280px", response.read())
            with urlopen(base + "/assets/player.js") as response:
                player = response.read().decode("utf-8")
                self.assertIn("window.Reveal.initialize(config)", player)
                self.assertIn("scrollActivationWidth: null", player)
                self.assertNotIn('classList.toggle("active"', player)
                self.assertNotIn("--stage-scale", player)
            for path, content_type in (
                ("/assets/vendor/reveal/dist/reveal.js", "text/javascript; charset=utf-8"),
                ("/assets/vendor/reveal/dist/reveal.css", "text/css; charset=utf-8"),
                ("/assets/vendor/reveal/dist/plugin/notes.js", "text/javascript; charset=utf-8"),
            ):
                with urlopen(base + path) as response:
                    self.assertEqual(response.headers["Content-Type"], content_type)
                    self.assertGreater(int(response.headers["Content-Length"]), 1000)
                    asset_csp = response.headers["Content-Security-Policy"]
                    self.assertIn("script-src 'self'", asset_csp)
                    self.assertIn("frame-src 'none'", asset_csp)
                    self.assertNotIn("'sha256-", asset_csp)
            for path in (
                "/secret.txt",
                "/assets/../secret.txt",
                "/assets/" + "0" * 64,
                "/assets/vendor/reveal/metadata.json",
                "/assets/vendor/reveal/LICENSE",
            ):
                with self.assertRaises(HTTPError) as caught:
                    urlopen(base + path)
                self.assertEqual(caught.exception.code, 404)
                caught.exception.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

    def test_theme_file_uses_cwd_relative_unicode_path_and_reloads(self):
        theme_dir = Path(self.temp.name) / "별도 테마 폴더"
        theme_dir.mkdir()
        theme = theme_dir / "발표 테마.CSS"
        theme.write_text(":root { --accent: red; }", encoding="utf-8")
        old_cwd = Path.cwd()
        try:
            os.chdir(Path(self.temp.name))
            server = PresentationHTTPServer(
                ("127.0.0.1", 0), self.document, theme_path="별도 테마 폴더/발표 테마.CSS"
            )
        finally:
            os.chdir(old_cwd)

        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_address[1]}"
        try:
            with urlopen(base + "/assets/theme.css") as response:
                self.assertEqual(response.headers["Content-Type"], "text/css; charset=utf-8")
                self.assertEqual(response.headers["Cache-Control"].split(",")[0], "no-store")
                self.assertEqual(response.read().decode("utf-8"), ":root { --accent: red; }")
            theme.write_text(":root { --accent: blue; }", encoding="utf-8")
            with urlopen(base + "/assets/theme.css") as response:
                self.assertEqual(response.read().decode("utf-8"), ":root { --accent: blue; }")

            absolute_server = PresentationHTTPServer(
                ("127.0.0.1", 0), self.document, theme_path=theme.resolve()
            )
            absolute_thread = threading.Thread(target=absolute_server.serve_forever, daemon=True)
            absolute_thread.start()
            try:
                absolute_base = f"http://127.0.0.1:{absolute_server.server_address[1]}"
                with urlopen(absolute_base + "/assets/theme.css") as response:
                    self.assertEqual(response.read().decode("utf-8"), ":root { --accent: blue; }")
            finally:
                absolute_server.shutdown()
                absolute_server.server_close()
                absolute_thread.join(timeout=2)

            theme.unlink()
            error_log = io.StringIO()
            with contextlib.redirect_stderr(error_log):
                with self.assertRaises(HTTPError) as caught:
                    urlopen(base + "/assets/theme.css")
            self.assertEqual(caught.exception.code, 500)
            caught.exception.close()
            self.assertIn(str(theme.resolve()), error_log.getvalue())
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

    def test_invalid_theme_paths_fail_before_server_start(self):
        text_file = self.root / "theme.txt"
        text_file.write_text("body {}", encoding="utf-8")
        bad_utf8 = self.root / "bad.css"
        bad_utf8.write_bytes(b"\xff")
        cases = (
            (self.root / "missing.css", FileNotFoundError),
            (self.root, IsADirectoryError),
            (text_file, ValueError),
            (bad_utf8, OSError),
        )
        for theme_path, error_type in cases:
            with self.subTest(theme_path=theme_path):
                with self.assertRaises(error_type):
                    PresentationHTTPServer(
                        ("127.0.0.1", 0), self.document, theme_path=theme_path
                    )

        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            exit_code = serve_main(
                ["-i", str(self.document), "--theme", str(self.root / "missing.css")]
            )
        self.assertEqual(exit_code, 1)
        self.assertIn(str(self.root / "missing.css"), output.getvalue())

    def test_port_collision_is_reported_by_http_server_startup(self):
        first = PresentationHTTPServer(("127.0.0.1", 0), self.document)
        second = None
        try:
            with self.assertRaises(OSError):
                second = PresentationHTTPServer(
                    ("127.0.0.1", first.server_address[1]), self.document
                )
        finally:
            if second is not None:
                second.server_close()
            first.server_close()


if __name__ == "__main__":
    unittest.main()

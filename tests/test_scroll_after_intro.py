"""Real Chromium wheel + native touch regression suite.
Run: python3 -m pip install playwright && python3 -m playwright install chromium
     python3 tests/test_scroll_after_intro.py
Serves site/ itself; no external server or pytest plugin needed.
"""
import functools
import http.server
from pathlib import Path
import threading
import unittest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PATHS = ("natural", "skip", "click", "Escape", "any-key", "nointro", "reduced-motion",
         "already-played", "failsafe", "loading-skip", "image-failure", "storage-denied", "motion-change", "replay")

class ScrollAfterIntro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT / "site"))
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}/"
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.server.shutdown()
        cls.server.server_close()

    def assert_released(self, page):
        page.wait_for_function("!document.getElementById('intro') && !document.documentElement.classList.contains('intro-on')", polling=100)
        self.assertTrue(page.evaluate("!document.elementFromPoint(innerWidth/2,innerHeight/2)?.closest('#intro')"))
        self.assertGreater(page.evaluate("document.scrollingElement.scrollHeight"), 844)

    def test_volume_controls(self):
        for path in ("?nointro", "what-people-say/"):
            with self.subTest(page=path):
                context = self.browser.new_context(viewport={"width":390,"height":844}, has_touch=True,
                                                  is_mobile=True, reduced_motion="reduce")
                self.addCleanup(context.close)
                page = context.new_page()
                page.goto(self.url + path)
                wall = page.locator("[data-volume]")
                stage = wall.locator(".volume__stage")
                stage.scroll_into_view_if_needed()
                self.assertEqual(wall.locator(".volume__quote:not([hidden])").count(), 1)
                self.assertEqual(wall.locator("[data-volume-pause]").text_content().strip(), "Resume")
                first = stage.inner_text()
                stage.tap()
                self.assertNotEqual(stage.inner_text(), first)
                stage.focus()
                second = stage.inner_text()
                page.keyboard.press("ArrowRight")
                self.assertNotEqual(stage.inner_text(), second)
                wall.locator("[data-volume-pause]").click()
                self.assertEqual(wall.locator("[data-volume-pause]").get_attribute("aria-pressed"), "false")
                wall.locator("[data-volume-pause]").click()
                paused_quote = stage.inner_text()
                page.wait_for_timeout(5200)
                self.assertEqual(stage.inner_text(), paused_quote)
                self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 390)
                context.close()
        # Real five-second auto advance, then explicit pause/resume.
        context = self.browser.new_context(viewport={"width":1280,"height":900}, reduced_motion="no-preference")
        self.addCleanup(context.close)
        page = context.new_page()
        page.goto(self.url + "?nointro")
        wall = page.locator("[data-volume]")
        wall.scroll_into_view_if_needed()
        page.mouse.move(1, 1)
        first = wall.locator(".volume__count").inner_text()
        page.wait_for_function("document.querySelector('.volume__count').textContent !== " + repr(first), timeout=8000)
        wall.locator("[data-volume-pause]").click()
        paused_quote = wall.locator(".volume__stage").inner_text()
        page.wait_for_timeout(5200)
        self.assertEqual(wall.locator(".volume__stage").inner_text(), paused_quote)
        wall.locator("[data-volume-pause]").click()
        previous = wall.locator(".volume__count").inner_text()
        page.wait_for_function("document.querySelector('.volume__count').textContent !== " + repr(previous), timeout=8000)
        context.close()

    def test_every_exit(self):
        for route in PATHS:
            with self.subTest(route=route):
                context = self.browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True,
                                                  is_mobile=True, reduced_motion="reduce" if route == "reduced-motion" else "no-preference")
                self.addCleanup(context.close)
                page = context.new_page()
                if route == "already-played":
                    page.add_init_script("sessionStorage.setItem('wcIntroV2','1')")
                if route == "storage-denied":
                    page.add_init_script("Object.defineProperty(window, 'sessionStorage', {get(){throw Error('denied')}})")
                if route == "failsafe":
                    # Freeze animation callbacks only: the real 6.5s guard must release the lock.
                    page.add_init_script("window.requestAnimationFrame = () => 1; window.cancelAnimationFrame = () => {}")
                if route == "loading-skip":
                    page.add_init_script("HTMLImageElement.prototype.decode = () => new Promise(() => {})")
                if route == "image-failure":
                    page.route("**/img/niki-brand.webp", lambda request: request.abort())
                page.goto(self.url + ("?nointro" if route == "nointro" else ""))
                if route in ("skip", "click", "Escape", "any-key", "motion-change", "failsafe", "storage-denied"):
                    page.wait_for_selector("html.intro-on")
                if route == "skip":
                    page.locator(".i-skip").click()
                elif route == "click":
                    page.mouse.click(195, 422)
                elif route in ("Escape", "any-key", "loading-skip"):
                    page.keyboard.press("Escape" if route != "any-key" else "a")
                elif route == "motion-change":
                    page.emulate_media(reduced_motion="reduce")
                elif route == "replay":
                    self.assert_released(page)
                    page.evaluate("window.wcReplay()")
                    page.wait_for_selector("html.intro-on")
                    page.keyboard.press("Escape")
                self.assert_released(page)
                page.evaluate("scrollTo(0,0)")
                page.mouse.move(195, 422)
                start = page.evaluate("scrollY")
                page.mouse.wheel(0, 650)
                page.wait_for_function("scrollY > 0", polling=100)
                self.assertGreater(page.evaluate("scrollY"), start, route + " wheel")
                page.evaluate("scrollTo(0,0)")
                page.wait_for_function("scrollY === 0")
                cdp = context.new_cdp_session(page)
                cdp.send("Input.dispatchTouchEvent", {"type":"touchStart", "touchPoints":[{"x":195,"y":680}]})
                for y in range(640, 199, -40):
                    cdp.send("Input.dispatchTouchEvent", {"type":"touchMove", "touchPoints":[{"x":195,"y":y}]})
                    page.wait_for_timeout(20)
                cdp.send("Input.dispatchTouchEvent", {"type":"touchEnd", "touchPoints":[]})
                page.wait_for_function("scrollY > 0", polling=100)
                self.assertGreater(page.evaluate("scrollY"), 0, route + " swipe")
                self.assert_released(page)
                context.close()

if __name__ == "__main__":
    unittest.main()

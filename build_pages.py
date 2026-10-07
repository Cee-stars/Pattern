"""Build the standalone app (GitHub Pages).

app.html is written for claude.ai artifacts (no <!doctype>/<head>), so this
wraps it in a full document and adds what a home-screen / Dock app needs:
manifest, icons, and a small service worker for offline use.

Output goes both to the repo root and to docs/, so the site works whether
GitHub Pages publishes from "/ (root)" or from "/docs".

Run after changing app.html, patterns.json or the icons:
    python3 build_pages.py
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
APP_NAME = "英語パターンノート"
SHORT_NAME = "パターン"
THEME = "#0b0b0c"

src = (ROOT / "app.html").read_text()
# everything before the first <style> (title, meta, font links) belongs in <head>
cut = src.index("<style>")
head_extra, body = src[:cut].strip(), src[cut:]

page = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{head_extra}
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="{SHORT_NAME}">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<style>
:root {{ padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }}
body {{ margin: 0; }}
img {{ max-width: 100%; }}
[hidden] {{ display: none !important; }}
</style>
</head>
<body>
{body}
<script>
if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(() => {{}});
</script>
</body>
</html>
"""

manifest = {
    "name": APP_NAME,
    "short_name": SHORT_NAME,
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "background_color": THEME,
    "theme_color": THEME,
    "lang": "ja",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}

# network first so updates show up right away; the cache is only for offline
sw = """const CACHE = "pattern-v1";
self.addEventListener("install", e => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  e.respondWith(
    fetch(req).then(res => {
      if (res.ok && (new URL(req.url).origin === location.origin || req.url.startsWith("https://fonts."))) {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy));
      }
      return res;
    }).catch(() => caches.match(req))
  );
});
"""

for out in (ROOT, DOCS):
    (out / "icons").mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page)
    (out / "manifest.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    (out / "sw.js").write_text(sw)
    (out / ".nojekyll").write_text("")
shutil.copy(ROOT / "patterns.json", DOCS / "patterns.json")
for name in ["apple-touch-icon.png", "icon-192.png", "icon-512.png", "icon-1024.png"]:
    shutil.copy(ROOT / "icons" / name, DOCS / "icons" / name)
print("built index.html and docs/")

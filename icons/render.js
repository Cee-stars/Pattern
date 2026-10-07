// Render the icon SVGs to PNGs with the preinstalled Chromium.
// Usage: node icons/render.js
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const dir = __dirname;
const jobs = [
  ["icon.svg", "icon-1024.png", 1024],        // macOS Dock / preview
  ["icon-full.svg", "icon-512.png", 512],     // PWA
  ["icon-full.svg", "icon-192.png", 192],     // PWA
  ["icon-full.svg", "apple-touch-icon.png", 180], // iPhone / iPad home screen
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const [src, out, size] of jobs) {
    const svg = fs.readFileSync(path.join(dir, src), "utf8");
    await page.setViewportSize({ width: size, height: size });
    await page.setContent(
      `<style>html,body{margin:0;background:transparent}svg{width:${size}px;height:${size}px;display:block}</style>${svg}`
    );
    await page.screenshot({ path: path.join(dir, out), omitBackground: true });
    console.log("wrote", out);
  }
  await browser.close();
})();

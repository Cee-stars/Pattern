"""Generate the app icon: a front-facing compass dial on a light tile.

Run:  python3 icons/make_icon.py   -> writes icons/icon.svg (rounded, for Dock)
                                      and icons/icon-full.svg (full-bleed, for iOS)
Then render PNGs with:  node icons/render.js
"""
import math
from pathlib import Path

OUT = Path(__file__).parent
C = 512        # centre
R = 330        # dial radius (full-bleed size)
NEEDLE_DEG = 38


def ticks():
    out = []
    for i in range(48):
        a = math.radians(i * 7.5)
        major = i % 12 == 0
        mid = i % 6 == 0
        r1 = R - (78 if major else 62 if mid else 48)
        r2 = R - 26
        w = 12 if major else 9 if mid else 6
        op = 1 if (major or mid) else 0.75
        x1, y1 = C + r1 * math.sin(a), C - r1 * math.cos(a)
        x2, y2 = C + r2 * math.sin(a), C - r2 * math.cos(a)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                   f'stroke="#ffffff" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round"/>')
    return "\n    ".join(out)


def svg(full_bleed: bool) -> str:
    if full_bleed:
        tile = '<rect width="1024" height="1024" fill="url(#tile)"/>'
        scale = 1.0
    else:
        tile = ('<rect x="100" y="114" width="824" height="824" rx="186" fill="#000" opacity="0.22" filter="url(#tileShadow)"/>'
                '<rect x="100" y="100" width="824" height="824" rx="186" fill="url(#tile)"/>'
                '<rect x="101" y="101" width="822" height="822" rx="185" fill="none" stroke="#000" stroke-opacity="0.06" stroke-width="2"/>')
        scale = 0.8
    L, W = 250, 46  # needle half-length and half-width
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <linearGradient id="tile" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#e6ecec"/>
    </linearGradient>
    <linearGradient id="dial" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#3cc0c4"/>
      <stop offset="1" stop-color="#11707c"/>
    </linearGradient>
    <radialGradient id="dialShine" cx="0.5" cy="0.15" r="0.75">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="ring" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#cfd9da"/>
    </linearGradient>
    <filter id="tileShadow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="18"/></filter>
    <filter id="dialShadow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
    <filter id="needleShadow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>
  </defs>

  {tile}
  <g transform="translate({C} {C}) scale({scale}) translate({-C} {-C})">
    <!-- dial sits slightly above the tile -->
    <circle cx="{C}" cy="{C + 14}" r="{R + 8}" fill="#0b3c42" opacity="0.30" filter="url(#dialShadow)"/>
    <circle cx="{C}" cy="{C}" r="{R + 10}" fill="url(#ring)"/>
    <circle cx="{C}" cy="{C}" r="{R}" fill="url(#dial)"/>
    <circle cx="{C}" cy="{C}" r="{R}" fill="url(#dialShine)"/>
    {ticks()}

    <!-- needle floats above the dial -->
    <g transform="translate({C + 10} {C + 18}) rotate({NEEDLE_DEG})" opacity="0.35" filter="url(#needleShadow)">
      <polygon points="0,{-L} {W},0 0,{L} {-W},0" fill="#05282d"/>
    </g>
    <g transform="translate({C} {C}) rotate({NEEDLE_DEG})">
      <polygon points="0,{-L} {-W},0 0,0" fill="#ff5a4a"/>
      <polygon points="0,{-L} {W},0 0,0" fill="#d8352a"/>
      <polygon points="0,{L} {-W},0 0,0" fill="#ffffff"/>
      <polygon points="0,{L} {W},0 0,0" fill="#dfe6e7"/>
    </g>
    <circle cx="{C}" cy="{C}" r="20" fill="#ffffff"/>
    <circle cx="{C}" cy="{C}" r="11" fill="#d8352a"/>
  </g>
</svg>
'''


(OUT / "icon.svg").write_text(svg(full_bleed=False))
(OUT / "icon-full.svg").write_text(svg(full_bleed=True))
print("wrote icon.svg, icon-full.svg")

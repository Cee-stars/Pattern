"""Generate the app icon.

Mixes three ideas: a black tile with a folded red ribbon (shading where the
strip bends), a thin red ring with serif lettering, and a compass dial with
tick marks and a two-colour needle.

Run:  python3 icons/make_icon.py   -> writes icons/icon.svg (rounded, for Dock)
                                      and icons/icon-full.svg (full-bleed, for iOS)
Then render PNGs with:  node icons/render.js
"""
import math
from pathlib import Path

OUT = Path(__file__).parent
C = 512          # centre
R = 360          # red ring radius (full-bleed size)
NEEDLE_DEG = 40


def ticks():
    out = []
    for i in range(48):
        if i % 12 == 0:
            continue  # the letters sit at N/E/S/W
        a = math.radians(i * 7.5)
        mid = i % 6 == 0
        r1 = R - (66 if mid else 52)
        r2 = R - 30
        w = 9 if mid else 5
        op = 0.95 if mid else 0.55
        x1, y1 = C + r1 * math.sin(a), C - r1 * math.cos(a)
        x2, y2 = C + r2 * math.sin(a), C - r2 * math.cos(a)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                   f'stroke="#ffffff" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round"/>')
    return "\n    ".join(out)


def letters():
    rr = R - 68
    font = "font-family=\"Georgia, 'DejaVu Serif', serif\" font-weight=\"700\" text-anchor=\"middle\" dominant-baseline=\"central\""
    return (f'<g {font}>'
            f'<text x="{C}" y="{C - rr}" font-size="74" fill="#e8322b">N</text>'
            f'<text x="{C + rr}" y="{C}" font-size="58" fill="#ffffff">E</text>'
            f'<text x="{C}" y="{C + rr}" font-size="58" fill="#ffffff">S</text>'
            f'<text x="{C - rr}" y="{C}" font-size="58" fill="#ffffff">W</text>'
            f'</g>')


def svg(full_bleed: bool) -> str:
    if full_bleed:
        tile = '<rect width="1024" height="1024" fill="url(#tile)"/>'
        scale = 0.98
    else:
        tile = ('<rect x="100" y="114" width="824" height="824" rx="186" fill="#000" opacity="0.35" filter="url(#tileShadow)"/>'
                '<rect x="100" y="100" width="824" height="824" rx="186" fill="url(#tile)"/>'
                '<rect x="101" y="101" width="822" height="822" rx="185" fill="none" stroke="#ffffff" stroke-opacity="0.08" stroke-width="2"/>')
        scale = 0.78
    L, W = 236, 50  # needle half-length and half-width
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <linearGradient id="tile" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1b1b1d"/>
      <stop offset="1" stop-color="#050506"/>
    </linearGradient>
    <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ff4a3d"/>
      <stop offset="1" stop-color="#b3140f"/>
    </linearGradient>
    <!-- ribbon fold: the red strip darkens toward the bend at the centre -->
    <linearGradient id="ribbonLit" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ff4136"/>
      <stop offset="0.75" stop-color="#e5251c"/>
      <stop offset="1" stop-color="#8f0d08"/>
    </linearGradient>
    <linearGradient id="ribbonDark" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#c1150e"/>
      <stop offset="0.7" stop-color="#9a0f0a"/>
      <stop offset="1" stop-color="#5c0805"/>
    </linearGradient>
    <linearGradient id="silverLit" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#bfc3c6"/>
    </linearGradient>
    <linearGradient id="silverDark" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0" stop-color="#cfd3d6"/>
      <stop offset="1" stop-color="#7d8387"/>
    </linearGradient>
    <filter id="tileShadow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="18"/></filter>
    <filter id="needleShadow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="10"/></filter>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="16"/></filter>
  </defs>

  {tile}
  <g transform="translate({C} {C}) scale({scale}) translate({-C} {-C})">
    <!-- red ring -->
    <circle cx="{C}" cy="{C}" r="{R}" fill="none" stroke="#e8322b" stroke-opacity="0.35" stroke-width="30" filter="url(#glow)"/>
    <circle cx="{C}" cy="{C}" r="{R}" fill="none" stroke="url(#ring)" stroke-width="26"/>

    {ticks()}
    {letters()}

    <!-- needle shadow -->
    <g transform="translate({C + 12} {C + 20}) rotate({NEEDLE_DEG})" opacity="0.7" filter="url(#needleShadow)">
      <polygon points="0,{-L} {W},0 0,{L} {-W},0" fill="#000"/>
    </g>
    <!-- needle: north half is a folded red ribbon, south half silver -->
    <g transform="translate({C} {C}) rotate({NEEDLE_DEG})">
      <polygon points="0,{-L} {-W},0 0,0" fill="url(#ribbonLit)"/>
      <polygon points="0,{-L} {W},0 0,0" fill="url(#ribbonDark)"/>
      <polygon points="0,{L} {-W},0 0,0" fill="url(#silverLit)"/>
      <polygon points="0,{L} {W},0 0,0" fill="url(#silverDark)"/>
    </g>
    <circle cx="{C}" cy="{C}" r="22" fill="#ffffff"/>
    <circle cx="{C}" cy="{C}" r="12" fill="#e8322b"/>
  </g>
</svg>
'''


(OUT / "icon.svg").write_text(svg(full_bleed=False))
(OUT / "icon-full.svg").write_text(svg(full_bleed=True))
print("wrote icon.svg, icon-full.svg")

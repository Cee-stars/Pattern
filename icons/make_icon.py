"""Generate the app icon (a tilted 3D compass) as SVG.

Run:  python3 icons/make_icon.py   -> writes icons/icon.svg (rounded, for Dock)
                                      and icons/icon-full.svg (full-bleed, for iOS)
Then render PNGs with:  node icons/render.js
"""
import math
from pathlib import Path

OUT = Path(__file__).parent

CX, CY = 512, 470      # centre of the compass top face
TILT = 0.80            # vertical squash = viewing angle
K = 1.23               # dial is drawn at r=244 and scaled up to fill the space
R = round(244 * K)     # dial radius
DIAL_DEPTH = 22        # thickness of the dial plate seen from the side


def ticks():
    out = []
    for i in range(72):
        a = math.radians(i * 5)
        if i % 18 == 0:
            r1, w, c = 168, 7, "url(#tickMajor)"
        elif i % 9 == 0:
            r1, w, c = 186, 5, "#2b3a40"
        elif i % 2 == 0:
            r1, w, c = 198, 3, "#3d4d53"
        else:
            r1, w, c = 204, 2, "#6b787c"
        r2 = 214
        x1, y1 = r1 * math.sin(a), -r1 * math.cos(a)
        x2, y2 = r2 * math.sin(a), -r2 * math.cos(a)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>')
    return "\n      ".join(out)


def rose():
    """Faint 8-point star printed on the dial."""
    pts = []
    for i in range(16):
        a = math.radians(i * 22.5)
        r = 150 if i % 4 == 0 else (95 if i % 2 == 0 else 38)
        pts.append(f"{r * math.sin(a):.1f},{-r * math.cos(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="#d9cfb6" opacity="0.55"/>'


def svg(full_bleed: bool) -> str:
    if full_bleed:
        bg = '<rect width="1024" height="1024" fill="url(#bg)"/>'
        bg_glow = '<rect width="1024" height="1024" fill="url(#bgGlow)"/>'
        clip_open, clip_close = "", ""
    else:
        bg = ('<rect x="100" y="112" width="824" height="824" rx="186" fill="#000" opacity="0.28" filter="url(#tileShadow)"/>'
              '<rect x="100" y="100" width="824" height="824" rx="186" fill="url(#bg)"/>')
        bg_glow = '<rect x="100" y="100" width="824" height="824" rx="186" fill="url(#bgGlow)"/>'
        clip_open = '<g clip-path="url(#tile)">'
        clip_close = "</g>"
        # macOS grid: shrink the compass into the tile
    scale = 0.9 if full_bleed else 0.80
    ry = R * TILT

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2a8c95"/>
      <stop offset="1" stop-color="#0e3b45"/>
    </linearGradient>
    <radialGradient id="bgGlow" cx="0.5" cy="0.3" r="0.7">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="tile"><rect x="100" y="100" width="824" height="824" rx="186"/></clipPath>
    <filter id="tileShadow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="18"/></filter>
    <filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="22"/></filter>
    <filter id="needleShadow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7"/></filter>

    <!-- brass case side: dark at the edges, bright where the light hits -->
    <linearGradient id="side" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#5a3d12"/>
      <stop offset="0.22" stop-color="#b98a3a"/>
      <stop offset="0.38" stop-color="#f2d58c"/>
      <stop offset="0.55" stop-color="#a87a2c"/>
      <stop offset="1" stop-color="#4a3210"/>
    </linearGradient>
    <linearGradient id="plateSide" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8f8466"/>
      <stop offset="0.35" stop-color="#e4dbc2"/>
      <stop offset="0.6" stop-color="#b8ad8f"/>
      <stop offset="1" stop-color="#6f6650"/>
    </linearGradient>
    <!-- brass top rim -->
    <linearGradient id="rim" x1="0.15" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="#fff1c2"/>
      <stop offset="0.3" stop-color="#e2b660"/>
      <stop offset="0.65" stop-color="#a6772a"/>
      <stop offset="1" stop-color="#6b4815"/>
    </linearGradient>
    <linearGradient id="rimInner" x1="0.85" y1="1" x2="0.15" y2="0">
      <stop offset="0" stop-color="#ffe9a8"/>
      <stop offset="0.5" stop-color="#c49340"/>
      <stop offset="1" stop-color="#5e3f12"/>
    </linearGradient>
    <!-- recessed dial: darker near the top wall (shadow cast by the rim) -->
    <radialGradient id="dial" cx="0.5" cy="0.6" r="0.6">
      <stop offset="0" stop-color="#fbf6e8"/>
      <stop offset="0.75" stop-color="#efe6cf"/>
      <stop offset="1" stop-color="#c9bb98"/>
    </radialGradient>
    <linearGradient id="dialWall" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#000" stop-opacity="0.38"/>
      <stop offset="0.35" stop-color="#000" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="tickMajor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#c0392b"/><stop offset="1" stop-color="#8e2318"/>
    </linearGradient>
    <!-- glass dome -->
    <radialGradient id="glass" cx="0.35" cy="0.25" r="0.75">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.55"/>
      <stop offset="0.35" stop-color="#ffffff" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="cap" cx="0.35" cy="0.3" r="0.8">
      <stop offset="0" stop-color="#fff6d6"/>
      <stop offset="0.45" stop-color="#d9a84e"/>
      <stop offset="1" stop-color="#5e3f12"/>
    </radialGradient>
  </defs>

  {bg}
  {bg_glow}
  {clip_open}
  <g transform="translate({CX} {CY + (45 if full_bleed else 30)}) scale({scale}) translate({-CX} {-CY})">
    <!-- shadow on the ground -->
    <ellipse cx="{CX}" cy="{CY + DIAL_DEPTH + ry * 0.9}" rx="{R * 0.95}" ry="{ry * 0.38}" fill="#021b20" opacity="0.55" filter="url(#soft)"/>

    <!-- the dial plate's own thickness (no metal case) -->
    <path d="M {CX - R} {CY} L {CX - R} {CY + DIAL_DEPTH} A {R} {ry} 0 0 0 {CX + R} {CY + DIAL_DEPTH} L {CX + R} {CY} Z" fill="url(#plateSide)"/>

    <!-- everything on the top face, drawn as a circle then tilted -->
    <g transform="translate({CX} {CY}) scale(1 {TILT})">
     <g transform="scale({K})">
      <circle r="244" fill="url(#dial)"/>
      <circle r="243" fill="none" stroke="#fffdf4" stroke-width="2" opacity="0.8"/>
      {rose()}
      <g>
      {ticks()}
      </g>
      <g font-family="Georgia, 'DejaVu Serif', serif" font-weight="700" text-anchor="middle" dominant-baseline="central">
        <text x="0" y="-128" font-size="62" fill="#b8301f">N</text>
        <text x="128" y="0" font-size="50" fill="#26353b">E</text>
        <text x="0" y="128" font-size="50" fill="#26353b">S</text>
        <text x="-128" y="0" font-size="50" fill="#26353b">W</text>
      </g>

      <!-- needle shadow cast on the dial (needle floats above it) -->
      <g transform="translate(16 22) rotate(32)" opacity="0.32" filter="url(#needleShadow)">
        <polygon points="0,-178 26,0 0,178 -26,0" fill="#000"/>
      </g>

      <!-- needle: each half has a lit face and a shaded face -->
      <g transform="rotate(32)">
        <polygon points="0,-180 -28,0 0,0" fill="#ef5a45"/>
        <polygon points="0,-180 28,0 0,0" fill="#a3241a"/>
        <polygon points="0,180 -28,0 0,0" fill="#f4f6f6"/>
        <polygon points="0,180 28,0 0,0" fill="#9aa5aa"/>
        <line x1="0" y1="-180" x2="0" y2="180" stroke="#000" stroke-opacity="0.15" stroke-width="1.5"/>
      </g>
      <circle r="30" fill="#3a2709" opacity="0.35" transform="translate(4 6)"/>
      <circle r="28" fill="url(#cap)"/>
      <circle r="9" cx="-8" cy="-9" fill="#fffbe9" opacity="0.8"/>

      <!-- glass highlight -->
      <circle r="244" fill="url(#glass)"/>
      <path d="M -200 -110 A 230 230 0 0 1 60 -226 A 260 260 0 0 0 -170 -60 Z" fill="#ffffff" opacity="0.35"/>
     </g>
    </g>
  </g>
  {clip_close}
</svg>
'''


(OUT / "icon.svg").write_text(svg(full_bleed=False))
(OUT / "icon-full.svg").write_text(svg(full_bleed=True))
print("wrote icon.svg, icon-full.svg")

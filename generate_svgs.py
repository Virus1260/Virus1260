"""
generate_svgs.py
================
Generates THREE custom animated SVGs for Shekhar Mishra (@Virus1260):

1. github-contribution-animation.svg (850 × 165)
   • Diagonal slanted wave reveal with bright glowing glints
   • Custom Industrial Reactor Palette: Gold (#f59e0b), Emerald (#10b981), Cyber Blue (#38bdf8)

2. terminal-card.svg (840 × 875)
   • GitHub avatar rendered as high-precision ASCII art
   • Animated left→right typewriter sweep line-by-line with amber cursor
   • macOS terminal chrome: Virus1260@heavy-eng: ~$ ./render_shekhar_portrait.sh

3. info-card.svg (500 × 522)
   • Neofetch-style system card for heavy mechanical design & automation
   • Animated staggered slide-up with custom specs, scale (16,930T), codes, and impact

Run:
    python generate_svgs.py
"""

import sys, os, random, html as _html
from urllib.request import urlopen, Request
from io import BytesIO
from PIL import Image

def xe(s): return _html.escape(str(s), quote=True)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ==============================================================================
# 1. github-contribution-animation.svg (Gold & Emerald Industrial Theme)
# ==============================================================================
def build_contrib():
    random.seed(1260)
    COLORS = ["#161b22", "#1e3a24", "#006d32", "#c59b27", "#f59e0b"]
    GLOW   = ["#21262d", "#34d399", "#10b981", "#fbbf24", "#fef08a"]

    def pick_level():
        r = random.random()
        if r < 0.30: return 0
        if r < 0.50: return 1
        if r < 0.68: return 2
        if r < 0.85: return 3
        return 4

    WEEKS   = 53
    DAYS    = 7
    SQ      = 11
    GAP     = 3
    STEP    = SQ + GAP   # 14
    GRAPH_X = 34
    GRAPH_Y = 28
    MONTHS  = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    W, H = 850, 165
    lines = []

    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    lines.append('<defs>')
    lines.append(
        '<filter id="cellglow" x="-70%" y="-70%" width="240%" height="240%">'
        '<feGaussianBlur stdDeviation="2.5" result="blur"/>'
        '<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>'
        '</filter>'
    )
    lines.append(
        '<linearGradient id="headerGlow" x1="0%" y1="0%" x2="100%" y2="0%">'
        '<stop offset="0%" stop-color="#f59e0b" stop-opacity="0.8"/>'
        '<stop offset="50%" stop-color="#10b981" stop-opacity="0.6"/>'
        '<stop offset="100%" stop-color="#38bdf8" stop-opacity="0.8"/>'
        '</linearGradient>'
    )
    lines.append('</defs>')

    lines.append(f'<rect width="{W}" height="{H}" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="1"/>')
    lines.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="url(#headerGlow)" stroke-width="1" stroke-opacity="0.4"/>')

    wpm = WEEKS / 12
    for i, m in enumerate(MONTHS):
        x = GRAPH_X + round(i * wpm) * STEP
        lines.append(f'<text x="{x}" y="18" fill="#8b949e" font-size="10" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">{m}</text>')

    for i, lbl in enumerate(["Mon","","Wed","","Fri","",""]):
        if lbl:
            y = GRAPH_Y + i * STEP + SQ - 1
            lines.append(f'<text x="6" y="{y}" fill="#8b949e" font-size="9" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">{lbl}</text>')

    anim_dur = 4.5
    pause    = 2.5
    total    = anim_dur + pause

    SLANT    = 0.6
    max_diag = (WEEKS - 1) + (DAYS - 1) * SLANT

    for col in range(WEEKS):
        for row in range(DAYS):
            lvl   = pick_level()
            color = COLORS[lvl]
            glow  = GLOW[lvl]
            x     = GRAPH_X + col * STEP
            y     = GRAPH_Y + row * STEP
            sq_id = f"s{col}_{row}"

            diag  = col + row * SLANT
            t_rev = diag / max_diag * anim_dur

            t0 = t_rev / total
            t1 = min(t0 + 0.015, 0.97)
            t2 = min(t0 + 0.055, 0.99)

            fa = ' filter="url(#cellglow)"' if lvl >= 3 else ''

            lines.append(
                f'<rect id="{sq_id}" x="{x}" y="{y}" width="{SQ}" height="{SQ}" rx="2.5" fill="{color}" opacity="0"{fa}>'
            )
            lines.append(
                f'<animate attributeName="opacity" values="0;0;1;1" '
                f'keyTimes="0;{t0:.4f};{t1:.4f};1" '
                f'dur="{total}s" repeatCount="indefinite"/>'
            )
            if lvl > 0:
                lines.append(
                    f'<animate attributeName="fill" values="{color};{color};{glow};{color};{color}" '
                    f'keyTimes="0;{t0:.4f};{t1:.4f};{t2:.4f};1" '
                    f'dur="{total}s" repeatCount="indefinite"/>'
                )
            lines.append('</rect>')

    lines.append('</svg>')

    out_path = os.path.join(OUT_DIR, "github-contribution-animation.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] github-contribution-animation.svg created ({os.path.getsize(out_path)//1024} KB)")


# ==============================================================================
# 2. terminal-card.svg (ASCII Art Portrait with Terminal Sweep & macOS Chrome)
# ==============================================================================
def build_terminal():
    USERNAME     = "Virus1260"
    DISPLAY_NAME = "Shekhar Mishra"

    print("[..] Generating ASCII portrait for Shekhar...")
    req = Request(
        f"https://avatars.githubusercontent.com/{USERNAME}?size=400",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    img_bytes = urlopen(req, timeout=20).read()

    ASCII_CHARS = "  `.-':=+*csS%#@"
    ART_W, ART_H = 100, 53

    img = Image.open(BytesIO(img_bytes)).convert("L")
    img = img.resize((ART_W, ART_H), Image.LANCZOS)
    pixels = list(img.getdata())

    rows = []
    for r in range(ART_H):
        row = ""
        for c in range(ART_W):
            px  = pixels[r * ART_W + c]
            idx = int((255 - px) / 255 * (len(ASCII_CHARS) - 1))
            row += ASCII_CHARS[idx]
        rows.append(row)

    W1      = 840
    ROW_H   = 15
    ROW_Y0  = 37
    FONT_SZ = 12.9
    ROW_DUR = 0.10
    TEXT_W  = 800
    TEXT_X  = 20

    FOOTER_LINE_Y = ROW_Y0 + ART_H * ROW_H   # 832
    FOOTER_TEXT_Y = FOOTER_LINE_Y + 19        # 851
    H1            = FOOTER_LINE_Y + 43        # 875

    WHOAMI_TEXT = f"{USERNAME}@static-cad:~$ whoami "
    CURSOR_X    = TEXT_X + len(WHOAMI_TEXT) * 7.73

    rows_svg = ""
    for i, row in enumerate(rows):
        begin  = i * ROW_DUR
        y_top  = ROW_Y0 + i * ROW_H
        y_text = y_top + 11.1
        safe   = xe(row)

        rows_svg += (
            f'<clipPath id="r{i}">'
            f'<rect x="{TEXT_X}" y="{y_top:.1f}" height="{ROW_H}" width="0">'
            f'<animate attributeName="width" from="0" to="{TEXT_W}" '
            f'begin="{begin:.3f}s" dur="{ROW_DUR}s" fill="freeze"/>'
            f'</rect></clipPath>\n'
            f'<g clip-path="url(#r{i})">'
            f'<text xml:space="preserve" x="{TEXT_X}" y="{y_text:.1f}" '
            f'fill="#d1d5db" font-size="{FONT_SZ}" '
            f'textLength="{TEXT_W}" lengthAdjust="spacing">{safe}</text>'
            f'</g>\n'
            f'<rect y="{y_top+1:.1f}" width="8" height="13" fill="#f59e0b" opacity="0">'
            f'<animate attributeName="x" from="{TEXT_X}" to="{TEXT_X+TEXT_W}" '
            f'begin="{begin:.3f}s" dur="{ROW_DUR}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0.9" begin="{begin:.3f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{begin+ROW_DUR:.3f}s"/>'
            f'</rect>\n'
        )

    svg1 = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W1}" height="{H1}" viewBox="0 0 {W1} {H1}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#111722"/>
    <stop offset="100%" stop-color="#0d1117"/>
  </linearGradient>
  <linearGradient id="termBorder" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#d4af37" stop-opacity="0.8"/>
    <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.4"/>
    <stop offset="100%" stop-color="#10b981" stop-opacity="0.8"/>
  </linearGradient>
</defs>
<rect width="{W1}" height="{H1}" rx="12" fill="url(#bg)"/>
<rect x="0.5" y="0.5" width="{W1-1}" height="{H1-1}" rx="12" fill="none" stroke="url(#termBorder)" stroke-width="1.2"/>
<line x1="0" y1="30" x2="{W1}" y2="30" stroke="#30363d"/>
<circle cx="20" cy="15.0" r="5" fill="#ff5f56"/>
<circle cx="36" cy="15.0" r="5" fill="#ffbd2e"/>
<circle cx="52" cy="15.0" r="5" fill="#27c93f"/>
<text x="{W1/2:.1f}" y="19.0" fill="#f59e0b" font-size="12" text-anchor="middle" font-weight="600">{USERNAME}@heavy-eng: ~$ ./render_shekhar_portrait.sh</text>
{rows_svg}
<line x1="0" y1="{FOOTER_LINE_Y:.1f}" x2="{W1}" y2="{FOOTER_LINE_Y:.1f}" stroke="#30363d"/>
<text x="20" y="{FOOTER_TEXT_Y:.1f}" fill="#7d8590" font-size="13">{USERNAME}@heavy-eng:~$ whoami <tspan fill="#f59e0b" font-weight="700">{DISPLAY_NAME}</tspan> <tspan fill="#38bdf8">[Lead Mechanical &amp; Automation]</tspan></text>
<rect x="{CURSOR_X + 180:.0f}" y="{FOOTER_TEXT_Y-13:.1f}" width="8" height="14" fill="#f59e0b">
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>
</rect>
</svg>"""

    out1 = os.path.join(OUT_DIR, "terminal-card.svg")
    with open(out1, "w", encoding="utf-8") as f:
        f.write(svg1)
    print(f"[OK] terminal-card.svg written ({W1}×{H1}px, {os.path.getsize(out1)//1024} KB)")


# ==============================================================================
# 3. info-card.svg (Neofetch Engineering Card for Shekhar Mishra)
# ==============================================================================
def build_infocard():
    USERNAME = "Virus1260"
    W2 = 500

    C_GOLD   = "#f59e0b"
    C_BLUE   = "#38bdf8"
    C_GREEN  = "#34d399"
    C_CYAN   = "#22d3ee"
    C_WHITE  = "#e5e7eb"
    C_DIM    = "#30363d"
    C_GRAY   = "#9ca3af"

    INFO_ROWS = [
        {"type": "header"},
        {"type": "section", "label": "— Identity & Role"},
        {"type": "field",   "label": "Role",      "value": "Sr. Mechanical Design Engineer"},
        {"type": "field",   "label": "Domain",    "value": "Static Equipment & Engineering Automation"},
        {"type": "field",   "label": "Company",   "value": "Grand Prix Engineering (P) Ltd."},
        {"type": "field",   "label": "Alum",      "value": "L&T Heavy Engineering · Kinam · Geecy"},
        {"type": "field",   "label": "Location",  "value": "Hazira, Surat — India"},

        {"type": "section", "label": "— Design Codes & Metallurgy"},
        {"type": "field",   "label": "Codes",     "value": "ASME Sec. VIII Div 1 & 2, PED, TEMA, API 660"},
        {"type": "field",   "label": "Standards", "value": "API 934 A/C/E, API 650/620, EN 13445, EJMA, IBR"},
        {"type": "field",   "label": "Alloys",    "value": "Cr-Mo, Super Duplex, Hastelloy, Titanium, Cu-Ni"},

        {"type": "section", "label": "— CAD, Simulation & Automation"},
        {"type": "field",   "label": "Modelling", "value": "AutoCAD, SolidWorks, Creo, CATIA, PV Elite"},
        {"type": "field",   "label": "FEA/CFD",   "value": "ANSYS (Master Certified), COMSOL, Nozzle PRO"},
        {"type": "field",   "label": "Code",      "value": "Python (In-house CAD engines), TypeScript, React"},
        {"type": "field",   "label": "Impact",    "value": "70%–85% man-hour reduction via Python PSDV tool"},

        {"type": "section", "label": "— Verified Scale & Highlights"},
        {"type": "bullet",  "value": "16,930 Tons Max Tonnage (KNPC Reactor/Regenerator)"},
        {"type": "bullet",  "value": "-212°C to +1200°C Operating Temperature Envelope"},
        {"type": "bullet",  "value": "0 NCRs Client Review (Saudi Aramco, KNPC, ExxonMobil)"},
        {"type": "bullet",  "value": "Leading 1,150 KTPA LLDPE/HDPE Swing Unit (BPCL Bina)"},
    ]

    SLIDE_DUR = 0.4
    STEP      = 0.05
    TOP_Y     = 56.0
    LINE_H    = 19.8

    parts = []
    cur_t = 0.15
    cur_y = TOP_Y

    for row in INFO_ROWS:
        t  = cur_t
        ks = "0.2 0.8 0.2 1"

        if row["type"] == "header":
            ulen = len(USERNAME)
            rule_x1 = 20 + (ulen + 1 + 6) * 8.2
            parts.append(
                f'<g opacity="0" transform="translate(0,5)">'
                f'<text x="20" y="{cur_y}" font-size="14" font-weight="700">'
                f'<tspan fill="{C_GOLD}">{xe(USERNAME)}</tspan>'
                f'<tspan fill="{C_GRAY}">@</tspan>'
                f'<tspan fill="{C_CYAN}">heavy-engineering</tspan>'
                f'</text>'
                f'<line x1="{rule_x1:.0f}" y1="{cur_y-4:.1f}" x2="475" y2="{cur_y-4:.1f}" stroke="{C_DIM}" stroke-opacity="0.8"/>'
                f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze" calcMode="spline" keySplines="{ks}"/>'
                f'</g>'
            )
            cur_y += LINE_H * 1.05
            cur_t += STEP

        elif row["type"] == "section":
            label   = row["label"]
            rule_x1 = 20 + len(label) * 7.4
            parts.append(
                f'<g opacity="0" transform="translate(0,5)">'
                f'<text x="20" y="{cur_y}" fill="{C_BLUE}" font-size="12.2" font-weight="700">{xe(label)}</text>'
                f'<line x1="{rule_x1:.0f}" y1="{cur_y-4:.1f}" x2="475" y2="{cur_y-4:.1f}" stroke="{C_DIM}" stroke-opacity="0.8"/>'
                f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze" calcMode="spline" keySplines="{ks}"/>'
                f'</g>'
            )
            cur_y += LINE_H * 1.3
            cur_t += STEP * 1.5

        elif row["type"] == "field":
            parts.append(
                f'<g opacity="0" transform="translate(0,5)">'
                f'<text x="20" y="{cur_y}" fill="{C_GOLD}" font-size="12" font-weight="700">{xe(row["label"])}</text>'
                f'<text x="105" y="{cur_y}" fill="{C_WHITE}" font-size="12">{xe(row["value"])}</text>'
                f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze" calcMode="spline" keySplines="{ks}"/>'
                f'</g>'
            )
            cur_y += LINE_H
            cur_t += STEP

        elif row["type"] == "bullet":
            dot_cy = cur_y - 4
            parts.append(
                f'<g opacity="0" transform="translate(0,5)">'
                f'<circle cx="23" cy="{dot_cy:.1f}" r="2.5" fill="{C_GREEN}"/>'
                f'<text x="34" y="{cur_y}" fill="{C_WHITE}" font-size="12">{xe(row["value"])}</text>'
                f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze" calcMode="spline" keySplines="{ks}"/>'
                f'</g>'
            )
            cur_y += LINE_H
            cur_t += STEP

    H2 = int(cur_y) + 26
    info_parts_svg = "\n".join(parts)

    svg2 = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<defs>
  <linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#111722"/>
    <stop offset="100%" stop-color="#0d1117"/>
  </linearGradient>
  <linearGradient id="infoBorder" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8"/>
    <stop offset="50%" stop-color="#f59e0b" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="#10b981" stop-opacity="0.8"/>
  </linearGradient>
</defs>
<rect width="{W2}" height="{H2}" rx="12" fill="url(#ibg)"/>
<rect x="0.5" y="0.5" width="{W2-1}" height="{H2-1}" rx="12" fill="none" stroke="url(#infoBorder)" stroke-width="1.2"/>
<line x1="0" y1="30" x2="{W2}" y2="30" stroke="#30363d"/>
<circle cx="20" cy="15.0" r="5" fill="#ff5f56"/>
<circle cx="36" cy="15.0" r="5" fill="#ffbd2e"/>
<circle cx="52" cy="15.0" r="5" fill="#27c93f"/>
<text x="{W2/2:.1f}" y="19.0" fill="{C_GRAY}" font-size="12" text-anchor="middle">{USERNAME}@heavy-eng: ~$ neofetch --static-eng</text>
{info_parts_svg}
</svg>"""

    out2 = os.path.join(OUT_DIR, "info-card.svg")
    with open(out2, "w", encoding="utf-8") as f:
        f.write(svg2)
    print(f"[OK] info-card.svg written ({W2}×{H2}px, {os.path.getsize(out2)//1024} KB)")


if __name__ == "__main__":
    build_contrib()
    build_terminal()
    build_infocard()
    print("\nAll custom profile SVGs generated successfully!")

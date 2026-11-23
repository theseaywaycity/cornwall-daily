"""Cornwall Daily graphic renderer.

Usage:
  python render.py logo out.png
  python render.py post post.json out.png

post.json fields:
  category  - NEWS | EVENT | BUSINESS | COMMUNITY | HISTORY | DEVELOPMENT
  headline  - short headline (aim for under 70 characters)
  dek       - optional one-line summary
  facts     - optional list of up to 3 short lines (e.g. "Sat, Nov 28 · 10 a.m.–4 p.m.")
  source    - source credit, e.g. "Cornwall Seaway News"
  date      - display date, e.g. "Monday, November 23"
"""
import html
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

NAVY = "#13294B"
RIVER = "#1D6F8C"
SUN = "#D9A441"
CREAM = "#F3ECDD"
INK = "#14212E"

FONTS = """
@font-face { font-family: 'Bitter'; src: url('file:///usr/share/fonts/truetype/google-fonts/ofl/bitter/Bitter[wght].ttf'); font-weight: 100 900; }
@font-face { font-family: 'DM Sans'; src: url('file:///usr/share/fonts/truetype/google-fonts/ofl/dmsans/DMSans[opsz,wght].ttf'); font-weight: 100 1000; }
* { margin: 0; padding: 0; box-sizing: border-box; }
"""

CATEGORY_COLORS = {
    "NEWS": RIVER,
    "EVENT": "#B4462F",
    "BUSINESS": "#2F7D4F",
    "COMMUNITY": "#7A4FA0",
    "HISTORY": "#8A6A2E",
    "DEVELOPMENT": "#4A5A6A",
}


def waves(color, width, stroke, count=3, gap=None, amp=None):
    gap = gap or stroke * 2.6
    amp = amp or stroke * 1.4
    seg = amp * 4
    paths = []
    for i in range(count):
        y = amp + 2 + i * gap
        d = f"M0 {y}"
        x = 0
        while x < width:
            d += f" q {seg/4} {-amp} {seg/2} 0 t {seg/2} 0"
            x += seg
        paths.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round"/>')
    h = amp * 2 + 4 + (count - 1) * gap
    return f'<svg width="{width}" height="{h}" viewBox="0 0 {width} {h}" xmlns="http://www.w3.org/2000/svg">{"".join(paths)}</svg>'


def logo_html():
    return f"""<html><head><style>{FONTS}
body {{ width:1080px; height:1080px; background:{NAVY}; display:flex; align-items:center; justify-content:center; }}
.wrap {{ display:flex; flex-direction:column; align-items:center; }}
.mono {{ font-family:'Bitter'; font-weight:800; color:#fff; font-size:430px; line-height:1; letter-spacing:-18px; }}
.wave {{ margin-top:30px; }}
.name {{ margin-top:46px; font-family:'DM Sans'; font-weight:700; color:{SUN}; font-size:58px; letter-spacing:14px; }}
</style></head><body><div class="wrap">
<div class="mono">CD</div>
<div class="wave">{waves(SUN, 520, 22, count=2, gap=58, amp=22)}</div>
<div class="name">CORNWALL DAILY</div>
</div></body></html>"""


def post_html(p):
    cat = p.get("category", "NEWS").upper()
    cat_color = CATEGORY_COLORS.get(cat, RIVER)
    headline = html.escape(p["headline"])
    n = len(p["headline"])
    size = 104 if n <= 40 else 92 if n <= 60 else 80 if n <= 80 else 68
    dek = f'<div class="dek">{html.escape(p["dek"])}</div>' if p.get("dek") else ""
    facts = "".join(f'<div class="fact"><span class="dot"></span>{html.escape(f)}</div>' for f in p.get("facts", [])[:3])
    facts_block = f'<div class="facts">{facts}</div>' if facts else ""
    source = html.escape(p.get("source", ""))
    date = html.escape(p.get("date", ""))
    return f"""<html><head><style>{FONTS}
body {{ width:1080px; height:1350px; background:{CREAM}; font-family:'DM Sans'; color:{INK}; display:flex; flex-direction:column; }}
.top {{ background:{NAVY}; padding:52px 72px 40px; color:#fff; }}
.mast {{ display:flex; justify-content:space-between; align-items:baseline; }}
.brand {{ font-family:'Bitter'; font-weight:800; font-size:54px; letter-spacing:-0.5px; }}
.date {{ font-size:28px; font-weight:500; color:#C9D6E3; }}
.topwave {{ margin-top:22px; }}
.main {{ flex:1; padding:70px 72px 0; display:flex; flex-direction:column; }}
.cat {{ align-self:flex-start; background:{cat_color}; color:#fff; font-weight:800; font-size:28px; letter-spacing:5px; padding:12px 24px; border-radius:6px; }}
.headline {{ font-family:'Bitter'; font-weight:800; font-size:{size}px; line-height:1.08; margin-top:44px; letter-spacing:-1px; }}
.dek {{ font-size:38px; line-height:1.35; margin-top:36px; color:#3A4A5A; font-weight:500; }}
.facts {{ margin-top:44px; border-top:3px solid {NAVY}; padding-top:30px; }}
.fact {{ font-size:36px; font-weight:700; margin-bottom:18px; display:flex; align-items:center; }}
.dot {{ width:16px; height:16px; background:{SUN}; border-radius:50%; margin-right:22px; flex:none; }}
.foot {{ padding:34px 72px 50px; display:flex; justify-content:space-between; align-items:flex-end; font-size:26px; color:#55657A; }}
.handle {{ font-weight:800; color:{NAVY}; font-size:30px; }}
</style></head><body>
<div class="top"><div class="mast"><div class="brand">Cornwall Daily</div><div class="date">{date}</div></div>
<div class="topwave">{waves(SUN, 936, 7, count=1, amp=9)}</div></div>
<div class="main"><div class="cat">{cat}</div><div class="headline">{headline}</div>{dek}{facts_block}</div>
<div class="foot"><div>{('Source: ' + source) if source else ''}</div><div class="handle">@theseawaycity</div></div>
</body></html>"""


def render(markup, out, w, h):
    tmp = Path(out).with_suffix(".html")
    tmp.write_text(markup)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(tmp.resolve().as_uri())
        pg.wait_for_timeout(300)
        pg.screenshot(path=out)
        b.close()
    tmp.unlink()


if __name__ == "__main__":
    if sys.argv[1] == "logo":
        render(logo_html(), sys.argv[2], 1080, 1080)
    else:
        render(post_html(json.loads(Path(sys.argv[2]).read_text())), sys.argv[3], 1080, 1350)

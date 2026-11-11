#!/usr/bin/env python3
"""Draw the Steering gantt (1920x1080, the deck's dark look) from a JSON spec.

Usage:
  python gantt.py SPEC.json OUT.svg [--png OUT.png]

The spec format is documented in ../assets/gantt-spec.md and there is a full
example in ../assets/gantt-steering-2.json (the gantt shown at Steering 2).
--png needs Playwright with a Chromium; without it, open the .html that is
written next to the SVG and take the screenshot by hand.
"""
import argparse, datetime as dt, html, json, os, sys

W, H = 1920, 1080
YEL, RED, BLUE, CYAN, ORANGE = '#FFD54A', '#FF5A4A', '#4FC3F7', '#4FD2FF', '#FF9F43'
BG, GRID, INK, INK2 = '#0B0B0B', '#2A2A2A', '#FFFFFF', '#DADADA'
X0, RIGHT_PAD, TOP = 340, 70, 58
SEC_COLORS = {'base': YEL, 'inc': BLUE, 'crit': RED}
BAR = {
    'done':    ('Hecho', f'fill="{YEL}"'),
    'pend':    ('Pendiente', f'fill="url(#hy)" stroke="{YEL}" stroke-width="2" stroke-dasharray="6 4"'),
    'late':    ('Atrasado', f'fill="url(#ho)" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="6 4"'),
    'crit':    ('Camino crítico', f'fill="url(#hr)" stroke="{RED}" stroke-width="2"'),
    'inc':     ('Incorporado pendiente', f'fill="url(#hb)" stroke="{BLUE}" stroke-width="2" stroke-dasharray="6 4"'),
    'incdone': ('Incorporado hecho', f'fill="{CYAN}"'),
}
DIAMOND = {
    'done': ('Hito logrado', YEL, YEL),
    'pend': ('Hito pendiente', 'url(#hb)', BLUE),
    'crit': ('Hito crítico pendiente', 'url(#hr)', RED),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('spec'); ap.add_argument('out_svg'); ap.add_argument('--png')
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding='utf-8'))
    svg = render(spec)
    open(a.out_svg, 'w', encoding='utf-8').write(svg)
    page = os.path.splitext(a.out_svg)[0] + '.html'
    open(page, 'w', encoding='utf-8').write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0;background:{BG}}} svg{{display:block}}</style></head><body>{svg}</body></html>')
    print(f'svg: {a.out_svg}\nhtml: {page}')
    if a.png:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            sys.exit('Playwright is not installed: open the .html and screenshot it at 1920x1080.')
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
            pg.goto('file://' + os.path.abspath(page))
            pg.screenshot(path=a.png, full_page=True)
            b.close()
        print(f'png: {a.png} (3840x2160)')


def render(spec):
    weeks = spec['weeks']
    n = len(weeks)
    colw = (W - X0 - RIGHT_PAD) / n
    start = dt.date.fromisoformat(spec['start'])
    year = start.year
    rh, hh, sh, bh, dr = (spec.get(k, d) for k, d in
                          [('row_h', 37), ('milestone_h', 28), ('section_h', 28), ('bar_h', 26), ('diamond_r', 9)])

    def wx(w):
        return X0 + (w - 1) * colw

    def dx(ddmm):
        d, m = int(ddmm[:2]), int(ddmm[3:5])
        return X0 + (dt.date(year, m, d) - start).days / 7 * colw

    def days(a, b):
        return (dt.date(year, int(b[3:5]), int(b[:2])) - dt.date(year, int(a[3:5]), int(a[:2]))).days

    out, used_bars, used_dias = [], [], []
    y = TOP + 8
    body = []
    for si, sec in enumerate(spec['sections']):
        if si:
            y += 6
        body.append(f'<text x="14" y="{y + 16}" class="sec" fill="{SEC_COLORS.get(sec.get("color", "base"), YEL)}">{esc(sec["title"])}</text>')
        y += sh
        for row in sec['rows']:
            cy = y + rh / 2
            cls = 'lab dim' if row.get('dim') else 'lab'
            pts_style = ' style="fill:#8a8a8a"' if row.get('dim') else ''
            body.append(f'<text x="14" y="{cy + 6}" class="{cls}">{esc(row["name"])}</text>'
                        f'<text x="{X0 - 12}" y="{cy + 5}" class="mono" text-anchor="end"{pts_style}>{esc(row.get("pts", ""))}</text>')
            for s0, s1, kind in row.get('segments', []):
                if kind not in used_bars:
                    used_bars.append(kind)
                x = wx(s0) + 1; w = (s1 - s0 + 1) * colw - 2
                body.append(f'<rect x="{x:.1f}" y="{cy - bh / 2}" width="{w:.1f}" height="{bh}" rx="5" {BAR[kind][1]}/>')
            if row.get('note'):
                nx = wx(row.get('note_week', spec.get('today_week', 1))) + 10
                body.append(f'<text x="{nx:.1f}" y="{cy + 5}" class="mono" style="fill:{RED};font-weight:bold">{esc(row["note"])}</text>')
            y += rh
            for ms in row.get('milestones', []):
                cy = y + hh / 2
                kind = ms.get('kind', 'done')
                if kind not in used_dias:
                    used_dias.append(kind)
                label = ms.get('label', ms.get('actual', ''))
                body.append(f'<text x="34" y="{cy + 5}" class="lab" style="font-size:14px;font-weight:600;fill:#e6e6e6">{esc(ms["name"])}</text>'
                            f'<text x="{X0 - 12}" y="{cy + 5}" class="mono" style="font-size:13px" text-anchor="end">{esc(label)}</text>')
                xr = dx(ms['actual'])
                if ms.get('base') and ms['base'] != ms['actual']:
                    if 'hb' not in used_dias:
                        used_dias.append('hb')
                    xb = dx(ms['base']); l, r = sorted((xb, xr))
                    body.append(f'<line x1="{l + dr:.1f}" y1="{cy}" x2="{r - dr:.1f}" y2="{cy}" stroke="#9a9a9a" stroke-width="1.5" stroke-dasharray="4 4"/>')
                    body.append(diamond(xb, cy, dr, 'none', '#9a9a9a'))
                    txt = f'{days(ms["base"], ms["actual"]):+d} d'
                    tx = max(xb, xr) + 14
                    if tx + 40 > W:
                        body.append(f'<text x="{min(xb, xr) - 14:.1f}" y="{cy + 4}" class="mono" text-anchor="end" style="font-size:12px;fill:#bdbdbd">{txt}</text>')
                    else:
                        body.append(f'<text x="{tx:.1f}" y="{cy + 4}" class="mono" style="font-size:12px;fill:#bdbdbd">{txt}</text>')
                _, f, st = DIAMOND[kind]
                body.append(diamond(xr, cy, dr, f, st))
                y += hh
    gbot = y + 4

    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    out.append(DEFS)
    out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f'<text x="14" y="38" class="wk" style="letter-spacing:2px">{esc(spec.get("title", "SEMANA"))}</text>')
    for i, (w, d) in enumerate(weeks):
        cx = wx(i + 1) + colw / 2
        out.append(f'<text x="{cx:.1f}" y="32" class="wk" text-anchor="middle">{esc(w)}</text><text x="{cx:.1f}" y="50" class="dt" text-anchor="middle">{esc(d)}</text>')
        out.append(f'<line x1="{wx(i + 1):.1f}" y1="{TOP}" x2="{wx(i + 1):.1f}" y2="{gbot}" stroke="{GRID}"/>')
    out.append(f'<line x1="0" y1="{TOP}" x2="{W}" y2="{TOP}" stroke="{GRID}"/>')
    ly = gbot + 24
    for dl in spec.get('deliveries', []):
        x = wx(dl['week'])
        style = dl.get('style', 'normal')
        if style == 'today':
            out.append(f'<line x1="{x:.1f}" y1="{TOP}" x2="{x:.1f}" y2="{gbot}" stroke="{RED}" stroke-width="2" stroke-dasharray="6 5"/>')
            out.append(f'<text x="{x:.1f}" y="{ly}" class="mono" text-anchor="middle" style="fill:{RED};font-size:16px;font-weight:bold">{esc(dl["label"])}</text>')
        elif style == 'end':
            x -= 1
            out.append(f'<line x1="{x:.1f}" y1="{TOP}" x2="{x:.1f}" y2="{gbot}" stroke="#d0d0d0" stroke-width="1.5" stroke-dasharray="6 5"/>')
            out.append(f'<text x="{x:.1f}" y="{ly}" class="mono" text-anchor="end" style="fill:#e8e8e8;font-size:16px;font-weight:bold">{esc(dl["label"])}</text>')
        else:
            out.append(f'<text x="{x:.1f}" y="{ly}" class="mono" text-anchor="middle" style="fill:#d0d0d0;font-size:15px">{esc(dl["label"])}</text>')
    out.extend(body)  # drawn after the lines so diamonds sit on top
    lx, gy = 14, ly + 44
    for k in used_bars:
        lab, s = BAR[k]
        out.append(f'<rect x="{lx}" y="{gy - 14}" width="38" height="20" rx="4" {s}/><text x="{lx + 48}" y="{gy + 1}" class="leg">{lab}</text>')
        lx += 48 + len(lab) * 8.3 + 40
    for k in used_dias:
        lab, f, st = ('Fecha base (Steering anterior)', 'none', '#9a9a9a') if k == 'hb' else DIAMOND[k]
        out.append(diamond(lx + 19, gy - 4, 11, f, st) + f'<text x="{lx + 40}" y="{gy + 1}" class="leg">{lab}</text>')
        lx += 40 + len(lab) * 8.3 + 34
    if lx > W:
        print(f'warning: the legend is {lx:.0f}px wide, wider than {W}px; shorten labels', file=sys.stderr)
    if gy + 22 > H:
        print(f'warning: content reaches {gy + 22:.0f}px, taller than {H}px; lower row_h/milestone_h in the spec', file=sys.stderr)
    out.append('</svg>')
    return '\n'.join(out)


def diamond(x, cy, r, fill, stroke):
    return f'<path d="M{x:.1f} {cy - r} L{x + r:.1f} {cy} L{x:.1f} {cy + r} L{x - r:.1f} {cy} Z" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def esc(s):
    return html.escape(str(s), quote=False)


DEFS = '''<defs>
<pattern id="hr" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#5a1d17"/><line x1="0" y1="0" x2="0" y2="8" stroke="#a8392d" stroke-width="3"/></pattern>
<pattern id="hb" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#0f2a36"/><line x1="0" y1="0" x2="0" y2="8" stroke="#2b6f8a" stroke-width="3"/></pattern>
<pattern id="hy" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#2e2610"/><line x1="0" y1="0" x2="0" y2="8" stroke="#8a7228" stroke-width="3"/></pattern>
<pattern id="ho" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#3a2310"/><line x1="0" y1="0" x2="0" y2="8" stroke="#a8642a" stroke-width="3"/></pattern>
<style>
.lab{font-family:'Inter Display','Inter',sans-serif;font-weight:800;font-size:16px;fill:#fff;letter-spacing:-0.2px}
.dim{fill:#8a8a8a}
.mono{font-family:'DejaVu Sans Mono',monospace;font-size:14px;fill:#cfcfcf}
.wk{font-family:'DejaVu Sans Mono',monospace;font-weight:bold;font-size:17px;fill:#FFD54A}
.dt{font-family:'DejaVu Sans Mono',monospace;font-size:12px;fill:#bdbdbd}
.sec{font-family:'DejaVu Sans Mono',monospace;font-weight:bold;font-size:13px;letter-spacing:1.5px}
.leg{font-family:'Inter','Inter Display',sans-serif;font-size:14px;fill:#fff}
</style></defs>'''

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Stage traces, capture batch 1, size-gate. The agent still has to look at the pixels."""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import Page, sync_playwright

SIZES = {
    'home': ((2400, 2900), (1700, 2000)),
    'flow-runner': ((2380, 2460), (1380, 1450)),
    'inspect': ((1900, 2200), (1400, 1650)),
    'runstep': ((400, 650), (350, 550)),
}


def run_flow(base: str, key: str, inp: dict) -> str:
    req = urllib.request.Request(
        f'{base}/api/runAction',
        data=json.dumps({'key': key, 'input': inp}).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        body = json.load(r)
        trace = r.headers.get('X-Genkit-Trace-Id') or (body.get('telemetry') or {}).get('traceId')
    if 'error' in body:
        raise SystemExit(body['error'])
    if not trace:
        raise SystemExit(f'no trace id for {key}')
    print('ran', key, trace)
    return trace


def hide_no_app(page: Page) -> None:
    page.evaluate(
        """() => {
          const walk = (n) => {
            if (n.nodeType === Node.TEXT_NODE && n.textContent.includes('No app detected')) {
              n.textContent = n.textContent.replace('No app detected', 'sample');
            }
            n.childNodes.forEach(walk);
          };
          walk(document.body);
        }"""
    )


def add_chrome(src: Path, dest: Path, url: str = 'localhost:4000') -> None:
    im = Image.open(src).convert('RGB')
    bar = 72
    out = Image.new('RGB', (im.width, im.height + bar), (36, 36, 40))
    out.paste(im, (0, bar))
    draw = ImageDraw.Draw(out)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        x = 20 + i * 28
        draw.ellipse((x, 26, x + 18, 44), fill=c)
    draw.rounded_rectangle((180, 18, im.width - 180, 54), radius=12, fill=(50, 50, 56))
    try:
        font = ImageFont.truetype('/System/Library/Fonts/SFNS.ttf', 22)
    except OSError:
        font = ImageFont.load_default()
    draw.text((im.width / 2, 36), url, fill=(210, 210, 214), font=font, anchor='mm')
    out.save(dest)


def clip_box(page: Page, box: dict, dest: Path) -> None:
    page.screenshot(
        path=str(dest),
        type='png',
        clip={
            'x': max(0, box['x']),
            'y': max(0, box['y']),
            'width': box['width'],
            'height': box['height'],
        },
    )


def first_box(page: Page, text: str):
    loc = page.get_by_text(text, exact=False).first
    loc.wait_for(timeout=10000)
    return loc.bounding_box()


def capture(base: str, out: Path, traces: dict[str, str]) -> dict[str, str]:
    texts: dict[str, str] = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page(
            viewport={'width': 1360, 'height': 886},
            device_scale_factor=2,
            color_scheme='dark',
        )
        page.goto(base, wait_until='domcontentloaded')
        page.get_by_text('menuSuggestionFlow').first.wait_for(timeout=15000)
        page.wait_for_timeout(400)
        hide_no_app(page)
        raw = out / '_home_raw.png'
        page.screenshot(path=str(raw), type='png')
        add_chrome(raw, out / 'home.png')
        texts['home'] = page.inner_text('body')
        page.close()

        page = browser.new_page(
            viewport={'width': 1212, 'height': 708},
            device_scale_factor=2,
            color_scheme='dark',
        )
        page.goto(f'{base}/flows/menuSuggestionFlow', wait_until='domcontentloaded')
        page.get_by_text('Input (JSON)').first.wait_for(timeout=15000)
        page.wait_for_timeout(500)
        closer = page.locator('button').filter(has_text='close').first
        if closer.count():
            closer.click()
            page.wait_for_timeout(300)
        hide_no_app(page)
        page.screenshot(path=str(out / 'flow-runner.png'), type='png')
        texts['flow-runner'] = page.inner_text('body')
        page.close()

        page = browser.new_page(
            viewport={'width': 1280, 'height': 800},
            device_scale_factor=2,
            color_scheme='dark',
        )
        page.goto(f'{base}/traces/{traces["inspect"]}', wait_until='domcontentloaded')
        page.get_by_text('complexMenuSuggestionFlow').first.wait_for(timeout=15000)
        page.wait_for_timeout(600)
        page.get_by_text('vertexai/gemini-2.5-flash').nth(1).click()
        page.wait_for_timeout(400)
        preview = page.get_by_text('Preview', exact=True)
        if preview.count():
            preview.first.click()
            page.wait_for_timeout(300)
        hide_no_app(page)
        tree_top = first_box(page, 'complexMenuSuggestionFlow')
        clip_box(
            page,
            {
                'x': 220,
                'y': (tree_top['y'] - 12) if tree_top else 56,
                'width': 1040,
                'height': 770,
            },
            out / 'inspect.png',
        )
        texts['inspect'] = page.inner_text('body')
        page.close()

        page = browser.new_page(
            viewport={'width': 1100, 'height': 700},
            device_scale_factor=2,
            color_scheme='dark',
        )
        page.goto(f'{base}/traces/{traces["runstep"]}', wait_until='domcontentloaded')
        page.get_by_text('retrieve-daily-menu').first.wait_for(timeout=15000)
        page.wait_for_timeout(400)
        hide_no_app(page)
        tree = page.evaluate(
            """() => {
              const nodes = [...document.querySelectorAll('div,nav,aside,section')];
              const hits = nodes.filter((e) => {
                const t = e.innerText || '';
                return (
                  t.includes('retrieve-daily-menu') &&
                  t.includes('menuQuestionFlow') &&
                  !t.includes('Export') &&
                  e.offsetWidth > 180 &&
                  e.offsetWidth < 520
                );
              });
              hits.sort((a, b) => b.offsetWidth - a.offsetWidth);
              const hit = hits[0];
              if (!hit) return null;
              const r = hit.getBoundingClientRect();
              return { x: r.x, y: r.y };
            }"""
        )
        if not tree:
            raise SystemExit('runstep: no tree panel')
        clip_box(
            page,
            {'x': tree['x'] - 4, 'y': tree['y'] - 4, 'width': 268, 'height': 216},
            out / 'runstep.png',
        )
        texts['runstep'] = page.inner_text('body')
        page.close()
        browser.close()
    return texts


def vet(out: Path, texts: dict[str, str]) -> bool:
    checks = {
        'home': {
            'in': ['menuSuggestionFlow', 'hello', 'gemini-2.5-flash'],
            'out': ['codegemma', 'No app detected', 'diffusiongemma'],
        },
        'flow-runner': {
            'in': ['menuSuggestionFlow', 'medieval', 'Run'],
            'out': ['No app detected'],
        },
        'inspect': {
            'in': ['complexMenuSuggestionFlow', 'vertexai/gemini-2.5-flash'],
            'out': ['codegemma'],
        },
        'runstep': {
            'in': ['menuQuestionFlow', 'retrieve-daily-menu'],
            'out': [],
        },
    }
    ok = True
    report = {}
    for sid, c in checks.items():
        path = out / f'{sid}.png'
        im = Image.open(path)
        w, h = im.size
        (wmin, wmax), (hmin, hmax) = SIZES[sid]
        size_ok = wmin <= w <= wmax and hmin <= h <= hmax
        missing = [x for x in c['in'] if x not in texts[sid]]
        leaked = [x for x in c['out'] if x in texts[sid]]
        passed = size_ok and not missing and not leaked
        if not passed:
            ok = False
        report[sid] = {'size': [w, h], 'size_ok': size_ok, 'missing': missing, 'leaked': leaked}
        flag = 'PASS' if passed else 'FAIL'
        print(f'{flag} {sid} {w}x{h} missing={missing} leaked={leaked}')
    (out / '_vet.json').write_text(json.dumps(report, indent=2))
    return ok


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--base-url', default='http://127.0.0.1:4104')
    p.add_argument('--out-dir', default=str(Path.home() / 'Desktop/genkit-docsite-shots/proposed'))
    args = p.parse_args()
    base = args.base_url.rstrip('/')
    out = Path(args.out_dir).expanduser()
    out.mkdir(parents=True, exist_ok=True)

    traces = {
        'inspect': run_flow(base, '/flow/complexMenuSuggestionFlow', {'theme': 'medieval'}),
        'runstep': run_flow(base, '/flow/menuQuestionFlow', {'question': 'What is a good starter for two people?'}),
    }
    run_flow(base, '/flow/menuSuggestionFlow', {'theme': 'medieval'})

    texts = capture(base, out, traces)
    if not vet(out, texts):
        raise SystemExit('FAIL: size or text gate. Run once more. Do not dump a full page.')
    print('SIZE GATES PASSED. Now look at old vs new pixels. Hesitate = reject.')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Capture all Batch 2 shots: runners, traces, datasets, and evaluations."""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

from PIL import Image
from playwright.sync_api import Page, sync_playwright

OLD_URLS = {
    'model-runner': 'https://raw.githubusercontent.com/genkit-ai/docsite/main/src/assets/developer_ui_model_runner.png',
    'prompt-runner': 'https://raw.githubusercontent.com/genkit-ai/docsite/main/src/assets/prompts-in-developer-ui.png',
}

COMPARE_HTML = """<!doctype html>
<meta charset="utf-8" />
<title>Batch 2 — live vs proposed</title>
<style>
  :root { color-scheme: dark; }
  body { margin: 24px; font: 15px/1.45 ui-sans-serif, system-ui; background: #121316; color: #e3e2e6; }
  h1 { font-size: 20px; font-weight: 600; margin: 0 0 6px; }
  .lead { color: #b0b0b4; margin: 0 0 28px; }
  section { margin: 0 0 48px; }
  h2 { font-size: 16px; font-weight: 600; margin: 0 0 8px; }
  .pair { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  figure { margin: 0; }
  figcaption { font-size: 12px; letter-spacing: .04em; text-transform: uppercase; color: #9aa0a6; margin: 0 0 8px; }
  img { width: 100%; background: #0d0e11; border: 1px solid #2f3033; border-radius: 8px; display: block; }
</style>
<h1>Batch 2 — live docsite vs proposed</h1>
<p class="lead">Left is live docsite (or baseline). Right is the proposed capture.</p>
"""


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


def fetch_old(out: Path) -> None:
    dest = out / 'old'
    dest.mkdir(parents=True, exist_ok=True)
    for sid, url in OLD_URLS.items():
        path = dest / f'{sid}.png'
        if path.exists() and path.stat().st_size > 1000:
            continue
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                path.write_bytes(r.read())
            print('old', path.name, path.stat().st_size)
        except Exception as e:
            print('could not fetch old', sid, e)


def capture(base: str, out: Path) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # 1. model-runner
        page = browser.new_page(
            viewport={'width': 1212, 'height': 708},
            device_scale_factor=2,
            color_scheme='dark',
        )
        page.goto(f'{base}/models?model=vertexai%2Fgemini-2.5-flash', wait_until='domcontentloaded')
        page.get_by_text('vertexai/gemini-2.5-flash').first.wait_for(timeout=15000)
        page.wait_for_timeout(500)
        msg_input = page.locator('textarea, [contenteditable="true"]').last
        if msg_input.count():
            msg_input.fill('Invent one medieval-themed restaurant dish.')
        if not page.get_by_text('Model config').count():
            cfg_btn = page.locator('button').filter(has_text='tune').first
            if cfg_btn.count():
                cfg_btn.click()
                page.wait_for_timeout(300)
        hide_no_app(page)
        page.screenshot(path=str(out / 'model-runner.png'), type='png')
        page.close()

        # 2. prompt-runner
        page = browser.new_page(
            viewport={'width': 1212, 'height': 708},
            device_scale_factor=2,
            color_scheme='dark',
        )
        page.goto(f'{base}/prompts/hello', wait_until='domcontentloaded')
        page.get_by_text('hello').first.wait_for(timeout=15000)
        page.wait_for_timeout(500)
        if not page.get_by_text('Model config').count():
            cfg_btn = page.locator('button').filter(has_text='tune').first
            if cfg_btn.count():
                cfg_btn.click()
                page.wait_for_timeout(300)
        hide_no_app(page)
        page.screenshot(path=str(out / 'prompt-runner.png'), type='png')
        page.close()

        # 3. traces
        page = browser.new_page(
            viewport={'width': 1212, 'height': 708},
            device_scale_factor=2,
            color_scheme='dark',
        )
        page.goto(f'{base}/traces', wait_until='domcontentloaded')
        page.get_by_text('Traces').first.wait_for(timeout=15000)
        page.wait_for_timeout(500)
        hide_no_app(page)
        page.screenshot(path=str(out / 'traces.png'), type='png')
        page.close()

        # 4. datasets list
        page = browser.new_page(
            viewport={'width': 1212, 'height': 708},
            device_scale_factor=2,
            color_scheme='dark',
        )
        page.goto(f'{base}/datasets', wait_until='domcontentloaded')
        page.get_by_text('menuSuggestionsDataset').first.wait_for(timeout=15000)
        page.wait_for_timeout(500)
        hide_no_app(page)
        page.screenshot(path=str(out / 'datasets.png'), type='png')
        page.close()

        # 5. dataset-create
        page = browser.new_page(
            viewport={'width': 1212, 'height': 800},
            device_scale_factor=2,
            color_scheme='dark',
        )
        page.goto(f'{base}/datasets', wait_until='domcontentloaded')
        page.get_by_text('Create dataset').first.wait_for(timeout=15000)
        page.get_by_text('Create dataset').first.click()
        page.wait_for_timeout(500)
        page.locator('input').first.fill('menuQuestionDataset')
        page.locator('mat-select').click()
        page.wait_for_timeout(300)
        page.get_by_text('menuQuestionFlow', exact=True).click()
        page.wait_for_timeout(300)
        hide_no_app(page)
        page.screenshot(path=str(out / 'dataset-create.png'), type='png')
        page.close()

        # 6. dataset-examples
        page = browser.new_page(
            viewport={'width': 1212, 'height': 708},
            device_scale_factor=2,
            color_scheme='dark',
        )
        page.goto(f'{base}/datasets/menuSuggestionsDataset', wait_until='domcontentloaded')
        page.get_by_text('menuSuggestionsDataset').first.wait_for(timeout=15000)
        page.wait_for_timeout(500)
        hide_no_app(page)
        page.screenshot(path=str(out / 'dataset-examples.png'), type='png')
        page.close()

        # 7. eval-run
        page = browser.new_page(
            viewport={'width': 1212, 'height': 708},
            device_scale_factor=2,
            color_scheme='dark',
        )
        page.goto(f'{base}/evaluate/new', wait_until='domcontentloaded')
        page.get_by_text('Create a new evaluation').first.wait_for(timeout=15000)
        page.locator('mat-select').first.click()
        page.wait_for_timeout(300)
        page.get_by_text('menuSuggestionFlow', exact=True).click()
        page.wait_for_timeout(300)
        page.locator('mat-select').nth(1).click()
        page.wait_for_timeout(300)
        page.get_by_text('menuSuggestionsDataset', exact=True).click()
        page.wait_for_timeout(300)
        hide_no_app(page)
        page.screenshot(path=str(out / 'eval-run.png'), type='png')
        page.close()

        # 8. eval-results
        page = browser.new_page(
            viewport={'width': 1212, 'height': 708},
            device_scale_factor=2,
            color_scheme='dark',
        )
        evals_dir = Path('/Users/huangjeff/Desktop/genkit-docsite-shots/sample/.genkit/evals')
        idx_file = evals_dir / 'index.json'
        eval_id = '68cd5928-3a88-4ed7-9329-5f7dafdb5383'
        if idx_file.exists():
            eval_idx = json.loads(idx_file.read_text())
            if eval_idx:
                eval_id = list(eval_idx.keys())[0]
        page.goto(f'{base}/datasets/menuSuggestionsDataset/evaluate/{eval_id}', wait_until='domcontentloaded')
        page.get_by_text('menuSuggestionFlow').first.wait_for(timeout=15000)
        page.wait_for_timeout(1000)
        hide_no_app(page)
        page.screenshot(path=str(out / 'eval-results.png'), type='png')
        page.close()

        browser.close()


def write_compare(out: Path) -> Path:
    shots = [
        'model-runner',
        'prompt-runner',
        'traces',
        'datasets',
        'dataset-create',
        'dataset-examples',
        'eval-run',
        'eval-results',
    ]
    parts = [COMPARE_HTML]
    for sid in shots:
        old_path = f'old/{sid}.png' if (out / f'old/{sid}.png').exists() else f'{sid}.png'
        parts.append(
            f'<section><h2>{sid}</h2><div class="pair">'
            f'<figure><figcaption>Live / Baseline</figcaption><img src="{old_path}" alt="live {sid}" /></figure>'
            f'<figure><figcaption>Proposed</figcaption><img src="{sid}.png" alt="proposed {sid}" /></figure>'
            f'</div></section>\n'
        )
    path = out / 'compare_batch2.html'
    path.write_text(''.join(parts))
    return path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--base-url', default='http://127.0.0.1:4104')
    p.add_argument('--out-dir', default=str(Path.home() / 'Desktop/genkit-docsite-shots/proposed'))
    args = p.parse_args()
    base = args.base_url.rstrip('/')
    out = Path(args.out_dir).expanduser()
    out.mkdir(parents=True, exist_ok=True)

    fetch_old(out)
    capture(base, out)
    compare = write_compare(out)
    print(f'Captured Batch 2 shots. Compare in {compare}')


if __name__ == '__main__':
    main()

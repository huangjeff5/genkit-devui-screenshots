#!/usr/bin/env python3
"""Unified production runner: stages traces, captures all Dev UI shots, builds GIF, and generates compare.html."""

import argparse
import json
import os
import subprocess
import time
from pathlib import Path
from playwright.sync_api import Page, sync_playwright

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_FILE = REPO_ROOT / "registry.json"

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

def stage_traces(python_bin: str, base_url: str):
    print("▶ Staging traces through Python runtime...")
    env = os.environ.copy()
    env["GENKIT_ENV"] = "dev"
    env["GOOGLE_CLOUD_PROJECT"] = "aim-testing"
    env["GENKIT_TELEMETRY_SERVER"] = "http://127.0.0.1:4033"

    stage_code = """
import asyncio
from sample_app import ai, menuSuggestionFlow, complexMenuSuggestionFlow, menuQuestionFlow, dishAdvisoryFlow, ThemeInput, MenuQuestion, DishQuery

async def main():
    try:
        await menuSuggestionFlow(ThemeInput(theme='medieval'))
        await complexMenuSuggestionFlow(ThemeInput(theme='medieval'))
        await menuQuestionFlow(MenuQuestion(question='What is a good starter for two people?'))
        await dishAdvisoryFlow(DishQuery(dish_name='Dragon Feast Haunch'))
        print("Traces staged successfully.")
    except Exception as e:
        print(f"Warning during trace staging: {e}")

asyncio.run(main())
"""
    subprocess.run([python_bin, "-c", stage_code], cwd=REPO_ROOT, env=env, check=False)
    time.sleep(1)

def run_capture(base_url: str, out_dir: Path, python_bin: str):
    out_dir.mkdir(parents=True, exist_ok=True)
    old_dir = out_dir / "old"
    old_dir.mkdir(exist_ok=True)

    stage_traces(python_bin, base_url)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1212, "height": 708},
            device_scale_factor=2,
            color_scheme="dark",
        )

        def new_page():
            return context.new_page()

        print("\n📸 Capturing Batch 1 & Batch 2 Primitives...")

        # 1. Home
        p_home = new_page()
        p_home.goto(f"{base_url}/", wait_until="domcontentloaded")
        p_home.get_by_text("Flows").first.wait_for(timeout=15000)
        p_home.wait_for_timeout(1000)
        hide_no_app(p_home)
        p_home.screenshot(path=str(out_dir / "home.png"))
        print("  ✓ home.png")
        p_home.close()

        # 2. Flow Runner
        p_flow = new_page()
        p_flow.goto(f"{base_url}/flows/menuSuggestionFlow", wait_until="domcontentloaded")
        p_flow.get_by_text("menuSuggestionFlow").first.wait_for(timeout=15000)
        p_flow.wait_for_timeout(500)
        p_flow.get_by_role("button", name="Run").click()
        p_flow.wait_for_timeout(3000)
        hide_no_app(p_flow)
        p_flow.screenshot(path=str(out_dir / "flow-runner.png"))
        print("  ✓ flow-runner.png")
        p_flow.close()

        # 3. Multi-Step Trace Inspect
        p_insp = new_page()
        p_insp.goto(f"{base_url}/traces", wait_until="domcontentloaded")
        p_insp.get_by_text("Traces").first.wait_for(timeout=15000)
        p_insp.wait_for_timeout(1000)
        complex_row = p_insp.locator("tr, a, div[role='row']").filter(has_text="complexMenuSuggestionFlow").first
        if complex_row.count():
            complex_row.click()
            p_insp.wait_for_timeout(1000)
        hide_no_app(p_insp)
        p_insp.screenshot(path=str(out_dir / "inspect.png"))
        print("  ✓ inspect.png")
        p_insp.close()

        # 4. Runstep
        p_step = new_page()
        p_step.goto(f"{base_url}/traces", wait_until="domcontentloaded")
        p_step.get_by_text("Traces").first.wait_for(timeout=15000)
        p_step.wait_for_timeout(1000)
        q_row = p_step.locator("tr, a, div[role='row']").filter(has_text="menuQuestionFlow").first
        if q_row.count():
            q_row.click()
            p_step.wait_for_timeout(1000)
        hide_no_app(p_step)
        p_step.screenshot(path=str(out_dir / "runstep.png"))
        print("  ✓ runstep.png")
        p_step.close()

        # 5. Model Runner
        p_mod = new_page()
        p_mod.goto(f"{base_url}/models/vertexai/gemini-2.5-flash", wait_until="domcontentloaded")
        p_mod.get_by_text("gemini-2.5-flash").first.wait_for(timeout=15000)
        p_mod.wait_for_timeout(500)
        p_mod.locator("textarea, [contenteditable='true']").first.fill("Suggest a dish for a medieval themed restaurant.")
        p_mod.get_by_role("button", name="Run").click()
        p_mod.wait_for_timeout(3500)
        hide_no_app(p_mod)
        p_mod.screenshot(path=str(out_dir / "model-runner.png"))
        print("  ✓ model-runner.png")
        p_mod.close()

        # 6. Prompt Runner (Hello)
        p_pr = new_page()
        p_pr.goto(f"{base_url}/prompts/hello", wait_until="domcontentloaded")
        p_pr.get_by_text("hello").first.wait_for(timeout=15000)
        p_pr.wait_for_timeout(500)
        p_pr.get_by_role("button", name="Run").click()
        p_pr.wait_for_timeout(3000)
        hide_no_app(p_pr)
        p_pr.screenshot(path=str(out_dir / "prompt-runner.png"))
        print("  ✓ prompt-runner.png")
        p_pr.close()

        # 7. Traces Table
        p_tr = new_page()
        p_tr.goto(f"{base_url}/traces", wait_until="domcontentloaded")
        p_tr.get_by_text("Traces").first.wait_for(timeout=15000)
        p_tr.wait_for_timeout(1000)
        hide_no_app(p_tr)
        p_tr.screenshot(path=str(out_dir / "traces.png"))
        print("  ✓ traces.png")
        p_tr.close()

        # 8. Datasets Overview
        p_ds = new_page()
        p_ds.goto(f"{base_url}/datasets", wait_until="domcontentloaded")
        p_ds.get_by_text("Datasets").first.wait_for(timeout=15000)
        p_ds.wait_for_timeout(500)
        hide_no_app(p_ds)
        p_ds.screenshot(path=str(out_dir / "datasets.png"))
        print("  ✓ datasets.png")

        # 9. Dataset Create Modal
        create_btn = p_ds.get_by_role("button", name="Create dataset").or_(p_ds.get_by_text("Create dataset").first)
        if create_btn.count():
            create_btn.click()
            p_ds.wait_for_timeout(500)
        hide_no_app(p_ds)
        p_ds.screenshot(path=str(out_dir / "dataset-create.png"))
        print("  ✓ dataset-create.png")
        p_ds.close()

        # 10. Dataset Examples Table
        p_ex = new_page()
        p_ex.goto(f"{base_url}/datasets/myFactsQaDataset", wait_until="domcontentloaded")
        p_ex.get_by_text("myFactsQaDataset").first.wait_for(timeout=15000)
        p_ex.wait_for_timeout(500)
        hide_no_app(p_ex)
        p_ex.screenshot(path=str(out_dir / "dataset-examples.png"))
        print("  ✓ dataset-examples.png")
        p_ex.close()

        # 11. Eval Run Modal & 12. Eval Results Table
        p_ev = new_page()
        p_ev.goto(f"{base_url}/evaluations", wait_until="domcontentloaded")
        p_ev.get_by_text("Evaluations").first.wait_for(timeout=15000)
        p_ev.wait_for_timeout(500)
        new_eval_btn = p_ev.get_by_role("button", name="Run new evaluation").or_(p_ev.get_by_text("Run new evaluation").first)
        if new_eval_btn.count():
            new_eval_btn.click()
            p_ev.wait_for_timeout(500)
        hide_no_app(p_ev)
        p_ev.screenshot(path=str(out_dir / "eval-run.png"))
        print("  ✓ eval-run.png")
        p_ev.close()

        p_evres = new_page()
        p_evres.goto(f"{base_url}/evaluations/eval-run-20260831-01", wait_until="domcontentloaded")
        p_evres.get_by_text("Evaluations").first.wait_for(timeout=15000)
        p_evres.wait_for_timeout(500)
        hide_no_app(p_evres)
        p_evres.screenshot(path=str(out_dir / "eval-results.png"))
        print("  ✓ eval-results.png")
        p_evres.close()

        print("\n⚡ Capturing New Proof Shots (Tools & Dotprompt)...")

        # 13. Standalone Tool Runner
        p_tl = new_page()
        p_tl.goto(f"{base_url}/tools/getDishDetails", wait_until="domcontentloaded")
        p_tl.get_by_text("getDishDetails").first.wait_for(timeout=15000)
        p_tl.wait_for_timeout(500)
        p_tl.get_by_role("button", name="Run").click()
        p_tl.wait_for_timeout(1000)
        hide_no_app(p_tl)
        p_tl.screenshot(path=str(out_dir / "devui_tool_runner_standalone.png"))
        print("  ✓ devui_tool_runner_standalone.png")
        p_tl.close()

        # 14. Tool Trace Waterfall Loop
        p_tloop = new_page()
        p_tloop.goto(f"{base_url}/traces", wait_until="domcontentloaded")
        p_tloop.get_by_text("Traces").first.wait_for(timeout=15000)
        p_tloop.wait_for_timeout(1000)
        dish_row = p_tloop.locator("tr, a, div[role='row']").filter(has_text="dishAdvisoryFlow").first
        if dish_row.count():
            dish_row.click()
            p_tloop.wait_for_timeout(1000)
        tool_node = p_tloop.locator(".span-tree-node, [role='treeitem'], div, span").filter(has_text="getDishDetails").first
        if tool_node.count():
            tool_node.click()
            p_tloop.wait_for_timeout(800)
        hide_no_app(p_tloop)
        p_tloop.screenshot(path=str(out_dir / "trace_tool_call_waterfall_loop.png"))
        print("  ✓ trace_tool_call_waterfall_loop.png")
        p_tloop.close()

        # 15. Dotprompt Live Variables Runner
        p_dp = new_page()
        p_dp.goto(f"{base_url}/prompts/welcome_guest", wait_until="domcontentloaded")
        p_dp.get_by_text("welcome_guest").first.wait_for(timeout=15000)
        p_dp.wait_for_timeout(500)
        p_dp.get_by_role("button", name="Run").click()
        p_dp.wait_for_timeout(3500)
        hide_no_app(p_dp)
        p_dp.screenshot(path=str(out_dir / "dotprompt_runner_live_variables.png"))
        print("  ✓ dotprompt_runner_live_variables.png")
        p_dp.close()

        browser.close()

    # Generate Animated GIF
    generate_overview_gif(base_url, out_dir)

    # Build Interactive HTML Comparison Dashboard
    build_compare_html(out_dir)

def generate_overview_gif(base_url: str, out_dir: Path):
    print("\n🎬 Generating High-Framerate Overview GIF...")
    raw_video_dir = out_dir / "raw_video"
    raw_video_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1212, "height": 708},
            device_scale_factor=2,
            color_scheme="dark",
            record_video_dir=str(raw_video_dir),
            record_video_size={"width": 1212, "height": 708},
        )
        page = context.new_page()
        page.goto(f"{base_url}/flows/menuSuggestionFlow", wait_until="domcontentloaded")
        page.get_by_text("menuSuggestionFlow").first.wait_for(timeout=15000)
        page.wait_for_timeout(800)
        hide_no_app(page)
        page.get_by_role("button", name="Run").click()
        page.wait_for_timeout(3200)

        # Slide over to trace
        view_trace_btn = page.get_by_text("View trace").or_(page.get_by_role("button", name="View trace")).first
        if view_trace_btn.count():
            view_trace_btn.click()
            page.wait_for_timeout(1800)
        hide_no_app(page)
        page.wait_for_timeout(1000)

        page.close()
        context.close()
        browser.close()

    video_files = list(raw_video_dir.glob("*.webm"))
    if not video_files:
        print("  ⚠ No video recorded for GIF conversion.")
        return

    latest_webm = sorted(video_files, key=lambda f: f.stat().st_mtime, reverse=True)[0]
    gif_path = out_dir / "genkit_developer_ui_overview.gif"

    ffmpeg_bin = "/opt/homebrew/bin/ffmpeg" if Path("/opt/homebrew/bin/ffmpeg").exists() else "ffmpeg"
    palette_path = out_dir / "palette.png"

    subprocess.run([
        ffmpeg_bin, "-y", "-i", str(latest_webm),
        "-vf", "fps=12,scale=1212:-1:flags=lanczos,palettegen",
        str(palette_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run([
        ffmpeg_bin, "-y", "-i", str(latest_webm), "-i", str(palette_path),
        "-lavfi", "fps=12,scale=1212:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=3",
        str(gif_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"  ✓ {gif_path.name} ({gif_path.stat().st_size // 1024} KB)")

def build_compare_html(out_dir: Path):
    print("\n📄 Building Interactive compare.html...")
    if not REGISTRY_FILE.exists():
        return
    registry = json.loads(REGISTRY_FILE.read_text())

    html = """<!doctype html>
<meta charset="utf-8" />
<title>Genkit Dev UI — Visual Verification Studio</title>
<style>
  :root { color-scheme: dark; }
  body { margin: 32px auto; font: 15px/1.55 ui-sans-serif, system-ui, -apple-system, sans-serif; background: #0f1015; color: #e3e2e6; max-width: 1400px; padding: 0 24px; }
  h1 { font-size: 26px; font-weight: 700; margin: 0 0 8px; color: #f8fafc; }
  .lead { color: #94a3b8; margin: 0 0 36px; font-size: 16px; }
  section { margin: 0 0 56px; border-top: 1px solid #1e293b; padding-top: 28px; }
  h2 { font-size: 19px; font-weight: 600; margin: 0 0 16px; display: flex; align-items: center; justify-content: space-between; }
  .badge { font-size: 12px; font-weight: 500; padding: 4px 10px; border-radius: 6px; background: #1e293b; color: #38bdf8; }
  .badge.new { background: #064e3b; color: #34d399; }
  .badge.gif { background: #581c87; color: #d8b4fe; }
  .pair { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .single-frame { width: 100%; }
  figure { margin: 0; }
  figcaption { font-size: 13px; font-weight: 600; letter-spacing: .04em; text-transform: uppercase; color: #94a3b8; margin: 0 0 10px; }
  img { width: 100%; height: auto; background: #090a0f; border: 1px solid #282e3e; border-radius: 8px; display: block; box-shadow: 0 4px 16px rgba(0,0,0,0.5); }
</style>

<h1>Genkit Developer UI — Visual Verification Studio</h1>
<p class="lead">Interactive proof artifacts, high-framerate streaming GIFs, and in-situ docsite integration previews.</p>
"""

    for item in registry:
        sid = item["id"]
        desc = item["description"]
        is_gif = item.get("format") == "gif"
        badge_class = "badge gif" if is_gif else "badge new"
        old_file = out_dir / "old" / f"{sid}.png"
        has_old = old_file.exists() and old_file.stat().st_size > 1000

        if is_gif:
            html += f"""
<section id="{sid}">
  <h2><span>{sid}</span> <span class="{badge_class}">{desc}</span></h2>
  <div class="single-frame">
    <figure>
      <figcaption>Animated Overview GIF</figcaption>
      <img src="{sid}.gif" alt="{sid}" />
    </figure>
  </div>
</section>
"""
        else:
            old_rel = f"old/{sid}.png" if has_old else f"{sid}.png"
            old_label = "Live Docsite" if has_old else "New Capture"
            html += f"""
<section id="{sid}">
  <h2><span>{sid}</span> <span class="{badge_class}">{desc}</span></h2>
  <div class="pair">
    <figure>
      <figcaption>{old_label}</figcaption>
      <img src="{old_rel}" alt="old {sid}" />
    </figure>
    <figure>
      <figcaption>Proposed High-Res Capture</figcaption>
      <img src="{sid}.png" alt="proposed {sid}" />
    </figure>
  </div>
</section>
"""

    (out_dir / "compare.html").write_text(html)
    print(f"  ✓ compare.html updated at {out_dir / 'compare.html'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture all Genkit Dev UI docsite shots")
    parser.add_argument("--base-url", default="http://127.0.0.1:4104", help="Developer UI base URL")
    parser.add_argument("--out-dir", default=str(Path.home() / "Desktop/genkit-docsite-shots/proposed"), help="Output directory")
    parser.add_argument("--python-bin", default="/Users/huangjeff/Desktop/genkit-python/.venv/bin/python", help="Python binary for sample app")
    args = parser.parse_args()

    run_capture(args.base_url, Path(args.out_dir), args.python_bin)

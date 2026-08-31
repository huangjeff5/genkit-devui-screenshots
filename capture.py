#!/usr/bin/env python3
"""Capture Dev UI screenshots, build animated overview GIF, capture full-page in-situ docsite views, and generate compare.html."""

import argparse
import os
import subprocess
import time
from pathlib import Path
from playwright.sync_api import Page, sync_playwright

REPO_ROOT = Path(__file__).resolve().parent

REFRESHED_SHOTS = [
    ("home", "Home Dashboard", "png"),
    ("flow-runner", "Flow Runner Interface", "png"),
    ("inspect", "Trace Waterfall Inspector", "png"),
    ("runstep", "Custom Step Telemetry (ai.run)", "png"),
    ("model-runner", "Model Runner & Configuration Drawer", "png"),
    ("prompt-runner", "Prompt Runner", "png"),
    ("genkit_developer_ui_overview", "Developer UI Overview Tour (GIF)", "gif"),
]

INSITU_SHOTS = [
    ("insitu_tool_calling_loop", "Tool Calling Guide: Waterfall Trace Loop (`docs/tool-calling`)", "png"),
    ("insitu_tool_runner_standalone", "Tool Calling Guide: Standalone Tool Runner (`docs/tool-calling`)", "png"),
    ("insitu_dotprompt_runner", "Dotprompt Guide: Live Variables & Prompt Testing (`docs/dotprompt`)", "png"),
    ("insitu_evaluation_results", "Evaluation Guide: Evaluation Results Matrix (`docs/evaluation`)", "png"),
]

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

def run_capture(base_url: str, docsite_url: str, out_dir: Path, python_bin: str):
    out_dir.mkdir(parents=True, exist_ok=True)
    old_dir = out_dir / "old"
    old_dir.mkdir(exist_ok=True)
    insitu_dir = out_dir / "in_situ"
    insitu_dir.mkdir(exist_ok=True)

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

        print("\n📸 Capturing Dev UI screenshots...")

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
        p_flow.get_by_role("button", name="Run").click(force=True)
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
        p_mod.goto(f"{base_url}/", wait_until="domcontentloaded")
        p_mod.get_by_text("Models").first.click()
        p_mod.get_by_text("gemini-2.5-flash").first.click()
        p_mod.wait_for_timeout(1000)
        p_mod.keyboard.press("Escape")
        p_mod.wait_for_timeout(500)
        p_mod.locator("textarea, [contenteditable='true']").first.fill("Suggest a dish for a medieval themed restaurant.")
        p_mod.get_by_role("button", name="Run").click(force=True)
        p_mod.wait_for_timeout(3500)
        hide_no_app(p_mod)
        p_mod.screenshot(path=str(out_dir / "model-runner.png"))
        print("  ✓ model-runner.png")
        p_mod.close()

        # 6. Prompt Runner
        p_pr = new_page()
        p_pr.goto(f"{base_url}/", wait_until="domcontentloaded")
        p_pr.get_by_text("Prompts").first.click()
        p_pr.get_by_text("hello").first.click()
        p_pr.wait_for_timeout(1000)
        p_pr.keyboard.press("Escape")
        p_pr.wait_for_timeout(500)
        p_pr.get_by_role("button", name="Run").click(force=True)
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

        browser.close()

    # Generate Animated GIF
    generate_overview_gif(base_url, out_dir)

    # Capture Full-Page In-Situ Docsite Views (1440x900 Laptop Standard)
    capture_insitu_views(docsite_url, insitu_dir)

    # Build Interactive HTML Comparison Dashboard
    build_compare_html(out_dir)

def generate_overview_gif(base_url: str, out_dir: Path):
    print("\n🎬 Generating overview GIF...")
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
        page.get_by_role("button", name="Run").click(force=True)
        page.wait_for_timeout(3200)

        view_trace_btn = page.get_by_text("View trace").or_(page.get_by_role("button", name="View trace")).first
        if view_trace_btn.count():
            view_trace_btn.click(force=True)
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

def capture_insitu_views(docsite_url: str, insitu_dir: Path):
    print("\n🔍 Capturing full in-situ docsite page views (1440x900 laptop standard)...")
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # 1. Tool Loop in Docsite Context
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2, color_scheme="dark")
        page.goto(f"{docsite_url}/docs/tool-calling/", wait_until="networkidle")
        time.sleep(1)
        img = page.locator("img[alt*='Inspecting tool calling']")
        if img.count():
            img.scroll_into_view_if_needed()
            time.sleep(0.5)
            # Scroll up slightly so surrounding context is visible
            page.evaluate("window.scrollBy(0, -120)")
            time.sleep(0.5)
            page.screenshot(path=str(insitu_dir / "insitu_tool_calling_loop.png"))
            print("  ✓ insitu_tool_calling_loop.png")
        page.close()

        # 2. Standalone Tool Runner in Docsite Context
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2, color_scheme="dark")
        page.goto(f"{docsite_url}/docs/tool-calling/", wait_until="networkidle")
        time.sleep(1)
        img = page.locator("img[alt*='Standalone tool runner']")
        if img.count():
            img.scroll_into_view_if_needed()
            time.sleep(0.5)
            page.evaluate("window.scrollBy(0, -120)")
            time.sleep(0.5)
            page.screenshot(path=str(insitu_dir / "insitu_tool_runner_standalone.png"))
            print("  ✓ insitu_tool_runner_standalone.png")
        page.close()

        # 3. Dotprompt Runner in Docsite Context
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2, color_scheme="dark")
        page.goto(f"{docsite_url}/docs/dotprompt/", wait_until="networkidle")
        time.sleep(1)
        img = page.locator("img[alt*='Dotprompt runner']")
        if img.count():
            img.scroll_into_view_if_needed()
            time.sleep(0.5)
            page.evaluate("window.scrollBy(0, -120)")
            time.sleep(0.5)
            page.screenshot(path=str(insitu_dir / "insitu_dotprompt_runner.png"))
            print("  ✓ insitu_dotprompt_runner.png")
        page.close()

        # 4. Evaluation Results in Docsite Context
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2, color_scheme="dark")
        page.goto(f"{docsite_url}/docs/evaluation/", wait_until="networkidle")
        time.sleep(1)
        img = page.locator("img[alt*='Evaluation run results']")
        if img.count():
            img.scroll_into_view_if_needed()
            time.sleep(0.5)
            page.evaluate("window.scrollBy(0, -120)")
            time.sleep(0.5)
            page.screenshot(path=str(insitu_dir / "insitu_evaluation_results.png"))
            print("  ✓ insitu_evaluation_results.png")
        page.close()

        browser.close()

def build_compare_html(out_dir: Path):
    print("\n📄 Building compare.html with full in-situ docsite views...")
    html = """<!doctype html>
<meta charset="utf-8" />
<title>Genkit Dev UI — Visual Verification Studio</title>
<style>
  :root { color-scheme: dark; }
  body { margin: 32px auto; font: 15px/1.55 ui-sans-serif, system-ui, -apple-system, sans-serif; background: #0f1015; color: #e3e2e6; max-width: 1400px; padding: 0 24px; }
  h1 { font-size: 26px; font-weight: 700; margin: 0 0 8px; color: #f8fafc; }
  .lead { color: #94a3b8; margin: 0 0 36px; font-size: 16px; }
  h2.section-header { font-size: 21px; font-weight: 700; color: #38bdf8; border-bottom: 2px solid #1e293b; padding-bottom: 10px; margin: 48px 0 24px; }
  section { margin: 0 0 48px; border-top: 1px solid #1e293b; padding-top: 24px; }
  h3 { font-size: 17px; font-weight: 600; margin: 0 0 16px; display: flex; align-items: center; justify-content: space-between; }
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
<p class="lead">Interactive proof artifacts, high-framerate streaming GIFs, and real in-situ docsite integration previews.</p>

<h2 class="section-header">Batch 1: Refreshed Existing Assets (Before vs. After)</h2>
"""

    for sid, desc, fmt in REFRESHED_SHOTS:
        is_gif = fmt == "gif"
        badge_class = "badge gif" if is_gif else "badge new"
        old_file = out_dir / "old" / f"{sid}.png"
        has_old = old_file.exists() and old_file.stat().st_size > 1000

        if is_gif:
            html += f"""
<section id="{sid}">
  <h3><span>{desc}</span> <span class="{badge_class}">public/{sid}.gif</span></h3>
  <div class="single-frame">
    <figure>
      <figcaption>Animated Overview GIF (12 fps, Lanczos Palette)</figcaption>
      <img src="{sid}.gif" alt="{sid}" />
    </figure>
  </div>
</section>
"""
        else:
            old_rel = f"old/{sid}.png" if has_old else f"{sid}.png"
            old_label = "Live Docsite (Old)" if has_old else "New Capture"
            html += f"""
<section id="{sid}">
  <h3><span>{desc}</span> <span class="{badge_class}">src/assets/{sid}.png</span></h3>
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

    html += """
<h2 class="section-header">Batch 2: Full In-Situ Docsite Previews (1440x900 Laptop Layout)</h2>
<p class="lead">Realistic browser viewport captures showing the actual layout: Left Navigation, Content Column, Typography, and Right Table of Contents.</p>
"""

    for card_id, desc, fmt in INSITU_SHOTS:
        html += f"""
<section id="{card_id}">
  <h3><span>{desc}</span> <span class="badge new">1440x900 Laptop View</span></h3>
  <div class="single-frame">
    <figure>
      <figcaption>Full Browser Viewport on Docsite</figcaption>
      <img src="in_situ/{card_id}.png" alt="{card_id}" />
    </figure>
  </div>
</section>
"""

    (out_dir / "compare.html").write_text(html)
    print(f"  ✓ compare.html updated at {out_dir / 'compare.html'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture all Genkit Dev UI docsite shots and full in-situ views")
    parser.add_argument("--base-url", default="http://127.0.0.1:4104", help="Developer UI base URL")
    parser.add_argument("--docsite-url", default="http://localhost:4321", help="Local Docsite preview URL")
    parser.add_argument("--out-dir", default=str(Path.home() / "Desktop/genkit-docsite-shots/proposed"), help="Output directory")
    parser.add_argument("--python-bin", default="/Users/huangjeff/Desktop/genkit-python/.venv/bin/python", help="Python binary for sample app")
    args = parser.parse_args()

    run_capture(args.base_url, args.docsite_url, Path(args.out_dir), args.python_bin)

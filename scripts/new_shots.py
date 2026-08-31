#!/usr/bin/env python3
"""Capture high-value 'Aha!' moment screenshots and animated developer overview GIF."""

import json
import os
import subprocess
import time
from pathlib import Path
from playwright.sync_api import Page, sync_playwright

OUT_DIR = Path("/Users/huangjeff/Desktop/genkit-docsite-shots/proposed")
OUT_DIR.mkdir(parents=True, exist_ok=True)
BASE_URL = "http://127.0.0.1:4104"

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

def capture_new_shots():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # 1. Tool Runner Standalone
        page = browser.new_page(
            viewport={"width": 1212, "height": 708},
            device_scale_factor=2,
            color_scheme="dark",
        )
        page.goto(f"{BASE_URL}/tools/getDishDetails", wait_until="domcontentloaded")
        page.get_by_text("getDishDetails").first.wait_for(timeout=15000)
        page.wait_for_timeout(500)
        # Click Run
        page.get_by_role("button", name="Run").click()
        page.wait_for_timeout(1000)
        hide_no_app(page)
        page.screenshot(path=str(OUT_DIR / "devui_tool_runner_standalone.png"))
        print("Captured devui_tool_runner_standalone.png")
        page.close()

        # 2. Trace view showing tool call inspection
        page = browser.new_page(
            viewport={"width": 1212, "height": 708},
            device_scale_factor=2,
            color_scheme="dark",
        )
        page.goto(f"{BASE_URL}/traces", wait_until="domcontentloaded")
        page.get_by_text("Traces").first.wait_for(timeout=15000)
        page.wait_for_timeout(1000)
        # Click the top trace (dishAdvisoryFlow)
        dish_row = page.locator("tr, a, div[role='row']").filter(has_text="dishAdvisoryFlow").first
        if dish_row.count():
            dish_row.click()
            page.wait_for_timeout(1000)
        # Click specifically on the getDishDetails span in the tree
        tool_node = page.locator(".span-tree-node, [role='treeitem'], div, span").filter(has_text="getDishDetails").first
        if tool_node.count():
            tool_node.click()
            page.wait_for_timeout(800)
        hide_no_app(page)
        page.screenshot(path=str(OUT_DIR / "trace_tool_call_waterfall_loop.png"))
        print("Captured trace_tool_call_waterfall_loop.png")
        page.close()

        # 3. Dotprompt Runner with Live Variables
        page = browser.new_page(
            viewport={"width": 1212, "height": 708},
            device_scale_factor=2,
            color_scheme="dark",
        )
        page.goto(f"{BASE_URL}/prompts/welcome_guest", wait_until="domcontentloaded")
        page.get_by_text("welcome_guest").first.wait_for(timeout=15000)
        page.wait_for_timeout(500)
        page.get_by_role("button", name="Run").click()
        page.wait_for_timeout(4000)
        hide_no_app(page)
        page.screenshot(path=str(OUT_DIR / "dotprompt_runner_live_variables.png"))
        print("Captured dotprompt_runner_live_variables.png")
        page.close()

        browser.close()

if __name__ == "__main__":
    capture_new_shots()

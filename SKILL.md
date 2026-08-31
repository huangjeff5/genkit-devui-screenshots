---
name: genkit-devui-screenshots
description: >-
  Audit Genkit docs for Dev UI opportunities, capture visual proof (GIFs and high-DPI screenshots)
  with intelligent DOM-anchored cropping, and compose GitHub PRs with 1440x900 in-situ previews.
---

# Dev UI docsite screenshots & visual PR pipeline

The Developer UI is Genkit's primary advantage over other frameworks, but our docs often describe complex runtime behaviors (tool loops, streaming, interrupts, evaluations) in abstract text without showing what the UI looks like.

Your job is:
1. Scan the docs to find open loops where a screenshot or short GIF closes a gap for a developer or coding agent.
2. Cleanly start/restart the sample app on isolated port 4104 and capture the Dev UI assets.
3. Automatically apply intelligent DOM-anchored cropping to eliminate edge artifacts.
4. Capture full 1440x900 in-situ docsite viewport screenshots on the running local docsite (`http://localhost:4321`).
5. Push in-situ preview cards to `huangjeff5/genkit-devui-screenshots/previews/`.
6. Compose the GitHub PR using `gh pr create` with the in-situ screenshots embedded in the PR description ONLY. Never include preview cards in the target docsite changeset.

---

## Intelligent Cropping Standards (One-Shot Execution)

To guarantee zero human intervention on cropping, always enforce these 4 mathematical invariants:

1. **Full Workbench vs. Isolated Subview**:
   - **Full Workbench Views** (`home`, `flow-runner`, `model-runner`, `prompt-runner`): Capture the full `1212x708` viewport with 2x Retina scaling.
   - **Trace Inspector Views** (`inspect`): Snap cleanly to the workbench root (`mat-drawer-content` / `x: 290..1212`). Never include a partial slice of the left navigation sidebar or its bottom collapse chevron.
   - **Isolated Tree Subviews** (`runstep`): Anchor to the tree container (`x: 270`, `y: 47`, `width: 304`, `height: 220`).
2. **Top Header Invariant**:
   - Header bars must include the entire top container block (`y: 47` in trace trees), providing 16–20px of breathing room above chevrons and icons. Never slice through top icons or text ascenders.
3. **Right Perimeter Invariant**:
   - Trace tree cards must end cleanly after the rightmost status badge/checkmarks (`width: 304`), terminating before the vertical panel divider line. Never include 1–2px line fragments or sliced text from the adjacent panel.
4. **Bottom Padding Invariant**:
   - Provide a minimum of 16px padding below the final child leaf node.

---

## Running the pipeline

```bash
# 1. Start the starter app on 4104 (clean restart)
export GENKIT_ENV=dev
export GOOGLE_CLOUD_PROJECT=aim-testing
cd ~/Desktop/genkit-devui-screenshots
genkit start -p 4104 -- /Users/huangjeff/Desktop/genkit-python/.venv/bin/python sample_app.py

# 2. Run intelligent capture engine + build overview GIF + capture 1440x900 in-situ views
python3 ~/Desktop/genkit-devui-screenshots/capture.py \
  --base-url http://127.0.0.1:4104 \
  --docsite-url http://localhost:4321 \
  --out-dir ~/Desktop/genkit-docsite-shots/proposed

# 3. Open comparison dashboard
open ~/Desktop/genkit-docsite-shots/proposed/compare.html
```

---

## Fresh-Eyes Visual QA Subagent Protocol

Before opening or updating a PR, the agent invokes an adversarial Visual QA Subagent to audit all PNGs in `previews/` against 4 criteria:

1. **Perimeter & Crop Slicing**: Inspect the outer 10px perimeter of every card. Reject if there are cut-off divider lines, adjacent panel slivers, stray 1px borders, or partial background bleeding.
2. **Icon & Label Integrity**: Confirm green checkmarks, latency badges (e.g., `1ms`, `2.23s`), and function names are 100% intact with comfortable padding.
3. **Zero Unpopulated Artifacts**: Verify that no "No app detected" strings, blank JSON inputs, or uninitialized spinners appear.
4. **In-Situ Docsite Flow (1440x900)**: Inspect the docsite context image. Verify that the image width, typography, and vertical spacing integrate smoothly with the documentation text without overpowering the column.

---

## PR Creation Checklist

- [ ] Target branch contains ONLY the modified `.mdx` files and legitimate `src/assets/` images (0 preview card files).
- [ ] In-situ viewport screenshots (1440x900) pushed to `huangjeff5/genkit-devui-screenshots/previews/`.
- [ ] PR description embeds the in-situ viewports and Before vs. After comparison tables via public raw GitHub URLs.
- [ ] `pnpm generate-language-pages` run and verified with 0 errors.

---
name: genkit-devui-screenshots
description: >-
  Capture Genkit Developer UI screenshots and animated GIFs for the genkit-ai/docsite,
  generate interactive visual diffs in compare.html, and sync approved assets to docsite.
  Use when the user mentions docsite screenshots, Dev UI screenshots, Developer UI pictures,
  "vet the shots", updating genkit.dev images of the local UI, or running the screenshot pipeline.
---

# Dev UI Docsite Screenshots & Visual Proof Pipeline

A deterministic, one-command pipeline that stages traces on a frozen sample app, captures 2x Retina screenshots and Lanczos palette GIFs across all Genkit primitives, builds an interactive visual diff dashboard (`compare.html`), and syncs approved assets into `genkit-docsite`.

Docs live in [genkit-ai/docsite](https://github.com/genkit-ai/docsite).

---

## 🚫 Critical Rules

- **Do not touch port 4000**: That is a user's persistent UI. The screenshot UI runs on isolated port **4104**.
- **Do not screenshot at scale 1**: Always capture at `device_scale_factor=2` with `color_scheme="dark"` and `viewport={"width": 1212, "height": 708}`.
- **Do not introduce catalog junk**: Use the frozen `TinyVertex` in `sample/app.py` so only defined models appear.
- **Clean frame requirement**: Mask any `No app detected` chips to `sample`, dismiss transient toast overlays, and verify trace timelines before capturing.

---

## 🚀 One-Command Execution

```bash
# REPO is this clone, e.g. ~/Desktop/genkit-devui-screenshots

# 1. Stage and run the frozen starter on port 4104 (if not already running)
mkdir -p ~/Desktop/genkit-docsite-shots/sample
cp "$REPO/sample/app.py" ~/Desktop/genkit-docsite-shots/sample/app.py

export GENKIT_ENV=dev
export GOOGLE_CLOUD_PROJECT=aim-testing
cd ~/Desktop/genkit-docsite-shots/sample
genkit start -p 4104 -- /Users/huangjeff/Desktop/genkit-python/.venv/bin/python app.py

# 2. Run the unified capture engine (stages traces, captures all 15 assets, builds GIF & compare.html)
python3 "$REPO/scripts/capture_all.py" \
  --base-url http://127.0.0.1:4104 \
  --out-dir ~/Desktop/genkit-docsite-shots/proposed

# 3. Open the visual review dashboard
open ~/Desktop/genkit-docsite-shots/proposed/compare.html
```

---

## 🔍 Self-Review Rubric (Required Before Sharing)

For every captured asset, inspect the pixels against the 4 criteria:

| # | Criterion | Rule |
| :--- | :--- | :--- |
| 1 | **The Beat** | Can a developer understand the core feature in 2 seconds without reading a caption? |
| 2 | **No Junk** | Zero transient error toasts, clean trace timelines, no `No app detected` text, no empty tabs. |
| 3 | **The Crop** | Standard 1212x708 frame, high-DPI (2x Retina), consistent dark mode padding. |
| 4 | **Vs Old** | The proposed capture must be strictly higher information density and cleaner than the live docsite baseline. |

---

## 📦 Syncing Approved Assets to Docsite

Once the PM approves the shots in `compare.html`:

```bash
python3 "$REPO/scripts/sync_to_docsite.py" \
  --shots-dir ~/Desktop/genkit-docsite-shots/proposed \
  --docsite-dir ~/Desktop/genkit-docsite
```

Then commit and push the updated docsite branch.

---
name: genkit-devui-screenshots
description: >-
  Audit Genkit docs for Dev UI opportunities, capture visual proof (GIFs and high-DPI screenshots),
  and present proposals for review before updating genkit-docsite.
---

# Dev UI docsite screenshots & opportunity scout

The Developer UI is Genkit's primary advantage over other frameworks, but our docs often describe complex runtime behaviors (tool loops, streaming, interrupts, evaluations) in abstract text without showing what the UI looks like.

Your job is:
1. Ensure `genkit-docsite` is up to date (`git pull origin main`).
2. Scan the docs to find open loops where a screenshot or short GIF closes a gap for a developer or coding agent.
3. Cleanly start/restart the sample app on isolated port 4104 and capture the shot.
4. Review old vs new with fresh eyes. Reject anything that requires explanation.
5. Show the user only clean survivors in `compare.html`.

Docs live in [genkit-ai/docsite](https://github.com/genkit-ai/docsite). Never land or copy assets until the user approves them.

---

## Rules & Hygiene

- **Sync docs first**: Always pull `main` on `genkit-docsite` before auditing or editing.
- **Do not touch port 4000**. That is the user's persistent UI. Screenshot UI is always **4104**. Kill and restart stale 4104 processes if the sample app changed.
- **Do not screenshot at scale 1**. Always use `device_scale_factor=2`, `color_scheme="dark"`, and viewport `1212x708`.
- **Do not use full VertexAI() or GoogleAI() plugins**. Use the frozen `TinyVertex` in `sample/app.py` so only defined models appear.
- **No UI junk**. Mask any `No app detected` text to `sample`, dismiss toasts, and keep the frame clean.
- **GIF vs Screenshot**:
  - **GIF** (3–8s loop, 12 fps): real-time streaming, pause/resume interrupts, parameter slider testing, or trace tree expanding.
  - **Screenshot** (PNG): static schemas, trace waterfalls, latency tables, or evaluation scoreboards.

---

## Running the pipeline

```bash
# 1. Ensure latest docsite main
cd ~/Desktop/genkit-docsite && git pull origin main

# 2. Start the starter app on 4104 (clean restart)
export GENKIT_ENV=dev
export GOOGLE_CLOUD_PROJECT=aim-testing
cd ~/Desktop/genkit-docsite-shots/sample
genkit start -p 4104 -- /Users/huangjeff/Desktop/genkit-python/.venv/bin/python app.py

# 3. Stage traces + capture all shots + build overview GIF + generate compare.html
python3 ~/Desktop/genkit-devui-screenshots/scripts/capture_all.py \
  --base-url http://127.0.0.1:4104 \
  --out-dir ~/Desktop/genkit-docsite-shots/proposed

# 4. Open comparison dashboard
open ~/Desktop/genkit-docsite-shots/proposed/compare.html
```

---

## Review rubric (before showing the user)

Open the pixels directly. Reject and retake any shot that fails any of these:

- **Beat**: Fail if a stranger cannot understand the single point in two seconds without reading a caption.
- **Junk**: Fail if there is `No app detected` text, error toast overlays, empty tabs, or raw stack traces.
- **Crop**: Fail if the frame is not standard 1212x708 dark-mode or is blurry.
- **Vs Old**: Fail if the proposed capture has lower information density or is harder to scan than what is currently live.

Any fail is a retake. Do not show failed shots.

---

## Syncing approved shots

Once the user approves the shots in `compare.html`:

```bash
# 1. Copy approved assets
python3 ~/Desktop/genkit-devui-screenshots/scripts/sync_to_docsite.py \
  --shots-dir ~/Desktop/genkit-docsite-shots/proposed \
  --docsite-dir ~/Desktop/genkit-docsite

# 2. Re-generate language pages and verify build
cd ~/Desktop/genkit-docsite && pnpm generate-language-pages
```

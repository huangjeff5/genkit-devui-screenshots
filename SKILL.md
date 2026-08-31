---
name: genkit-devui-screenshots
description: >-
  Audit Genkit docs for Dev UI opportunities, capture visual proof (GIFs and high-DPI screenshots),
  and present proposals for review before updating docs.
---

# Dev UI docsite screenshots & opportunity scout

The Developer UI is Genkit's primary advantage over other frameworks, but our docs often describe complex runtime behaviors (tool loops, streaming, interrupts, evaluations) in abstract text without showing what the UI looks like.

Your job is:
1. Scan the docs to find open loops where a screenshot or short GIF closes a gap for a developer or coding agent.
2. Cleanly start/restart the sample app on isolated port 4104 and capture the shot.
3. Review old vs new with fresh eyes. Reject anything that requires explanation.
4. Show the user only clean survivors in `compare.html`.
5. Slot approved assets into the target docsite on-demand.

---

## Rules & Hygiene

- **Do not touch port 4000**. That is the user's persistent UI. Screenshot UI is always **4104**.
- **Do not screenshot at scale 1**. Always use `device_scale_factor=2`, `color_scheme="dark"`, and viewport `1212x708`.
- **Do not use full VertexAI() or GoogleAI() plugins**. Use the frozen `TinyVertex` in `sample_app.py` so only defined models appear.
- **No UI junk**. Mask any `No app detected` text to `sample`, dismiss toasts, and keep the frame clean.
- **GIF vs Screenshot**:
  - **GIF** (3–8s loop, 12 fps): real-time streaming, pause/resume interrupts, parameter slider testing, or trace tree expanding.
  - **Screenshot** (PNG): static schemas, trace waterfalls, latency tables, or evaluation scoreboards.

---

## Running the pipeline

```bash
# 1. Start the starter app on 4104 (clean restart)
export GENKIT_ENV=dev
export GOOGLE_CLOUD_PROJECT=aim-testing
cd ~/Desktop/genkit-devui-screenshots
genkit start -p 4104 -- /Users/huangjeff/Desktop/genkit-python/.venv/bin/python sample_app.py

# 2. Stage traces + capture all shots + build overview GIF + generate compare.html
python3 ~/Desktop/genkit-devui-screenshots/capture.py \
  --base-url http://127.0.0.1:4104 \
  --out-dir ~/Desktop/genkit-docsite-shots/proposed

# 3. Open comparison dashboard
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

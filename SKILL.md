---
name: genkit-devui-screenshots
description: >-
  Audit Genkit docs for Dev UI opportunities, capture visual proof (GIFs and high-DPI screenshots),
  and compose GitHub PRs with full in-situ docsite viewport previews in the PR description only.
---

# Dev UI docsite screenshots & visual PR pipeline

The Developer UI is Genkit's primary advantage over other frameworks, but our docs often describe complex runtime behaviors (tool loops, streaming, interrupts, evaluations) in abstract text without showing what the UI looks like.

Your job is:
1. Scan the docs to find open loops where a screenshot or short GIF closes a gap for a developer or coding agent.
2. Cleanly start/restart the sample app on isolated port 4104 and capture the Dev UI assets.
3. Capture full 1440x900 in-situ docsite viewport screenshots on the running local docsite (`http://localhost:4321`).
4. Push in-situ preview cards to `huangjeff5/genkit-devui-screenshots/previews/`.
5. Compose the GitHub PR using `gh pr create` with the in-situ screenshots embedded in the PR description ONLY. Never include preview cards in the target docsite changeset.

---

## Strict Rules

- **Do not touch port 4000**. That is the user's persistent UI. Screenshot UI is always **4104**.
- **Do not screenshot at scale 1**. Always use `device_scale_factor=2`, `color_scheme="dark"`, and standard viewport `1212x708`.
- **Do not use full VertexAI() or GoogleAI() plugins**. Use the frozen `TinyVertex` in `sample_app.py` so only defined models appear.
- **In-Situ Viewports Must Be Full-Width (1440x900)**: Capture the full 3-column browser layout (left navigation + center content + right TOC) so reviewers can verify sizing, typography balance, and margins at a glance. Never crop tightly or zoom in.
- **Zero Changeset Contamination**: In-situ docsite screenshots belong in the **PR description ONLY**, hosted externally in `huangjeff5/genkit-devui-screenshots/previews/`. Never commit preview cards to the `genkit-ai/docsite` branch.
- **GIF vs Screenshot**:
  - **GIF** (3–8s loop, 12 fps, Lanczos): real-time streaming, pause/resume interrupts, parameter slider testing, or trace tree expanding.
  - **Screenshot** (PNG): static schemas, trace waterfalls, latency tables, or evaluation scoreboards.

---

## Running the pipeline

```bash
# 1. Start the starter app on 4104 (clean restart)
export GENKIT_ENV=dev
export GOOGLE_CLOUD_PROJECT=aim-testing
cd ~/Desktop/genkit-devui-screenshots
genkit start -p 4104 -- /Users/huangjeff/Desktop/genkit-python/.venv/bin/python sample_app.py

# 2. Run capture engine + build overview GIF + capture 1440x900 in-situ views
python3 ~/Desktop/genkit-devui-screenshots/capture.py \
  --base-url http://127.0.0.1:4104 \
  --docsite-url http://localhost:4321 \
  --out-dir ~/Desktop/genkit-docsite-shots/proposed

# 3. Open comparison dashboard
open ~/Desktop/genkit-docsite-shots/proposed/compare.html
```

---

## PR Creation Checklist

When submitting a pull request to `genkit-ai/docsite`:

- [ ] Target branch contains ONLY the modified `.mdx` files and legitimate `src/assets/` images (0 preview card files).
- [ ] In-situ viewport screenshots (1440x900) pushed to `huangjeff5/genkit-devui-screenshots/previews/`.
- [ ] PR description embeds the in-situ viewports and Before vs. After comparison tables via public raw GitHub URLs.
- [ ] `pnpm generate-language-pages` run and verified with 0 errors.

---

## 3. Fresh-Eyes Visual QA Subagent Protocol

To prevent author blindness and ensure zero cropped debris or perimeter artifacts, **every batch of screenshots MUST be passed to an independent Visual QA Subagent** before opening or updating a PR.

### Subagent Prompt Template

```text
Role: Visual QA & Staff Design Reviewer
Task: Inspect all generated screenshot PNGs and in-situ 1440x900 viewport captures in `previews/` using `view_file`.

Audit each image against these 4 strict criteria:
1. Perimeter & Crop Slicing: Check the outer 10px perimeter of every cropped card. Reject if there are cut-off divider lines, adjacent panel slivers, stray 1px borders, or partial background bleeding.
2. Icon & Label Integrity: Confirm green checkmarks, latency badges (e.g., `1ms`, `2.23s`), and function names are 100% intact with comfortable padding.
3. Zero Unpopulated Artifacts: Verify that no "No app detected" strings, blank JSON inputs, or uninitialized spinners appear.
4. In-Situ Docsite Flow (1440x900): Inspect the docsite context image. Verify that the image width, typography, and vertical spacing integrate smoothly with the documentation text without overpowering the column.

Return a pass/fail verdict with exact pixel/coordinate adjustments for any failures.
```

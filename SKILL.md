---
name: genkit-devui-screenshots
description: >-
  Audit Genkit documentation, discover high-impact Dev UI "Aha!" moment opportunities,
  capture visual proof (GIFs & high-DPI screenshots), and propose doc updates for PM review.
  Use when the user asks to "audit docs for Dev UI opportunities", "find aha moments",
  "propose new screenshots/gifs", "vet the shots", or "update docsite images".
---

# Dev UI Docsite Opportunity Scout & Visual Proof Pipeline

An intelligent, autonomous system for continuously scanning Genkit documentation, identifying high-leverage opportunities to showcase the Developer UI ("secret sauce"), generating live sample fixtures to capture the visual proof, and presenting rich in-situ proposals for PM approval.

---

## 🎯 The Core Mission: Finding "Aha!" Moments

Do not just refresh existing images. Actively audit the documentation to find where showing the Dev UI creates a high-value breakthrough for developers and coding agents:

1. **Closing Open Loops**: When docs explain a complex lifecycle (e.g. multi-turn tool loops, human-in-the-loop interrupts, recursive delegation), capture the trace waterfall that *proves* it visually.
2. **Eliminating Abstraction**: When docs describe typed schemas or configuration options, capture the auto-generated GUI forms and dynamic variable previewers.
3. **Format Decision Rubric**:
   - **🎬 Animated GIF (3–8s, Lanczos palette)**: For real-time streaming, pause/resume interrupt forms, parameter slider testing, or expandable trace trees.
   - **📸 Static Screenshot (2x Retina, Dark Mode)**: For structural data, schema validation trees, multi-span latency waterfalls, and correlated log streams.

---

## 🚫 Critical Guardrails

- **Never touch port 4000**: That is a user's persistent UI. Always use isolated port **4104**.
- **Never screenshot at scale 1**: Always use `device_scale_factor=2`, `color_scheme="dark"`, and standard viewport `1212x708`.
- **Zero catalog clutter**: Use isolated model fixtures (e.g. `TinyVertex`) so only the relevant models appear.
- **Clean frame requirement**: Mask `No app detected` text to `sample` and ensure zero transient error toasts.

---

## 🔄 The Autonomous Execution Loop

When a user asks to audit docs or propose new Dev UI features:

### Step 1: Scan & Identify Opportunities
- Audit `genkit-docsite/src/content/docs/docs/` for sections explaining abstract concepts without visual UI grounding.
- For each opportunity, define the exact code sample and matching Dev UI state.

### Step 2: Build Fixture & Trigger State
- Add the necessary flow, tool, prompt, or evaluator to `sample/app.py`.
- Run the flow with `GENKIT_TELEMETRY_SERVER=http://127.0.0.1:4033` to populate realistic trace telemetry.

### Step 3: Capture Visual Proof
- Run Playwright to capture 2x Retina screenshots or record video $\rightarrow$ convert with `ffmpeg` palettegen into a clean GIF.
- Save assets to `~/Desktop/genkit-docsite-shots/proposed/`.

### Step 4: Build In-Situ PM Comparison Studio
- Generate `~/Desktop/genkit-docsite-shots/proposed/compare.html` showing:
  - The animated GIFs and high-res screenshots.
  - The side-by-side code $\leftrightarrow$ UI pairing.
  - A realistic preview of how the doc page will look with the asset embedded.
- Open `compare.html` in the user's default browser.

### Step 5: Slot into Docsite upon Approval
- When the PM approves specific proposals, copy the assets to `genkit-docsite/src/assets/` or `genkit-docsite/public/`.
- Update the target `.mdx` doc files with appropriate markdown embeds and explanatory context.
- Run `pnpm dev` in `genkit-docsite` to let the PM preview the live documentation site.

# Genkit Dev UI docsite screenshots & visual engineering playbook

Comprehensive tooling and operational playbook for auditing the Genkit documentation, capturing high-DPI Developer UI proof artifacts (screenshots, animated GIFs, and 1080p video walkthroughs) across complex runtime scenarios, and submitting zero-noise GitHub PRs with full in-situ previews.

---

## Why this exists

1. **Dev UI is tribal knowledge**: The core team uses the Developer UI daily for rapid prototyping and trace debugging, but docs often fail to show external developers (and autonomous coding agents) that this exists out of the box.
2. **Closing conceptual loops**: Explaining recursive tool loops, agentic human interrupts, session state mutation, or scored evaluations with text alone leaves open loops. Visual proof closes the loop.
3. **Multi-format visual proof**: Simple features need a high-DPI screenshot; streaming needs an animated GIF; multi-turn agent execution with mutable state needs an interactive, 1080p Full HD video walkthrough.
4. **Zero-overhead review**: PR descriptions embed full 1440×900 in-situ viewport previews hosted externally, allowing reviewers to verify typography, margins, and placement in 60 seconds without checking out branches or running Astro locally.
5. **Decoupled architecture**: Preview assets live in this public repository (`previews/`), keeping the target `genkit-ai/docsite` changeset 100% clean.

---

## Scenario Catalog

This playbook is tuned for the full spectrum of Genkit capabilities:

- **Autonomous Agents & Mutable Session State (1080p Video Walkthrough)**: Multi-turn tool loops, trace waterfall visualization, session state expansion (`expand_all`), and smooth scrolling of live state mutations.
- **Recursive Tool Calling**: Nested trace trees showing `generate` $\rightarrow$ `tool(1ms)` $\rightarrow$ model synthesis.
- **Standalone Tool Runner**: Auto-generated GUI forms populated directly from Zod and Pydantic schemas.
- **Live Token Streaming**: 12 fps Lanczos-palette animated GIFs capturing real-time token streaming.
- **Human-in-the-Loop Interrupts**: Paused flow states with resumption forms and approval actions.
- **Dotprompt Engineering**: Real-time Handlebars variable resolution with typed schema form inputs.
- **Evaluations & Scoring**: LLM-as-a-judge results matrices, metric breakdowns, and dataset inspection.
- **Custom Step Telemetry**: Isolated `ai.run()` execution spans nested inside parent flow traces.

---

## Copy-Paste Jetski Prompts

### 1. Full Documentation Opportunity Scout
```text
Audit our documentation and look for high-impact opportunities where showcasing the Genkit Dev UI will create "aha!" moments or close open loops for developers.

For any page that could benefit from visual proof:
1. Decide whether a static screenshot, animated GIF, or 1080p video walkthrough is best.
2. Write the sample code needed to trigger that Dev UI state.
3. Capture the visual proof on isolated port 4104 (restart the starter app cleanly if already running).
4. Capture full 1440x900 in-situ docsite viewport screenshots from the local docsite.
5. Open compare.html showing the proposed assets embedded alongside the matching doc text so I can review them.
```

### 2. Audit a Specific Page or Concept
```text
Analyze docs/agents/overview.mdx. Find where developers will have questions about how agents, tools, and session state look in the Dev UI. Record a 1080p video walkthrough with 20% zoom and expanded session state, and show me a proposal with full 1440x900 in-situ viewport previews in compare.html.
```

### 3. Approve and Open PR
```text
I like proposals #1, #2, and #4 from compare.html. Please slot those screenshots/GIFs/videos and text adjustments into the docsite branch, push the 1440x900 in-situ preview cards to huangjeff5/genkit-devui-screenshots/previews/, and open a PR with the in-situ screenshots embedded in the PR description only (keeping the docsite git diff 100% clean).
```

---

## Execution Standards

- **Resolution & Scaling (Screenshots)**: All screenshots captured at `device_scale_factor=2`, dark theme, `1212x708` standard workspace size.
- **Video Walkthroughs**:
  - **Resolution & Zoom**: Viewport `1600 × 900` at `device_scale_factor=2` (20% visual zoom), upscaled to `1920 × 1080` in ffmpeg with Lanczos interpolation. Avoid CSS `zoom: 1.2` which breaks Angular Material layouts.
  - **Zero White Flicker**: Trim initial Chromium initialization frames (`ffmpeg -ss 2.0`) so playback starts on a solid dark interface.
  - **H.264 & Faststart**: Encoded with `libx264` CRF 16, `yuv420p`, and `-movflags +faststart`.
  - **Session State Tree**: Expand JSON with `expand_all` and smoothly scroll down the container to reveal updated state.
  - **Fallback Poster**: Always generate a high-DPI companion poster image (`<name>.png`).
  - **Realistic Data**: Production engineering scenarios; breadcrumb placeholder replaced with a clean app name.
- **GIF Optimization**: 12 fps, Lanczos color palette generation with Bayer dithering for smooth streaming playback under 3 MB.
- **Intelligent Bounding**: Snap to DOM elements (`mat-drawer-content`, `mat-tree`) to guarantee zero sliced dividers, border lines, or perimeter artifacts.
- **Fresh-Eyes QA Subagent**: Every batch is audited by an adversarial visual QA subagent before submitting PRs.

---

## Repository Structure

- `README.md`: Scenario catalog, engineering principles & copy-paste prompts.
- `SKILL.md`: Autonomous agent instructions, video recording standards, DOM cropping invariants, and review rubric.
- `sample_app.py`: Frozen starter app with models, flows, tools, prompts, and traces.
- `capture.py`: Automated Playwright capture engine, ffmpeg GIF converter, and in-situ viewport generator.
- `previews/`: Hosted full-page in-situ viewport screenshots for PR descriptions.

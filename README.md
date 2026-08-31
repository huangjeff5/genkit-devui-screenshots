# Genkit Dev UI docsite screenshots & visual engineering playbook

Comprehensive tooling and operational playbook for auditing the Genkit documentation, capturing high-DPI Developer UI proof artifacts across complex runtime scenarios, and submitting zero-noise GitHub PRs with full in-situ previews.

---

## Why this exists

1. **Dev UI is tribal knowledge**: The core team uses the Developer UI daily for rapid prototyping and trace debugging, but docs often fail to show external developers (and autonomous coding agents) that this exists out of the box.
2. **Closing conceptual loops**: Explaining recursive tool loops, agentic human interrupts, or scored evaluations with text alone leaves open loops. Visual proof closes the loop.
3. **Zero-overhead review**: PR descriptions embed full 1440×900 in-situ viewport previews hosted externally, allowing reviewers to verify typography, margins, and placement in 60 seconds without checking out branches or running Astro locally.
4. **Decoupled architecture**: Preview assets live in this public repository (`previews/`), keeping the target `genkit-ai/docsite` changeset 100% clean.

---

## Scenario Catalog

This playbook is tuned for the full spectrum of Genkit capabilities:

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
1. Decide whether an animated GIF or a static screenshot is better.
2. Write the sample code needed to trigger that Dev UI state.
3. Capture the visual proof on isolated port 4104 (restart the starter app cleanly if already running).
4. Capture full 1440x900 in-situ docsite viewport screenshots from the local docsite.
5. Open compare.html showing the proposed images/GIFs embedded alongside the matching doc text so I can review them.
```

### 2. Audit a Specific Page or Concept
```text
Analyze docs/agents/interrupts.mdx. Find where developers will have questions about what the UI looks like, capture the Dev UI in that exact state (as a GIF or screenshot), and show me a proposal with full 1440x900 in-situ viewport previews in compare.html.
```

### 3. Approve and Open PR
```text
I like proposals #1, #2, and #4 from compare.html. Please slot those screenshots/GIFs and text adjustments into the docsite branch, push the 1440x900 in-situ preview cards to huangjeff5/genkit-devui-screenshots/previews/, and open a PR with the in-situ screenshots embedded in the PR description only (keeping the docsite git diff 100% clean).
```

---

## Execution Standards

- **Resolution & Scaling**: All screenshots captured at `device_scale_factor=2`, dark theme, `1212x708` standard workspace size.
- **GIF Optimization**: 12 fps, Lanczos color palette generation with Bayer dithering for smooth streaming playback under 3 MB.
- **Intelligent Bounding**: Snap to DOM elements (`mat-drawer-content`, `mat-tree`) to guarantee zero sliced dividers, border lines, or perimeter artifacts.
- **Fresh-Eyes QA Subagent**: Every batch is audited by an adversarial visual QA subagent before submitting PRs.

---

## Repository Structure

- `README.md`: Scenario catalog, engineering principles & copy-paste prompts.
- `SKILL.md`: Autonomous agent instructions, DOM cropping invariants, and review rubric.
- `sample_app.py`: Frozen starter app with models, flows, tools, prompts, and traces.
- `capture.py`: Automated Playwright capture engine, ffmpeg GIF converter, and in-situ viewport generator.
- `previews/`: Hosted full-page in-situ viewport screenshots for PR descriptions.

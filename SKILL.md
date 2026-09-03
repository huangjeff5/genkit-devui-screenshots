---
name: genkit-devui-screenshots
description: >-
  Audit Genkit docs for Dev UI opportunities, capture visual proof (high-DPI screenshots,
  animated GIFs, and 1080p video walkthroughs) across complex runtime scenarios (agents,
  tool loops, streaming, session state, interrupts, evaluations), and compose GitHub PRs
  with 1440x900 in-situ previews.
---

# Genkit Dev UI visual verification & docsite pipeline

The Developer UI is Genkit's primary advantage over other frameworks: a zero-config, local workbench for interactive execution, trace inspection, prompt engineering, and evaluation. However, documentation often explains complex runtime dynamics in abstract prose without showing developers what the UI looks like in real-world scenarios.

This skill governs the end-to-end pipeline: auditing documentation gaps, generating deterministic runtime fixtures, capturing pixel-perfect assets (screenshots, GIFs, and Full HD videos), validating layouts with fresh-eyes visual QA, and generating 2-minute review PRs.

---

## 1. Format Selection Matrix: Screenshot vs. GIF vs. Video

When deciding how to visually illustrate a Genkit feature, choose the format that provides maximum clarity with minimal friction:

| Format | Best For | Technical Target | Duration |
| :--- | :--- | :--- | :--- |
| **Static Screenshot** | Single-screen layouts, inspected trace spans, auto-generated tool forms, evaluation matrices. | High-DPI PNG (`device_scale_factor=2`), DOM-anchored crop. | Static |
| **Animated GIF** | Short, looping micro-interactions like token streaming or rapid button triggers. | 12 fps, Lanczos color palette, Bayer dithering, `< 3 MB`. | 3–5 seconds |
| **1080p MP4 Video** | Multi-turn agent interactions, recursive tool calls, session state mutation, human-in-the-loop approvals, drawer toggles. | Full HD `1920 × 1080`, H.264 CRF 16, 20% zoom (`1600×900`), `-movflags +faststart`. | 15–25 seconds |

---

## 2. Scenario Catalog & Scenario-Specific Heuristics

### A. Autonomous Agents & Mutable Session State (Video Preferred)
- **The Concept**: Agents operating with tools, persistent session history, and live state mutations across turns.
- **Visual Goal**: Show natural human typing, trace waterfall execution, model completion, and the **Session State** drawer expanding and scrolling to verify state changes.
- **Capture Technique**:
  - Run a 1080p MP4 recording with 20% zoom (`1600 × 900` viewport).
  - Use realistic domain scenarios (e.g., canary deployment pipeline rather than toy todo items).
  - Open Session State (`[data-testid="session-state"]`), hover over the viewer, trigger `expand_all`, and smoothly scroll down the state tree to show updated properties.

### B. Recursive Tool Calling & Multi-Turn Loops
- **The Concept**: LLM emits a tool call, Genkit executes the local function, and feeds results back to the model for final synthesis.
- **Visual Goal**: Show the nested trace tree demonstrating the sequence (`generate` $\rightarrow$ `tool (1ms)` $\rightarrow$ `generate`).
- **Capture Technique**:
  - Standalone Tool Runner: Capture the auto-generated input schema form (`/tools/<toolName>`).
  - Waterfall Loop: Click the root flow trace, expand all child spans, select the tool execution span to display input parameters and output payload in the right drawer.

### C. Live Token Streaming
- **The Concept**: Real-time chunk delivery over HTTP/SSE.
- **Visual Goal**: Provide dynamic proof of streaming latency and chunk progression.
- **Capture Technique**:
  - Animated GIF (12 fps, Lanczos palette, 3–5s loop). Record the Flow Runner executing with the "Run" button clicked, showing chunks streaming into the response area.

### D. Human-in-the-Loop Interrupts & Agentic Pauses
- **The Concept**: Agents pausing execution to request external human approval or user clarification before proceeding.
- **Visual Goal**: Show the flow in the `INTERRUPTED` state with the resume input field and "Resume flow" action button.
- **Capture Technique**:
  - Trigger an interrupt with structured state. Capture the Flow Runner showing the active suspension banner and pending input payload form.

### E. Dotprompt & Dynamic Variable Resolution
- **The Concept**: Template files (`.prompt`) with frontmatter metadata, Pydantic/Zod input schemas, and Handlebars variables.
- **Visual Goal**: Show real-time variable binding and template rendering.
- **Capture Technique**:
  - Open `/prompts/<promptName>`. Fill the schema form with realistic domain data and capture with dynamic variables rendered.

### F. Evaluations & LLM-as-a-Judge Scoreboards
- **The Concept**: Automated testing of model outputs against gold-standard datasets using rubric evaluators.
- **Visual Goal**: Demonstrate dataset management, evaluator execution, and the scored results matrix.
- **Capture Technique**:
  - Navigate to `/evaluations`. Display a populated evaluation run showing metric columns (`answer_relevancy`, `latency`) with pass/fail badges and score distributions.

---

## 3. Production-Quality Video Walkthrough Standards

When producing interactive videos of the Dev UI, follow these strict recording and post-processing standards:

### A. Resolution & 20% Zoom Without Layout Breakage
- **The Problem**: Standard 1080p full-screen viewports make Dev UI text, code snippets, and drawer toggles too small when embedded inside documentation columns.
- **The Anti-Pattern**: Setting `document.body.style.zoom = '1.2'` breaks Angular Material layout by shifting fixed containers, pushing the top navigation bar off-screen, and misaligning drawer panels.
- **The Solution**:
  - Configure Playwright with a `1600 × 900` viewport (1920 / 1.20 = 1600, 1080 / 1.20 = 900) at `device_scale_factor: 2` (3200×1800 Retina raster).
  - Set `record_video_size={'width': 1600, 'height': 900}` to match the viewport exactly. **Never** set a larger `record_video_size` than `viewport` during recording, as Playwright will position the viewport in the corner with unwanted grey canvas padding.
  - Upscale the recorded video to `1920 × 1080` Full HD in ffmpeg using Lanczos interpolation (`scale=1920:1080:flags=lanczos`). Text and UI controls remain razor sharp and 20% larger.

### B. Zero White Screen / Lead-In Flicker Invariant
- **The Problem**: Playwright starts recording when `context.new_page()` opens Chromium's default white `about:blank` canvas. This causes an ugly white flash before dark stylesheets load.
- **The Solution**:
  - Launch Chromium with `args=["--force-dark-mode"]` and `color_scheme='dark'`.
  - Let the page navigate, wait for `networkidle`, sanitize breadcrumbs, and idle for 1.0s.
  - In post-processing, trim lead-in frames with `ffmpeg -ss <offset>` (typically `-ss 2.0`). Playback must start on the steady, fully rendered dark UI.

### C. H.264 Web Encoding & Faststart
Convert the raw Playwright WebM capture using this reference ffmpeg command:
```bash
ffmpeg -y -ss 2.0 -i raw_recording.webm \
  -vf "scale=1920:1080:flags=lanczos" \
  -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p \
  -movflags +faststart \
  agent-runner.mp4
```
- **CRF 16**: Visually lossless quality preserving clean font rendering and syntax highlighting.
- **`+faststart`**: Relocates the `moov` atom to the front of the MP4 container so browser video players can begin playback immediately without buffering the entire file.

### D. Realistic Context & Breadcrumb Sanitization
- **No Toy Data**: Always model production-grade engineering workflows (e.g. `releaseAgent` verifying canary health and updating cluster rollout status) rather than trivial chores ("buy milk", "todo list").
- **Clean Breadcrumbs**: Replace the default "No app detected" placeholder in `app-bar` with a realistic service name:
  ```python
  page.evaluate('''() => {
      const app = document.querySelector('app-bar');
      if (app) app.innerHTML = app.innerHTML.replace('No app detected', 'production-pipeline');
  }''')
  ```

### E. Natural Interaction Pacing & Session State Expansion
- **Typing Simulation**: Use `page.keyboard.type(prompt, delay=45)` so viewers can comfortably read the command. Pause 500ms before pressing Enter.
- **Execution Pause**: After the tool execution completes and the model replies, pause 1.2–1.5s so viewers can digest the trace waterfall and chat output.
- **Session State Expansion**:
  - Open the Session State tab via `page.locator('[data-testid="session-state"]').click()`.
  - Hover over the JSON container (`.json-viewer-content-wrapper`) to reveal the hidden `.action-buttons-overlay`.
  - Click `button:has(mat-icon:text("expand_all"))` to unfold the entire state tree.
- **Smooth Container Scrolling**:
  - If the expanded state exceeds drawer height, smoothly scroll inside the drawer using incremental wheel events:
    ```python
    page.mouse.move(1400, 450)
    for _ in range(10):
        page.mouse.wheel(0, 18)
        page.wait_for_timeout(100)
    ```
- **Final Hold**: Hold on the final scrolled state for 2.5–3.0s before stopping the recording.

### F. Accompanying High-DPI Poster Image
Always capture a high-DPI screenshot of the final settled state (`<name>.png`) right before closing the page. Use it as the `<video poster="...">` fallback in docsite markdown:
```html
<video controls muted playsinline poster="/_assets/announcing-genkit-agents/agent-runner.png">
  <source src="/_assets/announcing-genkit-agents/agent-runner.mp4" type="video/mp4" />
</video>
```

---

## 4. Intelligent DOM-Anchored Cropping Standards (Screenshots)

To ensure 100% one-shot execution without edge bleeding or awkward perimeter slices, enforce these mathematical bounding rules for static captures:

1. **Full Workbench Views** (`home`, `flow-runner`, `model-runner`, `prompt-runner`):
   - Capture full `1212x708` viewport with `device_scale_factor=2` and `color_scheme="dark"`.
2. **Workbench Inspector Views** (`inspect`):
   - Snap cleanly to `mat-drawer-content` (`x: 290..1212`, `y: 0..708`), completely excluding the left navigation sidebar and bottom collapse chevron.
3. **Isolated Tree Subviews** (`runstep`):
   - Snap to the tree container (`x: 270`, `y: 47`, `width: 304`, `height: 220`). Includes full dark gray header block (20px top breathing room) and ends before the vertical panel divider line.
4. **Zero Edge Artifacts Invariant**:
   - Outer 10px perimeter must never contain sliced border lines, 1px divider fragments, or cut-off text glyphs.

---

## 5. Fresh-Eyes Visual QA Subagent Protocol

Before opening or updating a PR, the agent invokes an adversarial Visual QA Subagent with a fresh context window to audit all visual assets:

```text
Role: Visual QA & Staff Design Reviewer
Task: Inspect all generated screenshots, GIFs, and MP4 videos using `view_file` and frame extraction.

Audit each asset against these criteria:
1. Video Startup: Check frame 0 of the MP4. Reject if there is any white canvas, blank screen, or loading flicker.
2. Video Sizing & Crispness: Confirm 1080p resolution, razor-sharp text, 20% zoom proportion, and zero grey letterboxing.
3. Realistic Data: Verify that breadcrumbs show a clean app name (no "No app detected") and workflows reflect realistic production scenarios.
4. Session State Interaction: Confirm that the Session State card was expanded with expand_all and scrolled to reveal mutated state.
5. Perimeter & Crop Slicing (Screenshots): Check the outer 10px perimeter. Reject if there are cut-off divider lines or background bleeding.
6. In-Situ Docsite Flow (1440x900): Inspect the docsite context image. Verify typography and vertical spacing integrate smoothly.

Return a pass/fail verdict with exact adjustments for any failures.
```

---

## 6. PR Formatting & Changeset Cleanliness

When submitting pull requests to `genkit-ai/docsite`:
- **Target Branch Git Diff**: Must contain ONLY modified `.mdx` guides and legitimate `_assets/` media. Zero preview cards or test scripts.
- **In-Situ Viewports (1440x900)**: Pushed to `huangjeff5/genkit-devui-screenshots/previews/` and embedded into the PR description via public `raw.githubusercontent.com` URLs.
- **2-Minute Approval Guarantee**: Reviewers must see the real docsite context, before/after diffs, and media playback directly inside GitHub without checking out the branch.

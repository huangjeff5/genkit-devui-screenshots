---
name: genkit-devui-screenshots
description: >-
  Audit Genkit docs for Dev UI opportunities, capture visual proof (GIFs and high-DPI screenshots)
  across complex runtime scenarios (tool loops, streaming, interrupts, evaluations, prompts), and compose
  GitHub PRs with 1440x900 in-situ previews.
---

# Genkit Dev UI visual verification & docsite pipeline

The Developer UI is Genkit's primary advantage over other frameworks: a zero-config, local workbench for interactive execution, trace inspection, prompt engineering, and evaluation. However, documentation often explains complex runtime dynamics in abstract prose without showing developers what the UI looks like in real-world scenarios.

This skill governs the end-to-end pipeline: auditing documentation gaps, generating deterministic runtime fixtures, capturing pixel-perfect assets with DOM-anchored cropping, validating layouts with fresh-eyes visual QA, and generating 2-minute review PRs.

---

## 1. Scenario Catalog & Scenario-Specific Heuristics

When auditing documentation or generating visual assets, match each concept to its tuned capture heuristic:

### A. Recursive Tool Calling & Multi-Turn Loops
- **The Concept**: LLM emits a tool call, Genkit executes the local function, and feeds results back to the model for final synthesis.
- **Visual Goal**: Show the nested trace tree demonstrating the sequence (`generate` $\rightarrow$ `tool (1ms)` $\rightarrow$ `generate`).
- **Capture Technique**:
  - Standalone Tool Runner: Capture the auto-generated input schema form (`/tools/<toolName>`).
  - Waterfall Loop: Click the root flow trace, expand all child spans, select the tool execution span to display input parameters and output payload in the right drawer.

### B. Live Token Streaming
- **The Concept**: Real-time chunk delivery over HTTP/SSE.
- **Visual Goal**: Provide dynamic proof of streaming latency and chunk progression.
- **Capture Technique**:
  - Animated GIF (12 fps, Lanczos palette, 3–5s loop). Record the Flow Runner executing with the "Run" button clicked, showing chunks streaming into the response area.

### C. Human-in-the-Loop Interrupts & Agentic Pauses
- **The Concept**: Agents pausing execution to request external human approval or user clarification before proceeding.
- **Visual Goal**: Show the flow in the `INTERRUPTED` state with the resume input field and "Resume flow" action button.
- **Capture Technique**:
  - Trigger an interrupt with structured state. Capture the Flow Runner showing the active suspension banner and pending input payload form.

### D. Dotprompt & Dynamic Variable Resolution
- **The Concept**: Template files (`.prompt`) with frontmatter metadata, Pydantic/Zod input schemas, and Handlebars variables.
- **Visual Goal**: Show real-time variable binding and template rendering.
- **Capture Technique**:
  - Open `/prompts/<promptName>`. Fill the schema form with realistic domain data (e.g., customer reservations, menu preferences) and capture with dynamic variables rendered.

### E. Evaluations & LLM-as-a-Judge Scoreboards
- **The Concept**: Automated testing of model outputs against gold-standard datasets using rubric evaluators.
- **Visual Goal**: Demonstrate dataset management, evaluator execution, and the scored results matrix.
- **Capture Technique**:
  - Navigate to `/evaluations`. Display a populated evaluation run showing metric columns (`answer_relevancy`, `faithfulness`, `latency`) with pass/fail badges and score distributions.

### F. Custom Step Telemetry (`ai.run`)
- **The Concept**: Wrapping custom business logic (database queries, external API calls, vector search) to make it observable in traces.
- **Visual Goal**: Show custom named spans nested cleanly inside the parent flow trace.
- **Capture Technique**:
  - Use isolated tree crop (`x: 270, y: 47, width: 304, height: 220`) showing the custom step with its exact execution time (e.g. `retrieve-daily-menu  1ms [✓]`).

---

## 2. Intelligent DOM-Anchored Cropping Standards

To ensure 100% one-shot execution without edge bleeding or awkward perimeter slices, enforce these mathematical bounding rules:

1. **Full Workbench Views** (`home`, `flow-runner`, `model-runner`, `prompt-runner`):
   - Capture full `1212x708` viewport with `device_scale_factor=2` and `color_scheme="dark"`.
2. **Workbench Inspector Views** (`inspect`):
   - Snap cleanly to `mat-drawer-content` (`x: 290..1212`, `y: 0..708`), completely excluding the left navigation sidebar and bottom collapse chevron.
3. **Isolated Tree Subviews** (`runstep`):
   - Snap to the tree container (`x: 270`, `y: 47`, `width: 304`, `height: 220`). Includes full dark gray header block (20px top breathing room) and ends before the vertical panel divider line.
4. **Zero Edge Artifacts Invariant**:
   - Outer 10px perimeter must never contain sliced border lines, 1px divider fragments, or cut-off text glyphs.

---

## 3. Fresh-Eyes Visual QA Subagent Protocol

Before opening or updating a PR, the agent invokes an adversarial Visual QA Subagent with a fresh context window to audit all PNGs in `previews/`:

```text
Role: Visual QA & Staff Design Reviewer
Task: Inspect all generated screenshot PNGs and in-situ 1440x900 viewport captures in `previews/` using `view_file`.

Audit each image against these 4 strict criteria:
1. Perimeter & Crop Slicing: Check the outer 10px perimeter of every cropped card. Reject if there are cut-off divider lines, adjacent panel slivers, stray 1px borders, or partial background bleeding.
2. Icon & Label Integrity: Confirm green checkmarks, latency badges (e.g., 1ms, 2.23s), and function names are 100% intact with comfortable padding.
3. Zero Unpopulated Artifacts: Verify that no "No app detected" strings, blank JSON inputs, or uninitialized spinners appear.
4. In-Situ Docsite Flow (1440x900): Inspect the docsite context image. Verify that the image width, typography, and vertical spacing integrate smoothly with the documentation text without overpowering the column.

Return a pass/fail verdict with exact pixel/coordinate adjustments for any failures.
```

---

## 4. PR Formatting & Changeset Cleanliness

When submitting pull requests to `genkit-ai/docsite`:
- **Target Branch Git Diff**: Must contain ONLY modified `.mdx` guides and legitimate `src/assets/` images. Zero preview cards or test scripts.
- **In-Situ Viewports (1440x900)**: Pushed to `huangjeff5/genkit-devui-screenshots/previews/` and embedded into the PR description via public `raw.githubusercontent.com` URLs.
- **2-Minute Approval Guarantee**: Reviewers must see the real docsite context and before/after diffs directly inside GitHub without checking out the branch.

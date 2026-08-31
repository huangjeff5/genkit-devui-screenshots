# Genkit Dev UI docsite screenshots & opportunity scout

Tooling and workflow for discovering opportunities to highlight the Genkit Developer UI, capturing high-DPI screenshots and GIFs, and creating high-clarity PRs with full in-situ docsite previews.

---

## Why this exists

1. **Dev UI is tribal knowledge**: The core team uses the local Developer UI continuously for rapid testing and trace debugging, but our documentation often fails to show external developers (and autonomous coding agents) that this exists out of the box.
2. **Abstract documentation**: Explaining recursive tool calling, human-in-the-loop pauses, or structured streaming with text alone leaves open loops. Showing the runtime trace closes the loop.
3. **Competitive advantage**: Other frameworks require external cloud platforms or paid dashboards to inspect traces. Genkit provides a zero-config local UI.
4. **Agent explainability**: Coding agents reading the docs can use visual artifacts to help developers verify agent behavior on specific tabs and spans.
5. **Zero-friction execution**: Anyone on the team can trigger audits, captures, and doc updates directly through natural language in Jetski without manually wiring up scripts or local test harnesses.

---

## Jetski prompts (copy & paste)

Paste these into chat to run the workflow:

### 1. Audit docs for new Dev UI opportunities
```text
Audit our documentation and look for high-impact opportunities where showcasing the Genkit Dev UI will create "aha!" moments or close open loops for developers.

For any page that could benefit from visual proof:
1. Decide whether an animated GIF or a static screenshot is better.
2. Write the sample code needed to trigger that Dev UI state.
3. Capture the visual proof on isolated port 4104 (restart the starter app cleanly if already running).
4. Capture full 1440x900 in-situ docsite viewport screenshots from the local docsite.
5. Open compare.html showing the proposed images/GIFs embedded alongside the matching doc text so I can review them.
```

### 2. Audit a specific page or PR
```text
Analyze docs/agents/interrupts.mdx. Find where developers will have questions about what the UI looks like, capture the Dev UI in that exact state (as a GIF or screenshot), and show me a proposal with full 1440x900 in-situ viewport previews in compare.html.
```

### 3. Approve and open PR
```text
I like proposals #1, #2, and #4 from compare.html. Please slot those screenshots/GIFs and text adjustments into the docsite branch, push the 1440x900 in-situ preview cards to huangjeff5/genkit-devui-screenshots/previews/, and open a PR with the in-situ screenshots embedded in the PR description only (keeping the docsite git diff 100% clean).
```

### 4. Retake or adjust a shot
```text
The shots look good except for "inspect". Please retake that shot with the getDishDetails span selected in the waterfall tree so its input/output payload drawer is visible, and refresh compare.html.
```

---

## Visual PR Standards

- **Full 1440x900 In-Situ Viewports**: Always capture the complete 3-column layout (left nav + content + right TOC) on the running docsite so reviewers can verify sizing and reading flow at a glance without zooming.
- **PR Description ONLY**: In-situ docsite preview cards are hosted in this public repository (`previews/`) and embedded in the PR body. They must **never** be committed to the target `genkit-ai/docsite` repository branch.
- **2-Minute Approvals**: Reviewers must be able to inspect all visual diffs and in-situ layouts directly on GitHub without checking out the branch.

---

## Format decision

- **GIF** (3–8s loop, 12 fps, Lanczos): real-time streaming, pause/resume interrupts, parameter slider testing, or expandable trace trees. Examples: interactive flow tour, live prompt variable resolution, multi-agent trace tree.
- **Screenshot** (PNG, 2x Retina): structural JSON, schema forms, multi-span latency waterfalls, or evaluation scoreboards. Examples: tool runner input form, tool trace waterfall, evaluation result matrix.

---

## Repo structure

- `README.md`: Playbook, visual PR standards & copy-paste Jetski prompts.
- `SKILL.md`: Jetski skill definition, guardrails, and review rubric.
- `sample_app.py`: Frozen starter app with models, flows, tools, and prompts.
- `capture.py`: Playwright capture engine, ffmpeg GIF generator, and in-situ viewport capturer.
- `previews/`: Hosted full-page in-situ viewport screenshots for PR descriptions.

---

## Manual CLI usage

```bash
# 1. Start the sample app on port 4104
export GENKIT_ENV=dev
export GOOGLE_CLOUD_PROJECT=aim-testing
cd ~/Desktop/genkit-devui-screenshots
genkit start -p 4104 -- /Users/huangjeff/Desktop/genkit-python/.venv/bin/python sample_app.py

# 2. Run capture pipeline + full in-situ viewport capture
python3 capture.py --base-url http://127.0.0.1:4104 --docsite-url http://localhost:4321

# 3. Open review dashboard
open ~/Desktop/genkit-docsite-shots/proposed/compare.html
```

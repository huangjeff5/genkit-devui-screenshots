# 📖 Genkit Developer UI: Docsite "Aha!" Moment Playbook

> **The PM & DevRel Playbook for transforming Genkit's "secret sauce" into high-impact visual documentation—powered autonomously by Jetski.**

---

## 🎯 The Problem This Playbook Solves

1. **The "Secret Sauce" is Hidden**: The Genkit core team uses the local Developer UI daily for rapid testing, live prompt experimentation, and trace debugging. However, for external developers and autonomous coding agents, this superpower has been tribal knowledge rather than front-and-center in our docs.
2. **Abstract Docs & Open Loops**: When documentation explains complex lifecycles—such as recursive tool loops, human-in-the-loop pauses, or streaming accumulations—pure code snippets leave open cognitive loops. Developers wonder: *"How do I actually observe, debug, and verify this at runtime?"*
3. **Competitive Edge Over Other Frameworks**: Competitors (LangChain, Vercel AI SDK, LlamaIndex) require either paid cloud accounts or external dashboards just to inspect traces. Genkit offers a zero-config, airgapped local Dev UI out of the box—we need to aggressively highlight this advantage.
4. **Agent-Oriented Docs**: Coding agents reading our docsite need visual proof artifacts so they can explain their reasoning and point human engineers to exact Dev UI tabs and traces to verify agent behavior.
5. **Zero Terminal Friction for PMs**: Product Managers shouldn't need to configure Python virtualenvs, manage Playwright headless browsers, or debug CSS layouts. The entire process must be triggerable via natural language in Jetski.

---

## 🚀 The PM Playbook (Copy-Paste Prompts for Jetski)

You do not need to use the terminal. Simply paste these prompts into your **Jetski** chat window.

---

### Play 1: Discover New "Aha!" Opportunities Across the Docs
*Use when docs change, new features ship, or you want to do a fresh audit.*

```text
Audit our documentation at genkit-docsite and look for high-impact opportunities where showcasing the Genkit Dev UI will create "aha!" moments or close open loops for developers.

For any page that could benefit from visual proof:
1. Decide whether an animated GIF or a static screenshot is better.
2. Write the sample code needed to trigger that Dev UI state.
3. Capture the visual proof on isolated port 4104.
4. Open compare.html showing the proposed images/GIFs embedded alongside the matching doc text so I can review them.
```

---

### Play 2: Audit a Specific Page or Feature
*Use when a PR or new guide lands (e.g., Agents, Tool Calling, or Evaluators).*

```text
We just updated docs/agents/interrupts.mdx. Analyze the page, find where developers will have questions about what the UI looks like, capture the Dev UI in that exact state (as a GIF or screenshot), and show me a proposal with the code and visual side-by-side in compare.html.
```

---

### Play 3: Approve Proposals & Sync into the Docsite
*Use after reviewing `compare.html` in your browser.*

```text
I like proposals #1, #2, and #4 from compare.html. Please slot those screenshots/GIFs and text adjustments into genkit-docsite and start the local docsite server so I can preview the final result in my browser.
```

---

### Play 4: Request a Visual Retake or Adjustment
*Use if a screenshot needs a different theme, open drawer, or specific input data.*

```text
The shots look good except for "inspect". Please retake that shot with the getDishDetails span selected in the waterfall tree so its input/output payload drawer is visible, and refresh compare.html.
```

---

## 🧠 The Decision Rubric: GIF vs. Static Screenshot

Jetski follows this strict product rubric when choosing between animated and static media:

| Format | When to Use | Examples |
| :--- | :--- | :--- |
| **🎬 Animated GIF**<br>*(3–8s loop, 12 fps, Lanczos)* | • Temporal transitions & streaming tokens<br>• Human-in-the-Loop interrupts (Pause $\rightarrow$ Input $\rightarrow$ Resume)<br>• Parameter slider tuning (dragging Temperature)<br>• Dynamic trace tree expanding/collapsing | • Interactive flow execution tour<br>• Live prompt variable resolution<br>• Multi-agent delegation waterfall |
| **📸 Static Screenshot**<br>*(2x Retina, Dark Mode)* | • Deep structural JSON & schema forms<br>• High-density trace waterfalls with latency metrics<br>• Multi-span correlated logs & error diagnostics<br>• Side-by-side code $\leftrightarrow$ UI alignments | • Standalone tool runner form<br>• Tool call trace waterfall breakdown<br>• Evaluation scoreboards & LLM judge reasoning |

---

## 🛠️ Repository Architecture

- **`SKILL.md`**: The Jetski skill definition that equips the AI agent with the Opportunity Scout mindset and self-review rubric.
- **`briefs/registry.json`**: The declarative registry of all captured assets, target routes, UI click actions, and docsite destinations.
- **`sample/app.py`**: The frozen, deterministic test harness containing models, flows, tools, and prompts.
- **`scripts/capture_all.py`**: Automated Playwright capture engine and `ffmpeg` palette-optimized GIF builder.
- **`scripts/sync_to_docsite.py`**: One-step asset syncer into `genkit-docsite`.

---

## 🛡️ Guardrails Built into the Engine

1. **Port Isolation**: Screenshot captures always run on isolated port `4104`, never disturbing your primary Dev UI on `4000`.
2. **Clean Frame Guarantee**: Auto-masks temporary `No app detected` text to `sample` and eliminates transient toast notifications.
3. **Retina Quality**: All assets are captured at `device_scale_factor=2` with dark-mode color scheme and standardized padding.

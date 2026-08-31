# What the original shots were deciding

Measured from the files on genkit.dev today. Use this as the taste bar, not as "copy the old chrome."

## Resolution

| file | pixels | what it is |
| --- | --- | --- |
| `genkit_dev_ui_home.png` | 2480×1772 | full window, ~2× retina |
| `welcome_to_genkit_developer_ui.png` | 2574×1457 | full macOS Chrome window, retina |
| `genkit_developer_ui_overview.gif` | 2546×1426, 900 frames, 13MB | recorded tour, retina, browser chrome |
| `agent-dev-ui-1.png` | 2626×1780 | full UI, retina |
| `devui-flows.png` | 1212×708 | cropped to the Run workspace |
| `devui-inspect.png` | 1040×770 | cropped to Inspect tree + detail |
| `devui-runstep.png` | **397×278** | cropped to the tree only |
| `developer_ui_model_runner.png` | 1423×630 | cropped three-pane runner |
| `evals_compare_*.png` | ~1600×680 | cropped to the compare grid |

A 1440×900 1× Playwright dump looks worse because the docsite displays these large. Text goes soft. Default scale is **2**.

## Format

- **Still** when the sentence points at one state: "from the Run tab you can run a flow", "the retrieval step shows up in the tree."
- **GIF** when the sentence is a tour: devtools says "here's a quick gif tour with cats." Motion *is* the product — pick a model, type, Run, watch tokens land.
- Do not replace a GIF with a still because stills are easier.

## Frame

Three sizes, picked on purpose:

1. **Product window** (home, welcome, gif) — include `localhost:4000` browser chrome. The reader should feel "this is a local app I open," not an IDE panel.
2. **Workspace crop** (flow runner, inspect, model runner) — left nav + the pane the sentence is about. No OS chrome. No unused drawers.
3. **Detail crop** (runstep) — *only* the tree. 397×278. The lesson is "this `run()` is its own row." Extra attributes and "(No logs found)" are not the lesson.

If you cannot say which of the three you are taking, you are taking a dump.

## What is in the app

The home shot is a **starter project**, not a plugin catalog.

- A handful of models a person would actually pick (`gemini-flash-latest`, maybe Imagen). Not 42 Vertex ids led by `codegemma`.
- One or two flows with names that match the page (`menuSuggestionFlow`), plus one prompt if the page talks about prompts.
- Trace rows that look like successful generates: green, tokens in/out, a few hundred ms to a few seconds. No failed Vertex 404 sitting in history.
- Expand the sidebar section the page is selling (Models on the welcome shot). Collapse empty zeros so the app does not look dead.

Stage this with a tiny sample. Do not screenshot `dev-ui-gallery` or a raw `VertexAI()` plugin dump.

## What is on screen

- Type something a stranger gets in one glance. The gif uses "Tell me a short fact about cats." The inspect page uses the medieval prix-fixe sample from the prose. Do not invent a third story.
- Empty input + Run is correct when the sentence is "you type here and run." A finished output is correct when the sentence is "you see the result / the trace."
- Never leave a failed run in the frame. Hide the history drawer unless the page is about history.
- "No app detected" in the header is a bug in the picture even if the sidebar lists flows. Do not ship it.
- Open Config when the page is about iterating on temperature / export `.prompt`. Close it when the page is about traces.

## The question to answer before any script runs

Read the sentence above the image, look at the old file, look at the current UI. Write one brief. If you cannot fill `inFrame` and `notInFrame` in a minute, you have not thought yet. The brief is what the capture script reads. Do not shoot from vibes and crop later.

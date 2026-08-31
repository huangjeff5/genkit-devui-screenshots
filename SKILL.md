---
name: genkit-devui-screenshots
description: >-
  Capture Genkit Developer UI screenshots for the genkit-ai/docsite and
  present them for a fast Jeff vet. Use when the user mentions docsite
  screenshots, Dev UI screenshots, Developer UI pictures, "vet the shots",
  or updating genkit.dev images of the local UI.
---

# Dev UI docsite screenshots

You do not invent the composition. A frozen starter and `scripts/batch1.py` already chose the sample, the crop, and the click. Your job is: run the script, **look at old vs new with fresh eyes**, reject anything a stranger would not get, then show Jeff only survivors.

Docs live in [genkit-ai/docsite](https://github.com/genkit-ai/docsite). Never land, commit, or PR until Jeff says `ok` on that shot.

## Do not

- Write a Playwright script, a new `app.py`, or a new brief.
- Call `VertexAI()` or `GoogleAI()` as a plugin. Those list a catalog. Home dies.
- Screenshot at scale 1, or screenshot the whole window and crop later.
- Kill anything on port **4000**. That is a long-lived UI. Screenshot UI is **4104**.
- Shoot or replace the cats gif unless Jeff says replace it.
- Tour the UI in chat. Do not sit and narrate.
- Show Jeff a shot the script marked `FAIL`.

## Run this

```bash
# 1. Copy the frozen starter (overwrite, do not edit)
mkdir -p ~/Desktop/genkit-docsite-shots/sample
cp ~/.cursor/skills/genkit-devui-screenshots/sample/app.py \
   ~/Desktop/genkit-docsite-shots/sample/app.py

# 2. If nothing is on 4104, start the frozen starter. Do not touch 4000.
#    Reuse 4104 if it is already this sample (Flows 3, Models 2).
export GENKIT_TELEMETRY_SERVER=http://127.0.0.1:4134
export GENKIT_ENV=dev
export GOOGLE_CLOUD_PROJECT=aim-testing
cd ~/Desktop/genkit-docsite-shots/sample
# only if 4104 is free:
# genkit start -p 4104 -- <repo>/py/.venv/bin/python app.py

# 3. Stage traces + capture + vet. One command.
python3 ~/.cursor/skills/genkit-devui-screenshots/scripts/batch1.py \
  --base-url http://127.0.0.1:4104 \
  --out-dir ~/Desktop/genkit-docsite-shots/proposed
```

If the script prints `FAIL`, run it **once** more. If it fails again, stop and paste the FAIL lines. Do not fix by shooting a full page.

## Self-review (required, before Jeff sees anything)

The script can tell you the crop is the right size. It cannot tell you the picture makes sense. You have to look.

For **each** of home, flow-runner, inspect, runstep:

1. Read `proposed/old/<id>.png` and `proposed/<id>.png`. Actually open the pixels. Do not vet from filenames or page text.
2. Answer these four questions with yes/no. A stranger on the docs page, two seconds, no caption.

| # | question | fail if |
| --- | --- | --- |
| Beat | Can they see the sentence's one thing? (home = a starter app; runner = type JSON and Run; inspect = this generate's ingredients; runstep = `retrieve-daily-menu` is its own row) | you have to explain the shot |
| Junk | Is the frame clean? | catalog junk, `No app detected`, a pink failed row, open history, empty Logs, Attributes soup |
| Crop | Is this the right size class? | home is a dump; runner/inspect include OS chrome; runstep includes the detail pane or left nav |
| Vs old | Is the new one at least as easy to get? | old showed a dish / a tight tree and you showed plumbing |

Any **no** → that id is a reject. Retake only that id. Jeff never sees it.

Do not talk yourself into a yes. If you hesitate, it is a no.

## Then say this (only survivors)

Open `~/Desktop/genkit-docsite-shots/proposed/compare.html`.

```
home: starter sidebar, two Gemini ids, a medieval menu in the traces
flow-runner: {"theme":"medieval"} + Run, history shut
inspect: ingredients Preview on the middle generate
runstep: retrieve-daily-menu as its own tree row
```

Wait for:

```
ok home, flow-runner, inspect, runstep
retake inspect (note)
skip gif
```

Copy only `ok` shots to the `dest` in `briefs/batch1.json`. Keep the filename. Wait for "PR it."

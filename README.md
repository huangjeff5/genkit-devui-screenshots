# genkit-devui-screenshots

Frozen recipe for [genkit.dev](https://genkit.dev) Developer UI pictures.

The agent does not compose. It runs a tiny starter, a shutter script, then looks at old vs new with fresh eyes and rejects anything a stranger would not get in two seconds.

## What’s in here

| path | what it is |
| --- | --- |
| `SKILL.md` | Recipe + do-nots + the four-question self-review |
| `sample/app.py` | Two Gemini models, three menu flows, one prompt. Not a catalog. |
| `scripts/batch1.py` | Stage traces, capture, size-gate |
| `briefs/batch1.json` | Dest paths and the sentence above each image |
| `compose.md` | Crop classes measured from the live files |
| `shots.md` | What to shoot and what not to |

No pictures in this repo. Captures land on the machine at `~/Desktop/genkit-docsite-shots/proposed`.

## Install

```bash
git clone https://github.com/jeffdh5/genkit-devui-screenshots.git \
  ~/src/genkit-devui-screenshots
```

Then follow `SKILL.md`. Set `REPO` to that clone.

## What “done” looks like

The agent opens `~/Desktop/genkit-docsite-shots/proposed/compare.html` and gives four one-liners. You vet with `ok` / `retake` / `skip gif`. They do not land or PR until you say so.

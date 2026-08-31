# Shot list

Status: `stale` = live image is old chrome or old models. `missing` = the page walks the UI and has no picture. `current` = keep unless Jeff says redo.

Dest paths are relative to the docsite repo root.

## Batch 1 — refresh what is already on the page

| id | page | dest | status | must show | sample |
| --- | --- | --- | --- | --- | --- |
| home | `docs/devtools` | `src/assets/dev_ui/genkit_dev_ui_home.png` | stale | Welcome dashboard, current sidebar, current model names | dev-ui-gallery |
| gif | `docs/devtools` | `public/genkit_developer_ui_overview.gif` | stale | Short tour of runners. Still cats in the current file. Ask before replacing | dev-ui-gallery |
| flow-runner | `docs/flows` | `src/assets/devui-flows.png` | stale | Run a defined flow from the runner with labeled JSON input | dev-ui-gallery |
| inspect | `docs/flows` | `src/assets/devui-inspect.png` | stale | Trace of a multi-generate flow, one model span selected, input/output visible | dev-ui-gallery |
| runstep | `docs/flows` | `src/assets/devui-runstep.png` | stale | Trace where a custom `run()` / `ai.run()` step is its own span | dev-ui-gallery |
| agent-chat | `docs/agents/overview` | `public/assets/agent-dev-ui-1.png` | current | Agent chat with a tool turn and session state. Recapture only if chrome drifted | agents sample |
| eval-compare | `docs/evaluation` | `src/assets/evals_compare_{light,dark}.png` | current | Side-by-side eval compare with metric highlight. Recapture only if chrome drifted | evals |

## Batch 2 — pages that walk the UI with no picture

| id | page | dest | status | must show | sample |
| --- | --- | --- | --- | --- | --- |
| model-runner | `docs/dotprompt`, `docs/models` | `src/assets/developer_ui_model_runner.png` | stale unused | Model runner with a prompt typed, config sidebar open | dev-ui-gallery |
| prompt-runner | `docs/dotprompt` | `src/assets/prompts-in-developer-ui.png` | stale unused | Loaded `.prompt`, input, system text, Export control | dev-ui-gallery |
| datasets | `docs/evaluation` | `src/assets/devui-datasets.png` | missing | Datasets list after clicking Datasets | evals |
| dataset-create | `docs/evaluation` | `src/assets/devui-dataset-create.png` | missing | Create dataset dialog (id, Flow type) | evals |
| dataset-examples | `docs/evaluation` | `src/assets/devui-dataset-examples.png` | missing | Dataset with a few examples saved | evals |
| eval-run | `docs/evaluation` | `src/assets/devui-eval-run.png` | missing | Run new evaluation dialog with target + dataset | evals |
| eval-results | `docs/evaluation` | `src/assets/devui-eval-results.png` | missing | Evaluation details: input, output, metrics | evals |
| traces | `docs/local-observability` | `src/assets/devui-traces.png` | missing | Trace list after a run | dev-ui-gallery |
| trace-logs | `docs/local-observability` | `src/assets/devui-trace-logs.png` | missing | One trace with log records on the emitting span | Go sample |

## Do not shoot

Mentions of the Dev UI in plugin, middleware, and framework pages are "it shows up in the list" asides. No picture unless Jeff adds a shot id.

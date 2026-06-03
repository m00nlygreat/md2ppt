---
name: interact
description: Open a reusable local GUI for progress updates and ongoing human-in-the-loop interaction. Use progress mode to keep the user-facing screen current during multi-step work, and use human-in-the-loop mode when Codex needs the user to choose between visual options, answer structured questions, approve a direction, or give iterative feedback. The skill runs a project-scoped local server, updates the browser screen dynamically, supports multiple user submissions, and reads submitted JSON answers before continuing.
---

# Interact

Use this skill to collaborate with the user through a local browser UI. The same open screen can be updated by the agent repeatedly, and the user can submit multiple answers during one task.

There are two distinct usage modes:

- Progress update mode: keep the screen current while the agent works. Use this aggressively between tool calls during long or multi-step tasks, even when no user response is needed.
- Human-in-the-loop mode: pause for the user when their input changes the next step. Use `wait --after-seq <last-seq>` and continue only after reading the submitted answer.

Do not treat this skill as only a final report surface. If the browser is open for an ongoing task, update it throughout the task.

## Workflow

Run commands from the project root. The server and answer files are project-scoped under `.interact/`.

1. Choose a stable interaction id for the task when the screen will be reused.
2. Ensure the server is running or let `ask` start it.
3. Send the first schema with `ask`.
4. Open the returned URL for the user, preferably with the in-app browser when available. Keep using this URL for later updates.
5. When telling the user where to answer, provide the local server address as a Markdown link, such as `[Open interact GUI](http://127.0.0.1:5199/i/example)`. Do not show a bare localhost URL as the user-facing instruction.
6. During work, call `update --id <interaction-id>` whenever the visible state should change. The already-open browser page polls the server and re-renders automatically.
7. When user input is needed, call `wait --id <interaction-id> --after-seq <last-seq>`.
8. Read the returned JSON and continue the original task.

## Progress Update Mode

Use this mode when the user should be able to watch what the agent is doing.

Requirements:

- For long or multi-step work, update the screen after meaningful tool results, before risky edits, while tests/builds are running, and after important outcomes.
- Do not wait until the final answer to update the GUI.
- Do not block on `wait` in progress mode unless the next step genuinely depends on user input.
- Prefer `info` fields for status-only screens, because they do not require submission.
- Keep status schemas short: current phase, what changed, next action, and any notable risk or blocker.
- Reuse the same interaction id so the user's browser tab keeps changing in place.

Example progress-only schema:

```json
{
  "id": "task-progress",
  "title": "Running tests",
  "description": "The agent has finished the code edit and is running the focused test suite.",
  "submitLabel": "Acknowledge",
  "fields": [
    {
      "id": "status",
      "type": "info",
      "label": "Status",
      "description": "No action is required. This screen will update again when the test result is available."
    }
  ]
}
```

## Human-In-The-Loop Mode

Use this mode when the user's answer changes the next tool call or implementation direction.

Requirements:

- Ask only for decisions that matter to the next step.
- Use explicit answer fields such as `single-select`, `multi-select`, `textarea`, `boolean`, or `number`.
- After each answer, store the returned `seq` and use `wait --after-seq <last-seq>` for the next user turn.
- Update the screen after consuming the user's answer so they can see what the agent is doing next.
- Avoid asking in the GUI when a simple chat question would be clearer.

Example loop:

```powershell
node .agents/skills/interact/scripts/interact-server.js ask --schema step-1.json
node .agents/skills/interact/scripts/interact-server.js wait --id task-progress
node .agents/skills/interact/scripts/interact-server.js update --id task-progress --schema working-on-choice.json
node .agents/skills/interact/scripts/interact-server.js update --id task-progress --schema step-2.json
node .agents/skills/interact/scripts/interact-server.js wait --id task-progress --after-seq 1
```

## Commands

Use the bundled script:

```powershell
node .agents/skills/interact/scripts/interact-server.js ensure
node .agents/skills/interact/scripts/interact-server.js ask --schema path/to/schema.json
node .agents/skills/interact/scripts/interact-server.js update --id <interaction-id> --schema path/to/next-schema.json
node .agents/skills/interact/scripts/interact-server.js wait --id <interaction-id>
node .agents/skills/interact/scripts/interact-server.js wait --id <interaction-id> --after-seq <last-seq>
node .agents/skills/interact/scripts/interact-server.js status
node .agents/skills/interact/scripts/interact-server.js stop
```

For quick one-off prompts, pass inline JSON:

```powershell
node .agents/skills/interact/scripts/interact-server.js ask --schema-json '{"title":"Choose a direction","fields":[{"id":"direction","type":"single-select","label":"Direction","required":true,"options":["A","B"]}]}'
```

`ask` returns:

```json
{
  "id": "interaction-id",
  "url": "http://127.0.0.1:5199/i/interaction-id",
  "markdownLink": "[Open interact GUI](http://127.0.0.1:5199/i/interaction-id)",
  "answerFile": ".interact/answers/interaction-id.json",
  "transcriptFile": ".interact/answers/interaction-id.jsonl"
}
```

Use `markdownLink` when writing an interim user update.

Each submitted answer includes a monotonically increasing `seq`:

```json
{
  "id": "interaction-id",
  "seq": 2,
  "values": { "decision": "revise" },
  "submittedAt": "2026-05-25T12:34:56.000Z"
}
```

Use `seq` as the cursor for follow-up waits. The `.json` file contains the latest answer, and `.jsonl` contains the full transcript.

## Schema

Top-level fields:

```json
{
  "id": "optional-stable-id",
  "title": "Question shown at the top",
  "description": "Optional context",
  "submitLabel": "Submit",
  "fields": []
}
```

Supported field types:

- `single-select`: radio-style option cards. Use for exactly one choice.
- `multi-select`: checkbox option cards. Use `min` and `max` when needed.
- `text`: short text input.
- `textarea`: long-form input.
- `number`: numeric input. Use `min` and `max` for bounds when needed.
- `select`: dropdown.
- `boolean`: checkbox toggle.
- `info`: non-answer explanatory text.

Each answer field should have an `id`, `type`, `label`, and optional `description`, `placeholder`, `required`, and `default`.

Options can be strings:

```json
{ "options": ["Continue", "Revise", "Stop"] }
```

Or objects:

```json
{
  "options": [
    { "value": "continue", "label": "Continue", "description": "Proceed with the current plan" },
    { "value": "revise", "label": "Revise", "description": "Change direction before implementation" }
  ]
}
```

## Reuse Rules

- Reuse the same server during a conversation.
- Use `ask` to start a new interaction. By default it clears prior answers for that interaction id; pass `--keep-answers` only when intentionally resuming a transcript.
- Use `update --id <interaction-id>` to change the open screen without clearing previous answers.
- Give each interaction a stable `id` only when the caller needs to refer to it later; otherwise let the script generate one.
- In progress update mode, update frequently and continue working without waiting.
- In human-in-the-loop mode, prefer `wait --after-seq <last-seq>` as the source of truth during iterative loops.
- Use `.interact/answers/<id>.json` for the latest answer and `.interact/answers/<id>.jsonl` for the full transcript.
- Keep schemas small and task-specific. Do not use the GUI when a normal chat question is clearer.
- Stop the server with `stop` when it is no longer useful.

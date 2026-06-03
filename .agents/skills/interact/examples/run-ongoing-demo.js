#!/usr/bin/env node

const BASE_URL = process.env.INTERACT_URL || "http://127.0.0.1:5199";
const INTERACTION_ID = process.env.INTERACT_ID || "ongoing-demo";
const DELAY_MS = Number(process.env.INTERACT_DELAY_MS || 3500);

const steps = [
  {
    id: INTERACTION_ID,
    title: "1 / 3 - Direction check",
    description: "Agent update 1. This is the first screen in the ongoing flow.",
    submitLabel: "Send step 1",
    fields: [
      {
        id: "direction",
        type: "single-select",
        label: "Direction",
        required: true,
        options: [
          { value: "continue", label: "Continue", description: "Move to the next screen." },
          { value: "revise", label: "Revise", description: "Ask the agent to adjust." }
        ]
      },
      {
        id: "note",
        type: "textarea",
        label: "Note",
        placeholder: "You can type while the agent keeps updating."
      }
    ]
  },
  {
    id: INTERACTION_ID,
    title: "2 / 3 - Priority tuning",
    description: "Agent update 2. The same URL has changed without reopening the browser.",
    submitLabel: "Send step 2",
    fields: [
      {
        id: "priority",
        type: "multi-select",
        label: "Priorities",
        required: true,
        min: 1,
        max: 2,
        options: [
          { value: "speed", label: "Speed", description: "Keep it quick." },
          { value: "polish", label: "Polish", description: "Improve the UI details." },
          { value: "docs", label: "Docs", description: "Clarify how agents should use it." }
        ]
      },
      {
        id: "confidence",
        type: "number",
        label: "Confidence",
        min: 1,
        max: 5,
        default: 3
      }
    ]
  },
  {
    id: INTERACTION_ID,
    title: "3 / 3 - Final confirmation",
    description: "Agent update 3. This screen can still submit another answer, then the agent can update again.",
    submitLabel: "Finish step 3",
    fields: [
      {
        id: "approved",
        type: "boolean",
        label: "Approved",
        placeholder: "Ready to proceed",
        default: true
      },
      {
        id: "final_comment",
        type: "text",
        label: "Final comment",
        placeholder: "Optional closing note"
      }
    ]
  },
  {
    id: INTERACTION_ID,
    title: "Loop continues - Agent changed it again",
    description: "A fourth update proves this is not limited to a one-shot report or exactly three screens.",
    submitLabel: "Send another response",
    fields: [
      {
        id: "reaction",
        type: "select",
        label: "Reaction",
        options: ["Works", "Needs changes", "Try another loop"]
      },
      {
        id: "details",
        type: "textarea",
        label: "Details",
        placeholder: "Tell the agent what to change next."
      }
    ]
  }
];

for (const [index, interaction] of steps.entries()) {
  const response = await fetch(`${BASE_URL}/api/interactions/${encodeURIComponent(INTERACTION_ID)}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ interaction })
  });

  if (!response.ok) {
    throw new Error(await response.text());
  }

  console.log(`updated ${index + 1}/${steps.length}: ${interaction.title}`);
  if (index < steps.length - 1) {
    await new Promise((resolve) => setTimeout(resolve, DELAY_MS));
  }
}

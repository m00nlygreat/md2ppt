# Ongoing Interaction Example

This example shows how one browser URL can support multiple agent-user turns.

Run from the project root:

```powershell
node .agents/skills/interact/scripts/interact-server.js ask --schema .agents/skills/interact/examples/ongoing-step-1.json
node .agents/skills/interact/scripts/interact-server.js wait --id ongoing-demo
node .agents/skills/interact/scripts/interact-server.js update --id ongoing-demo --schema .agents/skills/interact/examples/ongoing-step-2.json
node .agents/skills/interact/scripts/interact-server.js wait --id ongoing-demo --after-seq 1
node .agents/skills/interact/scripts/interact-server.js update --id ongoing-demo --schema .agents/skills/interact/examples/ongoing-step-3.json
node .agents/skills/interact/scripts/interact-server.js wait --id ongoing-demo --after-seq 2
```

The page at `/i/ongoing-demo` stays open and updates automatically. The latest
answer is written to `.interact/answers/ongoing-demo.json`; the complete answer
history is appended to `.interact/answers/ongoing-demo.jsonl`.

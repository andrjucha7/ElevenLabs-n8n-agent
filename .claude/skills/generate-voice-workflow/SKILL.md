---
name: generate-voice-workflow
description: Main orchestration skill. Takes a user's idea (one sentence) and generates both a production-ready ElevenLabs voice agent prompt AND a matching deployed n8n workflow in one shot. Use whenever the user describes something they want to build, e.g. "I want an apartment-setter voice agent", "Build me a lead-gen caller", "I need a booking agent for my dental clinic". Always generates BOTH outputs — never just one.
---

# Generate Voice Workflow

Take the user's idea and produce two matched, production-ready outputs:
1. An ElevenLabs voice agent system prompt (saved to `output-prompts/`)
2. A deployed n8n workflow (via n8n-mcp) that the voice agent calls

---

## Phase 1 — Context Extraction

Read `CLAUDE.md` first to recall the use case mapping table.

Extract the following from the user's idea. Ask for what's missing in **one single message** (not one-by-one):

**Required:**
- Company / project name (or use placeholder if user skips)
- Industry / what the business does (one line)
- Use case: appointment booking / inbound FAQ / outbound lead gen / customer service / other
- Call goal: what should be achieved by end of call?
- Tone: formal ("Sie" / "You") or casual ("du" / "you")
- Agent name (or suggest one based on context)
- Language for the generated prompt (default: match user's language)

**Ask only if relevant to the use case:**
- Tools needed (calendar API, CRM, booking system, etc.)
- Dynamic variables passed via API (caller's name, vehicle info, etc.)
- Business hours / locations
- Escalation phone number for `transfer_to_number`
- Forbidden topics or constraints

**Shortcut**: If the user's idea already contains enough context (e.g. "apartment-setter voice agent for a real estate company, formal tone, English"), extract directly without asking. Only ask for genuine gaps.

---

## Phase 2 — Select Templates

### ElevenLabs Template Selection
Read all files in `vorlagen/` and `plattform-guides/elevenlabs.md`.

| Use Case | Template File |
|---|---|
| Appointment booking | `vorlagen/terminbuchung.md` |
| Inbound FAQ / general info | `vorlagen/inbound-faq.md` |
| Outbound lead generation | `vorlagen/outbound-leadgen.md` |
| Customer service / support | `vorlagen/kundenservice.md` |
| Other | Build from scratch using structure in `plattform-guides/elevenlabs.md` |

### n8n Template Selection
Run `ls n8n-templates/` — do NOT read the JSON files yet.

Match the use case to the closest filename by keyword overlap. If no template matches, note this and offer to build one from scratch after the prompt is done.

---

## Phase 3 — Generate ElevenLabs Voice Agent Prompt

Fill the selected template with the extracted context. Adapt for the user's language — translate all placeholder text if needed.

**Quality checklist:**
- [ ] Every conversation path ends with `hangup`
- [ ] `<wait for user response>` after every question
- [ ] All tools listed under `# Tools` section
- [ ] Numbers and dates written out (e.g. "March fifteenth" not "15.03")
- [ ] No markdown formatting in spoken text (no `**bold**`, no `- lists`)
- [ ] `{{system__time}}` and `{{system__date}}` used where relevant
- [ ] Recommended First Message at the bottom (labeled clearly as separate from prompt)
- [ ] All `[PLACEHOLDER]` values either filled or marked with `[FILL IN: description]`

**n8n webhook integration**: In the Tools section of the prompt, add the n8n webhook URL placeholder:

```
# Tools
- 'kalenderCheck': Check calendar availability. Endpoint: POST [N8N_WEBHOOK_URL]?action=check
- 'terminBuchen': Book an appointment. Endpoint: POST [N8N_WEBHOOK_URL]?action=book
- 'hangup': End the call.
```

Save the completed prompt to:
`output-prompts/[company-name]-[use-case].md`

(lowercase, hyphens, no spaces)

---

## Phase 4 — Deploy n8n Workflow

Read the matched template JSON (the single file, not all of them).

**Strip credentials**: Walk the `nodes` array and delete the `credentials` key from every node. Do not modify anything else.

Deploy via MCP:
```
mcp__n8n-mcp__n8n_create_workflow(
  name: "[filename without .json]",
  nodes: [cleaned nodes array],
  connections: [connections object from template]
)
```

If no matching template exists:
- Tell the user which templates are available
- Offer to build a custom workflow — load `n8n-workflow-patterns` skill and design from scratch

After deploy, capture:
- Workflow ID
- Webhook path (from the Webhook node's `path` parameter)
- Full webhook URL: `[N8N_INSTANCE_URL]/webhook/[path]`

---

## Phase 5 — Present Unified Output

Present both outputs in a clear, structured summary:

---

### Output Summary

**ElevenLabs Voice Agent — [Agent Name]**
Saved to: `output-prompts/[filename].md`

[Print the full generated prompt here]

---

**n8n Workflow — [Workflow Name]**
Workflow ID: `[id]`
Webhook URL: `[full URL]`

---

### Integration: Wiring the Two Together

**Step 1 — Configure the webhook URL in ElevenLabs**
In the ElevenLabs Dashboard, open your agent → Tools.
Set the endpoint for `kalenderCheck` and `terminBuchen` to:
`[WEBHOOK_URL]`

**Step 2 — Set credentials in n8n**
In your n8n instance, open the workflow "[name]" and re-link credentials for:
- [list nodes that had credentials stripped]

**Step 3 — Set the First Message in ElevenLabs**
Copy the "Recommended First Message" from the prompt and paste it into the ElevenLabs Dashboard → Agent → First Message field.

**Step 4 — Configure dynamic variables (if any)**
In ElevenLabs Dashboard → Agent Settings → Variables, add: [list variables from prompt]

**Step 5 — Activate the n8n workflow**
Click "Activate" in n8n. The workflow is now listening at the webhook URL.

**Step 6 — Test**
Use the test payload in `n8n-input-examples/` to verify the workflow responds correctly, then run a test call in ElevenLabs.

---

## Rules

- **Always complete both Phase 3 and Phase 4** before presenting output — never deliver one without the other.
- **Match the user's language** in the generated prompt. The templates are in German; translate placeholders and spoken text to the user's language if different.
- **Never invent business facts** — use `[FILL IN: ...]` placeholders for anything the user hasn't provided.
- **Don't re-read templates you haven't matched** — filename matching only until deploy phase.
- **If n8n MCP is not connected**: Generate the ElevenLabs prompt fully, then offer to save the workflow JSON to `output-workflows/` for manual import instead of live deploy.

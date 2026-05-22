# VA-N8N — Voice Agent + Workflow Generator

## What This Is

A combined workspace that takes **one user idea** and produces two matched outputs simultaneously:

1. **ElevenLabs voice agent prompt** — a production-ready system prompt for a conversational AI phone agent
2. **n8n workflow** — the backend automation that the voice agent calls (webhooks, calendar checks, CRM updates, etc.)

The two outputs are designed to work together: the ElevenLabs agent calls the n8n webhook; n8n handles the business logic.

**Example input**: "I want an apartment-setter voice agent"
**Output**: A fully configured ElevenLabs agent prompt (with tools, tone, conversation flow) + a deployed n8n workflow with a webhook the agent can call to check and book slots.

---

## Layout

```
CLAUDE.md                          — This file. Project instructions.
.mcp.json.example                  — Safe MCP config scaffold with dummy values; tracked in git.
.mcp.json                          — Runtime MCP config with real keys; gitignored AND claudeignored (AI must never read it).
.claude/skills/
  generate-voice-workflow/         — MAIN SKILL: one-shot idea → both outputs
  deploy-template/                 — Deploy an n8n template to the n8n instance
  prompt-generieren/               — Generate a standalone ElevenLabs prompt
  n8n-workflow-patterns/           — n8n architectural patterns reference
  n8n-mcp-tools-expert/            — n8n MCP tool usage guide
  n8n-node-configuration/          — n8n node config reference
  n8n-validation-expert/           — n8n workflow validation
  n8n-code-javascript/             — n8n Code node JS patterns
  n8n-expression-syntax/           — n8n expression syntax reference
n8n-templates/                     — Pre-built n8n workflow JSONs (filename = workflow name)
n8n-input-examples/                — Sample webhook payloads for testing
output-workflows/                  — Exported/generated workflow JSONs
output-prompts/                    — Generated ElevenLabs voice agent prompts
plattform-guides/elevenlabs.md     — ElevenLabs conventions (structure, tools, tone)
prompt-templates/                  — ElevenLabs prompt templates by use case
  appointment-booking.md           — Appointment booking
  inbound-faq.md                   — Inbound FAQ / general info
  outbound-lead-generation.md        — Outbound lead generation
  customer-service.md              — Customer service
```

---

## Core Workflow

1. **User provides an idea** — one sentence, e.g. "I want an apartment-setter voice agent"
2. Run `/generate-voice-workflow` — the main skill that orchestrates both generators
3. The skill extracts structured context (use case, industry, tone, tools needed, integrations)
4. It generates and saves the **ElevenLabs prompt** to `output-prompts/`
5. It matches and deploys the **n8n workflow** via the n8n-mcp MCP server, and optionally deploys the **ElevenLabs agent** directly via elevenlabs MCP
6. It presents both outputs with a **unified integration guide** showing how to wire them together

---

## Use Cases & Template Mapping

| User Idea Keywords | ElevenLabs Template | n8n Template |
|---|---|---|
| appointment, booking, calendar, setter | `appointment-booking.md` | `appointment-setter-google-cal.json` |
| FAQ, info, questions, hours, prices | `inbound-faq.md` | (webhook + response node) |
| lead gen, outbound, cold call, sales | `outbound-lead-generation.md` | (webhook + CRM node) |
| customer service, support, complaints | `customer-service.md` | (webhook + ticketing) |

---

## Integration Architecture

The two systems connect via **webhook**:

```
Caller → ElevenLabs Agent
           │
           ├─ Tool: kalenderCheck ──→ POST /webhook/[n8n-path]?action=check
           ├─ Tool: terminBuchen  ──→ POST /webhook/[n8n-path]?action=book
           └─ Tool: hangup        ──→ (ElevenLabs built-in)
                                          │
                                   n8n Workflow
                                   ├─ Webhook node (receives call)
                                   ├─ Google Calendar (check/create event)
                                   ├─ CRM update (optional)
                                   └─ Webhook Response (returns result to agent)
```

The webhook URL from the deployed n8n workflow is the endpoint the ElevenLabs agent tools call. After generation, the user configures this URL in the ElevenLabs Dashboard under the tool definitions.

---

## Rules

- **Always generate both outputs** when the user gives an idea — never just one.
- **Don't invent n8n credentials** — strip them on deploy; user re-links in the n8n UI.
- **Don't invent business facts** — if the user hasn't provided company name, hours, or agent name, use clear placeholders (e.g., `[COMPANY NAME]`) and list what needs filling in.
- **Match by filename** for n8n templates — don't read all JSONs eagerly.
- **ElevenLabs prompts are always complete and directly usable** — every conversation path ends with `hangup`.
- **Output language** — match the user's language. If the user writes in English, generate the ElevenLabs prompt in English. German templates are the base; adapt to user's language.
- **Save outputs** to `output-prompts/[company]-[usecase].md` and `output-workflows/` respectively.
- **MCP Security Protocol** — Never read, print, or inspect `.mcp.json`. Assume MCP tools are configured and available. If a tool call fails, ask the operator to verify their `.mcp.json` values.

---

## MCP Integration

Two MCP servers are configured via `.mcp.json` (n8n and ElevenLabs) and provide complementary automation.

### Configuration & Secrets

- **MCP routing** lives in `.mcp.json` at the repo root (runtime file, gitignored and claudeignored). It holds the real API keys and URLs for the MCP servers.
- **Safe scaffold**: `.mcp.json.example` is tracked in git and contains only dummy placeholder values. Operator flow: copy `.mcp.json.example` → `.mcp.json`, then fill in real values manually — never commit `.mcp.json`.
- **Never hardcode secrets** in scripts, skills, or tracked files. Never commit `.mcp.json` to version control.

### MCP Security Protocol

- **AI must never attempt to read `.mcp.json`** — it is claudeignored. The AI must assume MCP tools are properly configured and available.
- If an MCP tool call fails, report the error and ask the operator to verify their `.mcp.json` values — do not try to inspect the file.
- Never suggest reading, printing, or echoing `.mcp.json` contents.

### Dual-key architecture (n8n)

| Variable | Used by | Purpose |
|---|---|---|
| `N8N_API_KEY` (in `.mcp.json`) | Claude / MCP (`n8n`) | Real-time workflow create/update/deploy during agent sessions |
| `N8N_API_KEY` (in scripts) | Developer `core/scripts/sync.py` (`npm run sync`) | REST API access to download workflow JSON into the repo for version control |

Both uses share the same key type but may be scoped differently. The `.mcp.json` key powers AI execution; the script key powers repository maintenance only.

### n8n MCP server

Exposes tools for creating, updating, and managing n8n workflows (server name: `n8n` in `.mcp.json`):

- `mcp__claude_ai_n8n__create_workflow_from_code` — deploy a workflow
- `mcp__claude_ai_n8n__update_workflow` — update an existing workflow
- `mcp__claude_ai_n8n__get_workflow_details` — read a deployed workflow

Set `N8N_HOST` and `N8N_API_KEY` in `.mcp.json` (copy from `.mcp.json.example`) before deploying via MCP.

### ElevenLabs MCP server

Exposes tools for creating, configuring, and managing ElevenLabs conversational AI agents directly (server name: `ElevenLabs` in `.mcp.json`):

**Agent Management:**
- `mcp__elevenlabs__create_agent` — create a new agent (name, system prompt, voice, model, tools)
- `mcp__elevenlabs__get_agent` — retrieve existing agent config
- `mcp__elevenlabs__list_agents` — list all agents in the account

**Voice & Audio:**
- `mcp__elevenlabs__text_to_speech` — generate audio from text
- `mcp__elevenlabs__search_voices` / `mcp__elevenlabs__get_voice` — find and retrieve voices
- `mcp__elevenlabs__voice_clone` — clone a voice from audio

**Calls & Conversations:**
- `mcp__elevenlabs__make_outbound_call` — initiate an outbound call from an agent
- `mcp__elevenlabs__list_conversations` / `mcp__elevenlabs__get_conversation` — conversation history and transcripts

**Knowledge & Context:**
- `mcp__elevenlabs__add_knowledge_base_to_agent` — attach a knowledge base to an agent

Set `ELEVENLABS_API_KEY` in `.mcp.json` (copy from `.mcp.json.example`). Output files are written to `output-prompts/` for version control.

**Key benefit**: Instead of manually copying prompts into the ElevenLabs Dashboard, `/generate-voice-workflow` can now deploy the agent directly via MCP — making the entire setup one-shot.

---

## Skills Reference

| Skill | Trigger | What it does |
|---|---|---|
| `/generate-voice-workflow` | User gives an idea | Main orchestrator — both outputs at once |
| `/deploy-template` | "Deploy [template name]" | Deploy a specific n8n template only |
| `/prompt-generieren` | "Generate a voice prompt for..." | Generate ElevenLabs prompt only |

Supporting skills (loaded automatically when needed):
- `n8n-workflow-patterns` — architectural guidance when building/customizing workflows
- `n8n-mcp-tools-expert` — how to use n8n MCP tools correctly
- `n8n-node-configuration` — node-specific config rules
- `n8n-validation-expert` — validate before activating
- `n8n-code-javascript` — Code node JS patterns
- `n8n-expression-syntax` — expression syntax gotchas

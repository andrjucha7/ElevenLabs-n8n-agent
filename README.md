# ElevenLabs n8n Voice Agent

Integrate ElevenLabs Conversational AI Voice Agents with n8n to build real-time, low-latency voice assistants that can execute complex workflows across your entire tech stack—no code required. 

This repository provides the configuration, workflow templates, and guidelines needed to connect an ElevenLabs smart voice agent to an n8n instance, enabling your voice assistant to interact with databases, CRMs, APIs, calendar events, and much more.

## Features

- **Real-Time Workflow Execution:** Voice agents trigger n8n workflows via secure webhooks instantly, delivering sub-second response times.
- **Dynamic Context Management:** Maintain conversation state and pass rich, real-time data back to ElevenLabs to personalize responses.
- **Extensive App Connectivity:** Seamlessly bridge ElevenLabs with over 1,000+ pre-built n8n nodes (Google Workspace, Slack, HubSpot, PostgreSQL, etc.).

---

## Prerequisites

Before you begin, ensure you have the following:

1. **ElevenLabs Account:** Access to the [ElevenLabs Conversational AI Dashboard](https://elevenlabs.io/agents) to create and train your voice agent.
2. **n8n Instance:** A self-hosted (Docker/npm) or Cloud-hosted instance of n8n (v1.39.1 or above recommended).
3. **API Keys:**
   - ElevenLabs API key (`xi-api-key`).
   - Relevant API keys for any third-party integrations inside your n8n workflow.

# VoiceOps Boilerplate: ElevenLabs + n8n

> **Production-ready integration framework** for building voice agents that execute backend workflows. Bridge conversational AI with enterprise automation.

---

## What This Is

VoiceOps Boilerplate is an enterprise-grade SDK for integrating **ElevenLabs Conversational AI** (voice agents) with **n8n** (workflow automation). Think of it as a reference architecture + deployment toolkit.

**In one sentence:** Deploy a voice-enabled AI agent that handles calendar bookings, lead qualification, or customer support—complete with backend logic, CRM updates, and payment processing—in minutes, not weeks.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Inbound Caller                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
     ┌─────────────────────────────────────┐
     │   ElevenLabs Conversational AI       │
     │   (WebRTC, Voice, Tool Integration) │
     └────────────┬────────────────────────┘
                  │
        POST /webhook/[path]
          + ?tool_name=check_calendar
                  │
                  ▼
     ┌─────────────────────────────────────┐
     │         n8n Workflow Engine         │
     │  ┌─────────────────────────────┐   │
     │  │ Webhook Router (Switch Node)│   │
     │  └──────────┬──────────────────┘   │
     │             │                       │
     │  ┌──────────┴──────────┐           │
     │  ▼                     ▼           │
     │ Google Calendar    Database/CRM   │
     │ (Date/Time Ops)    (Lead Logs)   │
     │                                   │
     │  Returns structured JSON response │
     └────────────┬────────────────────┘
                  │
        POST response to agent
                  │
                  ▼
     Agent interpolates in next turn
     of conversation and continues...
```

---

## One-Click Deployment Matrix

| Use Case | Template | Nodes | Est. Setup | Status |
|----------|----------|-------|-----------|--------|
| Appointment Booking | `templates/customer-support` | Webhook → Google Calendar → Respond | 20 min | ✓ Production Ready |
| Outbound Sales | `templates/outbound-sales` | (Placeholder) | TBD | 🔄 Coming Soon |
| Knowledge-Base FAQ | (Custom) | Webhook → Vector DB → Respond | 30 min | Available via skills |

---

## Quick Start

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/yourusername/va-n8n.git
cd va-n8n
pip install -r requirements.txt
npm install  # (optional, for npm scripts)
```

### 2. Deploy a Template

#### Option A: Import to n8n Manually

1. In n8n Dashboard: **Create New Workflow** → **Import**
2. Select `templates/customer-support/workflow.json`
3. Link Google Calendar OAuth2 credential
4. Activate and copy webhook URL

#### Option B: Use Sync Utility (Programmatic)

```bash
export N8N_API_URL="https://your-instance.app.n8n.cloud"
export N8N_API_KEY="your_api_key"

npm run sync -- --n8n-id [WORKFLOW_ID] --output templates/customer-support
```

### 3. Configure ElevenLabs Agent

1. Create a new Conversational AI agent in ElevenLabs Dashboard
2. Copy system prompt from `templates/customer-support/base_agent.txt`
3. Fill in the [PLACEHOLDERS] (company name, agent name, hours, etc.)
4. Add three tools with this webhook URL:
   - **check_calendar** → `POST /webhook/elevenlabs-gcal-booking?tool_name=check_calendar`
   - **book_calendar** → `POST /webhook/elevenlabs-gcal-booking?tool_name=book_calendar`
   - **hangup** → Built-in ElevenLabs tool

### 4. Test the Flow

```bash
curl -X POST "https://your-n8n/webhook/elevenlabs-gcal-booking?tool_name=check_calendar" \
  -H "Content-Type: application/json" \
  -d '{"requested_time": "2026-05-25T14:00", "caller_name": "John Doe"}'
```

Expect a response with available time slots.

---

## Developer Workflow

### Configuration: Dual-key setup

This project separates **MCP server routing** from **secrets**:

1. Copy `.mcp.json.example` to `.mcp.json` and fill in your real API keys manually (`.mcp.json` is never committed — it is gitignored and claudeignored).
2. MCP server configuration and credentials live exclusively in `.mcp.json` at the repo root.

| Credential | Where | When you need it |
|---|---|---|
| `N8N_HOST` + `N8N_API_KEY` | `.mcp.json` | **Required** for AI agents (Claude Code) to deploy and edit workflows via MCP in real time |
| `N8N_API_KEY` + `N8N_API_URL` | env vars / scripts | **Optional** — only if you run `npm run sync` / `core/scripts/sync.py` to pull workflow JSON from n8n into the repo |
| `ELEVENLABS_API_KEY` | `.mcp.json` | **Required** for ElevenLabs MCP tools (agent create/update, voices, calls) |

The `.mcp.json` key powers AI execution; the script key powers repository maintenance only. Never commit `.mcp.json`.

### Understanding the Directory Structure

```
va-n8n/
├── templates/              # Ready-to-deploy use-case folders
│   ├── customer-support/   # Appointment booking (production)
│   │   ├── workflow.json   # n8n workflow export
│   │   ├── agent_config.json  # ElevenLabs config template
│   │   ├── base_agent.txt  # System prompt (fill placeholders)
│   │   └── README.md       # Use-case specific docs
│   └── outbound-sales/     # Placeholder (coming soon)
│
├── core/                   # Shared utilities
│   ├── scripts/
│   │   └── sync.py         # Bi-directional sync: n8n ↔ local templates
│   └── ...
│
├── n8n-templates/          # (Legacy) Export storage
├── prompt-templates/       # ElevenLabs prompt templates by use case
├── plattform-guides/       # Platform-specific guidance
│
├── .github/workflows/      # CI/CD pipelines
│   └── lint.yml            # Automated validation on push
│
├── package.json            # npm task runner
├── requirements.txt        # Python dependencies
├── .mcp.json.example       # Safe MCP config scaffold with dummy values (tracked in git)
├── .mcp.json               # Runtime MCP config with real keys (gitignored, claudeignored — never commit)
├── .env.example            # Template for .env setup (copy to .env locally)
├── CLAUDE.md               # Claude Code project instructions
└── README.md               # This file
```

### Common Development Tasks

#### Validate All Configs

```bash
npm run lint:workflows
npm run lint:configs
```

#### Sync a Deployed Workflow Back to Local

```bash
python3 core/scripts/sync.py \
  --n8n-id [WORKFLOW_ID_FROM_N8N] \
  --output templates/my-use-case
```

#### Add a New Template

1. Create folder: `templates/my-use-case/`
2. Copy structure from `customer-support/`:
   - `workflow.json` (export from n8n)
   - `agent_config.json` (ElevenLabs config)
   - `base_agent.txt` (system prompt)
   - `README.md` (setup + customization guide)

#### Push Changes

```bash
git add templates/
git commit -m "feat: Add new [use-case] template"
git push origin main
```

CI/CD will automatically validate JSON syntax and structure.

---

## File Naming & Conventions

- **Workflow files:** `workflow.json` (always this name for clarity)
- **Agent configs:** `agent_config.json` (JSON schema for tool definitions)
- **Prompts:** `base_agent.txt` (plaintext for readability; fill [PLACEHOLDERS] at deploy time)
- **README:** Use-case specific, document nodes, tools, webhook schema, customization points
- **Credentials:** Use n8n credential IDs (e.g., `"id": "G4q2IMepxRlWc1mc"`), never embed API keys

---

## Security & Best Practices

### Credential Management

- Copy `.mcp.json.example` to `.mcp.json` and fill in real keys manually; never commit `.mcp.json`
- `.mcp.json` is both gitignored and claudeignored — the AI cannot read it and must never attempt to
- All actual API keys are stored in n8n's credential vault (not exported)
- Exported JSONs contain only credential ID references
- Before committing: run `npm run lint:configs` to ensure no raw secrets

### Webhook Authentication

Optional: Add custom Authorization header in agent config:
```json
"webhook": {
  "url": "https://your-n8n.cloud/webhook/path",
  "authHeader": "Authorization: Bearer [CUSTOM_TOKEN]"
}
```

Then update n8n Webhook node to validate this header.

### Data Privacy

- Workflows do not persist caller data; rely on your n8n instance's retention policies
- Ensure ElevenLabs agent is configured per your regional privacy laws (GDPR, CCPA, etc.)
- Audit logs available in both ElevenLabs Dashboard and n8n Executions

---

## Troubleshooting

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| "Webhook returned 404" | n8n workflow not active or path mismatch | Activate workflow, verify `path` parameter matches tool URL |
| "Credential not found" | OAuth2 credential deleted or n8n instance reset | Re-link Google Calendar in n8n Dashboard, update credential ID in workflow nodes |
| "No available slots returned" | Calendar has no events to test against | Create a busy event; test with intentionally full calendar first |
| "Agent says 'I couldn't reach the system'" | Network/timeout issue or 500 error from n8n | Check n8n Execution logs; verify webhook URL is reachable |

See `templates/[use-case]/README.md` for scenario-specific troubleshooting.

---

## Related Skills & Resources

- **`/generate-voice-workflow`** — Create both prompt + workflow in one command
- **`/deploy-template`** — Deploy a pre-built template to n8n
- **`/n8n-workflow-patterns`** — Architectural guidance for building custom workflows
- **`/prompt-generieren`** — Generate standalone ElevenLabs prompts
- **ElevenLabs Docs:** https://docs.elevenlabs.io/convai/overview
- **n8n Docs:** https://docs.n8n.io/

---

## Contributing

This is a reference boilerplate. To extend it:

1. **New Template:** Create `templates/[use-case]/` with the full structure
2. **Bug Fix:** Create an issue or PR with a minimal reproduction
3. **Docs:** Update relevant `README.md` files (not separate blog posts)

All contributions must pass `npm run lint:workflows && npm run lint:configs`.

---

## License

MIT — Use freely in personal and commercial projects. Attribution appreciated but not required.

---

## Support

- **Bugs or questions?** Open an issue on GitHub
- **Feature requests?** Use `/feedback` in Claude Code to suggest enhancements
- **Integration help?** Check `templates/[your-use-case]/README.md` for detailed setup guides

---

**Last Updated:** May 2026  
**Status:** Production Ready (Customer Support template tested and live)

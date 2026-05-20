# ElevenLabs n8n Voice Agent

Integrate ElevenLabs Conversational AI Voice Agents with n8n to build real-time, low-latency voice assistants that can execute complex workflows across your entire tech stack—no code required. 

This repository provides the configuration, workflow templates, and guidelines needed to connect an ElevenLabs smart voice agent to an n8n instance, enabling your voice assistant to interact with databases, CRMs, APIs, calendar events, and much more.

## Features

- **Real-Time Workflow Execution:** Voice agents trigger n8n workflows via secure webhooks instantly, delivering sub-second response times.
- **Dynamic Context Management:** Maintain conversation state and pass rich, real-time data back to ElevenLabs to personalize responses.
- **Extensive App Connectivity:** Seamlessly bridge ElevenLabs with over 1,000+ pre-built n8n nodes (Google Workspace, Slack, HubSpot, PostgreSQL, etc.).
- **Seamless Human Handoff:** Build escalating workflows that notify human agents (via Slack/Email) when the AI encounters a complex scenario.

---

## Prerequisites

Before you begin, ensure you have the following:

1. **ElevenLabs Account:** Access to the [ElevenLabs Conversational AI Dashboard](https://elevenlabs.io/agents) to create and train your voice agent.
2. **n8n Instance:** A self-hosted (Docker/npm) or Cloud-hosted instance of n8n (v1.39.1 or above recommended).
3. **API Keys:**
   - ElevenLabs API key (`xi-api-key`).
   - Relevant API keys for any third-party integrations inside your n8n workflow.

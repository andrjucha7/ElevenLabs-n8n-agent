# Customer Support: Appointment Setter Template

## Overview
This template implements an automated appointment scheduling system for customer support channels. The ElevenLabs voice agent handles inbound booking requests, while the n8n workflow manages calendar operations and availability logic.

## Architecture

### n8n Workflow Nodes

The workflow processes webhook requests from ElevenLabs and routes them based on the requested action:

**Routing Layer:**
- **Webhook** — Receives POST requests from ElevenLabs agent
- **Set Main** — Extracts and normalizes caller details (name, email, requested time)
- **Route by Tool** — Switch node that routes to calendar-check or calendar-book flows

**Calendar Check Flow:**
- **Get Events for Week** — Queries Google Calendar for 7-day availability window
- **Any Busy Slots?** — Conditional: has calendar events been returned?
- **Compute Free Slots** — JavaScript code node that:
  - Parses busy events (supports both all-day and timed events)
  - Generates 30-min appointment slots (08:00–17:00 daily)
  - Returns message with 3 recommended slots
  - Tracks week-wide availability metadata
- **Respond - Available Slots** — Returns candidate times to agent
- **Respond - Day Is Free** — Handles empty-calendar edge case

**Calendar Book Flow:**
- **Check Slot Available** — Validates the requested 30-minute slot is free
- **Is Slot Free?** — Conditional: does the slot conflict with existing events?
- **Book Appointment** — Creates Google Calendar event with:
  - Automatic Google Meet link
  - Caller name in event title
  - Caller email in event description
- **Respond - Booking Success** — Confirms booking to agent
- **Respond - Booking Failed** — Notifies agent of conflict

**Error Handling:**
- All Google Calendar nodes have `onError: continueErrorOutput`
- Respond - Check Failed handles API failures gracefully

### Webhook Payload Format

**Check Calendar Request:**
```json
{
  "tool_name": "check_calendar",
  "body": {
    "requested_time": "2026-05-25T14:00"
  }
}
```

**Book Calendar Request:**
```json
{
  "tool_name": "book_calendar",
  "body": {
    "requested_time": "2026-05-25T14:00",
    "caller_name": "John Doe",
    "caller_email": "john@example.com"
  }
}
```

### ElevenLabs Agent Tools

The voice agent uses three tools to interact with the workflow:

1. **check_calendar** — Query availability for a specific datetime
2. **book_calendar** — Create a confirmed appointment
3. **hangup** — End the call

Each tool call issues a webhook POST to the n8n webhook endpoint with the `tool_name` query parameter.

## Setup Instructions

### 1. Obtain Credentials

- **Google Calendar OAuth2**: Link a Google account with calendar read/write permissions
  - Used in nodes: "Get Events for Week", "Check Slot Available", "Book Appointment"
  - Credentials ID placeholder: `G4q2IMepxRlWc1mc` (replace with your linked credential)

### 2. Configure n8n Workflow

1. Import `workflow.json` into your n8n instance
2. In the Google Calendar nodes, select or link your Google Calendar OAuth2 credential
3. Set the calendar ID (default: "primary") to match your target calendar
4. Activate the workflow
5. Copy the generated webhook URL: `https://[YOUR_N8N_INSTANCE]/webhook/elevenlabs-gcal-booking`

### 3. Create ElevenLabs Agent

1. Deploy or update an ElevenLabs Conversational AI agent
2. Use `base_agent.txt` as the system prompt (fill in [PLACEHOLDERS])
3. Configure three tools:
   - **check_calendar** — POST to webhook with `?tool_name=check_calendar`
   - **book_calendar** — POST to webhook with `?tool_name=book_calendar`
   - **hangup** — Built-in ElevenLabs tool
4. Set voice and model per `agent_config.json`

### 4. Deployment Checklist

- [ ] n8n workflow is active and webhook URL is copied
- [ ] Google Calendar credential is linked in all calendar nodes
- [ ] ElevenLabs agent is deployed with correct webhook URL and tool definitions
- [ ] First Message is configured in ElevenLabs Dashboard
- [ ] Test with a sample call to verify check → book flow

## Customization

### Adjust Working Hours

Edit the Code node "Compute Free Slots":
```javascript
const DAY_START_TIME = "08:00";      // Change to your opening time
const DAY_END_TIME = "17:00";        // Change to your closing time
const APPOINTMENT_LENGTH_MINUTES = 30; // Slot duration
const DAYS_TO_LOOK_AHEAD = 7;        // Search window
```

### Change Appointment Duration

In the same Code node, adjust:
```javascript
const APPOINTMENT_LENGTH_MINUTES = 45; // Change from 30 to 45, etc.
```

### Modify Calendar Email/Calendar ID

In Google Calendar nodes:
- Change `placeholder@gmail.com` to your actual calendar email
- Change `primary` to a specific calendar ID if using multiple calendars

## File Structure

```
templates/customer-support/
├── workflow.json         # Exported n8n workflow (ready-to-import)
├── agent_config.json     # ElevenLabs agent configuration template
├── base_agent.txt        # ElevenLabs system prompt (fill placeholders)
└── README.md             # This file
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Credential not found" error | Link Google Calendar OAuth2 in n8n, update credential ID in nodes |
| "Webhook returned with error" | Check that ElevenLabs is sending correct `tool_name` query parameter |
| No slots returned | Verify calendar has events to check against; test with intentionally busy calendar |
| Agent hangs on booking | Ensure "Book Appointment" node is configured and connected correctly |

## Security Notes

- **Credential Storage**: All Google Calendar credentials are stored in n8n's secure credential vault; the exported JSON contains placeholder references only
- **Webhook Auth**: Add optional authorization header in `agent_config.json` if your n8n instance requires one
- **Data Retention**: The workflow does not store caller data; ensure your ElevenLabs account is configured per your privacy policy
- **Calendar Scope**: This workflow reads/writes to a single calendar. Ensure the credential has appropriate permissions.

## Related Templates

- **Outbound Sales** — For proactive outbound calling with lead capture
- **Inbound FAQ** — Simpler inbound bot with knowledge base lookups (no calendar)

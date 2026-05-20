# Skill: Generate Prompt

## Purpose
This skill guides the flow for creating a production-ready ElevenLabs
voice AI prompt from the user's description.

## Triggers
Activate when the user wants a new agent prompt:
- "Create a prompt for..."
- "I need an agent for..."
- "Build me a voice agent for..."

## Flow

### Phase 1 — Information gathering
Read `CLAUDE.md`, `plattform-guides/elevenlabs.md`, and all files in `prompt-templates/`.

Required fields — ask targeted questions for:
- Company name
- Industry / what the business offers
- Use case (inbound FAQ / appointment booking / outbound / customer service / other)
- Call goal (what should be achieved by the end of the call?)
- Desired tone (formal / informal)
- Agent name
- Which tools are needed? (e.g. calendar API, booking system, CRM)

Optional fields (only ask when relevant to the use case):
- Dynamic variables passed via API (e.g. name, vehicle details)
- Locations and business hours
- Escalation number for `transfer_to_number`
- Forbidden topics or special constraints
- Contact email or phone for handoff instructions

### Phase 2 — Select template
- Inbound FAQ → `prompt-templates/inbound-faq.md`
- Appointment booking → `prompt-templates/appointment-booking.md`
- Outbound → `prompt-templates/outbound-lead-generation.md`
- Customer service → `prompt-templates/customer-service.md`
- Other → build from scratch using the structure in `plattform-guides/elevenlabs.md`

### Phase 3 — Fill the prompt
Replace all placeholders with the gathered information. Adapt the step
structure to the concrete use case — add or remove steps as needed. Ensure:
- Every conversation path ends with hangup
- `<wait for user response>` follows every question
- All tools are listed in the Tools section
- Numbers and dates are spoken naturally (not as raw digits in speech)
- No markdown is used in spoken text

### Phase 4 — Save and output
Save to: `output-prompts/[company-name]-[use-case].md`

Output the full prompt in chat. Then explicitly remind the user of these manual steps:
1. Enter the First Message in the ElevenLabs dashboard (from the last section of the prompt)
2. Create tools in the dashboard and link them using the names from the prompt
3. Configure dynamic variables in agent settings (if applicable)

# Outbound Sales: Lead Generation Template

## Overview
This template scaffolds an outbound voice agent for proactive lead generation campaigns. The agent initiates calls via ElevenLabs, qualifies leads based on configurable criteria, and logs outcomes to a CRM or database via n8n webhooks.

## Status
Placeholder for future implementation. Use as a reference for building outbound lead-gen workflows.

## Next Steps
1. Define lead qualification criteria (budget, use case, timeline)
2. Create n8n workflow with:
   - CRM node (HubSpot, Salesforce, etc.)
   - Outbound call initiation via ElevenLabs API
   - Lead scoring and pipeline update
3. Configure ElevenLabs prompt with discovery questions
4. Set up callback webhook for lead results

## Files
```
templates/outbound-sales/
├── workflow.json         # (TBD)
├── agent_config.json     # (TBD)
├── base_agent.txt        # (TBD)
└── README.md             # This file
```

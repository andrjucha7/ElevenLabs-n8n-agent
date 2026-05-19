---
name: deploy-template
description: Deploy a pre-built n8n workflow template from n8n-templates/ to the connected n8n instance. Use when the user says things like "deploy a template", "push the appointment setter", "I need a workflow for X", or invokes /deploy-template. Matches user intent to a template filename, preserves the filename as the workflow name, and pushes via the n8n MCP.
---

# Deploy Template

Deploy an existing n8n workflow from `n8n-templates/` to the user's n8n instance without modification. The workflow name in n8n equals the template filename (without `.json`) — do not rename.

## Flow

1. **Ask the user what they want to build.** One short question. Example: "What kind of workflow do you want to deploy? (e.g. appointment setter, lead qualifier, etc.)"

2. **List available templates.** Run `ls n8n-templates/` via Bash. Do NOT read the template JSON files yet — they can be large.

3. **Match by filename.** Pick the single best filename match against the user's description using keyword overlap. If two filenames are close, ask the user which one. If none look like a match, tell the user and list what's available.

4. **Read the matched template.** Read the full JSON of the chosen file. It contains `nodes` and `connections`.

5. **Strip credential bindings.** Walk the `nodes` array and delete the `credentials` key from every node that has one. This forces the user to re-select credentials in the n8n UI after deploy — which is the intended demo behavior. Do not strip anything else (keep `onError`, `typeVersion`, `webhookId`, etc. intact).

6. **Deploy via MCP.** Call `mcp__n8n-mcp__n8n_create_workflow` with:
   - `name`: the filename without `.json` extension (verbatim — do not rewrite, reformat, or prettify)
   - `nodes`: the cleaned `nodes` array
   - `connections`: the `connections` object from the template JSON

7. **Report back.** Give the user the workflow name, the n8n workflow ID returned, and the webhook path if the template has a webhook node. Then give them these exact next steps in the n8n UI, listing the specific node names whose credentials were stripped:
   1. Open each node that needs credentials and click **"Create new credential"** to set it up.
   2. On calendar/email/account-scoped nodes, open the calendar/account dropdown and **select the correct email/account** from the list.
   3. Activate the workflow.

## Rules

- **Preserve the filename as the workflow name.** If the file is `appointment-setter-google-cal.json`, the n8n workflow is named `appointment-setter-google-cal`. This makes future lookups (delete, update, redeploy) trivial.
- **Don't read every template file just to match names.** Filename matching is enough. Only read the one you're deploying.
- **Don't tweak the template on deploy.** This skill is for clean deploys. If the user wants changes, deploy first, then edit separately via MCP partial updates.
- **Credentials referenced by ID inside the template will need to exist on the user's n8n instance.** If deploy succeeds but nodes show credential errors, tell the user which nodes need credentials re-linked.

## Testing the deployed workflow

`n8n-input-examples/` contains JSON payloads that match specific webhook templates (by filename pattern). If the user asks to test after deploy, curl the webhook URL with the matching input example.

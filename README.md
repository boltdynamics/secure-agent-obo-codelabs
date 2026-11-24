# Secure AI Agents on Google Cloud: Codelab

Hands-on workshop for **Numbat Bank**: deploy a secure, scalable, cost-controlled, rate-limited and
governable AI agent on Google Cloud that calls an API **on behalf of** the signed-in user (OAuth 2.0
Token Exchange, RFC 8693), then compare it with an agent that holds a shared admin credential.

Written in Google Codelabs format and hosted on GitHub Pages at
**https://boltdynamics.github.io/secure-agent-obo-codelabs/**. The code lives in
[boltdynamics/secure-agent-obo](https://github.com/boltdynamics/secure-agent-obo).

## What attendees do

| Step | Focus |
|------|-------|
| Deploy | One command in Cloud Shell: `./deploy.sh` |
| OBO in action | Prompt-injection style requests fail at the bank API, not in the prompt |
| Shared admin credential | The same prompts leak data and move money; the audit trail loses the customer |
| Guardrails | Human confirmation, consent scopes, rate limits, token budgets, budget kill switch, Model Armor |
| Governance | Audit records in BigQuery; removing the unsafe path with least privilege |

## Editing

Edit `hands-on-workshop.md`, then regenerate the page:

```bash
pip install markdown
python3 scripts/export.py        # writes index.html and codelab.json
# or, with claat installed: claat export hands-on-workshop.md
```

Screenshots in `images/` were captured locally against a scripted model, so replies in a live run will
be worded differently. Diagrams are exported from Lucidchart.

## Licence

[MIT](LICENSE)

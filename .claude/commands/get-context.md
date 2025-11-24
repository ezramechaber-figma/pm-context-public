---
description: Fetch current Asana tasks and Coda roadmap to provide session context
---

You are helping me gather context at the start of a session by fetching my current Asana tasks and Coda roadmap.

## Process:

1. **Fetch Asana Tasks:**
   - Run: `cd /Users/emechaber/Code/claude-code/pm-context/tools/asana-cli && ./asana list --filter all`
   - This will show all my tasks organized by section

2. **Fetch Coda Roadmap:**
   - Run: `cd /Users/emechaber/Code/claude-code/pm-context/tools/coda-cli && ./coda get-doc "_duvJr3XqEGh"`
   - This will show the doc structure and available tables
   - Look for the "Expansion-Team-Roadmap-2025" or similar table
   - Then fetch that specific table with: `./coda get-table "_duvJr3XqEGh" "Expansion-Team-Roadmap-2025" --limit 50`

3. **Present the context:**
   - Summarize the key information from both sources
   - Highlight overdue tasks or urgent items
   - Show upcoming milestones from the roadmap
   - Note any patterns or areas that need attention

4. **Ask if I want to dive deeper:**
   - Offer to focus on specific tasks or projects
   - Ask if there are particular areas I want to discuss

## Important:
- Run the commands from the correct directories (tools/asana-cli and tools/coda-cli)
- Format the output to be scannable and useful
- Don't just dump raw data - synthesize it into useful context
- If a command fails, explain what went wrong and suggest alternatives

Start by running both commands, then present a helpful summary of my current context.

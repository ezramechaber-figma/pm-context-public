# PM Context for Claude Code

A comprehensive context management system for Product Managers using Claude Code. This repository provides tools, templates, and workflows to help Claude understand your role, projects, and stakeholders - making it a more effective product coach and assistant.

## Goal

This system gives Claude Code deep context about your work as a PM, including:
- Your role, team, and stakeholders
- Company strategy and values
- Current projects and roadmap
- Task management (Asana) and documentation (Coda)
- Custom slash commands for common workflows

With this context, Claude can help you draft documents, brainstorm ideas, manage tasks, and provide coaching tailored to your specific situation.

## Quick Start

### 1. Clone and Personalize

```bash
git clone https://github.com/YOUR-USERNAME/pm-context-public.git
cd pm-context-public
```

### 2. Configure Your Context

Edit `.claude/CLAUDE.md` to fill in your personal details:

```markdown
# About My Role
I'm the PM for [YOUR TEAM NAME], inside of [YOUR ORG].
My goal is to [YOUR PRIMARY GOAL].

# What I'm Focused On Right Now
[FILL IN]

# What I'm Most Worried About Right Now
[FILL IN]

# Stakeholders
## [NAME] (My Manager)
* My boss, who oversees [AREA]
* Background: [FILL IN]
* Been at company for [DURATION]
```

**Important sections to customize:**
- About My Role
- Current focus areas
- Stakeholders (manager, skip-level, key executives)
- CLI tool paths (update to match your local setup)

### 3. Set Up API Keys

Create your config file from the example:

```bash
cp config.json.example config.json
```

Edit `config.json` with your API credentials:

#### Get Asana API Token
1. Go to https://app.asana.com/0/my-apps
2. Click "Create new personal access token"
3. Copy the token

#### Get Your Asana User ID
1. Go to https://app.asana.com/0/my-profile-settings
2. Click on your profile
3. Your user ID is in the URL: `https://app.asana.com/0/profile/[USER_ID]`

#### Get Your Asana Project ID
1. Open your personal tasks project in Asana
2. The project ID is in the URL: `https://app.asana.com/0/[PROJECT_ID]/list`

#### Get Coda API Token
1. Go to https://coda.io/account
2. Scroll to "API Settings"
3. Click "Generate API Token"
4. Copy the token

#### Update config.json

```json
{
  "asana": {
    "api_token": "YOUR_ASANA_API_TOKEN_HERE",
    "project_ids": [
      "YOUR_PERSONAL_TASKS_PROJECT_ID"
    ],
    "assignee": "YOUR_ASANA_USER_ID"
  },
  "coda": {
    "api_token": "YOUR_CODA_API_TOKEN_HERE"
  }
}
```

### 4. Configure Slash Commands

Edit `.claude/commands/get-context.md` to reference your specific Coda roadmap:

Find this section:
```markdown
2. **Fetch Coda Roadmap:**
   - Run: `cd /Users/YOUR_USERNAME/Code/claude-code/pm-context/tools/coda-cli && ./coda get-doc "_duvJr3XqEGh"`
```

**Update the doc ID** (`_duvJr3XqEGh`) with your own Coda roadmap document:
1. Open your roadmap doc in Coda
2. Copy the doc ID from the URL: `https://coda.io/d/[DocName]_d[YOUR_DOC_ID]`
3. Replace `_duvJr3XqEGh` with your doc ID (include the `_d` prefix)

**Update the paths** to match where you cloned this repo:
```markdown
cd /Users/YOUR_USERNAME/path/to/pm-context-public/tools/asana-cli
```

### 5. Test the Setup

```bash
# Test Asana CLI
cd tools/asana-cli
./asana list

# Test Coda CLI
cd ../coda-cli
./coda whoami
./coda list
```

### 6. Try a Slash Command

In Claude Code, run:
```
/get-context
```

This should fetch your current Asana tasks and Coda roadmap, providing a helpful summary.

## What's Included

### CLI Tools

#### Asana CLI (`tools/asana-cli/`)
Manage your tasks directly from Claude Code:
- `./asana list` - View your tasks
- `./asana add "Task name" --due tomorrow` - Create tasks
- `./asana complete [task_id]` - Mark tasks complete
- `./asana reschedule [task_id] [date]` - Change due dates

[Full documentation](tools/asana-cli/README.md)

#### Coda CLI (`tools/coda-cli/`)
Read and write Coda documents:
- `./coda list` - List all docs
- `./coda get-doc [doc_id]` - View doc structure
- `./coda get-page-content [doc_id] "Page Name"` - Export pages
- `./coda create-page` / `update-page` - Modify docs

[Full documentation](tools/coda-cli/README.md)

### Slash Commands (`.claude/commands/`)

#### `/get-context`
Fetches your current Asana tasks and Coda roadmap at the start of a session. Provides a helpful summary of what you're working on and what needs attention.

#### `/write-brief`
Interactive brief writer using Figma's product brief template. Guides you through documenting a new initiative with best practices.

### Context Files (`context/`)

- `brief_template.md` - Template for product briefs
- `values.md` - Company values and culture
- Add your own strategy docs, retros, roadmaps, etc.

### Example Context (`context/example-context/`)

Sample documents showing how to structure your context:
- `fictional-expansion-roadmap.md` - Example roadmap
- `peer-nomination-for-upgrades.md` - Example project brief

## Directory Structure

```
pm-context-public/
├── .claude/
│   ├── CLAUDE.md           # Main context file (customize this!)
│   ├── commands/           # Slash commands
│   │   ├── get-context.md  # Fetch tasks & roadmap (update Coda doc ID!)
│   │   └── write-brief.md  # Interactive brief writer
│   └── settings.local.json # Local Claude settings
├── tools/
│   ├── asana-cli/          # Asana task management
│   └── coda-cli/           # Coda doc management
├── context/                # Your context documents
│   ├── brief_template.md
│   ├── values.md
│   └── example-context/    # Examples to reference
├── config.json.example     # API keys template
└── config.json             # Your API keys (gitignored)
```

## Usage Tips

### Adding More Context

Add strategy documents, roadmaps, and other context to the `context/` directory. Claude will have access to these files and can reference them when helping you.

### Customizing Commands

Edit the `.claude/commands/*.md` files to create your own workflows. Commands can run CLI tools, fetch data, and guide Claude through multi-step processes.

### Working with Claude

Once set up, Claude will:
- Know your role, goals, and stakeholders
- Access your current tasks and roadmap
- Help draft documents that align with your company's style
- Provide coaching tailored to your specific challenges
- Ask probing questions to fill in gaps

Example prompts:
- "Help me draft a brief for [initiative]" → Use `/write-brief`
- "What should I focus on this week?" → Use `/get-context` first
- "Review my message to Dylan" → Claude knows Dylan's preferences
- "Create an Asana task to follow up with Alicia tomorrow"

### Security Notes

- `config.json` is gitignored - your API keys stay local
- Consider using a separate Asana project for personal tasks
- Review what context you commit to git (especially if making this public)
- The `.mcp.json` file is symlinked - update if your MCP config is elsewhere

## Customization Ideas

- Add your team's OKRs or KPIs to `context/`
- Create commands for common workflows (e.g., `/prep-for-1-1`)
- Add scripts to pull from other tools (Linear, Jira, Notion)
- Store retro notes and learnings in `context/`
- Add templates for common documents (PRDs, one-pagers, etc.)

## Troubleshooting

### "Config file not found"
- Make sure `config.json` exists in the repo root
- Check it has valid JSON with both `asana` and `coda` sections

### CLI commands fail
- Verify your API tokens are correct (no extra spaces)
- Check project IDs and user IDs are accurate
- Run `./asana list` or `./coda whoami` to test auth

### Slash commands don't work
- Update paths in `.claude/commands/*.md` to your actual directory
- Update Coda doc IDs to your actual documents
- Make sure the commands are in `.claude/commands/` directory

### Claude doesn't use my context
- Check that `.claude/CLAUDE.md` is properly filled out
- Add more specific details about your role and stakeholders
- Reference context files explicitly when prompting

## Contributing

This is a template - fork it and make it your own! If you add useful features or tools, consider sharing them back.

## License

MIT - Use this however helps you be a better PM.

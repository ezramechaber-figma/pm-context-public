# Asana CLI

A command-line tool to manage your personal Asana tasks.

## Setup

1. Get your Asana API token:
   - Go to https://app.asana.com/0/my-apps
   - Click "Create new personal access token"
   - Copy the token

2. Create the unified config file (in the pm-context root directory):
```bash
cd /path/to/pm-context  # Navigate to the pm-context root directory
cp config.json.example config.json
```

3. Edit `config.json` and add your Asana credentials under the `asana` key:
```json
{
  "asana": {
    "api_token": "YOUR_ASANA_API_TOKEN",
    "project_ids": ["1210729963039941"],
    "assignee": "YOUR_USER_ID"
  },
  "coda": { ... }
}
```

That's it! The `./asana` wrapper script will automatically create a virtual environment and install dependencies on first run.

## Usage

### List tasks

```bash
# All tasks (default)
./asana list

# Tasks due this week
./asana list --filter week

# Overdue tasks
./asana list --filter overdue

# Tasks due today
./asana list --filter today

# Show completed tasks
./asana list --completed

# Show subtasks alongside parent tasks
./asana list --show-subtasks

# List subtasks for a specific task
./asana list TASK_ID
```

### Complete a task

```bash
./asana complete TASK_ID
```

Example:
```bash
./asana complete 1211806085741275
```

### Reschedule a task

```bash
# Specific date
./asana reschedule TASK_ID 2025-11-10

# Today
./asana reschedule TASK_ID today

# Tomorrow
./asana reschedule TASK_ID tomorrow

# Relative dates
./asana reschedule TASK_ID +3d  # 3 days from now
./asana reschedule TASK_ID +1w  # 1 week from now
```

### Add a new task

```bash
# Basic task
./asana add "Review Q4 results"

# With due date
./asana add "Prep for 1:1 with Alicia" --due tomorrow

# With notes
./asana add "Draft PRD" --due +3d --notes "Focus on user personas and success metrics"

# To a specific project (if you have multiple configured)
./asana add "Task name" --project-index 1
```

### Work with subtasks

```bash
# Add a subtask to a parent task
./asana add-subtask PARENT_TASK_ID "Subtask name"

# Add a subtask with a due date
./asana add-subtask PARENT_TASK_ID "Research competitive options" --due +2d

# Add a subtask with notes
./asana add-subtask PARENT_TASK_ID "Review findings" --due tomorrow --notes "Focus on pricing comparison"

# List all subtasks for a task
./asana list PARENT_TASK_ID

# View subtasks in your regular task list
./asana list --show-subtasks
```

## Tips

- Task IDs are shown in brackets when you list tasks: `[1211806085741275]`
- You can copy the task ID from the URL in Asana too
- Add multiple project IDs to your config if you want to manage tasks across different projects
- Subtasks appear both as separate tasks (if they have due dates) and under their parent when using `--show-subtasks`
- All task commands (complete, reschedule, update) work on subtasks too - just use the subtask ID
- The config file is stored in the pm-context root directory (`config.json`)

## Troubleshooting

If you get "Config file not found":
- Make sure you created `config.json` in the pm-context root directory
- Check that it has valid JSON with the `asana` section containing `api_token` and `project_ids` fields

If you get "Forbidden" errors:
- Check that your API token is valid
- Make sure the project IDs are correct
- Verify you have access to those projects in Asana

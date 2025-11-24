# Asana CLI Roadmap

## Current State (v1.0)
- List tasks with various filters (today, week, overdue, all)
- Complete tasks
- Reschedule tasks
- Update task notes
- Add new tasks with due dates and notes

## Proposed Enhancement: Subtask Support

**Why:** Enable hierarchical task organization, which is essential for breaking down complex work.

### Commands to Add

#### 1. Create Subtask
```bash
./asana add-subtask PARENT_TASK_ID "Subtask name" [--due DATE] [--notes TEXT]
```
- Create a subtask under an existing task
- Supports same date formats as `add` command (today, tomorrow, +3d, YYYY-MM-DD)
- Auto-assigns to configured user

#### 2. List Subtasks
```bash
./asana list TASK_ID --subtasks
```
- List all subtasks for a given task
- Show indented/hierarchical view

#### 3. Show Subtasks in Regular List
```bash
./asana list --show-subtasks
```
- Include subtasks in regular list view with indentation
- Show parent task context
- Optional flag (default behavior remains unchanged for backward compatibility)

### API Requirements

- **Create subtask:** `POST /tasks` with `parent` field set to parent task GID
- **Get subtasks:** `GET /tasks/{task_id}/subtasks` endpoint
- **Filter subtasks:** Tasks with `parent.gid` field populated are subtasks

### Implementation Notes

- Asana API supports subtasks natively via the `parent` field
- Subtasks inherit workspace but not project membership by default
- Consider adding visual hierarchy markers (indentation, └─, ├─) for better readability
- Maintain current command patterns: simple, fast, CLI-friendly

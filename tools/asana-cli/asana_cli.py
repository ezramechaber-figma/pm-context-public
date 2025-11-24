#!/usr/bin/env python3
"""
Asana CLI - Manage your personal Asana tasks from the command line
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import click
import requests
from dateutil import parser as date_parser


# Look for config file in the parent directory (pm-context/)
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR.parent.parent / "config.json"
ASANA_API_BASE = "https://app.asana.com/api/1.0"


def load_config():
    """Load configuration from config file"""
    if not CONFIG_FILE.exists():
        click.echo(f"Error: Config file not found at {CONFIG_FILE}", err=True)
        click.echo("Please create the config file with your API tokens.", err=True)
        click.echo(f"See {CONFIG_FILE.parent / 'config.json.example'} for template.", err=True)
        raise click.Abort()

    with open(CONFIG_FILE) as f:
        full_config = json.load(f)

    # Extract Asana-specific config
    config = full_config.get("asana", {})

    if not config.get("api_token"):
        click.echo("Error: asana.api_token not set in config file", err=True)
        raise click.Abort()

    if not config.get("project_ids"):
        click.echo("Error: asana.project_ids not set in config file", err=True)
        raise click.Abort()

    return config


def asana_request(method, endpoint, config, **kwargs):
    """Make an authenticated request to Asana API"""
    headers = {
        "Authorization": f"Bearer {config['api_token']}",
        "Accept": "application/json",
    }

    url = f"{ASANA_API_BASE}/{endpoint}"

    try:
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json().get("data")
    except requests.exceptions.HTTPError as e:
        click.echo(f"API Error: {e}", err=True)
        if e.response is not None:
            try:
                error_data = e.response.json()
                if "errors" in error_data:
                    for error in error_data["errors"]:
                        click.echo(f"  {error.get('message', 'Unknown error')}", err=True)
            except:
                pass
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@click.group()
def cli():
    """Asana CLI - Manage your personal tasks"""
    pass


@cli.command()
@click.option("--filter", type=click.Choice(["today", "week", "overdue", "all"]), default="all", help="Filter tasks by due date")
@click.option("--completed", is_flag=True, help="Show completed tasks")
@click.option("--show-subtasks", is_flag=True, help="Include subtasks in the list")
@click.argument("task_id", required=False)
def list(filter, completed, show_subtasks, task_id):
    """List your tasks or subtasks of a specific task"""
    config = load_config()

    # If task_id is provided, list only that task's subtasks
    if task_id:
        try:
            parent_task = asana_request("GET", f"tasks/{task_id}", config, params={"opt_fields": "name"})
            subtasks = asana_request("GET", f"tasks/{task_id}/subtasks", config,
                                   params={"opt_fields": "name,completed,due_on,notes,gid,permalink_url"})

            if not subtasks:
                click.echo(f"No subtasks found for '{parent_task['name']}'")
                return

            click.echo(f"Subtasks for '{parent_task['name']}':\n")
            for subtask in subtasks:
                status = "✓" if subtask.get("completed") else "○"
                due = subtask.get("due_on", "No due date")
                click.echo(f"  {status} [{subtask['gid']}] {subtask['name']}")
                click.echo(f"    Due: {due}")
                if subtask.get("notes"):
                    notes = subtask["notes"][:100]
                    if len(subtask["notes"]) > 100:
                        notes += "..."
                    click.echo(f"    Notes: {notes}")
                click.echo(f"    URL: {subtask.get('permalink_url', 'N/A')}")
                click.echo()
            return
        except Exception as e:
            click.echo(f"Error fetching subtasks: {e}", err=True)
            raise click.Abort()

    today = datetime.now().date()

    all_tasks = []
    sections_by_project = {}

    # Get sections and tasks from all configured projects
    for project_id in config["project_ids"]:
        # Get sections for this project
        sections = asana_request("GET", f"projects/{project_id}/sections", config, params={"opt_fields": "name,gid"})
        if sections:
            sections_by_project[project_id] = {s["gid"]: s["name"] for s in sections}

        # Get tasks with memberships
        params = {
            "opt_fields": "name,completed,due_on,notes,gid,permalink_url,memberships.section.name,memberships.section.gid"
        }

        tasks = asana_request("GET", f"projects/{project_id}/tasks", config, params=params)

        if tasks:
            all_tasks.extend(tasks)

    # If show_subtasks is enabled, fetch subtasks for each task
    task_subtasks = {}
    if show_subtasks:
        for task in all_tasks:
            try:
                subtasks = asana_request("GET", f"tasks/{task['gid']}/subtasks", config,
                                       params={"opt_fields": "name,completed,due_on,notes,gid,permalink_url"})
                if subtasks:
                    task_subtasks[task['gid']] = subtasks
            except Exception:
                # If we can't get subtasks for a task, just skip it
                pass

    # Filter tasks by completion status
    filtered_tasks = []
    for task in all_tasks:
        if task.get("completed", False) != completed:
            continue

        due_on = task.get("due_on")

        # Apply date filters for non-"all" modes
        if filter == "today":
            if due_on != today.isoformat():
                continue
        elif filter == "week":
            if not due_on:
                continue
            task_date = datetime.fromisoformat(due_on).date()
            if task_date > today + timedelta(days=7):
                continue
        elif filter == "overdue":
            if not due_on:
                continue
            task_date = datetime.fromisoformat(due_on).date()
            if task_date >= today:
                continue

        filtered_tasks.append(task)

    if not filtered_tasks:
        click.echo("No tasks found.")
        return

    # For "all" filter, group by sections if available, otherwise by time periods
    if filter == "all":
        # Helper function to display a task
        def display_task(task, indent="  "):
            status = "✓" if task.get("completed") else "○"
            due = task.get("due_on", "No due date")
            click.echo(f"{indent}{status} [{task['gid']}] {task['name']}")
            click.echo(f"{indent}  Due: {due}")
            if task.get("notes"):
                notes = task["notes"][:100]
                if len(task["notes"]) > 100:
                    notes += "..."
                click.echo(f"{indent}  Notes: {notes}")
            click.echo(f"{indent}  URL: {task.get('permalink_url', 'N/A')}")

            # Display subtasks if available
            if show_subtasks and task['gid'] in task_subtasks:
                for subtask in task_subtasks[task['gid']]:
                    subtask_status = "✓" if subtask.get("completed") else "○"
                    subtask_due = subtask.get("due_on", "No due date")
                    click.echo(f"{indent}    ↳ {subtask_status} [{subtask['gid']}] {subtask['name']}")
                    click.echo(f"{indent}      Due: {subtask_due}")
                    if subtask.get("notes"):
                        subtask_notes = subtask["notes"][:80]
                        if len(subtask["notes"]) > 80:
                            subtask_notes += "..."
                        click.echo(f"{indent}      Notes: {subtask_notes}")

            click.echo()

        # Check if we have sections to group by (only for our configured projects)
        # Group by sections only if tasks have sections in our configured projects
        tasks_by_section = {}
        tasks_no_section = []

        for task in filtered_tasks:
            # Get section from memberships, but only for our configured project_ids
            section_name = None
            memberships = task.get("memberships", [])
            for membership in memberships:
                # Only look at sections from our configured projects
                project = membership.get("project", {})
                if project.get("gid") in config["project_ids"]:
                    section = membership.get("section")
                    if section and section.get("name"):
                        section_name = section["name"]
                        break

            if section_name:
                if section_name not in tasks_by_section:
                    tasks_by_section[section_name] = []
                tasks_by_section[section_name].append(task)
            else:
                tasks_no_section.append(task)

        # Only use section grouping if we have actual sections
        has_sections = len(tasks_by_section) > 0

        if has_sections:
            # Display tasks grouped by section
            for section_name in sorted(tasks_by_section.keys()):
                tasks = tasks_by_section[section_name]
                click.echo(f"{section_name.upper()} ({len(tasks)}):\n")
                for task in tasks:
                    display_task(task)

            if tasks_no_section:
                click.echo(f"NO SECTION ({len(tasks_no_section)}):\n")
                for task in tasks_no_section:
                    display_task(task)

        else:
            # Fallback: Group by time periods if no sections
            overdue = []
            today_tasks = []
            this_week = []
            next_week = []
            later = []
            no_due_date = []

            for task in filtered_tasks:
                due_on = task.get("due_on")

                if not due_on:
                    no_due_date.append(task)
                else:
                    task_date = datetime.fromisoformat(due_on).date()
                    if task_date < today:
                        overdue.append(task)
                    elif task_date == today:
                        today_tasks.append(task)
                    elif task_date <= today + timedelta(days=7):
                        this_week.append(task)
                    elif task_date <= today + timedelta(days=14):
                        next_week.append(task)
                    else:
                        later.append(task)

            if overdue:
                click.echo(f"OVERDUE ({len(overdue)}):\n")
                for task in overdue:
                    display_task(task)

            if today_tasks:
                click.echo(f"TODAY ({len(today_tasks)}):\n")
                for task in today_tasks:
                    display_task(task)

            if this_week:
                click.echo(f"THIS WEEK ({len(this_week)}):\n")
                for task in this_week:
                    display_task(task)

            if next_week:
                click.echo(f"NEXT WEEK ({len(next_week)}):\n")
                for task in next_week:
                    display_task(task)

            if later:
                click.echo(f"LATER ({len(later)}):\n")
                for task in later:
                    display_task(task)

            if no_due_date:
                click.echo(f"NO DUE DATE ({len(no_due_date)}):\n")
                for task in no_due_date:
                    display_task(task)

    else:
        # For other filters, display with header
        if filter == "today":
            click.echo(f"Tasks due today ({today.strftime('%Y-%m-%d')}):\n")
        elif filter == "week":
            week_end = (today + timedelta(days=7)).isoformat()
            click.echo(f"Tasks due this week (through {week_end}):\n")
        elif filter == "overdue":
            click.echo("Overdue tasks:\n")

        for task in filtered_tasks:
            status = "✓" if task.get("completed") else "○"
            due = task.get("due_on", "No due date")
            click.echo(f"{status} [{task['gid']}] {task['name']}")
            click.echo(f"  Due: {due}")
            if task.get("notes"):
                notes = task["notes"][:100]
                if len(task["notes"]) > 100:
                    notes += "..."
                click.echo(f"  Notes: {notes}")
            click.echo(f"  URL: {task.get('permalink_url', 'N/A')}")

            # Display subtasks if available
            if show_subtasks and task['gid'] in task_subtasks:
                for subtask in task_subtasks[task['gid']]:
                    subtask_status = "✓" if subtask.get("completed") else "○"
                    subtask_due = subtask.get("due_on", "No due date")
                    click.echo(f"    ↳ {subtask_status} [{subtask['gid']}] {subtask['name']}")
                    click.echo(f"      Due: {subtask_due}")
                    if subtask.get("notes"):
                        subtask_notes = subtask["notes"][:80]
                        if len(subtask["notes"]) > 80:
                            subtask_notes += "..."
                        click.echo(f"      Notes: {subtask_notes}")

            click.echo()


@cli.command()
@click.argument("task_id")
def complete(task_id):
    """Mark a task as complete"""
    config = load_config()

    try:
        # Mark task as completed
        data = {"data": {"completed": True}}
        asana_request("PUT", f"tasks/{task_id}", config, json=data)

        # Get task name for confirmation
        task = asana_request("GET", f"tasks/{task_id}", config, params={"opt_fields": "name"})
        click.echo(f"✓ Completed: {task['name']}")
    except Exception as e:
        click.echo(f"Error completing task: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("task_id")
@click.argument("date")
def reschedule(task_id, date):
    """Change the due date of a task

    DATE can be:
      - YYYY-MM-DD format (e.g., 2025-11-10)
      - Relative: 'today', 'tomorrow', '+3d' (3 days from now), '+1w' (1 week from now)
    """
    config = load_config()

    # Parse date
    try:
        if date.lower() == "today":
            new_date = datetime.now().date()
        elif date.lower() == "tomorrow":
            new_date = (datetime.now() + timedelta(days=1)).date()
        elif date.startswith("+"):
            # Parse relative date like +3d or +1w
            num = int(date[1:-1])
            unit = date[-1].lower()
            if unit == "d":
                new_date = (datetime.now() + timedelta(days=num)).date()
            elif unit == "w":
                new_date = (datetime.now() + timedelta(weeks=num)).date()
            else:
                raise ValueError(f"Unknown unit: {unit}")
        else:
            # Parse as ISO date
            new_date = datetime.fromisoformat(date).date()

        # Update task
        data = {"data": {"due_on": new_date.isoformat()}}
        asana_request("PUT", f"tasks/{task_id}", config, json=data)

        # Get task name for confirmation
        task = asana_request("GET", f"tasks/{task_id}", config, params={"opt_fields": "name"})
        click.echo(f"✓ Rescheduled '{task['name']}' to {new_date.isoformat()}")
    except ValueError as e:
        click.echo(f"Error parsing date: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error rescheduling task: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("task_id")
@click.option("--notes", help="Update task notes/description")
@click.option("--append-notes", help="Append to existing notes")
def update(task_id, notes, append_notes):
    """Update a task's properties"""
    config = load_config()

    try:
        # Get current task data if we need to append
        if append_notes:
            task = asana_request("GET", f"tasks/{task_id}", config, params={"opt_fields": "name,notes"})
            existing_notes = task.get("notes", "")

            # Append the new notes
            if existing_notes:
                updated_notes = f"{existing_notes}\n{append_notes}"
            else:
                updated_notes = append_notes

            data = {"data": {"notes": updated_notes}}
        elif notes is not None:
            data = {"data": {"notes": notes}}
        else:
            click.echo("Error: Must specify either --notes or --append-notes", err=True)
            raise click.Abort()

        # Update task
        asana_request("PUT", f"tasks/{task_id}", config, json=data)

        # Get task name for confirmation
        task = asana_request("GET", f"tasks/{task_id}", config, params={"opt_fields": "name"})
        click.echo(f"✓ Updated: {task['name']}")
    except Exception as e:
        click.echo(f"Error updating task: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("task_name")
@click.option("--due", help="Due date (YYYY-MM-DD, 'today', 'tomorrow', '+3d', etc.)")
@click.option("--notes", help="Task notes/description")
@click.option("--project-index", type=int, help="Which project to add to (0-indexed)")
@click.option("--workspace", default="10497086658021", help="Workspace ID to add task to")
def add(task_name, due, notes, project_index, workspace):
    """Add a new task"""
    config = load_config()

    # Prepare task data
    task_data = {
        "name": task_name,
        "workspace": workspace
    }

    # Add project if specified
    if project_index is not None:
        if project_index >= len(config["project_ids"]):
            click.echo(f"Error: Invalid project index {project_index}. You have {len(config['project_ids'])} projects configured.", err=True)
            raise click.Abort()

        project_id = config["project_ids"][project_index]
        task_data["projects"] = [project_id]

    # Set assignee if configured
    if "assignee" in config:
        task_data["assignee"] = config["assignee"]

    if notes:
        task_data["notes"] = notes

    if due:
        # Parse due date (reuse logic from reschedule)
        try:
            if due.lower() == "today":
                due_date = datetime.now().date()
            elif due.lower() == "tomorrow":
                due_date = (datetime.now() + timedelta(days=1)).date()
            elif due.startswith("+"):
                num = int(due[1:-1])
                unit = due[-1].lower()
                if unit == "d":
                    due_date = (datetime.now() + timedelta(days=num)).date()
                elif unit == "w":
                    due_date = (datetime.now() + timedelta(weeks=num)).date()
                else:
                    raise ValueError(f"Unknown unit: {unit}")
            else:
                due_date = datetime.fromisoformat(due).date()

            task_data["due_on"] = due_date.isoformat()
        except ValueError as e:
            click.echo(f"Error parsing due date: {e}", err=True)
            raise click.Abort()

    # Create task
    try:
        data = {"data": task_data}
        task = asana_request("POST", "tasks", config, json=data)
        click.echo(f"✓ Created task: {task['name']}")
        click.echo(f"  ID: {task['gid']}")
        click.echo(f"  URL: {task.get('permalink_url', 'N/A')}")
    except Exception as e:
        click.echo(f"Error creating task: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("parent_task_id")
@click.argument("subtask_name")
@click.option("--due", help="Due date (YYYY-MM-DD, 'today', 'tomorrow', '+3d', etc.)")
@click.option("--notes", help="Subtask notes/description")
def add_subtask(parent_task_id, subtask_name, due, notes):
    """Add a subtask to an existing task"""
    config = load_config()

    # Get parent task to verify it exists and get workspace
    try:
        parent_task = asana_request("GET", f"tasks/{parent_task_id}", config, params={"opt_fields": "name,workspace.gid"})
    except Exception:
        click.echo(f"Error: Could not find parent task {parent_task_id}", err=True)
        raise click.Abort()

    # Prepare subtask data
    task_data = {
        "name": subtask_name,
        "parent": parent_task_id,
        "workspace": parent_task.get("workspace", {}).get("gid", "10497086658021")
    }

    # Set assignee if configured
    if "assignee" in config:
        task_data["assignee"] = config["assignee"]

    if notes:
        task_data["notes"] = notes

    if due:
        # Parse due date using same logic as add command
        try:
            if due.lower() == "today":
                due_date = datetime.now().date()
            elif due.lower() == "tomorrow":
                due_date = (datetime.now() + timedelta(days=1)).date()
            elif due.startswith("+"):
                num = int(due[1:-1])
                unit = due[-1].lower()
                if unit == "d":
                    due_date = (datetime.now() + timedelta(days=num)).date()
                elif unit == "w":
                    due_date = (datetime.now() + timedelta(weeks=num)).date()
                else:
                    raise ValueError(f"Unknown unit: {unit}")
            else:
                due_date = datetime.fromisoformat(due).date()

            task_data["due_on"] = due_date.isoformat()
        except ValueError as e:
            click.echo(f"Error parsing due date: {e}", err=True)
            raise click.Abort()

    # Create subtask
    try:
        data = {"data": task_data}
        subtask = asana_request("POST", "tasks", config, json=data)
        click.echo(f"✓ Created subtask under '{parent_task['name']}':")
        click.echo(f"  {subtask['name']}")
        click.echo(f"  ID: {subtask['gid']}")
        click.echo(f"  URL: {subtask.get('permalink_url', 'N/A')}")
    except Exception as e:
        click.echo(f"Error creating subtask: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()

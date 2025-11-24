#!/usr/bin/env python3
"""
Coda CLI - Read and search Coda docs from the command line
"""

import json
import re
import sys
import time
from pathlib import Path

import click
import requests


# Look for config file in the parent directory (pm-context/)
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR.parent.parent / "config.json"
CODA_API_BASE = "https://coda.io/apis/v1"


def load_config():
    """Load configuration from config file"""
    if not CONFIG_FILE.exists():
        click.echo(f"Error: Config file not found at {CONFIG_FILE}", err=True)
        click.echo("Please create the config file with your API tokens.", err=True)
        click.echo(f"See {CONFIG_FILE.parent / 'config.json.example'} for template.", err=True)
        raise click.Abort()

    with open(CONFIG_FILE) as f:
        full_config = json.load(f)

    # Extract Coda-specific config
    config = full_config.get("coda", {})

    if not config.get("api_token"):
        click.echo("Error: coda.api_token not set in config file", err=True)
        raise click.Abort()

    return config


def coda_request(method, endpoint, config, **kwargs):
    """Make an authenticated request to Coda API"""
    headers = {
        "Authorization": f"Bearer {config['api_token']}",
        "Accept": "application/json",
    }

    url = f"{CODA_API_BASE}/{endpoint}"

    try:
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        click.echo(f"API Error: {e}", err=True)
        if e.response is not None:
            try:
                error_data = e.response.json()
                if "message" in error_data:
                    click.echo(f"  {error_data['message']}", err=True)
            except:
                pass
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


def extract_doc_id(url_or_id):
    """Extract doc ID from a Coda URL or return the ID if already an ID"""
    # If it looks like a doc ID already (starts with underscore), strip the _d prefix
    if url_or_id.startswith("_d"):
        return url_or_id[2:]  # Remove the _d prefix

    # Try to extract from URL
    # Coda URLs look like: https://coda.io/d/Doc-Name_dABCDEFGHIJ
    match = re.search(r'_d([A-Za-z0-9_-]+)', url_or_id)
    if match:
        return match.group(1)  # Return just the ID part without _d prefix

    # If no underscore prefix, assume it's already a clean ID
    if re.match(r'^[A-Za-z0-9_-]+$', url_or_id):
        return url_or_id

    return url_or_id


def get_all_pages(doc_id, config):
    """Fetch all pages from a doc, handling pagination"""
    page_items = []
    next_page_token = None

    while True:
        params = {}
        if next_page_token:
            params["pageToken"] = next_page_token
        else:
            params["limit"] = 100  # Only use limit on first request

        pages = coda_request("GET", f"docs/{doc_id}/pages", config, params=params)
        page_items.extend(pages.get("items", []))

        next_page_token = pages.get("nextPageToken")
        if not next_page_token:
            break

    return page_items


@click.group()
def cli():
    """Coda CLI - Read and search Coda docs"""
    pass


@cli.command()
@click.option("--limit", type=int, default=20, help="Maximum number of docs to return")
@click.option("--query", help="Search query to filter docs")
def list(limit, query):
    """List your Coda docs"""
    config = load_config()

    params = {"limit": limit}
    if query:
        params["query"] = query

    result = coda_request("GET", "docs", config, params=params)

    docs = result.get("items", [])

    if not docs:
        click.echo("No docs found.")
        return

    click.echo(f"Found {len(docs)} doc(s):\n")

    for doc in docs:
        click.echo(f"Name: {doc['name']}")
        click.echo(f"ID: {doc['id']}")
        click.echo(f"URL: {doc.get('browserLink', 'N/A')}")
        if doc.get('folder'):
            click.echo(f"Folder: {doc['folder'].get('name', 'N/A')}")
        click.echo(f"Created: {doc.get('createdAt', 'N/A')}")
        click.echo(f"Updated: {doc.get('updatedAt', 'N/A')}")
        click.echo()


@cli.command()
@click.argument("doc_url_or_id")
def get_doc(doc_url_or_id):
    """Get information about a specific doc by URL or ID"""
    config = load_config()

    doc_id = extract_doc_id(doc_url_or_id)

    click.echo(f"Fetching doc: {doc_id}\n")

    doc = coda_request("GET", f"docs/{doc_id}", config)

    click.echo(f"Name: {doc['name']}")
    click.echo(f"ID: {doc['id']}")
    click.echo(f"URL: {doc.get('browserLink', 'N/A')}")
    click.echo(f"Owner: {doc.get('owner', 'N/A')}")
    if doc.get('folder'):
        click.echo(f"Folder: {doc['folder'].get('name', 'N/A')}")
    click.echo(f"Created: {doc.get('createdAt', 'N/A')}")
    click.echo(f"Updated: {doc.get('updatedAt', 'N/A')}")
    click.echo(f"Published: {doc.get('published', False)}")

    # Get pages (with pagination)
    click.echo("\n--- Pages ---")
    page_items = get_all_pages(doc_id, config)

    if page_items:
        for page in page_items:
            click.echo(f"  - {page['name']} (ID: {page['id']})")
    else:
        click.echo("  No pages found.")

    # Get tables
    click.echo("\n--- Tables ---")
    tables = coda_request("GET", f"docs/{doc_id}/tables", config)
    table_items = tables.get("items", [])

    if table_items:
        for table in table_items:
            click.echo(f"  - {table['name']} (ID: {table['id']})")
    else:
        click.echo("  No tables found.")


@cli.command()
@click.argument("doc_url_or_id")
@click.argument("page_id_or_name")
def get_page(doc_url_or_id, page_id_or_name):
    """Get content of a specific page in a doc"""
    config = load_config()

    doc_id = extract_doc_id(doc_url_or_id)

    # First, list all pages to find the right one
    page_items = get_all_pages(doc_id, config)

    # Try to find page by ID or name
    target_page = None
    for page in page_items:
        if page['id'] == page_id_or_name or page['name'].lower() == page_id_or_name.lower():
            target_page = page
            break

    if not target_page:
        click.echo(f"Error: Page '{page_id_or_name}' not found in doc", err=True)
        click.echo("\nAvailable pages:", err=True)
        for page in page_items:
            click.echo(f"  - {page['name']} (ID: {page['id']})", err=True)
        raise click.Abort()

    # Get page content
    page = coda_request("GET", f"docs/{doc_id}/pages/{target_page['id']}", config)

    click.echo(f"Page: {page['name']}")
    click.echo(f"ID: {page['id']}")
    click.echo(f"URL: {page.get('browserLink', 'N/A')}")
    click.echo(f"\nContent Type: {page.get('contentType', 'N/A')}")

    # Note: The Coda API doesn't return the actual page content directly
    # You would need to export the doc or use other endpoints to get rich content
    click.echo("\nNote: Use the browser link to view full page content.")
    click.echo("The Coda API provides metadata but not rendered page content.")


@cli.command()
@click.argument("doc_url_or_id")
@click.argument("table_id_or_name")
@click.option("--limit", type=int, default=20, help="Maximum number of rows to return")
def get_table(doc_url_or_id, table_id_or_name, limit):
    """Get rows from a specific table in a doc"""
    config = load_config()

    doc_id = extract_doc_id(doc_url_or_id)

    # First, list all tables to find the right one
    tables = coda_request("GET", f"docs/{doc_id}/tables", config)
    table_items = tables.get("items", [])

    # Try to find table by ID or name
    target_table = None
    for table in table_items:
        if table['id'] == table_id_or_name or table['name'].lower() == table_id_or_name.lower():
            target_table = table
            break

    if not target_table:
        click.echo(f"Error: Table '{table_id_or_name}' not found in doc", err=True)
        click.echo("\nAvailable tables:", err=True)
        for table in table_items:
            click.echo(f"  - {table['name']} (ID: {table['id']})", err=True)
        raise click.Abort()

    # Get table columns
    columns = coda_request("GET", f"docs/{doc_id}/tables/{target_table['id']}/columns", config)
    column_items = columns.get("items", [])

    click.echo(f"Table: {target_table['name']}")
    click.echo(f"ID: {target_table['id']}")
    click.echo(f"\nColumns:")
    for col in column_items:
        click.echo(f"  - {col['name']}")

    # Get table rows
    params = {"limit": limit}
    rows = coda_request("GET", f"docs/{doc_id}/tables/{target_table['id']}/rows", config, params=params)
    row_items = rows.get("items", [])

    click.echo(f"\nRows (showing {len(row_items)}):")
    for row in row_items:
        click.echo(f"\nRow ID: {row['id']}")
        values = row.get('values', {})
        for col_name, value in values.items():
            click.echo(f"  {col_name}: {value}")


@cli.command()
def whoami():
    """Show information about the authenticated user"""
    config = load_config()

    user = coda_request("GET", "whoami", config)

    click.echo(f"Name: {user.get('name', 'N/A')}")
    click.echo(f"Login ID: {user.get('loginId', 'N/A')}")
    click.echo(f"Type: {user.get('type', 'N/A')}")
    click.echo(f"Workspace: {user.get('workspace', {}).get('name', 'N/A')}")


@cli.command()
@click.argument("doc_url_or_id")
@click.argument("page_id_or_name")
@click.option("--format", "output_format", type=click.Choice(["markdown", "html"]), default="markdown", help="Output format")
def get_page_content(doc_url_or_id, page_id_or_name, output_format):
    """Export and display the content of a page

    This uses the Coda API's async export feature to retrieve page content
    in markdown or HTML format.
    """
    config = load_config()

    doc_id = extract_doc_id(doc_url_or_id)

    # First, find the page ID if a name was provided
    page_items = get_all_pages(doc_id, config)

    target_page = None
    for page in page_items:
        if page['id'] == page_id_or_name or page['name'].lower() == page_id_or_name.lower():
            target_page = page
            break

    if not target_page:
        click.echo(f"Error: Page '{page_id_or_name}' not found in doc", err=True)
        click.echo("\nAvailable pages:", err=True)
        for page in page_items:
            click.echo(f"  - {page['name']} (ID: {page['id']})", err=True)
        raise click.Abort()

    page_id = target_page['id']

    click.echo(f"Exporting page '{target_page['name']}' as {output_format}...\n")

    # Step 1: Initiate export
    export_request = coda_request(
        "POST",
        f"docs/{doc_id}/pages/{page_id}/export",
        config,
        json={"outputFormat": output_format}
    )

    request_id = export_request.get("id")
    status = export_request.get("status")
    download_link = export_request.get("downloadLink")

    if not request_id:
        click.echo("Error: Failed to initiate export", err=True)
        raise click.Abort()

    # Check if download link is already available (fast export)
    if download_link:
        # S3 pre-signed URL - don't add auth headers
        content_response = requests.get(download_link)
        content_response.raise_for_status()
        click.echo(content_response.text)
        return

    # Step 2: Poll for completion
    max_attempts = 60
    attempt = 0

    while attempt < max_attempts:
        try:
            status_response = coda_request(
                "GET",
                f"docs/{doc_id}/pages/{page_id}/export/{request_id}",
                config
            )
        except Exception as e:
            # If polling fails, wait a bit and try again
            if attempt < max_attempts - 1:
                attempt += 1
                time.sleep(0.5)
                continue
            else:
                raise

        status = status_response.get("status")

        if status == "complete":
            download_link = status_response.get("downloadLink")
            if not download_link:
                click.echo("Error: Export completed but no download link provided", err=True)
                raise click.Abort()

            # Step 3: Download the content (S3 pre-signed URL - no auth needed)
            content_response = requests.get(download_link)
            content_response.raise_for_status()

            click.echo(content_response.text)
            return

        elif status == "failed":
            error_msg = status_response.get("error", "Unknown error")
            click.echo(f"Error: Export failed - {error_msg}", err=True)
            raise click.Abort()

        # Still in progress
        attempt += 1
        time.sleep(0.5)  # Wait 0.5 seconds before polling again

    click.echo("Error: Export timed out", err=True)
    raise click.Abort()


@cli.command()
@click.argument("doc_url_or_id")
@click.argument("page_name")
@click.option("--content", help="Initial page content (use - to read from stdin)")
@click.option("--format", "content_format", type=click.Choice(["markdown", "html"]), default="markdown", help="Content format (default: markdown)")
@click.option("--subtitle", help="Page subtitle")
@click.option("--parent", help="Parent page ID or name")
def create_page(doc_url_or_id, page_name, content, content_format, subtitle, parent):
    """Create a new page in a doc

    Examples:
        ./coda create-page "ejBp5P1ahr" "My New Page"
        ./coda create-page "ejBp5P1ahr" "My New Page" --content "# Hello World"
        echo "# My Content" | ./coda create-page "ejBp5P1ahr" "My New Page" --content -
    """
    config = load_config()
    doc_id = extract_doc_id(doc_url_or_id)

    # Read content from stdin if - is specified
    if content == "-":
        content = sys.stdin.read()

    # Build the request payload
    payload = {
        "name": page_name
    }

    if subtitle:
        payload["subtitle"] = subtitle

    # If parent is specified, resolve it to a page ID
    if parent:
        page_items = get_all_pages(doc_id, config)

        parent_page = None
        for page in page_items:
            if page['id'] == parent or page['name'].lower() == parent.lower():
                parent_page = page
                break

        if not parent_page:
            click.echo(f"Error: Parent page '{parent}' not found in doc", err=True)
            raise click.Abort()

        payload["parentPageId"] = parent_page['id']

    # Add content if provided
    if content:
        payload["pageContent"] = {
            "type": "canvas",
            "canvasContent": {
                "format": content_format,
                "content": content
            }
        }

    click.echo(f"Creating page '{page_name}' in doc {doc_id}...")

    result = coda_request("POST", f"docs/{doc_id}/pages", config, json=payload)

    click.echo(f"\nPage created successfully!")
    click.echo(f"Name: {result.get('name', 'N/A')}")
    click.echo(f"ID: {result.get('id', 'N/A')}")
    click.echo(f"URL: {result.get('browserLink', 'N/A')}")


@cli.command()
@click.argument("doc_url_or_id")
@click.argument("page_id_or_name")
@click.option("--content", help="New page content (use - to read from stdin)")
@click.option("--format", "content_format", type=click.Choice(["markdown", "html"]), default="markdown", help="Content format (default: markdown)")
@click.option("--mode", type=click.Choice(["replace", "append"]), default="replace", help="Replace or append content (default: replace)")
@click.option("--name", "new_name", help="Update the page name")
@click.option("--subtitle", help="Update the page subtitle")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt")
def update_page(doc_url_or_id, page_id_or_name, content, content_format, mode, new_name, subtitle, yes):
    """Update an existing page in a doc

    Examples:
        ./coda update-page "ejBp5P1ahr" "My Page" --name "Renamed Page"
        ./coda update-page "ejBp5P1ahr" "My Page" --content "# New content"
        echo "More content" | ./coda update-page "ejBp5P1ahr" "My Page" --content - --mode append

    Note: This command will prompt for confirmation before making changes.
    Use --yes/-y to skip the confirmation prompt.
    """
    config = load_config()
    doc_id = extract_doc_id(doc_url_or_id)

    # Find the page
    page_items = get_all_pages(doc_id, config)

    target_page = None
    for page in page_items:
        if page['id'] == page_id_or_name or page['name'].lower() == page_id_or_name.lower():
            target_page = page
            break

    if not target_page:
        click.echo(f"Error: Page '{page_id_or_name}' not found in doc", err=True)
        click.echo("\nAvailable pages:", err=True)
        for page in page_items:
            click.echo(f"  - {page['name']} (ID: {page['id']})", err=True)
        raise click.Abort()

    page_id = target_page['id']

    # Read content from stdin if - is specified
    if content == "-":
        content = sys.stdin.read()

    # Build the request payload
    payload = {}

    if new_name:
        payload["name"] = new_name

    if subtitle is not None:  # Allow empty string to clear subtitle
        payload["subtitle"] = subtitle

    # Add content if provided
    if content:
        payload["contentUpdate"] = {
            "insertionMode": mode,
            "canvasContent": {
                "format": content_format,
                "content": content
            }
        }

    if not payload:
        click.echo("Error: No updates specified. Use --name, --subtitle, or --content", err=True)
        raise click.Abort()

    # Show what will be updated
    click.echo(f"\nAbout to update page '{target_page['name']}' in doc {doc_id}")
    click.echo(f"Page URL: {target_page.get('browserLink', 'N/A')}")
    click.echo("\nChanges:")
    if new_name:
        click.echo(f"  - Rename to: {new_name}")
    if subtitle is not None:
        click.echo(f"  - Update subtitle: {subtitle}")
    if content:
        action = "Append to" if mode == "append" else "Replace"
        preview = content[:100] + "..." if len(content) > 100 else content
        click.echo(f"  - {action} content ({len(content)} chars): {preview}")

    # Confirm before updating
    if not yes:
        if not click.confirm("\nDo you want to proceed with this update?"):
            click.echo("Update cancelled.")
            raise click.Abort()

    click.echo(f"\nUpdating page...")

    result = coda_request("PUT", f"docs/{doc_id}/pages/{page_id}", config, json=payload)

    click.echo(f"\nPage updated successfully!")
    click.echo(f"Name: {result.get('name', 'N/A')}")
    click.echo(f"ID: {result.get('id', 'N/A')}")
    click.echo(f"URL: {result.get('browserLink', 'N/A')}")


if __name__ == "__main__":
    cli()

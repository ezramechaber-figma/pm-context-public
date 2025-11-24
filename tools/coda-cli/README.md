# Coda CLI

A command-line tool to view, search, and manage your Coda docs and pages.

## Setup

1. Get your Coda API token:
   - Go to https://coda.io/account
   - Scroll down to "API Settings" section
   - Click "Generate API Token"
   - Copy the token

2. Create the unified config file (in the pm-context root directory):
```bash
cd /path/to/pm-context  # Navigate to the pm-context root directory
cp config.json.example config.json
```

3. Edit `config.json` and add your Coda API token under the `coda` key:
```json
{
  "asana": { ... },
  "coda": {
    "api_token": "YOUR_CODA_API_TOKEN"
  }
}
```

That's it! The `./coda` wrapper script will automatically create a virtual environment and install dependencies on first run.

## Understanding Coda URLs and IDs

Coda URLs have a specific structure that's important to understand:

```
https://coda.io/d/[DocName]_d[DocID]/[PageName]_su[PageShortCode]
```

For example: `https://coda.io/d/AI-Add-on-HQ_dejBp5P1ahr/M2-checkin_suW6dS7W`

### Doc IDs

The `_d` in the URL is a **two-character delimiter** that separates the doc name from the doc ID.

The CLI accepts doc identifiers in three formats:
1. **Full URL**: `https://coda.io/d/AI-Add-on-HQ_dejBp5P1ahr/...` (recommended - most foolproof)
2. **String after `/d/`**: `_dejBp5P1ahr` (includes the `_d` delimiter)
3. **Clean ID**: `ejBp5P1ahr` (just the ID part)

All three formats work - the CLI automatically extracts the correct ID.

### Page IDs - Important Warning

**Page short codes from URLs (like `_suW6dS7W`) will NOT work with the CLI.**

Coda URLs contain short codes (`_suXXXXXX`) that are different from the actual API page IDs (like `canvas-b3Bn4LrEuI`). There's no way to convert between them.

**Instead, use page names:**
```bash
# Good - use the page name from the doc
./coda get-page-content ejBp5P1ahr "M2 checkin: End User Experience"

# Bad - URL short codes won't work
./coda get-page-content ejBp5P1ahr suW6dS7W  # Will fail!
```

If you don't know the exact page name, run `./coda get-doc [doc_id]` first to see all available pages and their actual IDs.

## Usage

### List docs

```bash
# List all your docs (default limit: 20)
./coda list

# List with a specific limit
./coda list --limit 50

# Search for docs by query
./coda list --query "product"
```

### Get doc information

```bash
# By URL
./coda get-doc "https://coda.io/d/Doc-Name_dABCDEFGHIJ"

# By doc ID
./coda get-doc "_dABCDEFGHIJ"
```

This will show:
- Doc metadata (name, owner, created/updated dates)
- List of pages in the doc
- List of tables in the doc

### Get page content

```bash
# By page name (recommended - easiest approach)
./coda get-page-content "https://coda.io/d/Doc-Name_dABCDEFGHIJ" "Page Name"

# Can also use just the doc ID
./coda get-page-content "_dABCDEFGHIJ" "Page Name"

# Or by the actual page ID (not the URL short code!)
./coda get-page-content "ejBp5P1ahr" "canvas-XYZ"
```

Note: Use the `get-page-content` command to export page content as markdown or HTML. The older `get-page` command only retrieves metadata.

### Create a new page

```bash
# Create an empty page
./coda create-page "ejBp5P1ahr" "My New Page"

# Create a page with content
./coda create-page "ejBp5P1ahr" "My New Page" --content "# Hello World\n\nThis is my page content."

# Create a page with subtitle and parent
./coda create-page "ejBp5P1ahr" "Child Page" --subtitle "A subpage" --parent "Parent Page Name"

# Create a page from stdin
echo "# My Content" | ./coda create-page "ejBp5P1ahr" "My New Page" --content -

# Use HTML format instead of markdown
./coda create-page "ejBp5P1ahr" "My New Page" --content "<h1>Hello</h1>" --format html
```

### Update an existing page

```bash
# Update page name (will prompt for confirmation)
./coda update-page "ejBp5P1ahr" "My Page" --name "Renamed Page"

# Replace page content
./coda update-page "ejBp5P1ahr" "My Page" --content "# New content"

# Append to page content
./coda update-page "ejBp5P1ahr" "My Page" --content "\n## More content" --mode append

# Update from stdin
echo "Additional content" | ./coda update-page "ejBp5P1ahr" "My Page" --content - --mode append

# Update subtitle
./coda update-page "ejBp5P1ahr" "My Page" --subtitle "Updated subtitle"

# Use HTML format
./coda update-page "ejBp5P1ahr" "My Page" --content "<p>New content</p>" --format html

# Skip confirmation prompt (for scripts)
./coda update-page "ejBp5P1ahr" "My Page" --content "# New content" --yes
```

**Safety:** The `update-page` command requires confirmation before making changes. It will show you what's about to be modified and ask for approval. Use `--yes` or `-y` to skip the prompt (useful for automated scripts).

Note: HTML and markdown can't perfectly represent all Coda features, so round-trip conversions may lose some formatting.

### Get table data

```bash
# By table name
./coda get-table "https://coda.io/d/Doc-Name_dABCDEFGHIJ" "Tasks" --limit 20

# By table ID
./coda get-table "_dABCDEFGHIJ" "grid-ABC" --limit 50
```

This will show:
- Table columns
- Table rows with their values

### Check authentication

```bash
./coda whoami
```

Shows information about the authenticated user and workspace.

## Tips

- **Always prefer pasting full URLs** - it's the most foolproof method
- Doc IDs are extracted automatically from URLs (handles the `_d` delimiter)
- **Use page names, not URL short codes** - page short codes (`_suXXXXXX`) won't work
- Run `./coda get-doc [doc_id]` to see all available pages and tables in a doc
- Page and table names are case-insensitive when searching
- Use `--content -` to pipe content from stdin for create/update commands
- Round-trip conversions between Coda and markdown/HTML may lose some formatting
- Use `--help` with any command to see available options

## Examples

```bash
# Find all docs with "roadmap" in the name
./coda list --query "roadmap"

# Get detailed info about a specific doc (shows all pages and tables)
./coda get-doc "https://coda.io/d/Product-Roadmap_dXYZ123"

# Export page content as markdown using page name
./coda get-page-content "https://coda.io/d/AI-Add-on-HQ_dejBp5P1ahr" "M2 checkin"

# All these doc ID formats work:
./coda get-doc "https://coda.io/d/Product-Roadmap_dXYZ123"  # Full URL
./coda get-doc "_dXYZ123"                                   # With _d prefix
./coda get-doc "XYZ123"                                     # Clean ID

# View a specific table in a doc
./coda get-table "XYZ123" "Q1 Goals" --limit 10

# Create a new page with content
./coda create-page "XYZ123" "Meeting Notes" --content "# Meeting Notes\n\n## Attendees\n- Alice\n- Bob"

# Update page content (append mode)
./coda update-page "XYZ123" "Meeting Notes" --content "\n## Action Items\n- Follow up on proposal" --mode append
```

## Troubleshooting

If you get "Config file not found":
- Make sure you created `config.json` in the pm-context root directory
- Check that it has valid JSON with the `coda` section containing an `api_token` field

If you get "Unauthorized" errors:
- Check that your API token is valid and properly copied
- Make sure there are no extra spaces in the token
- Try generating a new API token from your Coda account settings

If doc/page/table not found:
- Verify you have access to the doc in Coda
- For doc IDs: Make sure you're using the correct format (see "Understanding Coda URLs and IDs" section above)
  - If extracting manually from a URL, use everything after `_d` including the `_d` prefix (e.g., `_dejBp5P1ahr`)
  - Or just paste the full URL - the CLI will handle it
- For pages: Use the page name, not the short code from the URL
  - Run `./coda get-doc [doc_id]` first to see available pages
  - Page short codes like `_suXXXXXX` from URLs won't work
- Try listing pages/tables first to see what's available

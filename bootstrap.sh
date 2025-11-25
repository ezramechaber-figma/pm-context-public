#!/bin/bash
# Bootstrap script for pm-context-public
# Sets up symlinks and verifies configuration

set -e

echo "🚀 PM Context Bootstrap"
echo "======================="
echo ""

# Check if config.json exists
if [ ! -f "config.json" ]; then
    echo "⚠️  config.json not found"
    echo "   Creating from config.json.example..."
    cp config.json.example config.json
    echo "   ✓ Created config.json"
    echo "   → Edit config.json to add your Asana and Coda API tokens"
    echo ""
fi

# Handle MCP config symlink
if [ -L ".mcp.json" ]; then
    echo "✓ .mcp.json symlink already exists"
    echo "  Points to: $(readlink .mcp.json)"
    echo ""
elif [ -f ".mcp.json" ]; then
    echo "⚠️  .mcp.json exists as a regular file (not a symlink)"
    echo "   Skipping MCP config setup"
    echo ""
else
    echo "Looking for MCP config at ~/figma/figma/.mcp.json..."

    if [ -f ~/figma/figma/.mcp.json ]; then
        ln -s ~/figma/figma/.mcp.json .mcp.json
        echo "✓ Created symlink to ~/figma/figma/.mcp.json"
        echo ""
    else
        echo "⚠️  ~/figma/figma/.mcp.json not found"
        echo "   MCPs are optional - the core CLIs will work without them"
        echo "   If you have MCPs elsewhere, manually create a symlink:"
        echo "   ln -s /path/to/your/.mcp.json .mcp.json"
        echo ""
    fi
fi

# Handle devex symlink to monorepo
if [ -L "devex" ]; then
    echo "✓ devex symlink already exists"
    echo "  Points to: $(readlink devex)"
    echo ""
elif [ -d "devex" ]; then
    echo "⚠️  devex exists as a regular directory (not a symlink)"
    echo "   Skipping devex setup"
    echo ""
else
    echo "Looking for Figma monorepo devex at ~/figma/figma/devex/mcp-support..."

    if [ -d ~/figma/figma/devex/mcp-support ]; then
        mkdir -p devex
        rmdir devex  # Remove the empty directory we just created
        ln -s ~/figma/figma/devex devex
        echo "✓ Created symlink to ~/figma/figma/devex"
        echo ""
    else
        echo "⚠️  ~/figma/figma/devex/mcp-support not found"
        echo "   Devex tools are optional - the core CLIs will work without them"
        echo ""
    fi
fi

# Check CLI tools
echo "Checking CLI tools..."
echo ""

if [ -d "tools/asana-cli" ]; then
    echo "✓ Asana CLI found at tools/asana-cli"
    if [ ! -x "tools/asana-cli/asana" ]; then
        chmod +x tools/asana-cli/asana
        echo "  → Made tools/asana-cli/asana executable"
    fi
else
    echo "⚠️  Asana CLI not found"
fi

if [ -d "tools/coda-cli" ]; then
    echo "✓ Coda CLI found at tools/coda-cli"
    if [ ! -x "tools/coda-cli/coda" ]; then
        chmod +x tools/coda-cli/coda
        echo "  → Made tools/coda-cli/coda executable"
    fi
else
    echo "⚠️  Coda CLI not found"
fi

echo ""
echo "✅ Bootstrap complete!"
echo ""
echo "Next steps:"
echo "1. Edit config.json to add your API tokens"
echo "2. Edit .claude/CLAUDE.md to personalize your context"
echo "3. Edit .claude/commands/get-context.md to update Coda doc ID"
echo "4. Test the CLIs:"
echo "   cd tools/asana-cli && ./asana list"
echo "   cd tools/coda-cli && ./coda whoami"
echo ""

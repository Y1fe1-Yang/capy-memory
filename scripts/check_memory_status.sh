#!/bin/bash
# Check Memory MCP installation status

CONFIG_FILE="/home/node/.claude.json"
MEMORY_FILE="/home/node/.claude/memory/global.jsonl"
NPX_MEMORY_FILE=$(find /home/node/.npm/_npx -path "*/server-memory/dist/memory.jsonl" 2>/dev/null | head -1)

echo "🔍 Checking Memory MCP status..."
echo ""

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Configuration file not found: $CONFIG_FILE"
    exit 1
fi

# Check if Memory MCP is configured
if ! jq -e '.mcpServers.memory' "$CONFIG_FILE" > /dev/null 2>&1; then
    echo "❌ Memory MCP not configured"
    echo ""
    echo "Run: scripts/install_memory_mcp.py"
    exit 1
fi

echo "✅ Memory MCP is configured"
echo ""

# Show configuration
echo "Configuration:"
jq '.mcpServers.memory' "$CONFIG_FILE"
echo ""

# Check configured memory file
if [ -f "$MEMORY_FILE" ]; then
    SIZE=$(du -h "$MEMORY_FILE" | cut -f1)
    LINES=$(wc -l < "$MEMORY_FILE")
    echo "📍 Configured memory file: $MEMORY_FILE"
    echo "   Size: $SIZE"
    echo "   Entries: $LINES"
    echo "   ✅ Using correct path"
else
    echo "⚠️  Configured memory file not found: $MEMORY_FILE"
    echo "   (Will be created on first write operation)"
fi

echo ""

# Check if npx cache memory file exists
if [ -n "$NPX_MEMORY_FILE" ] && [ -f "$NPX_MEMORY_FILE" ]; then
    SIZE=$(du -h "$NPX_MEMORY_FILE" | cut -f1)
    LINES=$(wc -l < "$NPX_MEMORY_FILE")
    echo "⚠️  Found npx cache memory file: $NPX_MEMORY_FILE"
    echo "   Size: $SIZE"
    echo "   Entries: $LINES"
    echo "   ❌ This means Memory MCP is using wrong path!"
    echo ""
    echo "   To fix: Restart Claude Code to apply new configuration"
fi

echo ""
echo "✅ Memory MCP configuration check complete"

#!/bin/bash
# Check Memory MCP installation status

CONFIG_FILE="/home/node/.claude.json"
MEMORY_FILE="/home/node/.claude/memory/global.jsonl"

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

# Check memory file
if [ -f "$MEMORY_FILE" ]; then
    SIZE=$(du -h "$MEMORY_FILE" | cut -f1)
    LINES=$(wc -l < "$MEMORY_FILE")
    echo "📍 Memory file exists: $MEMORY_FILE"
    echo "   Size: $SIZE"
    echo "   Entries: $LINES"
else
    echo "ℹ️  Memory file not yet created: $MEMORY_FILE"
    echo "   (Will be created on first write operation)"
fi

echo ""
echo "✅ Memory MCP is ready to use"

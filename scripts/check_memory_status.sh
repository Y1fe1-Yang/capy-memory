#!/bin/bash
# Check Memory MCP installation status and scan for memory files

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
echo "🔍 Scanning for other memory files..."
echo ""

FOUND_COUNT=0

# 1. Check npx cache
NPX_FILES=$(find /home/node/.npm/_npx -path "*/server-memory/dist/memory.jsonl" 2>/dev/null)
if [ -n "$NPX_FILES" ]; then
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            SIZE=$(du -h "$file" | cut -f1)
            LINES=$(wc -l < "$file" 2>/dev/null || echo "0")
            echo "⚠️  [npx cache] $file"
            echo "   Size: $SIZE, Entries: $LINES"
            echo "   ❌ Memory MCP may be using this instead of configured path!"
            echo ""
            FOUND_COUNT=$((FOUND_COUNT + 1))
        fi
    done <<< "$NPX_FILES"
fi

# 2. Check .claude directories (excluding configured file)
CLAUDE_FILES=$(find /home/node/.claude -name "*.jsonl" -path "*/memory/*" 2>/dev/null | grep -v "$MEMORY_FILE")
if [ -n "$CLAUDE_FILES" ]; then
    while IFS= read -r file; do
        if [ -f "$file" ] && [ "$file" != "$MEMORY_FILE" ]; then
            # Validate it's a memory file by checking content
            if grep -q '"type":"entity"' "$file" 2>/dev/null || grep -q '"type":"relation"' "$file" 2>/dev/null; then
                SIZE=$(du -h "$file" | cut -f1)
                LINES=$(wc -l < "$file" 2>/dev/null || echo "0")
                echo "ℹ️  [.claude directory] $file"
                echo "   Size: $SIZE, Entries: $LINES"
                echo ""
                FOUND_COUNT=$((FOUND_COUNT + 1))
            fi
        fi
    done <<< "$CLAUDE_FILES"
fi

# 3. Check common locations in home directory
for name in memory.jsonl memories.jsonl mcp-memory.jsonl; do
    file="/home/node/$name"
    if [ -f "$file" ]; then
        if grep -q '"type":"entity"' "$file" 2>/dev/null || grep -q '"type":"relation"' "$file" 2>/dev/null; then
            SIZE=$(du -h "$file" | cut -f1)
            LINES=$(wc -l < "$file" 2>/dev/null || echo "0")
            echo "ℹ️  [home directory] $file"
            echo "   Size: $SIZE, Entries: $LINES"
            echo ""
            FOUND_COUNT=$((FOUND_COUNT + 1))
        fi
    fi
done

# 4. Check /tmp directory
TMP_FILES=$(find /tmp -name "memory*.jsonl" -type f 2>/dev/null)
if [ -n "$TMP_FILES" ]; then
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            if grep -q '"type":"entity"' "$file" 2>/dev/null || grep -q '"type":"relation"' "$file" 2>/dev/null; then
                SIZE=$(du -h "$file" | cut -f1)
                LINES=$(wc -l < "$file" 2>/dev/null || echo "0")
                echo "ℹ️  [tmp directory] $file"
                echo "   Size: $SIZE, Entries: $LINES"
                echo ""
                FOUND_COUNT=$((FOUND_COUNT + 1))
            fi
        fi
    done <<< "$TMP_FILES"
fi

# Summary
if [ $FOUND_COUNT -eq 0 ]; then
    echo "✅ No other memory files found"
elif [ $FOUND_COUNT -eq 1 ]; then
    echo "⚠️  Found 1 other memory file"
    echo ""
    echo "💡 To migrate all memory files to the configured path:"
    echo "   scripts/migrate_memory_data.py"
else
    echo "⚠️  Found $FOUND_COUNT other memory files"
    echo ""
    echo "💡 To migrate all memory files to the configured path:"
    echo "   scripts/migrate_memory_data.py"
fi

echo ""

# Final status
if [ $FOUND_COUNT -gt 0 ] && [ ! -f "$MEMORY_FILE" ]; then
    echo "⚠️  Status: Memory data exists but not in configured location"
    echo "   Action required: Run migration script and restart Claude Code"
elif [ $FOUND_COUNT -gt 0 ]; then
    echo "⚠️  Status: Memory data scattered across multiple locations"
    echo "   Recommended: Run migration script to consolidate data"
else
    echo "✅ Status: Memory configuration is healthy"
fi

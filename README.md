# capy-memory

Memory management skill for HappyCapy environment using Memory MCP.

## Overview

capy-memory enables Claude to remember your preferences, habits, and context across conversations through the Memory MCP (Model Context Protocol) server. It provides intelligent memory management with automatic learning, historical conversation import, and privacy-aware storage.

## Features

- **Automatic Installation**: One-time setup with user consent
- **Intelligent Memory**: Learns from conversations automatically
- **Historical Import**: Import preferences from past conversations
- **Privacy-First**: Automatic filtering of sensitive information
- **Global Storage**: Memories persist across all conversations
- **Proactive Learning**: Claude determines when to remember without explicit commands

## Installation

### Method 1: Through Claude (Recommended)

Simply invoke the skill when needed:

```
"Use capy-memory to remember my preferences"
"Help me set up memory"
```

Claude will guide you through installation if Memory MCP isn't configured yet.

### Method 2: Manual Installation

Run the installation script:

```bash
scripts/install_memory_mcp.py
```

Verify installation:

```bash
scripts/check_memory_status.sh
```

## Usage

### Automatic Learning

Claude learns automatically from your conversations:

- **Preferences**: "I prefer TypeScript over JavaScript"
- **Workflows**: "I always use pnpm for package management"
- **Background**: "I'm a senior frontend engineer"
- **Patterns**: Repeated choices and behaviors

### Explicit Memory Commands

You can also explicitly manage memory:

```
"Remember that I work in UTC+8"
"What do you remember about my coding style?"
"Update: I now use Bun instead of pnpm"
"Forget about my old JavaScript preference"
```

### Historical Import

On first use, you can import from previous conversations:

```
"Import my conversation history into memory"
```

Options:
- Last 7 days (quick)
- Last 30 days (recommended)
- All history (comprehensive)
- Custom selection

## Memory Storage

- **Location**: `/home/node/.claude/memory/global.jsonl`
- **Format**: JSONL (JSON Lines) with knowledge graph structure
- **Scope**: Global across all conversations
- **Program**: Managed by npx (`@modelcontextprotocol/server-memory`)

## What Gets Remembered

✅ **Good for Memory:**
- Language and framework preferences
- Tool and workflow preferences
- Code style and naming conventions
- Background and experience level
- Development practices
- Architecture decisions

❌ **Not Stored:**
- Temporary tasks or current bugs
- Sensitive information (passwords, API keys, emails)
- Rapidly changing details (line numbers, file paths)
- One-time problems

## Privacy

capy-memory automatically filters:
- Email addresses
- Passwords and API keys
- Credit card numbers
- Phone numbers
- Other personally identifiable information (PII)

## Advanced Usage

### View Memory Status

```bash
scripts/check_memory_status.sh
```

### Migrate Memory Data

If Memory MCP was using npx cache directory instead of the configured global path:

```bash
scripts/migrate_memory_data.py
```

This will copy data from npx cache to `/home/node/.claude/memory/global.jsonl` and warn you to restart Claude Code.

### Manual Backup

```bash
cp /home/node/.claude/memory/global.jsonl \
   ~/.claude/memory/backup-$(date +%Y%m%d).jsonl
```

### Query Memory Directly

```
"Show everything you remember about me"
"Search memory for TypeScript"
"How many things do you remember?"
```

## Technical Details

### Memory MCP Configuration

Located in `/home/node/.claude.json`:

```json
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {
        "MEMORY_FILE_PATH": "/home/node/.claude/memory/global.jsonl"
      }
    }
  }
}
```

### Available Tools

- `create_entities` - Create new memory entities
- `add_observations` - Add observations to existing entities
- `create_relations` - Create relationships between entities
- `read_graph` - Read complete memory graph
- `search_nodes` - Search for specific content
- `open_nodes` - Open specific entity by name
- `delete_observations` - Remove specific observations
- `delete_entities` - Remove entire entities

## Philosophy

capy-memory implements a "smart brain" approach:

1. **Proactive**: Claude decides when to remember without explicit commands
2. **Contextual**: Uses conversation context to determine what's worth remembering
3. **Privacy-aware**: Automatically filters sensitive information
4. **User-controlled**: Users can review, update, and delete memories
5. **Persistent**: Memories persist across conversations and sessions

## Troubleshooting

### Memory Not Persisting

Check configuration:
```bash
scripts/check_memory_status.sh
```

Verify file permissions:
```bash
ls -la /home/node/.claude/memory/global.jsonl
```

### Memory File Not Found

Memory file is created automatically on first write. If missing:
```bash
mkdir -p /home/node/.claude/memory
```

### Historical Import Issues

See detailed guide: `references/import-guide.md`

## References

- `references/memory-best-practices.md` - Usage guidelines
- `references/import-guide.md` - Historical import details
- `references/memory-management.md` - Advanced operations

## License

MIT License

## Contributing

This skill is part of the HappyCapy environment. For issues or suggestions, please contact support.

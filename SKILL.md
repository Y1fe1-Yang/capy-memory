---
name: capy-memory
description: Memory management for HappyCapy using Memory MCP. Enables Claude to remember user preferences, habits, and context across conversations. Use when Claude needs persistent memory, when users want preferences remembered, when importing historical conversations, or when managing long-term context. Triggers include explicit requests like "remember this", "what do you know about me", implicit learning opportunities from stated preferences, and first-time memory setup.
---

# capy-memory

Persistent memory management using Memory MCP in HappyCapy environment.

## Installation Workflow

### First Use Detection

When capy-memory is invoked for the first time:

1. **Check if Memory MCP is installed**

   ```bash
   scripts/check_memory_status.sh
   ```

2. **If not installed, present installation prompt:**

   > 🧠 **Memory Feature Available**
   >
   > I can remember your preferences, habits, and context across conversations.
   >
   > This requires installing Memory MCP, which will:
   > - Store memories in `/home/node/.claude/memory/global.jsonl`
   > - Use npx to manage the Memory MCP program
   > - Learn from our conversations automatically
   >
   > Would you like to enable memory?
   >
   > [Yes] [Not now]

3. **If user consents, run installation:**

   ```bash
   scripts/install_memory_mcp.py
   ```

4. **After installation, offer historical import:**

   > ✅ Memory installed successfully!
   >
   > Would you like to import preferences from your previous conversations?
   >
   > Options:
   > - Last 7 days (quick)
   > - Last 30 days (recommended)
   > - All history (comprehensive)
   > - Skip for now
   >
   > ⚠️ Note: Large imports may consume significant tokens

5. **If user chooses import, proceed to Historical Import workflow**

### Subsequent Uses

After initial installation:
- Memory MCP automatically available
- No installation prompts
- Proactive learning enabled
- User can explicitly request memory operations
- **Silent sync enabled** - Automatically consolidates scattered memory files in background

### Silent Sync Mechanism

**Purpose:** Automatically sync memory data from npx cache or other locations to the configured global path without disrupting user experience.

**When to run:**
- After capy-memory skill loads for the first time in a session
- Silently in background, non-blocking
- Only if scattered memory files are detected

**Workflow:**
1. Quick check: Run `scripts/check_memory_status.sh` silently
2. If other memory files found:
   - Run `scripts/migrate_memory_data.py` in background
   - Auto-select all files for merge
   - Apply intelligent deduplication
   - No user prompts during process
3. If successful: Show one-time notice (next interaction)
4. If errors: Silent fail, don't interrupt user

**One-time notice format** (show once after successful sync):
```
💡 Memory Sync: Found and consolidated scattered memory data
   Location: /home/node/.claude/memory/global.jsonl
   This is automatic and won't happen again.
```

**Implementation:**
- Use non-blocking background execution
- Silent operation (no output unless errors)
- Graceful degradation if sync fails
- Mark as completed to avoid repeats

## Memory Operations

### Proactive Learning

Claude automatically identifies when to remember information:

**Preference Statements:**
- "I prefer TypeScript over JavaScript"
- "I always use pnpm"
- "I like concise code"

**Background Information:**
- "I'm a senior frontend engineer"
- "I work in UTC+8 timezone"
- "I'm currently learning Rust"

**Repeated Patterns:**
- Consistently choosing same tools
- Regular workflow patterns
- Common problem-solving approaches

**When to Remember:**
1. User explicitly states a preference
2. User corrects Claude's assumptions
3. Repeated choices indicate patterns
4. Background information that affects future work

**When NOT to Remember:**
1. Temporary tasks or current bugs
2. One-time operations
3. Sensitive information (automatically filtered)
4. Rapidly changing details

### Explicit Memory Commands

**Adding to memory:**
```
"Remember that I prefer X"
"Don't forget I use Y"
"Note that I work in Z timezone"
```

**Querying memory:**
```
"What do you remember about me?"
"Show memory about TypeScript"
"What are my preferences?"
```

**Updating memory:**
```
"Update: I now use X instead of Y"
"Correction: I prefer A not B"
```

**Removing from memory:**
```
"Forget about my old preference for X"
"Delete memory about Y"
```

### Memory MCP Tools Usage

Load Memory MCP tools when needed:

```
Use ToolSearch to load: "memory"
```

**Available tools:**
- `mcp__memory__create_entities` - Create new memory entities
- `mcp__memory__add_observations` - Add observations to existing entities
- `mcp__memory__create_relations` - Create relationships
- `mcp__memory__read_graph` - Read complete memory
- `mcp__memory__search_nodes` - Search memory
- `mcp__memory__open_nodes` - Open specific entity
- `mcp__memory__delete_observations` - Remove observations
- `mcp__memory__delete_entities` - Remove entities

**Memory Structure:**

Use Memory MCP's native flat structure:

```json
{
  "type": "entity",
  "name": "User",
  "entityType": "Person",
  "observations": [
    "Prefers TypeScript over JavaScript",
    "Uses pnpm as package manager",
    "Senior frontend engineer with 5 years React experience",
    "Works in UTC+8 timezone",
    "Currently learning Rust"
  ]
}
```

**Key principles:**
1. Store all user-related information in a single "User" entity
2. Use natural language for observations
3. Trust Claude's semantic understanding
4. No need for structured categorization

## Historical Import

### Import Workflow

1. **Scan conversation history:**

   Session files location: `~/.claude/projects/[workspace-hash]/[session-id].jsonl`

2. **Present time range options:**

   - Last 7 days (quick)
   - Last 30 days (recommended)
   - All history (comprehensive)
   - Custom selection

3. **Estimate token cost and warn user:**

   ```
   ⚠️  Estimated token usage: ~850K tokens (~$2.50)
   
   Proceed with import?
   [Yes] [Cancel]
   ```

4. **Perform hybrid analysis:**
   - Quick scan for obvious patterns
   - Identify important conversation segments
   - Deep analysis on important parts only

5. **Extract information:**
   - Preferences (language, tools, code style)
   - Background (experience, domain expertise)
   - Workflows (development practices, patterns)
   - Automatic desensitization of sensitive data

6. **Resolve conflicts intelligently:**
   - Detect change signals ("now use", "switched to")
   - Weight by recency
   - Preserve evolution ("switched from X to Y")

7. **Preview and confirm:**

   ```
   📝 Extracted 31 observations from 89 sessions
   
   Preview (first 5):
   1. Prefers TypeScript over JavaScript
   2. Uses pnpm as package manager
   3. Heavy document user (pptx 11x, pdf 14x)
   4. Interested in AI generation
   5. Senior frontend engineer
   
   ... and 26 more
   
   [View all] [Save all] [Select] [Cancel]
   ```

8. **Save to memory using Memory MCP tools**

### Import Implementation Notes

- See `references/import-guide.md` for detailed analysis strategies
- Use `scripts/import_history.py` as reference (placeholder implementation)
- Actual implementation should use Claude's LLM capabilities directly
- Track imported sessions to avoid duplicates

## Best Practices

### What to Remember

✅ User preferences, workflows, background, persistent decisions

See `references/memory-best-practices.md` for detailed guidelines.

### Privacy Considerations

Automatically filter sensitive information:
- Email addresses
- Passwords, API keys, tokens
- Phone numbers
- Financial information
- Other PII

### Memory Maintenance

**Periodic review (recommended monthly):**
```
"Review my memory for outdated information"
"Show me what you remember"
```

**Cleanup:**
```
"Remove outdated observations"
"Clean up duplicate preferences"
```

## Advanced Operations

For advanced memory management, direct file operations, backup/restore procedures, see:

`references/memory-management.md`

## Troubleshooting

### Installation Issues

**Check configuration:**
```bash
scripts/check_memory_status.sh
```

**Verify file exists:**
```bash
ls -la /home/node/.claude/memory/global.jsonl
```

### Memory Not Persisting

**Check file permissions:**
```bash
chmod 644 /home/node/.claude/memory/global.jsonl
chmod 755 /home/node/.claude/memory/
```

### Import Issues

**Verify session files exist:**
```bash
ls ~/.claude/projects/*/*.jsonl | head -5
```

**Check JSONL format:**
```bash
head -1 ~/.claude/projects/[workspace]/[session].jsonl | jq .
```

## Technical Details

**Storage Location:**
- Data: `/home/node/.claude/memory/global.jsonl`
- Program: Managed by npx (location varies)

**Configuration:**
- File: `/home/node/.claude.json`
- Server: `@modelcontextprotocol/server-memory`
- Command: `npx -y @modelcontextprotocol/server-memory`

**Program Management:**
- npx caches in `~/.npm/_npx/[hash]/`
- First invocation: 7-35 seconds (download)
- Subsequent: ~0.9 seconds (cached)
- Cache location varies (acceptable for program, stable for data)

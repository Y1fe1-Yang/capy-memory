# Memory Storage Troubleshooting Guide

## Problem: Memory MCP Uses npx Cache Instead of Configured Path

### Symptoms

- Memory data is stored in `/home/node/.npm/_npx/[hash]/.../memory.jsonl`
- Configured path `/home/node/.claude/memory/global.jsonl` remains empty
- Memory persists across sessions despite "wrong" location

### Root Cause

Memory MCP server reads environment variables **once on startup** and caches the file path:

1. When Claude Code first starts, it spawns Memory MCP server via npx
2. Memory MCP reads `MEMORY_FILE_PATH` from environment
3. If variable is unset/empty, Memory MCP defaults to its own directory: `dist/memory.jsonl`
4. This path is cached for the server's lifetime
5. Server continues using npx cache location until process is restarted

**Technical detail**: The Memory MCP server is a long-running process. Once spawned, it doesn't re-read environment variables. Configuration changes in `.claude.json` only take effect after Claude Code restart.

### Why This Happens

**Scenario 1: Fresh Installation**
- User installs capy-memory skill
- Skill adds Memory MCP configuration to `.claude.json`
- But Memory MCP server is already running (spawned earlier)
- Server continues using old/default path

**Scenario 2: Configuration Update**
- User updates `MEMORY_FILE_PATH` in `.claude.json`
- Memory MCP server is already running
- Server doesn't see the new configuration

### Verification

Check both locations:

```bash
scripts/check_memory_status.sh
```

Expected output if problem exists:

```
✅ Memory MCP is configured

Configuration:
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-memory"],
  "env": {
    "MEMORY_FILE_PATH": "/home/node/.claude/memory/global.jsonl"
  }
}

⚠️  Configured memory file not found: /home/node/.claude/memory/global.jsonl
   (Will be created on first write operation)

⚠️  Found npx cache memory file: /home/node/.npm/_npx/abc123.../memory.jsonl
   Size: 2.4K
   Entries: 15
   ❌ This means Memory MCP is using wrong path!
   
   To fix: Restart Claude Code to apply new configuration
```

### Solution

#### Option 1: Restart Claude Code (Recommended)

The cleanest solution:

1. **Exit Claude Code completely**
   - Close all Claude Code windows/sessions
   - Ensure Claude Code process is terminated

2. **Restart Claude Code**
   - Memory MCP server will respawn with new configuration
   - Will use configured path: `/home/node/.claude/memory/global.jsonl`

3. **Verify:**
   ```bash
   scripts/check_memory_status.sh
   ```

**Important**: A simple session restart is NOT enough. You must fully exit and restart Claude Code to kill the Memory MCP server process.

#### Option 2: Migrate Existing Data

If you have important memory data in npx cache and want to preserve it:

1. **Run migration script:**
   ```bash
   scripts/migrate_memory_data.py
   ```

2. **What it does:**
   - Finds memory data in npx cache
   - Copies to `/home/node/.claude/memory/global.jsonl`
   - Creates backup if target file exists
   - Intelligently merges if both locations have data
   - Removes duplicate observations (fuzzy matching at 85% similarity)

3. **Restart Claude Code** (required for changes to take effect)

4. **Verify:**
   ```bash
   scripts/check_memory_status.sh
   ```

### Data Merge Scenarios

#### Scenario A: Only npx cache has data

**Before:**
- npx cache: 15 entries
- global: 0 entries

**After migration:**
- npx cache: 15 entries (unchanged)
- global: 15 entries (copied)

**Strategy**: Direct copy

#### Scenario B: Both locations have data

**Before:**
- npx cache: 12 entries
- global: 8 entries

**After migration:**
- npx cache: 12 entries (unchanged)
- global: 18 entries (merged, 2 duplicates removed)

**Strategy**: Intelligent merge with deduplication

**Merge algorithm:**
1. Entities merged by name
2. Observations deduplicated:
   - Exact duplicates removed
   - Similar observations removed (85% similarity threshold using SequenceMatcher)
3. Relations deduplicated by (from, to, relationType) tuple
4. Original global file backed up with timestamp

#### Scenario C: Only global has data

**Before:**
- npx cache: 0 entries
- global: 20 entries

**After migration:**
- No changes needed
- Migration script reports: "No memory data found in npx cache"

### Prevention

To avoid this issue in future:

1. **Always restart Claude Code after configuration changes**
   - After installing capy-memory skill
   - After modifying `.claude.json`
   - After updating `MEMORY_FILE_PATH`

2. **Check configuration immediately after installation**
   ```bash
   scripts/check_memory_status.sh
   ```

3. **If check shows wrong path, restart Claude Code before using memory features**

### FAQ

**Q: Will I lose my memory data if I restart Claude Code?**

A: No. Memory data is persisted to disk (JSONL file). Restarting only reloads the server process.

**Q: Can I manually copy the file instead of using migration script?**

A: Yes, but migration script is safer:
```bash
cp /home/node/.npm/_npx/[hash]/.../memory.jsonl \
   /home/node/.claude/memory/global.jsonl
```
However, the migration script provides:
- Automatic path detection
- Intelligent merging if target exists
- Automatic backup
- Verification

**Q: What happens to the npx cache memory file after migration?**

A: It remains unchanged. After Claude Code restart, Memory MCP will stop using it and switch to the global path. The old file can be safely deleted:
```bash
find /home/node/.npm/_npx -path "*/server-memory/dist/memory.jsonl" -delete
```

**Q: Why not just use npx cache location?**

A: npx cache directory:
- Has unpredictable hash-based paths
- Can be cleared by npm commands
- Makes manual backup/restore difficult
- Not intended for user data storage

Global path (`~/.claude/memory/global.jsonl`):
- Stable, predictable location
- Easy to backup/restore
- Survives npx cache clears
- Follows XDG conventions

**Q: How do I verify Memory MCP is using the correct path?**

A: After restart, create a test memory:
```
You: Remember that I tested memory storage on [date]
```

Then check:
```bash
cat /home/node/.claude/memory/global.jsonl | grep "tested memory storage"
```

If found, Memory MCP is using correct path.

**Q: Can I change the global path to a different location?**

A: Yes, edit `.claude.json`:
```json
{
  "mcpServers": {
    "memory": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {
        "MEMORY_FILE_PATH": "/your/custom/path/memory.jsonl"
      }
    }
  }
}
```

Then:
1. Migrate existing data to new location
2. Restart Claude Code
3. Verify with check_memory_status.sh

### Technical Details

**Memory MCP Process Lifecycle:**

1. Claude Code starts → spawns Memory MCP via npx
2. Memory MCP reads environment:
   ```javascript
   const memoryPath = process.env.MEMORY_FILE_PATH || './dist/memory.jsonl'
   ```
3. Path is cached in memory
4. All operations use cached path
5. Process continues until Claude Code exits
6. On restart, new process reads fresh environment

**Why environment variables aren't re-read:**

- Memory MCP is a Node.js process
- `process.env` is read-only snapshot at startup
- Changing parent process environment doesn't affect child
- Only way to apply new config: restart the process

**npx caching:**

- First invocation: Downloads to `~/.npm/_npx/[hash]/`
- Hash based on: package name, version, registry
- Subsequent invocations: Use cached version
- Cache location is implementation detail
- Cache can be cleared: `npx clear-npx-cache`

**JSONL format:**

- One JSON object per line
- Easy to append (no need to parse entire file)
- Human-readable
- Git-friendly (line-by-line diffs)

Example:
```jsonl
{"type":"entity","name":"User","entityType":"Person","observations":["Prefers TypeScript"]}
{"type":"relation","from":"User","to":"TypeScript","relationType":"prefers"}
```

# Memory Management

Advanced operations for managing capy-memory.

## Memory File Structure

```
/home/node/.claude/memory/
├── global.jsonl              # Main memory storage
├── imported_sessions.txt     # Tracking imported sessions
└── backups/                  # Manual backups (if created)
    ├── 20260226-pre-import.jsonl
    └── 20260225-daily.jsonl
```

## Direct File Operations

### Viewing Memory

**Read entire file:**
```bash
cat /home/node/.claude/memory/global.jsonl | jq .
```

**Count entries:**
```bash
wc -l /home/node/.claude/memory/global.jsonl
```

**Search for specific content:**
```bash
cat /home/node/.claude/memory/global.jsonl | jq 'select(.name=="User") | .observations[]' | grep -i "typescript"
```

### Backup and Restore

**Create backup:**
```bash
cp /home/node/.claude/memory/global.jsonl \
   ~/.claude/memory/backup-$(date +%Y%m%d-%H%M%S).jsonl
```

**Restore from backup:**
```bash
cp ~/.claude/memory/backup-20260226-120000.jsonl \
   /home/node/.claude/memory/global.jsonl
```

**Automated backup (add to cron):**
```bash
# Daily backup at midnight
0 0 * * * cp /home/node/.claude/memory/global.jsonl /home/node/.claude/memory/backups/daily-$(date +\%Y\%m\%d).jsonl
```

### Manual Editing

**Edit with care:**
```bash
nano /home/node/.claude/memory/global.jsonl
```

**Validate after editing:**
```bash
cat /home/node/.claude/memory/global.jsonl | jq . > /dev/null && echo "✅ Valid" || echo "❌ Invalid JSON"
```

## Using Memory MCP Tools

### Available Tools

```
create_entities      - Create new entities
add_observations     - Add observations to existing entity
create_relations     - Create relationships between entities
delete_observations  - Remove specific observations
delete_entities      - Remove entire entities
read_graph           - Read complete memory graph
search_nodes         - Search for specific content
open_nodes           - Open specific entity by name
```

### Example Operations

**Add observation to User:**
```
Use create_entities or add_observations tool:
{
  "entities": [{
    "name": "User",
    "entityType": "Person",
    "observations": ["New preference here"]
  }]
}
```

**Search memory:**
```
Use search_nodes tool:
{
  "query": "TypeScript"
}
```

**Read all memory:**
```
Use read_graph tool (no parameters)
```

## Memory Lifecycle

### Memory Creation

**First write triggers file creation:**
1. Memory MCP configured
2. User provides first information to remember
3. `create_entities` called
4. `global.jsonl` file created
5. First entity saved

### Memory Growth

**Observations accumulate over time:**
- New preferences added
- Patterns identified
- Corrections made
- Knowledge expands

**Monitor size:**
```bash
du -h /home/node/.claude/memory/global.jsonl
```

### Memory Maintenance

**Periodic review (recommended monthly):**
1. Query full memory
2. Identify outdated information
3. Update changed preferences
4. Remove obsolete observations

**Cleanup old information:**
```
"Review my memory for outdated info"
"Remove any observations older than 6 months"
"Clean up duplicate preferences"
```

## Advanced Patterns

### Multiple Entities

Create separate entities for organization:

```json
{
  "type": "entity",
  "name": "User",
  "entityType": "Person",
  "observations": ["Personal preferences..."]
}
```

```json
{
  "type": "entity",
  "name": "Current Project",
  "entityType": "Project",
  "observations": ["Project-specific info..."]
}
```

### Relations for Context

Connect entities with relations:

```json
{
  "type": "relation",
  "from": "User",
  "to": "React",
  "relationType": "expert_in"
}
```

```json
{
  "type": "relation",
  "from": "Current Project",
  "to": "TypeScript",
  "relationType": "uses"
}
```

### Temporal Information

Include time context when relevant:

```
"Switched to pnpm in January 2026"
"Learning Rust since February 2026"
"Used JavaScript before 2025"
```

## Troubleshooting

### Memory Not Persisting

**Check file permissions:**
```bash
ls -la /home/node/.claude/memory/global.jsonl
chmod 644 /home/node/.claude/memory/global.jsonl
```

**Check directory permissions:**
```bash
ls -la /home/node/.claude/memory/
chmod 755 /home/node/.claude/memory/
```

### Memory Corruption

**Symptoms:**
- JSON parse errors
- MCP fails to load
- Operations fail silently

**Recovery:**
1. Check JSON validity:
   ```bash
   jq . /home/node/.claude/memory/global.jsonl
   ```

2. Restore from backup if invalid

3. If no backup, manually fix JSON:
   ```bash
   nano /home/node/.claude/memory/global.jsonl
   ```

### Memory Too Large

**If file grows too large (>10MB):**

1. **Archive old observations:**
   ```bash
   # Split by date if timestamps exist
   # Or manually review and remove old items
   ```

2. **Consolidate duplicate information:**
   - Remove redundant observations
   - Merge similar preferences

3. **Start fresh (nuclear option):**
   ```bash
   # Backup first!
   mv /home/node/.claude/memory/global.jsonl \
      ~/.claude/memory/archive-$(date +%Y%m%d).jsonl

   # Start new
   # Fresh file will be created on next write
   ```

## Export and Migration

### Export Memory

**To JSON:**
```bash
cat /home/node/.claude/memory/global.jsonl | jq -s . > memory-export.json
```

**To readable text:**
```bash
cat /home/node/.claude/memory/global.jsonl | \
  jq -r 'select(.name=="User") | .observations[]' > user-preferences.txt
```

### Migrate to New Environment

**Export from old environment:**
```bash
scp user@old-server:/home/node/.claude/memory/global.jsonl ./
```

**Import to new environment:**
```bash
scp ./global.jsonl user@new-server:/home/node/.claude/memory/
```

**Verify after migration:**
```bash
ssh user@new-server "cat /home/node/.claude/memory/global.jsonl | jq ."
```

## Security Considerations

### Access Control

**Memory file is user-readable:**
```bash
# Current permissions (recommended)
-rw-r--r-- 1 node node ... global.jsonl

# Make private if needed
chmod 600 /home/node/.claude/memory/global.jsonl
```

### Sensitive Information

**If accidentally stored:**
1. Immediately backup
2. Edit file to remove sensitive data
3. Verify with: `grep -i "password\|api.key\|token" global.jsonl`
4. If found, remove those lines
5. Validate JSON after edit

### Multi-User Environments

**If multiple people share `node` account:**
- Memory is shared (by design)
- Consider periodic resets
- Or don't use memory feature
- Or use separate HappyCapy accounts

## Best Practices

1. **Regular backups** - Before major operations
2. **Periodic review** - Monthly cleanup
3. **Monitor size** - Keep under 5MB for performance
4. **Validate after edits** - Always check JSON validity
5. **Use Memory MCP tools** - Prefer over direct file edits
6. **Document changes** - Keep changelog of major updates
7. **Test after restore** - Verify memory works after backup restore

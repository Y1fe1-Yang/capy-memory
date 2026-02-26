# Historical Conversation Import Guide

Detailed guide for importing and learning from historical conversations.

## Overview

Historical import allows capy-memory to learn from your past conversations with Claude,
extracting valuable preferences and habits without manual re-teaching.

## Import Process

### Step 1: Scan Sessions

```
Location: ~/.claude/projects/[workspace-hash]/[session-id].jsonl

Structure:
• Each workspace = one directory
• Each session = one .jsonl file
• JSONL format: one operation/message per line
```

### Step 2: Select Time Range

**Options:**
1. **All history** - Learn from everything (recommended for first time)
2. **Last 30 days** - Recent preferences (good balance)
3. **Last 7 days** - Very recent only (quick)
4. **Custom selection** - Choose specific sessions

**Recommendation:** Start with 30 days, expand if needed

### Step 3: Analysis Modes

**Hybrid Analysis (Recommended):**
1. Quick scan all messages for obvious patterns
2. Identify important conversation segments
3. Deep analysis on important parts only
4. Balance between speed and accuracy

**What gets analyzed:**
- User messages (explicit preferences)
- Assistant responses (inferred context)
- Tool usage patterns
- Repeated choices and behaviors

### Step 4: Information Extraction

**Extracted information types:**

**Preferences:**
- Language/framework choices
- Tool preferences
- Code style preferences
- Workflow preferences

**Background:**
- Experience level
- Current learning
- Domain expertise
- Communication preferences

**Patterns:**
- Repeated choices
- Common workflows
- Problem-solving approaches
- Tool usage frequency

### Step 5: Conflict Resolution

**When same topic has different information:**

**Strategy: Intelligent Judgment**
- Detect change signals ("now use", "switched to", "改用")
- Weight by recency (newer is more relevant)
- Weight by frequency (repeated statements stronger)
- Preserve evolution ("switched from X to Y")

**Example:**
```
Week 1: "I use npm"
Week 2: "I switched to pnpm"
Week 3: "pnpm is great"

Result: "Uses pnpm as package manager (switched from npm)"
```

### Step 6: Sensitive Information Filtering

**Automatic filtering (脱敏处理):**

**Patterns detected and filtered:**
- Email addresses: `user@example.com` → Filtered
- API keys: `api_key=xxx` → Filtered
- Tokens: `Bearer ghp_xxxxx` → Filtered
- Passwords: `password: ****` → Filtered
- Phone numbers: `555-1234` → Filtered

**Desensitization approach:**
```
Input: "My API key is sk-abc123def456"
Output: "Has OpenAI API key configured" ✅

Input: "Email me at user@example.com"
Output: "Prefers email communication" ✅
```

### Step 7: Preview and Confirmation

**Preview format:**
```
📝 Extracted 23 observations from 197 sessions

Preview (first 5):
1. Prefers TypeScript over JavaScript
2. Uses pnpm as package manager
3. Heavy user of document tools (pptx, pdf, xlsx)
4. Interested in AI content generation
5. Senior frontend engineer with 5 years React experience

... and 18 more

Actions:
[View all 23] [Save all] [Let me select] [Cancel]
```

## Cost Considerations

**Token usage estimation:**

```
For 250 sessions with avg 10 turns each:
• Quick scan: ~500K tokens (~$1-2)
• Hybrid: ~1M tokens (~$2-5)
• Deep analysis: ~2M tokens (~$5-10)
```

**Cost-saving strategies:**
- Use hybrid mode (good balance)
- Limit time range (last 30 days)
- Sample large sessions (analyze portions)

**Display to user:**
```
⚠️  Estimated token usage: ~1M tokens (~$3)
```

## Technical Implementation

### Session File Format

```jsonl
{"type":"user","message":{"role":"user","content":"..."}}
{"type":"assistant","message":{"role":"assistant","content":"..."}}
{"type":"tool_use","tool":"...","parameters":{}}
```

### Analysis Workflow

```python
for session in selected_sessions:
    # Load messages
    messages = load_session(session)

    # Quick scan for patterns
    patterns = quick_scan(messages)

    # Identify important segments
    important = identify_important(messages, patterns)

    # Deep analysis on important parts
    observations = deep_analyze(important)

    # Filter sensitive info
    observations = filter_sensitive(observations)

    # Accumulate
    all_observations.extend(observations)

# Deduplicate and resolve conflicts
final_observations = resolve_conflicts(all_observations)

# Present to user
show_preview(final_observations)
```

## Best Practices

### Before Import

1. **Backup existing memory** (if any):
   ```bash
   cp /home/node/.claude/memory/global.jsonl \
      ~/.claude/memory/backup-pre-import.jsonl
   ```

2. **Decide time range** - Recent is usually more relevant

3. **Review memory goals** - What do you want to learn?

### During Import

1. **Be patient** - Analysis takes time
2. **Review previews** - Don't blindly accept all
3. **Check for sensitive info** - Extra safety check

### After Import

1. **Query memory** - Verify it learned correctly:
   ```
   "What did you learn about my preferences?"
   "Show me TypeScript-related memory"
   ```

2. **Correct mistakes** - If something wrong:
   ```
   "Update memory: I actually prefer X"
   "Remove that incorrect information"
   ```

3. **Test in practice** - See if Claude applies knowledge correctly

## Troubleshooting

**Import fails:**
- Check session files are readable
- Verify JSONL format is valid
- Check available disk space

**Too many observations:**
- Use stricter filtering
- Shorter time range
- Review and remove redundant ones

**Missing key information:**
- Check if those sessions were analyzed
- Look for those patterns manually
- Add explicitly if needed

## Incremental Import

**For future imports:**

capy-memory tracks imported sessions:
```
~/.claude/memory/imported_sessions.txt
```

Only new sessions will be analyzed, avoiding duplicates.

**Manual incremental import:**
```
./scripts/import_history.py --since-last-import
```

## Example Import Session

```
$ capy-memory import history

🔍 Scanning historical conversations...
   Found 247 sessions (2026-01-30 to 2026-02-26)
   Total size: 15.3 MB

Time range:
[1] All history (247 sessions)
[2] Last 30 days (89 sessions) ← Recommended
[3] Last 7 days (23 sessions)
[4] Let me select
[5] Cancel

Your choice: 2

🤖 Analyzing 89 sessions (hybrid mode)...
   [████████████████████] 100% (89/89)

   Extracted: 34 observations
   Filtered: 3 (sensitive info)

📝 Preview (first 5):
1. Prefers TypeScript over JavaScript
2. Uses pnpm as package manager
3. Heavy document user (pptx 11x, pdf 14x)
4. Interested in AI generation
5. Senior frontend engineer

... and 29 more

⚠️  Token usage: ~850K tokens (~$2.50)

[View all] [Save all] [Select] [Cancel]: Save all

✅ Saved 31 observations to memory
📍 Location: /home/node/.claude/memory/global.jsonl

Done! Try: "What do you remember about me?"
```

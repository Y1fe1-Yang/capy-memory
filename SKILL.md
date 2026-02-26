---
name: capy-memory
description: Memory management for HappyCapy using Memory MCP. Enables Claude to remember user preferences, habits, and context across conversations. AUTOMATICALLY loads memory at session start. Triggers include automatic session initialization, explicit requests like "remember this"/"what do you know about me", implicit learning from stated preferences/corrections, and first-time memory setup.
---

# capy-memory

Persistent memory management using Memory MCP in HappyCapy environment.

## ⚠️ CRITICAL: Automatic Memory Loading

**At the START of EVERY conversation, you MUST:**

1. **Automatically load memory** (no user action required):
   ```
   Use ToolSearch to load: "memory"
   Then call: mcp__memory__read_graph
   ```

2. **Process loaded memory:**
   - Identify user preferences
   - Note technology choices
   - Remember workflows and habits
   - Apply throughout the conversation

3. **Silent operation:**
   - This happens in the background
   - User doesn't need to say "load my memory"
   - Memory is immediately available for use

4. **Token cost:**
   - Reading memory: ~500-2000 tokens (depends on size)
   - This cost is acceptable for better user experience
   - One-time cost per session

**This is NOT optional - memory loading is automatic for every conversation.**

## When to Use This Skill

### Automatic (No User Trigger)

**1. Session Start (MANDATORY):**
- Load memory at the beginning of EVERY conversation
- Read user preferences, context, and knowledge
- Apply throughout the conversation

**2. During Conversation (Intelligent Recognition):**

**Technology & Tool Preferences:**
- "I use pnpm" → Save package manager preference
- "I prefer TypeScript" → Save language preference
- "Don't use semicolons" → Save code style preference
- "Always use tabs, not spaces" → Save indentation preference
- "I'm on Node.js v20" → Save environment info

**Workflow & Habits:**
- "I always run tests before committing" → Save workflow
- "I prefer to write tests first" → Save development approach
- "I like to review PRs in the morning" → Save work habits
- "I usually..." / "I generally..." → Save patterns

**Corrections (HIGH PRIORITY):**
- "No, use pnpm not npm" → Update preference + note correction
- "Actually, I prefer X" → Override previous info
- "Don't do that anymore" → Remove old behavior
- "I changed to..." → Note evolution

**Background & Context:**
- "I'm a senior frontend engineer" → Save experience level
- "I work in UTC+8 timezone" → Save timezone
- "I'm currently learning Rust" → Save learning context
- "I'm building an e-commerce site" → Save project context

**Repeated Patterns:**
- User mentions same preference 3+ times → Strengthen memory
- Consistent tool choice across sessions → Solidify preference
- Regular workflow appears multiple times → Confirm habit

### Explicit User Requests

**Save to Memory:**
- "remember this" / "记住这个"
- "save this" / "保存一下"
- "keep this in mind" / "记录一下"
- "next time remember" / "下次记得"
- "don't forget" / "别忘了"
- "note that" / "注意"
- "for future reference" / "以后参考"
- "I prefer..." / "我喜欢..."
- "I always..." / "我总是..."
- "I usually..." / "我通常..."
- "I like to..." / "我喜欢..."
- "make a note" / "记一下"

**Query Memory:**
- "what do you know about me" / "你知道我什么"
- "what do you remember" / "你记得什么"
- "show my preferences" / "显示我的偏好"
- "review my memory" / "查看我的记忆"
- "what's in my memory" / "记忆里有什么"
- "what have you learned about me" / "你学到了我什么"
- "tell me what you know" / "告诉我你知道什么"
- "do you remember when I..." / "你记得我..."

**Update Memory:**
- "update: I now use..." / "更新：我现在用..."
- "correction: I prefer..." / "纠正：我喜欢..."
- "I changed to..." / "我改成了..."
- "I switched from X to Y" / "我从 X 换到了 Y"
- "not anymore, now I..." / "不再...，现在我..."

**Delete from Memory:**
- "forget that" / "忘掉这个"
- "remove X from memory" / "从记忆中删除 X"
- "that's no longer true" / "这个不对了"
- "I changed my mind about" / "我改主意了"
- "delete memory about" / "删除关于...的记忆"
- "don't remember that anymore" / "别再记这个了"

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
- Memory auto-loads at session start
- No installation prompts
- Proactive learning enabled
- User can explicitly request memory operations

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

### Implicit Learning Examples

**Example 1: Technology Preference**
```
User: "Use pnpm instead of npm"
→ Action: Save observation "Prefers pnpm over npm for package management"
→ Confirmation: "✓ Noted: I'll use pnpm for your projects"
```

**Example 2: Workflow Habit**
```
User: "Always run tests before committing"
→ Action: Save observation "Workflow: Always runs tests before git commits"
→ Confirmation: "✓ Remembered: I'll remind you to run tests before commits"
```

**Example 3: Code Style**
```
User: "I use 2 spaces, not 4"
→ Action: Save observation "Code style: 2-space indentation"
→ Confirmation: "✓ Got it: Using 2-space indentation"
```

**Example 4: Project Context**
```
User: "I'm building an e-commerce site with Next.js"
→ Action: Save observations:
  - "Current project: e-commerce website"
  - "Tech stack: Next.js"
→ Confirmation: "✓ Context saved for your e-commerce project"
```

**Example 5: Correction**
```
User: "No, I don't use Redux anymore, I use Zustand now"
→ Action:
  - Update/remove "Uses Redux for state management"
  - Add "Switched from Redux to Zustand for state management"
→ Confirmation: "✓ Updated: Using Zustand instead of Redux"
```

**Example 6: Repeated Pattern**
```
User says "use TypeScript" in 3 different sessions
→ Action: Strengthen observation "Strong preference for TypeScript"
→ Internal note: High confidence on this preference
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

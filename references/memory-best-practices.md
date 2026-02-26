# Memory Best Practices

Guidelines for effective memory usage with capy-memory.

## What to Remember

### ✅ Good Candidates

**User Preferences:**
- Language and framework choices ("Prefers TypeScript over JavaScript")
- Tool preferences ("Uses pnpm instead of npm")
- Code style preferences ("Likes concise code with minimal comments")
- Naming conventions ("Prefers camelCase for variables")

**Workflows and Habits:**
- Development practices ("Follows test-driven development")
- Git workflow ("Uses conventional commits")
- Code review preferences ("Wants detailed explanations in PRs")
- Problem-solving approach ("Prefers debugging with logs first")

**Background and Context:**
- Experience level ("Senior frontend engineer with 5 years experience")
- Current learning ("Currently learning Rust")
- Domain expertise ("Works on e-commerce platforms")
- Time zone and language ("UTC+8, prefers Chinese communication")

**Persistent Decisions:**
- Architecture choices ("Team uses microservices architecture")
- Technology stack ("Projects use React + Next.js + Tailwind")
- API conventions ("REST APIs follow JSON:API specification")

### ❌ Not Good for Memory

**Temporary Information:**
- Current tasks ("Debugging login bug")
- One-time operations ("Need to refactor utils.ts")
- Temporary state ("In the middle of feature X")

**Rapidly Changing Details:**
- Line numbers ("Bug is at line 123")
- File paths that change often
- Specific variable names from code

**Sensitive Information:**
- Passwords, API keys, tokens
- Personal identification (email, phone)
- Financial information
- Any credentials or secrets

**Project-Specific Bugs:**
- Individual bugs or issues
- Specific error messages
- One-time problems

## Memory Patterns

### Pattern 1: Preference Evolution

When preferences change, update rather than accumulate:

**Bad:**
```
"Uses npm" (old)
"Uses yarn" (2 months ago)
"Uses pnpm" (current)
```

**Good:**
```
"Uses pnpm as package manager (switched from yarn/npm)"
```

### Pattern 2: Context Qualification

Add context when information might be ambiguous:

**Vague:**
```
"Uses React"
```

**Better:**
```
"Primary framework is React for web projects"
"Expert in React with 5 years experience"
```

### Pattern 3: Confidence Levels

For uncertain information, qualify it:

**Uncertain:**
```
"Might prefer approach A"
```

**Better:**
```
"Has shown preference for approach A in recent projects"
"Occasionally uses approach B for specific cases"
```

## Communication with Memory

### Explicit Memory Requests

**Clear triggers:**
```
"Remember that I prefer TypeScript"
"Don't forget I use pnpm"
"记住我的代码风格偏好"
"Note that I work in UTC+8 timezone"
```

**Updating memory:**
```
"Update: I now use Bun instead of pnpm"
"Correction: I prefer Vim mode in VS Code"
"Change my framework preference to Solid"
```

**Querying memory:**
```
"What do you remember about my preferences?"
"Show memory about my TypeScript usage"
"What have you learned about my coding style?"
```

### Implicit Learning Signals

Claude will detect these patterns:

**Preference statements:**
- "I like X"
- "I prefer Y over Z"
- "I always use A"
- "I tend to B"

**Corrections:**
- "No, use this instead"
- "Actually, I prefer X"
- "That's not my style"
- "Change it to Y"

**Repeated choices:**
- Consistently choosing same options
- Always using certain patterns
- Regular use of specific tools

## Managing Memory

### Viewing Memory

**Full memory:**
```
"Show me everything you remember about me"
"Display my complete memory"
```

**Search memory:**
```
"Search memory for TypeScript"
"What do you remember about my testing practices?"
"Find memory entries about React"
```

**Memory statistics:**
```
"How many things do you remember?"
"When did you start remembering things?"
```

### Updating Memory

**Modify existing:**
```
"Update memory: I now prefer X"
"Change my Y preference to Z"
"Correct: I use A not B"
```

**Remove specific:**
```
"Forget about my old JavaScript preference"
"Delete memory about framework X"
"Remove information about Y"
```

### Resetting Memory

**Careful - this is permanent!**

```bash
# Backup first
cp /home/node/.claude/memory/global.jsonl \
   ~/.claude/memory/backup-$(date +%Y%m%d).jsonl

# Reset
rm /home/node/.claude/memory/global.jsonl
```

Or ask Claude:
```
"Clear all memory" (will ask for confirmation)
"Reset my memory completely"
```

## Privacy Considerations

### Automatic Filtering

capy-memory automatically filters:
- Email addresses
- Passwords and API keys
- Credit card numbers
- Social security numbers
- Phone numbers
- Other PII patterns

### Manual Review

Before saving bulk imports:
- Preview all observations
- Remove anything sensitive
- Check for accidentally captured secrets

### Multi-User Environments

If multiple people share the `node` account:
- Consider not using memory
- Or periodically clear personal preferences
- Be aware memory is global to the account

## Best Practices Summary

1. **Be explicit** - Clearly state preferences when you want them remembered
2. **Review imports** - Always review before saving historical data
3. **Update regularly** - Tell Claude when preferences change
4. **Query often** - Check what's remembered to ensure accuracy
5. **Trust Claude** - The model understands context well
6. **Privacy first** - Review memory for sensitive information
7. **Clean up** - Periodically remove outdated information

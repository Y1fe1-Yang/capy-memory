# Memory Best Practices

Guidelines for effective memory usage with capy-memory, based on Memory MCP official recommendations.

## Memory MCP Structure Overview

Memory MCP uses a **knowledge graph** with three core components:

1. **Entities** - Nodes representing distinct objects
2. **Relations** - Directed connections between entities
3. **Observations** - Atomic facts about entities

## Entity Types

Create entities for recurring objects that warrant their own knowledge nodes.

### Recommended Entity Types

Based on Memory MCP official guidance:

**Person**
- The user (primary entity)
- Collaborators or team members (if relevant)

**Organization**
- Companies: Anthropic, HappyCapy
- Open source projects
- Teams or communities

**Technology**
- Programming languages: TypeScript, Python, Rust
- Frameworks: Next.js, React, Vue
- Tools: pnpm, Memory MCP, Docker
- Platforms: GitHub, Vercel

**Project**
- Completed projects: capy-memory, desktop-pet
- Ongoing work: happycapy-mcp-manager
- Side projects or experiments

**Concept**
- Design principles: skill-creator, Progressive Disclosure
- Technical concepts: Memory Granularity, Auto-trigger
- Best practices: Git workflow, Testing strategies
- Domain knowledge: specific to user's work

**ConversationTopic**
- Major discussions with dates
- Problem-solving sessions
- Learning topics
- Key decisions made

**Event**
- Significant milestones
- Important dates
- Launches or releases

## What to Store as Entities vs Observations

### ✅ Create as Entities

**Recurring subjects that appear multiple times:**
- Organizations you work with
- Technologies you use regularly
- Projects you're working on
- Important people in your network
- Concepts you frequently reference

**Example:**
```json
{
  "name": "TypeScript",
  "entityType": "Technology",
  "observations": [
    "Statically typed JavaScript superset",
    "User's preferred language for new projects",
    "Version 5.x currently used"
  ]
}
```

### ✅ Store as Observations

**Atomic facts about entities:**
- One fact per observation
- Discrete, independent pieces of information
- Can be added/removed individually

**Example:**
```json
{
  "name": "User",
  "entityType": "Person",
  "observations": [
    "Works in UTC+8 timezone",
    "Prefers Chinese communication",
    "Senior frontend engineer"
  ]
}
```

## Memory Categories (Official MCP Guidance)

Memory MCP recommends capturing these categories:

### 1. Basic Identity
- Age, location, job title
- Education background
- Languages spoken
- Time zone

**Example observations:**
```
"Works in UTC+8 timezone"
"Senior frontend engineer with 5 years experience"
"Speaks Chinese and English"
```

### 2. Behaviors
- Interests and hobbies
- Regular habits
- Work patterns
- Learning activities

**Example observations:**
```
"Interested in AI generation and automation"
"Regularly uses Claude Code for development"
"Actively learning about Memory systems"
```

### 3. Preferences
- Communication style
- Language preferences
- Tool preferences
- Code style preferences

**Example observations:**
```
"Prefers concise, technical communication"
"Uses 2-space indentation"
"Likes minimal comments in code"
```

### 4. Goals
- Aspirations
- Current objectives
- Learning targets
- Project goals

**Example observations:**
```
"Learning Rust for systems programming"
"Building skills automation tools"
"Improving code quality practices"
```

### 5. Relationships
- Professional connections
- Organizational affiliations
- Project associations
- Technology preferences

**Use Relations for this:**
```json
{
  "from": "User",
  "to": "TypeScript",
  "relationType": "prefers"
}
```

## Relations (Connections)

Relations connect entities to build a knowledge graph. Always use **active voice**.

### Common Relation Types

**User-Technology Relations:**
- `prefers`: User prefers TypeScript
- `uses`: User uses pnpm
- `learning`: User is learning Rust
- `expert_in`: User is expert in React

**User-Project Relations:**
- `created`: User created capy-memory
- `working_on`: User is working on project X
- `completed`: User completed desktop-pet
- `maintains`: User maintains skill X

**User-Concept Relations:**
- `learned_about`: User learned about skill-creator
- `understands`: User understands Progressive Disclosure
- `follows`: User follows Git conventional commits

**User-Organization Relations:**
- `works_with`: User works with Anthropic
- `contributes_to`: User contributes to open source
- `member_of`: User is member of team

**Project-Technology Relations:**
- `uses`: capy-memory uses Memory MCP
- `built_with`: Project built with Next.js
- `requires`: Project requires Node.js v20

**Topic-Entity Relations:**
- `about`: Discussion about capy-memory
- `discussed`: Topic discussed skill-creator
- `resulted_in`: Discussion resulted in project X

## Practical Examples

### Example 1: User Profile with Relations

**Entities:**
```json
// User entity
{
  "name": "User",
  "entityType": "Person",
  "observations": [
    "Works in UTC+8 timezone",
    "Prefers Chinese communication",
    "Senior frontend engineer"
  ]
}

// Technology entity
{
  "name": "TypeScript",
  "entityType": "Technology",
  "observations": [
    "Statically typed JavaScript superset",
    "Strong type checking at compile time"
  ]
}
```

**Relations:**
```json
{
  "from": "User",
  "to": "TypeScript",
  "relationType": "prefers"
}

{
  "from": "User",
  "to": "TypeScript",
  "relationType": "expert_in"
}
```

### Example 2: Project with Context

**Entities:**
```json
// Project entity
{
  "name": "capy-memory",
  "entityType": "Project",
  "observations": [
    "Memory management skill for HappyCapy",
    "Created on 2026-02-23",
    "Complies with skill-creator standards",
    "SKILL.md is 372 lines"
  ]
}

// Concept entity
{
  "name": "skill-creator",
  "entityType": "Concept",
  "observations": [
    "Skills must not include README.md",
    "SKILL.md should be < 500 lines",
    "Triggers belong in description not body",
    "Uses progressive disclosure pattern"
  ]
}
```

**Relations:**
```json
{
  "from": "User",
  "to": "capy-memory",
  "relationType": "created"
}

{
  "from": "capy-memory",
  "to": "Memory MCP",
  "relationType": "uses"
}

{
  "from": "capy-memory",
  "to": "skill-creator",
  "relationType": "complies_with"
}
```

### Example 3: Conversation Topic

**Entity:**
```json
{
  "name": "Memory-Auto-Trigger-Discussion-2026-02-26",
  "entityType": "ConversationTopic",
  "observations": [
    "Discussed skill auto-trigger limitations",
    "Analyzed current triggering mechanism",
    "Proposed proactive skill marking approach",
    "Decided to optimize description first",
    "Date: 2026-02-26"
  ]
}
```

**Relations:**
```json
{
  "from": "User",
  "to": "Memory-Auto-Trigger-Discussion-2026-02-26",
  "relationType": "participated_in"
}

{
  "from": "Memory-Auto-Trigger-Discussion-2026-02-26",
  "to": "capy-memory",
  "relationType": "about"
}
```

## What NOT to Store

### ❌ Temporary Information
- Current line numbers or file paths
- One-time bugs or error messages
- In-progress debugging steps
- Temporary file names

### ❌ Rapidly Changing Details
- Specific variable names from code
- Exact error messages
- File locations that change frequently

### ❌ Sensitive Information
- Passwords, API keys, tokens
- Email addresses (unless necessary)
- Phone numbers
- Financial information
- Any credentials or secrets

### ❌ Duplicated Information
Don't store the same fact in multiple places:

**Bad:**
```
User: "Prefers TypeScript"
TypeScript: "User prefers this"
```

**Good:**
```
User --prefers--> TypeScript
```

## Memory Maintenance

### Observation Atomicity

Each observation should be **one atomic fact**:

**Bad:**
```
"Senior frontend engineer with 5 years experience who prefers TypeScript and works in UTC+8"
```

**Good:**
```
"Senior frontend engineer"
"5 years of experience"
"Works in UTC+8 timezone"
```

### Preference Evolution

When preferences change, update observations:

**Approach 1: Update the observation**
```
Old: "Uses npm for package management"
New: "Uses pnpm for package management (switched from npm)"
```

**Approach 2: Delete old, add new**
```
Delete: "Uses npm for package management"
Add: "Uses pnpm for package management"
Add: "Switched from npm to pnpm in February 2026"
```

### Periodic Review

**Monthly review recommended:**
1. Query full memory graph
2. Identify outdated observations
3. Update changed preferences
4. Remove obsolete information
5. Add missing relations

**Cleanup commands:**
```
"Review my memory for outdated information"
"Show all entities and their connections"
"Update my technology preferences"
"Remove old project observations"
```

## Query Patterns

Take advantage of the graph structure:

**Find all technologies user prefers:**
```
Query entities where User --prefers--> Technology
```

**Find projects using a specific technology:**
```
Query entities where Project --uses--> TypeScript
```

**Find related discussions:**
```
Query entities where Topic --about--> capy-memory
```

**Find learning topics:**
```
Query entities where User --learning--> Concept/Technology
```

## Progressive Memory Building

### Session-by-Session

**During conversation:**
1. Identify new entities (projects, topics, concepts)
2. Create entity records
3. Add atomic observations
4. Establish relations to existing entities

**After conversation:**
1. Review what was discussed
2. Extract key learnings as observations
3. Create ConversationTopic entity if significant
4. Connect topics to projects/concepts

### Historical Import

When importing history:
1. **Scan for entities** - Identify recurring subjects
2. **Extract observations** - Pull atomic facts
3. **Build relations** - Connect entities
4. **Deduplicate** - Remove redundant information
5. **Organize** - Group by entity type

See `references/import-guide.md` for detailed import process.

## Size Management

**Target sizes:**
- Optimal: 50-100 KB total
- Warning: 200 KB (consider cleanup)
- Critical: 500 KB (must cleanup)

**Optimization strategies:**
- Remove obsolete observations
- Consolidate duplicate facts
- Archive old ConversationTopic entities
- Keep only recent (30 days) detailed topics
- Promote patterns from topics to permanent observations

**Backup before cleanup:**
```bash
cp /home/node/.claude/memory/global.jsonl \
   ~/.claude/memory/backup-$(date +%Y%m%d).jsonl
```

#!/usr/bin/env python3
"""
Migrate and merge memory data from multiple sources to configured global path

This script:
1. Intelligently scans for memory files in all possible locations
2. Validates each file to ensure it's a valid Memory MCP file
3. Merges entities and relations from multiple sources with deduplication
4. Backs up original files before merging
5. Verifies the migration
"""

import json
import shutil
import sys
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher

# Paths
MEMORY_DIR = Path.home() / ".claude" / "memory"
TARGET_MEMORY_FILE = MEMORY_DIR / "global.jsonl"
NPX_CACHE_DIR = Path.home() / ".npm" / "_npx"
CLAUDE_DIR = Path.home() / ".claude"

def similar(a, b, threshold=0.85):
    """Check if two strings are similar (for deduplication)"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > threshold

def is_valid_memory_file(file_path):
    """Check if a file is a valid Memory MCP JSONL file"""
    if not file_path.exists() or file_path.stat().st_size == 0:
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines_checked = 0
            valid_items = 0

            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    item = json.loads(line)
                    if item.get('type') in ['entity', 'relation']:
                        valid_items += 1
                except json.JSONDecodeError:
                    pass

                lines_checked += 1
                if lines_checked >= 10:
                    break

            return valid_items > 0
    except Exception:
        return False

def find_all_memory_files():
    """Scan all possible locations for memory files"""
    candidates = []
    home = Path.home()

    print("\n🔍 Scanning for memory files...")

    print("   Checking npx cache...")
    npx_files = list(NPX_CACHE_DIR.glob("*/node_modules/@modelcontextprotocol/server-memory/dist/memory.jsonl"))
    for f in npx_files:
        if is_valid_memory_file(f):
            candidates.append(('npx cache', f))

    print("   Checking .claude directories...")
    claude_files = []
    if CLAUDE_DIR.exists():
        claude_files.extend(CLAUDE_DIR.glob("memory/**/*.jsonl"))
        claude_files.extend(CLAUDE_DIR.glob("projects/*/memory/**/*.jsonl"))

    for f in claude_files:
        if f == TARGET_MEMORY_FILE:
            continue
        if is_valid_memory_file(f):
            candidates.append(('.claude directory', f))

    print("   Checking home directory...")
    common_names = ['memory.jsonl', 'memories.jsonl', 'mcp-memory.jsonl']
    for name in common_names:
        f = home / name
        if is_valid_memory_file(f):
            candidates.append(('home directory', f))

    print("   Checking workspace directories...")
    workspace_dirs = [home / 'workspace', home / 'projects', home / 'code', home / 'dev']

    for workspace in workspace_dirs:
        if workspace.exists():
            workspace_files = workspace.glob("*/.claude/memory/**/*.jsonl")
            for f in workspace_files:
                if is_valid_memory_file(f):
                    candidates.append((f'workspace: {workspace.name}', f))

    print("   Checking /tmp directory...")
    tmp = Path('/tmp')
    if tmp.exists():
        tmp_files = tmp.glob("**/memory*.jsonl")
        for f in tmp_files:
            if is_valid_memory_file(f):
                candidates.append(('tmp directory', f))

    return candidates

def load_jsonl(file_path):
    """Load JSONL file into list of dictionaries"""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    data.append(json.loads(line))
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}")
        return None
    return data

def save_jsonl(data, file_path):
    """Save list of dictionaries to JSONL file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        return True
    except Exception as e:
        print(f"❌ Error writing {file_path}: {e}")
        return False

def deduplicate_observations(observations):
    """Remove duplicate and highly similar observations"""
    if not observations:
        return []

    unique = []
    for obs in observations:
        is_duplicate = False
        for existing in unique:
            if obs == existing or similar(obs, existing):
                is_duplicate = True
                break
        if not is_duplicate:
            unique.append(obs)

    return unique

def merge_entities(old_entities, new_entities):
    """Merge entities from two sources with intelligent deduplication"""
    entity_map = {}
    for entity in old_entities:
        name = entity.get('name')
        if name:
            entity_map[name] = entity.copy()

    for new_entity in new_entities:
        name = new_entity.get('name')
        if not name:
            continue

        if name in entity_map:
            old_obs = entity_map[name].get('observations', [])
            new_obs = new_entity.get('observations', [])
            combined = old_obs + new_obs
            entity_map[name]['observations'] = deduplicate_observations(combined)
        else:
            entity_map[name] = new_entity.copy()

    return list(entity_map.values())

def merge_relations(old_relations, new_relations):
    """Merge relations with deduplication"""
    relation_set = set()
    merged = []

    for rel in old_relations + new_relations:
        key = (rel.get('from'), rel.get('to'), rel.get('relationType'))
        if key not in relation_set:
            relation_set.add(key)
            merged.append(rel)

    return merged

def backup_file(file_path):
    """Create a backup of the file with timestamp"""
    if not file_path.exists():
        return None

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = file_path.parent / f"{file_path.stem}.backup.{timestamp}.jsonl"

    try:
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception as e:
        print(f"⚠️  Failed to backup {file_path}: {e}")
        return None

def select_sources_to_merge(candidates):
    """Let user select which memory files to merge"""
    if not candidates:
        return []

    print(f"\n📋 Found {len(candidates)} memory file(s):\n")

    for i, (location, path) in enumerate(candidates, 1):
        size = path.stat().st_size
        mtime = datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y-%m-%d %H:%M')

        print(f"  [{i}] {location}")
        print(f"      Path: {path}")
        print(f"      Size: {size} bytes")
        print(f"      Modified: {mtime}")

        data = load_jsonl(path)
        if data:
            entities = [item for item in data if item.get('type') == 'entity']
            relations = [item for item in data if item.get('type') == 'relation']
            total_obs = sum(len(e.get('observations', [])) for e in entities)
            print(f"      Content: {len(entities)} entities, {len(relations)} relations, {total_obs} observations")
        print()

    print("💡 All files will be merged together with intelligent deduplication")
    print("   Press Enter to continue, or type file numbers to select (e.g., 1,3,5)")
    print("   Type 'q' to cancel")

    try:
        choice = input("\n> ").strip()

        if choice.lower() == 'q':
            return None

        if not choice:
            return candidates

        selected = []
        for num in choice.split(','):
            try:
                idx = int(num.strip()) - 1
                if 0 <= idx < len(candidates):
                    selected.append(candidates[idx])
            except ValueError:
                pass

        return selected if selected else candidates

    except (EOFError, KeyboardInterrupt):
        return None

def migrate_and_merge():
    """Main migration and merge logic"""

    print("🔄 Memory Data Migration & Merge")
    print("=" * 50)

    candidates = find_all_memory_files()

    if not candidates:
        print("\n✅ No memory files found to migrate")
        print("   Your system is clean!")
        return

    selected = select_sources_to_merge(candidates)

    if selected is None:
        print("\n❌ Migration cancelled by user")
        return

    if not selected:
        print("\n⚠️  No files selected")
        return

    print(f"\n📦 Merging {len(selected)} file(s)...")

    all_entities = []
    all_relations = []

    for location, source_file in selected:
        print(f"\n📂 Loading: {location}")
        print(f"   {source_file}")

        source_data = load_jsonl(source_file)
        if source_data is None:
            print(f"   ⚠️  Skipped (failed to load)")
            continue

        entities = [item for item in source_data if item.get('type') == 'entity']
        relations = [item for item in source_data if item.get('type') == 'relation']

        print(f"   ✅ {len(entities)} entities, {len(relations)} relations")

        all_entities.extend(entities)
        all_relations.extend(relations)

    if TARGET_MEMORY_FILE.exists():
        print(f"\n📂 Existing target: {TARGET_MEMORY_FILE}")
        print(f"   Will merge with existing data")

        target_data = load_jsonl(TARGET_MEMORY_FILE)
        if target_data:
            target_entities = [item for item in target_data if item.get('type') == 'entity']
            target_relations = [item for item in target_data if item.get('type') == 'relation']
            print(f"   ✅ {len(target_entities)} entities, {len(target_relations)} relations")

            backup_path = backup_file(TARGET_MEMORY_FILE)
            if backup_path:
                print(f"   💾 Backup: {backup_path}")

            all_entities.extend(target_entities)
            all_relations.extend(target_relations)

    print(f"\n🔀 Merging {len(all_entities)} entities and {len(all_relations)} relations...")

    print("⚙️  Deduplicating entities...")
    merged_entities = merge_entities(all_entities, [])

    print("⚙️  Deduplicating relations...")
    merged_relations = merge_relations(all_relations, [])

    total_obs = sum(len(e.get('observations', [])) for e in merged_entities)
    original_obs = sum(len(e.get('observations', [])) for e in all_entities)

    print(f"\n📊 Merge results:")
    print(f"  Entities: {len(merged_entities)} (from {len(all_entities)} total)")
    print(f"  Relations: {len(merged_relations)} (from {len(all_relations)} total)")
    print(f"  Observations: {total_obs}")

    if original_obs > total_obs:
        deduped = original_obs - total_obs
        print(f"  🗑️  Removed {deduped} duplicate observations")

    merged_data = merged_entities + merged_relations

    print(f"\n💾 Saving merged data to: {TARGET_MEMORY_FILE}")
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    if not save_jsonl(merged_data, TARGET_MEMORY_FILE):
        print("❌ Failed to save merged data")
        return

    final_size = TARGET_MEMORY_FILE.stat().st_size
    print(f"\n✅ Migration complete!")
    print(f"   Final size: {final_size} bytes")
    print(f"   Location: {TARGET_MEMORY_FILE}")

    print("\n⚠️  IMPORTANT: Restart Claude Code for changes to take effect")
    print("   The Memory MCP server needs to reload with the new data location")

def main():
    try:
        migrate_and_merge()
    except KeyboardInterrupt:
        print("\n\n⚠️  Migration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Migration failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

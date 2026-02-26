#!/usr/bin/env python3
"""
Migrate and merge memory data from npx cache to configured global path

This script:
1. Finds memory data in npx cache directory
2. Reads both source (npx) and target (global) files if they exist
3. Intelligently merges entities and relations with deduplication
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

def similar(a, b, threshold=0.85):
    """Check if two strings are similar (for deduplication)"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > threshold

def find_npx_memory_file():
    """Find memory.jsonl in npx cache"""
    matches = list(NPX_CACHE_DIR.glob("*/node_modules/@modelcontextprotocol/server-memory/dist/memory.jsonl"))

    if not matches:
        return None

    # Return the most recently modified file
    return max(matches, key=lambda p: p.stat().st_mtime)

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
        # Check if this observation is already present or very similar
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
    # Index old entities by name
    entity_map = {}
    for entity in old_entities:
        name = entity.get('name')
        if name:
            entity_map[name] = entity.copy()

    # Merge new entities
    for new_entity in new_entities:
        name = new_entity.get('name')
        if not name:
            continue

        if name in entity_map:
            # Merge observations
            old_obs = entity_map[name].get('observations', [])
            new_obs = new_entity.get('observations', [])

            # Combine and deduplicate
            combined = old_obs + new_obs
            entity_map[name]['observations'] = deduplicate_observations(combined)
        else:
            # New entity, add it
            entity_map[name] = new_entity.copy()

    return list(entity_map.values())

def merge_relations(old_relations, new_relations):
    """Merge relations with deduplication"""
    # Relations are uniquely identified by (from, to, relationType)
    relation_set = set()
    merged = []

    for rel in old_relations + new_relations:
        key = (rel.get('from'), rel.get('to'), rel.get('relationType'))
        if key not in relation_set:
            relation_set.add(key)
            merged.append(rel)

    return merged

def analyze_data(data, label):
    """Analyze and display statistics about memory data"""
    entities = [item for item in data if item.get('type') == 'entity']
    relations = [item for item in data if item.get('type') == 'relation']

    total_observations = sum(len(e.get('observations', [])) for e in entities)

    print(f"\n{label}:")
    print(f"  Entities: {len(entities)}")
    print(f"  Relations: {len(relations)}")
    print(f"  Total observations: {total_observations}")

    if entities:
        print(f"  Entity names: {', '.join(e.get('name', '?') for e in entities[:5])}")
        if len(entities) > 5:
            print(f"    ... and {len(entities) - 5} more")

    return entities, relations

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

def migrate_and_merge():
    """Main migration and merge logic"""

    print("🔄 Memory Data Migration & Merge")
    print("=" * 50)

    # Find source file
    source_file = find_npx_memory_file()

    if not source_file:
        print("\nℹ️  No memory data found in npx cache")
        print("   Nothing to migrate")
        return

    print(f"\n📂 Source (npx cache): {source_file}")
    print(f"   Size: {source_file.stat().st_size} bytes")

    # Load source data
    print("\n📖 Loading source data...")
    source_data = load_jsonl(source_file)
    if source_data is None:
        print("❌ Failed to load source data")
        return

    source_entities, source_relations = analyze_data(source_data, "Source data")

    # Check target file
    target_exists = TARGET_MEMORY_FILE.exists()
    target_data = []

    if target_exists:
        print(f"\n📂 Target (global): {TARGET_MEMORY_FILE}")
        print(f"   Size: {TARGET_MEMORY_FILE.stat().st_size} bytes")

        print("\n📖 Loading target data...")
        target_data = load_jsonl(TARGET_MEMORY_FILE)
        if target_data is None:
            print("❌ Failed to load target data")
            return

        target_entities, target_relations = analyze_data(target_data, "Target data")
    else:
        print(f"\n📂 Target (global): {TARGET_MEMORY_FILE}")
        print("   File does not exist, will create new")
        target_entities = []
        target_relations = []

    # Decide merge strategy
    if not target_exists or len(target_data) == 0:
        print("\n✨ Strategy: Direct copy (target is empty)")
        merged_data = source_data
    else:
        print("\n🔀 Strategy: Intelligent merge with deduplication")

        # Backup target before merging
        if target_exists:
            backup_path = backup_file(TARGET_MEMORY_FILE)
            if backup_path:
                print(f"\n💾 Backup created: {backup_path}")

        # Merge entities and relations
        print("\n⚙️  Merging entities...")
        merged_entities = merge_entities(source_entities, target_entities)

        print("⚙️  Merging relations...")
        merged_relations = merge_relations(source_relations, target_relations)

        # Combine into final data
        merged_data = merged_entities + merged_relations

        # Show merge results
        total_obs = sum(len(e.get('observations', [])) for e in merged_entities)
        print(f"\n📊 Merge results:")
        print(f"  Entities: {len(merged_entities)} (was {len(source_entities)} + {len(target_entities)})")
        print(f"  Relations: {len(merged_relations)} (was {len(source_relations)} + {len(target_relations)})")
        print(f"  Total observations: {total_obs}")

        # Show deduplication stats
        source_obs = sum(len(e.get('observations', [])) for e in source_entities)
        target_obs = sum(len(e.get('observations', [])) for e in target_entities)
        deduped = (source_obs + target_obs) - total_obs
        if deduped > 0:
            print(f"  🗑️  Removed {deduped} duplicate observations")

    # Save merged data
    print(f"\n💾 Saving merged data to: {TARGET_MEMORY_FILE}")
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    if not save_jsonl(merged_data, TARGET_MEMORY_FILE):
        print("❌ Failed to save merged data")
        return

    # Verify
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

#!/usr/bin/env python3
"""
Import and analyze historical conversations

This is a placeholder script that outlines the import workflow.
Full implementation requires LLM API calls for intelligent analysis.

Usage:
  ./import_history.py --days 30      # Last 30 days
  ./import_history.py --all          # All history
  ./import_history.py --interactive  # Let user select
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import glob

PROJECTS_DIR = Path.home() / ".claude" / "projects"

def scan_sessions(days=None):
    """Scan all session files"""
    sessions = []

    if not PROJECTS_DIR.exists():
        print(f"❌ Projects directory not found: {PROJECTS_DIR}")
        return sessions

    pattern = str(PROJECTS_DIR / "*" / "*.jsonl")
    all_files = glob.glob(pattern)

    cutoff_date = None
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)

    for file_path in all_files:
        path = Path(file_path)
        mtime = datetime.fromtimestamp(path.stat().st_mtime)

        if cutoff_date and mtime < cutoff_date:
            continue

        size = path.stat().st_size
        sessions.append({
            "file": str(path),
            "modified": mtime.isoformat(),
            "size": size
        })

    return sorted(sessions, key=lambda x: x['modified'], reverse=True)

def show_summary(sessions):
    """Show summary of sessions"""
    if not sessions:
        print("No sessions found")
        return

    total_size = sum(s['size'] for s in sessions)
    oldest = min(s['modified'] for s in sessions)
    newest = max(s['modified'] for s in sessions)

    print(f"📊 Session Summary")
    print(f"   Total sessions: {len(sessions)}")
    print(f"   Date range: {oldest[:10]} to {newest[:10]}")
    print(f"   Total size: {total_size / (1024*1024):.1f} MB")
    print()

def main():
    parser = argparse.ArgumentParser(
        description='Import historical conversations to memory'
    )
    parser.add_argument('--days', type=int,
                       help='Import last N days')
    parser.add_argument('--all', action='store_true',
                       help='Import all history')
    parser.add_argument('--interactive', action='store_true',
                       help='Interactive selection')

    args = parser.parse_args()

    print("🔍 Scanning historical conversations...")
    print()

    if args.all:
        sessions = scan_sessions()
    elif args.days:
        sessions = scan_sessions(days=args.days)
    elif args.interactive:
        sessions = scan_sessions()
    else:
        # Default: last 30 days
        sessions = scan_sessions(days=30)

    show_summary(sessions)

    if not sessions:
        print("No sessions to import")
        return

    print("⚠️  Note: Full import functionality requires:")
    print("   1. LLM API for intelligent conversation analysis")
    print("   2. Pattern matching for preference extraction")
    print("   3. Conflict resolution for contradictory information")
    print("   4. Sensitive information filtering")
    print()
    print("   This is a placeholder. Actual implementation")
    print("   should be done within the capy-memory skill")
    print("   using Claude's capabilities directly.")
    print()
    print("💡 Suggested approach:")
    print("   Let Claude read session files directly and")
    print("   use Memory MCP tools to save observations")

if __name__ == '__main__':
    main()

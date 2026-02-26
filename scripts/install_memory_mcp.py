#!/usr/bin/env python3
"""
Install and configure Memory MCP in HappyCapy environment

This script:
1. Creates the memory directory at /home/node/.claude/memory/
2. Configures Memory MCP in /home/node/.claude.json using npx
3. Preserves any existing MCP server configurations
"""

import json
import sys
from pathlib import Path

# Fixed paths in HappyCapy environment
CONFIG_FILE = Path.home() / ".claude.json"
MEMORY_DIR = Path.home() / ".claude" / "memory"
MEMORY_FILE = MEMORY_DIR / "global.jsonl"

def create_memory_directory():
    """Create memory directory if it doesn't exist"""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created memory directory: {MEMORY_DIR}")

def configure_memory_mcp():
    """Add Memory MCP configuration to .claude.json"""
    
    # Load existing config or create new one
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    
    # Ensure mcpServers section exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    # Check if memory is already configured
    if "memory" in config["mcpServers"]:
        print("ℹ️  Memory MCP already configured")
        return
    
    # Add Memory MCP configuration using npx
    config["mcpServers"]["memory"] = {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"],
        "env": {
            "MEMORY_FILE_PATH": str(MEMORY_FILE)
        }
    }
    
    # Write back to config file
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configured Memory MCP in {CONFIG_FILE}")
    print(f"   Memory file: {MEMORY_FILE}")
    print(f"   Command: npx -y @modelcontextprotocol/server-memory")

def main():
    print("🔧 Installing Memory MCP...")
    print()
    
    try:
        # Step 1: Create directory
        create_memory_directory()
        
        # Step 2: Configure MCP
        configure_memory_mcp()
        
        print()
        print("✅ Memory MCP installation complete!")
        print()
        print("Next steps:")
        print("1. Restart Claude Code (if currently running)")
        print("2. Memory will be created on first write operation")
        print("3. Run 'scripts/check_memory_status.sh' to verify")
        
    except Exception as e:
        print(f"❌ Installation failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

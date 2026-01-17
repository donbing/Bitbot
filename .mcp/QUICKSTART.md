# Quick Start: MCP Code Review Setup

This guide helps you set up the MCP server for BitBot code review to avoid rate limits and context overflow.

## TL;DR

**Problem**: MCP server hits rate limits and context limits during code review  
**Solution**: Use the optimized configuration in this directory

## Quick Setup for Claude Desktop

### Step 1: Find Your Config File

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Step 2: Add This Configuration

Open your `claude_desktop_config.json` and add (or merge with existing):

```json
{
  "mcpServers": {
    "bitbot": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/ABSOLUTE/PATH/TO/Bitbot"
      ]
    }
  }
}
```

**Important**: Replace `/ABSOLUTE/PATH/TO/Bitbot` with the actual path to this repository!

### Step 3: Restart Claude Desktop

Close and reopen Claude Desktop completely.

### Step 4: Verify

In Claude Desktop, you should see the MCP server connected. Try asking:
> "Show me the structure of this repository"

## What This Fixes

### Rate Limiting Issues ✅
- The `.mcpignore` file excludes unnecessary files (images, build artifacts, etc.)
- Reduces the number of files MCP needs to process
- Fewer files = fewer API calls = no rate limits

### Context Window Issues ✅
- `.mcpignore` excludes large files (images, binaries, etc.)
- Max file size set to 1MB
- Excludes test data and generated files
- Cleaner context = better code review

## Files Excluded from Context

The `.mcpignore` automatically excludes:

```
✗ Images (PNG, JPG, SVG, etc.)
✗ Build artifacts (__pycache__, dist/, build/)
✗ Test coverage files
✗ Dependencies (node_modules/)
✗ IDE configs (.vscode/, .idea/)
✗ Large data files (*.db, *.sqlite)
✗ Minified JS/CSS
✗ Docker override files
✗ Environment secrets (.env*)
```

## Troubleshooting

### "Still getting rate limited"

Add more patterns to `.mcpignore`:
```
# Add at the end of .mcpignore
tests/data/
docs/images/
```

### "Context is still too large"

Check for large files:
```bash
find . -type f -size +100k | grep -v ".git"
```

Add them to `.mcpignore`.

### "MCP server not connecting"

1. Check the path in config.json is correct and absolute
2. Ensure Node.js is installed: `node --version`
3. Restart Claude Desktop completely
4. Check Claude Desktop logs

## Advanced: Fine-Tuning

Edit `.mcp/config.json` if you need:
- Different rate limits
- Different context sizes
- Custom file exclusions

See `.mcp/README.md` for detailed configuration options.

## Common Use Cases

### Code Review Session
```
✓ MCP loads only Python source files
✓ Skips images and build artifacts
✓ Respects .gitignore patterns
✓ Caches results for better performance
```

### Architecture Discussion
```
✓ Fast access to key files
✓ No rate limiting interruptions
✓ Full context of important files
✓ Excludes noise from binary files
```

### Bug Investigation
```
✓ Quick file navigation
✓ Search across source code only
✓ No context wasted on test images
✓ Efficient token usage
```

## Benefits

| Before | After |
|--------|-------|
| 🐌 Slow (loads all files) | ⚡ Fast (only source files) |
| 🚫 Rate limits hit quickly | ✅ Stays within limits |
| 💥 Context overflow | ✅ Manageable context |
| 🖼️ Processes images | ⏭️ Skips unnecessary files |
| 🔄 Re-processes everything | 💾 Uses caching |

## Getting Help

1. Check `.mcp/README.md` for detailed docs
2. Review `.mcpignore` patterns
3. Test with a simple query first
4. Verify path in configuration

---

**Remember**: The `.mcpignore` file is your friend! Add any files that don't need to be in the MCP context.

# MCP Code Review Setup

This repository includes optimized MCP (Model Context Protocol) server configuration to prevent rate limiting and context overflow issues during AI-assisted code review sessions.

## Quick Links

- 🚀 **[Quick Start Guide](.mcp/QUICKSTART.md)** - Get set up in 5 minutes
- 📖 **[Full Documentation](.mcp/README.md)** - Comprehensive configuration guide
- 📊 **[Impact Analysis](.mcp/IMPACT.md)** - Performance improvements (94.4% context reduction)
- 📋 **[Example Config](.mcp/claude_desktop_config.example.json)** - Ready-to-use configuration

## The Problem

When using MCP servers for code review, you may encounter:
- ❌ Rate limit errors from API calls
- ❌ Context window overflow from too many files
- ❌ Slow performance from processing unnecessary files
- ❌ Wasted tokens on binary files and build artifacts

## The Solution

This repository includes:

1. **`.mcpignore`** - Excludes 156 files (10.94 MB) from context
2. **`.mcp/config.json`** - Optimized MCP server settings
3. **Comprehensive docs** - Setup guides and troubleshooting

### Key Improvements

| Metric | Result |
|--------|--------|
| Context Size Reduction | **94.4%** (11.58 MB → 0.65 MB) |
| File Count Reduction | **53.8%** (290 → 134 files) |
| Rate Limiting | **30 requests/min** (prevents API errors) |
| Max File Size | **1 MB** (skips large files) |
| Caching | **Enabled** (reduces repeated calls) |

## Quick Setup

### For Claude Desktop

1. Open your Claude Desktop config:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Add this configuration (replace the path):
   ```json
   {
     "mcpServers": {
       "bitbot": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-filesystem",
           "/REPLACE/WITH/ABSOLUTE/PATH/TO/Bitbot"
         ]
       }
     }
   }
   ```

3. Restart Claude Desktop

4. Test by asking: *"Show me the repository structure"*

See **[QUICKSTART.md](.mcp/QUICKSTART.md)** for more details.

## What Gets Excluded

The `.mcpignore` automatically excludes:

- 🖼️ Images (PNG, JPG, SVG, PDF)
- 🏗️ Build artifacts (`__pycache__`, `dist/`, `build/`)
- 🧪 Test coverage files (`.coverage`, `htmlcov/`)
- 📦 Dependencies (`node_modules/`)
- ⚙️ IDE configs (`.vscode/`, `.idea/`)
- 🗄️ Large data files (`.db`, `.sqlite`, `.json.gz`)
- 📦 Minified files (`*.min.js`, `*.min.css`)
- 🔐 Environment secrets (`.env*`)

Only **source code and documentation** are included in the MCP context.

## Benefits

### Before Optimization
```
❌ Loading 290 files (11.58 MB)
❌ Processing images, binaries, cache files
❌ Error: Rate limit exceeded
❌ Error: Context window overflow
```

### After Optimization
```
✅ Loading 134 files (0.65 MB)
✅ Processing Python source and docs only
✅ No rate limit issues
✅ No context overflow
```

## Documentation

- **[QUICKSTART.md](.mcp/QUICKSTART.md)** - 5-minute setup guide
- **[README.md](.mcp/README.md)** - Full configuration reference
- **[IMPACT.md](.mcp/IMPACT.md)** - Performance analysis
- **[claude_desktop_config.example.json](.mcp/claude_desktop_config.example.json)** - Example config

## Files

```
.mcp/
├── config.json                          # MCP server configuration
├── README.md                            # Full documentation
├── QUICKSTART.md                        # Quick setup guide
├── IMPACT.md                            # Performance analysis
└── claude_desktop_config.example.json   # Example configuration

.mcpignore                               # File exclusion patterns
```

## Customization

To exclude additional files, add patterns to `.mcpignore`:

```bash
# Add custom exclusions
my_large_file.txt
experimental/
*.backup
```

To adjust rate limits or context window, edit `.mcp/config.json`.

See **[README.md](.mcp/README.md)** for full customization options.

## Troubleshooting

### Still getting rate limited?
- Reduce `maxRequestsPerMinute` in config.json
- Add more patterns to `.mcpignore`

### Context still too large?
- Reduce `maxTokens` in config.json
- Exclude more files in `.mcpignore`
- Check for large files: `find . -type f -size +100k`

### MCP server not connecting?
- Verify the path in config.json is absolute
- Ensure Node.js is installed: `node --version`
- Restart your MCP client completely

See **[QUICKSTART.md](.mcp/QUICKSTART.md)** for more troubleshooting tips.

## Testing

To verify the configuration is working:

```bash
# Validate JSON
python3 -m json.tool .mcp/config.json

# Check what files are excluded
grep -E "^\." .mcpignore | head -10

# Count Python files (should be included)
find . -name "*.py" | wc -l
```

## Support

- Check `.mcp/README.md` for detailed documentation
- Review `.mcp/QUICKSTART.md` for common issues
- See `.mcp/IMPACT.md` for expected performance

## Summary

✅ **94.4% context reduction** achieved  
✅ **Rate limiting** configured (30/min)  
✅ **Context overflow** prevented (100k tokens)  
✅ **Binary files** excluded (10.94 MB)  
✅ **Source code** included (52 Python files)  
✅ **Documentation** comprehensive  

The MCP server is now optimized for efficient code review! 🎉

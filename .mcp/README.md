# MCP Server Configuration for BitBot Code Review

This directory contains configuration files for the Model Context Protocol (MCP) server used for code review of the BitBot project.

## Purpose

The MCP server configuration is designed to prevent rate limiting and context window overflow issues when performing code reviews or AI-assisted development on the BitBot codebase.

## Configuration Files

### `.mcp/config.json`

Main configuration file for the MCP server with the following optimizations:

#### Rate Limiting
- **maxRequestsPerMinute**: 30 - Limits API calls to prevent hitting rate limits
- **maxConcurrentRequests**: 3 - Controls parallel request processing
- **enabled**: true - Ensures rate limiting is active

#### Context Window Management
- **maxTokens**: 100,000 - Maximum tokens to process at once
- **chunkSize**: 10,000 - Size of individual chunks for processing
- **overlapTokens**: 500 - Overlap between chunks to maintain context continuity

#### File Filtering
- **respectGitignore**: true - Honors `.gitignore` patterns
- **respectMcpignore**: true - Honors `.mcpignore` patterns
- **maxFileSize**: 1MB (1,048,576 bytes) - Skips files larger than this
- **excludePatterns**: Comprehensive list of patterns to exclude:
  - Python artifacts (`__pycache__`, `*.pyc`, etc.)
  - Build artifacts (`dist/`, `build/`, etc.)
  - Binary files (images, PDFs, archives)
  - Minified files (`*.min.js`, `*.min.css`)
  - Test coverage and cache files

#### Caching
- **enabled**: true - Enables response caching
- **ttl**: 3600 seconds (1 hour) - Cache time-to-live
- **maxCacheSize**: 50MB (52,428,800 bytes) - Maximum cache size

### `.mcpignore`

Gitignore-style file that specifies additional files and directories to exclude from MCP server processing. This reduces context size and prevents unnecessary processing of:

- Build artifacts
- Dependencies
- Test coverage files
- Large binary files (images, PDFs)
- Temporary files
- IDE configuration files
- Environment files with secrets

## Usage

### For Claude Desktop

1. Copy the `.mcp/config.json` to your Claude Desktop MCP configuration directory:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Merge or replace the `mcpServers` section with the configuration from `.mcp/config.json`

3. Restart Claude Desktop

### For Cline/Continue/Other MCP Clients

1. Locate your MCP client's configuration directory
2. Add the server configuration from `.mcp/config.json` to your client's config
3. Adjust the file path in the `args` array to point to your local BitBot directory
4. Restart your MCP client

### For Command Line Usage

```bash
# Install the MCP filesystem server
npm install -g @modelcontextprotocol/server-filesystem

# Run with configuration
npx @modelcontextprotocol/server-filesystem /path/to/Bitbot
```

## Customization

### Adjusting Rate Limits

If you have a higher API tier or need different rate limiting:

```json
"rateLimit": {
  "enabled": true,
  "maxRequestsPerMinute": 60,  // Increase for higher tier
  "maxConcurrentRequests": 5   // Increase for better performance
}
```

### Adjusting Context Window

For larger or smaller models:

```json
"contextWindow": {
  "maxTokens": 200000,    // Increase for larger context windows
  "chunkSize": 20000,     // Adjust chunk size proportionally
  "overlapTokens": 1000   // Increase overlap for better continuity
}
```

### Adding File Exclusions

To exclude additional file patterns, add them to `.mcpignore`:

```
# Custom exclusions
my_large_file.txt
experimental/
*.backup
```

Or add to the `excludePatterns` array in `config.json`:

```json
"excludePatterns": [
  "**/__pycache__/**",
  "**/my_custom_pattern/**"
]
```

## Troubleshooting

### Still Hitting Rate Limits

1. Reduce `maxRequestsPerMinute` further
2. Reduce `maxConcurrentRequests` to 1 or 2
3. Add more file patterns to `.mcpignore`

### Context Window Still Too Large

1. Reduce `maxTokens` in context window settings
2. Reduce `chunkSize` for smaller processing units
3. Add more exclusions to `.mcpignore`
4. Reduce `maxFileSize` to skip larger files

### Files Not Being Excluded

1. Verify `.mcpignore` is in the repository root
2. Check that `respectMcpignore` is `true` in config
3. Ensure your MCP client supports `.mcpignore`
4. Add patterns to `excludePatterns` array as fallback

## Best Practices

1. **Keep excludePatterns Updated**: As the project grows, regularly review and update exclusion patterns
2. **Monitor Cache Size**: If cache grows too large, reduce `maxCacheSize` or `ttl`
3. **Test Changes**: After modifying configuration, test with a small code review task first
4. **Version Control**: Keep `.mcp/config.json` and `.mcpignore` in version control for team consistency

## File Size Limits

Current limits to prevent context overflow:
- Individual file: 1MB max
- Total cache: 50MB max
- Context window: 100,000 tokens max

These can be adjusted based on your needs and API tier.

## Security Notes

- The configuration excludes `.env` files and other sensitive data patterns
- Always verify that secrets are not included in context
- The MCP server should only be used on trusted codebases
- Cache directory should be secured appropriately

## Support

For issues with MCP server configuration:
1. Check the [MCP Documentation](https://modelcontextprotocol.io)
2. Review your MCP client's documentation
3. Verify your API tier and rate limits
4. Check the MCP server logs for specific errors

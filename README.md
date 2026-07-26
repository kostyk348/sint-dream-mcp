# sint-dream-mcp

**Agent Dreaming** — offline consolidation between MCP sessions.

Compresses similar memory blocks into generalized knowledge, finds error patterns, and suggests new skills.

## Tools

| Tool | Description |
|------|-------------|
| `dream_consolidate(blocks_json)` | Group blocks by domain+tags, merge into generalized FACT claims |
| `dream_error_patterns(blocks_json)` | Find recurring failure patterns → anti-patterns |
| `dream_skill_suggestions(blocks_json, usage_stats)` | Suggest skills when a tool is used 5+ times in a domain |
| `dream_generalize(domain)` | Generalize across all stored dreams for a domain |
| `dream_report()` | Full dream report combining all analyses |
| `dream_store(domain, content, kind)` | Persist a dream result to `~/.config/opencode/dreams/` |

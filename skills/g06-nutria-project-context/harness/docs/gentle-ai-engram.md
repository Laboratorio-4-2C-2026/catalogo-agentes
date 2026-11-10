# Gentle AI and Engram

This harness assumes **Gentle AI** (interpreting “Gentle-ui” as Gentle AI) can provide orchestration conventions and **Engram** provides persistent memory. They are complementary:

- Gentle AI determines delegation/review workflow when it is installed.
- NutrIA profiles define which role owns the task and its approval gate.
- Engram stores curated project context across sessions.

The installer provisions the official Engram binary into the target project at `.nutria/bin/` and wires its absolute path into the generated MCP configuration. It does not overwrite an existing MCP server with the same name. The generated MCP entry invokes `engram mcp --tools=agent`, and `.engram/config.json` fixes project detection.

Do not enable two competing Engram configurations. If an existing Gentle AI setup already provisions Engram, keep its server entry and only install NutrIA agents/skills.

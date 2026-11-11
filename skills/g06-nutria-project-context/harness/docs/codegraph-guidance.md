# CodeGraph protocol

CodeGraph is automatically provisioned by `nutria-harness` for Codex and Claude. It runs locally and exposes the read-only `codegraph_explore` MCP tool.

Use it before broad filesystem exploration for repository maps, architecture, dependencies, symbol references, call flows and impact analysis. The team rule is documented in `.ai/codegraph.md` and the portable skill is `codegraph-guidance`.

The harness initializes the graph only when the installation target is a recognized project. The runtime never auto-runs destructive/admin lifecycle commands.

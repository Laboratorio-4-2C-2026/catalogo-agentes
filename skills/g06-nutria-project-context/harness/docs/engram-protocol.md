# Engram protocol

Engram is mandatory project memory, not an opt-in assistant feature.

## Save immediately

Call `mem_save` after an architecture/design decision, convention/workflow change, bug fix, configuration change, non-obvious discovery, established pattern, significant artifact update, or confirmed user preference. Use a searchable verb title, a correct type, project scope, a stable `topic_key`, and structured **What / Why / Where / Learned** content.

Call `mem_save_prompt` when the original user prompt is observable so prompt capture can be attached to derived saves. Do not store secrets, tokens, PII or production data.

## Retrieve and review

- At session start or before architecture-sensitive work, call `mem_review list` when available.
- For recall/past-work requests, call `mem_context`, then `mem_search`, then `mem_get_observation` for the full record.
- Treat `needs_review` observations as stale until verified; never mark them reviewed automatically.
- Keep topic keys separate; update a known observation only when it is the same evolving topic.

## Close every session

Call `mem_session_summary` before reporting completion. Include goal, instructions, discoveries, accomplishments, next steps and relevant files.

## After compaction

Persist a session summary immediately, recover with `mem_context`, then continue.

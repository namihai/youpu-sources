---
name: youpu-gatekeeper
description: Use this skill when working in the youpu-sources repository and the task is to check imports, run ingest, validate the repository, explain import issues, inspect a URL, or perform a guarded submit/push. This skill should be used for repository gatekeeping workflows, not for source discovery or metadata completion.
---

# youpu Gatekeeper

This skill is the natural-language entrypoint for the `youpu` repository gatekeeping workflow.

Use it only for:

- checking `imports/`
- running `youpu ingest --dry-run`
- running `youpu ingest`
- running `youpu validate`
- running `youpu report`
- running `youpu submit --check-only`
- running `youpu submit --message "..." [--push]` with an AI-written message
- running `youpu inspect-url <url>`
- explaining `imports/reports/issues.md`

Do not use it for:

- source discovery
- webpage analysis
- filling missing accepted/rejected fields
- deciding whether an external source should be accepted or rejected
- writing directly to `accepted/` or `rejected/` without going through `youpu`

## Workflow

Follow these rules strictly:

1. Before any write operation, run the corresponding check first.
2. If a check returns problems, stop and explain them.
3. Do not invent rules beyond the repository docs and `youpu` output.
4. Use the default `imports/` directory only.

Write-operation guardrails:

- Before import:
  - run `./youpu ingest --dry-run`
  - only if it passes, run `./youpu ingest`
- Before submit:
  - run `./youpu submit --check-only`
  - only if it passes, inspect the current changes and write a concise commit message
  - then run `./youpu submit --message "..."` and optionally `--push`

## Command Mapping

Map user requests to commands like this:

- "检查 imports" -> `./youpu ingest --dry-run`
- "导入 imports" -> `./youpu ingest --dry-run`, then `./youpu ingest` if clean
- "检查仓库" -> `./youpu validate`
- "提交前检查" -> `./youpu submit --check-only`
- "提交" -> `./youpu submit --check-only`, then generate a message, then `./youpu submit --message "..."`
- "提交并推送" -> `./youpu submit --check-only`, then generate a message, then `./youpu submit --message "..." --push`
- "检查这个 URL" -> `./youpu inspect-url '<url>'`

## Failure Handling

Stop and report when any of these is true:

- `youpu ingest --dry-run` reports issues
- `youpu validate` fails
- `youpu submit --check-only` fails
- `imports/reports/issues.md` still lists unresolved issues
- a CLI command returns a runtime error you cannot safely recover from

When stopping:

- summarize the failing command
- point to the relevant file or report when available
- tell the user the next manual step

## Response Style

Be concise. Report:

- what command you ran
- whether it passed
- what blocked progress, if anything
- the next action

When the user asks to submit or push:

- do not ask the user to provide a commit message by default
- inspect the current changes
- write a short, concrete commit message that matches the change set
- tell the user which message you used

If you need repository details, consult:

- `docs/overview/project-scope.md`
- `docs/cli/scope.md`
- `docs/cli/spec.md`
- `docs/cli/user-guide.md`
- `docs/specs/url.md`

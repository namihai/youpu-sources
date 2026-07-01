# 常见失败与处理方式

这份文档说明 `youpu` 检查失败时如何定位问题。

## 基本原则

- 先看错误码 `code`
- 再看 `path`
- 修正对应文件后重新运行同一个命令
- 不要为了通过检查而绕过 `staging/` 或 `data/` 的目录边界

常用命令：

```bash
uv run python ./scripts/youpu validate-schema
uv run python ./scripts/youpu validate-repo
uv run python ./scripts/youpu validate-imports
uv run python ./scripts/youpu check-pr
uv run python ./scripts/youpu check-merge
```

## Schema 失败

常见错误码：

- `schema_missing`
- `schema_parse_error`
- `accepted_schema_invalid`
- `accepted_template_missing`
- `accepted_template_parse_error`
- `accepted_template_field_order_mismatch`

处理方式：

- 确认 `schemas/accepted.json` 存在且是合法 JSON
- 确认 `templates/accepted.md` 存在
- 如果调整字段，先改 schema，再同步 template 和文档
- 运行 `uv run python ./scripts/youpu validate-schema`

## 正式区失败

常见错误码：

- `data_unexpected_file`
- `accepted_parse_error`
- `accepted_invalid_filename`
- `accepted_missing_field`
- `accepted_unknown_field`
- `accepted_invalid_array`
- `accepted_invalid_enum`
- `accepted_invalid_canonical_url`
- `accepted_duplicate_index`
- `accepted_duplicate_canonical_url`
- `accepted_duplicate_title`

处理方式：

- `data/` 根目录只允许正式 accepted Markdown
- 正式文件名必须是 `SRC-####-slug.md`
- `canonical_url` 必须是合法 URL
- 同一个规范化后的 `canonical_url` 不能重复
- `title` 重复是 warning，但应人工确认是否确实是不同来源

## Staging 失败

常见错误码：

- `staging_unexpected_file`
- `staging_accepted_invalid_filename`
- `staging_accepted_parse_error`
- `staging_accepted_missing_field`
- `staging_accepted_unknown_field`
- `staging_accepted_invalid_array`
- `staging_accepted_invalid_enum`
- `staging_accepted_invalid_canonical_url`
- `staging_accepted_conflict_accepted`
- `staging_accepted_duplicate_canonical_url`
- `repo_accepted_conflict_index_failed`

处理方式：

- `staging/` 根目录只允许 Markdown 文件
- `staging/` 中只允许 Markdown 文件
- staging 文件名必须是英文小写 slug，例如 `example-source.md`
- staging 文件名不能使用 `SRC-####-slug.md`
- 不要把正式文件复制到 staging 里修改
- 如果 URL 已存在于 `data/`，这是新增候选与正式区冲突

## Ingest 失败

常见错误码：

- `staging_empty`
- `ingest_io_error`
- staging 或正式区相关错误码

处理方式：

- `staging_empty` 表示没有可导入的 `staging/*.md`
- 如果有 staging 诊断，先修正诊断问题再重新运行 ingest
- 如果是 I/O 错误，确认文件权限和工作区状态
- ingest 失败时不应产生部分正式写入

## Merge Check 失败

常见错误码：

- `merge_pending_staging`
- schema、repo、staging 相关错误码

处理方式：

- `merge_pending_staging` 表示还有待导入的 `staging/*.md`
- 对新增来源 PR，由维护者运行 `/finalize`
- 对直接修改 `data/` 的 PR，确认没有误留 staging 文件
- 其他错误按对应分类处理

## PR Check 失败

`check-pr` 聚合 schema、repo 和 staging 检查。

处理方式：

- 先修 error，再看 warning
- 如果失败摘要里信息不够，运行 `uv run python ./scripts/youpu check-pr --format json`
- 根据 diagnostics 的 `path` 定位具体文件

## 相关文档

- 贡献指南：[../guides/contributor.md](../guides/contributor.md)
- 维护者指南：[../guides/maintainer.md](../guides/maintainer.md)
- CLI 接口说明：[../reference/cli.md](../reference/cli.md)
- accepted 规范：[../specs/accepted.md](../specs/accepted.md)

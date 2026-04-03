# 常见失败与处理方式

这份文档面向贡献者和维护者，说明内容 PR 中最常见的失败情况、返回结果和处理方式。

默认流程是：

1. 贡献者把候选内容放进 `staging/`
2. 提交 PR
3. `check-pr` 自动运行
4. 根据反馈修正内容
5. `check-pr` 通过后，由维护者触发 `/ingest`

只要 `staging/` 中还存在任何 `error`，`check-pr` 就会失败，`./scripts/youpu ingest` 也不会执行正式写入。

## 看哪里

出现失败时，优先看这两个地方：

- PR 的 `check-pr` 结果
- 失败任务日志里的 `ERROR:` 行

每条错误通常都会带：

- `message`：错误说明
- `path`：对应文件或 CSV 行
- `code`：稳定错误码

## accepted Markdown 常见失败

### 1. 文件名不合法

常见现象：

- `check-pr` 失败
- 报错 `staging_accepted_invalid_filename`

常见原因：

- 文件名里有空格、下划线、大写字母或其他特殊字符
- 文件名写成了正式格式 `SRC-####-slug.md`

处理方式：

- 把文件名改成简短、可读、全小写的 slug
- 只使用小写字母、数字和连字符 `-`
- 不要自己写 `SRC-####-`

例如：

- 合法：`kanripo-daozang-index.md`
- 不合法：`SRC-0001-kanripo.md`
- 不合法：`Kanripo Daozang.md`

### 2. Markdown 无法解析

常见现象：

- `check-pr` 失败
- 报错 `staging_accepted_parse_error`

常见原因：

- 文件开头不是 `---`
- 缺少 closing `---`
- front matter 中存在无法解析的字段行

处理方式：

- 按 accepted 模板补齐 front matter
- 确保文件以 `---` 开始，并用第二个 `---` 结束 front matter

### 3. 缺少必填字段

常见现象：

- `staging_accepted_missing_field`

常见字段：

- `title`
- `summary`
- `canonical_url`
- `publisher`
- `modality`
- `access_level`
- `tags`（可选）

处理方式：

- 根据 [`accepted 规范`](../specs/accepted.md) 补齐字段
- 不要留空字符串

### 4. 使用了不属于 accepted schema 的字段

常见现象：

- `staging_accepted_unknown_field`

常见原因：

- 写入了 `id`、`period`、`created_at` 等不属于 accepted schema 的字段
- 字段名拼写错误，导致系统无法识别

处理方式：

- 删除报错里指出的字段
- 只保留 accepted 规范中的核心字段

### 5. `tags` 不是合法数组格式

常见现象：

- `staging_accepted_invalid_array`

处理方式：

- 改成单行数组格式，例如 `tags: [敦煌, 壁画]`
- 不要写成逗号分隔纯文本，也不要写成长句

### 6. `modality` 或 `access_level` 取值不合法

常见现象：

- `staging_accepted_invalid_enum`

处理方式：

- 改成 accepted 规范里定义的枚举值
- 不要自造近义词或中文值

### 7. `canonical_url` 非法

常见现象：

- `staging_accepted_invalid_canonical_url`

常见原因：

- 不是绝对 URL
- 缺少协议或域名

处理方式：

- 改成完整链接
- 用户输入可以是原始 URL；系统会在校验和入库时自动规范化

### 8. accepted 候选与现有正式记录冲突

常见现象：

- `staging_accepted_conflict_accepted`
- `staging_accepted_conflict_rejected`

含义：

- 该 `canonical_url` 规范化后已经存在于正式 `data/accepted/`
- 或已经存在于正式 `data/rejected.csv`

处理方式：

- 先确认这是不是同一个来源
- 如果是重复提交，删除导入文件
- 如果结论需要调整，先让维护者处理正式区，再重新提交

### 9. 同一个 PR 里 accepted 候选重复

常见现象：

- `staging_accepted_duplicate_canonical_url`

处理方式：

- 删掉重复文件
- 或把重复候选合并成一个文件

## staging/rejected/rows.csv 常见失败

### 9. rejected 文件名不对

常见现象：

- `staging_unexpected_file`

常见原因：

- 写成了 `staging/reject.csv`
- 写成了 `staging/rejected.csv`

处理方式：

- 文件路径必须固定为 `staging/rejected/rows.csv`

### 10. staging 里出现了不支持的文件

常见现象：

- `staging_unexpected_file`

常见原因：

- `staging/` 下放了不受支持的文件或目录

处理方式：

- `staging/` 只保留 `staging/accepted/*.md` 和 `staging/rejected/rows.csv`
- 删除其余文件

### 11. staging/rejected/rows.csv 表头错误

常见现象：

- `staging_rejected_invalid_header`

处理方式：

- 表头必须固定为：

```csv
url,title,reason
```

- 列顺序也要一致

### 12. staging/rejected/rows.csv 某一行缺字段

常见现象：

- `staging_rejected_missing_url`
- `staging_rejected_missing_title`
- `staging_rejected_missing_reason`

处理方式：

- 根据报错行号补齐对应列

### 13. staging/rejected/rows.csv 里的 URL 非法

常见现象：

- `staging_rejected_invalid_url`

处理方式：

- 改成合法绝对 URL
- 输入时可以先写原始 URL；系统会在入库时自动规范化

### 14. staging/rejected/rows.csv 内部重复

常见现象：

- `staging_rejected_duplicate_url`

含义：

- 同一个 `staging/rejected/rows.csv` 中，规范化后的 URL 重复出现

处理方式：

- 删掉重复行
- 同一个来源只保留一条 rejected 记录

### 15. rejected 候选与正式区冲突

常见现象：

- `staging_rejected_conflict_rejected`
- `staging_rejected_conflict_accepted`

含义：

- 该 URL 已经存在于正式 `data/rejected.csv`
- 或已存在于正式 `data/accepted/`

处理方式：

- 如果只是重复提交，删除该行
- 如果结论真的需要变更，先让维护者处理正式区，再重新提交

## 正式区常见失败

### 16. 正式 `data/accepted/` 本身不合法

常见现象：

- `check-pr` 失败，但 `staging/` 看起来没问题
- 日志里出现 `accepted_*` 错误码

含义：

- 正式区已有结构错误或字段错误

处理方式：

- 这类问题通常由维护者处理
- 先修正式区，再继续处理内容 PR

### 17. 正式 `data/rejected.csv` 本身不合法

常见现象：

- `rejected_invalid_header`
- `rejected_missing_url`
- `rejected_invalid_url`
- `rejected_duplicate_url`

说明：

- 如果 `data/rejected.csv` 根本不存在，当前会被视为空表，不会单独报错
- 只有文件已存在但内容不合法时，才会出现这些错误

处理方式：

- 由维护者修正正式 `data/rejected.csv`
- 修完后重新运行 `check-pr`

### 18. 正式区 accepted 和 rejected 互相冲突

常见现象：

- `cross_url_conflict`

含义：

- 同一个规范化后的 URL 同时出现在 `data/accepted/` 和 `data/rejected.csv`

处理方式：

- 维护者需要先决定最终结论
- 正式区只能保留一边

### 19. accepted 标题重复

常见现象：

- `accepted_duplicate_title`

当前行为：

- 这是 `warning`，不是 `error`
- 它不会单独阻塞 `check-merge`

处理方式：

- 如果确实是不同来源但标题相同，可以先保留
- 如果是重复记录，维护者应合并或删除其一

## `/ingest` 常见失败

### 20. `/ingest` 没反应

常见原因：

- 评论位置不对

### 21. staging 为空

常见现象：

- `staging_empty`

含义：

- 当前 `staging/` 中没有任何 accepted 候选
- 也没有任何 rejected 候选
- 仓库本身仍然可以是合法的，但这不是一个可 ingest 的新增候选 PR

处理方式：

- 如果这是新增来源 PR，就补充 `staging/accepted/*.md` 或 `staging/rejected/rows.csv`
- 如果这是修改或删除正式记录的 PR，就不应该再依赖 staging 流程

### 22. schema 和 template 不一致

常见现象：

- `accepted_schema_invalid`
- `rejected_schema_invalid`
- `accepted_template_field_order_mismatch`
- `rejected_template_header_mismatch`

含义：

- `schemas/accepted.json` 或 `schemas/rejected.json` 结构不合法
- 或 `templates/accepted.md` / `templates/rejected.rows.csv` 没有和 schema 保持一致

处理方式：

- 先运行 `./scripts/youpu validate-schema`
- 先修 schema，再修 template
- 不要只改模板而忘记同步 schema

正确操作：

- 在 PR 的 `Conversation` 页签里发一条新的顶层评论
- 确认 workflow 已经在默认分支生效

```text
/ingest
```

### 23. `/ingest` 被触发但失败

常见原因：

- `check-pr` 其实还没通过
- PR 分支里仍然有不合法 staging 内容
- 评论者没有足够权限

处理方式：

- 先修完 `check-pr` 报错
- 确认评论者有 `write`、`maintain` 或 `admin`
- 再重新评论 `/ingest`

### 24. `/ingest` 后没有正式结果

只要存在任何 `error`，`./scripts/youpu ingest` 就不会做部分导入。

这意味着：

- 不会只导入合法部分
- 不会自动跳过错误部分继续写正式区

处理方式：

- 先把所有 `error` 修完
- 等 `check-pr` 全绿后再 `/ingest`

## `check-merge` 常见失败

### 25. 提示还有 pending staging

常见现象：

- `merge_pending_staging`

含义：

- `staging/accepted/*.md` 或 `staging/rejected/rows.csv` 还存在

处理方式：

- 对内容 PR，先让维护者执行 `/ingest`
- `/ingest` 成功后，这些输入会被清掉

## 一般处理顺序

当 PR 失败时，建议按这个顺序处理：

1. 先看 `check-pr` 的第一条 `ERROR`
2. 按 `path` 找到对应文件或 CSV 行
3. 修完后重新 push
4. 等 `check-pr` 重新运行
5. 全绿后再让维护者执行 `/ingest`

## 相关文档

- [accepted 规范](../specs/accepted.md)
- [rejected 规范](../specs/rejected.md)
- [URL 规范](../specs/url.md)
- [维护者指南](../guides/maintainer.md)

# 常见失败与处理方式

这份文档面向贡献者和维护者，说明内容 PR 中最常见的失败情况、返回结果和处理方式。

默认流程是：

1. 贡献者把候选内容放进 `imports/`
2. 提交 PR
3. `check-pr` 自动运行
4. 根据反馈修正内容
5. `check-pr` 通过后，由维护者触发 `/ingest`

只要 `imports/` 中还存在任何 `error`，`check-pr` 就会失败，`youpu ingest` 也不会执行正式写入。

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
- 报错 `import_accepted_invalid_filename`

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
- 报错 `import_accepted_parse_error`

常见原因：

- 缺少 ```yaml fenced block
- Markdown 结构被破坏

处理方式：

- 按 accepted 模板补齐文档结构
- 确保文件包含 H1 和 ```yaml 代码块

### 3. 缺少 H1 或 H1 与 YAML `title` 不一致

常见现象：

- `import_accepted_missing_h1`
- `import_accepted_title_mismatch`

处理方式：

- 补上一级标题 `# 标题`
- 保证 H1 与 YAML 里的 `title` 完全一致

### 4. 缺少必填字段

常见现象：

- `import_accepted_missing_field`

常见字段：

- `title`
- `canonical_url`
- `domain`
- `content_type`
- `data_form`
- `data_type`
- `region`
- `source_type`
- `source_org`
- `permissions`
- `tags`
- `use_cases`

处理方式：

- 根据 [`accepted 规范`](../specs/accepted.md) 补齐字段
- 不要留空字符串

### 5. 使用了不再允许的字段

常见现象：

- `import_accepted_disallowed_field`

常见原因：

- 仍然写了 `id`、`subtitle`、`period`、`created_at` 等不属于 accepted 当前 schema 的字段

处理方式：

- 删除报错里指出的字段
- 只保留 accepted 规范中的核心字段

### 6. `tags` 或 `use_cases` 不是数组格式

常见现象：

- `import_accepted_invalid_array`

处理方式：

- 改成单行数组格式

例如：

```yaml
tags: [敦煌, 壁画]
use_cases: [研究分析, AI训练]
```

### 7. `canonical_url` 非法

常见现象：

- `import_accepted_invalid_canonical_url`

常见原因：

- 不是绝对 URL
- 缺少协议或域名

处理方式：

- 改成完整链接
- 用户输入可以是原始 URL；系统会在校验和入库时自动规范化

### 8. accepted 候选与现有正式记录冲突

常见现象：

- `import_accepted_conflict_accepted`
- `import_accepted_conflict_rejected`

含义：

- 该 `canonical_url` 规范化后已经存在于正式 `accepted/`
- 或已经存在于正式 `rejected.csv`

处理方式：

- 先确认这是不是同一个来源
- 如果是重复提交，删除导入文件
- 如果结论需要调整，先让维护者处理正式区，再重新提交

### 9. 同一个 PR 里 accepted 候选重复

常见现象：

- `import_accepted_duplicate_canonical_url`

处理方式：

- 删掉重复文件
- 或把重复候选合并成一个文件

## rejected.csv 常见失败

### 10. rejected 文件名不对

常见现象：

- `import_unexpected_file`

常见原因：

- 写成了 `imports/reject.csv`
- 写成了 `imports/rejected-list.csv`

处理方式：

- 文件名必须固定为 `imports/rejected.csv`

### 11. imports 里出现了不支持的文件

常见现象：

- `import_unexpected_file`

常见原因：

- `imports/` 下放了 `.txt`、`.json`、子目录内文件或其他临时文件

处理方式：

- `imports/` 只保留：
  - 根目录下的 `*.md`
  - `imports/rejected.csv`
- 删除其余文件

### 12. rejected.csv 表头错误

常见现象：

- `import_rejected_invalid_header`

处理方式：

- 表头必须固定为：

```csv
url,title,reason
```

- 列顺序也要一致

### 13. rejected.csv 某一行缺字段

常见现象：

- `import_rejected_missing_url`
- `import_rejected_missing_title`
- `import_rejected_missing_reason`

处理方式：

- 根据报错行号补齐对应列

### 14. rejected.csv 里的 URL 非法

常见现象：

- `import_rejected_invalid_url`

处理方式：

- 改成合法绝对 URL
- 输入时可以先写原始 URL；系统会在入库时自动规范化

### 15. rejected.csv 内部重复

常见现象：

- `import_rejected_duplicate_url`

含义：

- 同一个 `imports/rejected.csv` 中，规范化后的 URL 重复出现

处理方式：

- 删掉重复行
- 同一个来源只保留一条 rejected 记录

### 16. rejected 候选与正式区冲突

常见现象：

- `import_rejected_conflict_rejected`
- `import_rejected_conflict_accepted`

含义：

- 该 URL 已经存在于正式 `rejected.csv`
- 或已存在于正式 `accepted/`

处理方式：

- 如果只是重复提交，删除该行
- 如果结论真的需要变更，先让维护者处理正式区，再重新提交

## 正式区常见失败

### 17. 正式 `accepted/` 本身不合法

常见现象：

- `check-pr` 失败，但 `imports/` 看起来没问题
- 日志里出现 `accepted_*` 错误码

含义：

- 当前正式区已有结构错误或字段错误

处理方式：

- 这类问题通常由维护者处理
- 先修正式区，再继续处理内容 PR

### 18. 正式 `rejected.csv` 本身不合法

常见现象：

- `rejected_invalid_header`
- `rejected_missing_url`
- `rejected_invalid_url`
- `rejected_duplicate_url`

处理方式：

- 由维护者修正正式 `rejected.csv`
- 修完后重新运行 `check-pr`

### 19. 正式区 accepted 和 rejected 互相冲突

常见现象：

- `cross_url_conflict`

含义：

- 同一个规范化后的 URL 同时出现在 `accepted/` 和 `rejected.csv`

处理方式：

- 维护者需要先决定最终结论
- 正式区只能保留一边

### 20. accepted 标题重复

常见现象：

- `accepted_duplicate_title`

当前行为：

- 这是 `warning`，不是 `error`
- 它不会单独阻塞 `check-merge`

处理方式：

- 如果确实是不同来源但标题相同，可以先保留
- 如果是重复记录，维护者应合并或删除其一

## `/ingest` 常见失败

### 21. `/ingest` 没反应

常见原因：

- 评论位置不对
- 不是一条新的顶层评论
- workflow 尚未在默认分支生效

正确操作：

- 在 PR 的 `Conversation` 页签里发一条新的顶层评论

```text
/ingest
```

### 22. `/ingest` 被触发但失败

常见原因：

- `check-pr` 其实还没通过
- PR 分支里仍然有不合法 imports 内容
- 评论者没有足够权限

处理方式：

- 先修完 `check-pr` 报错
- 确认评论者有 `write`、`maintain` 或 `admin`
- 再重新评论 `/ingest`

### 23. `/ingest` 后没有正式结果

当前实现下，只要存在任何 `error`，`youpu ingest` 就不会做部分导入。

这意味着：

- 不会只导入合法部分
- 不会自动跳过错误部分继续写正式区

处理方式：

- 先把所有 `error` 修完
- 等 `check-pr` 全绿后再 `/ingest`

## `check-merge` 常见失败

### 24. 提示还有 pending imports

常见现象：

- `merge_pending_imports`

含义：

- `imports/*.md` 或 `imports/rejected.csv` 还存在

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
- [维护者操作手册](maintainer-guide.md)

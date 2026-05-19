# 贡献指南

这份文档面向仓库使用者，说明在 `youpu-sources` 中如何做新增、修改和删除。

先记住一条总规则：

- 新增：走 `staging/`
- 修改：直接改 `data/`
- 删除：直接改 `data/`

不要把已有正式记录复制到 `staging/` 里尝试“覆盖更新”。`staging/` 只用于新增候选输入，不用于修改或删除正式记录。

## 目录角色

- `staging/*.md`：新增 accepted 候选
- `data/`：正式 accepted 记录

`staging/` 中出现非 Markdown 文件或子目录时，检查会失败。

## 场景 1：新增 accepted

适用情况：

- 你发现了一个新的、应当收录的数据集来源

操作方式：

1. 在 `staging/` 新建一个 Markdown 文件
2. 按 accepted 规范填写内容
3. 提交 PR
4. 等待 `check-pr`
5. 检查通过后，由维护者执行 `/finalize`

注意：

- 文件名不能使用正式区的 `SRC-####-slug.md`
- 文件名会作为正式文件名中的 `slug` 使用，必须由你自己命名
- 文件名只能使用英文小写字母、数字和连字符 `-`，不得包含中文字符
- YAML 中必须包含 `summary`
- 如果 `canonical_url` 已经存在于正式区，检查会失败

系统在正式入库时只会自动补上 `SRC-####` 编号前缀，不会替你生成、翻译或修改后面的 `slug`。

## 场景 2：修改已有 accepted

适用情况：

- 你要修正文案
- 你要补字段
- 你要修正 `canonical_url`
- 你要更新正文说明

操作方式：

1. 新建分支
2. 直接修改 `data/` 中对应文件
3. 提交 PR
4. 等待 `check-pr` 和 `check-merge`

注意：

- 不要把正式文件复制到 `staging/`
- 如果复制到 staging，系统会把它视为“新增候选”，而不是“修改正式记录”
- 如果保留相同 `canonical_url`，通常会被判定为与正式区冲突

## 场景 3：删除正式记录

适用情况：

- 某条 accepted 记录应当被移除

操作方式：

1. 新建分支
2. 直接删除 `data/` 中对应 Markdown 文件
3. 提交 PR
4. 在 PR 描述中说明删除原因
5. 等待 `check-pr` 和 `check-merge`

## 系统会做什么

对新增流程：

- `check-pr` 会检查正式区与 staging
- `check-merge` 也会自动运行；只要 `staging/` 里还有待处理内容，它会失败并提示 `merge_pending_staging`
- `/finalize` 会在需要时执行 ingest，把合法的 staging 输入写入正式区
- `/finalize` 成功后会清空已处理的 staging 输入，并再次确认当前分支可合并

对修改和删除流程：

- 不需要 ingest
- `check-pr` 会检查正式区是否合法
- `check-merge` 会确认当前分支可合并

## 维护者入口

维护者统一使用下面的评论命令：

```text
/finalize
```

行为说明：

- 如果没有 `staging/*.md` 候选，系统不会执行 ingest，只会验证当前分支是否可合并
- 如果存在 `staging/*.md` 候选，系统会先校验，再执行 ingest，再验证最终是否可合并

## 什么时候不要用 staging

以下情况都不应该使用 `staging/`：

- 修改已有 accepted
- 删除正式记录
- 想“覆盖”正式区中的现有来源

这些情况都应直接修改 `data/`。

## 相关文档

- README：[../../README.md](../../README.md)
- 常见失败与处理方式：[../operations/failures.md](../operations/failures.md)
- 维护者操作手册：[maintainer.md](maintainer.md)
- accepted 规范：[../specs/accepted.md](../specs/accepted.md)
- URL 规范：[../specs/url.md](../specs/url.md)

# 贡献指南

这份文档面向仓库使用者，说明在 `youpu-sources` 中如何做新增、修改和删除。

先记住一条总规则：

- 新增：走 `staging/`
- 修改：直接改 `data/`
- 删除：直接改 `data/`

不要把已有正式记录复制到 `staging/` 里尝试“覆盖更新”。`staging/` 只用于新增候选输入，不用于修改或删除正式记录。

## 目录角色

- `staging/accepted/*.md`：新增 accepted 候选
- `staging/rejected/rows.csv`：新增 rejected 候选
- `data/accepted/`：正式 accepted 记录
- `data/rejected.csv`：正式 rejected 记录

## 场景 1：新增 accepted

适用情况：

- 你发现了一个新的、应当收录的数据集来源

操作方式：

1. 在 `staging/accepted/` 新建一个 Markdown 文件
2. 按 accepted 规范填写内容
3. 提交 PR
4. 等待 `check-pr`
5. 检查通过后，由维护者执行 `/ingest`

注意：

- 文件名不能使用正式区的 `SRC-####-slug.md`
- YAML 中必须包含 `subtitle`
- 如果 `canonical_url` 已经存在于正式区，检查会失败

## 场景 2：新增 rejected

适用情况：

- 你发现了一个新的、应当明确拒绝的数据集来源

操作方式：

1. 在 `staging/rejected/rows.csv` 中追加记录
2. 提交 PR
3. 等待 `check-pr`
4. 检查通过后，由维护者执行 `/ingest`

注意：

- staging 中 rejected 的输入文件名固定为 `staging/rejected/rows.csv`
- 如果 URL 已经存在于正式区，检查会失败
- 如果正式区还没有 `data/rejected.csv`，系统会把它视为空表；首次 ingest rejected 候选时会自动创建

## 场景 3：修改已有 accepted

适用情况：

- 你要修正文案
- 你要补字段
- 你要修正 `canonical_url`
- 你要更新正文说明

操作方式：

1. 新建分支
2. 直接修改 `data/accepted/` 中对应文件
3. 提交 PR
4. 等待 `check-pr` 和 `check-merge`

注意：

- 不要把正式文件复制到 `staging/accepted/`
- 如果复制到 staging，系统会把它视为“新增候选”，而不是“修改正式记录”
- 如果保留相同 `canonical_url`，通常会被判定为与正式区冲突

## 场景 4：修改已有 rejected

适用情况：

- 你要修改 `data/rejected.csv` 中已有行的 `title`
- 你要修正 `reason`
- 你要修正 URL

操作方式：

1. 新建分支
2. 直接修改 `data/rejected.csv`
3. 提交 PR
4. 等待 `check-pr` 和 `check-merge`

## 场景 5：删除正式记录

适用情况：

- 某条 accepted 记录应当被移除
- 某条 rejected 记录应当被移除

操作方式：

1. 新建分支
2. 直接在 `data/` 中删除对应记录
3. 提交 PR
4. 在 PR 描述中说明删除原因
5. 等待 `check-pr` 和 `check-merge`

对应删除位置：

- 删除 accepted：删除 `data/accepted/` 中对应 Markdown 文件
- 删除 rejected：删除 `data/rejected.csv` 中对应行

## 系统会做什么

对新增流程：

- `check-pr` 会检查正式区与 staging
- `/ingest` 会把合法的 staging 输入写入正式区
- `/ingest` 成功后会清空已处理的 staging 输入

对修改和删除流程：

- 不需要 `/ingest`
- `check-pr` 会检查正式区是否合法
- `check-merge` 会确认当前分支可合并

## 什么时候不要用 staging

以下情况都不应该使用 `staging/`：

- 修改已有 accepted
- 修改已有 rejected
- 删除正式记录
- 想“覆盖”正式区中的现有来源

这些情况都应直接修改 `data/`。

## 相关文档

- README：[../../README.md](../../README.md)
- 常见失败与处理方式：[../operations/failures.md](../operations/failures.md)
- 维护者操作手册：[maintainer.md](maintainer.md)
- accepted 规范：[../specs/accepted.md](../specs/accepted.md)
- rejected 规范：[../specs/rejected.md](../specs/rejected.md)
- URL 规范：[../specs/url.md](../specs/url.md)

# 维护者操作手册

这份文档面向仓库维护者，说明如何检查 PR、区分新增与正式区修改、触发 `/ingest`、以及在需要时做本地排障。

## 维护者职责

维护者主要负责：

- 审查贡献者提交的 `staging/` 或 `data/` 变更
- 在 PR 检查通过后触发 `/ingest`
- 确认正式区结果无误后合并
- 在需要时本地复现和排查问题

## 日常流程

### 1. 检查内容 PR

先判断 PR 属于哪一类：

- 新增来源：改动发生在 `staging/`
- 修改正式记录：改动直接发生在 `data/`
- 删除正式记录：改动直接发生在 `data/`

新增来源 PR 的正常顺序是：

1. 贡献者把候选内容放进 `staging/`
2. 提交 PR
3. 等待 `check-pr`
4. 根据检查结果修改 PR

维护者在这一阶段主要看：

- 候选内容本身是否合理
- `check-pr` 是否通过
- PR diff 是否只包含本次候选输入
- 如果是 staging PR，`staging/` 里必须真的有候选内容；空 staging PR 会以 `staging_empty` 失败

如果是修改或删除正式记录，维护者应确认：

- 变更直接发生在 `data/`
- PR 没有误把正式文件复制到 `staging/`
- 修改或删除理由明确
- `check-pr` 与 `check-merge` 通过

### 2. 什么时候触发 `/ingest`

只有“新增来源”这类 staging PR 才需要 `/ingest`。

当内容和 PR 检查都没问题后，在 PR 的 `Conversation` 里评论：

```text
/ingest
```

注意：

- 必须发在 PR 的普通评论区
- 必须是一条新的顶层评论
- 评论者需要有 `write`、`maintain` 或 `admin` 权限

### 3. 检查 `/ingest` 结果

`/ingest` 成功后，workflow 会：

1. 再跑一次 `youpu check-pr`
2. 执行 `youpu ingest`
3. 自动提交结果回原分支
4. 执行 `youpu check-merge`

维护者需要确认：

- `staging/accepted/*.md` 和 `staging/rejected/rows.csv` 已被清空
- `data/accepted/` 或 `data/rejected.csv` 的正式结果符合预期
- PR checks 最终为绿色

### 4. 合并 PR

新增来源 PR：

- 在 `/ingest` 结果正确且 `check-merge` 通过后再合并

修改或删除正式记录 PR：

- 不需要 `/ingest`
- 只要 `check-pr` 和 `check-merge` 通过，并且变更理由清楚，即可合并

建议：

- 维护者不要直接 push `main`
- 每次改动都通过 PR 合并
- PR merge 后删除对应分支

## fork PR 的处理

fork PR 只支持检查，不支持自动回写 ingest 结果。

对 fork PR：

1. 让 `check-pr` 正常运行
2. 如果是新增来源且内容值得入库，由维护者把对应输入复制到主仓库内部分支
3. 如果是修改或删除正式记录，由维护者在内部分支直接修改 `data/`
4. 如果是新增来源，再在内部分支 PR 上执行 `/ingest`

## 本地排障

如果需要在本地复现或排查，维护者可以使用：

```bash
youpu validate-schema
youpu validate-repo
youpu validate-imports
youpu check-pr
youpu ingest
youpu check-merge
youpu report
```

常见用途：

- `youpu validate-repo`
  检查正式区
- `youpu validate-imports`
  检查当前 `staging/`
- `youpu validate-schema`
  检查 `schemas/` 与 `templates/` 是否一致
- `youpu check-pr`
  复现 PR 检查
- `youpu ingest`
  本地执行确定性入库
- `youpu check-merge`
  确认当前状态是否可合并
- `youpu report`
  快速查看仓库摘要

如果本次 PR 涉及字段调整、模板调整或 CLI schema 逻辑调整，建议先单独跑一次 `youpu validate-schema`，再看 `check-pr` / `check-merge`。

如果需要继续修改 CLI 实现本身，源码当前位于 `src/youpu/`，并按 `cli / app / domain / infra` 分层；具体见 [source-layout.md](source-layout.md)。

## 相关文档

- 常见失败与处理方式：[failures.md](failures.md)
- 仓库设置：[github-repo-setup.md](github-repo-setup.md)
- 源码结构：[source-layout.md](source-layout.md)
- CLI 用户文档：[../cli/user-guide.md](../cli/user-guide.md)
- CLI 开发接口：[../cli/spec.md](../cli/spec.md)
- 项目边界：[project-scope.md](project-scope.md)

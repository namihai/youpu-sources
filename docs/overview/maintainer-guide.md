# 维护者操作手册

这份文档面向仓库维护者，说明如何检查 PR、触发 `/ingest`、以及在需要时做本地排障。

## 维护者职责

维护者主要负责：

- 审查贡献者提交的 `imports/`
- 在 PR 检查通过后触发 `/ingest`
- 确认正式区结果无误后合并
- 在需要时本地复现和排查问题

## 日常流程

### 1. 检查内容 PR

内容 PR 的正常顺序是：

1. 贡献者把候选内容放进 `imports/`
2. 提交 PR
3. 等待 `check-pr`
4. 根据检查结果修改 PR

维护者在这一阶段主要看：

- 候选内容本身是否合理
- `check-pr` 是否通过
- PR diff 是否只包含本次候选输入

### 2. 触发 `/ingest`

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

- `imports/*.md` 和 `imports/rejected.csv` 已被清空
- `accepted/` 或 `rejected.csv` 的正式结果符合预期
- PR checks 最终为绿色

### 4. 合并 PR

在 `/ingest` 结果正确且 `check-merge` 通过后再合并。

建议：

- 维护者不要直接 push `main`
- 每次改动都通过 PR 合并
- PR merge 后删除对应分支

## fork PR 的处理

fork PR 只支持检查，不支持自动回写 ingest 结果。

对 fork PR：

1. 让 `check-pr` 正常运行
2. 如果内容值得入库，由维护者把对应输入复制到主仓库内部分支
3. 在内部分支 PR 上再执行 `/ingest`

## 本地排障

如果需要在本地复现或排查，维护者可以使用：

```bash
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
  检查当前 `imports/`
- `youpu check-pr`
  复现 PR 检查
- `youpu ingest`
  本地执行确定性入库
- `youpu check-merge`
  确认当前状态是否可合并
- `youpu report`
  快速查看仓库摘要

## 相关文档

- 常见失败与处理方式：[common-failures.md](common-failures.md)
- 仓库设置：[github-repo-setup.md](github-repo-setup.md)
- CLI 用户文档：[../cli/user-guide.md](../cli/user-guide.md)
- CLI 开发接口：[../cli/spec.md](../cli/spec.md)
- 项目边界：[project-scope.md](project-scope.md)

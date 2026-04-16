# GitHub 仓库设置

这份文档说明 `youpu-sources` 在 GitHub 上需要开启哪些设置，才能让当前 PR / CI / `/finalize` 流程正常工作。

## 目标

仓库当前的协作模型是：

- 普通贡献者提交 `staging/`
- PR 自动跑检查
- 维护者评论 `/finalize`
- 内部分支 PR 在需要时自动回写 ingest 结果
- fork PR 只做检查，不自动回写

为了让这个模型稳定工作，GitHub 仓库设置需要与代码和 workflow 保持一致。

## 必要设置

### 1. 开启 GitHub Actions

确认仓库允许运行 GitHub Actions。

如果组织层面对 Actions 做了限制，需要确保以下 action 可用：

- `actions/checkout`
- `astral-sh/setup-uv`
- `actions/github-script`

### 2. 收缩默认分支写权限

如果当前使用的是私有仓库免费方案，不一定能依赖 GitHub 的 branch protection。

这时建议：

- 只给少数维护者保留 `main` 的写权限
- 普通贡献者统一通过 PR 协作
- 团队内部约定不直接 push `main`
- 把 `check-pr` 和 `check-merge` 作为合并前必看结果

### 3. 选择强制检查项

如果当前仓库计划升级到支持 branch protection 的方案，建议至少把以下 workflow 结果设为 required status checks：

- `check-pr`
- `check-merge`

如果当前不使用 branch protection，这一项可以退化为团队约定：维护者只在 `check-pr` 和 `check-merge` 通过后合并。

### 4. 允许 Actions 写回内部分支

`/finalize` workflow 会在内部分支 PR 上按需自动提交 ingest 结果。

因此需要确认：

- `GITHUB_TOKEN` 对仓库内容拥有写权限
- Actions 允许创建提交并 push 到非受保护分支

如果组织策略默认将 `GITHUB_TOKEN` 设为只读，需要为这个仓库单独放开写权限。

## `/finalize` 的使用规则

### 内部分支 PR

以下场景支持自动 `/finalize`：

- PR 来自主仓库分支
- 评论者拥有 `write`、`maintain` 或 `admin` 权限
- 评论内容以 `/finalize` 开头

workflow 会：

1. 再跑一次 `uv run python ./scripts/youpu check-pr`
2. 若 `staging/` 不为空，则执行 `uv run python ./scripts/youpu ingest`
3. 若本次发生写回，则自动提交结果回原分支
4. 执行 `uv run python ./scripts/youpu check-merge`

### fork PR

fork PR 不支持自动回写 finalize 结果。

对 fork PR：

- `pr-check.yml` 和 `merge-check.yml` 仍然会自动检查输入是否合法、当前分支是否可合并
- `/finalize` 会停止并给出提示
- 维护者需要把对应变更转移到内部分支后再执行 `/finalize`

## 推荐团队约定

建议在团队内部约定：

- 内部协作者优先使用主仓库分支，不走 fork
- 外部贡献只负责提交输入，不直接进入自动 ingest 路径
- `/finalize` 只由维护者触发
- 维护者不直接 push `main`
- 合并前优先确认 `check-merge` 的结果

## 非阻塞建议

这些设置不是主流程必须，但值得后续补齐：

- 启用自动删除已合并分支
- 配置 CODEOWNERS
- 根据团队需要补充 PR 模板
- 根据团队需要补充 issue 模板

## 仓库对应文件

- PR 检查 workflow：[../../.github/workflows/pr-check.yml](../../.github/workflows/pr-check.yml)
- Merge 检查 workflow：[../../.github/workflows/merge-check.yml](../../.github/workflows/merge-check.yml)
- `/finalize` workflow：[../../.github/workflows/finalize.yml](../../.github/workflows/finalize.yml)
- 贡献入口：[../../README.md](../../README.md)

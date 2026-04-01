# GitHub Repo Setup

这份文档说明 `youpu-sources` 在 GitHub 上需要开启哪些设置，才能让当前 PR / CI / `/ingest` 流程正常工作。

## 目标

仓库当前的协作模型是：

- 普通贡献者提交 `imports/`
- PR 自动跑检查
- 维护者评论 `/ingest`
- 内部分支 PR 自动回写 ingest 结果
- fork PR 只做检查，不自动回写

为了让这个模型稳定工作，GitHub 仓库设置需要与代码和 workflow 保持一致。

## 必要设置

### 1. 开启 GitHub Actions

确认仓库允许运行 GitHub Actions。

如果组织层面对 Actions 做了限制，需要确保以下 action 可用：

- `actions/checkout`
- `actions/setup-python`
- `actions/github-script`

### 2. 设置默认分支保护

建议对默认分支开启 branch protection，至少包括：

- Require a pull request before merging
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Restrict direct pushes to the default branch

如果团队规模允许，建议再加：

- Require at least 1 approval

### 3. 选择强制检查项

建议至少把以下 workflow 结果设为 required status checks：

- `PR Check / check-pr`

如果后续希望把 ingest 后状态也纳入强制检查，可以再考虑把 `/ingest` 相关结果纳入流程约束。但第一阶段只要求 PR 检查即可。

### 4. 允许 Actions 写回内部分支

`/ingest` workflow 会在内部分支 PR 上自动提交 ingest 结果。

因此需要确认：

- `GITHUB_TOKEN` 对仓库内容拥有写权限
- Actions 允许创建提交并 push 到非受保护分支

如果组织策略默认将 `GITHUB_TOKEN` 设为只读，需要为这个仓库单独放开写权限。

## `/ingest` 的使用规则

### 内部分支 PR

以下场景支持自动 `/ingest`：

- PR 来自主仓库分支
- 评论者拥有 `write`、`maintain` 或 `admin` 权限

workflow 会：

1. 再跑一次 `youpu check-pr`
2. 执行 `youpu ingest`
3. 自动提交结果回原分支
4. 执行 `youpu check-merge`

### fork PR

fork PR 不支持自动回写 ingest 结果。

对 fork PR：

- `pr-check.yml` 仍然会自动检查输入是否合法
- `/ingest` 会停止并给出提示
- 维护者需要把对应 `imports/` 内容转移到内部分支后再执行 `/ingest`

## 推荐团队约定

建议在团队内部约定：

- 内部协作者优先使用主仓库分支，不走 fork
- 外部贡献只负责提交输入，不直接进入自动 ingest 路径
- `/ingest` 只由维护者触发
- 合并前优先确认 `check-merge` 的结果

## 非阻塞建议

这些设置不是主流程必须，但值得后续补齐：

- 启用自动删除已合并分支
- 配置 CODEOWNERS
- 根据团队需要补充 PR 模板
- 根据团队需要补充 issue 模板

## 当前仓库对应文件

- PR 检查 workflow：[/.github/workflows/pr-check.yml](/Users/xianqiu/Projects/youpu-sources/.github/workflows/pr-check.yml)
- `/ingest` workflow：[/.github/workflows/ingest.yml](/Users/xianqiu/Projects/youpu-sources/.github/workflows/ingest.yml)
- 贡献入口：[README.md](/Users/xianqiu/Projects/youpu-sources/README.md)

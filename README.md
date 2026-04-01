# youpu-sources

`youpu-sources` 用来维护一份可靠、可持续整理的数据集来源清单。

这个仓库只保存两类已经有明确结论的记录：

- `accepted/`：确认保留的数据集来源
- `rejected/rejected.csv`：确认不保留的数据集来源

这个仓库不保存数据集文件本身，也不负责帮你发现外部来源。

## 贡献流程

这个仓库的主流程是：

1. 把候选内容放进 `imports/`
2. 提交 Pull Request
3. 等待 GitHub Actions 自动检查
4. 根据 CI 反馈修改内容
5. 由维护者在 PR 中触发 `/ingest`
6. 审查最终入库结果并合并

普通贡献者不需要依赖本地命令行完成主流程。

适用范围：

- 内部协作者：推荐直接在主仓库分支上提交 PR，支持自动 `/ingest`
- 外部协作者：可以提交 fork PR 做输入检查，但正式 ingest 由维护者转到内部分支接管

## 你需要提交什么

把候选内容放到默认导入目录：

```text
imports/
  accepted/
  rejected/
```

- 放进 `imports/accepted/` 的内容，表示你希望它进入 `accepted/`
- 放进 `imports/rejected/` 的内容，表示你希望它进入 `rejected/rejected.csv`

如果你不确定格式是否正确，先看：

- [`docs/specs/accepted.md`](docs/specs/accepted.md)
- [`docs/specs/rejected.md`](docs/specs/rejected.md)
- [`docs/specs/url.md`](docs/specs/url.md)

## PR 中会发生什么

当你提交 PR 后，系统会自动执行检查：

- 校验正式区 `accepted/` 和 `rejected/`
- 校验 `imports/` 中的候选内容
- 报出格式问题、重复和冲突

如果检查失败，你只需要根据反馈修改 PR。

当 PR 检查通过后，维护者会在 PR 中评论：

```text
/ingest
```

这个动作会触发受控 workflow：

1. 再次执行 PR 检查
2. 运行 `youpu ingest`
3. 把正式区变更提交回该 PR 分支
4. 运行合并前检查

说明：

- 只有主仓库内部分支 PR 支持自动回写
- fork PR 仍然可以跑检查
- 如果 fork PR 需要正式入库，维护者应将对应 `imports/` 内容转移到内部分支后再执行 `/ingest`

## 目录职责

仓库中几个主要目录的职责如下：

- `imports/`：待处理输入区
- `accepted/`：正式保留记录
- `rejected/`：正式拒绝记录
- `templates/`：候选内容模板
- `docs/`：详细文档

`imports/` 不是归档区。内容一旦被成功 ingest，对应输入文件就应从 `imports/` 中移除。

## 维护者接口

`youpu` 是仓库规则内核，主要供 GitHub Actions 和维护者使用。

维护者通常会用到：

- `youpu check-pr`
- `youpu ingest`
- `youpu check-merge`

## 去哪里看详细说明

- 文档总入口：[docs/index.md](docs/index.md)
- 项目边界：[docs/overview/project-scope.md](docs/overview/project-scope.md)
- GitHub 仓库设置：[docs/overview/github-repo-setup.md](docs/overview/github-repo-setup.md)
- CLI 用户文档：[docs/cli/user-guide.md](docs/cli/user-guide.md)
- CLI 开发接口：[docs/cli/spec.md](docs/cli/spec.md)
- accepted 规范：[docs/specs/accepted.md](docs/specs/accepted.md)
- rejected 规范：[docs/specs/rejected.md](docs/specs/rejected.md)
- URL 规范：[docs/specs/url.md](docs/specs/url.md)

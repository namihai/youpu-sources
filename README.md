# youpu-sources

`youpu-sources` 用来维护一份可靠、可持续整理的数据集来源清单。

这个仓库只保存两类已经有明确结论的记录：

- `accepted/`：确认保留的数据集来源
- `rejected.csv`：确认不保留的数据集来源

这个仓库不保存数据集文件本身，也不负责帮你发现外部来源。

## 贡献流程

普通贡献者的主流程是：

1. 把候选内容放进 `imports/`
2. 提交 Pull Request
3. 等待 GitHub Actions 自动检查
4. 根据 CI 反馈修改内容
5. 等维护者完成入库和合并

普通贡献者不需要依赖本地命令行完成主流程。

## 你需要提交什么

把候选内容放到默认导入目录：

```text
imports/
  *.md
  rejected.csv
```

- 放进 `imports/*.md` 的内容，表示你希望它进入 `accepted/`
- 放进 `imports/rejected.csv` 的内容，表示你希望它进入 `rejected.csv`

`imports/` 只接收两类输入：根目录下的候选 accepted Markdown，以及固定文件名 `imports/rejected.csv`。

如果你不确定格式是否正确，先看：

- [`docs/specs/accepted.md`](docs/specs/accepted.md)
- [`docs/specs/rejected.md`](docs/specs/rejected.md)
- [`docs/specs/url.md`](docs/specs/url.md)

## PR 中会发生什么

当你提交 PR 后，系统会自动执行检查：

- 校验正式区 `accepted/` 和 `rejected.csv`
- 校验 `imports/` 中的候选内容
- 报出格式问题、重复和冲突

如果检查失败，你只需要根据反馈修改 PR。

PR 检查通过后，维护者会接手后续入库和合并。

## 目录职责

仓库中几个主要目录的职责如下：

- `imports/`：待处理输入区
- `accepted/`：正式保留记录
- `rejected.csv`：正式拒绝记录
- `templates/`：候选内容模板
- `docs/`：详细文档

`imports/` 不是归档区。内容一旦被成功 ingest，对应输入文件就应从 `imports/` 中移除。

## 去哪里看详细说明

- 文档总入口：[docs/index.md](docs/index.md)
- 维护者操作手册：[docs/overview/maintainer-guide.md](docs/overview/maintainer-guide.md)
- 项目边界：[docs/overview/project-scope.md](docs/overview/project-scope.md)
- GitHub 仓库设置：[docs/overview/github-repo-setup.md](docs/overview/github-repo-setup.md)
- CLI 用户文档：[docs/cli/user-guide.md](docs/cli/user-guide.md)
- CLI 开发接口：[docs/cli/spec.md](docs/cli/spec.md)
- accepted 规范：[docs/specs/accepted.md](docs/specs/accepted.md)
- rejected 规范：[docs/specs/rejected.md](docs/specs/rejected.md)
- URL 规范：[docs/specs/url.md](docs/specs/url.md)

# youpu-sources

`youpu-sources` 用来维护一份可靠、可持续整理的数据集来源清单。

这个仓库只保存两类已经有明确结论的记录：

- `data/accepted/`：确认保留的数据集来源
- `data/rejected.csv`：确认不保留的数据集来源

同时，仓库使用配置化 schema 描述 accepted / rejected 的结构：

- `schemas/accepted.json`
- `schemas/rejected.json`

这个仓库不保存数据集文件本身，也不负责帮你发现外部来源。

## 快速开始

先区分三种操作：

- 新增：使用 `staging/`
- 修改：直接改 `data/`
- 删除：直接改 `data/`

新增 accepted / rejected 时，把候选内容放到默认导入目录：

```text
staging/
  accepted/
    *.md
  rejected/
    rows.csv
```

- 放进 `staging/accepted/*.md` 的内容，表示你希望它进入 `data/accepted/`
- 放进 `staging/rejected/rows.csv` 的内容，表示你希望它进入 `data/rejected.csv`

`staging/` 只接收两类输入：`staging/accepted/` 下的候选 accepted Markdown，以及固定文件名 `staging/rejected/rows.csv`。

如果你要修改或删除已有正式记录，不要使用 `staging/`，而是直接在分支中修改 `data/` 后提交 PR。

## 测试

运行当前 CLI 回归测试：

```bash
make test
```

## 进一步阅读

完整流程见：

- [操作手册](docs/overview/contributor-guide.md)
- [常见失败与处理方式](docs/overview/failures.md)
- [accepted 规范](docs/specs/accepted.md)
- [rejected 规范](docs/specs/rejected.md)
- [schema 规范](docs/specs/schema.md)
- [URL 规范](docs/specs/url.md)

## 去哪里看详细说明

- 文档总入口：[docs/index.md](docs/index.md)
- 操作手册：[docs/overview/contributor-guide.md](docs/overview/contributor-guide.md)
- 常见失败与处理方式：[docs/overview/failures.md](docs/overview/failures.md)
- 维护者操作手册：[docs/overview/maintainer-guide.md](docs/overview/maintainer-guide.md)
- 项目边界：[docs/overview/project-scope.md](docs/overview/project-scope.md)
- GitHub 仓库设置：[docs/overview/github-repo-setup.md](docs/overview/github-repo-setup.md)
- CLI 用户文档：[docs/cli/user-guide.md](docs/cli/user-guide.md)
- CLI 开发接口：[docs/cli/spec.md](docs/cli/spec.md)
- accepted 规范：[docs/specs/accepted.md](docs/specs/accepted.md)
- rejected 规范：[docs/specs/rejected.md](docs/specs/rejected.md)
- schema 规范：[docs/specs/schema.md](docs/specs/schema.md)
- URL 规范：[docs/specs/url.md](docs/specs/url.md)

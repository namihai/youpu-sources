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

推荐先使用 `uv` 创建并管理本地环境：

```bash
uv venv --python 3.14.4
uv run python ./scripts/youpu report
```

如果你只是来提交新的来源记录，不需要修改项目代码，也不要直接 push 到 `main`。

按下面的步骤操作即可：

1. 从 `main` 新建一个工作分支，不要直接在 `main` 上提交
2. 给分支起一个简单名字
3. 把你的内容放进 `staging/`
4. 提交分支并创建 PR
5. 在 PR 描述里说明你这次新增了什么，以及需要更新哪些记录
6. 等待仓库检查通过，再由维护者执行 `/finalize`

PR 描述可以直接按下面的格式填写：

```text
本次新增：
- 来源名称：<名称>
- 网址：<URL>
- 更新内容：<这次补充了哪些 accepted / rejected 记录>
- 说明：<为什么要新增这些记录>
```

推荐分支命名：

- 新增来源：`add/source-来源简名`

命名尽量使用简短英文、小写、连字符，例如：

- `add/source-openalex`
- `add/source-huggingface-dataset`
- `add/source-example-dataset`

如果你手上还是未标准化的原始文档，可以先放在 `incoming/`：

- `incoming/` 只用于本地暂存未标准化材料，不参与校验、导入或追踪
- 整理完成后，再把内容移动到 `staging/`

内容请放到下面的默认导入目录：

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

放置方式：

- 新增来源时，按需要在 `staging/accepted/` 新建 Markdown 文件
- 新增来源时，按需要把记录追加到 `staging/rejected/rows.csv`
- 如果一次提交同时涉及两边，就在同一个分支里一起更新

`staging/accepted/*.md` 的文件名会作为正式文件名中的 `slug` 使用。请自行使用英文小写字母、数字和连字符命名，不要包含中文字符，也不要写 `SRC-####-`；系统正式入库时只自动补编号前缀。

如果你要修改或删除已有正式记录，不要使用 `staging/`，而是直接在分支中修改 `data/` 后提交 PR。详细规则见操作手册。

## 进一步阅读

完整流程见：

- [操作手册](docs/guides/contributor.md)
- [常见失败与处理方式](docs/operations/failures.md)
- [accepted 规范](docs/specs/accepted.md)
- [rejected 规范](docs/specs/rejected.md)
- [schema 规范](docs/specs/schema.md)
- [URL 规范](docs/specs/url.md)

## 去哪里看详细说明

- 文档总入口：[docs/index.md](docs/index.md)
- 操作手册：[docs/guides/contributor.md](docs/guides/contributor.md)
- 常见失败与处理方式：[docs/operations/failures.md](docs/operations/failures.md)
- 维护者操作手册：[docs/guides/maintainer.md](docs/guides/maintainer.md)
- 项目边界：[docs/architecture/project-boundary.md](docs/architecture/project-boundary.md)
- GitHub 仓库设置：[docs/operations/github-setup.md](docs/operations/github-setup.md)
- CLI 接口说明：[docs/reference/cli.md](docs/reference/cli.md)
- accepted 规范：[docs/specs/accepted.md](docs/specs/accepted.md)
- rejected 规范：[docs/specs/rejected.md](docs/specs/rejected.md)
- schema 规范：[docs/specs/schema.md](docs/specs/schema.md)
- URL 规范：[docs/specs/url.md](docs/specs/url.md)

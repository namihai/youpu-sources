# youpu-sources

`youpu-sources` 用来维护一份可靠、可持续整理的数据集来源清单。

这个仓库只保存两类已经有明确结论的记录：

- `accepted/`：确认保留的数据集来源
- `rejected/rejected.csv`：确认不保留的数据集来源

如果你只是想开始使用，这个页面就够了；更详细的说明都放在 [`docs/index.md`](/Users/xianqiu/Projects/youpu-sources/docs/index.md)。

## 你可以用它做什么

- 把你整理好的候选记录放进导入目录
- 先检查这些候选记录能不能进入正式仓库
- 只把符合规范、没有冲突的内容合并进去
- 在提交前再做一次完整检查

这个仓库不保存数据集文件本身，也不负责帮你发现外部来源。

## Quickstart

### 1. 准备候选内容

把要导入的内容放到默认导入目录：

```text
imports/
  accepted/
  rejected/
```

- 放进 `imports/accepted/` 的内容，表示你希望它进入 `accepted/`
- 放进 `imports/rejected/` 的内容，表示你希望它进入 `rejected/rejected.csv`

如果你不确定文件格式是否正确，先看详细规范：

- [`docs/specs/accepted.md`](/Users/xianqiu/Projects/youpu-sources/docs/specs/accepted.md)
- [`docs/specs/rejected.md`](/Users/xianqiu/Projects/youpu-sources/docs/specs/rejected.md)

### 2. 使用 skill 检查导入内容

推荐直接使用 `youpu-gatekeeper` 这项 skill，用自然语言发出请求，例如：

```text
检查 imports
```

skill 会先做导入前检查，并告诉你：

- 哪些内容可以导入
- 哪些内容有格式问题
- 哪些内容与现有记录冲突

如果你需要了解这项 skill 的边界和行为，见 [`docs/skills/youpu-gatekeeper.md`](/Users/xianqiu/Projects/youpu-sources/docs/skills/youpu-gatekeeper.md)。

### 3. 处理问题清单

如果有不能导入的内容，可以查看：

- [`imports/reports/issues.md`](/Users/xianqiu/Projects/youpu-sources/imports/reports/issues.md)

这个文件会告诉你：

- 哪些内容可以导入
- 哪些内容有格式问题
- 哪些内容与现有记录冲突

### 4. 让 skill 执行导入

确认没有问题后，可以直接对 skill 说：

```text
导入 imports 里的内容
```

skill 会先检查，再执行导入。只有符合规范的内容才会被合并进正式仓库。

### 5. 导入后再做一次检查

你可以继续让 skill 做一次仓库检查，例如：

```text
检查仓库
```

或者：

```text
做一次提交前检查
```

### 6. 提交前检查

如果你准备提交，也可以直接让 skill 帮你执行，例如：

```text
提交
```

如果还要推送到远端：

```text
提交并推送
```

默认情况下，AI 会根据当前改动自动生成合适的 commit message。

命令行的具体用法放在 [`docs/cli/user-guide.md`](/Users/xianqiu/Projects/youpu-sources/docs/cli/user-guide.md)。

## 仓库结构

```text
.
├── accepted/
├── rejected/
│   └── rejected.csv
├── docs/
│   ├── index.md
│   ├── overview/
│   ├── specs/
│   ├── cli/
│   └── skills/
├── templates/
│   └── accepted.md
├── cli/
└── youpu
```

你通常只需要关心这些位置：

- `accepted/`：正式保留的记录
- `rejected/rejected.csv`：正式拒绝的记录
- `imports/`：临时导入目录
- `docs/`：详细文档
- `youpu`：底层命令入口

## 去哪里看详细说明

- 文档总入口：[docs/index.md](/Users/xianqiu/Projects/youpu-sources/docs/index.md)
- Skill 文档：[docs/skills/youpu-gatekeeper.md](/Users/xianqiu/Projects/youpu-sources/docs/skills/youpu-gatekeeper.md)
- CLI 用户文档：[docs/cli/user-guide.md](/Users/xianqiu/Projects/youpu-sources/docs/cli/user-guide.md)
- accepted 规范：[docs/specs/accepted.md](/Users/xianqiu/Projects/youpu-sources/docs/specs/accepted.md)
- rejected 规范：[docs/specs/rejected.md](/Users/xianqiu/Projects/youpu-sources/docs/specs/rejected.md)
- URL 规范：[docs/specs/url.md](/Users/xianqiu/Projects/youpu-sources/docs/specs/url.md)

如果你是第一次使用，建议从 [`docs/index.md`](/Users/xianqiu/Projects/youpu-sources/docs/index.md) 开始。

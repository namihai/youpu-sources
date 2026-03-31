# youpu CLI 用户文档

这份文档面向仓库使用者，说明 `youpu` 应该怎么用。

如果你只想快速开始，先看 [README.md](../../README.md)。如果你要看开发接口和返回码，再看 [spec.md](spec.md)。

## `youpu` 是做什么的

`youpu` 是这个仓库的守门命令。它只负责：

- 检查正式仓库是否合规
- 检查并导入 `imports/` 中的候选内容
- 在提交前做最后检查
- 输出当前仓库摘要
- 诊断单个 URL

常用命令只有 5 个：

```bash
youpu validate
youpu ingest
youpu submit
youpu report
youpu inspect-url
```

## 你通常怎么用

推荐按这个顺序：

1. 把候选内容放进 `imports/accepted/` 和 `imports/rejected/`
2. 运行 `youpu ingest --dry-run`
3. 查看 `imports/reports/issues.md`
4. 修正不能处理的内容
5. 运行 `youpu ingest`
6. 运行 `youpu validate` 或 `youpu report`
7. 提交前运行 `youpu submit --check-only`
8. 最后再运行 `youpu submit --message "..."`

## 导入目录

`youpu ingest` 固定读取这个目录：

```text
imports/
  accepted/
  rejected/
  reports/
```

说明：

- `imports/accepted/`：放候选 accepted Markdown
- `imports/rejected/`：放候选 rejected CSV
- `imports/reports/`：保存检查结果和问题清单

`youpu` 不支持切换到其他导入目录。

## 常用命令

### 先检查导入内容

```bash
youpu ingest --dry-run
```

这个命令会检查 `imports/` 里的内容，但不会修改正式仓库。

最小示例输出：

```text
Ingest dry-run completed
imports root: imports
accepted candidates ready: 0
rejected candidates ready: 0
issues: 0
```

### 正式导入

```bash
youpu ingest
```

这个命令会把合规的候选内容写入正式仓库，并保留不能处理的内容供你手工修正。

最小示例输出：

```text
Ingest completed
imports root: imports
accepted candidates ready: 1
rejected candidates ready: 1
issues: 0
```

### 检查正式仓库

```bash
youpu validate
```

这个命令会检查正式仓库中的：

- `accepted/`
- `rejected/rejected.csv`
- 重复记录
- accepted / rejected 冲突

最小示例输出：

```text
Validation passed
```

### 查看当前摘要

```bash
youpu report
```

最小示例输出：

```text
Repository summary
accepted files: 93
rejected rows: 82
latest accepted id: SRC-0095
validation: passed
duplicates: none
cross-conflicts: 0
imports pending accepted: 0
imports pending rejected: 0
imports issues: 0
```

### 提交前检查

```bash
youpu submit --check-only
```

这个命令会在提交前确认：

- 正式仓库合法
- `imports/` 里没有待处理内容
- `imports/reports/` 里没有未解决问题

最小示例输出：

```text
Submit check passed
```

### 提交并可选推送

```bash
youpu submit --message "your commit message"
youpu submit --message "your commit message" --push
```

最小示例输出：

```text
Submit completed
```

### 诊断单个 URL

```bash
youpu inspect-url 'https://example.com/path?utm_source=x#intro'
```

这个命令会输出规范化后的 URL。

最小示例输出：

```text
https://example.com/path
```

## 遇到问题先看哪里

运行 `youpu ingest` 或 `youpu ingest --dry-run` 后，优先查看：

- [`imports/reports/issues.md`](../../imports/reports/issues.md)

这里会列出：

- 哪些文件可以导入
- 哪些文件格式不对
- 哪些文件和现有记录冲突

系统还会生成：

- [`imports/reports/summary.json`](../../imports/reports/summary.json)

这个文件更适合脚本或 agent 使用。

## 如果你需要 JSON 输出

```bash
youpu --format json <command>
```

例如：

```bash
youpu --format json ingest --dry-run
youpu --format json validate
youpu --format json report
```

## 相关文档

- 文档总入口：[../index.md](../index.md)
- accepted 规范：[../specs/accepted.md](../specs/accepted.md)
- rejected 规范：[../specs/rejected.md](../specs/rejected.md)
- URL 规范：[../specs/url.md](../specs/url.md)
- CLI 开发接口：[spec.md](spec.md)

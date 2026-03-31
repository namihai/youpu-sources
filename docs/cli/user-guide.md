# youpu CLI 用户文档

这份文档面向两类使用者：

- 技术用户
- 会调用命令行工具的大模型或 agent

如果你要看接口边界、返回码和开发约束，请看 [spec.md](/Users/xianqiu/Projects/youpu-sources/docs/cli/spec.md)。

## 目标

`youpu` 是仓库的守门 CLI，只做这几件事：

- 检查正式仓库是否合法
- 检查并合并 `imports/` 中的候选内容
- 在提交前做最终守门
- 输出仓库摘要
- 诊断单个 URL

统一入口：

```bash
youpu <command> [options]
```

当前对外命令：

- `youpu validate`
- `youpu ingest`
- `youpu submit`
- `youpu report`
- `youpu inspect-url`

## 默认导入目录

`ingest` 固定使用：

```text
imports/
  accepted/
  rejected/
  reports/
```

其中：

- `imports/accepted/`：放候选 accepted Markdown
- `imports/rejected/`：放候选 rejected CSV
- `imports/reports/`：自动生成问题清单和摘要

## 常用命令

### 校验正式仓库

```bash
youpu validate
```

用途：

- 检查 `accepted/`
- 检查 `rejected/rejected.csv`
- 检查重复
- 检查 cross-conflict

最小示例输出：

```text
Validation passed
```

### 预检查导入内容

```bash
youpu ingest --dry-run
```

用途：

- 扫描 `imports/accepted/` 和 `imports/rejected/`
- 只检查，不写正式仓库
- 刷新 `imports/reports/`

最小示例输出：

```text
Ingest dry-run completed
imports root: imports
accepted candidates ready: 0
rejected candidates ready: 0
issues: 0
```

### 合并合法候选内容

```bash
youpu ingest
```

用途：

- 把合法候选合并进正式仓库
- 自动做 URL 规范化、编号分配和 slug 规范化
- 保留有问题的文件供人工处理

最小示例输出：

```text
Ingest completed
imports root: imports
accepted candidates ready: 1
rejected candidates ready: 1
issues: 0
```

### 提交前检查

```bash
youpu submit --check-only
```

用途：

- 在 git 提交前做最终守门
- 检查正式仓库
- 检查 `imports/` 是否还有待处理内容或问题

最小示例输出：

```text
Submit check passed
```

### 提交并可选推送

```bash
youpu submit --message "your commit message"
youpu submit --message "your commit message" --push
```

用途：

- 先做守门检查
- 通过后执行 `git add -A`
- 然后执行 `git commit`
- `--push` 时继续执行 `git push`

最小示例输出：

```text
Submit completed
```

### 查看仓库摘要

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

### 诊断 URL

```bash
youpu inspect-url 'https://example.com/path?utm_source=x#intro'
```

最小示例输出：

```text
https://example.com/path
```

## `imports/reports/` 会生成什么

每次运行 `youpu ingest` 或 `youpu ingest --dry-run`，都会刷新：

- `imports/reports/issues.md`
- `imports/reports/summary.json`

其中：

- `issues.md` 适合人阅读
- `summary.json` 适合 agent 或脚本读取

## JSON 输出

如果命令结果需要给 agent 或自动化消费，使用：

```bash
youpu --format json <command>
```

例如：

```bash
youpu --format json ingest --dry-run
youpu --format json validate
youpu --format json report
```

最小示例输出：

```json
{
  "ok": true,
  "command": "report",
  "summary": "Repository summary\naccepted files: 93\nrejected rows: 82\nlatest accepted id: SRC-0095\nvalidation: passed\nduplicates: none\ncross-conflicts: 0\nimports pending accepted: 0\nimports pending rejected: 0\nimports issues: 0",
  "diagnostics": [],
  "data": {
    "accepted_files": 93,
    "rejected_rows": 82,
    "latest_accepted_id": "SRC-0095",
    "validation_ok": true,
    "duplicates_ok": true,
    "cross_conflicts": 0,
    "imports_pending_accepted": 0,
    "imports_pending_rejected": 0,
    "imports_issues": 0
  }
}
```

## 返回码

```text
0  成功，无问题
1  校验失败或守门检查失败
2  参数错误
3  运行时异常
4  保留
```

## 建议用法

推荐流程：

1. 把候选内容放进 `imports/accepted/` 和 `imports/rejected/`
2. 运行 `youpu ingest --dry-run`
3. 查看 `imports/reports/`
4. 修正无法处理的项
5. 运行 `youpu ingest`
6. 运行 `youpu validate` 或 `youpu submit --check-only`
7. 没问题后再执行 `youpu submit --message "..."`

## 相关文档

- 开发接口文档：[spec.md](/Users/xianqiu/Projects/youpu-sources/docs/cli/spec.md)
- CLI 边界：[scope.md](/Users/xianqiu/Projects/youpu-sources/docs/cli/scope.md)
- URL 规范化规则：[url-normalization.md](/Users/xianqiu/Projects/youpu-sources/docs/url-normalization.md)

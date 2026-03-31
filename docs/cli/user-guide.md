# youpu CLI 用户文档

这份文档面向两类使用者：

- 技术用户
- 会调用命令行工具的大模型或 agent

如果你要看接口边界、返回码和开发约束，请看 [spec.md](/Users/xianqiu/Projects/youpu-sources/docs/cli/spec.md)。

## 目标

`youpu` 是仓库的统一 CLI，用于：

- 校验 `accepted/` 和 `rejected/rejected.csv`
- 检查重复和交叉冲突
- 新建 `accepted` / `rejected` 记录
- 规范化 URL
- 输出仓库摘要

统一入口：

```bash
youpu <command> [options]
```

## 第一版边界

当前第一版 CLI 只做三类事：

- 检查
- 规范化
- 安全新增

不做的事：

- 不自动修复已有 `accepted/*.md`
- 不自动修复已有 `rejected/rejected.csv`
- 不自动批量迁移历史目录
- 不自动改写业务判断结论

如果需要改已有内容，应先用检查命令定位问题，再由用户或后续专门命令显式处理。

## 常用命令

### 校验仓库

```bash
youpu validate
youpu validate --scope accepted
youpu validate --scope rejected
youpu validate --scope all
```

用途：

- 检查结构是否符合规范
- 检查 `accepted` / `rejected` 是否存在交叉冲突

常见结果：

- `Validation passed`
- `Validation failed`

最小示例输出：

```text
Validation passed
```

### 检查重复

```bash
youpu duplicates
youpu duplicates --scope accepted
youpu duplicates --scope rejected
youpu duplicates --scope cross
youpu duplicates --scope all
```

用途：

- 检查 `accepted` 内重复
- 检查 `rejected` 内重复
- 检查 accepted/rejected 交叉重复

最小示例输出：

```text
No duplicates found
```

### 新建 accepted

```bash
youpu new accepted <slug>
youpu new accepted <slug> --title "标题"
youpu new accepted <slug> --title "标题" --url https://example.com/source
youpu new accepted <slug> --dry-run
```

行为：

- 自动扫描当前最大编号
- 创建下一个 `SRC-####-slug.md`
- 从 `templates/accepted.md` 生成文件
- `--dry-run` 只预览，不写文件

示例：

```bash
youpu new accepted muraldh --title "敦煌壁画数字修复图像数据集（MuralDH）"
```

最小示例输出：

```text
Would create accepted/SRC-0001-demo-slug.md
```

### 新增 rejected

```bash
youpu new rejected --url <url> --title <title> --reason <reason>
youpu new rejected --url <url> --title <title> --reason <reason> --dry-run
```

行为：

- 先规范化 URL
- 检查是否与 `rejected` 现有记录重复
- 检查是否与 `accepted.canonical_url` 冲突
- `--dry-run` 只预览，不写 CSV

示例：

```bash
youpu new rejected \
  --url https://example.com/dataset?utm_source=test \
  --title "Example Dataset" \
  --reason "版权或许可条款不清，暂不收录。"
```

最小示例输出：

```text
Would add rejected entry to rejected/rejected.csv
```

### 规范化 URL

```bash
youpu normalize-url <url>
```

示例：

```bash
youpu normalize-url 'https://example.com/path?utm_source=x#intro'
```

输出：

```text
https://example.com/path
```

### 查看仓库摘要

```bash
youpu report
```

输出内容：

- `accepted` 文件数
- `rejected` 行数
- 最新 accepted 编号
- 校验状态
- 重复状态
- 交叉冲突数量

最小示例输出：

```text
Repository summary
accepted files: 93
rejected rows: 82
latest accepted id: SRC-0095
validation: passed
duplicates: none
cross-conflicts: 0
```

## JSON 输出

如果命令结果需要给 agent、脚本或自动化逻辑消费，使用：

```bash
youpu --format json <command>
```

例如：

```bash
youpu --format json validate
youpu --format json duplicates --scope cross
youpu --format json report
```

最小示例输出：

```json
{
  "ok": true,
  "command": "report",
  "summary": "Repository summary\naccepted files: 93\nrejected rows: 82\nlatest accepted id: SRC-0095\nvalidation: passed\nduplicates: none\ncross-conflicts: 0",
  "diagnostics": [],
  "data": {
    "accepted_files": 93,
    "rejected_rows": 82,
    "latest_accepted_id": "SRC-0095",
    "validation_ok": true,
    "duplicates_ok": true,
    "cross_conflicts": 0
  }
}
```

适用场景：

- 让大模型读取结构化结果
- 在脚本中判断 `ok`、`diagnostics`、`data`
- 将 CLI 作为 skill 或 agent 的底层执行接口

## 返回码

```text
0  成功，无问题
1  校验失败或发现重复
2  参数错误
3  运行时异常
4  拒绝执行
```

`4` 常见于：

- 新增 rejected 时 URL 已存在
- 新增 rejected 时与 accepted 冲突
- 新增 accepted 时目标文件已存在

## 建议用法

- 新增或修改记录后，先跑 `youpu validate`
- 批量迁移后，再跑 `youpu duplicates`
- 写入前优先用 `--dry-run`
- 如果是自动化调用，优先使用 `--format json`

## 相关文档

- 开发接口文档：[spec.md](/Users/xianqiu/Projects/youpu-sources/docs/cli/spec.md)
- URL 规范化规则：[url-normalization.md](/Users/xianqiu/Projects/youpu-sources/docs/url-normalization.md)

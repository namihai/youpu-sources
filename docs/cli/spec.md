# youpu CLI 开发接口文档

这份文档面向 CLI 开发者，定义 `youpu` 的命令接口、返回码和行为边界。

如果你要看面向技术用户或大模型调用方的用法说明，请看 [user-guide.md](/Users/xianqiu/Projects/youpu-sources/docs/cli/user-guide.md)。

## 目标

`youpu` 是本仓库的守门 CLI，用于：

- 校验正式 `accepted/` 与 `rejected/rejected.csv`
- 从默认 `imports/` 目录安全合并候选内容
- 在提交前做最终检查
- 输出仓库摘要
- 对单个 URL 做轻量诊断

设计原则：

- 单入口
- 只保留少量主命令
- 默认输出可读
- 支持机器可读 JSON
- 只做守门，不做发现
- 不做隐式高风险修复

## 命令入口

统一入口：

```bash
youpu <command> [options]
```

对外命令只保留：

- `youpu validate`
- `youpu ingest`
- `youpu submit`
- `youpu report`
- `youpu inspect-url`

## 全局参数

所有命令共享以下全局参数：

```bash
--format text|json
--no-color
--root <path>
```

说明：

- `--format text`：默认，终端友好输出
- `--format json`：结构化输出
- `--no-color`：关闭颜色
- `--root <path>`：指定仓库根目录，默认自动探测

## 退出码

```text
0  成功，无问题
1  校验失败或守门检查失败
2  参数错误
3  运行时异常
```

## 默认导入目录

`youpu ingest` 固定使用默认导入目录：

```text
imports/
  accepted/
  rejected/
  reports/
```

其中：

- `imports/accepted/`：候选 accepted Markdown
- `imports/rejected/`：候选 rejected CSV
- `imports/reports/`：由 `ingest` 生成的问题清单和摘要

CLI 不支持切换导入目录路径。

## 数据模型

### accepted

accepted 文档字段保持为：

```yaml
title:
canonical_url:
domain:
content_type:
data_form:
data_type:
region:
source_type:
source_org:
permissions:
tags:
use_cases:
```

`canonical_url` 必填，用于重复检查和 accepted/rejected 交叉冲突检查。

### rejected

rejected CSV 保持为：

```csv
url,title,reason
```

其中 `url` 应为规范化后的 canonical URL。

## 命令规格

### `validate`

用途：

- 校验正式仓库是否处于合法状态

接口：

```bash
youpu validate
youpu validate --format json
```

行为：

- 检查 `accepted/` 结构与字段
- 检查 `rejected/rejected.csv` 结构与字段
- 检查 accepted 内重复
- 检查 rejected 内重复
- 检查 accepted/rejected cross-conflict

约束：

- 固定检查全仓
- 不暴露 `scope`
- 不做写操作

### `ingest`

用途：

- 从默认 `imports/` 目录检查并合并候选内容

接口：

```bash
youpu ingest --dry-run
youpu ingest
youpu ingest --format json
```

行为：

- 读取 `imports/accepted/*.md`
- 读取 `imports/rejected/*.csv`
- 检查 schema、冲突和重复
- 对合法内容做确定性修正
  - `canonical_url` / `url` 规范化
  - `accepted` 编号分配
  - 文件名 slug 规范化
- 在写模式下把合法内容合并到正式仓库
- 成功导入的源文件会从 `imports/` 中清理
- 生成：
  - `imports/reports/issues.md`
  - `imports/reports/summary.json`

约束：

- 不自动补事实字段
- 不自动判断 accepted/rejected
- 不支持自定义导入目录

### `submit`

用途：

- 在 git 提交前做最终守门

接口：

```bash
youpu submit --check-only
youpu submit --message "..."
youpu submit --message "..." --push
```

行为：

- 先运行全仓检查
- 检查 `imports/` 是否还有待处理内容
- 检查 `imports/` 是否仍有未解决问题
- `--check-only` 只返回检查结果
- `--message` 模式下：
  - 执行 `git add -A`
  - 执行 `git commit -m "..."`
  - 若带 `--push`，再执行 `git push`

### `report`

用途：

- 输出仓库摘要

接口：

```bash
youpu report
youpu report --format json
```

输出内容：

- `accepted` 文件数
- `rejected` 行数
- 最新 accepted 编号
- validation 状态
- duplicates 状态
- cross-conflicts 数量
- `imports` 待处理文件数量
- `imports` 当前问题数量

### `inspect-url`

用途：

- 对单个 URL 做轻量诊断

接口：

```bash
youpu inspect-url <url>
youpu inspect-url <url> --format json
```

行为：

- 校验 URL 是否合法
- 输出规范化后的 canonical URL

约束：

- 不做写操作
- 不承担来源发现

## 自动处理边界

允许自动处理：

- URL 规范化
- accepted 编号分配
- accepted 文件名 slug 规范化
- 导入时的重复与冲突拦截

不允许自动处理：

- 自动补事实字段
- 自动推断来源真实性
- 自动决定 accepted 或 rejected
- 自动重写 rejected `reason`
- 自动覆盖正式库已有记录

## JSON 输出

所有命令都支持：

```bash
youpu --format json <command>
```

返回统一结构：

```json
{
  "ok": true,
  "command": "report",
  "summary": "Repository summary\n...",
  "diagnostics": [],
  "data": {}
}
```

其中：

- `ok`：命令是否通过
- `summary`：面向人类的摘要
- `diagnostics`：结构化问题列表
- `data`：补充字段

## 非目标

CLI 不负责：

- 外部来源发现
- 网页抓取和页面理解
- 自动从原始网页推断数据源
- 通用工作流管理
- 对正式库做高风险自动修复

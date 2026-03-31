# youpu CLI 开发接口文档

这份文档面向 CLI 开发者，定义 `youpu` 的命令接口、参数、返回码、数据模型和行为边界。

如果你要看面向技术用户或大模型调用方的用法说明，请看 [user-guide.md](/Users/xianqiu/Projects/youpu-sources/docs/cli/user-guide.md)。

## 目标

`youpu` 是本仓库的统一命令行入口，用于：

- 校验 `accepted/` 与 `rejected/rejected.csv` 是否符合项目规范
- 检查并阻止重复记录
- 安全地新增 `accepted` / `rejected` 记录
- 规范化 URL
- 输出适合非技术用户阅读的结果
- 输出适合 skill 或自动化消费的结构化结果

设计原则：

- 单入口
- 子命令明确
- 默认输出可读
- 支持机器可读输出
- 校验与修复分离
- 不做隐式破坏性修改

第一版边界：

- 第一版只做检查、规范化和安全新增
- 第一版不做自动修复
- 第一版不批量改写现有 accepted/rejected 内容，除非用户显式执行对应写命令

## 命令入口

统一入口：

```bash
youpu <command> [subcommand] [options]
```

示例：

```bash
youpu validate
youpu duplicates
youpu new accepted muraldh
youpu new rejected --url https://example.com --title "Example" --reason "不是具体数据集来源"
youpu normalize-url https://example.com?a=1&utm_source=x
youpu report
```

## 终端体验

终端输出使用 `rich`。

要求：

- 成功：绿色状态
- 警告：黄色状态
- 错误：红色状态
- 表格型结果：使用 `rich.table`
- 多项问题：按条列出
- 默认输出适合非技术用户直接阅读
- 支持 `--format json` 输出结构化结果，供 skill 或脚本消费

## 全局参数

所有命令共享以下全局参数：

```bash
--format text|json
--quiet
--verbose
--no-color
--root <path>
```

说明：

- `--format text`：默认，终端友好输出
- `--format json`：结构化输出
- `--quiet`：只输出结论，不输出过程信息
- `--verbose`：输出更多细节
- `--no-color`：关闭颜色
- `--root <path>`：指定仓库根目录，默认当前目录或自动探测

## 退出码规范

```text
0  成功，无问题
1  校验失败或发现重复
2  参数错误
3  运行时异常
4  拒绝执行（例如将产生重复记录）
```

## 数据模型要求

### accepted schema

建议将 `accepted` YAML 扩展为：

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

新增字段：

- `canonical_url`
  - 必填
  - 表示该来源的稳定主链接
  - 用于 accepted 内部去重
  - 用于 accepted/rejected 交叉冲突检查

### rejected schema

保持：

```csv
url,title,reason
```

其中：

- `url` 为规范化后的 canonical URL

## 命令规格

### `validate`

用途：

- 校验仓库整体规范

接口：

```bash
youpu validate
youpu validate --scope accepted
youpu validate --scope rejected
youpu validate --scope all
youpu validate --format json
```

参数：

- `--scope accepted|rejected|all`
  - 默认 `all`

检查项：

`accepted`

- 文件名符合 `SRC-####-slug.md`
- 存在 H1
- 存在 fenced YAML block
- H1 与 YAML `title` 一致
- 必填字段齐全
- 不包含废弃字段
- `tags` / `use_cases` 为 inline array
- `canonical_url` 非空
- `canonical_url` 为合法 URL

`rejected`

- CSV 表头为 `url,title,reason`
- 每行 `url/title/reason` 非空
- `url` 为合法 URL
- `url` 不重复

`cross-check`

- `accepted.canonical_url` 不得出现在 `rejected.url`
- 若冲突，视为校验失败

输出：

- 文本模式：摘要 + 问题列表
- JSON 模式：返回每类问题及文件位置

文本输出示例：

```text
Validation failed

accepted:
- accepted/SRC-0098-example.md: missing required field `canonical_url`
- accepted/SRC-0099-demo.md: H1 title does not match YAML `title`

rejected:
- rejected/rejected.csv:45: duplicate url

cross:
- canonical_url exists in both accepted and rejected: https://example.com/data
```

### `duplicates`

用途：

- 专门检查重复，不做其他结构校验

接口：

```bash
youpu duplicates
youpu duplicates --scope accepted
youpu duplicates --scope rejected
youpu duplicates --scope cross
youpu duplicates --scope all
```

参数：

- `--scope accepted|rejected|cross|all`
  - 默认 `all`

检查规则：

`accepted`

- `canonical_url` 重复
- `title` 完全重复
- 可选后续扩展：归一化标题近似重复

`rejected`

- `url` 重复

`cross`

- `accepted.canonical_url` 与 `rejected.url` 冲突

输出：

- 表格列出重复项、涉及文件/行号、冲突值

### `new accepted`

用途：

- 新建一个 accepted 模板文件

接口：

```bash
youpu new accepted <slug>
youpu new accepted <slug> --title "标题"
youpu new accepted <slug> --title "标题" --url https://example.com
```

参数：

- `<slug>` 必填
- `--title <text>` 可选
- `--url <canonical_url>` 可选
- `--dry-run` 可选

行为：

- 扫描当前最大编号
- 创建下一个文件，如 `SRC-0096-<slug>.md`
- 从模板生成新文件
- 若提供 `--title`，填入 H1 和 YAML `title`
- 若提供 `--url`，填入 YAML `canonical_url`
- 若目标文件已存在，报错
- 不自动提交、不自动校验

输出示例：

```text
Created accepted/SRC-0096-muraldh.md
```

`--dry-run` 输出示例：

```text
Would create accepted/SRC-0096-muraldh.md
```

### `new rejected`

用途：

- 安全地向 `rejected/rejected.csv` 追加一条记录

接口：

```bash
youpu new rejected --url <url> --title <title> --reason <reason>
```

参数：

- `--url` 必填
- `--title` 必填
- `--reason` 必填
- `--dry-run` 可选

行为：

- 将 `--url` 规范化为 canonical URL
- 检查该 URL 是否已存在于 `rejected`
- 检查该 URL 是否已存在于 `accepted.canonical_url`
- 若冲突，拒绝写入
- 若无冲突，追加到 CSV

拒绝条件：

- URL 已存在于 rejected
- URL 已存在于 accepted
- URL 非法
- title/reason 为空

输出示例：

```text
Added rejected entry:
- url: https://example.com/data
- title: Example Dataset
- reason: 不是具体数据集来源
```

### `normalize-url`

用途：

- 规范化 URL，供人工检查或其他命令复用

接口：

```bash
youpu normalize-url <url>
```

行为：

- 去掉锚点
- 去掉常见追踪参数，如 `utm_*`
- 去掉无意义 query
- 保留能唯一标识资源的关键参数
- 输出 canonical URL

输出示例：

```text
https://example.com/dataset/123
```

JSON 输出示例：

```json
{
  "input": "https://example.com/dataset/123?utm_source=x#intro",
  "canonical_url": "https://example.com/dataset/123"
}
```

### `report`

用途：

- 输出仓库当前状态摘要

接口：

```bash
youpu report
youpu report --format json
```

输出内容：

- accepted 文件总数
- rejected 记录总数
- accepted 最大编号
- 是否存在校验错误
- 是否存在重复
- 是否存在 accepted/rejected 冲突

文本示例：

```text
Repository summary

- accepted files: 95
- rejected rows: 83
- latest accepted id: SRC-0095
- validation: passed
- duplicates: none
- cross-conflicts: none
```

## URL 规范化规则

`canonical_url` / `rejected.url` 的规范化应遵循：

- 优先使用详情页主链接
- 去掉 `utm_*`
- 去掉页面锚点
- 去掉明显无意义 query
- 保留数据集唯一标识参数
- 对 DOI、Dataverse、Zenodo、Hugging Face、Kaggle 等来源保留稳定主链接

注意：

- 规范化规则应是可预测的
- 不应过度“智能猜测”
- 无法确定时保守保留原始主链接

边界约束：

- 可以去掉锚点和追踪参数
- 可以删除明显无意义的 query 参数
- 必须保留能唯一标识资源的关键参数
- 不应自动把详情页替换成第三方镜像页
- 不应自动把论文页推断成数据页
- 不应跨站点合并链接，除非规则中已明确约定

## 输出格式要求

### 文本模式

适合非技术用户：

- 摘要在前
- 问题分组
- 文件路径和行号尽量明确
- 给出下一步建议

### JSON 模式

适合 skill / 自动化：

建议结构：

```json
{
  "ok": false,
  "command": "validate",
  "scope": "all",
  "summary": {
    "accepted_files": 95,
    "rejected_rows": 83,
    "errors": 3
  },
  "errors": [
    {
      "type": "accepted_missing_field",
      "path": "accepted/SRC-0098-example.md",
      "field": "canonical_url",
      "message": "missing required field `canonical_url`"
    }
  ]
}
```

## 非目标

第一版 CLI 不做这些事：

- 不自动修复 accepted 文件内容
- 不自动修复 rejected.csv 中的业务结论
- 不自动批量迁移历史目录
- 不自动根据正文猜测 canonical URL
- 不自动重写 rejected 理由
- 不做模糊 dedupe 合并

这些以后可以单独设计 `fix` 或 `import` 命令。

## 第一版推荐范围

建议 MVP 只做这 6 个命令：

- `youpu validate`
- `youpu duplicates`
- `youpu new accepted`
- `youpu new rejected`
- `youpu normalize-url`
- `youpu report`

## 相关文档

- 用户文档：[user-guide.md](/Users/xianqiu/Projects/youpu-sources/docs/cli/user-guide.md)
- 当前开发清单：[implementation-checklist.md](/Users/xianqiu/Projects/youpu-sources/docs/cli/implementation-checklist.md)

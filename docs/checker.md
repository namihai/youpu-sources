# 检查器

`scripts/check.py` 是这个仓库唯一的校验入口。

在仓库根目录运行：

```bash
python3 scripts/check.py
```

检查器会读取 [`../scripts/checker.json`](../scripts/checker.json)，扫描 `data/` 目录中的 Markdown 文件，输出诊断信息；如果校验失败，会以退出码 `1` 结束。

检查器只输出报告结果。成功时输出：

```text
Status: PASS
Files checked: 116
```

失败时输出失败列表：

```text
Status: FAIL
Files checked: 116
Failures: 1

Code                     File
------------------------ ----------------------------------------
body_too_short           data/example.md
```

## 检查内容

- `data/` 必须存在。
- `data/` 只允许包含 Markdown 文件，隐藏文件除外。
- 数据文件名必须使用小写字母、数字和连字符，例如 `digital-dunhuang.md`。
- 每个 Markdown 文件必须以 `---` 包裹的 front matter 开头。
- front matter 中只能出现 `checker.json` 配置过的字段。
- 必填字段必须存在且不能为空。
- 字段值必须符合配置中的类型。
- 枚举字段必须使用配置允许的值。
- 标记为 `unique: true` 的字段在 `data/` 内必须唯一。
- Markdown 正文的非空白字符数不能低于 `min_body_chars` 配置值。
- 重复的 `title` 会作为 warning 输出。

## 错误代码

检查器使用少量稳定代码标识问题类型：

- `config_missing`：缺少检查器配置文件。
- `config_invalid`：检查器配置格式不正确。
- `data_missing`：`data/` 目录不存在。
- `data_not_directory`：`data` 路径不是目录。
- `data_unexpected_file`：`data/` 中出现非 Markdown 文件或目录。
- `invalid_filename`：数据文件名不符合规则。
- `front_matter_missing`：缺少 front matter。
- `front_matter_unclosed`：front matter 没有闭合。
- `front_matter_invalid`：front matter 内容格式不合法。
- `front_matter_duplicate_key`：front matter 中出现重复字段。
- `unknown_field`：出现未配置的 meta 字段。
- `missing_required_field`：缺少必填字段。
- `invalid_url`：URL 字段不是合法绝对 URL。
- `invalid_enum`：枚举字段取值不在允许范围内。
- `invalid_inline_array`：内联数组字段格式不合法。
- `duplicate_source`：多个文件的 `canonical_url` 规范化后相同。
- `duplicate_unique_field`：其他唯一字段重复。
- `duplicate_title`：标题重复；当前作为 warning。
- `badge_count_mismatch`：README 中的 sources badge 数量与 `data/*.md` 数量不一致；当前作为 warning。
- `body_too_short`：正文非空白字符数低于配置值。

## 不检查内容

- 不分配或校验 `SRC-####` 编号。
- 不读取 `staging/`。
- 不执行入库或导入操作。
- 不自动改写文件。
- 不联网抓取 URL，也不验证外部页面是否可访问。
- 不判断某个来源是否应该被收录。
- 不强制校验 Markdown 正文中的章节标题。

## Front Matter 格式

检查器只支持一个很小的 front matter 子集：

```md
---
title: "数字敦煌"
summary: "一个简短、客观的来源说明。"
canonical_url: "https://www.e-dunhuang.com/"
publisher: "敦煌研究院"
modality: "image"
access_level: "open"
tags: [敦煌, 壁画]
---
```

字段值支持普通字符串、带引号字符串和单行内联数组。这样可以让检查器不依赖第三方库，并保持行为可预测。

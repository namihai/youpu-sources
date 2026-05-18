# Accepted 规范

## 定义

`data/accepted/` 中的记录表示：某个数据集来源已经过核验，确认真实存在，并值得在仓库中保留。

这里记录的是“来源”，不是数据集文件本身。

## 文件形式

- 每条记录对应一个 Markdown 文件
- 文件放在 `data/accepted/` 目录下
- 文件名遵循统一命名规则
- accepted 的字段定义以 [`../../schemas/accepted.json`](../../schemas/accepted.json) 为准
- [`../../templates/accepted.md`](../../templates/accepted.md) 是面向贡献者的填写模板，结构需要与 schema 保持一致
- schema / template / CLI 的维护关系见 [`schema.md`](schema.md)

## 文件命名

`data/accepted/` 下的文件名统一使用以下格式：

```text
SRC-####-slug.md
```

例如：

```text
SRC-0001-muraldh.md
SRC-0002-ihchina.md
SRC-0003-figshare-dunhuang-restoration.md
```

命名规则：

- 前缀固定为 `SRC`
- `####` 为四位递增编号
- `slug` 为用户提供的简短英文标识
- 文件扩展名固定为 `.md`

`slug` 要求：

- 使用小写字母、数字和连字符 `-`
- 只能使用英文字符，不得包含中文字符
- 保持简短，便于人工识别
- 不要求完整表达中文标题
- 不建议包含随机 hash
- 不建议直接使用超长中文标题

正式入库时，系统只负责自动分配 `SRC-####` 编号前缀；`slug` 必须由用户在 `staging/accepted/` 的文件名中提供。系统不会替用户生成、翻译、改写或规范化 `slug`。

维护者如果要在本地调试 accepted 导入流程，可以按下面方式验证：

1. 用户先把候选 Markdown 放进 `staging/accepted/`
2. 运行 `uv run python ./scripts/youpu validate-imports`
3. 修正问题后运行 `uv run python ./scripts/youpu ingest`

`ingest` 会在正式合并时：

- 自动计算下一个编号
- 保留 staging 文件名中的 `slug`
- 生成 `SRC-####-slug.md`，其中只自动补上 `SRC-####-` 前缀
- 写入正式 accepted 文件名

不建议使用以下命名方式：

- 中文全标题加随机字符串
- 包含任何中文字符的文件名
- `Untitled`
- 带空格的超长文件名
- 以 URL 直接作为文件名

## 标准结构

accepted 文档由两部分组成：

1. 文件开头的 YAML front matter
2. front matter 之后的 Markdown 正文

示意：

```md
---
title: 标题
summary: 一句话客观描述这个来源是什么
canonical_url: https://example.com/dataset
publisher: 发布或维护该来源的主体
modality: text
access_level: open
tags: [标签1, 标签2]
---

## 来源概述

## 收录内容与边界

## 获取方式

## 使用与访问限制

## 质量与风险
```

## YAML 字段要求

accepted 记录只保留少量稳定、客观、适合长期维护的核心字段。

### 必填字段

以下字段必须存在，且应填写明确值：

```yaml
title:
summary:
canonical_url:
publisher:
modality:
access_level:
```

以下字段可以按需填写：

```yaml
tags:
```

说明：

- `title`：来源名称。
- `summary`：一句话客观描述这个来源是什么。它用于卡片和快速浏览，应简洁、可验证，避免评价性表述，也不要直接照抄正文中的长段说明。
- `canonical_url`：来源的 `canonical_url`，通常应填写介绍该数据集或来源的数据集主页，作为 accepted 内部去重与交叉校验的主标识。它一般不是下载链接。下载链接应在 Markdown 正文中单独说明；如果该数据集没有独立主页、只有下载链接，可将下载链接作为 `canonical_url`。
- `publisher`：发布、维护或主要提供该来源的主体名称。它不要求一定是正式机构，也可以是项目组、联合体或个人。
- `modality`：该来源主要提供的数据模态。
- `access_level`：访问门槛。
- `tags`：可选的辅助检索标签。它用于补充前端搜索和简单聚类，不承担主分类职责。

## 链接要求

- YAML 中必须包含 `canonical_url`
- `canonical_url` 应尽量填写该来源的数据集主页或详情页，而不是下载直链
- 如果没有独立主页、只有下载链接，可以使用下载链接作为 `canonical_url`
- 应尽量使用规范化后的主链接，避免追踪参数与无意义锚点
- 输入阶段可以先使用原始 URL；系统会在校验和入库时按统一规则规范化
- 具体规则见 [`url.md`](url.md)

## `modality` 要求

`modality` 必须使用以下枚举值之一：

- `text`
- `image`
- `audio`
- `video`
- `tabular`
- `geospatial`
- `multimodal`
- `other`

说明：

- `multimodal`：该来源的核心数据天然由多种模态组成，并且这些模态通常是配套出现的。
- `other`：确实不适合归入以上任一类时使用，不应滥用。

## `access_level` 要求

`access_level` 必须使用以下枚举值之一：

- `open`
- `request`
- `restricted`
- `unknown`

说明：

- `open`：可直接访问或下载，不需要额外人工审批。
- `request`：需要注册、申请、登录、提交表单或其他额外步骤才能获得完整访问。
- `restricted`：明确不可公开获得，或只有封闭授权渠道。
- `unknown`：当前无法确认访问方式。

## `summary` 要求

- YAML 中必须包含 `summary`
- `summary` 应为一句话
- 应客观描述这个来源是什么
- 应避免价值判断和宣传性语言
- 不应只是重复 `title`
- 不应写成长段背景说明

## `tags` 要求

- `tags` 是可选字段
- 如果填写，必须使用单行数组语法
- 值应简短、客观、便于检索
- 不要把句子、评价或正文摘要塞进 `tags`

示例：

```yaml
tags: [敦煌, 壁画, 古籍]
```

## 正文建议结构

正文建议使用以下结构：

- `## 来源概述`
- `## 收录内容与边界`
- `## 获取方式`
- `## 使用与访问限制`
- `## 质量与风险`

各 section 的边界如下：

- `来源概述`：说明这个来源是什么，由谁维护，为什么它可以作为一个稳定的数据集来源。
- `收录内容与边界`：说明它实际收录什么，不收录什么，覆盖范围和粒度如何。
- `获取方式`：说明如何浏览、检索、下载、调用，入口是否稳定，是否提供批量获取方式。
- `使用与访问限制`：说明登录、申请、授权、版权、引用要求等限制条件。
- `质量与风险`：说明完整性、稳定性、结构化程度、已知问题和失效风险。

## 校验边界

自动化工具优先校验以下内容：

- 文件名是否合规
- 文件名是否只使用英文字符、数字和连字符，不含中文字符
- 是否存在以 `---` 包裹的 YAML front matter
- 必填字段是否齐全
- `tags` 如果出现，是否为合法数组
- `modality` 和 `access_level` 是否命中枚举
- 是否出现未定义的额外 meta 字段

正文内容本身不作为严格校验对象；自动化工具主要校验文件名、YAML 结构、必填字段和枚举字段。

# Accepted 规范

## 定义

`accepted/` 中的记录表示：某个数据集来源已经过核验，确认真实存在，并值得在仓库中保留。

这里记录的是“来源”，不是数据集文件本身。

## 文件形式

- 每条记录对应一个 Markdown 文件
- 文件放在 `accepted/` 目录下
- 文件名规则见 [`docs/naming.md`](/Users/xianqiu/Projects/youpu-sources/docs/naming.md)

## 标准结构

accepted 文档由三部分组成：

1. 一级标题 `# 标题`
2. YAML 元信息块
3. 正文内容

示意：

````md
# 标题

```yaml
title: ...
canonical_url: ...
...
```

## 数据集概览
...
````

## 关于历史遗留内容

部分历史 Markdown 文件来自 Notion 导出，标题与 YAML 之间包含额外文字，例如：

- `描述`
- `数据类型`
- `标签`
- `访问方式`
- `协议`
- `序号`
- `状态`

这部分内容不视为标准结构，也不作为后续校验工具的必检对象。

当前阶段不要求清洗历史文件，但新提交内容应尽量以 YAML 和正文作为主结构。

## YAML 字段要求

当前阶段采用精简字段集，只保留后续查询和展示所需的核心字段。

### 必填字段

以下字段必须存在，且应填写明确值：

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

说明：

- `title`：来源名称。
- `canonical_url`：该来源的稳定主链接，作为 accepted 内部去重与后续交叉校验的主标识。
- `domain`：所属主题领域，例如文化资源。
- `content_type`：内容类型，例如素材、名录、目录入口等。
- `data_form`：数据呈现形态，例如文本、结构化表 / API、多媒体。
- `data_type`：主要数据类型，例如图像、文本、表格、JSON、混合。
- `region`：地理覆盖范围。
- `source_type`：来源机构类型，例如学术机构、政府开放平台、开源社区。
- `source_org`：来源机构名称。
- `permissions`：访问或使用权限的简要判断，例如公开、需申请、不明。
- `tags`：检索标签。
- `use_cases`：适用场景。

### `region` 的占位值

`region` 允许使用标准占位值，例如：

- `不明`
- `待确认`
- `不适用`

## tags 和 use_cases 的要求

- `tags` 应为数组
- `use_cases` 应为数组
- 值应简洁、可检索、避免句子化

示例：

```yaml
tags: [敦煌, 壁画, 图像修复, 文物修复]
use_cases: [研究分析, AI训练]
```

## 标题要求

- 正文应保留一级标题 `# 标题`
- YAML 中必须包含 `title`
- 正文 H1 与 YAML `title` 必须一致

## 链接要求

- YAML 中必须包含 `canonical_url`
- `canonical_url` 应填写该来源的稳定主链接
- 应尽量使用规范化后的主链接，避免追踪参数与无意义锚点
- 具体规则见 [`docs/url-normalization.md`](/Users/xianqiu/Projects/youpu-sources/docs/url-normalization.md)

## 正文建议结构

当前阶段正文不做严格校验，但建议尽量保持以下结构：

- `## 数据集概览`
- `## 数据内容说明`
- `## 数据获取方式`
- `## 使用限制与合规说明`
- `## 数据质量与已知问题`
- `## 备注`

## 校验边界

后续自动化工具优先校验以下内容：

- 文件名是否合规
- 是否存在 H1 标题
- 是否存在 YAML 元信息块
- 必填字段是否齐全
- H1 标题与 YAML `title` 是否一致
- `tags` 和 `use_cases` 是否为数组

正文和历史遗留的 Notion 导出文字暂不作为严格校验对象。

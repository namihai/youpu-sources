# Accepted 规范

## 定义

`data/accepted/` 中的记录表示：某个数据集来源已经过核验，确认真实存在，并值得在仓库中保留。

这里记录的是“来源”，不是数据集文件本身。

## 文件形式

- 每条记录对应一个 Markdown 文件
- 文件放在 `data/accepted/` 目录下
- 文件名遵循统一命名规则

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
- `slug` 为简短英文或拼音
- 文件扩展名固定为 `.md`

`slug` 要求：

- 使用小写字母、数字和连字符 `-`
- 保持简短，便于人工识别
- 不要求完整表达中文标题
- 不建议包含随机 hash
- 不建议直接使用超长中文标题

维护者如果要在本地调试 accepted 导入流程，可以按下面方式验证：

1. 用户先把候选 Markdown 放进 `staging/accepted/`
2. 运行 `youpu validate-imports`
3. 修正问题后运行 `youpu ingest`

`ingest` 会在正式合并时：

- 自动计算下一个编号
- 优先根据 staging 文件名生成 `slug`
- 生成 `SRC-####-slug.md`
- 写入正式 accepted 文件名

不建议使用以下命名方式：

- 中文全标题加随机字符串
- `Untitled`
- 带空格的超长文件名
- 以 URL 直接作为文件名

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

## YAML 字段要求

accepted 记录使用精简字段集，只保留查询、校验和展示所需的核心字段。

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
- `canonical_url`：来源的 `canonical_url`，通常应填写介绍该数据集或来源的数据集主页，作为 accepted 内部去重与交叉校验的主标识。它一般不是下载链接。下载链接应在 Markdown 正文中单独说明；如果该数据集没有独立主页、只有下载链接，可将下载链接作为 `canonical_url`。
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
- `canonical_url` 应尽量填写该来源的数据集主页或详情页，而不是下载直链
- 如果没有独立主页、只有下载链接，可以使用下载链接作为 `canonical_url`
- 应尽量使用规范化后的主链接，避免追踪参数与无意义锚点
- 输入阶段可以先使用原始 URL；系统会在校验和入库时按统一规则规范化
- 具体规则见 [`url.md`](url.md)

## 正文建议结构

正文建议尽量保持以下结构：

- `## 数据集概览`
- `## 数据内容说明`
- `## 数据获取方式`
- `## 使用限制与合规说明`
- `## 数据质量与已知问题`
- `## 备注`

## 校验边界

自动化工具优先校验以下内容：

- 文件名是否合规
- 是否存在 H1 标题
- 是否存在 YAML 元信息块
- 必填字段是否齐全
- H1 标题与 YAML `title` 是否一致
- `tags` 和 `use_cases` 是否为数组

正文内容本身不作为严格校验对象；自动化工具主要校验文件名、H1、YAML 结构和必填字段。

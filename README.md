# youpu-sources

这个仓库用于记录已经过核验的数据集来源结论，不收集数据集本身，也不承载个人工作流。

仓库当前只保留两类有结论的结果：

- `accepted/`：已确认真实有效、值得保留的数据集来源记录。每条记录为一个 Markdown 文件。
- `rejected/rejected.csv`：已确认不保留的数据集来源记录。每条记录为一行 CSV。

不纳入本仓库的内容：

- 个人采集流程
- 中间验证过程
- Notion 页面和临时笔记
- 待处理、进行中、待复核等过程状态
- 数据集文件本体

## 目录结构

```text
.
├── accepted/
├── rejected/
│   └── rejected.csv
├── docs/
│   ├── accepted-spec.md
│   ├── rejected-spec.md
│   └── naming.md
├── templates/
│   └── accepted.md
└── tools/
    └── validate/
```

## accepted 记录

`accepted/` 中每个文件表示一个已确认有效的数据集来源。

约束：

- 一个来源对应一个 Markdown 文件
- 文件名遵循统一命名规则，见 [`docs/naming.md`](/Users/xianqiu/Projects/youpu-sources/docs/naming.md)
- 文档主体采用统一模板，见 [`templates/accepted.md`](/Users/xianqiu/Projects/youpu-sources/templates/accepted.md)
- 当前阶段以 YAML 元信息为主要规范对象
- 标题与 YAML 之间可能存在历史遗留的 Notion 导出文字，这部分不视为标准结构
- 正文保留 `# title`，并要求与 YAML `title` 一致

accepted 当前只保留以下字段：

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

accepted 的详细规范见 [`docs/accepted-spec.md`](/Users/xianqiu/Projects/youpu-sources/docs/accepted-spec.md)。

其中 `canonical_url` 表示该来源的稳定主链接，用于 accepted 内部去重和后续与 `rejected.csv` 的交叉检查。

## rejected 记录

`rejected/rejected.csv` 用于记录已确认不保留的数据集来源。

字段：

- `url`
- `title`
- `reason`

其中 `url` 应填写规范化后的 `canonical_url`，作为 rejected 记录的唯一标识。

rejected 的详细规范见 [`docs/rejected-spec.md`](/Users/xianqiu/Projects/youpu-sources/docs/rejected-spec.md)。

## URL 规范

`rejected.csv` 中的 `url` 应为规范化后的 `canonical_url`。填写时遵循以下原则：

- 优先使用来源页面的稳定主链接
- 尽量去掉追踪参数，例如 `utm_*`
- 去掉无意义锚点，例如 `#intro`
- 对同一资源的不同跳转链接，应尽量归并为同一个主链接
- 如果站点同时提供详情页和下载页，优先记录更能代表该来源的主页面链接

accepted 文档中也应尽量明确给出对应的真实主链接，以便后续工具做比对和校验。

当前仓库只保留规范化后的 `accepted/` 与 `rejected/` 结果，不再保留历史中间目录与过程性草稿。

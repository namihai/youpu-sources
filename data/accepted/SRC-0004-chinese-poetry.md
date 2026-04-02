# 中国古诗词数据库（chinese-poetry，GitHub）

```yaml
title: 中国古诗词数据库（chinese-poetry，GitHub）
canonical_url: https://github.com/chinese-poetry/chinese-poetry
domain: 文化资源
content_type: 素材
data_form: 文本
data_type: JSON
region: 不适用
source_type: 开源社区
source_org: chinese-poetry（GitHub）
permissions: 公开可下载
tags: [古诗词, 语料库, 数字人文, 语言资源, 开源, 自然语言处理]
use_cases: [研究分析, AI训练, 产品选题]
```

## 数据集概览

- **数据集名称**：中国古诗词数据库（chinese-poetry，GitHub）
- **覆盖内容**：该仓库以 JSON 形式分发古典诗词与相关元数据，并在说明中提到包含唐诗、宋诗、宋词等多个子集；具体字段与是否包含注释/译文/异体字处理规则需以仓库文件结构核验。
- **核心价值**：以工程友好的结构化格式提供可直接用于检索、统计分析与建模训练的古典诗词文本底座，适合数字人文与中文 NLP 场景。
- **适用场景**：古典文学检索与知识库、诗词文本挖掘、风格与主题分析、语言模型训练与评测（需自定清洗与切分口径）。

## 数据内容说明

1. 数据对象与边界：古典诗词作品文本与元数据（作品、作者、朝代等；以仓库现有字段为准）。
2. 数据组织方式：按子集/朝代/文集拆分为多个 JSON 文件或目录（以仓库为准）。
3. 数据量：不明/待确认（仓库可能提供规模说明，建议落库时补齐版本口径）。

## 数据获取方式

### 代码 / Repo

- **Repo**：[https://github.com/chinese-poetry/chinese-poetry](https://github.com/chinese-poetry/chinese-poetry)
- **包含内容**：数据文件（JSON）、结构说明与可能的处理脚本（以仓库内容为准）。
- **快速使用**：Git clone 或下载 ZIP 获取数据。

### 文件下载

- **下载地址**：[https://github.com/chinese-poetry/chinese-poetry](https://github.com/chinese-poetry/chinese-poetry)
- **格式**：JSON
- **说明**：公开下载。

## 使用限制与合规说明

- **版权归属**：不明/待确认（需核验数据来源与仓库声明）。
- **使用许可**：MIT（以仓库 LICENSE 为准）。
- **禁止事项**：不明/待确认（以 LICENSE 与仓库声明为准）。
- **合规依据**：MIT License。
- **敏感性**：一般不涉及个人信息。

## 数据质量与已知问题

- **完整性**：不明/待确认（不同子集可能字段不一致或缺少部分元数据）。
- **一致性**：作者名、篇名异体字与版本差异可能导致重复或不一致，需要做实体对齐与去重。
- **时效性**：更新不定期。
- **稳定性**：GitHub 链接稳定性较高，建议落库时记录具体 commit 或 release 版本。

## 备注

它最独特的是以统一 JSON 结构分发多子集古典诗词语料，因此适合快速做检索与建模；但受限于来源与字段口径不明，落库前需要补齐字段说明与权利声明。

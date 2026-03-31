# 中文诗歌总集

```yaml
title: 中文诗歌总集
canonical_url: https://github.com/open-chinese/poetry-collection
domain: 文化资源
content_type: 文本
data_form: 文本
data_type: JSON
region: 不适用
source_type: 开源社区
source_org: open-chinese（GitHub）
permissions: 公开可下载
tags: [古诗词, 语料库, JSON, 开源]
use_cases: [研究分析, AI训练, 产品选题]
```

## 数据集概览

- **数据集名称**：中文诗歌总集（统一 Schema，MIT）
- **覆盖内容**：以统一 JSON schema 汇编多朝代诗歌文本，仓库口径声称规模约 37 万首作品；汇编型语料常见重复、来源混杂与版本差异，需配套清洗与去重策略。
- **核心价值**：统一 schema 能显著降低跨朝代/跨来源的字段适配成本，适合工程化批量处理、检索与建模；严谨研究场景建议抽样校验并固化版本。
- **适用场景**：诗歌检索与推荐、跨朝代比较分析、古文 NLP 训练、教育内容产品（建议先做作者/朝代规范与去重）。

## 数据内容说明

1. 数据对象与边界：诗歌作品文本与基本元数据（字段以仓库 schema 为准）。
2. 数据组织方式：JSON 文件集合，统一字段结构。
3. 数据量：约 37 万首（仓库口径，需核验统计口径）。

## 数据获取方式

### 代码 / Repo

- **Repo**：[https://github.com/open-chinese/poetry-collection](https://github.com/open-chinese/poetry-collection)
- **包含内容**：JSON 数据、schema 与说明（以仓库为准）。

### 文件下载

- **下载地址**：[https://github.com/open-chinese/poetry-collection](https://github.com/open-chinese/poetry-collection)
- **格式**：JSON
- **说明**：公开下载。

## 使用限制与合规说明

- **版权归属**：不明/待确认
- **使用许可**：MIT（以仓库 LICENSE 为准）。
- **禁止事项**：不明/待确认
- **合规依据**：MIT License。
- **敏感性**：无个人信息。

## 数据质量与已知问题

- **完整性**：规模大，但不同朝代覆盖与质量可能不均。
- **一致性**：来源混杂可能导致文本版本、标点、作者名规范不一致，需要清洗与对齐。
- **时效性**：不定期更新。
- **稳定性**：GitHub 稳定；建议固化版本与清洗规则。

## 备注

它最独特的是用统一 JSON schema 汇编大规模诗歌语料，因此适合工程化批量处理；但受限于汇编来源差异，落库前需要建立可复现的去重与版本固化流程。

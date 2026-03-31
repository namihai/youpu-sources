# M+ 博物馆藏品元数据数据集

```yaml
title: M+ 博物馆藏品元数据数据集
canonical_url: https://github.com/mplusmuseum/collection-data
domain: 文化资源
content_type: 名录
data_form: 结构化表
data_type: CSV / JSON
region: 香港
source_type: 学术机构
source_org: M+ Museum
permissions: 公开可下载
tags: [博物馆藏品, 元数据, 开放数据, CC0]
use_cases: [研究分析, 知识组织, 产品选题]
```

## 数据集概览

- **数据集名称**：M+ 博物馆藏品元数据数据集（CC0）
- **覆盖内容**：提供约 9,300 条藏品元数据记录，以 CSV/JSON 形式分发，并明确不包含图像（出于权利限制）。
- **核心价值**：许可为 CC0 且可批量获取，使其非常适合作为“藏品目录索引与字段规范参考”的底座，工程与合规成本低，可用于跨库对齐与知识组织。
- **适用场景**：藏品检索原型、元数据字段规范与映射、知识图谱/实体对齐、内容策划索引（作为主索引再挂接外部影像来源）。

## 数据内容说明

1. 数据对象与边界：藏品条目元数据（字段以仓库数据字典为准）。
2. 数据组织方式：提供 CSV/JSON 数据文件与说明。
3. 数据量：约 9,300 条记录。

## 数据获取方式

### 代码 / Repo

- **Repo**：[https://github.com/mplusmuseum/collection-data](https://github.com/mplusmuseum/collection-data)
- **包含内容**：CSV/JSON 数据、更新记录与说明（以仓库为准）。

### 文件下载

- **下载地址**：[https://github.com/mplusmuseum/collection-data](https://github.com/mplusmuseum/collection-data)
- **格式**：CSV / JSON
- **说明**：公开下载。

## 使用限制与合规说明

- **版权归属**：不明/待确认
- **使用许可**：CC0（元数据）；图像不包含在内（以仓库声明为准）。
- **禁止事项**：不明/待确认
- **合规依据**：CC0 1.0。
- **敏感性**：无个人信息。

## 数据质量与已知问题

- **完整性**：元数据覆盖范围受馆藏编目进度影响。
- **一致性**：字段相对规范，但跨语种、年代、作者表示仍可能需要清洗。
- **时效性**：不定期更新。
- **稳定性**：GitHub 托管稳定，建议落库时记录版本（release/commit）。

## 备注

它最独特的是提供 CC0 且可批量下载的藏品元数据主索引，因此适合做知识组织与对齐；但不包含图像，视觉相关任务需另接入影像来源。

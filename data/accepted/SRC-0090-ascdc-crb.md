# ASCDC 中文古籍 LOD 数据集（CRB）

```yaml
title: ASCDC 中文古籍 LOD 数据集（CRB）
canonical_url: https://lod-cloud.net/dataset/ASCDC-CRB
domain: 文化资源
content_type: 素材
data_form: 结构化
data_type: 表格
region: 台湾 / 中文古籍相关
source_type: 学术机构
source_org: ASCDC
permissions: 公开可访问
tags: [古籍, LOD, RDF, 数字人文]
use_cases: [研究分析, 知识组织]
```

## 数据集概览

- **数据集名称**：ASCDC 中文古籍 LOD 数据集（CRB）
- **覆盖内容**：将中文古籍相关书目/条目以 LOD/RDF 方式组织，便于做跨库链接与语义检索；更偏“语义关系层”，不是全文内容。
- **核心价值**：适合做“古籍目录的知识图谱化”，用于实体对齐、版本关系、作者关系等；但落地通常需要SPARQL/本体映射与外部资源挂接。
- **适用场景**：数字人文研究、古籍目录聚合、知识图谱与语义检索（适合先做小范围对齐试点）。

## 数据内容说明

1. 以RDF triples/LOD为核心（字段与本体以平台说明为准）。
2. 更适合作为上层系统的语义底座，而非直接阅读型资源。
3. 若要与全文/影像结合，需要额外挂接外部资源链接。

## 数据获取方式

### 网页访问

- **链接**：[https://lod-cloud.net/dataset/ASCDC-CRB](https://lod-cloud.net/dataset/ASCDC-CRB)
- **说明**：从LOD-cloud登记页跳转到下载/查询入口。

## 使用限制与合规说明

- **使用许可**：登记信息称为开放许可（细则以平台说明为准）。
- **敏感性**：无个人隐私。

## 数据质量与已知问题

- **完整性**：覆盖范围取决于数据集收录口径。
- **一致性**：LOD结构一致性强，但跨数据集本体差异仍需映射。
- **稳定性**：依赖平台与下载镜像。


## 备注

中文古籍目录LOD语义层数据，用于实体对齐与关系查询（需SPARQL/本体映射，建议先小范围试点）。

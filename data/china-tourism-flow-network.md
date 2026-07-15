---
title: "中国旅游流动网络数据集"
summary: "基于游记行程序列构建的中国旅游POI流动网络数据集，包含POI元数据和有向转移边。"
canonical_url: "https://doi.org/10.6084/m9.figshare.30184726"
publisher: "Figshare"
modality: "tabular"
access_level: "open"
tags: ["旅游流动", "POI", "网络数据", "游记", "地理数据", "CSV", "Figshare", "CC BY 4.0"]
---

# 中国旅游流动网络数据集
## 要点
- 数据大小：25.93MB。
- 包含POI元数据与游记访问序列。
- 许可协议：CC BY 4.0
- URL：https://doi.org/10.6084/m9.figshare.30184726
## 数据内容
这是一个基于游记行程序列构建的中国旅游 POI 流动网络数据集。它包含两类基础信息：
- POI 元数据：景点/地点 ID、中文名、英文名、城市、GCJ-02 坐标、标签。
- 游记访问序列：匿名游记 ID、抓取日期、出发日期、同行关系、按顺序访问的 POI ID 列表。
由访问序列进一步派生出网络数据：
- 节点`Nodes_*`：参与某类网络转移的 POI。
- 边`Edges_*`：从一个 POI 到下一个 POI 的有向转移。
- `Weight`：同一有向转移在所有行程中出现的次数。
## 原始数据规模
| 文件 | 行数 | 字段 |
|---|---:|---|
| `POIs_V2.csv` | 23,736 | `Encrypted_ID`, `Name_ZH`, `Name_EN`, `City_ZH`, `City_EN`, `Latitude_GCJ02`, `Longitude_GCJ02`, `Label_ZH`, `Label_EN` |
| `Visit_Sequences_V2.csv` | 68,531 | `Anonymized_Blog_ID`, `Retrieval_Date`, `Departure_Date`, `Travel_Partners`, `Visit_Sequence` |

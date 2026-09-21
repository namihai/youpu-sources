---
title: "欧洲文化遗产数字平台（Europeana）"
summary: "汇聚欧洲数千家文化机构的数字文化遗产，提供超过 6,000 万项资源的检索入口。"
canonical_url: "https://www.europeana.eu/en"
publisher: "Europeana"
modality: "multimodal"
access_level: "open"
tags: [API, 元数据, 博物馆藏品, 开放数据, 数字人文, 数字馆藏, 文化遗产, 机器学习]
---

# 欧洲文化遗产数字平台（Europeana）

## 亮点

- 汇聚欧洲数千家文化机构的数字文化遗产，提供超过 6,000 万项资源的检索入口。
- 资源类型包括图像、文本、声音、视频和三维对象，内容覆盖艺术、考古、报刊、时尚、音乐、科学和体育等主题。
- 采用欧洲文化遗产数据模型（Europeana Data Model，EDM）组织元数据，关联文化对象、数字资源及人物、地点等背景信息。
- 支持网页检索、API 查询、元数据批量下载和 OAI-PMH 元数据采集。
- 许可协议：元数据采用 CC0 1.0；具体数字对象及预览内容按各条目的权利声明使用。
- URL：https://www.europeana.eu/en

## 资源内容与来源

Europeana 由欧洲数字图书馆基金会（Europeana Foundation）运营，汇集美术馆、图书馆、档案馆、博物馆等机构提供的文化遗产资源。平台通过聚合机构网络接收数据：聚合机构收集馆藏条目及相关描述，进行检查、整理与信息补充，再将资源接入统一检索体系。[平台介绍](https://www.europeana.eu/en/about-us)

资源按媒体形态分为图像、文本、声音、视频和三维对象，包含艺术作品、图书、报刊、音乐与影像等内容。艺术、考古、时尚、科学、体育等属于主题维度，与媒体类型分别组织；同一主题可包含多种媒体资源。

平台记录连接馆藏描述、预览内容和来源机构的访问入口。元数据由不同机构提供，数字对象的展示、下载和访问条件随条目而异。Europeana 持续修订元数据、补充新信息，资源规模和记录内容也随之变化。[数据来源](https://www.europeana.eu/en/rights/europeana-data-sources)；[元数据使用说明](https://www.europeana.eu/en/rights/usage-guidelines-for-metadata)

## 元数据组织与关联

Europeana 使用 EDM 整合不同文化机构的描述体系，兼容博物馆、档案馆和数字图书馆等领域的元数据标准。其组织方式区分文化遗产对象与对象的数字化呈现，并保留两者之间的联系。

除对象本身的描述外，EDM 还支持关联人物、地点、概念和事件等背景资源，并通过权威词表与外部知识库补充语义信息。对于数字化图书等复杂对象，模型能够表达整体与章节、插图、补充材料之间的关系，也能连接同一对象的多种数字呈现形式。不同记录实际包含的信息取决于来源机构提供的数据及后续补充情况。[EDM 官方说明](https://europeana.atlassian.net/wiki/spaces/EF/pages/2916974597/Europeana+Data+Model)

## 检索与数据获取

网站提供统一搜索入口；程序化访问则包括以下主要接口：

| 获取方式 | 主要内容 |
|---|---|
| Search API | 检索元数据记录与媒体资源，返回 JSON 格式的结果摘要，支持条件筛选和分页 |
| Record API | 获取单个条目的详细信息 |
| IIIF APIs | 提供对象的结构化描述，并支持在兼容查看器中展示二维数字资源 |
| 元数据批量下载 | 按数据集提供 ZIP 压缩包，包含 RDF/XML 或 Turtle 格式的元数据记录 |
| OAI-PMH 服务 | 按数据集或记录创建、修改日期采集元数据，返回 EDM RDF/XML |

Search API 可按关键词查询，并结合权利状态、是否具有可访问媒体链接、是否具有缩略图等条件筛选；也可限定艺术、手稿、地图、音乐、报刊、摄影等主题集合。接口返回的搜索摘要与单条记录的完整描述分别由 Search API 和 Record API 提供。[检索接口文档](https://europeana.atlassian.net/wiki/spaces/EF/pages/2385739812/Search+API+Documentation)

API 密钥可免费申请，申请前需注册 Europeana 账户。批量下载按数据集组织，每个压缩包包含该数据集的元数据记录；OAI-PMH 则支持按创建或修改时间选择记录。上述元数据下载与原始图像、音视频文件的获取是不同的操作，数字资源仍需通过条目中的媒体链接或来源机构页面访问。[API 入口](https://api.europeana.eu/en)；[批量下载与 OAI-PMH 文档](https://europeana.atlassian.net/wiki/spaces/EF/pages/2324463617/Dataset+download+and+OAI-PMH+service)

## 访问与授权

Europeana 发布的元数据采用 CC0 1.0。平台在元数据使用指引中请求使用者标明来源机构、参与聚合的机构及 Europeana，并尽可能保留原始资源链接；该指引明确说明，这些要求属于使用倡议，不是额外的法律合同。

图像、声音、视频、三维对象及其预览内容各自具有权利信息，不能因描述它们的元数据采用 CC0，就将数字资源一并视为 CC0。具体使用条件由条目附带的权利声明表示，机器可读记录中使用 `edm:rights` 等字段传递相关信息；缺少权利说明时，需进一步查看来源机构页面。[使用条款](https://www.europeana.eu/en/rights/terms-of-use)

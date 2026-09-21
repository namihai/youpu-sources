---
title: "中国非物质文化遗产传播数据集（Communication of Chinese Intangible Heritage）"
summary: "收录 2,500 条中国非物质文化遗产（ICH）在全球主流社交媒体平台的国际传播内容记录。"
canonical_url: "https://www.kaggle.com/datasets/colabsss/communication-of-chinese-intangible-heritage"
publisher: "colabsss"
modality: "multimodal"
access_level: "open"
tags: [非物质文化遗产, 传播, 多模态, Kaggle, 文化研究]
---

# 中国非物质文化遗产传播数据集（Communication of Chinese Intangible Heritage）

## 亮点

- 收录 2,500 条中国非物质文化遗产（ICH）在全球主流社交媒体平台的国际传播内容记录。
- 每条记录含多模态属性（图像/视频/文本）、叙事与视觉风格、语言及平台传播特征，并附点赞、评论、分享、浏览量、互动率等受众互动指标。
- 附 target_label 结果列标注国际传播效果等级，可做跨平台、跨非遗类别、跨呈现方式的传播效果比较。
- 单一 CSV 表格（约 683 KB），不含外部媒体文件；采用 CC0（公有领域）许可，可自由使用。
- URL：https://www.kaggle.com/datasets/colabsss/communication-of-chinese-intangible-heritage

## 项目概述

中国非物质文化遗产传播数据集（Kaggle 标识 colabsss/communication-of-chinese-intangible-heritage，现名 Communication of Chinese Intangible Heritage，副题 Multimodal Content and Audience Engagement Analysis）收录了 2,500 条记录，刻画中国非物质文化遗产在全球主流社交媒体平台上的国际传播情况。每条记录代表一件用于向国际受众推广中国非遗的数字内容，整合了多模态内容特征（图像、视频、文本）、叙事与视觉呈现风格、语言使用以及平台特有的传播属性，并附点赞、评论、分享、浏览量、互动率等受众互动指标，便于系统考察不同文化类别、叙事策略与媒体组合如何影响全球受众反应与传播效果。

## 收录内容与规模

数据集共 2,500 条记录，以单一 CSV 文件（Multimodal_Communication_Dataset.csv，约 683 KB）存储，不含外部媒体文件。每条记录含 22 个字段：content_id（唯一标识）、platform（传播平台）、ich_category（非遗类别）、data_modality（媒体模态组合）、media_type（主要数字媒体格式）、image_available / video_available / text_available（是否含相应模态）、text_description（面向国际受众的描述性叙事）、language（跨文化传播所用语言）、duration_sec（视频时长，秒）、visual_style（视觉呈现风格）、storytelling_type（叙事策略）、visual_features / text_features（视觉与文本特征编码）、selected_features（对传播效果贡献最大的关键内容属性），以及 likes（点赞数）、comments（评论数）、shares（分享数）、views（浏览量）、engagement_rate（互动率）等受众互动指标。

## 组织方式与检索

数据集为表格化结构，target_label 为目标列，表示国际传播效果等级，可用于跨平台、跨非遗类别、跨呈现方式的传播效果比较；likes、comments、shares、views、engagement_rate 等字段量化受众互动与传播范围，image_available、video_available、text_available 及 data_modality 字段描述多模态组合情况。数据面向国际文化传播、数字遗产推广、多媒体内容分析与社交媒体互动评估等研究，支持描述性与分析性研究目标，无需依赖外部媒体文件。

## 访问与使用条件

数据集由 Kaggle 用户 Colabsss 发布，采用 CC0（Public Domain，公有领域）许可，可自由使用、修改与再分发。数据当前为第 1 版，Kaggle 可用性评分为 0.647，最近更新于 2025 年 12 月。

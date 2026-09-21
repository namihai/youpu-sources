---
title: "中国历代人物传记资料库（CBDB）"
summary: "收录约 649,533 位中国历史人物（截至 2025 年 5 月），主体为 7 至 19 世纪（唐五代至明清）人物。"
canonical_url: "https://projects.iq.harvard.edu/cbdb"
publisher: "Harvard University / Academia Sinica / Peking University"
modality: "tabular"
access_level: "open"
tags: [历史人物, 传记资料, 关系数据库, 中国史, 数字人文]
---

# 中国历代人物传记资料库（CBDB）

## 亮点

- 收录约 649,533 位中国历史人物（截至 2025 年 5 月），主体为 7 至 19 世纪（唐五代至明清）人物。
- 关系型数据库，记录人物基本信息、别名、籍贯、亲属关系、社会关系、任职经历与文献出处。
- 提供在线查询与录入系统，并可下载 Microsoft Access、SQLite 两种单机版。
- 由哈佛大学费正清中国研究中心、中研院历史语言研究所、北京大学中国古代史研究中心联合建设。
- 免费开放获取，供学术使用，无使用限制。
- URL：https://projects.iq.harvard.edu/cbdb

## 数据内容与来源

中国历代人物传记资料库（China Biographical Database，CBDB）是免费开放的关系型数据库，收录中国历史人物的传记资料。截至 2025 年 5 月约收录 649,533 人，主体为 7 至 19 世纪（唐代至清代）人物，数据适用于统计分析、社会网络分析、空间分析，也可作为传记参考资料。项目的长期目标是系统收录中国历史记载中所有重要的传记材料，并持续为唐、五代、辽、宋、金、元、明、清各代补充新条目。

数据库源自 Robert M. Hartwell（1932–1996）的工作；Hartwell 将遗产连同数据库的首个版本遗赠哈佛燕京学社。此后 Peter K. Bol 负责项目，Michael A. Fuller 重新设计，高级项目经理为 Hongsu Wang。目前由哈佛大学费正清中国研究中心、中研院历史语言研究所、北京大学中国古代史研究中心三方联合建设。

## 数据组织

数据库以人物记录为核心，围绕每位人物关联多种信息：别名（alternative names）、籍贯与地址（biographical addresses）、亲属关系（kinship）、社会关系（social associations，含书信往来、同僚等）、任职经历（posting records）、社会身份（social status），以及指向史料来源的文献出处（entry records）。任官信息由一套任官代码表组织，2025 年 5 月的版本将原任官类型代码表拆分为 APPOINTMENT_CODES、APPOINTMENT_TYPES 与 APPOINTMENT_CODE_TYPE_REL 等表。

SQLite 单机版的原始导出不含便捷视图与反规范化的 ADDRESSES 表，需用官方脚本另行生成：可为各表添加外键约束、创建 18 个便捷视图（如 View_PeopleData、View_EntryData、View_PostingOfficeData），并构建按时间解析完整行政层级的 ADDRESSES 表，也可通过 Colab 笔记本一键完成。

## 版本与更新

单机版 Microsoft Access 格式的最新版本为 CBDB_bi_20250520（2025-05-21 起提供），含 649,533 位男女人物。该版本新增内容包括：据《宋登科记考》补充 4,138 人及其条目、别名、籍贯；据《明清戏曲序跋纂笺》补充 363 位剧作家及相关别名、任职、籍贯与条目；据《国朝画识》补充 545 位清初至中期画家；据《全元文》墓志补充 513 人。同期众包组、北京大学编辑组与人民大学（Renmin）编辑组另对数万条记录新增或修改。SQLite 版本持续更新，最新导出为 2026-09-14 生成的 cbdb_20260914.sqlite3。

## 获取与访问

CBDB 提供在线与离线两种使用方式。在线查询系统由引得项目（Inindex）提供（inindex.com/biog），免费注册后可使用详细信息、可视化与文本库功能；另有在线录入系统（input.cbdb.fas.harvard.edu），可查看数据的录入方式、所用代码及任意人物信息，但为只读，不能保存修改。

离线可下载单机版，格式包括 Microsoft Access 与 SQLite。SQLite 版本的下载与处理脚本托管于 GitHub 仓库 cbdb-project/cbdb_sqlite，最新发布与历史版本另托管于 Hugging Face 数据集页 cbdb/cbdb-sqlite。数据库还提供 CBDB API，可按人物 CBDB ID 或姓名（中文或拼音）查询并返回 JSON，供其他系统实时调用。

## 授权与引用

数据库内容免费开放，供学术使用且无使用限制。项目给出的引用格式为：Harvard University, Academia Sinica, and Peking University, China Biographical Database (August 2021), https://projects.iq.harvard.edu/cbdb。

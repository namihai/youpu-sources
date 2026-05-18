---
title: "中国古代手写字符数据库（CASIA-AHCDB）"
summary: "CASIA-AHCDB 中国古代手写字符数据库：2,264,285 个标注字符样本、12,229 类，来源于 12,000+ 页古代手写文档；分 Style1（四库全书）与 Style2（佛经）两子库；提供 GNTX 格式与多子集下载。"
canonical_url: "https://nlpr.ia.ac.cn/pal/CASIA-AHCDB.html"
publisher: "中国科学院自动化研究所（CASIA）"
modality: "image"
access_level: "request"
tags: [机器学习, 计算机视觉]
---

## 来源概述
CASIA-AHCDB 中国古代手写字符数据库：2,264,285 个标注字符样本、12,229 类，来源于 12,000+ 页古代手写文档；分 Style1（四库全书）与 Style2（佛经）两子库；提供 GNTX 格式与多子集下载。

## 收录内容与边界
1. 数据对象与边界：字符识别用的标注字符样本（bitmap）及其类别（Unicode/类）；样本来自古代手写文档页面的字符切分与标注。
2. 数据组织方式：按来源分为两大子库：
    - Style1：四库全书（Complete Library in Four Sections）
    - Style2：古佛经（Ancient Buddhist Scriptures）
    
    并按应用划分为 basic / enhanced / reserved 三类集合（reserved 因样本少不再划分训练/测试）。
    
3. 规模与粒度：总计 12,229 类、2,264,285 个字符样本（以官网统计表为准）。
4. 训练/测试划分（官网说明）：
    - Style1：25 本书（book_01–book_25），book_01–20 为训练集，book_21–25 为测试集（部分书由同一书写者书写）。
    - Style2：10 个时期的佛经卷，period_09–10 为训练集，period_01–08 为测试集。
5. 数据格式：官网给出 GNTX 格式字段说明（sample size、Unicode、width、height、bitmap 等）。

## 获取方式
需申请

## 使用与访问限制
需申请；具体许可、引用和再利用边界应以来源页面声明为准。

## 质量与风险
- **完整性**：类别多但长尾类别可能样本稀少。
- **一致性**：不同子集扫描质量与噪声类型差异大，训练需分层抽样与增强。
- **时效性**：不明/待确认
- **稳定性**：依赖申请渠道与维护方支持，稳定性存疑。

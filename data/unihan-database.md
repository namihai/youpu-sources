---
title: "统一汉字属性数据库（Unihan）"
summary: "Unicode 联盟建置的汉字属性数据库，即《Unicode 标准附录 #38》（UAX #38，Unicode Han Database），是 Unicode 标准关于汉字（表意文字）的权威数据规范。"
canonical_url: "https://www.unicode.org/reports/tr38/"
publisher: "Unicode Consortium"
modality: "text"
access_level: "open"
tags: [汉字, Unicode, 字符属性, 编码, 文字学]
---

# 统一汉字属性数据库（Unihan）

## 亮点

- Unicode 联盟建置的汉字属性数据库，即《Unicode 标准附录 #38》（UAX #38，Unicode Han Database），是 Unicode 标准关于汉字（表意文字）的权威数据规范。
- 当前对应 Unicode 17.0.0，覆盖 102,998 个汉字（含 17.0 新增的 CJK 统一表意文字扩展 J 区 4,298 字）。
- 属性按类别组织，属性名均以小写字母 k 开头，涵盖读音（粤语、普通话、日、韩、越等）、字典索引、英文释义、部首笔画、简繁/语义/防伪变体及与其它字符集（GB、JIS、CNS 等）的映射。
- 数据以 Unihan.zip 随 Unicode 字符数据库（UCD）发布，为 8 个 UTF-8、NFC、Unix 行尾的文本文件；遵循 UNICODE LICENSE V3，免费开放使用。
- URL：https://www.unicode.org/reports/tr38/

## 项目概述

Unihan 数据库是 Unicode 联盟汇集其关于 Unicode 标准所收汉字的知识的仓库。它与西方文字不同——汉字的基本属性是其"义"而非"音"，因此除读音外还须提供结构分析与定义。该文档（UAX #38）即是对这一数据库的指南，描述其组织方式、内容性质及各类属性的状态；它属 Unicode 标准附录，是标准的一部分，可作规范性引用。

当前正式版本为 Unicode 17.0.0（2025 年 9 月 9 日发布），对应 UAX #38 修订版 39（2025-08-21），编辑为 Ken Lunde。Unicode 17.0 共新增 4,803 个字符、总量达 159,801 字符，其中汉字部分新增 CJK 统一表意文字扩展 J 区（U+323B0—U+3347F）。

## 数据内容与属性

数据库由多个字段组成，每个汉字对应若干属性；字段名一律由 ASCII 字母和数字构成、以历史原因统一以小写字母 k 开头（如 kMandarin 普通话读音、kCantonese 粤语读音、kDefinition 英文释义、kRSUnicode 部首笔画、kTotalStrokes 总笔画、kSimplifiedVariant/kTraditionalVariant 简繁变体等）。属性按用途归为若干类别：

- IRG Sources：中/港/日/韩/朝/越等 IRG 成员的官方映射，属数据库中少数规范性、且核验最严格的属性。
- Other Mappings 与 Dictionary Indices：与其它字符集及字典（如康熙字典、汉语大词典等）的索引映射。
- Readings：各语言读音。
- Dictionary-like Data：字典类释义与数据。
- Radical-Stroke Counts：部首笔画计数，支撑部首笔画索引。
- Variants：变体，含简体/繁体变体、语义变体与防伪（spoofing）变体。
- Numeric Values 与 Source References：数值及来源引用。

数据以 UTF-8、Normalization Form C（NFC）存储。Unihan 属性可扩展应用于部分非统一表意文字（如康熙部首字形），通过 UCD 的 Equivalent_Unified_Ideograph 属性关联其等价统一表意文字。

## 获取与使用条件

数据库作为 Unicode 字符数据库（UCD）的一部分，以 `Unihan.zip` 打包发布，内含 8 个文本文件（如 `Unihan_Readings.txt` 等），每条记录为"码点、属性名、属性值"三个制表符分隔字段。用户可从 UCD 发布目录（https://www.unicode.org/Public/17.0.0/ucd/）下载，或通过 Unihan Database Lookup 页面（https://www.unicode.org/charts/unihan.html）按码点或部首笔画在线检索。

数据文件与软件遵循 UNICODE LICENSE V3（Copyright © 1991-2026 Unicode, Inc.），允许免费使用、复制、修改、合并、发布、分发及销售，仅须在副本或关联文档中保留版权与许可声明。

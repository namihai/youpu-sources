---
title: "统一汉字属性数据库"
summary: "该数据库提供 Unicode 汉字属性信息，可用于字符处理和文本标准化。"
canonical_url: "https://www.unicode.org/reports/tr38/"
publisher: "Unicode Consortium"
modality: "text"
access_level: "open"
tags: [汉字, Unicode, 字符属性, 编码, 文字学]
---

## 来源概述

Unihan Database 是 Unicode Consortium 维护的统一汉字属性数据库，配合 Unicode 标准记录中日韩越统一表意文字的编码、读音、字典索引和若干语言属性。它适合用于字符处理、汉字检索和文本标准化。

## 收录内容与边界

该来源收录的是 Unicode 编码体系下的汉字属性数据，并非古籍全文、书法图像或专门的文字释读数据库。属性字段覆盖范围随 Unicode 版本更新而变化，不同字段的可靠性和来源口径也可能不同。

## 获取方式

用户可通过 Unicode 技术报告页面查看字段说明，并通过 Unicode 官方数据文件获取 Unihan 数据。工程使用时应固定 Unicode 版本，避免不同版本造成字段差异。

## 使用与访问限制

该来源公开提供。正式使用前应核验 Unicode 数据文件的许可声明、引用要求和版本信息，尤其是在软件或数据产品中再分发时。

## 质量与风险

Unihan 适合做字符级标准化和属性查询。主要风险在于它面向编码标准服务，部分读音、字典索引或语义字段不适合作为单一语言学结论；复杂文字学研究仍需结合专业字书和文献证据。

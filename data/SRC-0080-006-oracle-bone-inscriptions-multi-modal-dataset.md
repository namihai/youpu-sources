---
title: "甲骨文多模态数据集"
summary: "该数据集汇集甲骨拓片、摹本和字符标注，支持甲骨文识别研究。"
canonical_url: "https://huggingface.co/datasets/KLOBIP/OBIMD"
publisher: "KLOBIP / Key Laboratory of Oracle Bone Inscriptions Information Processing"
modality: "multimodal"
access_level: "open"
tags: [甲骨文, 古文字, 图像标注, 多模态, 商代]
---

## 来源概述

Oracle Bone Inscriptions Multi-modal Dataset 是面向甲骨文识别与释读研究的数据集，由甲骨文信息处理相关团队在 Hugging Face 发布。它把甲骨拓片、摹本、字级标注、句级转写和阅读顺序组织在同一数据来源中，适合用于古文字图像识别和多模态建模。

## 收录内容与边界

公开说明列出 10,077 张甲骨图像、93,652 个已标注字符、21,941 条经过句法校验的句子，以及若干缺损位置和非句子元素。数据面向甲骨文材料，不覆盖其他古文字体系；其中现代字映射和释读信息属于参考性材料，不宜直接等同于最终文字学结论。

## 获取方式

用户可通过 Hugging Face 数据集页面查看文件并下载数据包。页面显示数据集查看器当前受脚本兼容问题影响，批量使用时更适合直接查看 Files and versions 区域或使用 Hugging Face 工具链固定版本获取。

## 使用与访问限制

页面标注许可为 CC BY 4.0，并提供引用信息。开放下载并不等同于无需署名或可任意改写来源说明，正式用于论文、模型训练或再分发时，应保留许可、作者和数据版本信息。

## 质量与风险

该来源提供图像、框选、字符标签和阅读顺序等多层信息，适合构建甲骨文识别基准。主要风险在于古文字释读本身存在不确定性，且平台数据查看器不可用会增加快速预览和字段确认成本；使用前应先完成小样本字段核验。

---
title: "中文古籍光学字符识别评测数据集"
summary: "该来源提供少量古籍图文样本，可用于 OCR 流程测试和评测。"
canonical_url: "https://huggingface.co/datasets/VirtualLUO/Chronicles-OCR"
publisher: "VirtualLUO / Anyang Normal University Key Laboratory / Palace Museum"
modality: "multimodal"
access_level: "open"
tags: [古籍OCR, 中文文献, 图像文本, 评测集, 数字化]
---

## 来源概述

Chronicles-OCR 是发布在 Hugging Face 上的中文古籍 OCR 相关数据来源，页面将其列为图像和文本模态。它主要服务于古籍页面识别、文本转写和模型评测场景，适合用作小规模测试或流程验证材料。

## 收录内容与边界

公开页面显示该数据集当前包含 default 子集和 test 划分，规模为 14 行。由于规模较小，它更适合作为评测样例或演示数据，不宜直接视为覆盖各类古籍版式、字体和印刷质量的完整语料。

## 获取方式

用户可通过 Hugging Face 数据集页在线查看数据表，也可使用平台下载入口或 datasets 库读取。落地使用时应记录数据集版本，并检查图像、文本字段和外部依赖是否完整。

## 使用与访问限制

页面未清晰显示独立许可证字段。该来源可公开访问，但正式用于模型训练、论文发布或二次分发前，应进一步核验仓库文件、论文说明和原始图像版权边界。

## 质量与风险

该来源便于快速验证 OCR 流程，但数据量有限，代表性不足。用于评测时应避免把结果推广到所有中文古籍场景，并应人工复核标注文本、图像来源和评价口径。

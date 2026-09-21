---
title: "岭南建筑图像标注数据集"
summary: "数据对象为岭南地区典型建筑图像。"
canonical_url: "https://huggingface.co/datasets/noncegeek/lingnan-architecture-image-annotation"
publisher: "noncegeek"
modality: "multimodal"
access_level: "open"
tags: [地域文化, 岭南, 岭南建筑, 建筑分类, 建筑外观, 建筑构件, 建筑风格, 文化遗产]
---

# 岭南建筑图像标注数据集
## 亮点
- 数据对象为岭南地区典型建筑图像。
- 建筑类型包括碉楼、骑楼、祠堂等。
- 标注内容包括建筑类型、构件、装饰工艺、材质、颜色等外观特征。
- AI DimSum Lab 页面将该数据归入“文化新闻图片”类别。
- Hugging Face 页面显示该数据集包含 1 个 default 子集和 1 个 train split。
- 当前 Hugging Face Dataset Viewer 无法解析该数据集的 train split。
- 数据大小：AI DimSum Lab 页面显示 5.20GB；Hugging Face 页面显示 Total file size 为 4.11GB。
- URL：https://huggingface.co/datasets/noncegeek/lingnan-architecture-image-annotation

## 数据内容
AI DimSum Lab 页面说明，“岭南建筑图片数据集”汇集展现岭南地区传统文化特色的图像资料，内容涵盖建筑、服饰、民俗、艺术、饮食等多个方面。Hugging Face 页面中的“岭南建筑图像标注数据集”对应其中的建筑图像标注部分。

该数据集对岭南地区典型建筑进行外观特征标注。页面列出的建筑对象包括碉楼、骑楼、祠堂等；标注维度包括建筑类型、构件、装饰工艺、材质和颜色。Hugging Face 数据卡说明中将其描述为面向岭南建筑文化的多模态基础资源。

## 来源页面信息
Hugging Face 页面标注语料来源为 AI DimSum Lab。AI DimSum Lab 语料库页面中可以检索到“岭南建筑图像标注数据集”，页面说明与 Hugging Face 数据卡中的简介基本一致。

两个页面显示的数据大小存在差异：AI DimSum Lab 页面显示大小为 5.20GB；Hugging Face 页面显示 Total file size 为 4.11GB。当前草稿同时保留两个来源的大小信息。

## 数据状态
Hugging Face 页面显示该数据集包含 default 子集，train split 处于可见状态，但 Dataset Viewer 当前无法展示数据内容。页面错误信息显示，平台在解析 train split 时无法提取 features columns，报错包括 JSON parse error、ArrowInvalid 和 UTF-8 解码错误。

错误信息中出现 “UnicodeDecodeError: 'utf-8' codec can't decode byte 0xfe in position 10: invalid start byte”。页面同时显示 YAML Metadata Warning，提示数据集卡片中的 YAML metadata 为空或缺失。

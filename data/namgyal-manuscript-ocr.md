---
title: "Namgyal 藏文写本集合 OCR 数据集（Namgyal Manuscript Collection Datasets）"
summary: "面向藏文写本识别与版面分割的数据集，由维也纳藏文写本项目（Tibetan Manuscript Project Vienna，TMPV）于 2023—2024 年构建。"
canonical_url: "https://zenodo.org/records/14247731"
publisher: "Eric Werner、Markus Viehbeck / TMPV"
modality: "multimodal"
access_level: "open"
---

# Namgyal 藏文写本集合 OCR 数据集（Namgyal Manuscript Collection Datasets）

## 亮点

- 面向藏文写本识别与版面分割的数据集，由维也纳藏文写本项目（Tibetan Manuscript Project Vienna，TMPV）于 2023—2024 年构建。
- 含 OCR 数据集（行图像—行标注对）、Unicode 与 Wylie 转写的 PageXML 标注、版面标注（行、图像、题注、页边）以及 OCR 模型（PyTorch 与 ONNX）。
- 数据大小约 1.3 GB，共 7 个文件。
- 许可协议：CC BY 4.0。
- URL：https://zenodo.org/records/14247731

## 数据内容

Namgyal 写本集合数据集是 Eric Werner、Markus Viehbeck 为维也纳藏文写本项目制作的官方数据集，发布于 2024 年 11 月（DOI 10.5281/zenodo.14247731）。数据围绕古典藏文写本构建，覆盖从版面标注到识别模型的完整流程：其一为从 PageXML 标注生成的 OCR 数据集，以行图像—行标注成对形式组织；其二为 Transkribus 的 PageXML 标注，分别提供 Unicode 与 Wylie 转写两种版本；其三为用于图像分割训练的版面标注（含行、图像、题注、页边）；其四为 OCR 模型，含 PyTorch 检查点与 ONNX 模型文件。

## 获取与许可

数据以 CC BY 4.0 发布，可从 Zenodo 直接下载；配套处理代码见 GitHub 仓库 eric86y/Namgyal-OCR。数据集语言为古典藏文，可用于藏文写本的文字识别、版面分割与相关模型训练。

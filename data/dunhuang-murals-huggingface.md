---
title: "敦煌壁画方位分类图像数据集（murals）"
summary: "数据托管在 Hugging Face，数据集名称为 steven191/murals。"
canonical_url: "https://huggingface.co/datasets/steven191/murals"
publisher: "Hugging Face"
modality: "image"
access_level: "open"
tags: [壁画, 敦煌, 文化遗产]
---

# 敦煌壁画方位分类图像数据集（murals）
## 亮点
- 数据托管在 Hugging Face，数据集名称为 steven191/murals。
- 数据类型为图像数据，格式为 imagefolder。
- 数据包含 1 个 train split，共 263 行。
- 数据字段包括 image 和 label。
- image 字段为敦煌壁画图像。
- label 字段为 8 类 class label，标签内容与壁画所在方位或壁面位置有关。
- 页面可见标签包括东壁、东披、北壁、北披、南壁、南披、西壁（二维部分）、西披。
- Dataset Viewer 显示图片宽度范围约为 270px 到 1.02kpx。
- Hugging Face 页面显示该数据集已自动转换为 Parquet。
- 页面当前显示 No dataset card yet，没有补充性数据卡说明。
- 数据大小：544MB。
- URL：https://huggingface.co/datasets/steven191/murals

## 数据内容
该数据集是一个敦煌壁画图像分类数据集。Hugging Face 页面显示，数据集中共有 263 条样本，每条样本由一张图像和一个标签组成。图像字段名为 image，标签字段名为 label。

label 字段为 class label 类型，共 8 个类别。从 Dataset Viewer 预览可见，类别名称与敦煌壁画图像所在方位或壁面位置相关，包括：
- 0 东壁。
- 1 东披。
- 2 北壁。
- 3 北披。
- 4 南壁。
- 5 南披。
- 6 西壁（二维部分）。
- 7 西披。

页面预览显示，不同类别在列表中按标签编号呈现。部分样本标签为“东壁”“东披”“北壁”“北披”“南壁”“南披”“西壁（二维部分）”“西披”。这些标签反映的是壁画图像在洞窟空间中的位置分类，而不是人物、题材、时代、洞窟编号或损伤类型分类。

## 数据结构
Hugging Face 页面显示该数据集包含一个 split：
- split 名称：train。
- 行数：263。
- 数据字段：image、label。
- 图像格式：imagefolder。
- 标签类型：class label。
- 标签类别数：8。
- 总文件大小：544MB。

Dataset Viewer 中的 image 字段直接展示图像预览。页面还显示 image width 统计范围，图像宽度约从 270px 到 1.02kpx。当前页面未显示统一的图像高度、原始图像来源、洞窟编号、拍摄设备、采集时间或图像分辨率标准。

## 页面状态
Hugging Face 页面显示该数据集已自动转换为 Parquet，并可通过 Dataset Viewer 查看样本。页面同时显示 No dataset card yet，说明数据集作者没有提供更完整的数据说明文档。

页面可见的公开元数据包括：
- Modalities：Image。
- Formats：imagefolder。
- Size：小于 1K。
- Libraries：Datasets。
- Number of rows：263。
- Total file size：544MB。
- Downloads last month：83。

## 信息缺失
当前页面没有提供以下信息：
- 数据来源机构或原始图像出处。
- 图像是否来自公开网页、论文数据、个人整理或其他敦煌壁画数据集。
- 许可协议。
- 采集时间和采集方式。
- 洞窟编号、时代、题材、壁画内容、人物或场景标注。
- train split 之外的验证集或测试集。
- 类别分布统计。
- 标注人员、标注规则和质量检查方式。

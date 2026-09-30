---
title: "陶瓷器型图像数据集（Ceramic Ware Types Dataset）"
summary: "收录 17,265 张陶瓷器型图像，覆盖 19 种器型，包括抱月瓶、转心瓶、荸荠瓶、出戟尊等。"
canonical_url: "https://doi.org/10.57760/sciencedb.j00133.00390"
publisher: "徐星、庄智惶（闽南师范大学）"
modality: "image"
access_level: "request"
---

# 陶瓷器型图像数据集（Ceramic Ware Types Dataset）

## 亮点

- 收录 17,265 张陶瓷器型图像，覆盖 19 种器型，包括抱月瓶、转心瓶、荸荠瓶、出戟尊等。
- 按 3:7 比例划分为训练集与测试集，train、test 目录下按器型类别分子目录组织。
- 图像主压缩包约 430.60 MB，全部 22 个分发文件合计约 439.05 MB；采用 CC0 许可。
- 附带环境及数据说明、运行参数说明及 11 个模型的评测结果等辅助文件。
- URL：https://doi.org/10.57760/sciencedb.j00133.00390

## 项目概述

陶瓷器型图像数据集（Ceramic Ware Types Dataset）是面向陶瓷器型自动分类研究的图像数据集，由闽南师范大学的徐星（XuXing）与庄智惶（Zhuang Zhihuang）整理发布，2024 年 1 月 4 日发布第 1 版。数据来源于百度飞桨（AI Studio）平台上的「陶瓷器型19分类 英文」数据集（https://aistudio.baidu.com/datasetdetail/144248/0，作者川泽，2022 年 5 月发布），经整理后在 ScienceDB 上公开，覆盖 19 种陶瓷器型，用于训练和评估器型分类模型。

## 收录内容与规模

数据集共 17,265 张陶瓷器型图像，覆盖 19 种器型，包括抱月瓶、转心瓶、荸荠瓶、出戟尊等。图像以压缩包形式提供，主文件 ceramics-qixing-3t7v.zip 约 430.60 MB（451,514,676 字节，MD5 05efcf3f8240b368e458c07efffcba65）。除图像外，ScienceDB 页面共列出 22 个分发文件，合计约 439.05 MB（460,382,329 字节），包括环境及数据说明.docx、运行参数说明.docx，以及所提方法与 ResNet50、ResNeSt50、SEResNet50、ViT-B、Conformer、Hornet 等 11 个模型在数据集上的评测结果 JSON 文件、论文图 5–图 9 的 PNG 图像和表 1–表 3 的 XLSX 表格。

## 组织方式与检索

数据按 3:7 比例划分为训练集与测试集，train 目录存放训练数据、test 目录存放测试数据，两个目录下再按器型类别分为子目录，目录名采用类别拼音（如 baoyue_ping、biqi_ping、chuji_zun 等），便于按器型检索并训练分类模型。所附的评测结果 JSON 与图表文件记录了关联论文《基于交叉多尺度深度残差网络的陶瓷器型分类》（Classification of Ceramic Ware Types Based on Cross-Multiscale Deep Residual Networks，数据分析与知识发现，2024 年第 8 卷第 8 期，第 261–270 页）中各模型的分类结果，可用于复现或对照实验。

## 访问与使用条件

数据集在 ScienceDB 上公开，采用 CC0（公有领域）许可，可自由使用、修改与再分发；下载需登录 ScienceDB 后获取文件。关联论文由庄智惶、徐星、夏学文、张应龙、周新宇撰写，报告所提方法的分类准确率为 95.71%，较 ResNet50 基线提升 1.01%。

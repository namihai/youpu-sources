---
title: "DH_Mural 敦煌壁画修复整合图像数据集"
summary: "整合 MuralDH、Dunhuang_Grottoes_Painting、Dunhuang_Faces、DhMurals1714 四个敦煌壁画数据集，服务敦煌壁画修复研究。"
canonical_url: "https://www.kaggle.com/datasets/mrzzzz22/dh-version1"
publisher: "mrzzzz22"
modality: "image"
access_level: "open"
tags: [图像数据, 中文文化, Kaggle, 视觉识别, 数据集]
---

# DH_Mural 敦煌壁画修复整合图像数据集

## 亮点

- 整合 MuralDH、Dunhuang_Grottoes_Painting、Dunhuang_Faces、DhMurals1714 四个敦煌壁画数据集，服务敦煌壁画修复研究。
- 含 images（512×512 缩放/裁剪图块）、lines（XDoG 算子提取的线稿）、masks（损坏区域标记，白色为损坏）三类数据。
- 数据规模约 8.3 GB；作者声明仅供研究用途、禁止商业用途，并须遵守各原始数据集许可。
- URL：https://www.kaggle.com/datasets/mrzzzz22/dh-version1

## 项目概述

DH_Mural（原始清单标题为「DH 第一版图像数据集」，Kaggle 现名 DH_Mural，URL 标识为 dh-version1）是整合了 MuralDH、Dunhuang_Grottoes_Painting、Dunhuang_Faces、DhMurals1714 四个敦煌壁画数据集的图像集合，主要用于敦煌壁画修复的相关研究。作者 Mr_z（mrzzzz22）在说明中注明：如涉及侵权可联系本人将数据集下架，联系方式见其 GitHub 主页（github.com/Mr-Asher-Zheng）。

## 收录内容与规模

数据集总规模约 8.3 GB，含三个目录：images 为对四个原始数据集图片进行 512×512 缩放或裁剪得到的图块；lines 为用 XDoG 算子从 images 提取的线稿图；masks 为损坏区域标记（白色部分表示损坏），由在 MuralDH 的 Mural_seg 子集上微调的 SAM-Adapter 模型生成（测试集 IoU 约 0.3，应用到其他三个数据集时可能存在漏检或错检）。四个原始数据集分别为 MuralDH（GitHub）、Dunhuang_Grottoes_Painting（Kaggle）、Dunhuang_Faces（图像源自数字敦煌项目）、DhMurals1714（GitHub）。

## 组织方式与检索

数据集按 images、lines、masks 三个目录组织，分别存放壁画图块、线稿与损坏区域掩膜，可用于敦煌壁画修复（图像补全）模型的训练与评估；作者欢迎社区对掩膜进行再标注或改进模型，以产出质量更高的版本并分享。

## 访问与使用条件

数据集由 Kaggle 用户 Mr_z（mrzzzz22）发布，Kaggle 许可字段标注为 Unknown（未知）；作者在说明中要求遵守各原始数据集的许可、禁止商业用途、仅限研究用途。数据当前为第 3 版，Kaggle 可用性评分为 0.438，最近更新于 2025 年 12 月。

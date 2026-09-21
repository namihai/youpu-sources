---
title: "中国传统民乐创作音频数据集（Traditional Chinese Folk Music Composition Dataset）"
summary: "收录 2,374 条中国传统民乐样本的结构化记录，附地域、风格、乐器、速度、调式、主题等文化信息标签。"
canonical_url: "https://www.kaggle.com/datasets/ziya07/traditional-chinese-folk-music-composition-dataset"
publisher: "ziya07"
modality: "audio"
access_level: "open"
tags: [民间音乐, 中国传统音乐, 音频, 作曲, Kaggle]
---

# 中国传统民乐创作音频数据集（Traditional Chinese Folk Music Composition Dataset）

## 亮点

- 收录 2,374 条中国传统民乐样本的结构化记录，附地域、风格、乐器、速度、调式、主题等文化信息标签。
- 每条记录含 tempo_bpm、pitch_key 等元数据及 MFCC 等数值型音频衍生特征，可用于民乐风格分类与 AIGC 音乐生成。
- 附 style_label 目标列（如花儿、江南、蒙古等），面向监督学习与生成式建模。
- 单一 CSV 表格（约 1.1 MB），不含原始音频文件；采用 CC0（公有领域）许可，可自由使用。
- URL：https://www.kaggle.com/datasets/ziya07/traditional-chinese-folk-music-composition-dataset

## 项目概述

中国传统民乐创作音频数据集（Kaggle 标识 ziya07/traditional-chinese-folk-music-composition-dataset，现名 Traditional Chinese Folk Music Composition Dataset，副题 Metadata, MFCC Features, and Style Labels for AIGC Music Generation）收录了中国传统民乐样本的详细、富含文化信息的元数据，用于支持基于人工智能的音乐生成、风格分类与文化遗产保护研究。每条记录代表一个独特的民乐样本，以地域、风格、乐器、速度、调式与主题等标签描述，并附统计性的音频特征以刻画其音乐特性，可用于构建学习、分类或生成与中华文化相契合的传统音乐模型，注重保持风格本真性与文化语境。

## 收录内容与规模

数据集共 2,374 行，以单一 CSV 文件（traditional_music_dataset.csv，约 1.1 MB）存储，不含原始音频文件。每条记录含 file_name（样本唯一标识）、region（来源省份或地区，如甘肃、江苏）、style_label（风格标签，目标列，如花儿、江南、蒙古）、instrument（主要乐器，如人声、笛）、tempo_bpm（估算速度，拍/分钟）、pitch_key（调式，如 C、D、E）、theme_label（主题内容，如爱情、民间故事、节庆）、noise_level（模拟田野录音噪声，低/中/高），以及多个描述音色与节奏特性的数值型音频衍生特征列（含 MFCC 特征）。

## 组织方式与检索

数据集为表格化结构，style_label 为目标列，用于监督学习中的地域民乐风格分类；tempo_bpm、pitch_key、instrument 等元数据与 MFCC 等数值特征共同刻画音色与节奏特性，可用于训练具有文化意识的音乐生成模型，或通过数字音乐分析支持文化遗产保护。数据面向民乐风格分类、面向文化的 AIGC 音乐生成、数字音乐分析与传统音乐形式的创造性探索等用途，适合监督式或生成式建模任务。

## 访问与使用条件

数据集由 Kaggle 用户 Ziya（ziya07）发布，采用 CC0（Public Domain，公有领域）许可，可自由使用、修改与再分发。数据当前为第 1 版，Kaggle 可用性评分为 0.823，最近更新于 2025 年 7 月。

---
title: "MOLHW 传统蒙古文在线手写数据集（MOLHW）"
summary: "词级传统蒙古文在线手写数据集，由 200 名书写者经手机 App 触屏书写，耗时约一年采集。"
canonical_url: "https://www.kaggle.com/datasets/fandaoerji/molhw-ooo"
publisher: "fandaoerji"
modality: "text"
access_level: "open"
---

# MOLHW 传统蒙古文在线手写数据集（MOLHW）

## 亮点

- 词级传统蒙古文在线手写数据集，由 200 名书写者经手机 App 触屏书写，耗时约一年采集。
- 词汇量 40,605 词，样本数 164,631 条，平均每词约 4 个样本。
- 许可协议：CC0（Public Domain）。
- 提供原始与预处理两个版本，每条样本含拉丁转写标签、书写者 ID 与书写轨迹坐标。
- URL：https://www.kaggle.com/datasets/fandaoerji/molhw-ooo

## 数据内容

MOLHW 是面向传统蒙古文（区别于西里尔蒙古文）在线手写识别研究的数据集，由 Kaggle 用户 fandaoerji 发布。作者指出此前没有公开的蒙古文在线手写数据集，遂自行构建：由 200 人经手机 App 用手指在触屏上书写，耗时约一年，并经人工严格校验。数据集含 40,605 个词、164,631 条样本，平均每词约 4 个样本、每人约 823 个样本。数据为文本格式，每条样本含拉丁转写标签（大小写敏感，经 ASCII2Unicode.txt 映射到蒙古文 Unicode）、书写者 MD5 加密 ID、屏幕宽高与像素密度、书写轨迹坐标（[-1,-1] 表示抬笔）。数据集同时提供原始版与预处理版（贝塞尔插值、每 5 像素重采样、纵向居中、坐标归一化至 0~1）。

## 获取与许可

数据以 CC0（Public Domain）发布，可从 Kaggle 直接下载，预计年度更新。可用于蒙古文在线手写识别、书写者识别与手写文本生成等研究；构建工作获国家自然科学基金（61763034）资助。

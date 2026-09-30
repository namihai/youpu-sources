---
title: "中药花图像数据集（Chinese medicinal blossom-dataset）"
summary: "传统中药植物花朵图像集，分 12 类，原始图像 1,716 张，经数据增强后共 12,538 张。"
canonical_url: "https://data.mendeley.com/datasets/r3z6vp396m"
publisher: "Mei-Ling Huang、Yi-Xuan Xu"
modality: "image"
access_level: "open"
---

# 中药花图像数据集（Chinese medicinal blossom-dataset）

## 亮点

- 传统中药植物花朵图像集，分 12 类，原始图像 1,716 张，经数据增强后共 12,538 张。
- 覆盖丁香、木棉、白兰、梅、合欢、马尾松、枇杷、槐、桃、梧桐、菩提树、槟榔等药用植物的花朵图像。
- 许可协议：CC BY 4.0。
- 附数据集划分（训练/验证/测试 80:10:10）与增强流程说明，可用于图像分类与分割实验。
- URL：https://data.mendeley.com/datasets/r3z6vp396m

## 数据内容

Chinese medicinal blossom-dataset 由 Mei-Ling Huang 与 Yi-Xuan Xu 于 2021 年发布，当前为第 2 版（DOI 10.17632/r3z6vp396m.2）。数据集为传统中药植物的花朵图像，图像通过 Google 搜索采集，经裁剪去除文字与边框、删除手写与模糊图、居中并调整长宽等预处理后，按类别分文件夹组织，格式为 JPG，各图像尺寸不一。

数据分 12 类：丁香（Syringa）、木棉（Bombax malabarica）、白兰（Michelia alba）、梅（Armeniaca mume）、合欢（Albizia julibrissin）、马尾松（Pinus massoniana）、枇杷（Eriobotrya japonica）、槐（Styphnolobium japonicum）、桃（Prunus persica）、梧桐（Firmiana simplex）、菩提树（Ficus religiosa）、槟榔（Areca catechu）。原始图像共 1,716 张，按 80:10:10 的比例划分为训练、验证与测试子集，再经高斯滤波、图像亮度增减、镜像旋转、噪声增加、90° 与 180° 旋转等增强后，共 12,538 张。

## 获取与许可

数据从 Mendeley Data 直接下载，以 CC BY 4.0 发布。发布方说明，该数据集可帮助中药师对中草药进行分类，也可作为机器学习或深度学习图像分割与图像分类算法的实验资源。

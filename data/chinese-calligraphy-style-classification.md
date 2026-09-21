---
title: "中国书法风格分类图像数据集（Chinese Calligraphy Styles）"
summary: "由 Richard Cornelius Suwandi（Kaggle 用户名 richardcsuwandi）发布，包含 2,000 张中国书法图像，覆盖篆书、草书、隶书、楷书四种书体，每种 500 张。"
canonical_url: "https://www.kaggle.com/datasets/richardcsuwandi/chinese-calligraphy-styles"
publisher: "Kaggle"
modality: "image"
access_level: "open"
tags: [书法, 书体, 风格分类, 图像分类]
---

# 中国书法风格分类图像数据集（Chinese Calligraphy Styles）

## 亮点

- 由 Richard Cornelius Suwandi（Kaggle 用户名 richardcsuwandi）发布，包含 2,000 张中国书法图像，覆盖篆书、草书、隶书、楷书四种书体，每种 500 张。
- 图像从 Google 图片搜索抓取，按书体分目录存放，均为 JPG 格式。
- 数据大小：约 386 MB（386,431,104 字节）。
- 许可协议：CC0: Public Domain（公有领域）。
- URL：https://www.kaggle.com/datasets/richardcsuwandi/chinese-calligraphy-styles

## 数据内容与来源

该数据集由作者为构建中国书法风格分类器而自行整理。作者是在中国学习的留学生，因检索不到现成的多书体书法图像数据集，改用 Google 图片搜索自行抓取：以“书体名称 + 字帖網格”为关键词组合搜索，用 JavaScript 脚本获取搜索结果中的图片 URL，再通过 fast.ai 的 download_images 函数批量下载；作者也曾尝试用类似脚本从百度图片下载。

数据集覆盖四种书体：篆书（zhuanshu）、草书（caoshu）、隶书（lishu）、楷书（kaishu）。这四种书体分属不同历史时期，各有独特的字形结构与笔画排布。图片统一为 JPG 格式，书体类别通过所在目录体现，未附带其他标注文件。

## 文件组织与规模

数据共 2,000 张图像，统一存放在 train 目录下，按书体分为四个子目录，每个子目录含 500 张图像：train/caoshu（草书）、train/kaishu（楷书）、train/lishu（隶书）、train/zhuanshu（篆书）。文件名采用编号形式，如 train/caoshu/0.jpg。

数据总大小约 386 MB（386,431,104 字节）。数据集为 Version 1（初始版本），发布于 2020 年 7 月 31 日。

## 访问与授权

数据集在 Kaggle 上公开，下载入口位于来源页面。许可协议为 CC0: Public Domain，作者将作品置于公有领域。作者另维护配套的 chinese-calligraphy-classifier 项目（GitHub 仓库及一篇 Medium 文章），介绍用 fast.ai 和 ResNet-50 在该数据上训练分类器；其中训练集与验证集的 80:20 划分、224 像素缩放及数据清理均在配套代码中完成，不属于本数据集发布包的内容。

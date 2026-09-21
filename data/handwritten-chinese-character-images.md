---
title: "手写汉字图像数据集（Handwritten Chinese Character (Hanzi) Datasets）"
summary: "由 Pascal Bliem 通过 Kaggle 发布，数据源自中国科学院自动化研究所模式识别国家重点实验室建立的中文离线手写数据库 CASIA-HWDB。"
canonical_url: "https://www.kaggle.com/datasets/pascalbliem/handwritten-chinese-character-hanzi-datasets"
publisher: "Kaggle"
modality: "image"
access_level: "open"
tags: [OCR, 字符识别, 版权合规]
---

# 手写汉字图像数据集（Handwritten Chinese Character (Hanzi) Datasets）

## 亮点

- 由 Pascal Bliem 通过 Kaggle 发布，数据源自中国科学院自动化研究所模式识别国家重点实验室建立的中文离线手写数据库 CASIA-HWDB。
- 包含 7,330 个字符类别，覆盖 GB2312 编码中的全部 6,763 个汉字，以及 171 个字母、数字和符号。
- 手写样本由 1,020 位书写者在 2007 至 2010 年间完成，原始二进制文件已转换为 PNG 图像。
- 数据划分为 CASIA-HWDB_Train 和 CASIA-HWDB_Test 两个目录，当前版本为 Version 3。
- 数据大小：约 13.77 GB（13,769,843,863 字节，按十进制换算）。
- 许可协议：页面标注为 Other（specified in description），说明数据一般可免费用于非商业用途。
- URL：https://www.kaggle.com/datasets/pascalbliem/handwritten-chinese-character-hanzi-datasets

## 数据内容与来源

该数据集是 CASIA-HWDB 离线手写汉字数据库的 PNG 图像版本。原始数据库由中国科学院自动化研究所模式识别国家重点实验室建立，手写样本由 1,020 位书写者在 2007 至 2010 年间产生。原始资料以自定义编码的二进制文件公开，本数据集由 Pascal Bliem 将书写样本转换为带标签的 PNG 图像，并在 Kaggle 上重新发布。

数据集覆盖 7,330 个字符类别，包括 GB2312 编码中的全部 6,763 个汉字，以及 171 个字母、数字和符号。这里的 7,330 是字符类别数量，不是图像总数；每张图像对应一个手写单字样本。发布说明同时指向原始数据库的下载页和二进制编码说明，便于核对本数据集与原始文件的关系。

## 数据划分与文件结构

图像按字符标签分组，每个标签对应一个文件夹，文件夹内的文件为 PNG 图像。数据集分为 CASIA-HWDB_Train 和 CASIA-HWDB_Test 两个顶层目录，分别存放训练和测试数据。当前 Version 3 的版本说明为 added training data，即该版本补充了训练数据。

Kaggle 数据浏览器显示，数据包约 13.77 GB，文件总数约 400 万。这一数量代表数据包中的文件规模，主要对应手写单字 PNG 图像；字符类别数量仍以 7,330 类为准。

## 访问与授权

数据通过 Kaggle 数据集页面公开发布，下载入口位于来源页面。原始 CASIA-HWDB 数据库的二进制文件可由中国科学院自动化研究所的下载页面获取，二进制编码说明记录在离线数据库页面。

来源页面将许可协议标注为 Other（specified in description），并在说明中指出数据一般可免费用于非商业用途，具体条件见 CASIA 手写数据库申请表格页面。原始数据由 NLPR、中国科学院自动化研究所及参与书写样本的志愿者提供。

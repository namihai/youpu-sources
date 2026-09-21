---
title: "中国古代手写字符数据库（CASIA-AHCDB）"
summary: "数据库英文名为 Chinese Ancient Handwritten Characters Database，缩写为 CASIA-AHCDB。"
canonical_url: "https://nlpr.ia.ac.cn/pal/CASIA-AHCDB.html"
publisher: "中国科学院自动化研究所（CASIA）"
modality: "image"
access_level: "request"
tags: [机器学习, 计算机视觉]
---

# 中国古代手写字符数据库（CASIA-AHCDB）
## 亮点
- 数据库英文名为 Chinese Ancient Handwritten Characters Database，缩写为 CASIA-AHCDB。
- 数据面向古代手写汉字字符识别研究。
- 数据包含超过 220 万个已标注字符样本。
- 字符类别数为 10,658 类。
- 字符样本来自 12,000 余页已标注中国古代手写文献。
- 数据按文献来源分为两个主要子库：style1 和 style2。
- style1 来源为《四库全书》类文献，style2 来源为古代佛经文献。
- 每个子库按应用划分为 basic category set、enhanced category set 和 reserved category set。
- style1 和 style2 的 basic category set 具有相同的 2,365 个类别。
- 数据大小：官方提供 6 个 ZIP 文件，合计 4,428,160,688 bytes，约 4.43GB。
- URL：https://nlpr.ia.ac.cn/pal/CASIA-AHCDB.html

## 数据内容
CASIA-AHCDB 是中国古代手写字符数据库。官方页面说明，该数据库用于字符识别研究，包含超过 220 万个标注字符样本，覆盖 10,658 个字符类别。字符样本来自 12,000 余页已标注中国古代手写文献。

数据库按照文献来源分为两个主要子库：
- style1：Complete Library in Four Sections，对应《四库全书》类文献。
- style2：Ancient Buddhist Scriptures，对应古代佛经文献。

每个子库根据应用划分为三部分：
- basic category set。
- enhanced category set。
- reserved category set。

官方说明中写明，style1 和 style2 的 basic category set 具有相同的 2,365 个类别；style1 和 style2 的 enhanced category set 没有相交类别；reserved category set 由于样本较少，没有划分训练集和测试集。

## 数据划分
style2 的文献按 period 和 volume 编号。页面示例说明，01 period 中第 001 卷佛经编号为 `period_01/volume_001`。

style2 的训练和测试划分方式为：
- period 09-10 的佛经作为训练集。
- period 01-08 的佛经作为测试集。

## 数据格式
官方页面给出了单个样本的数据记录结构：
- Sample size：4 bytes，用于记录一个样本的字节数。
- Unicode：4 bytes，用于记录字符 Unicode。
- Width：2 bytes，用于记录图像宽度像素数。
- Height：2 bytes，用于记录图像高度像素数。
- Bitmap：`width * height` bytes，按行存储位图数据。

## 下载文件
官方页面提供 6 个 ZIP 下载文件：
- `style1_basic_test.zip`：738,929,262 bytes，约 704.70MiB。
- `style1_basic_train_part1.zip`：910,549,170 bytes，约 868.37MiB。
- `style1_basic_train_part2.zip`：764,077,504 bytes，约 728.68MiB。
- `style1_basic_train_part3.zip`：830,371,907 bytes，约 791.90MiB。
- `style1_enhanced.zip`：471,663,188 bytes，约 449.81MiB。
- `style2.zip`：712,569,657 bytes，约 679.56MiB。

上述文件大小来自官方下载链接返回的 Content-Length 响应头。6 个文件合计 4,428,160,688 bytes，约 4.43GB。

## 引用信息
官方页面列出的参考文献为：

Yue Wu, Fei Yin, Xu-Yao Zhang, Cheng-Lin Liu, “CASIA-AHCDB: A large-scale Chinese ancient handwritten characters database”, Proc. 15th ICDAR, Sydney, Australia, 2019.

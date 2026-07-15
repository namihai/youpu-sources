---
title: "中国传统纹样层次化标注数据集"
summary: "包含高分辨率中国传统纹样文物图像及层次化边界框标注，支持目标检测和纹样识别。"
canonical_url: "https://doi.org/10.57760/sciencedb.34731"
publisher: "ScienceDB"
modality: "image"
access_level: "open"
tags: ["中国传统纹样", "文物图像", "目标检测", "层次化标注", "YOLO", "JSON", "文化遗产", "图像数据集"]
---

# 中国传统纹样层次化标注数据集
## 要点
- 包含5700张高分辨率中国传统纹样文物图像。
- 包含13841个具有层次化语义关系的边界框标注。
- 覆盖宝相花纹、八吉祥纹、福字纹、工字纹等17类核心纹样。
- 遵循《T/CPRA 200.2-2024》
- 格式兼容YOLO、JSON。
- 数据大小：1.82GB。
- 数据已被收录于国家自然科学基金。
- URL：https://doi.org/10.57760/sciencedb.34731。
## 数据内容
本数据集实际由三部分组成：
1. 完整目录版本数据集——TCM Pattern Dataset
2. 标准划分发布版本数据集——Chinese_Traditional_Pattern_Dataset
3. 预览图副本——TCM Pattern Dataset/previews

具体内容如下：
| 类别目录 | 中文含义 | 图像数 | 原始标注行数 |
|---|---:|---:|---:|
| `hewen` | 鹤纹 | 1174 | 2589 |
| `yuwen` | 鱼纹 | 895 | 1716 |
| `baoxianghuawen` | 宝相花纹 | 821 | 3025 |
| `shouziwen` | 寿字纹 | 787 | 1743 |
| `huwen` | 虎纹 | 498 | 661 |
| `lianhuawen` | 莲花纹 | 290 | 625 |
| `guwen` | 谷纹 | 243 | 380 |
| `jiaoyewen` | 蕉叶纹 | 192 | 382 |
| `bajixiangwen` | 八吉祥纹 | 164 | 1054 |
| `yuanyangwen` | 鸳鸯纹 | 146 | 347 |
| `xiziwen` | 喜字纹 | 137 | 301 |
| `wanziwen` | 万字纹 | 129 | 620 |
| `fuziwen` | 福字纹 | 109 | 141 |
| `guibeiwen` | 龟背纹 | 52 | 108 |
| `panchangwen` | 盘长纹 | 39 | 84 |
| `taiyangwen` | 太阳纹 | 23 | 61 |
| `gongziwen` | 弓字纹 | 1 | 4 |
## 标准发布板结构
```Chinese_Traditional_Pattern_Dataset/
  README.md
  LICENSE.txt
  images/
    train/ 3946
    val/   840
    test/  862
  annotations/
    train/ 3946
    val/   840
    test/  862
  dataset_statistics/
    category_distribution.csv
    summary_report.txt
  metadata/
    category_mapping.json
```
## 图像属性
标准版 5648 张图全部是 JPEG。图像尺寸差异很大，共有 2293 种尺寸组合：
常见尺寸：1350x1800、640x480、480x640、1080x1440、640x426
最小像素面积：27300
中位像素面积：约 676220
平均像素面积：约 1266507
最大像素面积：50320896

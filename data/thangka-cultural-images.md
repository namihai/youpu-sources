---
title: "唐卡文化图像数据集"
summary: "包含唐卡图像及佛像、菩萨、法器等37类目标标注的文化图像数据集。"
canonical_url: "https://doi.org/10.57760/sciencedb.14085"
publisher: "ScienceDB"
modality: "image"
access_level: "open"
tags: ["唐卡", "文化图像", "目标检测", "佛教艺术", "LabelMe", "Pascal VOC", "YOLO", "ScienceDB", "CC BY 4.0"]
---

# 唐卡文化图像数据集
## 要点
- 包含6200张唐卡图像。
- 数据大小：3.91GB。
- 文件量：112。
- 采用X-anylabeling标注软件，使用矩形工具对图像中的元素进行精细标注。共计37个类别，接近16000个标签。
- 标签数据提供两种格式，VOC和WOLO。
- 图像尺寸差异很大，发现2711种不同尺寸。常见尺寸包括800x800、1080x1440、500x500等。宽度范围为180-17626，高度范围为240-13960。
- 使用协议：CC BY 4.0
- URL：https://doi.org/10.57760/sciencedb.14085
## 数据内容
主体内容是唐卡、佛像、菩萨、法器、坐骑等视觉对象。数据规模中等，标注体系清晰，提供了 LabelMe JSON、Pascal VOC XML、YOLO TXT 三套格式；三套格式的类别计数完全一致，整体转换可靠。但训练前建议清洗空标注、异常框和重复图像。
## 数据结构
| 路径 | 内容 | 数量 |
|---|---:|---:|
| [image](/Users/yuzheng/Downloads/TKdataset/image) | 图像 + LabelMe JSON | 6139 张图像，6128 个 JSON |
| [voc](/Users/yuzheng/Downloads/TKdataset/voc) | Pascal VOC XML | 6128 个 XML |
| [yolo](/Users/yuzheng/Downloads/TKdataset/yolo) | YOLO TXT | 6139 个 TXT |
| [shunxu.txt](/Users/yuzheng/Downloads/TKdataset/shunxu.txt) | 类别索引表 | 37 类 |
## 标注格式
`image/*.json` 是 LabelMe 风格，所有标注都是 `rectangle`。
`voc/*.xml` 是 Pascal VOC 格式，包含 `filename / size / object / bndbox`。
`yolo/*.txt` 是 YOLO 格式：`class_id x_center y_center width height`，坐标已归一化。
[shunxu.txt](/Users/yuzheng/Downloads/TKdataset/shunxu.txt) 是 YOLO 类别 id 到中文标签的映射。
## 内容主题
数据集覆盖 37 个类别，核心是宗教人物、法器、坐具和坐骑。高频类别包括：
| 类别 | 数量 |
|---|---:|
| 发冠 | 1989 |
| 释迦牟尼 | 1580 |
| 莲花座 | 1490 |
| 文殊菩萨 | 1034 |
| 马头金刚 | 1007 |
| 发髻 | 738 |
| 四臂观音 | 684 |
| 智慧宝剑 | 591 |
| 僧帽 | 589 |
| 绿度母 | 583 |

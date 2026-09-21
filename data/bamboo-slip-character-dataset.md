---
title: "简牍文字检测与识别数据集（DeepJiandu）"
summary: "数据集英文名为 “DeepJiandu dataset for character detection and recognition on Jiandu manuscript”。"
canonical_url: "https://www.scidb.cn/en/detail?dataSetId=7f627b99d06e4430a5e5d21b20614b46"
publisher: "科学数据银行"
modality: "multimodal"
access_level: "open"
tags: [OCR, 古文字, 古文档, 古籍数字化, 图像标注, 字符检测, 字符识别, 数据集评测]
---

# 简牍文字检测与识别数据集（DeepJiandu）
## 亮点
- 数据集英文名为 “DeepJiandu dataset for character detection and recognition on Jiandu manuscript”。
- DOI：10.57760/sciencedb.08560。
- ScienceDB 页面标注版本为 V2，结构化元数据版本号为 2.0.0。
- ScienceDB 页面元数据发布时间为 2024 年 5 月 15 日；页面引用格式中标注年份为 2025 年 2 月。
- 数据集访问状态为 PUBLIC。
- 数据大小为 3,002,834,502 bytes，约 3.00 GB。
- 许可协议：CC BY 4.0。
- 数据集包含 7,416 张简牍图像、99,888 个字符标注、2,272 个类别。
- 关键词包括 Bamboo and wooden slips、Jiandu、Character detection、Character recognition、Ancient characters。
- URL：https://www.scidb.cn/en/detail?dataSetId=7f627b99d06e4430a5e5d21b20614b46

## 数据内容
DeepJiandu 是面向简牍文字检测与识别的数据集。ScienceDB 页面说明，简牍是中国古代纸张普及前记录历史信息的重要载体，该数据集针对简牍图像中的字符定位和字符类别识别进行整理。

数据集包含 7,416 张图像，并标注 99,888 个字符，覆盖 2,272 个字符类别。页面描述中提到，数据集中存在字符残损、版式差异、字形变化等情况。关联论文说明，数据图像选用红外图像；红外成像用于呈现竹木载体和墨迹中的字符细节。论文还说明图像经过专家验证，字符位置和字符类别由标注流程记录。

## 文件组成与格式
ScienceDB 文件列表包括：

1. `DeepJiandu.zip`：主图像压缩包，格式为 ZIP，大小 2,980,406,175 bytes，MD5 为 `aebe02ea893ad7c08d62b00c0b66e584`。
2. `DeepJiandu_labels.zip`：标注压缩包，格式为 ZIP，大小 5,087,163 bytes，MD5 为 `8dfa971543fda8b1e8092a3dfc1dafce`。
3. `Character Statistics.xlsx`：字符统计表，格式为 XLSX，大小 141,080 bytes，MD5 为 `92d476500d830600b585b4d767667df4`。
4. `simsunb.ttf`：字体文件，格式为 TTF，大小 17,200,084 bytes，MD5 为 `42b78d510b142e4cd9c3b0a0f8003d87`。

标注包 `DeepJiandu_labels.zip` 中包含 `train`、`val`、`test` 三个目录。实际文件清单显示 XML 标注文件共 7,416 个，其中训练集 5,922 个、验证集 751 个、测试集 743 个。XML 标注文件采用 VOC 风格结构，包含 `filename`、`size`、`object`、`name`、`bndbox`、`xmin`、`ymin`、`xmax`、`ymax` 等节点。

## 统计字段与样例
`Character Statistics.xlsx` 的字段包括：

1. `id`
2. `cls_names`
3. `images`
4. `objects`
5. `min_h_bbox`
6. `max_h_bbox`
7. `min_w_bbox`
8. `max_w_bbox`
9. `min_area_bbox`
10. `max_area_bbox`

统计表前几类包括 `□`、`月`、`十`、`三`、`二`、`一`、`長` 等字符类别，并记录每个类别涉及的图像数量、目标数量以及边界框高度、宽度、面积的最小值和最大值。

## 关联论文与标注说明
该数据集关联论文为 *DeepJiandu Dataset for Character Detection and Recognition on Jiandu Manuscript*，发表于 Scientific Data，2025 年 3 月 7 日，论文 DOI 为 10.1038/s41597-025-04716-3。

论文说明，标注过程使用 LabelImg 工具，对简牍图像中的字符位置和类别进行标注；字符标注经过简牍专家指导和复核。论文中报告的数据规模为 7,416 张图像、99,852 个字符标注、2,242 个类别，与 ScienceDB 当前 V2 页面元数据中的 99,888 个字符标注、2,272 个类别存在版本差异。当前卡片以 ScienceDB V2 页面元数据为主，并记录论文中的规模差异。

## 作者与发布平台
ScienceDB 页面列出的作者包括 Liu Yiran、Zhang Qiang、Qi Ying、Wan Teng、Zhang Defang、Li Yutong、Zhang Xin、Ma Longbin、Ruan Qiuyue、Guo Huanting、Li Yingchun、Miao Xinyue、Xiao Wenjun、Li Yongbo、Chen Shanxiong 等。作者机构包括 Northwest Normal University 和 Southwest University。

数据发布平台为 Science Data Bank。页面提供 BibTeX 引用格式，出版方为 Science Data Bank，版本标注为 V2。

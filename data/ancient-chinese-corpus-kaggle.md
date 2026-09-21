---
title: "古汉语古籍文本语料集（ancient-Chinese）"
summary: "由 Jack Hu（Kaggle 用户名 `hushiyang`）发布，改编自 NiuTrans/Classical-Modern 古文—现代文语料项目。"
canonical_url: "https://www.kaggle.com/datasets/hushiyang/ancient-chinese"
publisher: "Kaggle"
modality: "text"
access_level: "open"
tags: [语料库, 语言资源]
---

# 古汉语古籍文本语料集（ancient-Chinese）

## 亮点

- 由 Jack Hu（Kaggle 用户名 `hushiyang`）发布，改编自 NiuTrans/Classical-Modern 古文—现代文语料项目。
- 以单个 `ancient_Chinese.jsonl` 文件提供数据，已核验记录将书名、篇章信息与正文存放在 `text` 字段中。
- 文本涉及《山海经》《尚书》《淮南子》《水浒传》《史记》等古籍，涵盖多种体裁与知识领域。
- Version 1 发布于 2025 年 1 月 12 日。
- 数据文件大小：约 260.39 MB（260,391,733 字节，按十进制换算）。
- URL：https://www.kaggle.com/datasets/hushiyang/ancient-chinese

## 数据内容与来源

该数据集将古籍文本整理为 JSONL 文件，发布说明明确将 [NiuTrans/Classical-Modern](https://github.com/NiuTrans/Classical-Modern) 列为改编来源。上游项目同时整理古文原文和古文—现代文平行数据，Kaggle 版本则以一个独立文件发布。

已核验的文件片段包含《东游记》《山海经》《尚书》《淮南子》《水浒传》《传习录》《乐府诗集》《医学源流论》《齐民要术》《战国策》《史记》等书目。文本内容涉及小说、经史、诸子、诗歌、医学及农学等领域。

上游项目的原文按书籍及篇章、章节组织；平行数据另按句子划分，并提供原文、译文和双语文件。Kaggle 文件已核验的记录以古籍正文为主要内容，书名和篇章路径直接嵌入文本，不宜将上游平行语料的句对数量或目录结构直接套用于这一版本。

## 文件结构与文本形态

数据包包含一个 `ancient_Chinese.jsonl` 文件。JSONL 按行存放 JSON 对象；已完整读取的前 2,146 条记录均只有一个 `text` 字段，字段值为字符串。该数量仅对应已核验的文件片段，不代表数据集总规模。

记录中的文本可采用“《书名/篇章》：正文”的组织方式。例如，文件开头包含《东游记》第三十一回、第四十四回和第五十四回的记录，篇章信息与正文保存在同一字段中，未拆分为独立的书名、章节或正文列。

部分记录保留 `<strong>`、`<br/>` 等 HTML 标签，分别出现在篇章标题、诗句换行或其他排版位置。因此，文本字段除古籍内容外，还包含部分来源文本的格式标记。已核验记录未设置独立的现代文译文字段，也未以 `source`、`target` 等字段显式组织古今文配对。

## 上游语料整理方式

NiuTrans/Classical-Modern 的原始材料来自互联网。对于平行语料，上游项目将篇章级对齐的古今文经过分句与对齐处理，形成句子级对应数据；对齐方法结合归一化编辑距离与长度比指标。原文库与平行语料库分开保存，后者仅收录具有双语句对的数据。

上游项目在各书目下通过 `数据来源.txt` 记录出处，并提供处理过程和相关脚本。上述信息说明了改编来源的整理方式，不代表 Kaggle 文件保留了上游全部书目、出处文件或处理脚本。

## 发布与获取

数据由 Jack Hu 通过 Kaggle 公开发布，当前版本为 Version 1，初始发布日期及最近更新时间均为 2025 年 1 月 12 日。数据文件可通过 Kaggle 的数据集下载入口获取。

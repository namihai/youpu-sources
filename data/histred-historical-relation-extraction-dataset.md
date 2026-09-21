---
title: "历史文档级关系抽取数据集（HistRED）"
summary: "首个面向历史领域的文档级关系抽取（RE）数据集，从《燕行录》39 部典籍构建，对应 ACL 2023 长文（arXiv:2307.04285）。"
canonical_url: "https://huggingface.co/datasets/Soyoung/HistRED"
publisher: "Soyoung / HistRED authors"
modality: "text"
access_level: "open"
tags: [历史文档, 关系抽取, 信息抽取, 中文NLP, 标注语料]
---

# 历史文档级关系抽取数据集（HistRED）

## 亮点

- 首个面向历史领域的文档级关系抽取（RE）数据集，从《燕行录》39 部典籍构建，对应 ACL 2023 长文（arXiv:2307.04285）。
- 韩文—汉文（Hanja）双语平行标注：实体在韩文与汉文文本中同时标注，关系标注于韩文，并附证据句索引。
- 面向朝鲜王朝史料语境新定义 10 类命名实体、20 类关系类型，如 per:position_held、nearby、alternate_name。
- 以序列级别（SL）控制子文本长度，覆盖从句子级到文档级的多种上下文，供评估模型在不同长度下的鲁棒性。
- 许可证 CC BY-NC-ND 4.0；仓库发布 900 个 JSON 文档，覆盖 SL_0 / SL_1 / SL_2 三个层级，各 100/100/100 划分。
- URL：https://huggingface.co/datasets/Soyoung/HistRED

## 数据内容与来源

HistRED 由韩国科学技术院（KAIST AI）的 Soyoung Yang、Minseok Choi、Youngwoo Cho、Jaegul Choo 构建，发表于 ACL 2023 长文（第 3207—3224 页），代码托管于 github.com/dudrrm/HistRED。

语料取自《燕行录》（Yeonhaengnok），即朝鲜王朝（1392—1897 年）使臣出使清朝（Chung／Qing）沿途所记的旅行日记汇编。这些文献原以汉文（Hanja，即古典中文书写）写成，后译为韩文；作者从韩国古典翻译院（ITKC）开源数据库（db.itkc.or.kr）中选取信息丰富的 39 部典籍，组成 2,019 篇完整文献（每篇对应一天行程，成文于 16—19 世纪），数据使用经 ITKC 授权。

标注由 15 名具备至少 4 年汉文语言学／文学训练的标注者完成，采用「初标 + 交叉复核」两阶段，逐篇标注四类信息：实体、关系类型、指代（coreference）与证据句。实体在韩文与汉文文本中同时标注，关系仅在韩文文本中标注以减轻标注负担；证据句用于标识支撑某条关系的上下文句子。随后剔除引用他书与诗歌的片段、过滤无关系信息的文本，并按序列级别切分为自包含子文本——论文报告切分后得到 5,816 篇文档（SL=2）至 5,852 个实例（SL=0）。

论文统计显示：平均每篇约 11 个实体（中位数 10），10 类实体中 Location 占 35.91%、Person 占 34.55%、Number 占 13.61%、Datetime 占 4.82%、Product 占 4.40%；20 类关系中 per:position_held 占 32.05%、nearby 占 27.28%、alternate_name 占 7.59%、per:country_of_citizenship 占 5.35%、product:provided_by 占 3.82%。

## 数据字段

每个 JSON 文档对应一个自包含子文本，字段如下：

- text：{ han, kor }，该子文本的汉文与韩文正文。
- entity：实体列表，每项含 han 与 kor，分别为实体在汉文、韩文中的提及。
- relation：关系列表，每项含 han、kor（两实体在对应语言中的提及）与 label（关系类型）。
- meta：元数据，含 book_title（书名）、book_volume（卷名）、copyright（版权信息，如「ⓒ 한국고전번역원 | 译者 | 年份」）与 new_snt_idx（切分后的新句子索引）。
- sentence_start_end：{ han: [起,止], kor: [起,止] }，标记该子文本在原文档中的句子边界。

关系类型由 label_map.json 定义，共 21 个键——含 None（无关系，索引 0）及 20 类实际关系；实体类型由 ner_map.json 定义，共 10 类：Person、Organization、Location、Datetime、Number、Book、Food、Clothes、Product、Other。README 另以概念化字段描述关系信息（主宾语实体 sbj_kor／sbj_han／obj_kor／obj_han 及证据句索引 evidence_kor／evidence_han），实际 JSON 以「entity 列表 + relation 列表」结构承载这些信息。

## 文件组织

仓库无 Parquet 分片或列式切分，属纯文件托管，以 JSON 文件按三个序列级别目录组织：SL_0、SL_1、SL_2，每级目录下再分 train / valid / test，各含 100 个文档，即每层级 300 篇、三个层级共 900 个 JSON 文件。仓库另附 dataset.py（提供 KoreanDataset、HanjaDataset、JointDataset 三种加载方式）、label_map.json、ner_map.json 与 example.png；仓库总占用约 3.8 MB（3,996,658 字节），创建于 2023-05-18，最近更新于 2023-08-01。

论文报告完整数据集为 5,816 篇文档（SL=2）至 5,852 个实例（SL=0），并含 SL_0／1／2／4／8 五个层级；HF 仓库发布的 900 个文件（每层级 300 篇、仅 SL_0／1／2 三个层级）为其中用于评测的子集，README 将其定位为「Testbed」。

## 获取与授权

数据集在 Hugging Face 公开托管、非门控，许可证 CC BY-NC-ND 4.0，任务标注为 token-classification、语言标注为韩文（ko），可经 datasets 库以 load_dataset("Soyoung/HistRED") 加载（由 dataset.py 处理为可输入通用 NLP 模型的数据），或用 hf download Soyoung/HistRED --repo-type dataset 下载；除数据集外的代码见 github.com/dudrrm/HistRED。

原始文献来自 ITKC 开源数据库，作者已获 ITKC 授权利用这些材料；数据集本身按 CC BY-NC-ND 4.0 开放（禁止商业使用与演绎分发）。关联论文为 arXiv:2307.04285（ACL 2023），作者提出利用韩文与汉文双语语境的 RE 模型，其在 HistRED 上优于单语基线。

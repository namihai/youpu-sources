---
title: "语保工程方言点元数据（YuBao Sites）"
summary: "收录中国语言资源保护工程（语保工程）汉语方言调查点的元数据，共约 1,250 条记录。"
canonical_url: "https://huggingface.co/datasets/kalbin/yubao_sites"
publisher: "kalbin / Centre for the Protection of Language Resources of China"
modality: "text"
access_level: "open"
tags: [汉语方言, 语言资源, 调查点, 元数据, 语保工程]
---

# 语保工程方言点元数据（YuBao Sites）

## 亮点

- 收录中国语言资源保护工程（语保工程）汉语方言调查点的元数据，共约 1,250 条记录。
- 每条记录含调查点编号、地理位置、方言系属说明及关联句子编号，以 Parquet 格式托管。
- 覆盖官话、粤、闽、客家、湘、吴、赣等汉语主要方言大类的众多调查点。
- 与视频元数据 kalbin/yubao_videos 共同构成汉语方言语音基准 YuBao，对应论文 arXiv:2601.07274。
- URL：https://huggingface.co/datasets/kalbin/yubao_sites

## 数据内容与来源

语保工程指中国语言资源保护工程及其采录展示平台（zhongguoyuyan.cn）。平台面向中国境内汉语方言调查点，采录方言语音、方言转写、国际音标（IPA）标注与普通话翻译，覆盖 1,000 个汉字、1,200 个词语和 50 个句子的平行语料，涉及 1,300 余个调查点；音频与视频版权归负责该工程的机构（Centre for the Protection of Language Resources of China）。

本数据集 kalbin/yubao_sites 是上述平台方言调查点的元数据集合，共约 1,250 条记录，以唯一分片 train 组织。它不包含语音或视频本体，只记录调查点的位置、方言归属及关联句子编号，用于配合视频元数据（kalbin/yubao_videos）组装语音检索基准。

数据集由论文《Towards Comprehensive Semantic Speech Embeddings for Chinese Dialects》的作者（Kalvin Chang、Yiwen Shao、Jiahong Li、Dong Yu）整理发布。论文提出面向汉语方言的跨方言语义对齐语音表征，并发布 YuBao 语音检索基准：取 50 句平行口语语料、覆盖 78 个调查点，跨越官话、粤、闽（含闽南）、客家、湘、吴、赣七大方言大类。

## 数据字段

每条记录对应一个调查点，包含四个字段：

- site_id：调查点编号，5 位编码，如 15J15、31C91。
- site：调查点地理位置，按「省份_地市_区县」格式，如「广东_云浮市_罗定县」。
- subgrouping：方言系属或小片说明，如「粤语广府系属不明」「西南官话川黔片陕南小片」；部分记录为空，或给出更长的方言分布描述。
- sentences：该点采录的句子编号列表，编号形如 15J15mb01yf0001，单点最多关联 50 条。

仓库说明提示存在同名调查点（同一区县出现多条记录），如江西上饶广丰区、浙江温州苍南、海南三亚崖州区、福建宁德霞浦、福建南平浦城、海南东方市等，作者建议以括号标注区分。

## 获取与授权

元数据以 Parquet 格式在 Hugging Face 公开托管，标注为中文语种、标签 chinese-dialects 与 benchmark，可经 datasets 库直接加载，或用 hf download kalbin/yubao_sites --repo-type dataset 下载。

平台音频与视频本体不在本数据集内，需在 zhongguoyuyan.cn 注册（需中国大陆手机号）后按调查点获取；视频元数据另存于 kalbin/yubao_videos。关联论文为 arXiv:2601.07274，代码托管于 github.com/kalvinchang/yubao。

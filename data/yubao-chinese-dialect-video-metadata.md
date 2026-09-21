---
title: "语保工程方言视频元数据（YuBao Videos）"
summary: "收录中国语言资源保护工程（语保工程）汉语方言视频句子的元数据，共 57,636 条记录。"
canonical_url: "https://huggingface.co/datasets/kalbin/yubao_videos"
publisher: "kalbin / Centre for the Protection of Language Resources of China"
modality: "text"
access_level: "open"
tags: [汉语方言, 方言视频, 元数据, 语言资源, 语保工程]
---

# 语保工程方言视频元数据（YuBao Videos）

## 亮点

- 收录中国语言资源保护工程（语保工程）汉语方言视频句子的元数据，共 57,636 条记录。
- 每条记录包含方言转写、普通话翻译、国际音标（IPA）转写与英文翻译，并标注所属调查点及方言系属。
- 以 Parquet 格式托管于 Hugging Face，单一 train 切分，共 7 个字符串字段。
- 与方言点元数据 kalbin/yubao_sites 共同构成汉语方言语音检索基准 YuBao，对应论文 arXiv:2601.07274。
- URL：https://huggingface.co/datasets/kalbin/yubao_videos

## 数据内容与来源

语保工程指中国语言资源保护工程及其采录展示平台（zhongguoyuyan.cn）。平台面向中国境内汉语方言调查点，采录方言语音、方言转写、国际音标（IPA）标注与普通话翻译，覆盖 1,000 个汉字、1,200 个词语和 50 个句子的平行语料，涉及 1,300 余个调查点；音频与视频版权归负责该工程的机构（Centre for the Protection of Language Resources of China）。

本数据集 kalbin/yubao_videos 是该平台方言视频句子的元数据集合，共 57,636 条记录，以单一 train 切分组织；视频与音频本体不在其中，每条记录只含转写、翻译、音标及所属调查点信息，用于配合方言点元数据（kalbin/yubao_sites）组装语音检索基准。

数据集由论文《Towards Comprehensive Semantic Speech Embeddings for Chinese Dialects》的作者（Kalvin Chang、Yiwen Shao、Jiahong Li、Dong Yu）整理发布。论文提出面向汉语方言的跨方言语义对齐语音表征，并发布 YuBao 语音检索基准：取 50 句平行口语语料、覆盖 78 个调查点，跨越官话、粤、闽（含闽南）、客家、湘、吴、赣七大方言大类。本数据集承载该基准所需的句子级元数据，其中 english 字段共有 50 种取值，与 50 个平行句子对应。

## 数据字段

每条记录对应一个视频句子，包含七个字符串字段：

- transcript：方言转写，如「张仔琴日钓到条大鱼我冇钓倒」。
- translation：普通话翻译，如「小张昨天钓了一条大鱼我没有钓到鱼」。
- ipa：国际音标转写，标注声调，如「tsœŋ55tsɐi35khɐm21…」。
- english：英文翻译，如「Xiao Zhang caught a big fish yesterday, but I didn't catch any.」。
- utterance_id：句子唯一编号，形如 15J15mb01yf0001，前五位为调查点编号，与 yubao_sites 的 site_id 对应。
- site：调查点地理位置，按「省份_地市_区县」格式，如「广东_云浮市_罗定县」。
- subgrouping：方言系属或小片说明，如「粤语广府系属不明」；部分为较长的方言分布描述。

方言转写保留对答结构，用 a./b. 分隔一问一答，如「你平时食烟冇冇我冇食烟㗎」对应普通话「你平时抽烟吗不我不抽烟」，音标与英文翻译同步保留该结构。

## 文件组织

数据以单个 Parquet 文件 data/train-00000-of-00001.parquet 发布，下载大小约 4.5 MB（4,749,377 字节），对应配置 default 与切分 train。仓库创建于 2025-12-19，最近更新于 2026-01-14。

## 获取与授权

元数据以 Parquet 格式在 Hugging Face 公开托管，标注中文语种、任务 automatic-speech-recognition 与 translation，可经 datasets 库直接加载，或用 hf download kalbin/yubao_videos --repo-type dataset 下载。

视频与音频本体不在本数据集内，需在 zhongguoyuyan.cn 注册（需中国大陆手机号）后按调查点下载视频（平台当前仅提供视频、不含独立音频），再由视频抽取音频。音频与视频版权归负责语保工程的机构（Centre for the Protection of Language Resources of China）。关联论文为 arXiv:2601.07274，代码托管于 github.com/kalvinchang/yubao。

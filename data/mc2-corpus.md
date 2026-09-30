---
title: "MC² 中国少数民族语言多语言语料库（MC²）"
summary: "面向中国少数民族语言的最大开源多语言语料库，覆盖藏语、维吾尔语、哈萨克语（阿拉伯字母）与蒙古语（传统蒙古文）四种语言。"
canonical_url: "https://huggingface.co/datasets/pkupie/mc2_corpus"
publisher: "北京大学"
modality: "text"
access_level: "open"
---

# MC² 中国少数民族语言多语言语料库（MC²）

## 亮点

- 面向中国少数民族语言的最大开源多语言语料库，覆盖藏语、维吾尔语、哈萨克语（阿拉伯字母）与蒙古语（传统蒙古文）四种语言。
- 数据规模（full 版）：藏文约 2.2GB、维吾尔约 736MB、哈萨克（阿拉伯字母）约 937MB、蒙古（传统蒙古文）约 970MB。
- 许可协议：CC0（Public Domain）。
- 关注长期被忽略的文字系统（哈萨克阿拉伯字母、传统蒙古文），强调数据质量与地理文化感知。
- URL：https://huggingface.co/datasets/pkupie/mc2_corpus

## 数据内容

MC²（Multilingual Corpus of Minority Languages in China）是北京大学 Zhang Chen、Tao Mingxu、Huang Quzhe、Lin Jiuheng、Chen Zhibin、Feng Yansong 等发布的少数民族语言语料库，论文发表于 ACL 2024（DOI 10.18653/v1/2024.acl-long.479）。作者指出，现有大语言模型对低资源语言、尤其是中国少数民族语言理解不足，根源在于预训练数据稀缺，故构建这一同类型中规模最大的开源语料。

语料覆盖四种语言，各含两个子集：MC² (crawl) 为新建的网络爬取部分，MC² (full) 为整合 CulturaX、Wikipedia 等既有资源后的完整集。数据为 JSON 行格式，每条含 title、text、url 三个字段；蒙古子集于 2024 年 6 月由 874MB 更新为 970MB。

## 获取与许可

数据以 CC0（Public Domain）发布，北京大学在法律允许范围内放弃对 MC² 的版权及相关权利；网络爬取部分可从 Hugging Face 直接下载，CulturaX 与 Wikipedia 部分需下载原始数据后用 GitHub 仓库（luciusssss/mc2_corpus）提供的脚本处理。配套发布两个预训练模型 MC²XLMR-large（基于 XLM-RoBERTa-large）与 MC²Llama-13B（基于 Llama2-13B），并另提供少数民族语言评测套件 MiLiC-Eval。

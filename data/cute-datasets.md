---
title: "CUTE 中英维藏四语跨语言知识迁移数据集（CUTE）"
summary: "面向低资源语言跨语言知识迁移的四语数据集，覆盖中文、英文两个高资源语言与维吾尔语、藏语两个低资源语言。"
canonical_url: "https://huggingface.co/datasets/CMLI-NLP/CUTE-Datasets"
publisher: "中央民族大学 CMLI-NLP"
modality: "text"
access_level: "open"
---

# CUTE 中英维藏四语跨语言知识迁移数据集（CUTE）

## 亮点

- 面向低资源语言跨语言知识迁移的四语数据集，覆盖中文、英文两个高资源语言与维吾尔语、藏语两个低资源语言。
- 由机器翻译构建，含平行与非平行两个各约 25GB 的语料集合，总规模约 50GB。
- 许可协议：CC BY 4.0。
- 是迄今维吾尔语、藏语规模最大的开源语料，规模约为 MC 数据集的 10 倍。
- URL：https://huggingface.co/datasets/CMLI-NLP/CUTE-Datasets

## 数据内容

CUTE（Chinese, Uyghur, Tibetan, English）是中央民族大学 Wenhao Zhuang、Yuan Sun 等发布的多语言数据集，论文发表于 arXiv（2509.16914，2025 年 9 月）。作者指出，大语言模型在资源丰富语言上的能力突出，但对低资源语言支持不足，主要源于训练语料稀缺，故以机器翻译方式从资源丰富语言扩充低资源语言数据，构建这一平行与非平行并存的四语语料。

数据集覆盖中文、英文两个高资源语言与维吾尔语、藏语两个低资源语言；构建前经母语者人工评估，确认中维、中藏机器翻译质量接近中英翻译水平。维吾尔语与藏语部分规模为迄今最大开源语料，约为既有 MC 数据集的 10 倍，且采用机器翻译避免了语言误标问题，语言与内容领域分布更均衡。Hugging Face 上以 text 字段提供，约 426 万行、单一 train 切分。

## 获取与许可

数据以 CC BY 4.0 发布，可从 Hugging Face 直接下载；论文与代码见 GitHub 仓库 CMLI-NLP/CUTE。配套发布基于不同语料类型训练的 CUTE-Llama 两个版本，用于验证平行语料在高低资源语言间知识迁移中的作用。

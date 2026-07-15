---
title: "文化视觉问答数据集"
summary: "用于评估视觉语言模型文化理解能力的视觉问答基准，覆盖多国文化内容。"
canonical_url: "https://huggingface.co/datasets/mair-lab/CulturalVQA"
publisher: "MAIR Lab"
modality: "multimodal"
access_level: "open"
tags: ["视觉问答", "VQA", "文化理解", "视觉语言模型", "Hugging Face", "图像问答", "跨文化", "CC BY-SA 4.0"]
---

# 文化视觉问答数据集
## 要点
- 问答基准（Q&A Benchmark）数据集。
- 2378组图像，每个问题对应1-5个答案，涵盖5大洲11个国家的文化内容。
- 覆盖服饰、食物、饮品、仪式和传统。
- 数据大小：1.1GB
- 许可协议：CC BY-SA 4.0
- URL：https://huggingface.co/datasets/mair-lab/CulturalVQA
## 数据介绍
本数据集旨在评估视觉语言模型队不同地理区域文化的理解能力。

如需加载并使用，可以使用以下命令：
```
from datasets import load_dataset

culturalvqa_dataset = load_dataset('mair-lab/CulturalVQA')
```

数据集加载后，每个样本包含以下字段：数据集加载后，每个样本包含以下字段：
- `u_id`：每组图像—问题对的唯一标识符。
- `image`：以二进制格式存储的图像数据。
- `question`：与图像相关的问题。
- `facet`：该图像—问题对所属的文化维度。
- `country`：该图像—问题对所属的国家。
- `all_answers`：参与者针对某一问题提供的全部答案。
## 引用规则
> @inproceedings{nayak-etal-2024-benchmarking,
>     title = "Benchmarking Vision Language Models for Cultural Understanding",
>     author = "Nayak, Shravan  and
>       Jain, Kanishk  and
>       Awal, Rabiul  and
>       Reddy, Siva  and
>       Steenkiste, Sjoerd Van  and
>       Hendricks, Lisa Anne  and
>       Stanczak, Karolina  and
>       Agrawal, Aishwarya",
>     editor = "Al-Onaizan, Yaser  and
>       Bansal, Mohit  and
>       Chen, Yun-Nung",
>     booktitle = "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing",
>     month = nov,
>     year = "2024",
>     address = "Miami, Florida, USA",
>     publisher = "Association for Computational Linguistics",
>     url = "https://aclanthology.org/2024.emnlp-main.329",
>     pages = "5769--5790"
> }

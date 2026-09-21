---
title: "中国食文化视觉问答数据集（FoodieQA）"
summary: "FoodieQA 是一个面向中国地方食物文化细粒度理解的多模态问答数据集。"
canonical_url: "https://huggingface.co/datasets/lyan62/FoodieQA"
publisher: "lyan62等"
modality: "multimodal"
access_level: "open"
tags: [基准测试, 多模态VQA, 数据集评测, 文化偏置, 文化理解, 机器学习, 视觉问答, 语义检索]
---

# 中国食文化视觉问答数据集（FoodieQA）
## 亮点
- FoodieQA 是一个面向中国地方食物文化细粒度理解的多模态问答数据集。
- 数据任务包括 Multi-image VQA、Single-image VQA 和 TextQA。
- 数据基于 389 张独立食物图片和 350 个独立食物条目构建。
- 食物图片由个人志愿者采集，页面说明中强调图片不是从网络收集。
- 数据语言包括中文和英文。
- 数据格式为 imagefolder。
- 数据文件总大小：864MB。
- 许可协议：CC BY-NC-ND 4.0。
- URL：https://huggingface.co/datasets/lyan62/FoodieQA

## 数据内容
FoodieQA 的完整题名为“FoodieQA: A Multimodal Dataset for Fine-Grained Understanding of Chinese Food Culture”。数据围绕中国地方食物文化构建，问题类型覆盖图像问答和文本问答。页面说明中写明，数据集用于评估视觉语言模型对中国食物文化的细粒度理解能力。

数据包含 389 张独立食物图片和 350 个独立食物条目。图片由个人志愿者采集，而不是从网页直接收集。页面说明中将这一点与评测公平性联系在一起，避免模型因为训练阶段见过网络图片而影响测试结果。

## 数据结构
数据文件包括图像文件夹和三个 JSON 问答文件：
- `/images`：包含 Multi-image VQA 和 Single-image VQA 任务所需图片。
- `mivqa_tidy.json`：Multi-image VQA 任务问题。
- `sivqa_tidy.json`：Single-image VQA 任务问题。
- `textqa_tidy.json`：TextQA 任务问题。

`mivqa_tidy.json` 的字段包括 question、choices、answer、question_type、question_id、ann_group、images 和 question_en。其中 images 字段可以包含多张图片路径。

`sivqa_tidy.json` 的字段包括 question、choices、answer、question_type、food_name、question_id、food_meta、question_en 和 choices_en。food_meta 中包含 main_ingredient、id、food_name、food_type、food_location 和 food_file 等信息。

`textqa_tidy.json` 的字段包括 question、choices、answer、question_type、food_name、cuisine_type 和 question_id。

## 使用条件
页面说明中写明，下载和使用数据即表示用户已阅读、理解并同意相关使用条款。条款包括：
- 数据仅可用于研究目的，不得用于商业活动。
- 数据只能用于评测，不得用于训练模型或系统。
- 使用数据时需遵守适用法律法规。
- 基于该数据产生的论文或展示需要注明来源。
- 数据采用 CC BY-NC-ND 4.0 许可协议。

Hugging Face 页面还显示，访问该数据集文件和内容前需要同意共享联系信息，并接受访问条件。

## 评测信息
页面列出了 VQA 和 TextQA 任务上的若干模型结果。VQA 表格包含 Multi-image VQA 中文、Multi-image VQA 英文、Single-image VQA 中文、Single-image VQA 英文四个评测列。页面中列出的模型包括 Phi-3-vision-4.2B、Idefics2-8B、Mantis-8B、Qwen-VL-12B、Yi-VL、GPT-4V 和 GPT-4o。

TextQA 表格列出了 Phi-3-medium、Mistral-7B-instruct、Llama3-8B-Chinese、YI、Qwen2-7B-instruct 和 GPT-4 等模型的 Best Accuracy。

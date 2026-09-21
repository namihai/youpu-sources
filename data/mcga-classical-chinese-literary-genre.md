---
title: "古典中文文学体裁音频语料库（MCGA）"
summary: "首个面向中文古典研究领域的大规模开源音频语料库，119 小时、22,008 条样本，全部为普通话母语者朗读。"
canonical_url: "https://huggingface.co/datasets/yxdu/MCGA"
publisher: "yxdu / MCGA authors"
modality: "multimodal"
access_level: "open"
tags: [古典文学, 音频语料, 文体识别, 中文语料, 朗读]
---

# 古典中文文学体裁音频语料库（MCGA）

## 亮点

- 首个面向中文古典研究领域的大规模开源音频语料库，119 小时、22,008 条样本，全部为普通话母语者朗读。
- 覆盖赋、诗、文、词、曲五大体裁，跨越 11 个历史时期，形成 37 个时期-体裁类别，收录 4,497 部作品。
- 每段音频附带自动语音识别、语音到文本翻译、语音情感描述、口语问答、语音理解、语音推理六类任务标注。
- 许可证 CC BY-NC-SA-4.0，录音经版权转让授权，录音与质检志愿者均签署劳动协议并获酬。
- URL：https://huggingface.co/datasets/yxdu/MCGA

## 数据内容与来源

MCGA（Multi-task Classical Chinese Literary Genre Audio Corpus）是首个面向中文古典研究（CCS）的大规模、开源、完全自有版权的音频语料库，由哈尔滨工业大学、鹏城实验室、华南理工大学等单位联合构建，论文发表于 ACL 2026 Findings（arXiv:2601.09270）。

语料共 22,008 条样本、约 119 小时，按 train / val / test 三个切分组织（18,571 / 1,489 / 1,948 条）。文本取自网络公开的古典文学原文及对应拼音，均为公有领域（成书逾 150 年）；文本先分段，使每段朗读时长不超过 30 秒，再由 28 名普通话母语者（13 男 15 女，18—40 岁，约半数为中文专业）通过专用网站朗读，每段至少由一男一女各读一遍，朗读时要求语调贴合文本情感、环境安静。

## 数据字段

每条记录以音频片段为核心，关联 25 个字段，包括：

- 基础元数据：id、author（作者）、title（篇名）、dynasty（朝代）、genre（体裁）、gender（朗读者性别）。
- audio：音频片段（音频特征列，decode 关闭）。
- asr：普通话朗读转写；s2tt：语音到文本翻译，将朗读的文言转译为现代白话。
- sec_1 / sec_2 / sec_3：语音情感描述（SEC）的三段标注。
- sqa / sqa_a：口语问答的问题与答案；su / su_a：语音理解；sr / sr_a：语音推理。
- time：音频时长（秒）；asr_split、s2tt_split、sec_split、sqa_split、su_split、sr_split：各任务对应的切分标记。

六类语音任务的问答对由 DeepSeek-V3.2 基于全文语境生成，并经 DeepSeek-V3.2、GPT-5-mini、Gemini-3-Flash 三重校验过滤；验证集与测试集另经人工核验，发音错误或背景噪声的低质量样本被移除。

## 文件组织

数据在 Hugging Face 上以 Parquet 格式分片发布（data/ 目录，按 train、val、test 三个切分），下载大小约 1.06 GB（1,138,130,667 字节）；仓库另附 MCGA_train.tar.gz、MCGA_val.tar.gz、MCGA_test.tar.gz 三个原始音频压缩包，仓库总占用约 14.3 GB。仓库创建于 2026-01-14，最近更新于 2026-07-29。

## 获取与授权

数据集在 Hugging Face 公开托管，语言标注为中文，任务标注为 automatic-speech-recognition 与 audio-text-to-text，许可证 CC BY-NC-SA-4.0，可经 datasets 库直接加载，或用 hf download yxdu/MCGA --repo-type dataset 下载；也可克隆 github.com/yxduir/MCGA 后运行 down_data.sh 下载并解压三个 tar.gz 压缩包。

全部音频由朗读者本人录制并完成版权转让，录音与质检志愿者签署劳动协议并获得报酬，数据集因此具备完整版权授权。关联论文为 arXiv:2601.09270（ACL 2026 Findings），对 10 个多模态大模型的评估显示，当前模型在 MCGA 测试集上仍面临较大挑战。

---
title: "中国古典文献语料集（Chinese Classical Corpus）"
summary: "面向大语言模型训练与评测的中国古典文献结构化语料，覆盖十三经（完整）、说文解字、资治通鉴与二十四史前 15 部，共 30 部典籍。"
canonical_url: "https://huggingface.co/datasets/gujilab/chinese-classical-corpus"
publisher: "gujilab"
modality: "text"
access_level: "open"
---

# 中国古典文献语料集（Chinese Classical Corpus）

## 亮点

- 面向大语言模型训练与评测的中国古典文献结构化语料，覆盖十三经（完整）、说文解字、资治通鉴与二十四史前 15 部，共 30 部典籍。
- 源语料含 12,005 条章节/篇/卷级记录、约 1,724 万字，另有约 197 万条古译今、今译古与断句指令对。
- 许可协议：数据集以 CC0 1.0 Universal 释出（代码以 MIT 释出）。
- 提供 corpus、translate、punctuate 三种配置，可通过 Hugging Face datasets 库直接加载。
- URL：https://huggingface.co/datasets/gujilab/chinese-classical-corpus

## 数据内容

Chinese Classical Corpus 是 gujilab 发布的古典文献结构化语料集，当前版本 v1.3。它将殆知阁古代文献、chinese-poetry、中文维基文库、ctext.org、chtxt、NiuTrans 等公开文本整理为统一 JSON 结构的清洁语料，按篇章、卷、字头组织，覆盖 30 部典籍：说文解字（9,831 字头）；经部为论语、孟子、大学、中庸、诗经、尚书、礼记、周易、春秋左传、春秋公羊传、春秋穀梁传、孝经、尔雅；史部为二十四史前 15 部（史记、汉书、后汉书、三国志、晋书、宋书、南齐书、梁书、陈书、魏书、北齐书、周书、南史、北史、隋书），另含编年体资治通鉴 294 卷。

## 数据配置

- corpus：源语料，12,005 条章节/篇/卷级记录，约 1,724 万字。通用字段为 id、source、author、era、category、content；字书类另含 char、radical、pinyin、fanqie，经类另含 chapter、subchapter、section、title，史类另含 volume、volume_suffix、chapter。
- translate：古译今与今译古双向翻译指令，共 1,924,378 条，覆盖 97 部典籍，来源为 NiuTrans/Classical-Modern（MIT）。
- punctuate：断句加标点指令，共 46,546 条，从 corpus 抽取章节段并去除标点作为输入、原文作为输出，覆盖 14 部正史与经传。

## 获取与许可

数据可通过 Hugging Face datasets 库按配置加载，例如 `load_dataset("gujilab/chinese-classical-corpus", "corpus")`；代码仓库 github.com/gujilab/chinese-classical-corpus 提供完整抽取流程与 14 个 Python 脚本。translate 指令数据约 640 MB jsonl，punctuate 约 60 MB jsonl。数据集以 CC0 1.0 Universal 释出，无附加限制；代码以 MIT 释出。

发布者列出的已知数据问题包括：说文解字仍有 356 字以 □ 表示（约 3.6%，跨来源无法消歧）；资治通鉴卷 258 的作者属字在源文中误作「寀」（应作「宋」）；极个别生僻字可能在转换中丢失。配套评测基准 gujilab/chinese-classical-bench 从本语料抽样构建。

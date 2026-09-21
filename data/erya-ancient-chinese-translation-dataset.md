---
title: "尔雅古汉语翻译数据集（Erya）"
summary: "作者称为目前规模最大的古汉语资源：单语部分约 8,880 万条古文句子、约 19.4 亿字符，平均句长 21.9 字。"
canonical_url: "https://huggingface.co/datasets/RUCAIBox/Erya-dataset"
publisher: "RUCAIBox"
modality: "text"
access_level: "open"
tags: [古汉语, 翻译, 文言文, 中文NLP, 语料库]
---

# 尔雅古汉语翻译数据集（Erya）

## 亮点

- 作者称为目前规模最大的古汉语资源：单语部分约 8,880 万条古文句子、约 19.4 亿字符，平均句长 21.9 字。
- 古文—现代文平行语料约 208.8 万句对、约 8,477 万字符，古文与现代文平均句长分别为 17.3 与 23.3 字。
- 三个压缩包各司其职：monolingual.tgz（古文单语）、trans.tgz（古文—现代文平行）、finetune.tgz（典籍翻译基准），trans 与 finetune 数据不重叠。
- 内置覆盖汉书、明史、史记、太平广记、新唐书、徐霞客游记六部典籍的古文翻译基准，配套发布 Erya 与 Erya4FT 两个模型。
- 许可证 Apache-2.0，对应 NLPCC 2023 论文《Towards Effective Ancient Chinese Translation: Dataset, Model, and Evaluation》。
- URL：https://huggingface.co/datasets/RUCAIBox/Erya-dataset

## 数据内容与来源

尔雅（Erya）由中国人民大学高瓴人工智能学院 RUCAIBox 团队构建，是论文《Towards Effective Ancient Chinese Translation: Dataset, Model, and Evaluation》（NLPCC 2023，arXiv:2308.00240）发布的数据集，官方代码托管于 github.com/RUCAIBox/Erya，实现基于文本生成库 TextBox 2.0。

语料从互联网爬取并结合开源数据整理而成，覆盖公元前 1000 年至公元 1600 年间的历代古文。清洗流程包括三方面：一是噪声过滤，删除汉字以外的字符（如阿拉伯数字、英文），将繁体转为简体，统一非文字符号（如把「转为“）；二是去重，采用 MinHash 算法比较不同来源的文本片段，相似度低于 0.5 时仅保留一份；三是自动断句，对缺少标点的单语文本用 guwen-punc 工具补加标点。

经清洗后，数据集按文本与时代特征分类：参照传统「四部分类」与时代划分，分出 History（历史，含三个时段——上古：先秦至汉、公元 3 世纪前；中古：三国至宋、公元 4—12 世纪；近古：元至清、公元 13—19 世纪）、Article（文章，含诗词、散文、哲学著作与文论）与 Novel（小说，兼具文言与近古白话特征）三大类。论文表 1 对比显示，其单语与平行规模均居所列同类资源之首。

## 数据字段

数据集不含 Hugging Face 列式字段（无 Parquet 与切分），以句对齐层级组织，分三类内容：

- 单语数据（monolingual.tgz）：古文句子，用于学习古文一般语言知识，共 88,808,928 句。
- 平行数据（trans.tgz）：古文句子与现代文句子逐句对齐的句对，用于弥合古今语言差异，共 2,087,804 句对。
- 基准数据（finetune.tgz）：选自典籍的古文—现代文平行句对，附 train / valid / test 划分，作为翻译评测基准，与 trans.tgz 不重叠。

论文表 2 给出其中五部典籍的划分规模与平均句长（#ASL）：

- 汉书（Book of Han）：训练 18,646 / 验证 2,331 / 测试 2,331，平均句长 21.2。
- 新唐书（New Tang History）：训练 9,396 / 验证 1,174 / 测试 1,175，平均句长 20.5。
- 明史（Ming History）：训练 66,730 / 验证 8,341 / 测试 8,342，平均句长 21.5。
- 徐霞客游记（Xu Xiake's Travels）：训练 16,649 / 验证 2,081 / 测试 2,082，平均句长 25.1。
- 太平广记（Taiping Guangji）：训练 45,162 / 验证 5,645 / 测试 5,646，平均句长 20.0。

（GitHub README 另列史记（Shi Ji）一项，论文表 2 未给出其统计，故不在此补充数字。）

## 文件组织

仓库以三个 tgz 压缩包托管于 Hugging Face：monolingual.tgz、trans.tgz、finetune.tgz，另附 README.md 与 .gitattributes；仓库总占用约 2.74 GB（2,939,178,882 字节）。仓库创建于 2023-07-21，最近更新于 2023-07-24。

该仓库没有 Parquet 分片或可在线预览的列式切分，属纯文件托管；README 未说明压缩包内部的文件格式与字段命名，需下载解包后按论文所述的句对齐结构使用。

## 获取与授权

数据集在 Hugging Face 公开托管、非门控，许可证 Apache-2.0，任务标注为 translation 与 text-generation，可经 hf download RUCAIBox/Erya-dataset --repo-type dataset 下载，或按 GitHub README 将下载的基准数据（如 xint）放入 TextBox 的 dataset 目录。

配套模型 Erya（可直接做零样本翻译）与 Erya4FT（用于进一步微调）分别发布在 huggingface.co/RUCAIBox/Erya 与 huggingface.co/RUCAIBox/Erya4FT。论文报告 Erya 模型在五个领域的零样本翻译上较 GPT-3.5 提升逾 12.0 BLEU，人工评测优于 ERNIE Bot。

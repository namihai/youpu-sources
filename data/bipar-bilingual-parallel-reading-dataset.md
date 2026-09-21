---
title: "小说中英双语阅读理解数据集（BiPaR）"
summary: "首个公开的双语平行小说式机器阅读理解（MRC）数据集，每个（段落、问题、答案）三元组均以中英双语平行标注，支持单语、多语与跨语言阅读理解。"
canonical_url: "https://multinlp.github.io/BiPaR/"
publisher: "MultiNLP / BiPaR authors"
modality: "text"
access_level: "open"
tags: [小说, 双语语料, 阅读理解, 中文NLP, 跨语言]
---

# 小说中英双语阅读理解数据集（BiPaR）

## 亮点

- 首个公开的双语平行小说式机器阅读理解（MRC）数据集，每个（段落、问题、答案）三元组均以中英双语平行标注，支持单语、多语与跨语言阅读理解。
- 从《鹿鼎记》《天龙八部》《三体》《了不起的盖茨比》《老人与海》《哈利·波特》六部中英文小说收集 3,667 个双语平行段落，构建 14,668 个平行问答对，对应 EMNLP-IJCNLP 2019 长文（arXiv:1910.05040）。
- 答案均为段落中的连续片段，数据格式与 SQuAD 一致；开发集与测试集的每个问题另附多个参考答案。
- 问题以 why（15.6%）、how（9.5%）等类型呈现，解答需指代消解、多句推理与隐式因果理解等能力。
- 许可证 CC BY-NC 4.0；数据与评测脚本托管于 GitHub。
- URL：https://multinlp.github.io/BiPaR/

## 数据内容与来源

BiPaR 由苏州大学计算机科学与技术学院的 Yimin Jing、Deyi Xiong、Yan Zhen 构建，论文发表于 EMNLP-IJCNLP 2019，数据集主页与代码分别托管于 multinlp.github.io/BiPaR 与 github.com/sharejing/BiPaR。

语料取自六部主题不同的中英文小说，涵盖中文武侠、科幻与西方奇幻、现代文学等题材；其中既有中文原著译为英文者，也有英文原著译为中文者。作者在已有中英段落对齐的基础上筛选出 3,667 个双语平行段落，中文段落字数限定在 120—600 之间；同时剔除含诗词、对联、文言词的段落，排除对话过多而难以脱离上下文识别说话者的段落与整段武功打斗描写，并弃用英文比中文少 10 词以上、对齐不可靠的段落。各小说的段落数为：《鹿鼎记》（The Duke of the Mount Deer）1,948 段、《哈利·波特》（Harry Potter）822 段、《三体》（The Three-Body Problem）490 段、《了不起的盖茨比》（The Great Gatsby）245 段、《老人与海》（The Old Man and the Sea）87 段、《天龙八部》（Demi-Gods and Semi-Devils）75 段；全部段落英文平均 227.3 词、中文平均 198.2 词。

问答对由众包人工标注完成，150 名双语标注者、3 名双语审核员与 1 名专家参与。3,667 个段落分为 150 组随机分配，每个段落至少创建 3 个双语平行问答对；答案须为段落中的连续片段，中英文答案不平行时该问题须删除重做，标注者被鼓励优先提出 how、why 类问题。质量控制采用三轮抽样复核：每组随机抽 30% 交由审核员复核并修正答案，再从每位审核员处抽 5% 交由专家复查，准确率低于 95% 时相关标注者与审核员须返工，该循环执行三次。最终得到 14,668 个问答对，随机划分为训练集 11,668 对、开发集 1,500 对、测试集 1,500 对；开发集与测试集的每个问题另由标注者补充至少两个参考答案，以增强评测稳健性。

## 任务形式

BiPaR 的中英平行结构支持三种阅读理解任务形式。单语 MRC 使用同一语言的段落、问题与答案，即（Pen, Qen, Aen）或（Pzh, Qzh, Azh）。多语 MRC 将中英两套三元组联合输入（Pen, Qen, Aen, Pzh, Qzh, Azh），用于训练同时处理两种语言的单一模型。跨语言 MRC 分两类：其一用某种语言的问题从另一种语言的段落中抽取答案，如（Pen, Qzh, Aen）或（Pzh, Qen, Azh）；其二在一种语言的问题下同时从两种语言的段落中寻找答案，如（Pen, Pzh, Qzh, Azh, Aen）。主页按这四个任务分别列出基线评测榜单，例如单语任务上人类表现为英文 EM 80.50 / F1 91.93、中文 EM 81.50 / F1 92.12，而 BERT-large 英文仅 EM 42.53 / F1 56.48，与人类相差 30 分以上。

## 数据字段与文件组织

每条数据沿用 SQuAD 的 JSON 字段：context 为段落正文，id 为样本标识（如 TRAIN_tian_long_ba_bu_34_QUERY_3_EN，含书名、段落号与问题序号），question 为问题，answers 为答案列表，每项含 answer_start（答案起始位置）与 text（答案片段）。仓库按任务形式分目录存放 JSON 文件：

- Monolingual/EN 与 Monolingual/ZH 各含 Monolingual_*_train/valid/test.json 三份单语文件；
- Multilingual/ 含 zh_and_en_train/valid/test.json 三份中英联合文件；
- Crosslingual/QEN 与 Crosslingual/QZH 各含 Crosslingual_*_train/valid/test.json 三份跨语言文件。

仓库另附评测脚本 cmrc2018_evaluate_changed.py（基于 CMRC2018 的中文评测脚本改写）与跨语言任务样例 cross-lingual-task-4-sample.json。

## 获取与授权

数据与评测脚本在 GitHub（github.com/sharejing/BiPaR）公开下载，许可证为 CC BY-NC 4.0（署名—非商业性使用 4.0 国际）。数据集相关问题可联系 yymmjing@gmail.com。关联论文为 arXiv:1910.05040（EMNLP-IJCNLP 2019），报告了在 BiPaR 上构建的单语、多语与跨语言 MRC 基线模型及其结果。

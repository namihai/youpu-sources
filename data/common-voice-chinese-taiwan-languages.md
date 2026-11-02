---
title: "中文、粤语及台湾原住民族语言朗读语音数据集（Common Voice）"
summary: "Mozilla Common Voice 社区众包语音资源，按语言或地区分别发布，音频与朗读文本、验证投票及说话者自愿提供的信息关联。"
canonical_url: "https://commonvoice.mozilla.org/zh-CN/datasets"
publisher: "Mozilla / Common Voice 社区"
modality: "audio"
access_level: "request"
---

# 中文、粤语及台湾原住民族语言朗读语音数据集（Common Voice）

## 亮点

- Mozilla Common Voice 社区众包语音资源，按语言或地区分别发布，音频与朗读文本、验证投票及说话者自愿提供的信息关联。
- 本卡介绍 Scripted Speech 27.0 的中文相关子集及泰雅语、布农语子集，包含 MP3 音频和 TSV 标注。
- 数据大小：各语种分别打包，中文相关包为 2.96—21.40 GB，泰雅语约 250.93 MB、布农语约 235.71 MB。
- 许可协议：CC0-1.0；经 Mozilla Data Collective 获取时，另有禁止识别说话者身份及禁止重新托管、转分享数据的条件。
- URL：https://commonvoice.mozilla.org/zh-CN/datasets

## 数据内容

Common Voice 由 Mozilla 发起，通过社区志愿者录制语音、提交文本和核验录音，建立多语言语音资源。朗读语音以给定句子为录音提示，记录说话者实际朗读的声音，并由其他参与者判断音频与文本是否相符。同一句文本可以对应多个录音片段，文本句数与音频片段数采用不同统计口径。

以下子集属于 Scripted Speech 27.0，语料版本标识为 `cv-corpus-27.0-2026-09-11`，数据发布页所列发布日期为 2026 年 9 月 17 日。每种语言或地区单独提供 `.tar.gz` 压缩包，表中大小为各压缩包大小。

| 子集 | 代码 | 压缩包大小 |
|---|---|---|
| 中文（中国大陆） | zh-CN | 21.40 GB |
| 中文（香港） | zh-HK | 3.43 GB |
| 华语（台湾） | zh-TW | 2.96 GB |
| 粤语 | yue | 5.99 GB |
| 泰雅语 | tay | 250.93 MB |
| 布农语 | bnn | 235.71 MB |

香港中文与粤语以不同代码独立发布。粤语子集含 279,396 个录音片段、1,188 位说话者，录音总时长 307.44 小时，其中通过验证的录音为 210.78 小时；其文本库含 28,727 句。台湾华语子集含 2,336 位说话者、131.7 小时录音，其中 79.92 小时通过验证，文本库含 22,778 句。台湾华语文本由 Mozilla 台湾社群、g0v 社群及其他志愿者共同整理，保留繁体中文书写。

泰雅语和布农语子集主要包含台湾维基媒体协会族语录音计划的成果，录音文本取自原住民族语文教材第一至九阶课文。泰雅语涵盖赛考利克、泽敖利等变体；布农语涵盖卓群、卡群、郡群、峦群及丹群等变体，另含获授权的布农语圣经选句。布农语说明特别指出，部分教材文本存在文意或拼写问题，录制时未能预先更正；项目采录的年龄、性别信息也有较大可靠性限制。

## 标注字段与数据组织

音频采用 MP3 格式。录音标注 TSV 每行对应一个片段，`path` 记录音频相对路径，`sentence` 为朗读文本，`sentence_id` 为文本唯一标识，`client_id` 为说话者的哈希标识。`up_votes` 与 `down_votes` 分别记录认为音频与文本相符、不相符的投票数；`locale`、`variant`、`accents` 记录语言地区、变体和口音，`sentence_domain` 记录文本领域。年龄、性别和口音等信息由参与者自愿提供，存在缺失。

文本另有独立的 TSV 表。`validated_sentences.tsv` 收录通过审核的句子，并以 `source`、`is_used`、`clips_count` 记录文本来源、是否仍用于录音以及关联录音数；`unvalidated_sentences.tsv` 保存未通过审核流程的句子及投票、待审或拒绝状态。句子审核与录音验证分别管理。

录音按已验证、未通过验证和其他待定片段分组，另提供训练、开发和测试划分。以香港中文子集为例，124,379 个片段中，94,172 个已验证、4,720 个未通过验证、25,487 个待定；训练、开发和测试分别包含 8,452、5,604、5,604 个片段。这三个划分仅覆盖部分已验证录音，不能将它们之和视为全部已验证片段数。

## 获取与使用条件

数据通过 [Mozilla Data Collective 的 Common Voice 专区](https://mozilladatacollective.com/organization/cmfh0j9o10006ns07jq45h7xk)按语种获取，需创建账户；程序化下载可使用平台 API 或 Python SDK。平台当前对免费账户设置每日 7 次数据集下载限额。

各子集标注 CC0-1.0，同时要求不得尝试识别说话者身份，不得重新托管或转分享数据。Mozilla Data Collective 的[官方说明](https://community.mozilladatacollective.com/faq-why-cant-i-re-host-or-share-common-voice-datasets-that-i-download-from-mdc/)将禁止镜像分发列为平台条款。历史版本采用另行申请的获取流程。

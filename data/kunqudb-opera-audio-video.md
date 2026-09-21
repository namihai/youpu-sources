---
title: "昆曲音视频标注数据集（KunquDB）"
summary: "KunquDB 是一个昆曲音视频标注数据集。"
canonical_url: "https://hualizhou167.github.io/KunquDB/"
publisher: "KunquDB 项目团队"
modality: "multimodal"
access_level: "request"
tags: [机器学习]
---

# 昆曲音视频标注数据集（KunquDB）
## 亮点
- KunquDB 是一个昆曲音视频标注数据集。
- 数据包含 339 位说话人，内容总时长为 128 小时。
- 原始材料来自《昆曲艺术大典》。
- 数据按对白行组织，每条语音片段对应一行标注。
- 标注字段包括视频 ID、开始时间、结束时间、角色名、表演者名、性别、行当/角色类型、发声方式分类和初步文本转写。
- 发声方式分类包括 stage speech（念白）和 singing（演唱）。
- 许可协议：CC BY-NC-SA 4.0。
- 数据大小：128 小时。
- URL：https://hualizhou167.github.io/KunquDB/

## 数据来源
KunquDB 的原始材料来自《昆曲艺术大典》。页面说明中介绍，《昆曲艺术大典》汇集了昆曲 600 余年历史中的文学、音乐和音视频材料，包含超过 2,230 万字文本资料、396 套重印文献、超过 70,000 页文献、127 小时录音、超过 400 小时录像和 6,000 余幅图片，共编为 149 卷。

页面说明提到，研究团队购买《昆曲艺术大典》后，与出版社协商并获得授权，将其中数字资源用于昆曲研究。出版社说明，相关数字资源经出版社批准后仅可用于学术或研究用途，不得非法传播或用于商业用途。

## 数据内容
KunquDB 按对白行组织数据，元数据存储在 CSV 表中。每条 utterance 对应一段视频中的语音或演唱片段，标注内容包括：
- video ID：对应视频编号。
- start 和 end timestamps：片段在视频中的开始与结束时间。
- character name：片段中表演角色的名称。
- performer name：饰演该角色的表演者姓名。
- vocal manner type：发声方式类别，用于区分 stage speech（念白）和 singing（演唱）。
- preliminary content transcription：片段对应的初步文本转写。

页面示例中展示了《牡丹亭》和《牧羊记》的若干标注行，字段包括剧目名称、开始时间、结束时间、角色名、表演者名、发声方式和唱词/念白文本。

## 角色与发声方式
页面统计部分展示了说话人角色类型分布和发声方式分布。角色类型包括：
- Dan（旦）：年轻女性角色。
- LaoDan（老旦）：老年女性角色。
- OtherFemale（其他女性角色）：旦、老旦以外的女性角色。
- XiaoSheng（小生）：年轻男性角色。
- LaoSheng（老生）：老年男性角色。
- OtherMale（其他男性角色）：小生、老生以外的男性角色。
- MultiGender（跨性别角色类型）：同一说话人饰演不同性别角色。

发声方式分布部分用于统计不同 utterance 的 vocal manner frequency。页面说明中提到，各类发声方式的总时长接近相等。

## 数据获取
页面说明中写明，研究者可通过购买《昆曲艺术大典》获得原始视频数据，并需自行获得出版社批准，用于非商业研究。KunquDB 页面只提供标注数据和处理脚本。

如需获取标注数据，需要通过邮件联系 huali.zhou@dukekunshan.edu.cn 或 ming.li369@dukekunshan.edu.cn，并提供所在机构信息以及出版社同意材料。

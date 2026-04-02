# 昆曲音视频数据集（KunquDB）

```yaml
title: 昆曲音视频数据集（KunquDB）
canonical_url: https://hualizhou167.github.io/KunquDB/
domain: 文化资源
content_type: 素材
data_form: 多媒体
data_type: 混合
region: 中国
source_type: 学术机构
source_org: KunquDB 项目团队
permissions: 仅研究 / 禁止商用 / 需授权（需出版方同意）
tags: [昆曲, 戏曲, 音视频, 多模态, 唱白, 角色]
use_cases: [研究分析, AI训练]
```

## 数据集概览

- **数据集名称**：昆曲音视频数据集（KunquDB）
- **覆盖内容**：大规模、带标注的昆曲音视频数据集，包含 339 位说话人、约 128 小时内容；数据源自《昆曲艺术大典》（Kunqu yishu dadian）。数据按“台词行/utterance”组织，提供角色名、表演者（说话人）名、性别、唱/白（vocal manner：singing / stage speech）以及初步文本转写等标注（以项目说明为准）。
- **核心价值**：在戏曲场景下同时提供“音视频 + utterance 级结构化标注”，可支撑说话人/角色相关任务与唱白区分等多模态对齐研究；同时提供标注集与处理脚本，便于复现。
- **适用场景**：戏曲场景说话人验证/识别、角色/唱白分类、多模态检索与分段、教育导赏与检索原型验证（需严格遵循非商用与授权要求）。

## 数据内容说明

1. 数据对象与边界：昆曲表演音视频语料及其 utterance 级标注；标注字段包含 video ID、起止时间戳、角色名（character name）、表演者/说话人名（performer/speaker）、性别、唱白类型（vocal manner：singing / stage speech）、初步文本转写等（以项目说明为准）。
2. 数据组织方式：项目说明为“按对话台词行结构化组织（structured by dialogue lines）”，以便定位到视频中的具体片段；并提供标注数据与处理脚本。
3. 数据规模与粒度：339 位说话人、约 128 小时；utterance 级切分与标注（以项目说明为准）。
4. 数据来源说明：源自《昆曲艺术大典》数字资源；原始视频数据需通过购买书籍并获得出版方同意后用于研究（项目说明）。

## 数据获取方式

### 网页访问

- **链接**：[https://hualizhou167.github.io/KunquDB/](https://hualizhou167.github.io/KunquDB/)
- **说明**：页面包含数据集简介、标注格式说明、论文引用与下载/许可说明。

### 文件下载

- **下载地址**：需邮件联系获取（项目页“download”部分）。
- **格式**：项目团队仅提供“标注数据集（annotation dataset）+ 处理脚本（processing scripts）”；原始视频数据需用户自行购买《昆曲艺术大典》并取得出版方同意后用于非商业研究（项目说明）。
- **申请方式**：发送邮件并附单位/机构信息与出版方同意材料。
- **联系邮箱**：[huali.zhou@dukekunshan.edu.cn](mailto:huali.zhou@dukekunshan.edu.cn)；[ming.li369@dukekunshan.edu.cn](mailto:ming.li369@dukekunshan.edu.cn)

## 使用限制与合规说明

- **版权归属**：与《昆曲艺术大典》数字资源相关的权利以出版方/权利方为准（项目说明强调需获得出版方同意）。
- **使用许可**：标注数据集许可为 CC BY-NC-SA 4.0（非商业使用、署名、相同方式共享；详见项目页 License/Licence 与仓库 LICENSE）。
- **使用限制**：出版方声明其数字资源仅可在出版方批准下用于学术/研究用途，不得非法传播或用于商业用途（项目页 Note/Download）。
- **合规依据**：项目页 Note / Download / License 段落与 LICENSE 文件。
- **敏感性**：不涉及个人隐私为主，但涉及表演者肖像/声音与音视频版权，需按非商用与授权边界使用。

## 数据质量与已知问题

- **完整性**：曲目/流派/场景覆盖可能有限。
- **一致性**：不同录制条件会带来音画质量差异；标注质量可能需要抽样复核。
- **时效性**：不明/待确认
- **稳定性**：依赖项目站点托管。

## 备注

该数据集的独特性在于提供昆曲场景的“音视频 + utterance 级结构化标注”，适合开展说话人/角色相关研究与唱白区分等任务；但获取与使用需同时满足：1）原始视频数据的出版方授权与非商用研究边界；2）按 CC BY-NC-SA 4.0 进行署名与共享，避免二次传播与商业化使用风险。

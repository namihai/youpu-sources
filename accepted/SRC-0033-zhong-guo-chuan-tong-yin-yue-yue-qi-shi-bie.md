# 中国传统音乐乐器识别数据集

```yaml
title: 中国传统音乐乐器识别数据集
canonical_url: https://github.com/HaoranWeiUTD/ChMusic
domain: 文化资源
content_type: 素材
data_form: 多媒体
data_type: 音频
region: 不明/待确认
source_type: 学术机构
source_org: GitHub（HaoranWeiUTD/ChMusic）
permissions: 公开可下载（需外链网盘/Google Drive）
tags: [民族音乐, 传统乐器, 音频分类, 乐器识别]
use_cases: [研究分析, AI训练]
```

## 数据集概览

- **数据集名称**：中国传统乐器识别音频数据集
- **覆盖内容**：用于传统乐器识别模型训练与性能评估的音频数据集，覆盖 11 种乐器：二胡、琵琶、三弦、笛子、唢呐、坠琴、中阮、柳琴、古筝、扬琴、笙。每种乐器包含 5 段传统音乐片段，共 55 段；每段仅由单一乐器演奏。
- **核心价值**：提供基线级、可复现的传统乐器识别数据与配套 baseline（MFCC + KNN / MFCC + CNN），便于快速跑通特征-分类流程与做对照实验。
- **适用场景**：传统乐器识别基线、音频特征与模型对比实验、MIR 教学与研究复现。

## 数据内容说明

1. 数据对象与边界：乐器类别标注的传统音乐片段；每段仅由单一乐器演奏（以仓库说明为准）。
2. 数据组织方式：音频文件为 .wav；文件命名遵循 `x.y.wav`：`x` 为乐器编号（1–11），`y` 为该乐器的片段编号（1–5）（以仓库说明为准）。
3. 规模与粒度：11 类 × 每类 5 段，共 55 段；采样率 44.1kHz、双声道；单段时长约 25–280 秒（以仓库说明为准）。
4. 数据体量：约 530 MB。

## 数据获取方式

### 代码 / Repo

- **Repo**：[https://github.com/HaoranWeiUTD/ChMusic](https://github.com/HaoranWeiUTD/ChMusic)
- **包含内容**：baseline 代码（如 KNN

a [ChMusic.py](http://ChMusic.py)、CNN_[ChMusic.py](http://ChMusic.py)，均以 MFCC 为特征），以及数据集说明。

### 文件下载

- **下载地址**：[https://github.com/HaoranWeiUTD/ChMusic](https://github.com/HaoranWeiUTD/ChMusic)
- **格式**：WAV（双声道，44.1kHz；以仓库说明为准）
- **说明**：数据约 530MB；如网盘链接失效需在仓库内更新或联系作者。

## 使用限制与合规说明

- **版权归属**：不明/待确认（片段演奏/录制相关权利边界需以作者/采集声明为准）。
- **使用许可**：MIT License（仓库声明；注意该许可主要约束仓库代码/内容，音频数据的权利边界仍建议单独核验）。
- **禁止事项**：不明/待确认
- **合规依据**：仓库 LICENSE（MIT）与数据集说明。
- **敏感性**：一般不涉及个人信息。

## 数据质量与已知问题

- **完整性**：样本量小，类别内多样性不足。
- **一致性**：不同来源音频可能存在采样率/响度差异。
- **时效性**：一次性数据。
- **稳定性**：依赖 GitHub 托管。

## 备注

该数据集以“小规模、单乐器、长片段（25–280s）WAV”的形式覆盖 11 种传统乐器，适合作为识别任务的基线与复现实验。

---
title: "中国竹笛演奏技法标注数据集（CBFdataset）"
summary: "CBFdataset 是面向中国竹笛（笛子，dizi）演奏的首个公开数据集，专为在真实演奏语境下分析演奏技法而构建。"
canonical_url: "https://zenodo.org/record/5744336"
publisher: "Zenodo"
modality: "audio"
access_level: "open"
tags: [Zenodo, 数据集评测, 机器学习, 民族音乐, 演奏技法, 演奏音频, 竹笛, 语音识别]
---

# 中国竹笛演奏技法标注数据集（CBFdataset）

## 亮点

- CBFdataset 是面向中国竹笛（笛子，dizi）演奏的首个公开数据集，专为在真实演奏语境下分析演奏技法而构建。
- 由 10 位专业竹笛演奏者录制，含经典曲目完整演奏与独立技法录音，并附 7 种演奏技法的专家标注。
- 7 种标注技法：气震音（vibrato）、震音（tremolo）、颤音（trill）、花舌（flutter-tongue）、倚音（acciaccatura）、滑音（portamento）、滑音（glissando）。
- 在专业录音棚用 Zoom H6 以 44.1 kHz/24 bit 录制；单文件 CBFdataset.zip 约 1.57 GB，总时长约 2.6 小时。
- 许可协议：CC BY 4.0。
- URL：https://zenodo.org/record/5744336

## 数据内容与来源

该数据集全称 CBFdataset: A Dataset of Chinese Bamboo Flute Performances，收录单声部（monophonic）的经典竹笛曲目完整演奏与独立技法录音，录音由 10 位专业竹笛演奏者完成，并配有演奏者本人对七种演奏技法的专家标注。七种技法分为两组：周期调制类（periodic modulations）四种——气震音（vibrato）、震音（tremolo）、颤音（trill）、花舌（flutter-tongue）；音高演变类（pitch evolution）三种——倚音（acciaccatura）、滑音（portamento）、滑音（glissando）。

收录曲目共四首经典竹笛曲：扬鞭催马运粮忙（Busy Delivering Harvest）、喜相逢（Jolly Meeting）、早晨（Morning）、鹧鸪飞（Flying Partridge）。所有数据在专业录音棚用 Zoom H6 录音机以 44.1 kHz/24 bit 录制。演奏者按笛型 C 调与 G 调分组（分别对应南派与北派最具代表性的笛型），各自使用自己的竹笛。

## 标注方式

技法标注由演奏者本人完成，每条标注包含该技法片段的起止时间（onset–offset）与技法标签；对持续时间较长的调制，标注遵循每段至少包含三个调制单元的约定。互相重叠的演奏技法分别单独标注。

## 版本与组织

该数据集按版本逐步扩充。V1.0 仅包含 CBF-periDB（周期调制子集）；V1.1 将数据拆分为两个子集——CBF-periDB 与 CBF-petsDB，前者含全部完整曲目、独立技法及四种周期调制技法（气震音、震音、颤音、花舌）标注，后者含同样的完整曲目与独立技法，以及三种音高演变类技法（倚音、滑音、滑音）标注；V1.2 为完整版，总时长约 2.6 小时。当前 Zenodo 记录即为 Version 1.2，发布为单个 CBFdataset.zip 压缩包，约 1.57 GB（1,571,110,267 字节）。

## 访问与授权

数据集在 Zenodo 上开放获取，许可协议为 CC BY 4.0。相关更新、演示与可复现代码原托管于 c4dm.eecs.qmul.ac.uk/CBFdataset.html。作者为 Changhong Wang、Emmanouil Benetos（伦敦玛丽女王大学）与 Elaine Chew（CNRS-UMR9912/STMS IRCAM），另有 Vincent Lostanlen 参与论文撰写。使用本数据集请引用论文：Changhong Wang, Emmanouil Benetos, Vincent Lostanlen, and Elaine Chew, "Adaptive Scattering Transforms for Playing Technique Recognition," IEEE/ACM Transactions on Audio, Speech, and Language Processing (TASLP), 30 (2022): 1407–1421。

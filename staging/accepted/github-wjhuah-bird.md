---
title: "BIRD: Bronze Inscription Restoration and Dating"
summary: "面向青铜铭文修复与年代判定的开源数据与建模仓库，包含铭文文本、断代标注、领域语料和字形异体关系。"
canonical_url: "https://github.com/wjhuah/BIRD"
publisher: "wjhuah（GitHub）"
modality: "text"
access_level: "open"
tags: [古文字, 文化遗产, 深度学习]
---

## 来源概述
BIRD 是一个用于中国青铜铭文修复与断代研究的开源仓库。仓库 README 明确说明其数据包括编码后的青铜铭文文本、古文字资源、领域自适应预训练语料、修复任务文本、断代标注表和字形异体关系文件。

## 收录内容与边界
收录内容主要位于仓库 `data/` 目录，包括 `dapt.txt` 领域语料、`tapt_*.txt` 修复任务文本、`dating.csv` 断代标签数据，以及 `*.edge` 字形异体关系。该条目不应被理解为图像或拓片原始数据集，核心数据形态是编码文本与关系数据。

## 获取方式
通过 GitHub 仓库直接访问和下载代码与数据文件。

## 使用与访问限制
仓库标注为 MIT license；使用时仍应按论文引用要求引用对应研究。

## 质量与风险
该数据适合文本建模、修复和断代任务；如果任务需要原始青铜器图像、拓片图像或逐字图像标注，需要另行寻找图像来源。

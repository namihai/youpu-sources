---
title: "中国古汉语OCR共享任务数据集"
summary: "面向古汉语 OCR 的共享任务数据集（多模态 LLM 导向）；测试集 2026-02-03 发布；训练集需注册后获取，含古籍图文对。"
canonical_url: "https://github.com/GoThereGit/EvaHan"
publisher: "EvaHan 共享任务组织方"
modality: "image"
access_level: "request"
tags: [机器学习, 计算机视觉]
---

## 来源概述
面向古汉语 OCR 的共享任务数据集（多模态 LLM 导向）；测试集 2026-02-03 发布；训练集需注册后获取，含古籍图文对。

## 收录内容与边界
1. 数据对象与边界：古籍页面图像与对应文本标注/转写，样本以图像-文本对形式组织（文本为繁体中文；项目页）。
2. 数据组织方式：项目页说明包含 3 个子集（A/B/C）：A 印刷体（Printed Texts，含《四库全书》来源样例）；B 混合版式（Mixed image-text / Mixed Layouts）；C 手写体（Handwritten Texts，含佛典相关手写资料；项目页）。
3. 数据格式：图像-文本对 + JSON 文件（项目页说明为“stored in JSON files with multiple encoding formats”，以发布包为准）。
4. 数据量：训练集每个子集约 5000 对图像-文本；测试集每个子集约 200–500 对图像-文本（项目页）。

## 获取方式
需申请

## 使用与访问限制
GitHub 仓库公开可访问；复用代码或数据应以仓库 LICENSE、README 和引用说明为准。

## 质量与风险
- **完整性**：面向评测，覆盖面由赛题定义，不等同于“通用 OCR 全覆盖”。
- **一致性**：赛题通常提供统一标注口径，但不同阶段可能发生格式迭代。
- **时效性**：赛程结束后可能不再更新。
- **稳定性**：依赖赛事方发布与托管平台可用性。

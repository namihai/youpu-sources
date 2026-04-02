# 文化视觉问答数据集

```yaml
title: 文化视觉问答数据集
canonical_url: https://culturalvqa.org/
domain: 文化实践
content_type: 素材
data_form: 多媒体
data_type: 混合
region: 不明/待确认
source_type: 学术机构
source_org: Mila Quebec AI Institute/Université de Montréal/McGill University/Google Research/Google DeepMind
permissions: 可访问
tags: [CulturalVQA, 跨文化视觉问答, 多文化理解]
use_cases: [研究分析, AI训练, 政策评估]
```

## 数据集概览

- **数据集名称**：文化视觉问答数据集
- **覆盖内容**：覆盖 11 国文化相关图像与开放式问答（约 2328 张图像、2378 组问答），涵盖传统、仪式、食物、饮品、服饰等五类文化面向；开放式答案受 prompt 与归一策略影响较大，需统一评测规则。
- **核心价值**：把“文化理解”落到可比较的基准测试维度，便于发现模型在不同文化概念与地区上的偏置与泛化弱点，可用于安全与合规视角的文化敏感性评估。
- **适用场景**：多模态模型评测与对齐 / 跨文化理解研究 / 文化偏置与安全评测 / 教学与案例分析

## 数据内容说明

1. 数据集由 2378 对图像-问答对组成，包含 2328 张独立图像。
2. 每个问题有 1–5 个人工标注答案。
3. 五类文化面向：Traditions、Rituals、Food、Drink、Clothing。

## 数据获取方式

### 网页访问

- **链接**：[https://culturalvqa.org/](https://culturalvqa.org/)

### 文件下载

- **下载地址**：[https://huggingface.co/datasets/mair-lab/CulturalVQA](https://huggingface.co/datasets/mair-lab/CulturalVQA)
- **格式**：JSON/CSV

### API（示例）

```bash
curl -X GET \
	"https://datasets-server.huggingface.co/rows?dataset=mair-lab%2FCulturalVQA&config=default&split=test&offset=0&length=100"
```

## 使用限制与合规说明

- **使用许可**：CC BY 4.0
- **敏感性**：不涉及个人隐私。

## 数据质量与已知问题

- **完整性**：覆盖 11 国与五类文化面向，但类别可能不均衡。
- **一致性**：开放式问答格式多样，评估标准需一致定义。
- **稳定性**：依赖 Hugging Face 平台稳定性。

## 备注

Hugging Face 可直接下载（文件大小未标注）；作为跨文化开放式 VQA benchmark 很适合做偏置/安全评测，但需要先固定答案归一与评分规则，避免分数被 prompt 与评测口径强影响。

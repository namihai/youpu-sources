# 中国古代手写字符数据库（CASIA-AHCDB）

```yaml
title: 中国古代手写字符数据库（CASIA-AHCDB）
canonical_url: https://nlpr.ia.ac.cn/pal/CASIA-AHCDB.html
domain: 文化资源
content_type: 素材
data_form: 多媒体
data_type: 图像
region: 中国
source_type: 学术机构
source_org: 中国科学院自动化研究所（CASIA）
permissions: 申请可获取
tags: [古文档, 手写体, OCR, 字符识别, 版面分析]
use_cases: [研究分析, AI训练]
```

## 数据集概览

- **数据集名称**：中国古代手写字符数据库（CASIA-AHCDB）
- **覆盖内容**：面向古文档手写体字符识别研究的字符级图像样本与分类体系，包含 2,264,285 个标注字符样本、12,229 类，来源于 12,000+ 页标注文档；按来源分为两大子库：Style1（四库全书，style1）与 Style2（古佛经，style2）。
- **核心价值**：针对古文档 OCR 的“字形变化大、噪声多、类别多”问题提供关键训练与对标资源，适合做基线对比与预训练；但数据获取通常需要申请，且工程落地仍需结合目标版式与领域做适配。
- **适用场景**：古文档字符识别/检测、版面分析、去噪与超分等前处理模型训练与评测。

## 数据内容说明

1. 数据对象与边界：字符识别用的标注字符样本（bitmap）及其类别（Unicode/类）；样本来自古代手写文档页面的字符切分与标注。
2. 数据组织方式：按来源分为两大子库：
    - Style1：四库全书（Complete Library in Four Sections）
    - Style2：古佛经（Ancient Buddhist Scriptures）
    
    并按应用划分为 basic / enhanced / reserved 三类集合（reserved 因样本少不再划分训练/测试）。
    
3. 规模与粒度：总计 12,229 类、2,264,285 个字符样本（以官网统计表为准）。
4. 训练/测试划分（官网说明）：
    - Style1：25 本书（book_01–book_25），book_01–20 为训练集，book_21–25 为测试集（部分书由同一书写者书写）。
    - Style2：10 个时期的佛经卷，period_09–10 为训练集，period_01–08 为测试集。
5. 数据格式：官网给出 GNTX 格式字段说明（sample size、Unicode、width、height、bitmap 等）。

## 数据获取方式

### 网页访问

- **链接**：[https://nlpr.ia.ac.cn/pal/CASIA-AHCDB.html](https://nlpr.ia.ac.cn/pal/CASIA-AHCDB.html)
- **说明**：官网提供数据集介绍、统计表、数据格式说明与分子集下载入口。

### 文件下载

- **下载入口（官网）**：页面 Data Download 区提供 style1/style2 的分子集下载（如 style1_basic_train_part1/2/3、style1_basic_test、style1_enhanced、style2 等）。
- **说明**：页面同时提供 CASIA-10k（5.2G）下载入口（以官网为准）。

### 人工对接（如适用）

- **联系邮箱**：[liucl@nlpr.ia.ac.cn](mailto:liucl@nlpr.ia.ac.cn)
- **电话**：(+86-10) 8254-4797

## 使用限制与合规说明

- **版权归属**：不明/待确认
- **使用许可**：不明/待确认（官网页面未给出明确开源许可条款时，以官方说明/下载协议为准）。
- **禁止事项**：不明/待确认
- **合规依据**：官网页面说明与下载协议（如有）。
- **敏感性**：一般不涉及个人信息，但可能涉及文献影像版权与使用范围。

## 数据质量与已知问题

- **完整性**：类别多但长尾类别可能样本稀少。
- **一致性**：不同子集扫描质量与噪声类型差异大，训练需分层抽样与增强。
- **时效性**：不明/待确认
- **稳定性**：依赖申请渠道与维护方支持，稳定性存疑。

## 备注

该数据集的独特性在于提供“大规模古文档手写字符 + 明确的 style/子集划分 + 训练/测试拆分规则”，适合做古文档 OCR 的对标与预训练；但许可条款需以官网/下载协议为准。

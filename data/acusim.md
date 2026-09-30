---
title: "AcuSim 头颈部针灸穴位定位合成数据集（AcuSim）"
summary: "面向头颈部针灸穴位定位的合成数据集，含 63,936 张多视角 RGB-D 图像与 504 个合成解剖模型，标注 174 个体积穴位。"
canonical_url: "https://datadryad.org/dataset/doi:10.5061/dryad.zs7h44jkz"
publisher: "Qilei Sun 等（西交利物浦大学、苏州市中医医院）"
modality: "multimodal"
access_level: "open"
---

# AcuSim 头颈部针灸穴位定位合成数据集（AcuSim）

## 亮点

- 面向头颈部针灸穴位定位的合成数据集，含 63,936 张多视角 RGB-D 图像与 504 个合成解剖模型，标注 174 个体积穴位。
- 数据大小：约 13.04 GB。
- 许可协议：CC0（Public Domain）。
- 图像提供 64×64 至 1024×1024 多分辨率，配套 2D/3D 关键点坐标、可见性权重、经络类别与可见性掩码等结构化标注。
- URL：https://datadryad.org/dataset/doi:10.5061/dryad.zs7h44jkz

## 数据内容

AcuSim 是 Qilei Sun 等（西交利物浦大学、苏州市中医医院）于 2025 年发布在 Dryad 的合成数据集，用于从头颈区域图像定位针灸穴位。穴位位置因个体身高、体重与脂肪比例差异而不同，且人工标注依赖专家、成本高，作者采用自动渲染与标注流水线生成 63,936 张多视角 RGB-D 图像与 504 个合成解剖模型，标注 174 个体积穴位，以覆盖人体解剖的多样性与可变性。

图像提供 64×64、128×128、256×256、512×512 与 1024×1024 多种分辨率；配套 JSON 标注含 2D/3D 关键点坐标、可见性权重（0.9–1.0）、经络类别索引与可见性掩码，并对被遮挡穴位保留经络类别、赋予默认坐标与加权可见性评分。数据采用 Blender 3.5 多视角渲染并模拟遮挡，附 174 个标准穴位的 map.txt 清单、PyTorch 数据加载示例及遮挡检测脚本。

## 获取与许可

数据以 CC0（Public Domain）发布，可从 Dryad 直接下载，主文件 acuSim.zip 约 13.04 GB，另附 README.md。配套论文发表于 Scientific Data（DOI 10.1038/s41597-025-04934-9），渲染与可视化代码见 GitHub 仓库 ZoeApokalypse/acuSim。

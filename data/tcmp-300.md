---
title: "中药植物多部位识别图像数据集（TCMP-300）"
summary: "包含300个中药植物类别、52,089张图像，同时覆盖花、叶、茎、果实、根和全株等不同形态。"
canonical_url: "https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2025.1672394/full"
publisher: "Yanling Zhang、Wanhui Sun、Chuanguang Yang 等"
modality: "image"
access_level: "open"
---

# 中药植物多部位识别图像数据集（TCMP-300）

## 亮点

- 包含300个中药植物类别、52,089张图像，同时覆盖花、叶、茎、果实、根和全株等不同形态。
- 按植物类别组织图像，附拉丁学名、中文名、科名及训练与验证数量表，保留类别间样本量差异。
- 图像来自Bing搜索，经CLIP辅助筛查与人工核验；提供配套采集、清洗及分类训练代码。
- 数据大小：Figshare第2版下载总量标注约11.94 GB。
- 许可标注：Figshare第2版为CC BY 4.0；Hugging Face托管页另标CC BY-NC-SA 4.0。
- URL：https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2025.1672394/full

## 一个植物类别中的多种外观

TCMP-300由Yanling Zhang、Wanhui Sun、Chuanguang Yang等研究者构建，参与机构包括信阳农林学院和中国科学院计算技术研究所，原始数据论文发表于2025年7月。图像以药用植物类别归组，覆盖花、叶、茎、果实、根和全株；识别对象跨越局部器官与整株外观，300类并非按六种部位进一步展开后的标签总数。

这种组织保留了同一植物在不同观察部位下的外观差异。花部颜色、叶形与根部形态提供的视觉线索不同，某张图没有展现某个器官，不代表该类别缺少这一植物结构。发布的类别信息表按植物名称及分类信息建立索引，未把“每类均有六种部位的均衡样本”作为数据组织前提。

材料通过Bing搜索采集，先用预训练视觉模型CLIP辅助发现不相关图像，再进行人工核验。配套代码同时支持文本检索图像和参考图检索图像两种清洗方式。它记录的是网络图片条件下的类别外观，图像数量不能视为独立采集植株数或实地调查样本量。

## 类别信息表保留了什么

`tcmp-info-20250329.csv`为类别级信息表，包含 `No`、`Latin Name`、`Family`、`Chinese Name`、`Train Num`、`Val Num`、`Total Num`。同一行连接类别编号、名称和两种数据划分的数量，不是逐张图像的拍摄或器官标注表。

| 类别示例 | 拉丁学名 | 训练图像 | 验证图像 | 合计 |
|---|---|---:|---:|---:|
| 阿拉伯婆婆纳 | Veronica persica Poir. | 247 | 107 | 354 |
| 白及 | Bletilla striata (Thunb. ex A. Murray) Rchb. f. | 173 | 75 | 248 |
| 当归 | Angelica sinensis (Oliv.) Diels | 76 | 33 | 109 |

各类别数量并不相等，数据保留长尾分布。上表示例中，同样属于一个分类标签的阿拉伯婆婆纳和当归，图像数量相差三倍以上；类别数与总图像数因此不足以说明每一类获得了多少训练材料，类别信息表提供了这一层区分。

## 文件组织与获取

图像包名为 `tcmp-300-release.tar.gz`，解压后按“类别编号.植物学名”建立目录，例如 `001.Veronica persica Poir.`。图像包含PNG、JPG、JPEG和WebP格式，类别编号用于与CSV信息表对应。

原始数据论文关联[Figshare发布页](https://figshare.com/articles/dataset/TCMP-300/29432726)，当前列为第2版，发布于2025年6月29日；图像包和类别表也见于[Hugging Face文件目录](https://huggingface.co/datasets/anzhulin/tcmp-300/tree/main)。[项目代码仓库](https://github.com/winycg/TCMP-300)提供数据清洗、分类训练、推理及可视化工具，代码和图像数据分别发布。

## 不同托管页的许可

Figshare第2版标注CC BY 4.0，Hugging Face页面标注CC BY-NC-SA 4.0，两处声明不同。Hugging Face版本含非商业与相同方式共享条件，不能将Figshare的许可标注直接套用于另一托管版本。

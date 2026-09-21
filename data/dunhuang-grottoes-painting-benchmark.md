---
title: "敦煌石窟壁画数据集与基准（Dunhuang Grottoes Painting Dataset and Benchmark）"
summary: "由敦煌研究院、天津大学等机构作者基于莫高窟第 7 窟壁画制作，是首个公开的敦煌石窟壁画修复数据集。"
canonical_url: "https://www.kaggle.com/datasets/xuhangc/dunhuang-grottoes-painting-dataset-and-benchmark"
publisher: "Kaggle"
modality: "image"
access_level: "open"
tags: [壁画, 敦煌, 文化遗产, 文物图像, 莫高窟]
---

# 敦煌石窟壁画数据集与基准（Dunhuang Grottoes Painting Dataset and Benchmark）

## 亮点

- 由敦煌研究院、天津大学等机构作者基于莫高窟第 7 窟壁画制作，是首个公开的敦煌石窟壁画修复数据集。
- 共 600 组图像（训练 500 组、测试 100 组），每组含真实壁画、缺损掩膜和模拟缺损图像三张，共 1,800 张 JPG。
- 数据大小：约 448 MB（448,050,882 字节）。
- 许可协议：CC0: Public Domain（公有领域）。
- URL：https://www.kaggle.com/datasets/xuhangc/dunhuang-grottoes-painting-dataset-and-benchmark

## 数据内容与来源

该数据集来自莫高窟第 7 窟南北壁壁画的数字化图像。莫高窟位于甘肃敦煌，现存超过 45,000 平方米壁画和 2,000 余身彩塑，其中约半数壁画经受腐蚀与老化。第 7 窟开凿于中唐时期（公元 766–835 年），南北壁壁画内容涵盖佛像、菩萨、供养人、建筑、乐舞与装饰图案。考古学者将整幅大型壁画切分为 600 张图像，每张聚焦单一主题（佛像、建筑、装饰、人物等），分辨率约 500×800 像素、dpi 为 75，并按图像内容完整性原则选取。

数据集作为敦煌壁画修复（inpainting）基准发布，任务是从模拟缺损的壁画图像恢复出完整壁画。作者在每张真实壁画（ground truth）之外，另行生成一张缺损区域二值掩膜和一张模拟缺损图像，构成 GT、mask、masked 三元组。

## 缺损模拟与基准任务

缺损掩膜由随机游走生成：在 256×256 的空白二值图上随机选取起点，随后进行约 10,000 步随机游走，将经过的像素标记为缺损，再缩放到真实壁画尺寸并把对应 RGB 像素置为黑色，得到模拟老化缺损的图像。这是作者提供的一种模拟壁画老化的基准方法，用户也可自行生成缺损用于训练。

基准采用平均 DSSIM（1 减结构相似度）与局部均方误差（LMSE）评估修复结果。原挑战赛仅向参赛者公开测试集的缺损图像与掩膜、不公开真实壁画，参赛者提交恢复结果后由服务器与 ground truth 比对。

## 文件组织与规模

数据包顶层为“壁画挑战数据集”目录，下设 train 与 test 两个子目录。train 目录含 train_GT、train_mask、train_masked 三个子目录，各 500 张，编号 001–500；test 目录含 test_GT、test_mask、test_masked 三个子目录，各 100 张，编号 501–600。文件均为 JPG 格式，如 train_GT/001.jpg、train_mask/001_mask.jpg、train_masked/001_masked.jpg。总计 1,800 张图像，约 448 MB（448,050,882 字节）。

## 访问与授权

数据集由 xuhangc 托管于 Kaggle，Version 1（初始版本）上传于 2024 年 11 月 7 日，许可协议为 CC0: Public Domain。数据集首次公开于 2019 年，随论文 arXiv:1907.04589 发布，作者来自敦煌研究院、天津大学、暨南大学、天津医科大学及澳大利亚 CSIRO 等机构，项目获敦煌研究院与微软亚洲研究院支持。原始挑战赛下载需注册，而该 Kaggle 托管版公开了包括测试集真实壁画在内的全部内容。

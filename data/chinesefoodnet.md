---
title: "中国菜品图像识别数据集（ChineseFoodNet）"
summary: "面向中式菜肴图像识别的大规模公开数据集，共 185,628 张图片，覆盖 208 类中式菜肴。"
canonical_url: "https://sites.google.com/view/chinesefoodnet"
publisher: "ChineseFoodNet authors"
modality: "image"
access_level: "open"
tags: [中国饮食, 菜品图像, 图像识别, 食物文化, 计算机视觉]
---

# 中国菜品图像识别数据集（ChineseFoodNet）

## 亮点

- 面向中式菜肴图像识别的大规模公开数据集，共 185,628 张图片，覆盖 208 类中式菜肴。
- 图片来自豆果网（douguo.com）用户拍摄，由美的（Midea）员工标注，总大小约 19.4 GB。
- 按训练集 145,065 张、验证集 20,253 张、测试集 20,310 张划分，测试集不含类别标签。
- 配套论文提出融合颜色、纹理与深度网络特征的 TastyNet 方法，验证集 top-1 准确率 81.43%、测试集 81.55%。
- 供学术研究免费使用；商业用途需另行申请授权。
- URL：https://sites.google.com/view/chinesefoodnet

## 数据来源与标注

ChineseFoodNet 是一个面向中式菜肴图像识别的大规模数据集，由美的集团旗下美的新兴技术有限公司（Midea Emerging Technology Co., Ltd.）构建。数据集中的图片来自美食社区豆果网（douguo.com）用户上传的菜肴照片，由美的员工依据菜品类别逐张标注，共覆盖 208 类中式菜肴。标注完成的图片连同类别信息打包发布，供图像识别研究使用。

## 数据规模与划分

数据集共收录 185,628 张图片，总大小约 19.4 GB，划分为训练集（train）145,065 张、验证集（val）20,253 张、测试集（testing）20,310 张。配套论文《ChineseFoodNet: A large-scale Image Dataset for Chinese Food Recognition》（arXiv:1705.02743，2017 年）由 Xin Chen、Yu Zhu、Hua Zhou、Liang Diao、Dongyan Wang 等作者撰写，提出融合颜色、纹理与深度网络特征的 TastyNet 方法，在验证集上取得 top-1 准确率 81.43%，在测试集上取得 81.55%。

## 文件组织

数据集以文件夹形式组织：train 与 val 文件夹下各含 208 个以编号 000 至 207 命名的子目录，每个子目录对应一类菜肴，子目录内存放该类菜肴的图片；testing 文件夹存放测试图片但不含类别标签。此外，随数据包提供 class_names.csv（内含 208 类菜肴的中英文类名对照）、train_list.txt、val_list.txt 等列表文件，以及 README 与 COPYRIGHT 说明文件。

## 访问与使用条件

数据集通过项目官网提供下载（下载链接 https://goo.gl/kWNV8a），供学术研究免费使用；商业用途需联系美的方另行申请授权（联系邮箱 mideaetc@midea.com）。版权方面，图片版权归属豆果网用户而非美的公司，除合理使用（fair use）外，其他使用需与图片所有者另行协商。站点所列下载与使用条款将数据限定于非商业研究与教育目的，并要求使用者按站点给出的方式引用。

---
title: "甲骨文解码模型（OBSD）"
summary: "探索了用于解码甲骨文并将其翻译成现代汉字的扩散模型。"
canonical_url: "https://github.com/guanhaisu/OBSD"
publisher: "GitHub"
modality: "text"
access_level: "open"
tags: [古文字, 深度学习]
---

# 甲骨文解码模型（OBSD）
## 要点
- 探索了用于解码甲骨文并将其翻译成现代汉字的扩散模型。
- 仓库中包含论文中的官方实现、数据集和训练脚本。
- 数据大小：15.8MB
- URL：https://github.com/guanhaisu/OBSD
## 数据结构
```
Your_dataroot/
├── train/
│   ├── input/
│   │   ├── train_安_1.png
│   │   ├── train_安_2.png
│   │   ├── train_北_1.png
│   │   └── train_北_2.png
│   └── target/
│       ├── train_安_1.png
│       ├── train_安_2.png
│       ├── train_北_1.png
│       └── train_北_2.png
└── test/
    ├── input/
    │   ├── test_1.png
    │   └── test_2.png
    └── target/
        ├── test_1.png
        └── test_2.png
```
其中：
- `train/input`：训练用甲骨文字形图片；
- `train/target`：对应的现代汉字图片；
- `test/input`：测试输入图片；
- `test/target`：测试目标图片；
- 输入与目标图片通过相同文件名建立对应关系；
- README 示例采用 PNG 格式。
整体属于典型的成对图像转换数据结构。
## 配置与使用
数据路径通过`configs.yaml`配置，README.md列出的主要字段包括：
```
data:
  train_data_dir: "/Your_dataroot/train/"
  test_data_dir: "/Your_dataroot/test/"
  test_save_dir: "Your_project_path/OBS_Diffusion/result"
  val_save_dir: "Your_project_path/OBS_Diffusion/validation/"
  tensorboard: "Your_project_path/OBS_Diffusion/logs"

training:
  resume: "/Your_save_root/diffusion_model"
```
## 快速开始
```
git clone https://github.com/guanhaisu/OBSD.git
cd OBS_Diffusion

conda create -n OBSD python=3.10
conda activate OBSD
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
pip install -r requirements.txt
```
## 引用
```
@misc{guan2025decipheringoraclebonelanguage,
  title        = {Deciphering Oracle Bone Language with Diffusion Models},
  author       = {Haisu Guan and Huanxin Yang and Xinyu Wang and Shengwei Han and Yongge Liu and Lianwen Jin and Xiang Bai and Yuliang Liu},
  year         = {2025},
  eprint       = {2406.00684},
  archivePrefix= {arXiv},
  primaryClass = {cs.CV},
  url          = {https://arxiv.org/abs/2406.00684}
}
```

---
title: "中国遗产建筑损伤图像数据集（Chinese Heritage Building Crack Protection Dataset）"
summary: "收录中国传统村落遗产建筑影像 408 张（.jpg），涵盖祠堂、木构民居、石屋、寺庙、院落等建筑类型。"
canonical_url: "https://www.kaggle.com/datasets/colabsss/chinese-heritage-building-damage-dataset"
publisher: "colabsss"
modality: "image"
access_level: "open"
tags: [遗产建筑, 建筑损伤, 图像数据, 文化遗产, Kaggle]
---

# 中国遗产建筑损伤图像数据集（Chinese Heritage Building Crack Protection Dataset）

## 亮点

- 收录中国传统村落遗产建筑影像 408 张（.jpg），涵盖祠堂、木构民居、石屋、寺庙、院落等建筑类型。
- 每张影像附村落、省份、温度、湿度、降雨、振动、应变、倾斜、建材、拍摄来源等字段，damage_category 为目标列（无/轻微/中等/严重四级损伤）。
- 采用地面相机与航拍（无人机）两种视角，覆盖木、石、砖、土等材料及屋顶、墙、柱、梁、基础等构件。
- 以 CC0（公有领域）许可发布，可自由使用。
- URL：https://www.kaggle.com/datasets/colabsss/chinese-heritage-building-damage-dataset

## 项目概述

中国遗产建筑损伤图像数据集（Kaggle 标识 colabsss/chinese-heritage-building-damage-dataset，现名 Chinese Heritage Building Crack Protection Dataset）收录了中国各地传统村落遗产建筑的影像记录，呈现历史乡土建筑的结构状态、环境作用与可见的劣化样式。传统村落中的祠堂、木构民居、石屋、寺庙与院落等建筑体现了地域营建工艺与悠久匠作传统，数据集的影像即对这些建筑在潮湿、降雨、植被生长与材料长期老化等真实环境下的物理状态进行记录。

## 收录内容与规模

数据集共含 408 张遗产建筑影像（.jpg 格式，总大小约 18 MB），由地面相机与航拍（无人机）两种视角拍摄，覆盖木、石、砖、土等多种建筑材料，以及屋顶、墙体、柱、梁、基础等不同构件。每张影像对应一条带字段的记录，字段包括 image_id（唯一标识）、village_name（村落名）、province（省份）、temperature_c（环境温度，摄氏度）、humidity_percent（相对湿度百分比）、rainfall_mm（降雨量，毫米）、vibration_level（结构振动）、strain_value（结构应变）、tilt_degree（倾斜角度）、building_material（主要建材）、capture_source（拍摄来源，地面相机或航拍）以及目标列 damage_category。

## 组织方式与检索

数据集以影像文件加表格（含上述字段列）的形式组织，damage_category 为目标列，将观测到的结构状态分为 no damage（无损伤）、minor damage（轻微损伤）、moderate damage（中等损伤）、severe damage（严重损伤）四级；温度、湿度、降雨、振动、应变、倾斜等字段来自部署在建筑周边的环境与结构监测传感器。影像可用于识别中国古建筑常见的表面裂缝、风化、生物滋生与结构变形等劣化样式。

## 访问与使用条件

数据集由 Kaggle 用户 Colabsss 发布，采用 CC0（Public Domain，公有领域）许可，可自由使用、修改与再分发。数据当前为第 2 版，Kaggle 可用性评分为 0.588。

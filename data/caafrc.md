---
title: "中国古天文基础参考星表（CAAFRC）"
summary: "全天亮星基础参考星表，以依巴谷星表（Hipparcos）为基础，汇集 HIP2、XHIP 等数据集的恒星参数，统一归算到 J2000.0 历元。"
canonical_url: "https://nadc.china-vo.org/res/r100877/"
publisher: "国家天文科学数据中心 / 何勃亮"
modality: "tabular"
access_level: "request"
---

# 中国古天文基础参考星表（CAAFRC）

## 亮点

- 全天亮星基础参考星表，以依巴谷星表（Hipparcos）为基础，汇集 HIP2、XHIP 等数据集的恒星参数，统一归算到 J2000.0 历元。
- 收录亮于 7 等的恒星共 15,537 颗，含赤经赤纬、V 星等、自行、三角视差与视向速度等参数，可用于回推不同历史时期恒星的空间位置。
- 数据大小：约 1.78 MB（2 个文件）。
- 许可协议：CC BY 4.0。
- URL：https://nadc.china-vo.org/res/r100877/

## 数据内容

中国古天文基础参考星表（Chinese Ancient Astronomical Fundamental Reference Star Catalog，简称 CAAFRC）由国家天文科学数据中心（NADC）于 2024 年 1 月 10 日发布，作者为何勃亮。星表以欧洲空间局依巴谷（Hipparcos）卫星星表为基础，汇集 HIP2、XHIP 等数据集的恒星参数，归算到 J2000.0 历元，是一份面向中国古代天文研究的基础参考星表：借助自行与视向速度等运动参数，可将恒星位置回推到不同历史时期，用于古代星表的认证与古星图绘制。

星表按亮度选取亮于 7 等的恒星，共 15,537 颗。每条记录以依巴谷编号（HIP）为标识符，给出 J2000.0 历元的赤经、赤纬与 V 星等，并附自行、三角视差和视向速度。

## 数据字段

| 字段 | 单位 | 说明 |
|---|---|---|
| HIP | — | 标识符（依巴谷编号） |
| RA | deg | 赤经（Epoch = J2000.0） |
| Dec | deg | 赤纬（Epoch = J2000.0） |
| Vmag | mag | V 星等 |
| pmRA | mas/yr | 赤经自行（RA·cos(Dec)） |
| pmDE | mas/yr | 赤纬自行 |
| Plx | mas | 三角视差 |
| RV | km/s | 视向速度 |

## 文件与获取方式

星表以 FITS 与 CSV 两种格式提供，共 2 个文件、约 1.78 MB，其中 caafrc.csv 约 902.39 kB、caafrc.fits 约 919.69 kB。数据为完全共享，无需申请，注册国家天文科学数据中心账号后即可下载。发布说明建议使用 astropy 的 SkyCoord.apply_space_motion 方法计算不同时间点的恒星位置。

星表注册 DOI 为 10.12149/100877、CSTR 为 11379.11.100877，并在虚拟天文台注册为 ivo://China-VO/data/ccafrc。数据以知识共享署名 4.0 国际许可协议（CC BY 4.0）发布。

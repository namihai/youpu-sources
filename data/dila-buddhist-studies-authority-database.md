---
title: "佛学规范资料库（Buddhist Studies Authority Database）"
summary: "由法鼓文理学院图书资讯馆数字典藏组建置，整合时间、人名、地名与佛经目录四类规范资料，用于佛教文献中人名、地名的消歧及地理空间参照。"
canonical_url: "https://authority.dila.edu.tw/"
publisher: "Dharma Drum Institute of Liberal Arts / DILA"
modality: "text"
access_level: "open"
tags: [佛学, 规范资料, 人名地名, 知识组织, 数字人文]
---

# 佛学规范资料库（Buddhist Studies Authority Database）

## 亮点

- 由法鼓文理学院图书资讯馆数字典藏组建置，整合时间、人名、地名与佛经目录四类规范资料，用于佛教文献中人名、地名的消歧及地理空间参照。
- 截至 2026 年 9 月，人名规范资料库收录 49,487 人，地名规范资料库收录 59,375 笔地名，佛经目录规范资料库收录 8,674 笔资料。
- 时间规范资料库提供中日韩三历对照与干支年月查询，可查范围自秦始皇帝元年（公元前 220 年）至今，支持并行东亚年代展示。
- 提供 XML/TEI、RDF 与 MySQL SQL 原始数据下载，并托管于 GitHub 公开仓库，另提供返回 JSON 的 Web API。
- 许可协议：Creative Commons 署名-相同方式共享（CC BY-SA），时间库页面标注 2.5 台湾版，GitHub 仓库标注 3.0 国际版。
- URL：https://authority.dila.edu.tw/

## 项目与四个子库

佛学规范资料库（Buddhist Studies Authority Database Project）由法鼓文理学院图书资讯馆数字典藏组建置，旨在整合该组各已完成与进行中数位佛学专案的人物与地点资料，并建立历史对照年表，以便日后资源分享与跨专案搜寻。计划主持人为释惠敏，共同主持人为杜正民、马德伟（Marcus Bingenheimer）与洪振洲，编辑为张伯雍、葛贤敏，程式由李志贤负责；网站版权标注 DILA, 2008，赞助单位为浩然基金会。

资料库由时间、人名、地名与佛经目录四个子库构成。时间规范资料库（Time Authority Database）提供中国、日本、韩国的中西历时间对照、日期规范码与干支年月查询，特色是并行展示东亚各国年代，可查询范围为：中国自秦始皇帝元年（公元前 220 年 11 月 14 日）至今，韩国自公元前 56 年至 1910 年，日本自 593 年至今。人名规范资料库（Person Authority Database，Beta 版）收录佛典相关人名，截至 2026 年 9 月 20 日共 49,487 人、110 个人名群组，提供别名数量、卒年分布与被参考次数等统计。地名规范资料库（Place Authority Database，Beta 版）收录佛典相关地名，共 59,375 笔、95 个地名群组，附经纬度并支持 KML 输出，其中中国历史行政地名资料来源于中央研究院"中华文明之时空基础架构系统"第一版（2002）。佛经目录规范资料库（Authority Database of Buddhist Tripitaka Catalogues）收录佛教经典目录，目前共 8,674 笔，并按作译者、完成地点与完成年代提供统计。

## 数据组织与文件格式

人名与地名资料库的原始数据以 XML/TEI 格式发布，另有 RDF 序列化版本；时间资料库提供 MySQL 5.x 导出的 SQL 转储，并附数据库结构与内容说明。下载区按子库分版提供压缩包：人名资料库为 authority_person.2026-09.zip（8.42 MB，2026 年 9 月版）与 authority_person_rdf.2020-12.rdf（58.57 MB）；地名资料库为 authority_place.2026-09.zip（3.94 MB）与 authority_place_rdf.2020-12.rdf（38.34 MB）。时间资料库自 2012 年 2 月起发布 authority_time.2012-02.zip（1.34 MB，含中日韩三历完整数据），并分列仅中文（667.64 KB，覆盖公元前 220 年至 1912 年）、仅日文（293.24 KB，覆盖 593 至 1872 年）与仅韩文（603.35 KB，覆盖公元前 56 年至 1885 年）三个子集。

地名资料库的 GitHub 仓库说明还区分了数据来源：发布档案包含约 19,000 条由 DILA 自行建立的条目，另有约 38,000 条来自中央研究院地理资讯科学中心，完整资料可透过线上界面与 API 访问。

## 检索与 API

各子库均提供线上检索界面。人名与地名资料库可浏览被参考次数排名、最近新增与最近修改条目及最多别名等排行；佛经目录资料库首页汇总作品数量最多的作译者、作品最多的地点，以及按朝代划分的作品完成年代统计。检索结果通过规范码（如人名 aid、地名 code 与地点 PL 编号）链接至条目详情，并附 CBETA 大正藏、卍续藏、嘉兴藏、中国佛寺史志汇刊等文献的出处引用。

除网页检索外，资料库提供 Web Data-Provider Service：第三方应用可经 HTTP 请求 getAuthorityData.php，按 authority id 查询人名、地名与日期实体并取得 JSON 回应；另有弹出注解服务（Pop-up Annotation Service）可供网页嵌入，Get-ID 服务处于规划阶段。该服务对每日调用次数不设限制。

## 授权与获取

资料可在线检索与浏览，原始数据可从下载区及 GitHub 公开仓库（DILA-edu/Authority-Databases）免费获取。时间资料库页面将数据标注为 Creative Commons 署名-相同方式共享 2.5 台湾版（CC BY-SA 2.5 TW），GitHub 仓库 README 则将整体资料标注为 Creative Commons 署名-相同方式共享 3.0 国际版（CC BY-SA 3.0）。资料库公布的联系邮箱为 authority@dila.edu.tw。

---
title: "中国图像志主题词表（CIT）"
summary: "支持中英文双语检索。"
canonical_url: "https://github.com/iconclass/cit"
publisher: "**V&A（DCMS** 资助项目；CIT Editorial Team）/ GitHub iconclass/cit"
modality: "tabular"
access_level: "open"
tags: [机器学习]
---

# 中国图像志主题词表（CIT）
## 要点
- 支持中英文双语检索。
- 主题词规模17465条。
- 目录规模12893条。
- 可转换为SQLite全文检索数据库。
- 可导出为SKOS JSON-LD，适合知识图谱和关联数据应用。
- 提供Docker镜像与本地运行方法。
- 数据大小：6.7MB
- 许可协议：CC0 1.0
- URL：https://github.com/iconclass/cit
## 数据内容
数据中主题词覆盖：
- 自然；
- 人类；
- 社会与文化；
- 宗教；
- 神话与传说；
- 历史与地理；
- 文学作品；
- 植物、动物、人物、器物、事件；
- 历史、宗教、神话和文学中的人名与地名；
- 图案、母题、题材和主题。

主题词记录包含：
```
SEQ           顺序号
TYPE          记录类型
ID            CIT稳定标识
TERM_ZH       中文主词
TERM_EN       英文主词
TERM_PINYIN   拼音
KW_ZH         中文同义词、异体或检索词
KW_EN         英文同义词、检索词
BROADER       直接上位词
C             子节点
R             关联词
P             完整上位路径
```
例如一个概念可以同时具有繁体主词、简体异体、英文译名、拼音、上位词和相关概念。这已经具备规范主题词表和轻量本体的基本结构。

藏品与图像目录中，记录主要包含：
```
ID              内部记录ID
COL             收藏机构代码
TYPE            记录类型，当前主要为image
LOCATION.INV    收藏机构名称
DESCRIPTION     对象类型或描述
TITLE           藏品标题
URL.IMAGE       图像文件名
URL.WEBPAGE     原始收藏机构页面
CIT             关联的CIT主题词ID
DATE            制作年代
PERSON.ARTIST   作者或制作者
PERSON.ROLE     人物角色
INSTIT.INV      机构藏品号
ID.INV.ALT      其他编号
ID.INV.INST     编号类型
```
一件藏品可以关联多个 CIT 主题词。例如一方砚台可以同时关联器物类型、材质、动物纹样、历史时期和神话母题。

## 数据结构
CIT 使用一种名为 `.dmp` 的纯文本记录格式。每条记录由若干“字段名—字段值”组成，多值字段用分号续行，记录之间使用 `$` 分隔。
示意机构：
```
SEQ 4
TYPE CIT
ID CIT0284391
KW_ZH 气
TERM_PINYIN qi
TERM_EN qi
KW_EN effluvium
; breath
; vital breath
BROADER CIT290300
TERM_ZH 氣
$
```
## 数据处理链路
```
V&A馆藏管理系统
        ↓
主题词与目录XML导出
        ↓
转换脚本
        ↓
CIT.dmp + CATALOG.dmp
        ↓
SQLite检索库 / SKOS JSON-LD
        ↓
FastAPI网站与中英文检索界面
```
具体包括：
- `convert_thesaurus.py`：把主题词 XML 转换为 `CIT.dmp`；
- `convert_catalog.py`：把收藏机构目录 XML 转换为 `CATALOG.dmp`；
- `convert_todb.py`：把两个 DMP 文件转换为 `CIT.sqlite`；
- `SQLite` 使用 `FTS5` 建立全文检索索引；
- 数据库建立 `terms` 和 `images` 两个视图；
- `objs_cit` 表保存藏品与主题词之间的关联；

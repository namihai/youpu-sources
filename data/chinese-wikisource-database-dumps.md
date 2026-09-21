---
title: "中文维基文库数据库转储（zhwikisource）"
summary: "维基媒体基金会托管的「中文维基文库」数据库完整快照，以 XML 与 SQL 两种形式提供，按月生成、免费下载。"
canonical_url: "https://dumps.wikimedia.org/zhwikisource/latest/"
publisher: "Wikimedia Foundation"
modality: "text"
access_level: "open"
tags: [维基文库, 中文文本, 数据转储, 开放知识, 古典文献]
---

# 中文维基文库数据库转储（zhwikisource）

## 亮点

- 维基媒体基金会托管的「中文维基文库」数据库完整快照，以 XML 与 SQL 两种形式提供，按月生成、免费下载。
- 含正文当前版本、含元数据当前版本、完整修订历史、页面摘要与标题列表，以及 page、pagelinks、categorylinks 等原始数据表。
- 覆盖典籍、史书、小说、诗歌、法律条文、政府公报、判例、宪法、条约等海量中文文献，正文原创内容以 GFDL 与 CC BY-SA 4.0 双重授权。
- 该 latest 目录属已弃用的旧版 XML 转储（中文维基文库最近一次生成于 2022 年 7 月），官方现推荐改用 MediaWiki Content File Exports。
- URL：https://dumps.wikimedia.org/zhwikisource/latest/

## 项目概述

中文维基文库（Chinese Wikisource）是维基媒体基金会运营的免费中文文献数字图书馆，收录典籍、史书、小说、诗歌、散文、演讲、歌词、宗教经书等各类作品，并汇集中华人民共和国与中华民国的法律、政府公报、宪法、条约、判例及联合国文件等文献，代表性文集包括红楼梦、三国演义、西游记、诗经、史记、资治通鉴、全唐诗、道德经等。数据库转储（database dump）则是该维基站点的数据库完整快照，由维基媒体基金会以可下载文件形式公开，供研究、镜像、离线阅读与再分发使用。

## 转储内容与格式

该目录提供的核心文件包括：正文条目当前版本 pages-articles.xml.bz2、含元数据的当前全部页面 pages-meta-current.xml.bz2、完整修订历史 pages-meta-history.xml.bz2、页面摘要 abstract.xml.gz（含简体、繁体变体）、全部页面标题 all-titles 文件，以及 page、pagelinks、categorylinks、redirect 等原始数据库表（SQL 格式）与更小的 stub 子集文件，并附 md5sums.txt、sha1sums.txt 校验文件。以 2022 年最近一次转储计，正文条目约 2 GB、含完整历史版本约 5 GB。这些快照由维基媒体基金会按月生成。

## 获取与使用条件

转储免费公开下载；维基媒体对下载实施用户代理政策、速率限制与每 IP 三连接上限，并建议定期用户订阅 xmldatadumps-l 邮件列表。内容许可方面，除特别说明外，转储中的原创文本内容以 GNU 自由文档许可证（GFDL）与 Creative Commons 署名—相同方式共享 4.0（CC BY-SA 4.0）双重授权，部分文本仅适用 CC 许可；维基文库所收录的古籍原文本身多属公有领域，站点的编辑性贡献（格式、校注、标注等）适用上述许可，具体以站内各条目说明与 dumps.wikimedia.org/legal.html 为准。

## 状态与替代入口

维基媒体官方已将旧版 XML 数据库转储标记为「已弃用」，推荐改用 MediaWiki Content File Exports（提供 Content History 与 Content Current 两类数据集，采用与 Special:Export 兼容的压缩 XML）。就中文维基文库而言，本 latest 目录的旧式转储最近一次生成停留在 2022 年 7 月（20220720），如需最新数据宜改从新入口获取；本卡片所记录的原始 URL 仍指向旧系统的 latest 目录。

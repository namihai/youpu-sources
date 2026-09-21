---
title: "敦煌早期禅宗文献 XML 数据集（Four Early Chan Texts from Dunhuang）"
summary: "四部敦煌早期禅宗文献的全部现存写本的 TEI/XML 电子版，共 48 个敦煌写本证本（witness）。"
canonical_url: "https://zenodo.org/records/1133490"
publisher: "Zenodo"
modality: "text"
access_level: "open"
tags: [古文档, 敦煌, 语料库]
---

# 敦煌早期禅宗文献 XML 数据集（Four Early Chan Texts from Dunhuang）

## 亮点

- 四部敦煌早期禅宗文献的全部现存写本的 TEI/XML 电子版，共 48 个敦煌写本证本（witness）。
- 覆盖楞伽师资记、传法宝纪、修心要论、观心论四部文献，另附南宗定是非论一部的标记文本。
- 含 XML 正文、XSLT 样式表、RelaxNG 校验模式，以及 6295 张异体字（生僻字）图像的外字集。
- 由中华佛学研究所（Chung-hwa Institute of Buddhist Studies）组织资助，2014–2017 年完成标记。
- 许可协议：Zenodo 记录标注 CC BY 4.0；压缩包内 README 声明 CC BY-SA 4.0。
- URL：https://zenodo.org/records/1133490

## 数据内容与来源

该数据集是纸质出版物《Four Early Chan Texts from Dunhuang – A TEI-based Edition》（早期禅宗文献四部——以 TEI 标记重订敦煌写卷）配套的电子数据。该项目由中华佛学研究所组织资助，2014–2017 年间，编者将四部早期禅宗文献的全部 48 个现存敦煌写本证本转录为 XML/TEI 格式，以探索中国敦煌文献高端数字编校的最佳实践。

四部文献为：楞伽师资记（Lengqie shizi ji）、传法宝纪（Chuan fabao ji）、修心要论（Xiuxin yao lun）、观心论（Guanxin lun）。此外，压缩包还收录了南宗定是非论（Nanzong ding shifei lun）的标记文本，该书未纳入纸质版。写本证本来自多个收藏机构，文件名前缀分别对应：P（伯希和收藏，法国国家图书馆）、S（斯坦因收藏，英国国家图书馆）、Dh（圣彼得堡收藏）、BD（北京国家图书馆）、Ryukoku（日本龙谷大学图书馆）等。

## 文件组织

压缩包 4earlyChanTextsFromDunhuang-aTEIbasedEdition_2017.zip 约 29 MB（29,025,761 字节），解压后共 67 个文件，分四个目录：

- `xml_and_stylesheets/`：各文献的写本逐本转写 XML（以「文献名-收藏号」命名）、每部文献的注释（-00notes）与包装（-00wrapper）文件，以及共享的文献书目（00-bibliography.xml）、编码说明（00-encodingDesc.xml）、顶层包装（00-wrapperDunhuang.xml）和通假字表（01-phoneticLoanCharacters.txt）；另有三个 XSLT 样式表，用于生成单写本的摹写版/规范版对照视图、多写本对齐视图及书目视图。
- `schema/`：RelaxNG 紧凑语法校验模式（dunhuang-schema.rnc）及用于 ROMA 生成该模式的定制文件（dunhuang-schema.xml）。
- `gaiji/png.zip`：6295 张异体字（生僻字）PNG 图像，多数尚未字体化，供需要展示单个字符的在线界面使用。
- 根目录：`README.txt`（说明文件）与 `introduction.pdf`（项目导论，说明项目缘由、涉及文献与标记方案）。

## 相关出版与获取条件

基于该数据的纸质版分三卷，由台北新文丰出版公司于 2018 年出版：第一卷摹写版（ISBN 978-957-17-2274-0）、第二卷对照与点注版（ISBN 978-957-17-2275-7）、第三卷抄经版（ISBN 978-957-17-2276-4）。编者为 Marcus Bingenheimer 马德伟（天普大学）与张伯雍（中华佛学研究所）。

压缩包不包含写本原件的图像文件，原件图像可在国际敦煌项目（International Dunhuang Project，idp.bl.uk）在线获取。数据集在 Zenodo 上开放获取，记录许可标注为 CC BY 4.0；压缩包内 README 则声明为 CC BY-SA 4.0，两者存在差异，使用者应留意。Zenodo 记录 DOI 为 10.5281/zenodo.1133490，元数据发布日期标注为 2017-12-28。

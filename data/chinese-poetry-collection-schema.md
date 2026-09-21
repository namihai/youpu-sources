---
title: "中国诗歌总集数据集"
summary: "项目宣称累计收录约 37 万首诗、词、曲、赋及少量散文。"
canonical_url: "https://github.com/open-chinese/poetry-collection"
publisher: "open-chinese（GitHub）"
modality: "text"
access_level: "open"
tags: [古诗词, 开源, 语料库]
---

# 中国诗歌总集数据集
## 亮点
- 项目宣称累计收录约 37 万首诗、词、曲、赋及少量散文。
- 时间范围从先秦延伸至清代。
- 重点覆盖唐诗、宋诗、宋词和元曲。其中，唐诗、宋诗和宋词覆盖较多。
- 数据在2026年有部分更新。
- 数据格式：JSON
- 数据大小：129.9MB
- 许可协议：MIT
- URL：https://github.com/open-chinese/poetry-collection
## 数据内容
收录内容覆盖：
- 周：《诗经》《论语》《离骚》等
- 汉：《古诗十九首》等
- 三国：曹植诗集等
- 两晋：陶渊明等
- 唐：《全唐诗》《唐诗三百首》等
- 宋：宋诗、宋词、《宋词三百首》等
- 元：元曲
- 清：纳兰性德诗集、《红楼梦》诗歌等
## 数据结构
每首作品采用统一JSON对象，主要字段为：
```
{
  "uuid": "cc4e4cbbb0fbcdeddbcf3f5446e5341c",
  "title": "关雎",
  "author": "佚名",
  "content": "关关雎鸠，在河之洲……",
  "dynasty": "周",
  "collection_info": {
    "collection": "诗经",
    "volume": "国风",
    "section": "周南"
  }
}
```
字段含义如下：
| 字段 | 内容 |
|---|---|
| `uuid` | 用于作品去重和关联的哈希标识 |
| `title` | 作品标题 |
| `author` | 作者或归属说明 |
| `content` | 正文，使用换行符保存分行 |
| `dynasty` | 朝代 |
| `collection_info` | 作品所属总集、卷次、章节等来源信息 |

`collection_info`是一个可变的嵌套对象。不同作品可能包含：
- `collection`
- `volume`
- `section`
也可能直接为`null`。例如按诗人整理的李白数据中，相当一部分作品的`collection_info`为空。

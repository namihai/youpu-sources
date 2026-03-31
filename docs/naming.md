# 命名规范

## accepted 文件命名

`accepted/` 下的文件名统一使用以下格式：

```text
SRC-####-slug.md
```

例如：

```text
SRC-0001-muraldh.md
SRC-0002-ihchina.md
SRC-0003-figshare-dunhuang-restoration.md
```

## 规则

- 前缀固定为 `SRC`
- `####` 为四位递增编号
- `slug` 为简短英文或拼音
- 文件扩展名固定为 `.md`

## slug 要求

- 使用小写字母、数字和连字符 `-`
- 保持简短，便于人工识别
- 不要求完整表达中文标题
- 不建议包含随机 hash
- 不建议直接使用超长中文标题

## 推荐做法

当前推荐通过导入流程生成正式 accepted 文件：

1. 用户先把候选 Markdown 放进 `imports/accepted/`
2. 运行 `./youpu ingest --dry-run`
3. 修正问题后运行 `./youpu ingest`

`ingest` 会在正式合并时：

- 自动计算下一个编号
- 生成 `SRC-####-slug.md`
- 对文件名做规范化处理

## 不推荐做法

不建议使用以下命名方式：

- 中文全标题加随机字符串
- `Untitled`
- 带空格的超长文件名
- 以 URL 直接作为文件名

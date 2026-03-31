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

人工新增 accepted 记录时：

1. 找到当前最大编号
2. 顺序加一
3. 取一个短 slug
4. 从 [`templates/accepted.md`](/Users/xianqiu/Projects/youpu-sources/templates/accepted.md) 复制新文件

也可以直接使用辅助脚本生成新文件：

```bash
python3 tools/validate/new_accepted.py muraldh
```

脚本会：

- 自动计算下一个编号
- 生成 `SRC-####-slug.md`
- 从模板复制初始内容

## 不推荐做法

不建议使用以下命名方式：

- 中文全标题加随机字符串
- `Untitled`
- 带空格的超长文件名
- 以 URL 直接作为文件名

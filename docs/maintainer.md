# 维护者手册

这份文档说明如何新增或修改 `youpu-sources` 中的来源记录。

## 新增或修改来源

直接编辑 `data/` 目录中的 Markdown 文件：

```text
data/digital-dunhuang.md
```

文件名要求：

- 使用英文小写字母、数字和连字符
- 以 `.md` 结尾
- 不使用编号

字段怎么写请参考 [meta-fields.md](meta-fields.md)。

## 本地检查

写完后运行：

```bash
python3 scripts/check.py
```

检查通过后即可提交 PR。检查器的完整行为说明见 [checker.md](checker.md)。

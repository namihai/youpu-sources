# youpu-sources

`youpu-sources` 用来维护一份数据集与数字资源来源清单。

仓库只保存“来源记录”，不保存数据集文件本身，也不自动发现外部来源。

## 快速开始

新增或修改来源时，直接编辑 `data/` 目录中的 Markdown 文件：

```text
data/digital-dunhuang.md
```

文件名使用英文小写字母、数字和连字符，并以 `.md` 结尾。不要使用编号。

字段怎么写请参考 [docs/meta-fields.md](docs/meta-fields.md)。

写完后运行检查：

```bash
python3 scripts/check.py
```

检查通过后即可提交 PR。检查器的完整行为说明见 [docs/checker.md](docs/checker.md)。

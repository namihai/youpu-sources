# youpu CLI 用户文档

这份文档说明 `youpu` 命令集应该怎么用。

`youpu` 现在主要供两类场景使用：

- GitHub Actions 调用
- 维护者本地调试或排障

普通贡献者的主流程见 [README.md](../../README.md)。

如果你要修改字段定义、模板结构或 schema 校验逻辑，建议同时阅读 [schema 规范](../specs/schema.md)。

## 协作约定

- 内部协作者应使用主仓库分支提交 PR，这类 PR 支持维护者通过 `/ingest` 自动回写
- 外部 fork PR 只作为输入检查入口，不支持自动回写 ingest 结果
- 如果外部贡献需要正式入库，维护者应在内部分支接管对应 `staging/` 内容

## 命令列表

当前主命令如下：

```bash
youpu validate-repo
youpu validate-imports
youpu validate-schema
youpu check-pr
youpu check-merge
youpu ingest
youpu report
```

## 你通常怎么用

### 检查 schema 和模板

```bash
youpu validate-schema
```

用于检查：

- `schemas/accepted.json`
- `schemas/rejected.json`
- `templates/accepted.md`
- `templates/rejected.rows.csv`

这个命令适合在修改字段定义、模板结构或 CLI schema 逻辑后单独运行。

### 维护 PR

如果你要在本地复现 PR 检查，运行：

```bash
youpu check-pr
```

这个命令会同时：

- 检查 schema 与模板
- 检查正式区
- 检查 `staging/`
- 如果 `staging/` 中没有任何候选内容，会以 `staging_empty` 失败

### 准备合并

如果你要确认当前分支是否已经达到可合并状态，运行：

```bash
youpu check-merge
```

这个命令要求：

- 正式区合法
- `staging/accepted/` 没有待处理 Markdown
- `staging/rejected/rows.csv` 不存在
- 当前分支没有遗留导入问题

### 执行正式入库

如果你要执行确定性的导入，运行：

```bash
youpu ingest
```

这个命令会：

- 读取 `staging/`
- 校验候选内容
- 对允许自动修正的部分做确定性处理
- 写入 `data/accepted/` / `data/rejected.csv`
- 删除已处理的输入文件

如果候选内容存在问题，命令会直接失败，不会做部分写入。
如果 `staging/` 为空，命令也会失败，因为没有任何可导入内容。

## 单独检查命令

### 检查正式区

```bash
youpu validate-repo
```

用于检查：

- `data/accepted/`
- `data/rejected.csv`
- 正式区重复
- accepted / rejected 冲突

### 检查导入区

```bash
youpu validate-imports
```

用于检查：

- `staging/accepted/*.md`
- `staging/rejected/rows.csv`
- 与正式区的冲突
- `staging/` 内部重复

这个命令是只读的，不会执行 ingest，也不会默认把报告写入版本控制。

## 输出格式

所有命令都支持：

```bash
youpu --format text <command>
youpu --format json <command>
```

例如：

```bash
youpu --format json check-pr
youpu --format json check-merge
```

JSON 输出适合 CI、脚本或后续生成 PR 注释。

## 退出码

```text
0  成功
1  规则检查失败
2  参数错误
3  运行时异常
```

## 相关文档

- 文档总入口：[../index.md](../index.md)
- 项目边界：[../overview/project-scope.md](../overview/project-scope.md)
- CLI 边界：[scope.md](scope.md)
- CLI 开发接口：[spec.md](spec.md)

# Schema 规范

这份文档说明本仓库中 schema、template 和 CLI 校验之间的关系，以及在字段变更时应该如何修改。

## 目标

schema 的作用不是给普通贡献者直接填写内容，而是作为仓库结构规则的单一真源。

它负责定义：

- accepted 的字段集合、顺序、类型和必填约束
- template 应该展示哪些字段
- CLI 校验与 ingest 写回应遵循什么结构

## 文件位置

schema 配置位于：

- `schemas/accepted.json`

对应的人工模板位于：

- `templates/accepted.md`

## 真源关系

仓库采用以下关系：

- `schemas/accepted.json` 是结构真源
- `templates/accepted.md` 是面向人的展示模板
- CLI 从 schema 读取规则
- `validate-schema` 负责检查 schema 与 template 是否一致

也就是说：

- 不应把 template 当成 schema 真源
- 修改字段时，应优先改 schema
- template 需要随后同步，但不是规则来源

## 修改顺序

如果你要新增、删除或调整 accepted 字段，推荐按下面顺序修改：

1. 修改 `schemas/accepted.json`
2. 同步修改 `templates/accepted.md`
3. 同步更新相关规范文档
4. 运行 `uv run python ./scripts/youpu validate-schema`
5. 再运行相关数据检查命令

不建议的做法：

- 先改 template，再让 CLI 猜测字段变化
- 只改 template，不改 schema
- 只改 CLI 代码里的局部判断，不改 schema

## `validate-schema` 的职责

`uv run python ./scripts/youpu validate-schema` 主要检查：

- schema 文件存在且结构合法
- `templates/accepted.md` 中 YAML 字段顺序与 accepted schema 一致

它不负责：

- 校验正式 `data/` 内容
- 校验 `staging/` 候选内容
- 自动生成 template

## 与 accepted 规范的关系

- accepted 的具体字段语义见 [`accepted.md`](accepted.md)

accepted 规范回答“字段是什么意思”，而本文件回答“这些结构规则从哪里来，以及应该如何维护”。

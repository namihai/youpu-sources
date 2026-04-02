# youpu CLI 接口说明

这份文档定义 `youpu` 的命令接口、返回码和行为边界。

这里的 `youpu` 表示逻辑接口名。当前仓库内实际执行入口是 `./scripts/youpu`，例如：

```bash
./scripts/youpu check-pr
```

## 目标

`youpu` 是 `youpu-sources` 的规则接口，用于：

- 校验正式区
- 校验导入区
- 表达 PR 与合并前检查
- 执行确定性 ingest
- 输出结构化结果

## 不负责什么

`youpu` 不负责：

- Git 提交或推送
- 外部来源发现
- 自动补全事实字段
- 接受或拒绝结论的主观判断
- PR 权限控制

这些职责应分别由 GitHub、维护者和仓库外围流程承担。

## 命令入口

逻辑入口：

```bash
youpu <command> [options]
```

当前命令：

- `youpu validate-repo`
- `youpu validate-imports`
- `youpu validate-schema`
- `youpu check-pr`
- `youpu check-merge`
- `youpu ingest`
- `youpu report`

## 全局参数

所有命令共享：

```bash
--format text|json
--root <path>
```

## 退出码

```text
0  成功
1  规则检查失败
2  参数错误
3  运行时异常
```

## 设计约束

- 检查命令与写入命令分离
- 退出码稳定
- JSON 输出适合机器消费
- 不为了方便而引入高风险自动修正

CLI 识别的导入区边界为：

- `staging/accepted/*.md`：accepted 候选输入
- `staging/rejected/rows.csv`：rejected 候选输入

## 命令规格

### `validate-schema`

用途：

- 校验 schema 配置与模板的一致性

检查范围：

- `schemas/accepted.json`
- `schemas/rejected.json`
- `templates/accepted.md`
- `templates/rejected.rows.csv`

约束：

- 只读
- 不检查正式数据和 staging 数据本身

### `validate-repo`

用途：

- 校验正式区状态

检查范围：

- `data/accepted/`
- `data/rejected.csv`
- 正式区重复
- accepted / rejected 冲突

补充：

- 缺失 `data/rejected.csv` 时，按“正式 rejected 为空表”处理，不单独报错

约束：

- 只读
- 不检查 `staging/`

### `validate-imports`

用途：

- 校验 `staging/` 中候选内容

检查范围：

- `staging/accepted/*.md`
- `staging/rejected/rows.csv`
- 与正式区的冲突
- `staging/` 内部重复

约束：

- 只读
- 不执行 ingest

### `check-pr`

用途：

- 作为 PR 检查的统一入口

行为：

- 调用 `validate-schema`
- 调用 `validate-repo`
- 调用 `validate-imports`
- 允许 `staging/` 中存在待处理文件
- 如果 `staging/` 中没有任何候选内容，返回 `staging_empty`

### `check-merge`

用途：

- 作为合并前检查的统一入口

行为：

- 调用 `validate-schema`
- 调用 `validate-repo`
- 要求 `staging/accepted/` 没有待处理 Markdown
- 要求 `staging/rejected/rows.csv` 不存在
- 要求当前分支没有遗留导入问题

### `ingest`

用途：

- 执行确定性的正式入库

行为：

- 读取 `staging/`
- 校验候选内容
- 进行确定性修正
- 写入 `data/accepted/` / `data/rejected.csv`
- 删除已处理输入
- 如果正式 `data/rejected.csv` 不存在且本次有合法 rejected 候选，会自动创建该文件

输入约束：

- `staging/accepted/*.md` 作为 accepted 候选输入
- `staging/rejected/rows.csv` 作为 rejected 候选输入

约束：

- 如果存在诊断问题，命令失败且不做部分写入
- 如果 `staging/` 中没有任何候选内容，命令失败并返回 `staging_empty`
- 不负责 git 提交

### `report`

用途：

- 输出仓库摘要

约束：

- 不承担 gate 语义

## 输出结构

所有命令都应输出：

- `ok`
- `command`
- `summary`
- `diagnostics`
- `data`

`diagnostics` 中的项包含：

- `level`
- `message`
- `path`
- `code`
- `details`

`data` 的具体字段按命令不同而不同，但当前命名约定应与仓库结构保持一致：

- staging 相关字段使用 `staging_*`
- 不再新增 `imports_*` 风格字段

## 自动修正边界

accepted / rejected 的结构定义应集中放在 `schemas/*.json` 中，由 CLI 的校验与序列化逻辑共享；新增或删除字段时，应优先修改 schema 定义，而不是在多个命令中分别维护字段列表。模板目前保持手写，但必须通过 `validate-schema` 与 schema 保持一致。schema 的维护关系与修改顺序见 [`../specs/schema.md`](../specs/schema.md)。

允许自动修正：

- URL 规范化
- accepted 编号分配
- 文件名 slug 规范化

不允许自动修正：

- 缺失事实字段补全
- accepted / rejected 分类猜测
- 主观判断型冲突处理

## 相关文档

- 维护者指南：[../guides/maintainer.md](../guides/maintainer.md)
- 项目边界：[../architecture/project-boundary.md](../architecture/project-boundary.md)
- 源码结构：[../architecture/source-layout.md](../architecture/source-layout.md)

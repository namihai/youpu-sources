# CLI 边界

这份文档定义 `youpu` CLI 负责什么、不负责什么，以及对外命令的边界。

相关的项目总边界见 [`../overview/project-scope.md`](/Users/xianqiu/Projects/youpu-sources/docs/overview/project-scope.md)。

## CLI 的职责

`youpu` CLI 是仓库内的守门工具，负责：

- 规范校验
- 导入目录检查与安全合并
- 提交前检查
- URL 诊断

CLI 不负责外部信息发现，也不负责复杂采集工作流。

## 设计原则

CLI 保持小而稳的能力集合：

- 让用户把候选内容放进导入目录
- 让 CLI 通过少量主命令负责检查、清单和安全合并
- 让 skill 只做编排和解释

## 对外命令

对外只保留以下 5 个命令：

- `youpu validate`
- `youpu ingest`
- `youpu submit`
- `youpu report`
- `youpu inspect-url`

其中：

- `validate`、`ingest`、`submit`、`report` 是主流程命令
- `inspect-url` 是辅助诊断命令

以下能力不作为对外命令暴露：

- 手工新增 `accepted` / `rejected` 的命令
- 单独暴露的重复检查命令
- 单独暴露的 URL 规范化命令
- 多工作区或多来源路径参数

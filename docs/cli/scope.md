# CLI 边界

这份文档定义 `youpu` CLI 负责什么、不负责什么，以及对外命令的边界。

## CLI 的职责

`youpu` 是仓库规则内核，负责：

- 校验正式区
- 校验导入区
- 表达 PR 检查与合并前检查
- 执行确定性 ingest
- 输出文本或 JSON 结果

## CLI 不负责什么

`youpu` 不负责：

- Git 提交或推送
- 外部来源发现
- 自动补全事实字段
- 接受或拒绝结论的主观判断
- PR 权限控制

这些职责应分别由 GitHub、维护者和仓库外围流程承担。

## 设计原则

- GitHub Actions 中的仓库规则检查应通过 `youpu` 命令表达
- 检查命令与写入命令分离
- 退出码稳定
- JSON 输出适合机器消费
- 不为了方便而引入高风险自动修正

CLI 识别的导入区边界为：

- `staging/accepted/*.md`：accepted 候选输入
- `staging/rejected/rows.csv`：rejected 候选输入

## 对外命令

对外主命令为：

- `youpu validate-repo`
- `youpu validate-imports`
- `youpu validate-schema`
- `youpu check-pr`
- `youpu check-merge`
- `youpu ingest`
- `youpu report`

其中：

- `validate-schema` / `validate-repo` / `validate-imports` 是基础检查命令
- `check-pr` / `check-merge` 是协作状态命令
- `ingest` 是唯一写入命令
- `report` 是辅助观测命令

## 相关文档

- 项目边界：[../overview/project-scope.md](../overview/project-scope.md)
- CLI 用户文档：[user-guide.md](user-guide.md)
- CLI 开发接口：[spec.md](spec.md)

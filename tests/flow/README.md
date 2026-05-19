# Flow Tests

这个文档是流程测试的主入口，面向后续维护测试的 agent 和维护者。

当前流程测试关注 3 个动作：

- `check-pr`
- `check-merge`
- `/finalize`

## 当前流程规则

- `pr-check` 运行的是 `uv run python ./scripts/youpu check-pr`
- `check-pr` 会校验正式区 `data/` 和候选区 `staging/`
- `staging/` 非空不会导致 `check-pr` 失败
- `staging/` 非空会导致 `check-merge` 失败，错误码为 `merge_pending_staging`
- `/finalize` 是唯一维护者入口
- 如果 `staging/` 为空，`/finalize` 不执行 ingest，只验证当前分支是否可合并
- 如果 `staging/` 有候选，`/finalize` 会执行 ingest，再验证当前分支是否可合并
- `data/` 和 `staging/` 根目录中的非规范文件或目录应导致检查失败
- 只要存在任何 `error`，`check-pr` 失败，`/finalize` 也不会执行部分导入

## 维护者极简原则

如果当前协作范围只考虑主仓库内部分支 PR，不考虑 fork PR，维护者可以默认：

1. 先看 PR 改动是否大致符合预期
2. 直接评论 `/finalize`
3. 根据结果决定是否合并或回到排障

在这个模型下：

- `data` PR：`/finalize` 不执行 ingest，只确认当前分支是否可合并
- `staging` PR：`/finalize` 自动执行校验、ingest 和最终 merge 检查
- 如果 PR 本身不合法，`/finalize` 会在 `check-pr` 阶段失败，不会误写正式数据

## 用例矩阵

| 编号 | 类型 | 场景 | `pr-check` | `check-merge` | ingest | ingest 后 `check-merge` |
| --- | --- | --- | --- | --- | --- | --- |
| T01 | data 基线 | `data` 空，`staging` 空 | 通过 | 通过 | 跳过 | 跳过 |
| T02 | data 基线 | `data` 非空，`staging` 空 | 通过 | 通过 | 跳过 | 跳过 |
| T03 | staging 主路径 | `data` 空，`staging` 合法 | 通过 | 失败 | 通过 | 通过 |
| T04 | staging 主路径 | `data` 非空，`staging` 合法 | 通过 | 失败 | 通过 | 通过 |
| T05 | staging 冲突 | staging accepted 与 `data/` 重复 | 失败 | 失败 | 跳过 | 跳过 |
| T06 | staging 非法输入 | staging accepted 内部 canonical_url 重复 | 失败 | 失败 | 跳过 | 跳过 |
| T07 | staging 非法输入 | staging 中有不支持的文件 | 失败 | 失败 | 跳过 | 跳过 |
| T08 | staging 非法输入 | staging accepted 文件名非法，包括中文文件名 | 失败 | 失败 | 跳过 | 跳过 |
| T09 | staging 非法输入 | staging accepted 内容结构非法 | 失败 | 失败 | 跳过 | 跳过 |
| T10 | data 非法输入 | 正式区 `data/` 非法 | 失败 | 失败 | 跳过 | 跳过 |
| T11 | data 非法输入 | 正式区存在 `data/` 之外的文件 | 失败 | 失败 | 跳过 | 跳过 |
| T12 | staging 非法输入 | staging 中存在 `staging/` 之外的目录 | 失败 | 失败 | 跳过 | 跳过 |
| T13 | 边界验证 | pending staging 时 `pr-check` 过、`check-merge` 失败 | 通过 | 失败 | 通过 | 通过 |
| T14 | 闭环验证 | ingest 成功后再次 `check-merge` | 通过 | 失败 | 通过 | 通过 |

## 本地自动化

当前本地 runner 已覆盖 `T01-T14` 全部流程用例。

目录：

- 用例目录：`tests/flow/cases/catalog.py`
- 执行入口：`tests/flow/run_flow_tests.py`
- 结果目录：`tests/flow/generated/`

输入素材：

- accepted 正向样例：直接复用 `tests/source-examples/*.md`
- accepted 异常样例：由脚本自动变异生成，包括 accepted 中文文件名
- 非规范路径样例：由脚本构造，用于确认检查会失败

命名相关规则：

- `staging/*.md` 的文件名必须是用户提供的合法英文 slug
- ingest 只负责给 accepted 正式文件名补 `SRC-####` 编号前缀
- ingest 不负责生成、翻译、改写或规范化 slug

常用命令：

```bash
uv run python tests/flow/run_flow_tests.py --list
uv run python tests/flow/run_flow_tests.py --plan
uv run python tests/flow/run_flow_tests.py --run
```

高价值子集：

```bash
uv run python tests/flow/run_flow_tests.py --plan --high-value-only
uv run python tests/flow/run_flow_tests.py --run --high-value-only
```

指定用例：

```bash
uv run python tests/flow/run_flow_tests.py --run --case T01 --case T03
```

运行后会在 `tests/flow/generated/` 下生成：

- `results.json`
- `results.md`
- 每个用例对应的临时仓库目录

## 用例构造规则

accepted：

- 正向：直接复用 `tests/source-examples/*.md`
- 冲突：把相同来源同时写入 `data/` 和 `staging/`
- 重复：在 `staging/` 中制造相同规范化 `canonical_url`
- 非法：删除必填字段、改坏 URL、改坏文件名

非规范路径：

- `data/rows.csv`：构造正式区根目录文件，期望 `data_unexpected_file`
- `staging/extra/`：构造 staging 根目录额外目录，期望 `staging_unexpected_file`

## 推荐执行顺序

1. 先跑 data 基线：T01-T02
2. 再跑 staging 主路径：T03-T04
3. 再跑高风险失败路径：T05-T12
4. 最后跑边界与闭环：T13-T14

## 高价值回归子集

如果只跑一轮高价值回归，建议至少执行：

- T01
- T02
- T03
- T04
- T05
- T06
- T07
- T12

## 下一阶段

GitHub 联调目前还未自动化，后续将单独实现：

- 建分支、push、建 PR
- 读取 `pr-check` 和 `check-merge`
- 评论 `/finalize`
- 拉取 workflow 结果
- 汇总到 issue

当前已落地 GitHub 联调的前置脚手架：

- `tests/flow/run_github_flow_tests.py`

当前支持：

- 列出 GitHub 联调用例
- 输出 GitHub 联调计划
- 检查当前 `gh` 登录状态
- 生成 issue 模板

命令：

```bash
uv run python tests/flow/run_github_flow_tests.py --list
uv run python tests/flow/run_github_flow_tests.py --plan
uv run python tests/flow/run_github_flow_tests.py --check-auth
uv run python tests/flow/run_github_flow_tests.py --issue-template
```

# Flow Tests

这个文档是流程测试的主入口，面向后续维护测试的 agent 和维护者。

当前流程测试关注 3 个动作：

- `check-pr`
- `check-merge`
- `/finalize`

## 当前流程规则

- `pr-check` 运行的是 `./scripts/youpu check-pr`
- `check-pr` 会校验正式区 `data/` 和候选区 `staging/`
- `staging/` 非空不会导致 `check-pr` 失败
- `staging/` 非空会导致 `check-merge` 失败，错误码为 `merge_pending_staging`
- `/finalize` 是唯一维护者入口
- 如果 `staging/` 为空，`/finalize` 不执行 ingest，只验证当前分支是否可合并
- 如果 `staging/` 不为空，`/finalize` 会执行 ingest，再验证当前分支是否可合并
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
| T03 | staging 主路径 | `data` 空，`staging/accepted` 合法 | 通过 | 失败 | 通过 | 通过 |
| T04 | staging 主路径 | `data` 空，`staging/rejected` 合法 | 通过 | 失败 | 通过 | 通过 |
| T05 | staging 主路径 | `data` 非空，`staging` 同时有 accepted 和 rejected | 通过 | 失败 | 通过 | 通过 |
| T06 | staging 冲突 | staging accepted 与 `data/accepted/` 重复 | 失败 | 失败 | 跳过 | 跳过 |
| T07 | staging 冲突 | staging accepted 与 `data/rejected.csv` 冲突 | 失败 | 失败 | 跳过 | 跳过 |
| T08 | staging 冲突 | staging rejected 与 `data/rejected.csv` 重复 | 失败 | 失败 | 跳过 | 跳过 |
| T09 | staging 冲突 | staging rejected 与 `data/accepted/` 冲突 | 失败 | 失败 | 跳过 | 跳过 |
| T10 | staging 非法输入 | staging accepted 内部重复 | 失败 | 失败 | 跳过 | 跳过 |
| T11 | staging 非法输入 | staging rejected 内部重复 | 失败 | 失败 | 跳过 | 跳过 |
| T12 | staging 非法输入 | staging 中有不支持的文件 | 失败 | 失败 | 跳过 | 跳过 |
| T13 | staging 非法输入 | staging accepted 文件名非法 | 失败 | 失败 | 跳过 | 跳过 |
| T14 | staging 非法输入 | staging accepted 内容结构非法 | 失败 | 失败 | 跳过 | 跳过 |
| T15 | staging 非法输入 | staging rejected 表头或行结构非法 | 失败 | 失败 | 跳过 | 跳过 |
| T16 | data 非法输入 | 正式区 `data/accepted/` 非法 | 失败 | 失败 | 跳过 | 跳过 |
| T17 | data 非法输入 | 正式区 `data/rejected.csv` 非法 | 失败 | 失败 | 跳过 | 跳过 |
| T18 | data 非法输入 | 正式区 accepted / rejected 交叉冲突 | 失败 | 失败 | 跳过 | 跳过 |
| T19 | 边界验证 | pending staging 时 `pr-check` 过、`check-merge` 失败 | 通过 | 失败 | 通过 | 通过 |
| T20 | 闭环验证 | ingest 成功后再次 `check-merge` | 通过 | 失败 | 通过 | 通过 |

## 本地自动化

当前本地 runner 已覆盖 `T01-T20` 全部流程用例。

目录：

- 用例目录：`tests/flow/cases/catalog.py`
- 执行入口：`tests/flow/run_flow_tests.py`
- 结果目录：`tests/flow/generated/`

输入素材：

- accepted 正向样例：直接复用 `tests/source-examples/*.md`
- rejected 正向样例：由脚本自动构造合法 `rows.csv`
- accepted / rejected 异常样例：由脚本自动变异生成

常用命令：

```bash
python3 tests/flow/run_flow_tests.py --list
python3 tests/flow/run_flow_tests.py --plan
python3 tests/flow/run_flow_tests.py --run
```

高价值子集：

```bash
python3 tests/flow/run_flow_tests.py --plan --high-value-only
python3 tests/flow/run_flow_tests.py --run --high-value-only
```

指定用例：

```bash
python3 tests/flow/run_flow_tests.py --run --case T01 --case T03
```

运行后会在 `tests/flow/generated/` 下生成：

- `results.json`
- `results.md`
- 每个用例对应的临时仓库目录

## 用例构造规则

accepted：

- 正向：直接复用 `tests/source-examples/*.md`
- 冲突：把相同来源同时写入 `data/accepted/` 和 `staging/accepted/`
- 重复：在 `staging/accepted/` 中制造相同规范化 `canonical_url`
- 非法：删除必填字段、改坏 URL、改坏文件名

rejected：

- 正向：脚本构造合法 `rows.csv`
- 冲突：把相同 URL 同时写到正式区和 staging
- 重复：在同一个 `rows.csv` 中制造相同规范化 URL
- 非法：改坏表头、改坏 URL、改坏字段数

## 推荐执行顺序

1. 先跑 data 基线：T01-T02
2. 再跑 staging 主路径：T03-T05
3. 再跑高风险失败路径：T06-T18
4. 最后跑边界与闭环：T19-T20

## 高价值回归子集

如果只跑一轮高价值回归，建议至少执行：

- T01
- T02
- T03
- T05
- T06
- T08
- T10
- T19

## 下一阶段

GitHub 联调目前还未自动化，后续将单独实现：

- 建分支、push、建 PR
- 读取 `pr-check` 和 `check-merge`
- 评论 `/finalize`
- 拉取 workflow 结果
- 汇总到 issue

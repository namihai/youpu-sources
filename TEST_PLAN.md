# 全面流程测试计划

本文档用于验证当前仓库在以下流程中的行为是否符合预期：

- `check-pr`
- `check-merge`
- `/finalize`

测试目标：

- 确认 `data/` 与 `staging/` 在不同组合下的校验结果
- 确认重复、冲突、非法输入等失败路径
- 确认 `pr-check`、`check-merge`、`/finalize` 三者职责边界正确

## 先确认的规则

在开始测试前，需要先明确当前实现中的几个关键规则：

- `pr-check` 运行的是 `./scripts/youpu check-pr`
- `check-pr` 会校验正式区 `data/` 和候选区 `staging/`
- `staging/` 非空不会导致 `pr-check` 失败
- `staging/` 非空会导致 `check-merge` 失败，错误码为 `merge_pending_staging`
- `/finalize` 是唯一维护者入口
- 如果 `staging/` 为空，`/finalize` 不执行 ingest，只验证当前分支是否可合并
- 如果 `staging/` 不为空，`/finalize` 会执行 ingest，再验证当前分支是否可合并
- 只要存在任何 `error`，`check-pr` 失败，`/finalize` 也不会执行部分导入

## 测试范围

本计划覆盖 4 类测试：

1. 基线场景
2. 与正式区冲突
3. `staging/` 内部冲突与非法输入
4. 完整流程联调

## 测试前置条件

建议每个测试用例都在独立分支中执行，避免相互污染。

通用前置条件：

- 从最新 `main` 拉出测试分支
- 每次只构造一个明确目标场景
- push 后观察 GitHub 上的 `pr-check`
- 涉及合并阶段时，额外验证 `check-merge`
- 涉及维护者收口阶段时，额外验证 `/finalize`

建议记录以下信息：

- 用例编号
- 分支名
- 变更文件
- 预期结果
- 实际结果
- 错误码
- 是否与预期一致

## 执行约定

为避免在执行过程中反复判断，本计划将用例分成 3 类动作：

- 自动检查：只需要 push，观察 `pr-check` 和 `check-merge`
- 维护者收口：在自动检查结果符合预期后，再触发 `/finalize`
- 可选验证：不是主路径必须动作，只在需要补充确认时执行

`/finalize` 是否需要实际触发，按下面规则处理：

- 对预期通过的 staging 用例：需要触发
- 对预期通过的 data 用例：可选触发，用于验证统一维护者入口
- 对预期失败的用例：默认不触发；如触发，预期会在 `check-pr` 阶段失败

## 测试矩阵总览

| 编号 | 类型 | 场景 | `pr-check` | `check-merge` | `/finalize` | 是否必须触发 `/finalize` |
| --- | --- | --- | --- | --- | --- | --- |
| T01 | data 基线 | `data` 空，`staging` 空 | 通过 | 通过 | 通过 | 可选 |
| T02 | data 基线 | `data` 非空，`staging` 空 | 通过 | 通过 | 通过 | 可选 |
| T03 | staging 主路径 | `data` 空，`staging` 有合法 accepted | 通过 | 失败 | 成功 | 必须 |
| T04 | staging 主路径 | `data` 空，`staging` 有合法 rejected | 通过 | 失败 | 成功 | 必须 |
| T05 | staging 主路径 | `data` 非空，`staging` 同时有合法 accepted 和 rejected | 通过 | 失败 | 成功 | 必须 |
| T06 | staging 冲突 | staging accepted 与 `data/accepted/` 重复 | 失败 | 失败 | 失败 | 否 |
| T07 | staging 冲突 | staging accepted 与 `data/rejected.csv` 冲突 | 失败 | 失败 | 失败 | 否 |
| T08 | staging 冲突 | staging rejected 与 `data/rejected.csv` 重复 | 失败 | 失败 | 失败 | 否 |
| T09 | staging 冲突 | staging rejected 与 `data/accepted/` 冲突 | 失败 | 失败 | 失败 | 否 |
| T10 | staging 非法输入 | staging accepted 内部重复 | 失败 | 失败 | 失败 | 否 |
| T11 | staging 非法输入 | staging rejected 内部重复 | 失败 | 失败 | 失败 | 否 |
| T12 | staging 非法输入 | staging 中有不支持的文件 | 失败 | 失败 | 失败 | 否 |
| T13 | staging 非法输入 | staging accepted 文件名非法 | 失败 | 失败 | 失败 | 否 |
| T14 | staging 非法输入 | staging accepted 内容结构非法 | 失败 | 失败 | 失败 | 否 |
| T15 | staging 非法输入 | staging rejected 表头或行结构非法 | 失败 | 失败 | 失败 | 否 |
| T16 | data 非法输入 | 正式区 `data/accepted/` 非法 | 失败 | 失败 | 失败 | 否 |
| T17 | data 非法输入 | 正式区 `data/rejected.csv` 非法 | 失败 | 失败 | 失败 | 否 |
| T18 | data 非法输入 | 正式区 accepted / rejected 交叉冲突 | 失败 | 失败 | 失败 | 否 |
| T19 | 边界验证 | push 后 `pr-check` 通过，但 `check-merge` 因 pending staging 失败 | 通过 | 失败 | 成功后恢复 | 必须 |
| T20 | 闭环验证 | `/finalize` 成功后再次验证 | 通过 | 通过 | 已完成 | 必须 |

## 详细测试用例

### T01 `data` 空，`staging` 空

前置条件：

- `data/accepted/` 为空
- `data/rejected.csv` 不存在或为空
- `staging/accepted/` 为空
- `staging/rejected/rows.csv` 不存在

操作步骤：

1. 提交并 push
2. 观察 `pr-check`
3. 如需验证维护者入口，执行 `/finalize`

预期结果：

- `pr-check` 通过
- `check-merge` 通过
- `/finalize` 通过，且不会执行 ingest

### T02 `data` 非空，`staging` 空

前置条件：

- `data/` 中已有至少一条合法正式记录
- `staging/` 为空

操作步骤：

1. 对 `data/` 做一次合法修改，或仅提交测试分支
2. push 并观察检查结果

预期结果：

- `pr-check` 通过
- `check-merge` 通过
- 如果执行 `/finalize`，应直接完成 merge 检查

### T03 `data` 空，`staging` 有合法 accepted

前置条件：

- `data/` 为空
- `staging/accepted/` 中放入 1 个合法 Markdown

操作步骤：

1. 提交并 push
2. 观察 `pr-check`
3. 验证 `check-merge`
4. 执行 `/finalize`
5. 再次验证 `check-merge`

预期结果：

- `pr-check` 通过
- `/finalize` 前 `check-merge` 失败，错误码 `merge_pending_staging`
- `/finalize` 成功后，正式数据写入 `data/accepted/`
- 对应 staging 文件被清空
- 之后 `check-merge` 通过

### T04 `data` 空，`staging` 有合法 rejected

前置条件：

- `data/` 为空
- `staging/rejected/rows.csv` 中放入 1 行合法 rejected

操作步骤：

1. 提交并 push
2. 观察 `pr-check`
3. 验证 `check-merge`
4. 执行 `/finalize`

预期结果：

- `pr-check` 通过
- `/finalize` 前 `check-merge` 失败，错误码 `merge_pending_staging`
- `/finalize` 成功后写入 `data/rejected.csv`
- staging 被清空
- 之后 `check-merge` 通过

### T05 `data` 非空，`staging` 同时有合法 accepted 和 rejected

前置条件：

- `data/` 中已有合法数据
- `staging/accepted/` 中有合法 accepted
- `staging/rejected/rows.csv` 中有合法 rejected
- 两者与正式区不冲突

操作步骤：

1. 提交并 push
2. 观察 `pr-check`
3. 验证 `check-merge`
4. 执行 `/finalize`

预期结果：

- `pr-check` 通过
- `/finalize` 前 `check-merge` 失败，错误码 `merge_pending_staging`
- `/finalize` 后 accepted 和 rejected 都正确进入正式区
- staging 被清空
- 之后 `check-merge` 通过

### T06 staging accepted 与 `data/accepted/` 重复

前置条件：

- `data/accepted/` 已有某个 `canonical_url`
- `staging/accepted/*.md` 使用相同的规范化 URL

操作步骤：

1. 提交并 push
2. 观察 `check-merge`

预期结果：

- `pr-check` 失败
- `check-merge` 失败
- 错误码：`staging_accepted_conflict_accepted`
- 如果触发 `/finalize`，会在 `check-pr` 阶段失败，不会进入 ingest
- 处理方式：删除重复文件或调整为新的来源后重新提交

### T07 staging accepted 与 `data/rejected.csv` 冲突

前置条件：

- `data/rejected.csv` 已有某个 URL
- `staging/accepted/*.md` 使用相同的规范化 URL

预期结果：

- `pr-check` 失败
- `check-merge` 失败
- 错误码：`staging_accepted_conflict_rejected`
- 如果触发 `/finalize`，会在 `check-pr` 阶段失败

### T08 staging rejected 与 `data/rejected.csv` 重复

前置条件：

- `data/rejected.csv` 已有某个 URL
- `staging/rejected/rows.csv` 再次写入相同规范化 URL

预期结果：

- `pr-check` 失败
- `check-merge` 失败
- 错误码：`staging_rejected_conflict_rejected`
- 如果触发 `/finalize`，会在 `check-pr` 阶段失败

### T09 staging rejected 与 `data/accepted/` 冲突

前置条件：

- `data/accepted/` 已有某个 `canonical_url`
- `staging/rejected/rows.csv` 使用相同规范化 URL

预期结果：

- `pr-check` 失败
- `check-merge` 失败
- 错误码：`staging_rejected_conflict_accepted`
- 如果触发 `/finalize`，会在 `check-pr` 阶段失败

### T10 staging accepted 内部重复

前置条件：

- `staging/accepted/` 中放入 2 个不同文件
- 两个文件的 `canonical_url` 规范化后相同

预期结果：

- `pr-check` 失败
- `check-merge` 失败
- 错误码：`staging_accepted_duplicate_canonical_url`
- 如果触发 `/finalize`，会在 `check-pr` 阶段失败

### T11 staging rejected 内部重复

前置条件：

- `staging/rejected/rows.csv` 中有 2 行
- 两行 URL 规范化后相同

预期结果：

- `pr-check` 失败
- `check-merge` 失败
- 错误码：`staging_rejected_duplicate_url`
- 如果触发 `/finalize`，会在 `check-pr` 阶段失败

### T12 staging 中有不支持的文件

前置条件：

- 在 `staging/` 下加入不允许的文件或目录

示例：

- `staging/tmp.txt`
- `staging/rejected.csv`
- `staging/accepted/sample.txt`

预期结果：

- `pr-check` 失败
- `check-merge` 失败
- 错误码：`staging_unexpected_file`
- 如果触发 `/finalize`，会在 `check-pr` 阶段失败

### T13 staging accepted 文件名非法

前置条件：

- 在 `staging/accepted/` 中创建非法文件名

示例：

- `SRC-0001-sample.md`
- `Bad Name.md`
- `sample_file.md`

预期结果：

- `pr-check` 失败
- `check-merge` 失败
- 错误码：`staging_accepted_invalid_filename`
- 如果触发 `/finalize`，会在 `check-pr` 阶段失败

### T14 staging accepted 内容结构非法

前置条件：

- accepted Markdown front matter 不合法，或缺少必填字段，或字段值非法

示例：

- 缺少 `summary`
- `canonical_url` 非法
- `modality` 枚举值非法

预期结果：

- `pr-check` 失败
- `check-merge` 失败
- 可能错误码包括：
- `staging_accepted_parse_error`
- `staging_accepted_missing_field`
- `staging_accepted_unknown_field`
- `staging_accepted_invalid_array`
- `staging_accepted_invalid_enum`
- `staging_accepted_invalid_canonical_url`
- 如果触发 `/finalize`，会在 `check-pr` 阶段失败

### T15 staging rejected 表头或行结构非法

前置条件：

- `staging/rejected/rows.csv` 表头错误，或某行列数不对，或字段缺失

示例：

- 表头不是 `url,title,reason`
- 某行缺少 `reason`
- 某行 URL 非法

预期结果：

- `pr-check` 失败
- `check-merge` 失败
- 可能错误码包括：
- `staging_rejected_invalid_header`
- `staging_rejected_invalid_row_shape`
- `staging_rejected_missing_url`
- `staging_rejected_missing_title`
- `staging_rejected_missing_reason`
- `staging_rejected_invalid_url`
- 如果触发 `/finalize`，会在 `check-pr` 阶段失败

### T16 正式区 `data/accepted/` 非法

前置条件：

- 人为构造一个不合法的正式 accepted 文件

预期结果：

- `pr-check` 失败
- `check-merge` 失败
- 如果触发 `/finalize`，会在 `check-pr` 阶段失败
- 典型错误码为 `accepted_*`

说明：

- 这是正式区问题，不是 staging 问题
- 即使 staging 合法，也应整体失败

### T17 正式区 `data/rejected.csv` 非法

前置条件：

- 人为构造一个不合法的 `data/rejected.csv`

示例：

- 表头错误
- URL 非法
- 同一个 URL 重复

预期结果：

- `pr-check` 失败
- `check-merge` 失败
- 如果触发 `/finalize`，会在 `check-pr` 阶段失败
- 可能错误码包括：
- `rejected_invalid_header`
- `rejected_invalid_url`
- `rejected_duplicate_url`

### T18 正式区 accepted / rejected 交叉冲突

前置条件：

- 同一个规范化 URL 同时存在于 `data/accepted/` 和 `data/rejected.csv`

预期结果：

- `pr-check` 失败
- `check-merge` 失败
- 如果触发 `/finalize`，会在 `check-pr` 阶段失败
- 错误码：`cross_url_conflict`

### T19 push 后 `pr-check` 通过，但 `check-merge` 因 pending staging 失败

目标：

- 专门确认 `pr-check` 和 `check-merge` 的职责边界

前置条件：

- 构造任意一个 staging 合法但未 ingest 的 PR

操作步骤：

1. push 后确认 `pr-check` 通过
2. 观察自动触发的 `check-merge`

预期结果：

- `pr-check` 通过
- `check-merge` 失败
- 错误码：`merge_pending_staging`

### T20 `/finalize` 成功后再次验证

目标：

- 确认 ingest 后状态闭环正确

前置条件：

- T03、T04 或 T05 已通过 `pr-check`

操作步骤：

1. 触发 `/finalize`
2. 确认正式区已写入
3. 确认 staging 已清空
4. 再次验证 `check-merge`

预期结果：

- `/finalize` 成功
- 没有残留 pending staging
- `check-merge` 通过

## 最小必测集

如果这轮只想先跑一版高价值回归，建议至少执行下面 8 个用例：

- T01
- T02
- T03
- T05
- T06
- T08
- T10
- T19

这 8 个用例可以较快覆盖：

- 空仓与非空仓
- accepted / rejected 新增路径
- 与正式区冲突
- staging 内部重复
- `pr-check` 与 `check-merge` 的职责边界

## 推荐执行清单

如果按一轮标准回归来跑，建议使用下面这份清单：

1. 先跑 data 基线
- T01
- T02

2. 再跑 staging 主路径
- T03
- T04
- T05

3. 再跑高风险失败路径
- T06
- T08
- T10
- T12
- T14
- T16
- T18

4. 最后跑流程边界与闭环
- T19
- T20

执行原则：

- 标记为“必须”的用例，实际执行 `/finalize`
- 标记为“可选”的用例，只在需要验证统一维护者入口时执行 `/finalize`
- 标记为“否”的用例，默认不触发 `/finalize`，只观察自动检查结果

## 执行顺序建议

建议按下面顺序执行，减少来回清理环境的成本：

1. 先跑基线场景：T01-T05
2. 再跑冲突场景：T06-T09
3. 再跑 staging 非法输入：T10-T15
4. 最后跑正式区异常和联调闭环：T16-T20

## 测试记录模板

可直接按下面格式记录每次执行结果：

```md
## 用例编号

- 编号：
- 分支：
- 变更文件：
- 操作：
- 预期结果：
- 实际结果：
- 错误码：
- 是否通过：
- 备注：
```

## 结论标准

本轮测试通过的判断标准：

- 所有“预期通过”的用例均通过
- 所有“预期失败”的用例均以正确错误码失败
- `pr-check`、`check-merge`、`/finalize` 的职责边界与当前实现一致
- `/finalize` 前后状态变化符合预期，没有残留脏状态

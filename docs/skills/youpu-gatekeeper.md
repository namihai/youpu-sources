# youpu-gatekeeper

这份文档定义 `youpu-gatekeeper` 这项 skill 的定位、边界和最小交互规则。

## 定位

`youpu-gatekeeper` 是 `youpu` CLI 的自然语言编排层。

它的职责不是替代仓库规则，也不是扩展新的数据发现能力，而是帮助用户用自然语言完成仓库守门流程。

在当前阶段，规则执行层只有一个：

- `youpu` CLI

skill 只负责：

- 理解用户意图
- 选择合适的 `youpu` 命令
- 汇总 CLI 输出
- 解释问题清单
- 在必要时阻止继续执行

## 核心目标

这项 skill 只服务一个目标：

- 让用户更容易、安全地完成 `imports -> ingest -> validate -> submit` 这条守门路径

它不负责来源发现，也不负责事实补全。

## 负责什么

当前 skill 负责：

- 检查 `imports/` 中的候选内容
- 执行导入前预检查
- 执行正式导入
- 检查正式仓库状态
- 执行提交前检查
- 在通过检查后执行提交与可选推送
- 解释 `imports/reports/issues.md`
- 对单个 URL 做轻量诊断

## 不负责什么

当前 skill 不负责：

- 外部来源发现
- 网页抓取与页面理解
- 自动寻找数据集 URL
- 自动补齐 accepted / rejected 字段
- 自动生成候选 accepted / rejected 内容
- 自动修改正式库中的已有记录
- 绕过 `youpu` 直接写仓库结果

## 唯一依赖的 CLI 命令

skill 只应编排以下命令：

- `youpu ingest --dry-run`
- `youpu ingest`
- `youpu validate`
- `youpu report`
- `youpu submit --check-only`
- `youpu submit --message "..." [--push]`
- `youpu inspect-url <url>`

除了这些命令，skill 不应自行发明额外规则。

## 支持的用户意图

### 1. 检查导入目录

典型表达：

- “检查 imports”
- “看看这些候选能不能导入”
- “跑一遍导入预检查”

skill 行为：

1. 运行 `youpu ingest --dry-run`
2. 读取结果
3. 如有问题，解释 `imports/reports/issues.md`
4. 汇总哪些内容可导入，哪些需要手工修正

### 2. 执行导入

典型表达：

- “导入 imports 里的内容”
- “执行合并”

skill 行为：

1. 先运行 `youpu ingest --dry-run`
2. 如果存在问题，停止并解释
3. 如果没有问题，再运行 `youpu ingest`
4. 汇报导入结果

### 3. 检查仓库

典型表达：

- “检查仓库”
- “看看现在是否合法”
- “做一次提交前检查”

skill 行为：

- 根据用户意图选择：
  - `youpu validate`
  - 或 `youpu submit --check-only`
- 汇总通过状态或问题清单

### 4. 提交与推送

典型表达：

- “提交”
- “帮我提交并推送”
- “用这个 message 提交”

skill 行为：

1. 先运行 `youpu submit --check-only`
2. 如果检查失败，停止并解释
3. 如果检查通过，再运行：
   - `youpu submit --message "..."`
   - 必要时加 `--push`

### 5. 诊断 URL

典型表达：

- “看看这个 URL 会怎么规范化”
- “检查这个链接是否像合法 canonical URL”

skill 行为：

- 运行 `youpu inspect-url <url>`
- 返回 canonical URL 或错误原因

## 必须遵守的规则

### 规则 1

所有写操作前，必须先做检查。

也就是：

- 导入前先 `youpu ingest --dry-run`
- 提交前先 `youpu submit --check-only`

### 规则 2

如果存在问题，必须停止，不得继续执行写操作。

例如：

- `ingest --dry-run` 发现问题
- `validate` 未通过
- `submit --check-only` 未通过

这时 skill 只能解释问题，不能继续导入或提交。

### 规则 3

skill 只解释现有规则，不新增业务判断。

skill 的判断依据只能来自：

- `youpu` 输出
- `imports/reports/issues.md`
- 仓库内已有规范文档

### 规则 4

skill 只使用默认 `imports/` 目录。

skill 不应引入多工作区、多导入路径或其他额外复杂度。

## 停止条件

出现以下任一情况时，skill 必须停止当前写操作，并向用户说明原因：

- `youpu ingest --dry-run` 返回问题
- `youpu validate` 未通过
- `youpu submit --check-only` 未通过
- `imports/reports/issues.md` 仍有未解决问题
- 用户未提供提交 message，但要求执行提交
- CLI 返回运行时错误，且 skill 无法自动恢复

## 输出要求

skill 输出应尽量简洁，并覆盖这些信息：

- 当前执行了什么命令
- 结果是通过还是失败
- 如果失败，问题在哪
- 用户下一步该做什么

不要输出与仓库规则无关的推测性建议。

## 推荐工作流

### 场景 A：检查候选内容

1. 用户把候选文件放进 `imports/accepted/` 和 `imports/rejected/`
2. skill 运行 `youpu ingest --dry-run`
3. 如有问题，skill 解释 `imports/reports/issues.md`
4. 用户手工修正问题

### 场景 B：执行导入

1. skill 先运行 `youpu ingest --dry-run`
2. 确认无问题后运行 `youpu ingest`
3. skill 汇报导入结果
4. 建议用户继续执行 `validate` 或 `submit --check-only`

### 场景 C：提交与推送

1. skill 运行 `youpu submit --check-only`
2. 如果失败，停止并解释
3. 如果通过，执行 `youpu submit --message "..."`
4. 如用户明确要求，再执行 `--push`

## 示例

### 示例 1

用户：

```text
检查 imports
```

skill：

1. 运行 `youpu ingest --dry-run`
2. 解释：
   - 可导入多少项
   - 有哪些失败项
   - 应该先看 `imports/reports/issues.md`

### 示例 2

用户：

```text
导入 imports 里的内容
```

skill：

1. 先运行 `youpu ingest --dry-run`
2. 如果没有问题，再运行 `youpu ingest`
3. 汇报合并结果

### 示例 3

用户：

```text
帮我提交并推送，message 用 "update sources"
```

skill：

1. 先运行 `youpu submit --check-only`
2. 如果通过，再运行：
   - `youpu submit --message "update sources" --push`

## 当前结论

`youpu-gatekeeper` 当前只是一个轻量 skill：

- 它是守门流程的自然语言入口
- 它不替代 CLI
- 它不替代仓库规范
- 它不承担外部发现和事实补全

这就是当前阶段最稳的设计。

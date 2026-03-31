# youpu-gatekeeper

`youpu-gatekeeper` 是这个仓库推荐使用的 skill。  
它的作用很简单：帮你用自然语言完成导入检查、正式导入、仓库检查和提交前检查。

如果你不想直接使用命令行，优先使用这项 skill。

## 这项 skill 能帮你做什么

- 检查 `imports/` 里的候选内容能不能导入
- 执行正式导入
- 检查正式仓库当前是否合规
- 做一次提交前检查
- 在检查通过后执行提交和推送
- 解释 `imports/reports/issues.md` 里的问题
- 诊断单个 URL

## 这项 skill 不做什么

它不负责：

- 帮你发现新的外部来源
- 自动补齐缺失字段
- 自动判断一个外部链接该不该收录
- 绕过仓库规则直接写 `accepted/` 或 `rejected/`

也就是说，这项 skill 是“守门助手”，不是“采集助手”。

## 你怎么使用它

你只需要用自然语言描述想做的事。

常见说法例如：

```text
检查 imports
导入 imports 里的内容
检查仓库
做一次提交前检查
提交
提交并推送
检查这个 URL：https://example.com/path?utm_source=x#intro
```

## 推荐使用顺序

### 1. 先准备候选内容

把文件放进：

```text
imports/
  accepted/
  rejected/
```

### 2. 先让 skill 检查

你可以说：

```text
检查 imports
```

这一步不会直接导入，而是先帮你找出问题。

### 3. 看问题清单

如果有问题，优先查看：

- [`imports/reports/issues.md`](../../imports/reports/issues.md)

这份清单会告诉你：

- 哪些内容可以导入
- 哪些内容格式不对
- 哪些内容与现有记录冲突

### 4. 再执行正式导入

确认问题处理完后，你可以说：

```text
导入 imports 里的内容
```

### 5. 导入后检查仓库

你可以说：

```text
检查仓库
```

或者：

```text
做一次提交前检查
```

### 6. 最后提交

如果你已经确认要提交，可以说：

```text
提交
```

如果还要推送到远端：

```text
提交并推送
```

默认情况下，AI 会根据当前改动自动生成合适的 commit message。

## 它会在什么时候停下来

这项 skill 不会盲目继续往下执行。

遇到这些情况时，它会停下来并告诉你为什么：

- `imports/` 里还有格式问题
- 导入内容与现有记录冲突
- 正式仓库当前没有通过检查
- 提交前检查没有通过

这时你需要先处理问题，再继续。

## 命令行和 skill 的关系

这项 skill 的底层其实还是在调用 `youpu`。  
如果你更喜欢直接用命令行，可以看：

- [CLI 用户文档](../cli/user-guide.md)

如果你只是正常使用仓库，优先用 skill 就可以。

## 相关文档

- 文档总入口：[../index.md](../index.md)
- CLI 用户文档：[../cli/user-guide.md](../cli/user-guide.md)
- accepted 规范：[../specs/accepted.md](../specs/accepted.md)
- rejected 规范：[../specs/rejected.md](../specs/rejected.md)

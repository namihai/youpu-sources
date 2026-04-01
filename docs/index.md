# 文档索引

这里是 `youpu-sources` 的详细说明入口。

如果你刚开始使用仓库，建议按这个顺序阅读：

1. [README.md](../README.md)
2. [项目边界](overview/project-scope.md)
3. [CLI 用户文档](cli/user-guide.md)
4. 需要时再看具体规范

## 面向贡献者

- README：[../README.md](../README.md)
- 常见失败与处理方式：[overview/failures.md](overview/failures.md)
- CLI 用户文档：[cli/user-guide.md](cli/user-guide.md)
- accepted 规范：[specs/accepted.md](specs/accepted.md)
- rejected 规范：[specs/rejected.md](specs/rejected.md)
- URL 规范：[specs/url.md](specs/url.md)

## 面向维护者

- 常见失败与处理方式：[overview/failures.md](overview/failures.md)
- 维护者操作手册：[overview/maintainer-guide.md](overview/maintainer-guide.md)
- 项目边界：[overview/project-scope.md](overview/project-scope.md)
- GitHub 仓库设置：[overview/github-repo-setup.md](overview/github-repo-setup.md)
- CLI 边界：[cli/scope.md](cli/scope.md)
- CLI 用户文档：[cli/user-guide.md](cli/user-guide.md)
- CLI 开发接口：[cli/spec.md](cli/spec.md)

## 说明

- `youpu` 现在主要是 GitHub Actions 和维护者使用的规则接口
- 普通贡献者的主流程是提交 `imports/` 并通过 PR 协作完成入库
- `imports/` 的有效输入只有两类：根目录 Markdown 和 `imports/rejected.csv`

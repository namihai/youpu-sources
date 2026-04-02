# 文档索引

这里是 `youpu-sources` 的详细说明入口。

如果你刚开始使用仓库，建议按这个顺序阅读：

1. [README.md](../README.md)
2. [贡献指南](guides/contributor.md)
3. [项目边界](architecture/project-boundary.md)
4. 需要时再看具体规范

## 指南

- README：[../README.md](../README.md)
- 贡献指南：[guides/contributor.md](guides/contributor.md)
- 维护者指南：[guides/maintainer.md](guides/maintainer.md)

## 参考

- CLI 接口说明：[reference/cli.md](reference/cli.md)

## 架构

- 项目边界：[architecture/project-boundary.md](architecture/project-boundary.md)
- 源码结构：[architecture/source-layout.md](architecture/source-layout.md)

## 运维

- 常见失败与处理方式：[operations/failures.md](operations/failures.md)
- GitHub 仓库设置：[operations/github-setup.md](operations/github-setup.md)

## 规范

- accepted 规范：[specs/accepted.md](specs/accepted.md)
- rejected 规范：[specs/rejected.md](specs/rejected.md)
- schema 规范：[specs/schema.md](specs/schema.md)
- URL 规范：[specs/url.md](specs/url.md)
- Schema 配置：[../schemas/accepted.json](../schemas/accepted.json) / [../schemas/rejected.json](../schemas/rejected.json)

## 说明

- `youpu` 是逻辑命令接口名；当前仓库内实际执行入口为 `./scripts/youpu`
- 新增来源走 `staging/`
- 修改和删除正式记录直接改 `data/`

# URL 规范

这份文档定义本仓库中 `canonical_url` 与 `rejected.csv:url` 的统一规范。

适用范围：

- `accepted/*.md` 中的 `canonical_url`
- `rejected/rejected.csv` 中的 `url`
- `youpu inspect-url`
- `youpu ingest`
- 任何做去重或交叉冲突检查的逻辑

## 目标

规范化的目标是稳定标识“同一个来源”，而不是生成最短 URL。

优先级：

1. 稳定
2. 可预测
3. 可复现
4. 保守

## 基本原则

- 优先使用来源的稳定主链接
- 优先使用详情页、数据集主页面、仓库主页面等能代表来源本身的页面
- 如果同一来源同时存在详情页和下载页，优先保留更能代表来源本身的详情页
- 对同一资源的不同跳转链接，应尽量归并到同一个主链接

## 允许的规范化

- 去掉页面锚点，例如 `#intro`
- 去掉追踪参数，例如 `utm_*`
- 去掉明显无意义的 query 参数
- 去掉默认端口，例如 `:80`、`:443`
- 保留能够唯一标识资源的关键参数，例如：
  - `dataSetId`
  - `persistentId`
  - DOI 相关参数

## 不应做的事

- 不应自动把一个站点链接改写成另一个站点链接
- 不应自动把论文页推断成数据页
- 不应自动把详情页替换成第三方镜像页
- 不应跨站点合并链接，除非规则已明确约定
- 不应为了“更短”而删掉会影响唯一标识的参数

## 无法确定时

- 保守保留当前主链接
- 不做隐式猜测
- 如果仍无法形成稳定主链接，应在记录中显式标注待确认，而不是随意改写

## CLI 实现规则

`youpu` 当前实现的 URL 规范化包括：

- 去锚点
- 去 `utm_*`
- 去常见追踪参数：
  - `fbclid`
  - `gclid`
  - `dclid`
  - `mc_cid`
  - `mc_eid`
  - `igshid`
- 去默认端口
- 保留关键 query 参数

这是一套保守规则，不做页面级智能推断。

## 示例

### 示例 1

输入：

```text
https://example.com/dataset/123?utm_source=x#intro
```

输出：

```text
https://example.com/dataset/123
```

### 示例 2

输入：

```text
https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/70A2QQ&utm_campaign=test
```

输出：

```text
https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi%3A10.7910%2FDVN%2F70A2QQ
```

## 相关文档

- accepted 规范：[accepted.md](accepted.md)
- rejected 规范：[rejected.md](rejected.md)
- CLI 开发接口文档：[spec.md](../cli/spec.md)
- CLI 用户文档：[user-guide.md](../cli/user-guide.md)

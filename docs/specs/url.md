# URL 规范

这份文档定义本仓库中 `canonical_url` 与 `data/rejected.csv:url` 的统一规范。

适用范围：

- `data/accepted/*.md` 中的 `canonical_url`
- `data/rejected.csv` 中的 `url`
- `uv run python ./scripts/youpu ingest`
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
- `canonical_url` 代表来源的 canonical URL，通常应是介绍该数据集的主页、详情页、仓库主页面等能代表来源本身的页面
- `canonical_url` 一般不是下载链接；下载链接应在 Markdown 正文中说明
- 如果数据集没有独立主页、只有下载链接，可以使用下载链接作为 `canonical_url`
- 如果同一来源同时存在详情页和下载页，优先保留更能代表来源本身的详情页
- 对同一资源的不同跳转链接，应尽量归并到同一个主链接

## 允许的规范化

- 去掉页面锚点，例如 `#intro`
- 去掉追踪参数，例如 `utm_*`
- 去掉默认端口，例如 `:80`、`:443`
- 保留 IPv4、IPv6 和显式用户信息的合法主机写法
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

`youpu` 的 URL 规范化包括：

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
- 保留合法的 IPv6 主机方括号形式

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
- CLI 接口说明：[../reference/cli.md](../reference/cli.md)

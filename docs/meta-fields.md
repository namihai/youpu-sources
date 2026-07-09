# Meta 字段

Meta 字段写在每个 `data/*.md` 文件开头的 front matter 中。当前生效的机器可读规则定义在 [`../scripts/checker.json`](../scripts/checker.json)。

## 必填字段

- `title`：来源名称。
- `summary`：一句简短、客观的话，说明这个来源是什么。
- `canonical_url`：主要来源 URL，通常是数据集页面或来源主页。
- `publisher`：发布、维护或提供该来源的机构、项目、团队或个人。
- `modality`：主要数据模态。
- `access_level`：获取该来源的访问门槛。

## 选填字段

- `tags`：用于检索和简单分组的短标签，使用单行内联数组书写。

## 字段类型

- `string`：字符串；如果字段是必填字段，则不能为空。
- `url`：绝对 URL，必须包含 scheme 和 host。
- `enum`：枚举值，必须从配置允许的值中选择一个。
- `inline_array`：单行数组，例如 `[敦煌, 壁画, 图像]`。

## 枚举值

`modality` 必须使用以下值之一：

- `text`
- `image`
- `audio`
- `video`
- `tabular`
- `geospatial`
- `multimodal`
- `other`

`access_level` 必须使用以下值之一：

- `open`：可以直接访问或下载，不需要人工审批。
- `request`：需要登录、注册、申请、提交表单或其他访问步骤。
- `restricted`：不公开可用，或只能通过封闭授权渠道获取。
- `unknown`：当前无法确认访问条件。

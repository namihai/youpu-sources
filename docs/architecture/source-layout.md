# 源码结构

这份文档说明 `youpu-sources` 当前 CLI 代码的源码布局，以及新增逻辑时应放在哪一层。

## 总体结构

当前源码位于：

- `src/youpu/`

仓库内部执行入口位于：

- `scripts/youpu`

测试默认通过下面的真实命令运行：

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## 分层约定

`src/youpu/` 采用四层结构：

- `src/youpu/cli/`
- `src/youpu/app/`
- `src/youpu/domain/`
- `src/youpu/infra/`

### `cli`

职责：

- 命令入口
- 参数解析
- 退出码映射
- 文本 / JSON 输出封装

不负责：

- 规则判断细节
- 仓库文件读写
- 跨命令业务编排

换句话说，`cli` 应该尽量薄，只调用 `app` 层。

### `app`

职责：

- 用例编排
- 聚合多个检查或流程步骤
- 把 domain / infra 组织成完整的业务动作

当前典型内容：

- `checks.py`
- `ingest.py`
- `report.py`

如果一个功能描述更像“执行一次完整操作”，通常应该先考虑放在 `app`。

### `domain`

职责：

- 领域模型
- 规则定义
- 纯函数校验
- schema 语义
- URL 规范化

不负责：

- 命令行参数
- stdout / stderr
- 直接读写仓库文件

如果一段逻辑在理想情况下不需要知道文件系统、命令行或进程状态，它更适合放在 `domain`。

### `infra`

职责：

- 仓库目录布局
- schema 文件读取
- accepted / rejected 文件读写
- 与 `Path`、`csv`、磁盘文件等基础设施打交道

如果代码直接依赖文件路径、目录结构、文件格式或磁盘操作，它更适合放在 `infra`。

## 新增代码时怎么放

可以按下面规则判断：

- 新增一个对外命令：放 `src/youpu/cli/commands/`
- 新增一个完整检查流程或 ingest 流程：放 `src/youpu/app/`
- 新增一个字段规则、重复判断、URL 处理：放 `src/youpu/domain/`
- 新增一个 markdown/csv/json 文件解析器或 repo 布局函数：放 `src/youpu/infra/`

## 不推荐的做法

- 在 `cli` 里直接写业务规则
- 在 `domain` 里直接做磁盘写入
- 把共享逻辑塞进 `utils.py` 或 `helpers.py`
- 让命令模块彼此调用 `run()`

这些做法会重新把边界打散，长期会回到难测试、难维护的状态。

## 本地运行

维护者或自动化流程推荐方式：

```bash
./scripts/youpu report
./scripts/youpu validate-schema
PYTHONPATH=src python3 -m unittest discover -s tests
```

如果需要直接通过 Python 模块运行，应显式带上 `src`：

```bash
PYTHONPATH=src python3 -m youpu.cli report
PYTHONPATH=src python3 -m youpu.cli.main report
```

## 相关文档

- CLI 接口说明：[../reference/cli.md](../reference/cli.md)
- 项目边界：[project-boundary.md](project-boundary.md)

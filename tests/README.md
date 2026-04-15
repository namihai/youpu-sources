# Tests

这个目录是测试入口。

当前测试分两层：

1. 规则与 CLI 层测试
2. 流程测试

## 目录说明

- `test_*.py`
  现有单元测试与 CLI 契约测试
- `source-examples/`
  accepted 正向真实样例
- `flow/`
  流程测试文档、用例目录和本地自动化 runner

## 流程测试入口

流程测试的主文档在：

- [`tests/flow/README.md`](./flow/README.md)

本地流程测试入口：

```bash
python3 tests/flow/run_flow_tests.py --list
python3 tests/flow/run_flow_tests.py --run
```

## 维护建议

后续 agent 如果要维护流程测试，优先阅读：

1. `tests/flow/README.md`
2. `tests/flow/cases/catalog.py`
3. `tests/flow/run_flow_tests.py`

不要再维护仓库根目录的独立测试计划文档，避免计划和实现分叉。

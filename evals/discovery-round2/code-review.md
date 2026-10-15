# pool --review Python review

结论：**Approve**。当前未提交的 `cli.py`、`discovery.py`、`tests/test_discovery.py` 变更未发现需要修复的正确性、安全性或兼容性问题。

## 审查范围与依据

- `pool --review` 是可选展开；默认 `pool` 返回值与 HEAD 实现逐项相等（同时检查有、无 report 两种调用）。
- 摘录索引使用 `(source_id, excerpt_id)` 联合键；字段 support 和 counterevidence 都从该联合键读取原文及 locator，并从对应 source 读取 URL。
- review 仅遍历已选中的 needs；已有 study/report 校验确保支持来源属于该 need 的 social run，且该 run 被报告选择。全库建立索引不会直接输出未引用内容。
- 展开使用新字典，不修改输入状态或台账；unknown basis 保留空 evidence；未声明的 claim 字段仍被严格校验拒绝。

## 验证结果

运行 `.venv/bin/python -m pytest -q tests/test_discovery.py tests/test_cli.py`：**27 passed，8 subtests passed**。

另外运行了不落盘的定向断言，全部通过：

- 两个来源均包含 e1/e2，引用 s2:e2 与 s1:e2 时分别返回正确原文、locator 和 URL，保留多个支持引用的顺序。
- 反证 s2:e1 不会错误绑定到 s1:e1。
- 未选需求与未引用来源的特征文本不出现在 review 结果。
- report 的 need_ids 为空或缺省时，claim_review 为空。
- unknown 字段没有虚构 evidence；额外未声明字段被 WorkbenchError 拒绝。
- 调用前后输入 study 深度相等；CLI 回归测试确认 research.json 字节不变。
- 默认输出与 HEAD 实现相等。

ruff、mypy、pylint、black 在当前环境均未安装，因此未执行这些静态分析工具。

本次仅创建此审查报告，未修改代码、测试或其他 agent 的文件。

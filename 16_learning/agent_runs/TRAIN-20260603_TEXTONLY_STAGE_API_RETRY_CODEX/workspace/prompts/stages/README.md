# 阶段提示词文件

本目录为每个工作流阶段保存一个提示词合同。

命名约定：

```text
<stage_order>_<stage_id>.md
```

上级规范：

```text
prompts/stage_prompt_contract.md
```

这些文件只提供设计和执行指导。除非后续任务明确把它们接入脚本，否则它们不会改变 Python 运行行为。

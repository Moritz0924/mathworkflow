{
  "status": "blocked",
  "summary": "无法执行润色：缺少 artifact_freeze_registry.csv 和 09_paper/ 下的草稿章节，无法提取受保护事实原子进行安全润色。",
  "files": [
    {
      "path": "10_polish/polish_stage_blocked.md",
      "operation": "write",
      "content": "# Polish 阶段阻塞说明\n\n- **阻塞时间**：初始迭代\n- **阻塞原因**：`14_contracts/artifact_freeze_registry.csv` 未找到；`09_paper/` 下的草稿 `.tex` 章节文件未提供或不可读。\n- **依赖条件**：`revision` 阶段已关闭所有 fail/major 问题或取得人工豁免，且章节内容已冻结并注册到 `artifact_freeze_registry.csv`。\n- **后续步骤**：完成 `revision` 并生成冻结登记表；提供 `09_paper/` 下的具体章节路径。\n- **风险说明**：在无原文的情况下无法提取受保护事实原子（数字、单位、公式、标签、引用、模型名），任何直接润色都可能破坏内容完整性，违反阶段约束。\n"
    }
  ],
  "unresolved": [
    {
      "issue": "precondition_not_met: missing artifact_freeze_registry.csv and paper draft sections",
      "blocker": "Cannot extract protected atoms; polish cannot proceed without original text to diff-check."
    }
  ]
}

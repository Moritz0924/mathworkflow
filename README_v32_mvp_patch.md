# 数学建模工作流 v3.2-MVP 补丁说明

这个补丁在 v3.0 的基础上增加最小治理层，用于连接 `nature-skills`、Prior DB 检索、合同校验、自动审稿和受控迭代。

## 补丁包含什么

- `AGENTS.md`：Codex 与技能治理规则。
- `config/*.yaml`：执行、技能、合同、迭代和 Prior DB 策略。
- `14_contracts/*`：合同总线模板。
- `11_review/*`：审稿器与评分表模板。
- `13_prior_db/*`：受控先验数据库骨架。
- `15_iteration_memory/*`：迭代记忆模板。
- `docs/directory_structure_v32_mvp.md`：目标目录树。
- `docs/scripts_modification_plan.md`：需要修改和新增的脚本说明。
- `docs/nature_skills_integration.md`：`nature-skills` 集成说明。

## 手动应用方式

1. 将这些文件复制到 v3.0 项目根目录。
2. 保留现有 v3.0 文件夹和脚本。
3. 按 `docs/scripts_modification_plan.md` 修改脚本。
4. 将 `nature-skills` 克隆到 `vendor/nature-skills`。
5. 使用本地 Codex 时，将完整技能目录同步到 `~/.codex/skills/`。
6. 在论文生成、润色和最终导出前运行合同校验。

## MVP 边界

本补丁不实现完整自动化。它先定义稳定的文件合同和控制规则；合同总线被接受后，再补齐脚本实现。

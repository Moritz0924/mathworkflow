# Prior Retrieval Stage Summary

- **执行时间**: 2025-01-17 (simulated)
- **阶段状态**: 阻塞（缺失必要输入，已按失败恢复策略生成占位）
- **输出**:
  - `13_prior_db/pre_solve_cards.md` (占位经验卡片)
  - `11_review/prior_retrieval_stage_summary.md` (本文件)
- **缺失输入**:
  1. `config/prior_db_policy.yaml`
  2. `01_task_analysis/problem_model_profile.csv`
  3. `13_prior_db/` 先验数据库目录（无任何历史卡片）
- **风险**: 下游模型路由只能依赖通用知识，无法获得历史经验支持；可能增大模型选择偏差风险。
- **建议**: 在执行 `model_route` 前务必完成 `task_analysis` 并生成 `problem_model_profile.csv`；如有先验材料（如 PDF 题库），应执行 preprocessing 抽取卡片。
- **人工确认**: 因前置缺失，本次未进行实质先验检索。所生成的占位卡片仅作为后续阶段参考，不替代正式先验分析。

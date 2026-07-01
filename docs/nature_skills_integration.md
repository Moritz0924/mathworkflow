# `nature-skills` 集成说明

## 安装策略

使用项目 vendor 文件夹作为锁定来源：

```bash
git clone https://github.com/Yuan1z0825/nature-skills.git vendor/nature-skills
```

需要本地 Codex 使用时，再同步到 Codex 技能目录：

```bash
mkdir -p ~/.codex/skills
for d in vendor/nature-skills/skills/nature-*; do
  cp -R "$d" ~/.codex/skills/
done
```

## 技能使用边界

| 技能 | v3.2-MVP 用法 | 边界 |
|---|---|---|
| `nature-figure` | 图表设计与导出质量 | 必须使用 `figure_contract.csv` |
| `nature-writing` | 分章节论证草拟 | 必须使用论断、结果、图表、公式、引用合同 |
| `nature-polishing` | 学术润色 | 必须保留受保护事实原子 |
| `nature-citation` | 引用候选与支撑等级 | 不得伪造元数据 |
| `nature-data` | 数据可用性与 FAIR 说明 | 适配比赛可复现性语境 |
| `nature-reader` | 先验论文阅读 | 求解前只能抽取经验卡片 |
| `nature-response` | 审稿任务归并 | 不得直接修改正式交付物 |
| `nature-paper2ppt` | 终稿后的展示材料 | 只能在终稿后使用 |
| `nature-academic-search` | 安装 MCP 后的检索 | MVP 中可选，不阻塞工作流 |

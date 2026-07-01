# LaTeX 模板说明

## 结构
- `main.tex`：主文件，引入章节子文件。
- `sections/`：各章节占位文件。
- `figures/`：放置图片（如有，可创建子目录）。

## 编译方法
建议使用 XeLaTeX 或 LuaLaTeX 编译以原生支持中文，命令：
```
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```
或使用 `latexmk -xelatex main.tex`（需安装 latexmk）。

## 标签命名规则
- 图：  `fig:节名_描述`
- 表：  `tab:节名_描述`
- 公式：`eq:节名_描述`
- 节：  `sec:节名`
- 算法：`alg:算法名`
- 文献：键格式 `FirstAuthorYearKeyword`（如 `Zhang2020Survey`）

## 注意事项
1. 模板中所有内容均为占位符，不包含任何实际题目的事实或结果。
2. 后续生成实际内容时，需严格通过合同系统绑定：`claim_evidence_map.csv`, `result_contract.csv`, `figure_contract.csv`, `formula_contract.csv`, `citation_contract.csv`。
3. 所有图表必须先登记到 `figure_contract.csv` 并生成实际文件后才可在论文中引用。

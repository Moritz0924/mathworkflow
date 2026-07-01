# LaTeX 模板说明

## 编译方式
- 使用 XeLaTeX 引擎，需安装完整的 TeX 发行版（TeX Live / MiKTeX）。
- 需要 `ctex` 宏包及中文字体支持。
- 运行 `compile.bat` 或手动执行 `xelatex main` → `bibtex main` → `xelatex main` → `xelatex main`。

## 标签命名规则
- 章：`sec:xxx`
- 图：`fig:xxx`
- 表：`tab:xxx`
- 公式：`eq:xxx`
- 算法：`alg:xxx`
- 所有标签须在相应合同文件中登记。

## 合同接口
- 数值结果：须在 `14_contracts/result_contract.csv` 中记录。
- 图/表：须在 `14_contracts/figure_contract.csv` 中登记。
- 公式：须在 `14_contracts/formula_contract.csv` 中登记。
- 引用：须在 `14_contracts/citation_contract.csv` 中登记。

## 占位文本
- 所有章节目前仅含占位说明，不含任何建模事实。替换时请保留 LaTeX 结构。

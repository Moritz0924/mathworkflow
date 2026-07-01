from __future__ import annotations
from pathlib import Path
from workflow_utils import ROOT, assert_stage_allowed, complete_stage

def write_if_missing(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or not path.read_text(encoding="utf-8", errors="ignore").strip(): path.write_text(text, encoding="utf-8")

def main(dev_debug: bool=False):
    assert_stage_allowed("latex_template", dev_debug)
    base=ROOT/"02_latex_template"; sec=base/"sections"; (base/"figures").mkdir(parents=True, exist_ok=True); sec.mkdir(parents=True, exist_ok=True)
    write_if_missing(base/"main.tex", r'''\documentclass[UTF8,a4paper,12pt]{ctexart}
\input{preamble.tex}
\begin{document}
\input{sections/00_abstract}
\input{sections/01_background}
\input{sections/02_problem_analysis}
\input{sections/03_assumptions}
\input{sections/04_symbols}
\input{sections/05_data_analysis}
\input{sections/06_model_q1}
\input{sections/07_model_q2}
\input{sections/08_model_q3}
\input{sections/09_sensitivity}
\input{sections/10_model_evaluation}
\input{sections/11_conclusion}
\bibliographystyle{gbt7714-numerical}
\bibliography{references}
\appendix
\input{sections/appendix}
\end{document}
''')
    write_if_missing(base/"preamble.tex", r'''\usepackage{geometry}
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}
\usepackage{amsmath,amssymb,bm,graphicx,booktabs,longtable,array,float,caption,subcaption,algorithm,algpseudocode,hyperref,xcolor}
\usepackage{cn_math_style}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=blue}
\captionsetup{font=small, labelfont=bf}
\setlength{\parindent}{2em}
\setlength{\parskip}{0.2em}
''')
    write_if_missing(base/"cn_math_style.sty", r'''\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{cn_math_style}[2026/05/07 Chinese mathematical modeling style]
\RequirePackage{ctex}
\RequirePackage{titlesec}
\RequirePackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\cfoot{\thepage}
\titleformat{\section}{\centering\heiti\zihao{3}}{\thesection}{1em}{}
\titleformat{\subsection}{\heiti\zihao{4}}{\thesubsection}{1em}{}
\titleformat{\subsubsection}{\heiti\zihao{-4}}{\thesubsubsection}{1em}{}
\newcommand{\figref}[1]{图~\ref{#1}}
\newcommand{\tabref}[1]{表~\ref{#1}}
\newcommand{\eqnref}[1]{式~\eqref{#1}}
''')
    write_if_missing(base/"references.bib", "% 请填入真实参考文献，禁止虚构文献。\n")
    sections=[("00_abstract.tex",r'''% 摘要建议在全文完成后最后生成。
\begin{abstract}
% TODO: 摘要最后生成，避免与正文不一致。
\end{abstract}
\noindent\textbf{关键词：} TODO；数学建模；数据分析；模型求解
'''),("01_background.tex","\\section{问题背景与问题重述}\n\n% TODO: 基于赛题原文填写。\n"),("02_problem_analysis.tex","\\section{问题分析}\n\n% TODO: 基于分问拆解填写。\n"),("03_assumptions.tex","\\section{模型假设}\n\n% TODO: 假设必须服务模型，不得空泛。\n"),("04_symbols.tex","\\section{符号说明}\n\n% TODO: 用三线表列出变量和含义。\n"),("05_data_analysis.tex","\\section{数据预处理与数据分析}\n\n% TODO: 插入数据质量报告和 EDA 结论。\n"),("06_model_q1.tex","\\section{问题一模型建立与求解}\n\n% TODO: 基于真实 Q1 结果填写。\n"),("07_model_q2.tex","\\section{问题二模型建立与求解}\n\n% TODO: 基于真实 Q2 结果填写。\n"),("08_model_q3.tex","\\section{问题三模型建立与求解}\n\n% TODO: 基于真实 Q3 结果填写。\n"),("09_sensitivity.tex","\\section{灵敏度分析与误差分析}\n\n% TODO: 基于真实结果填写。\n"),("10_model_evaluation.tex","\\section{模型评价}\n\n% TODO: 写优缺点和改进方向。\n"),("11_conclusion.tex","\\section{结论}\n\n% TODO: 全文完成后填写。\n"),("appendix.tex","\\section{附录}\n\n% TODO: 放置代码说明、补充图表和必要推导。\n")]
    for fn, txt in sections: write_if_missing(sec/fn, txt)
    complete_stage("latex_template", "已生成 v3.0 LaTeX 模板和章节骨架。")
    print("[OK] generated 02_latex_template/")
if __name__ == "__main__":
    import sys; main("--dev-debug" in sys.argv)

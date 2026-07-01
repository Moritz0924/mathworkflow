@echo off
REM 使用 XeLaTeX 编译主文件（需要安装 TeX Live 或 MiKTeX 并包含 ctex 宏包）
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex

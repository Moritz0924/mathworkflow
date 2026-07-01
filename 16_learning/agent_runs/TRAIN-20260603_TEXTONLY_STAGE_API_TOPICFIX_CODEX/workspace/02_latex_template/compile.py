#!/usr/bin/env python3
"""简单的 LaTeX 编译脚本，使用 xelatex 编译 main.tex 两次以生成目录与交叉引用。
注意：编译前请确保已安装 TeX Live 并配置好中文字体（如 SimSun, SimHei 等）。
"""
import subprocess
import sys
import os

TEX_FILE = "main.tex"

def run_xelatex():
    for i in range(2):
        print(f"第 {i+1} 次编译...")
        result = subprocess.run(["xelatex", "-interaction=nonstopmode", TEX_FILE],
                                capture_output=True, text=True)
        if result.returncode != 0:
            print("编译失败，输出如下：")
            print(result.stdout)
            print(result.stderr)
            return False
        print("编译通过")
    return True

if __name__ == "__main__":
    if not os.path.exists(TEX_FILE):
        print(f"错误：未找到 {TEX_FILE}")
        sys.exit(1)
    success = run_xelatex()
    if not success:
        sys.exit(1)
    print("编译完成，PDF 已生成。")

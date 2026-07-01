from __future__ import annotations
import shutil, subprocess, sys
from workflow_utils import ROOT, assert_stage_allowed, complete_stage
def main(dev_debug=False):
    assert_stage_allowed("compile",dev_debug)
    texdir=ROOT/"02_latex_template"; outdir=ROOT/"12_export"; outdir.mkdir(parents=True,exist_ok=True); log=outdir/"compile_log.txt"
    xelatex=shutil.which("xelatex")
    if not xelatex:
        log.write_text("未检测到 xelatex。请安装 TeX Live/MacTeX/MiKTeX 后手动编译 02_latex_template/main.tex。\n",encoding="utf-8")
        print("[WARN] xelatex not found; wrote compile_log.txt"); complete_stage("compile","未检测到 xelatex，已写出编译说明。"); return
    outs=[]
    for _ in range(2):
        p=subprocess.run([xelatex,"-interaction=nonstopmode","main.tex"],cwd=str(texdir),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT); outs.append(p.stdout)
    log.write_text("\n".join(outs),encoding="utf-8")
    pdf=texdir/"main.pdf"
    if pdf.exists(): shutil.copy2(pdf,outdir/"final_paper.pdf"); complete_stage("compile","LaTeX 编译完成，已导出 final_paper.pdf。"); print("[OK] wrote 12_export/final_paper.pdf")
    else: raise SystemExit("[FAIL] 编译后未生成 PDF，请查看 12_export/compile_log.txt")
if __name__=="__main__": main("--dev-debug" in sys.argv)

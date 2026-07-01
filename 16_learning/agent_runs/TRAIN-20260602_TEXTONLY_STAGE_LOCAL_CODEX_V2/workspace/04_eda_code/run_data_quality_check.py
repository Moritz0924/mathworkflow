from __future__ import annotations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/"03_data/raw"; OUT_MD=ROOT/"03_data/data_quality_report.md"; OUT_TEX=ROOT/"03_data/data_quality_report.tex"
def esc(s): return str(s).replace('&','\\&').replace('%','\\%').replace('_','\\_').replace('#','\\#')
def read_table(p):
    try:
        import pandas as pd
        if p.suffix.lower() in {".xlsx",".xls"}: return pd.read_excel(p), ""
        if p.suffix.lower() in {".csv",".tsv"}: return pd.read_csv(p, sep="\t" if p.suffix.lower()==".tsv" else None, engine="python"), ""
        if p.suffix.lower() in {".json",".geojson"}: return pd.read_json(p), ""
    except Exception as e: return None, str(e)
    return None, "unsupported format"
def main():
    md=["# 数据质量报告","","本报告由 v3.0 自动生成，字段含义和异常处理仍需人工确认。",""]; tex=["\\section{数据预处理与数据质量诊断}","","本节由自动数据质量检查生成，字段含义和异常处理仍需人工确认。",""]
    for p in sorted(RAW.iterdir() if RAW.exists() else []):
        if not p.is_file() or p.name.startswith("."): continue
        df,err=read_table(p); md += [f"## {p.name}",""]; tex += [f"\\subsection{{{esc(p.name)}}}"]
        if df is None:
            md += [f"- 暂未自动读取：{err}",""]; tex += [esc(f"暂未自动读取：{err}"),""]; continue
        n,m=df.shape; dup=int(df.duplicated().sum()); md += [f"- 行数：{n}",f"- 列数：{m}",f"- 重复行：{dup}"]
        high=[(str(c),float(df[c].isna().mean())) for c in df.columns if float(df[c].isna().mean())>0.3]
        md.append("- 高缺失字段：" + ("；".join(f"{c}({r:.1%})" for c,r in high) if high else "无")); md.append("")
        tex += [f"数据文件共有 {n} 行、{m} 列，检测到重复行 {dup} 行。", ("高缺失字段包括："+"；".join(f"{esc(c)}({r:.1%})" for c,r in high)+"。") if high else "未发现缺失率超过 30\\% 的字段。", ""]
    OUT_MD.write_text("\n".join(md)+"\n",encoding="utf-8"); OUT_TEX.write_text("\n".join(tex)+"\n",encoding="utf-8"); print(f"[OK] wrote {OUT_MD.relative_to(ROOT)}")
if __name__=="__main__": main()

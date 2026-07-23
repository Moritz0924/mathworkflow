from __future__ import annotations
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/"03_data/raw"; FIG=ROOT/"08_figures/output"; REG=ROOT/"08_figures/figure_registry.csv"


def has_correlation_ready_columns(non_null_counts):
    """Return true only when at least two numeric columns have observations."""
    return sum(int(count) >= 2 for count in non_null_counts.values()) >= 2


def main():
    try:
        import pandas as pd, matplotlib.pyplot as plt
    except Exception as e:
        print(f"[WARN] 缺少 pandas/matplotlib，跳过 EDA 图生成：{e}"); return
    plt.rcParams["font.sans-serif"]=["Noto Sans CJK SC","Microsoft YaHei","SimHei","PingFang SC","Arial Unicode MS"]; plt.rcParams["axes.unicode_minus"]=False
    FIG.mkdir(parents=True, exist_ok=True); rows=[]; idx=1
    for p in sorted(RAW.iterdir() if RAW.exists() else []):
        if p.suffix.lower() not in {".csv",".tsv",".xlsx",".xls"}: continue
        try: df=pd.read_excel(p) if p.suffix.lower() in {".xlsx",".xls"} else pd.read_csv(p, sep="\t" if p.suffix.lower()==".tsv" else None, engine="python")
        except Exception as e: print(f"[WARN] skip {p.name}: {e}"); continue
        num=df.select_dtypes(include="number")
        non_null_counts={str(column): int(num[column].notna().sum()) for column in num.columns}
        if not has_correlation_ready_columns(non_null_counts):
            print(f"[INFO] skip correlation EDA for {p.name}: fewer than two observed numeric columns")
            continue
        ready_columns=[column for column in num.columns if int(num[column].notna().sum()) >= 2]
        if len(ready_columns)>=2:
            num=num[ready_columns]
            corr=num.corr(numeric_only=True); fig,ax=plt.subplots(figsize=(8,6),dpi=160); im=ax.imshow(corr,cmap="viridis",vmin=-1,vmax=1)
            ax.set_xticks(range(len(corr.columns)),labels=[str(c) for c in corr.columns],rotation=45,ha="right",fontsize=8); ax.set_yticks(range(len(corr.index)),labels=[str(c) for c in corr.index],fontsize=8); ax.set_title(f"{p.stem} 数值变量相关性热力图",fontsize=12,fontweight="bold"); fig.colorbar(im,ax=ax); fig.tight_layout()
            out=FIG/f"eda_{p.stem}_corr_heatmap.png"; fig.savefig(out,bbox_inches="tight"); plt.close(fig)
            rows.append({"figure_id":f"EDA{idx}","path":str(out.relative_to(ROOT)),"title":f"{p.stem} 数值变量相关性热力图","question_id":"ALL","section":"数据分析","data_source":p.name,"main_message":"展示数值变量相关结构，辅助变量筛选。","used_in_paper":"待定","quality_score":"4.2"}); idx+=1
    if rows:
        fields=["figure_id","path","title","question_id","section","data_source","main_message","used_in_paper","quality_score"]
        with REG.open("w",encoding="utf-8-sig",newline="") as f: w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"[OK] EDA figures generated: {len(rows)}")
if __name__=="__main__": main()

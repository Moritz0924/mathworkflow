# data_analysis / ChatGPT

## 结果
基于Codex验证的数据报告完成问题拆解，指出数据能支持和不能支持的建模结论。

## 边界
不得修改统计量或把EDA相关性写成因果关系；模型选择留给下一阶段。

## 交付
给出子问题依赖、变量角色、数据限制、评价指标候选及后续建模所需证据。

## 验收
所有数据判断引用交接包中的字段、统计或图表，且明确缺失值和异常值影响。

## 阻塞
数据报告与题面口径冲突、样本不足或关键字段无法解释时提出修订请求。

## Response metadata

Begin the response with this exact metadata block:

---
protocol: mmwf-handoff/v1
project_id: ccmc2025-a
stage: data_analysis
handoff_id: H-4709302CC4F4
context_sha256: 5c588472fb675356b4d656f153cf75f9476e4c6b14f280027902cfab5a4dec0f
---

## Verified context

## `00_problem/attachments_overview.md`

# 附件总览（经原始文件核验）

## 题目文件

| 文件 | 类型 | 状态 | 说明 |
|---|---|---|---|
| A题.pdf | .pdf | 已验证可读（PDF-1.7，286,520 bytes） | 赛题原文；可提取 1 页文本 |

## 数据文件

| 文件 | 类型 | 路径 | 说明 |
|---|---|---|---|
| result1.xlsx | .xlsx | 03_data/raw/result1.xlsx | 问题三结果模板：FY1 三枚干扰弹参数（运动方向、速度、投放点坐标、起爆点坐标、有效干扰时长） |
| result2.xlsx | .xlsx | 03_data/raw/result2.xlsx | 问题四结果模板：FY1/FY2/FY3 协同干扰参数 |
| result3.xlsx | .xlsx | 03_data/raw/result3.xlsx | 问题五结果模板：全编队五机三弹协同分配参数（含所干扰导弹编号） |

## 先验数据库

| 目录 | 说明 |
|---|---|
| 13_prior_db/ | 已构建结构化先验数据库（含 TF-IDF 全文索引、检索结果、论文卡片） |
| 论文数据集/ | 原始论文 PDF 集合（按建模方法分类：线性规划、神经网络等38类） |


## `00_problem/contest_info.yaml`

contest:
  name: "高教社杯全国大学生数学建模竞赛"
  year: 2025
  problem_id: "A"
  problem_title: "烟幕干扰弹的投放策略"
  source_file: "00_problem/inbox/A题.pdf"
  start_time: ""
  end_time: ""
  total_hours: 72
  current_time: ""

team:
  team_id: ""
  members:
    - name: ""
      role: ""
      responsibility: []

ai_policy:
  require_ai_log: true
  require_paper_anchor: true
  require_ai_usage_detail_pdf: true
  ai_superscript_format: "^{AI-xx}"


## `00_problem/problem_statement.md`

# 赛题原文摘要（经 A题.pdf 核验）

## 来源与适用范围

- 来源：`00_problem/inbox/A题.pdf`，2025 年高教社杯全国大学生数学建模竞赛 A 题。
- 题名：**烟幕干扰弹的投放策略**。
- 本文件是用于工作流交接的事实摘要；以原始 PDF 为最高优先级，不替代 PDF。

## 背景与目标

无人机受领任务后投放烟幕干扰弹，在来袭空地导弹与真目标之间形成烟幕遮蔽。需针对五种场景设计无人机航向、速度、烟幕弹投放点和起爆点，使对真目标的有效遮蔽时间尽可能长；不同烟幕弹形成的遮蔽区间可以不连续。

## 空间与运动参数

### 坐标与目标

- 假目标为坐标原点，水平面为 x-y 平面，z 轴表示高度。
- 真目标是半径 7 m、高 10 m 的圆柱体；其下底面圆心为 `(0, 200, 0)`。
- 三枚来袭导弹均以 300 m/s 匀速直线飞向假目标（原点）。

| 导弹 | 初始坐标 (m) |
|---|---|
| M1 | (20000, 0, 2000) |
| M2 | (19000, 600, 2100) |
| M3 | (18000, -600, 1900) |

| 无人机 | 初始坐标 (m) |
|---|---|
| FY1 | (17800, 0, 1800) |
| FY2 | (12000, 1400, 1400) |
| FY3 | (6000, -3000, 700) |
| FY4 | (11000, 2000, 1800) |
| FY5 | (13000, -2000, 1300) |

### 无人机约束

- 受领任务后可瞬时调整一次飞行方向。
- 以 70–140 m/s 的速度等高度、匀速、直线飞行。
- 各机航向与速度可以不同，但一旦确定不得再次调整。
- 结果模板中航向角以 x 轴正向为 0°，逆时针为正，取值范围为 `[0°, 360°)`。

### 烟幕干扰弹与烟幕云团

- 同一无人机任意两枚干扰弹的投放时间间隔不得小于 1 s。
- 干扰弹脱离无人机后仅受重力作用运动；其初始速度继承方式、重力常数及起爆时序范围需在建模阶段显式登记。
- 起爆后瞬时形成球状烟幕云团，云团中心以 3 m/s 匀速下沉。
- 起爆后 20 s 内，云团中心 10 m 范围为有效烟幕区域。

## 五个问题

### 问题 1：固定单机单弹情形

FY1 以 120 m/s 朝假目标方向飞行；受领任务 1.5 s 后投放一枚烟幕干扰弹，投放后 3.6 s 起爆。计算其对 M1 的有效遮蔽时长。

### 问题 2：单机单弹优化

利用 FY1 对 M1 投放一枚烟幕干扰弹，确定 FY1 飞行方向、飞行速度、投放点和起爆点，使遮蔽时间尽可能长。

### 问题 3：单机三弹协同

利用 FY1 投放三枚烟幕干扰弹对 M1 实施干扰，给出投放策略，并将结果填写到 `03_data/raw/result1.xlsx`。

### 问题 4：三机各一弹协同

利用 FY1、FY2、FY3 三架无人机，各投放一枚烟幕干扰弹对 M1 实施干扰，给出策略，并将结果填写到 `03_data/raw/result2.xlsx`。

### 问题 5：五机多弹多目标协同

利用 FY1–FY5 五架无人机，每架至多投放三枚烟幕干扰弹，对 M1–M3 实施干扰；给出策略，并将结果填写到 `03_data/raw/result3.xlsx`。

## 待在后续阶段明确的建模口径

题面给出了烟幕云团和真目标的几何参数，但未用公式定义“有效遮蔽”判据。后续须明确：

1. 导弹—真目标视线与烟幕球相交的判定，以及真目标圆柱体的几何表示；
2. 干扰弹释放瞬间的初速度继承、重力常数、起爆是否受地面边界限制；
3. 多枚干扰弹对同一导弹的遮蔽时长是否按时间并集计量；
4. 问题 5 多导弹遮蔽时间的聚合目标。

## 结果与审计要求

- Q3、Q4、Q5 分别使用 `result1.xlsx`、`result2.xlsx`、`result3.xlsx` 模板。
- 所有后续数值结果必须登记到 `14_contracts/result_contract.csv`；公式、图表和论断也必须先登记对应合同。


## `03_data/cleaning_rules.md`

# 数据清洗规则

| 规则编号 | 字段 | 问题 | 处理方式 | 是否影响主结果 | 记录文件 |
|---|---|---|---|---|---|
| CR001 | 无人机运动速度 (m/s) | 超出 70~140 m/s 范围 | 标记异常，人工确认 | 是 | processed/cleaning_log.csv |
| CR002 | 无人机运动方向 | 超出 0~360 度范围 | 归化到 [0, 360) | 否 | processed/cleaning_log.csv |
| CR003 | 有效干扰时长 (s) | 非正值 | 标记异常，阻塞结果冻结 | 是 | processed/cleaning_log.csv |
| CR004 | 坐标字段 | 非数值 | 标记异常，回退校验 | 是 | processed/cleaning_log.csv |

## 原始数据保留原则

- 原始数据 `03_data/raw/` 不得覆盖。
- 清洗数据写入 `03_data/processed/`。
- 清洗前后差异必须可追溯。


## `03_data/data_dictionary.csv`

file_name,column_name,inferred_type,missing_rate,unique_count,sample_values,possible_meaning,risk_note
result1.xlsx,无人机运动方向,numeric,high,?,?,无人机飞行方向角（以x轴为正向逆时针0~360度）,需人工填写
result1.xlsx,无人机运动速度 (m/s),numeric,high,?,?,无人机飞行速度（70~140 m/s）,需人工填写
result1.xlsx,烟幕干扰弹编号,integer,0,3,"1,2,3",三枚干扰弹的序号,主键
result1.xlsx,烟幕干扰弹投放点的x坐标 (m),numeric,high,?,?,投放时刻弹体空间x坐标,需建模计算
result1.xlsx,烟幕干扰弹投放点的y坐标 (m),numeric,high,?,?,投放时刻弹体空间y坐标,需建模计算
result1.xlsx,烟幕干扰弹投放点的z坐标 (m),numeric,high,?,?,投放时刻弹体空间z坐标,需建模计算
result1.xlsx,烟幕干扰弹起爆点的x坐标 (m),numeric,high,?,?,起爆时刻弹体空间x坐标,需建模计算
result1.xlsx,烟幕干扰弹起爆点的y坐标 (m),numeric,high,?,?,起爆时刻弹体空间y坐标,需建模计算
result1.xlsx,烟幕干扰弹起爆点的z坐标 (m),numeric,high,?,?,起爆时刻弹体空间z坐标,需建模计算
result1.xlsx,有效干扰时长 (s),numeric,high,?,?,干扰弹起爆后有效干扰的持续时间,需建模计算
result2.xlsx,无人机编号,categorical,0,3,"FY1,FY2,FY3",无人机标识,主键
result2.xlsx,无人机运动方向,numeric,high,?,?,无人机飞行方向角,需人工/计算填写
result2.xlsx,无人机运动速度 (m/s),numeric,high,?,?,无人机飞行速度,需人工/计算填写
result2.xlsx,烟幕干扰弹投放点的x坐标 (m),numeric,high,?,?,投放点x坐标,需建模计算
result2.xlsx,烟幕干扰弹投放点的y坐标 (m),numeric,high,?,?,投放点y坐标,需建模计算
result2.xlsx,烟幕干扰弹投放点的z坐标 (m),numeric,high,?,?,投放点z坐标,需建模计算
result2.xlsx,烟幕干扰弹起爆点的x坐标 (m),numeric,high,?,?,起爆点x坐标,需建模计算
result2.xlsx,烟幕干扰弹起爆点的y坐标 (m),numeric,high,?,?,起爆点y坐标,需建模计算
result2.xlsx,烟幕干扰弹起爆点的z坐标 (m),numeric,high,?,?,起爆点z坐标,需建模计算
result2.xlsx,有效干扰时长 (s),numeric,high,?,?,有效干扰的持续时间,需建模计算
result3.xlsx,无人机编号,categorical,0,5,"FY1,FY2,FY3,FY4,FY5",无人机标识,主键
result3.xlsx,无人机运动方向,numeric,high,?,?,无人机飞行方向角,需人工/计算填写
result3.xlsx,无人机运动速度 (m/s),numeric,high,?,?,无人机飞行速度,需人工/计算填写
result3.xlsx,烟幕干扰弹编号,integer,0,3,"1,2,3",三枚干扰弹的序号,主键
result3.xlsx,烟幕干扰弹投放点的x坐标 (m),numeric,high,?,?,投放点x坐标,需建模计算
result3.xlsx,烟幕干扰弹投放点的y坐标 (m),numeric,high,?,?,投放点y坐标,需建模计算
result3.xlsx,烟幕干扰弹投放点的z坐标 (m),numeric,high,?,?,投放点z坐标,需建模计算
result3.xlsx,烟幕干扰弹起爆点的x坐标 (m),numeric,high,?,?,起爆点x坐标,需建模计算
result3.xlsx,烟幕干扰弹起爆点的y坐标 (m),numeric,high,?,?,起爆点y坐标,需建模计算
result3.xlsx,烟幕干扰弹起爆点的z坐标 (m),numeric,high,?,?,起爆点z坐标,需建模计算
result3.xlsx,有效干扰时长 (s),numeric,high,?,?,有效干扰的持续时间,需建模计算
result3.xlsx,干扰的导弹编号,categorical,high,3,"M1,M2,M3",该弹负责干扰的目标导弹编号,需分配决策


## `03_data/data_quality_report.md`

# 数据质量报告

本报告由 v4 工作流生成，字段含义和异常处理仍需人工确认。

## result1.xlsx

- 行数：6（含表头1行 + 空行1行 + 注释1行），有效数据行 3 行
- 已填入字段：烟幕干扰弹编号（1, 2, 3）
- 待计算字段：运动方向、速度、投放点坐标、起爆点坐标、有效干扰时长

## result2.xlsx

- 行数：6（含表头1行 + 空行1行 + 注释1行），有效数据行 3 行
- 已填入字段：无人机编号（FY1, FY2, FY3）
- 待计算字段：运动方向、速度、投放点坐标、起爆点坐标、有效干扰时长

## result3.xlsx

- 行数：18（含表头1行 + 空行1行 + 注释1行），有效数据行 15 行（5机 × 3弹）
- 已填入字段：无人机编号（FY1~FY5）、烟幕干扰弹编号（1, 2, 3）
- 待计算字段：运动方向、速度、投放点坐标、起爆点坐标、有效干扰时长、干扰的导弹编号


## `03_data/data_quality_report.tex`

\section{数据预处理与数据质量诊断}

本节由自动数据质量检查生成，字段含义和异常处理仍需人工确认。



## `03_data/input_decision_table.csv`

input_id,field_name,source_file,question,model,decision,reason,risk_level,fallback,notes
IN01,导弹初始位置,00_problem/problem_statement.md,Q1-Q5,全问,采用题面给定坐标,题面硬数据不可改,低,,M1/M2/M3 坐标
IN02,无人机初始位置,00_problem/problem_statement.md,全问,全问,采用题面给定坐标,题面硬数据不可改,低,,FY1~FY5 坐标
IN03,导弹速度,00_problem/problem_statement.md,全问,全问,300 m/s 恒定,题面给定,低,,
IN04,无人机速度范围,00_problem/problem_statement.md,全问,全问,70~140 m/s 约束,题面给定,低,,
IN05,干扰弹起爆延迟,00_problem/problem_statement.md,Q1-Q2,单弹模型,1.5 s,题面给定,低,,
IN06,烟幕形成时间,00_problem/problem_statement.md,Q1-Q2,单弹模型,3.6 s,题面给定,低,,


## `04_eda_code/eda_visuals.py`

from __future__ import annotations
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/"03_data/raw"; FIG=ROOT/"08_figures/output"; REG=ROOT/"08_figures/figure_registry.csv"
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
        if num.shape[1]>=2:
            corr=num.corr(numeric_only=True); fig,ax=plt.subplots(figsize=(8,6),dpi=160); im=ax.imshow(corr,cmap="viridis",vmin=-1,vmax=1)
            ax.set_xticks(range(len(corr.columns)),labels=[str(c) for c in corr.columns],rotation=45,ha="right",fontsize=8); ax.set_yticks(range(len(corr.index)),labels=[str(c) for c in corr.index],fontsize=8); ax.set_title(f"{p.stem} 数值变量相关性热力图",fontsize=12,fontweight="bold"); fig.colorbar(im,ax=ax); fig.tight_layout()
            out=FIG/f"eda_{p.stem}_corr_heatmap.png"; fig.savefig(out,bbox_inches="tight"); plt.close(fig)
            rows.append({"figure_id":f"EDA{idx}","path":str(out.relative_to(ROOT)),"title":f"{p.stem} 数值变量相关性热力图","question_id":"ALL","section":"数据分析","data_source":p.name,"main_message":"展示数值变量相关结构，辅助变量筛选。","used_in_paper":"待定","quality_score":"4.2"}); idx+=1
    if rows:
        fields=["figure_id","path","title","question_id","section","data_source","main_message","used_in_paper","quality_score"]
        with REG.open("w",encoding="utf-8-sig",newline="") as f: w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"[OK] EDA figures generated: {len(rows)}")
if __name__=="__main__": main()


## `04_eda_code/generate_data_dictionary.py`

from __future__ import annotations
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/"03_data/raw"; OUT=ROOT/"03_data/data_dictionary.csv"
def read_table(path):
    try:
        import pandas as pd
        if path.suffix.lower() in {".xlsx",".xls"}: return pd.read_excel(path)
        if path.suffix.lower() in {".csv",".tsv"}: return pd.read_csv(path, sep="\t" if path.suffix.lower()==".tsv" else None, engine="python")
        if path.suffix.lower() in {".json",".geojson"}: return pd.read_json(path)
    except Exception as e: print(f"[WARN] {path.name}: {e}")
    return None
def main():
    RAW.mkdir(parents=True, exist_ok=True); rows=[]
    for p in sorted(RAW.iterdir()):
        if not p.is_file() or p.name.startswith("."): continue
        df=read_table(p)
        if df is None:
            rows.append({"file_name":p.name,"column_name":"","inferred_type":"unsupported","missing_rate":"","unique_count":"","sample_values":"","possible_meaning":"","risk_note":"暂不支持自动读取该格式"}); continue
        for c in df.columns:
            s=df[c]; miss=float(s.isna().mean()) if len(s) else 0.0
            rows.append({"file_name":p.name,"column_name":str(c),"inferred_type":str(s.dtype),"missing_rate":f"{miss:.4f}","unique_count":int(s.nunique(dropna=True)),"sample_values":" | ".join(map(str,s.dropna().head(5).tolist())),"possible_meaning":"待人工确认","risk_note":"缺失率较高，需人工确认" if miss>0.3 else ""})
    fields=["file_name","column_name","inferred_type","missing_rate","unique_count","sample_values","possible_meaning","risk_note"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w",encoding="utf-8-sig",newline="") as f: w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"[OK] wrote {OUT.relative_to(ROOT)} ({len(rows)} rows)")
if __name__=="__main__": main()


## `04_eda_code/run_data_quality_check.py`

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


## `04_eda_code/run_eda_pipeline.py`

from __future__ import annotations
import subprocess, sys
from pathlib import Path
ROOT0=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT0/"scripts"))
from workflow_utils import ROOT, assert_stage_allowed, complete_stage
def run(script):
    p=subprocess.run([sys.executable,str(script)],cwd=str(ROOT),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT); print(p.stdout)
    if p.returncode: raise SystemExit(p.returncode)
def main(dev_debug=False):
    assert_stage_allowed("eda", dev_debug)
    run(ROOT/"04_eda_code/generate_data_dictionary.py"); run(ROOT/"04_eda_code/run_data_quality_check.py"); run(ROOT/"04_eda_code/eda_visuals.py")
    complete_stage("eda","已生成数据字典、数据质量报告和初步 EDA 图表。请完成 Gate 1 后再进入分问拆解。")
if __name__=="__main__":
    import sys; main("--dev-debug" in sys.argv)

from __future__ import annotations
import argparse, csv
from workflow_utils import ROOT, assert_stage_allowed, complete_stage
PROFILE=ROOT/"01_task_analysis/problem_model_profile.csv"; OUT_BASE=ROOT/"06_solution_code"
def read_profile(q):
    if not PROFILE.exists(): raise SystemExit("[FAIL] 缺少 problem_model_profile.csv，请先运行 task_analysis")
    with PROFILE.open("r",encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
    for r in rows:
        if (r.get("question_id") or r.get("question")) == q: return r
    raise SystemExit(f"[FAIL] 未找到 {q} 的任务画像")
def script_text(q,kind,row):
    fam=row.get("model_family","综合集成"); main=row.get("main_model","待定模型")
    if kind=="data": return f'''from pathlib import Path\nROOT=Path(__file__).resolve().parents[2]\nRAW=ROOT/"03_data/raw"; PROCESSED=ROOT/"03_data/processed"\ndef main():\n    PROCESSED.mkdir(parents=True, exist_ok=True)\n    print("[{q}] 请在此脚本中完成真实数据清洗、字段选择、单位统一和样本筛选。")\n    print("[{q}] 当前模型族：{fam}")\nif __name__=="__main__": main()\n'''
    if kind=="model": return f'''from pathlib import Path\nimport json\nROOT=Path(__file__).resolve().parents[2]; RESULTS=ROOT/"07_results"\ndef main():\n    (RESULTS/"metrics").mkdir(parents=True, exist_ok=True)\n    print("[{q}] 候选模型：{main}")\n    print("[{q}] 请实现真实建模逻辑；禁止写入虚构结果。")\n    metrics={{"question":"{q}","model_family":"{fam}","main_model":"{main}","status":"skeleton_only","note":"尚未运行真实模型"}}\n    (RESULTS/"metrics"/"{q.lower()}_metrics.json").write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding="utf-8")\nif __name__=="__main__": main()\n'''
    if kind=="eval": return f'''def main():\n    print("[{q}] 请基于真实模型输出补充评价指标、稳健性检验和误差分析。")\nif __name__=="__main__": main()\n'''
    return f'''from pathlib import Path\nROOT=Path(__file__).resolve().parents[2]; RESULTS=ROOT/"07_results"\ndef main():\n    out=RESULTS/"result_summary.tex"\n    if not out.exists(): out.write_text("% 模型结果汇总。只有真实代码输出后才能写入正式结论。\\n",encoding="utf-8")\n    print("[{q}] 请将真实结果表、指标和可引用结论导出到 07_results/。")\nif __name__=="__main__": main()\n'''
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--question",required=True); ap.add_argument("--mode",default="deep"); ap.add_argument("--dev-debug",action="store_true"); a=ap.parse_args()
    assert_stage_allowed("codegen",a.dev_debug)
    if a.question.lower()=="all" and not a.dev_debug: raise SystemExit("[FAIL] 单环节深度模式禁止 --question all")
    row=read_profile(a.question)
    if row.get("human_confirmed") not in {"是","yes","true","True","已确认"}: print("[WARN] human_confirmed 不是“是”。已生成代码骨架，但正式建模前必须人工确认模型路线。")
    qdir=OUT_BASE/a.question; qdir.mkdir(parents=True,exist_ok=True)
    for fn,kind in {f"{a.question.lower()}_data_prepare.py":"data",f"{a.question.lower()}_model.py":"model",f"{a.question.lower()}_evaluate.py":"eval",f"{a.question.lower()}_export_results.py":"export"}.items():
        p=qdir/fn
        if not p.exists(): p.write_text(script_text(a.question,kind,row),encoding="utf-8")
    (qdir/f"README_{a.question}.md").write_text(f"# {a.question} 建模代码说明\n\n- 模型族：{row.get('model_family','')}\n- 候选主模型：{row.get('main_model','')}\n- 当前文件为 v3.0 自动生成骨架。\n- 禁止在未运行真实模型时写入正式论文结果。\n",encoding="utf-8")
    complete_stage("codegen",f"已生成 {a.question} 的建模代码骨架。请运行并人工检查真实结果后确认 Gate 3。")
    print(f"[OK] generated code skeleton for {a.question}")
if __name__=="__main__": main()

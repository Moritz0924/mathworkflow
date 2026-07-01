from __future__ import annotations
import csv, re, sys
from workflow_utils import ROOT, assert_stage_allowed, complete_stage
PROBLEM=ROOT/"00_problem/problem_statement.md"; PROFILE=ROOT/"01_task_analysis/problem_model_profile.csv"; OUT_MD=ROOT/"01_task_analysis/task_decomposition.md"; OUT_TEX=ROOT/"01_task_analysis/task_decomposition.tex"; GRAPH=ROOT/"01_task_analysis/question_dependency_graph.md"
RULES=[("优化决策型","优化决策",["最优","优化","约束","规划","调度","分配","成本","收益","路径","选址"]),("数据评价型","统计评价",["评价","评估","指标","权重","排序","排名","等级","TOPSIS","熵权","层次分析"]),("预测分析型","预测回归",["预测","趋势","未来","回归","拟合","时间序列","误差","残差"]),("机理仿真型","机理仿真",["仿真","模拟","微分方程","动力学","传播","演化","状态转移","情景"]),("分类识别型","机器学习",["分类","识别","聚类","训练","测试","特征","准确率","召回率"]),("网络空间型","空间网络",["空间","地图","经纬度","网络","节点","路径","拓扑","连通"])]
def split_questions(text):
    if not text.strip(): return [("Q1","未读取到题目文本，请人工补充。")]
    parts=re.split(r'(?=问题\s*[一二三四五六七八九十0-9]+|第\s*[一二三四五六七八九十0-9]+\s*问|任务\s*[一二三四五六七八九十0-9]+)',text)
    parts=[p.strip() for p in parts if len(p.strip())>20]
    if len(parts)<=1:
        paras=[p.strip() for p in re.split(r'\n\s*\n+', text) if p.strip()]
        parts=[p for p in paras if re.search(r'建立|求解|分析|预测|评价|优化|给出|设计',p)] or [text[:1500]]
    return [(f"Q{i}",p[:1200]) for i,p in enumerate(parts[:6],1)]
def classify(text):
    scores=[]
    for ptype,family,kws in RULES:
        hit=[kw for kw in kws if kw.lower() in text.lower()]; scores.append((len(hit),ptype,family,hit))
    scores.sort(reverse=True)
    if scores[0][0]==0: return "综合开放型","综合集成","待定","关键词不足，需人工复核"
    _,ptype,family,hit=scores[0]
    main={"优化决策":"规划模型/启发式算法","统计评价":"熵权-TOPSIS/AHP","预测回归":"回归/时间序列模型","机理仿真":"微分方程/仿真模型","机器学习":"随机森林/聚类/分类模型","空间网络":"空间统计/网络模型"}.get(family,"综合集成模型")
    return ptype,family,main,"命中关键词："+"、".join(hit[:8])
def main(dev_debug=False):
    assert_stage_allowed("task_analysis",dev_debug)
    text=PROBLEM.read_text(encoding="utf-8",errors="ignore") if PROBLEM.exists() else ""; qs=split_questions(text)
    rows=[]; md=["# 分问拆解与任务画像","","本文件由 v3.0 工作流自动生成，需人工复核。",""]; tex=["\\section{问题分析}","","本文首先对赛题进行分问拆解。以下内容由工作流自动生成，具体任务边界仍需人工复核。",""]
    for q,body in qs:
        ptype,family,main,note=classify(body)
        rows.append({"question_id":q,"question":q,"problem_type":ptype,"model_family":family,"main_model":main,"data_feature":"待结合数据字典确认","output_goal":"待人工确认","input_data":"待匹配附件","core_variables":"待识别","evaluation_metric":"待定","risk_level":"中","human_confirmed":"否","notes":note})
        md += [f"## {q}","",f"- 初步题型：{ptype}",f"- 初步模型族：{family}",f"- 候选主模型：{main}",f"- 判断依据：{note}","","### 题目片段","",body,""]
        tex += [f"\\subsection{{{q} 任务分析}}",f"该问题初步判断为{ptype}，候选模型族为{family}。候选主模型为{main}。该判断仍需结合数据字段和题目约束进行人工复核。",""]
    PROFILE.parent.mkdir(parents=True,exist_ok=True); fields=list(rows[0].keys()) if rows else ["question_id","question","problem_type","model_family","human_confirmed"]
    with PROFILE.open("w",encoding="utf-8-sig",newline="") as f: w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    OUT_MD.write_text("\n".join(md)+"\n",encoding="utf-8"); OUT_TEX.write_text("\n".join(tex)+"\n",encoding="utf-8"); GRAPH.write_text("# 问题依赖关系\n\n- 默认假设各问相对独立；若后续结果显示存在递进关系，请人工修改。\n",encoding="utf-8")
    complete_stage("task_analysis","已生成分问拆解、任务画像表和问题依赖关系草稿。")
    print(f"[OK] wrote {PROFILE.relative_to(ROOT)}")
if __name__=="__main__": main("--dev-debug" in sys.argv)

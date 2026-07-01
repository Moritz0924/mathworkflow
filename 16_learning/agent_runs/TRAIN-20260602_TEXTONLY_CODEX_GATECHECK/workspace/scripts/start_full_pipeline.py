from __future__ import annotations
import argparse
from workflow_utils import ROOT, assert_stage_allowed, read_state, run_python
SCRIPT_MAP = {
 "latex_template": ROOT/"scripts/generate_latex_template.py",
 "intake": ROOT/"scripts/start_from_inputs.py",
 "eda": ROOT/"04_eda_code/run_eda_pipeline.py",
 "task_analysis": ROOT/"scripts/decompose_problem.py",
 "prior_retrieval": ROOT/"scripts/retrieve_prior_cards.py",
 "model_route": ROOT/"scripts/route_weight_config.py",
 "codegen": ROOT/"scripts/generate_model_code.py",
 "figures": ROOT/"scripts/check_figure_quality.py",
 "paper_draft": ROOT/"scripts/generate_paper_sections.py",
 "paper_full": ROOT/"scripts/generate_paper_sections.py",
 "polish": ROOT/"scripts/polish_latex_sections.py",
 "compile": ROOT/"scripts/compile_latex.py",
}
def main():
    ap=argparse.ArgumentParser(description="v3.0 全流程入口，默认单环节深度模式")
    ap.add_argument("--mode", default="deep", choices=["deep"]); ap.add_argument("--stage", default="current")
    ap.add_argument("--question", default="Q1"); ap.add_argument("--section", default="current"); ap.add_argument("--dev-debug", action="store_true")
    a=ap.parse_args()
    if a.stage == "all" and not a.dev_debug: raise SystemExit("[FAIL] 正式模式禁止 --stage all")
    stage = read_state().get("current_stage") if a.stage == "current" else a.stage
    if stage not in SCRIPT_MAP: raise SystemExit(f"[FAIL] 未知阶段：{stage}")
    assert_stage_allowed(stage, a.dev_debug)
    args=[]
    if stage == "codegen": args += ["--question", a.question, "--mode", "deep"]
    if stage in {"paper_draft","paper_full","polish"}: args += ["--section", a.section, "--mode", "deep"]
    if a.dev_debug: args.append("--dev-debug")
    raise SystemExit(run_python(SCRIPT_MAP[stage], args))
if __name__ == "__main__": main()

from pathlib import Path
import py_compile
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "AGENTS.md",
    "config/execution_policy.yaml",
    "config/skill_enhancement.yaml",
    "config/contract_policy.yaml",
    "config/iteration_policy.yaml",
    "config/prior_db_policy.yaml",
    "config/learning_policy.yaml",
    "config/agent_mode_policy.yaml",
    "14_contracts/claim_evidence_map.csv",
    "14_contracts/result_contract.csv",
    "14_contracts/figure_contract.csv",
    "14_contracts/formula_contract.csv",
    "14_contracts/citation_contract.csv",
    "14_contracts/artifact_freeze_registry.csv",
    "14_contracts/polish_diff_check.csv",
    "14_contracts/revision_tasks.csv",
]
python_files = [
    "scripts/workflow_utils.py",
    "scripts/run_current_stage.py",
    "scripts/start_full_pipeline.py",
    "scripts/start_dashboard.py",
    "scripts/validate_contracts.py",
    "scripts/check_gates.py",
    "scripts/generate_paper_sections.py",
    "scripts/polish_latex_sections.py",
    "scripts/check_figure_quality.py",
    "scripts/learning_utils.py",
    "scripts/build_prior_corpus.py",
    "scripts/build_prior_cards.py",
    "scripts/build_prior_index.py",
    "scripts/retrieve_prior_cards.py",
    "scripts/check_prior_copy_risk.py",
    "scripts/train_workflow_scorers.py",
    "scripts/optimize_workflow_policy.py",
    "scripts/agent_mode_utils.py",
    "scripts/run_agent_mode.py",
    "scripts/benchmark_agent_run.py",
    "scripts/validate_agent_run.py",
]
missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    print("[FAIL] Missing required files:")
    for item in missing:
        print("  -", item)
    sys.exit(1)
for rel in python_files:
    py_compile.compile(str(ROOT / rel), doraise=True)
print("[PASS] v3.2-MVP export structure and Python syntax look OK.")

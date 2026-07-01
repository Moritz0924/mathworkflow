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

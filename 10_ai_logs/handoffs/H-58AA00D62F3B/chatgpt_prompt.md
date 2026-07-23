# result_freeze / ChatGPT

## 结果
只解释Codex已经验证的结果，说明它们回答了什么、没有回答什么以及残余不确定性。

## 边界
不得修改数值、单位、模型标签、置信区间或冻结状态，不得从未冻结输出推导结论。

## 交付
给出按子问题组织的结果含义、比较、局限、敏感性解释和可用于论文的候选论断。

## 验收
每个数字可映射到结果合同，解释方向与验证输出一致，并明确不确定性。

## 阻塞
结果冲突、单位不一致、敏感性改变结论或合同缺行时停止解释并请求Codex复核。

## Response metadata

Begin the response with this exact metadata block:

---
protocol: mmwf-handoff/v1
project_id: ccmc2025-a
stage: result_freeze
handoff_id: H-58AA00D62F3B
context_sha256: 00bf0013ea3195a5fa126a2fd1e06bf511e73641990d6d24931b9b5718f9abae
---

## Verified context

## `05_model/assumptions.csv`

assumption_id,content,source,applies_to,risk_level,validation_or_sensitivity,confirmation_status,notes
A01,导弹视为质点并在到达假目标原点前保持题面给定的匀速直线运动,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,低,与题面初始位置和到达时刻核对,human_confirmed,model_freeze_gate 于 2026-07-22T09:48:20+00:00 确认
A02,无人机在t=0瞬时完成一次转向后保持固定水平航向和恒定高度飞行,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,低,检查航向速度在同机各弹记录中一致,human_confirmed,model_freeze_gate 于 2026-07-22T09:48:20+00:00 确认
A03,干扰弹释放瞬间继承无人机水平速度且初始竖直速度为0,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,中,与不继承水平速度的替代口径比较,human_confirmed,model_freeze_gate 于 2026-07-22T09:48:20+00:00 确认
A04,起爆前忽略空气阻力并取重力加速度g=9.8 m/s²,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,中,比较g=9.8与g=9.81并记录差异,human_confirmed,model_freeze_gate 于 2026-07-22T09:48:20+00:00 确认
A05,起爆后烟幕不保留水平速度且不受风影响，仅以3 m/s竖直下沉,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,中,检查烟幕中心轨迹和风场缺失的影响,human_confirmed,model_freeze_gate 于 2026-07-22T09:48:20+00:00 确认
A06,干扰弹只允许在地面以上起爆，即起爆高度z≥0,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,中,验证延迟不超过由高度导出的物理上界,human_confirmed,model_freeze_gate 于 2026-07-22T09:48:20+00:00 确认
A07,烟幕中心到达地面后停止计入有效遮蔽,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,中,与中心停留地面的替代口径比较,human_confirmed,model_freeze_gate 于 2026-07-22T09:48:20+00:00 确认
A08,主模型以全部圆柱代表点均被遮挡作为有效遮蔽判据,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,高,与中心点和覆盖比例口径作敏感性分析,human_confirmed,model_freeze_gate 于 2026-07-22T09:48:20+00:00 确认
A09,同一导弹受到多枚烟幕的有效时长按时间区间并集计算且不重复累计,ChatGPT模型设计 H-21D19FE5FD2C,Q3-Q5,中,构造重叠区间单元测试,human_confirmed,model_freeze_gate 于 2026-07-22T09:48:20+00:00 确认
A10,Q5中每一枚已使用干扰弹登记一个主目标导弹编号,ChatGPT模型设计 H-21D19FE5FD2C,Q5,中,检查结果3模板的目标编号字段,human_confirmed,model_freeze_gate 于 2026-07-22T09:48:20+00:00 确认
A11,Q5按先总遮蔽时长后最短导弹遮蔽时长的字典序目标优化,ChatGPT模型设计 H-21D19FE5FD2C,Q5,高,与公平性优先的备选目标比较,human_confirmed,model_freeze_gate 于 2026-07-22T09:48:20+00:00 确认
A12,Q5要求M1/M2/M3均至少分配一枚产生正有效时长的已使用干扰弹,ChatGPT模型设计 H-21D19FE5FD2C,Q5,高,检查每枚导弹的T_j>0并做取消约束对照,human_confirmed,model_freeze_gate 于 2026-07-22T09:48:20+00:00 确认
A13,未使用弹位在内部数据中标记is_used=0且最终模板默认留空,ChatGPT模型设计 H-21D19FE5FD2C,Q5,中,检查未使用行不输出伪坐标或负值,human_confirmed,model_freeze_gate 于 2026-07-22T09:48:20+00:00 确认


## `05_model/implementation_contract.md`

# 实现交接合同（模型已冻结）

## 边界

本文件把已导入的模型设计映射到仓库目录。控制器已记录 `model_freeze_gate` 的人工确认，因此正式实现写入 `06_code/`；候选数值结果仍不得视为 `result_freeze` 的正式结论。

## 计划模块

| 模块 | 职责 | 关键验收 |
|---|---|---|
| `constants.py` / `entities.py` | 题面常数、导弹、无人机、炸弹计划数据结构 | 单位和 ID 与题面、模板一致 |
| `dynamics.py` | 导弹、无人机、干扰弹、烟幕中心位置 | Q1 固定参数回归；起爆高度和时间边界 |
| `target_geometry.py` | 圆柱体代表点集及加密方案 | 代表点数和加密结果可复现 |
| `occlusion.py` | 视线投影参数、垂距、全代表点判据 | 视线前后、相切、越界的单元测试 |
| `intervals.py` | 有效区间定位、合并及长度计算 | 重叠、相邻、空区间的单元测试 |
| `constraints.py` / `validators.py` | 速度、起爆高度、投放间隔、Q5 分配和空行规则 | 每条约束均有拒绝用例 |
| `q1_evaluator.py` 至 `q5_solver.py` | 分问评估与优化入口 | Q1 无优化；Q2–Q5 先给可行解再作收敛与稳定性检查 |
| `exporters.py` | 内部结果合同与三份 Excel 模板映射 | 写入前从结果合同复算字段 |

## 数值配置的冻结规则

- 初始时间扫描步长、根求解容差、代表点密度、随机种子和最大评估次数均暂不设正式数值。
- 实施阶段须记录加密/收敛试验，再将通过验证的数值写入配置；不得凭经验在本阶段伪造。
- 主模型要同中心点、固定时间步和逐弹贪心基线比较，但基线不替代主模型结论。

## 本地依赖检查（2026-07-22）

- 可用：NumPy 2.0.2、SciPy 1.13.1、Pandas 2.3.3、OpenPyXL 3.1.5、PyYAML 6.0.3。
- SciPy 的差分进化和 Powell 实现用于冻结路线指定的连续全局搜索与局部精修；任何改用不同类别求解器的建议，仍须判断其是否改变已冻结目标或约束。


## `05_model/model_route.md`

# 模型路线登记（已人工冻结）

## 来源与状态

- 决策来源：`10_ai_logs/handoffs/H-21D19FE5FD2C/chatgpt_response.md`。
- 本文件仅将 ChatGPT 的模型设计转写为本地可审计工件；不代表任何数值结果。
- 人工确认记录：控制器已在 `2026-07-22T09:48:20+00:00` 记录 `model_freeze_gate`。该记录来自 `workflow_state.yaml` 的 `human_gate_confirmed` 事件；本文件只同步该控制器事实。

## 主路线

采用“**三维确定性运动学—圆柱目标多视线遮挡—连续时间区间并集—分层混合优化**”路线：

1. 以三维匀速直线运动描述导弹和无人机，以无阻力抛体运动描述起爆前干扰弹，以竖直下沉描述起爆后烟幕中心；
2. 将半径 7 m、高 10 m 的真目标保留为圆柱体，并用确定性代表点集近似其几何；
3. 只有烟幕球同时遮挡全部代表点对应的导弹—目标视线时，才计为有效遮蔽；
4. 对同一导弹的多枚烟幕遮蔽区间求并集，重叠部分不重复累计；
5. Q2–Q4 使用连续黑箱全局搜索加局部精修；Q5 先做离散任务分配，再优化连续飞行和投放参数。

## 各问目标与输出边界

| 问题 | 决策/计算 | 评价目标 |
|---|---|---|
| Q1 | 使用题面给定 FY1 航向、120 m/s、投放时刻 1.5 s、起爆延迟 3.6 s | 计算对 M1 的实际有效遮蔽时长，不优化 |
| Q2 | FY1 的航向、速度、投放时刻和起爆延迟 | 最大化单弹对 M1 的有效遮蔽时长 |
| Q3 | FY1 的固定航向/速度及 3 枚弹的时序 | 最大化 M1 的遮蔽区间并集长度 |
| Q4 | FY1–FY3 各自的航向、速度、投放时刻和起爆延迟 | 最大化 M1 的遮蔽区间并集长度 |
| Q5 | FY1–FY5 每架至多 3 枚弹的使用、主目标分配和连续参数 | 先最大化 M1–M3 总遮蔽时长，再最大化三者最短遮蔽时长 |

## 约束与待冻结假设

- 题面硬约束：无人机速度为 70–140 m/s；飞行高度不变；同机相邻投放间隔至少 1 s；烟幕半径 10 m、物理有效期 20 s、中心下沉速度 3 m/s。
- 公式登记见 `14_contracts/formula_contract.csv`；全部假设及其风险见 `05_model/assumptions.csv`。
- A08（全代表点遮挡）、A11（Q5 字典序目标）和 A12（三枚导弹均须获得正遮蔽）为高风险建模口径，已随 `model_freeze_gate` 冻结；任何改动均须进入模型修订流程。

## 已冻结的实施口径

1. 干扰弹继承无人机水平速度，忽略空气阻力，取 `g=9.8 m/s²`；
2. 烟幕中心到达地面后立即停止计入有效遮蔽；
3. 主模型使用全圆柱代表点遮挡口径；中心点和覆盖比例仅可作已登记的基线/敏感性对照；
4. 多弹遮蔽按时间区间并集统计；
5. Q5 先最大化总遮蔽时长，再最大化最短导弹遮蔽时长，且 M1–M3 均须有正有效遮蔽；
6. 每枚已使用干扰弹只向登记的主目标导弹贡献 Q5 正式目标；附带遮蔽仅作诊断记录；
7. 未使用弹位在内部标记 `is_used=0`，最终模板的待计算字段留空；
8. 代表点密度、时间扫描步长、求根容差和优化预算仍须通过收敛试验确定，不能凭经验虚填。

## 备选路线与触发条件

- 若全代表点口径下所有可行策略均为 0，则仅在人工批准后启用覆盖比例敏感性分析；
- 若代表点加密不收敛，则改用精确投影视锥几何方案；
- 若 Q5 总时长目标过度集中资源，比较公平性优先的备选目标；
- 以上均为已登记备选，不得由实现阶段自行切换。

## 实现可行性结论

运动学、视线距离、区间合并和模板映射均可由本地 Python 实现。建议的 `differential_evolution` 与 `Powell` 求解器通常依赖 SciPy；当前环境有 NumPy 和 OpenPyXL，但未安装 SciPy，故在 implementation 阶段开始前必须以受控依赖方式补齐 SciPy 或把等价求解器提交给 ChatGPT 重新确认。该依赖缺口不改变当前模型路线。


## `06_code/README.md`

# 代码说明

## 运行方式

```bash
pip install -r requirements.txt
python run_all.py
```

## 目录说明

- `src/`: 主模型、数据处理、绘图函数。
- `notebooks/`: 探索性分析笔记本，可选。
- `execution_log.md`: 每次运行记录。

## 结果输出约定

- 每问结果输出到 `07_results/q*_results.csv`。
- 总指标输出到 `07_results/metrics_summary.csv`。
- 结果来源映射输出到 `07_results/result_source_map.csv`。


## `06_code/execution_log.md`

# 代码执行日志

| run_id | 时间 | 命令 | 状态 | 输出文件 | 报错 | 修复 |
|---|---|---|---|---|---|---|
| RUN001 |  |  | 未运行 |  |  |  |
| RUN-20260722T102855Z | 2026-07-22T10:28:55.957614+00:00 | python 06_code/run_all.py | success | 07_results/q1_results.csv ... q5_results.csv |  | candidate run; no result freeze |
| RUN-20260722T102919Z | 2026-07-22T10:29:19.765053+00:00 | python 06_code/run_all.py | success | 07_results/q1_results.csv ... q5_results.csv |  | candidate run; no result freeze |
| RUN-20260722T103344Z | 2026-07-22T10:33:44.451958+00:00 | python 06_code/run_all.py | success | 07_results/q1_results.csv ... q5_results.csv |  | candidate run; no result freeze |
| RUN-20260722T103612Z | 2026-07-22T10:36:12.743032+00:00 | python 06_code/run_all.py | success | 07_results/q1_results.csv ... q5_results.csv |  | candidate run; no result freeze |


## `06_code/requirements.txt`

numpy==2.0.2
scipy==1.13.1
pandas==2.3.3
openpyxl==3.1.5
PyYAML==6.0.3


## `06_code/run_all.py`

from __future__ import annotations

import argparse
import csv
import importlib.metadata
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml

from src.entities import BombEvaluation, BombPlan
from src.evaluator import EvaluatorConfig, evaluate_q1
from src.exporters import export_candidate_template
from src.solvers import CandidateSolution, SolverConfig, solve_q2, solve_q3, solve_q4, solve_q5


ROOT = Path(__file__).resolve().parents[1]
CODE_ROOT = ROOT / "06_code"
DEFAULT_OUTPUT_DIR = ROOT / "07_results"
CONFIG_PATH = CODE_ROOT / "solver_config.yaml"
EXECUTION_LOG = CODE_ROOT / "execution_log.md"


def _read_config(quick: bool) -> SolverConfig:
    raw = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
    section = raw["quick" if quick else "candidate"]
    target = section["target"]
    timing = section["time_evaluation"]
    optimization = section["optimization"]
    return SolverConfig(
        evaluator=EvaluatorConfig(
            angular_samples=int(target["angular_samples"]),
            height_samples=int(target["height_samples"]),
            radial_samples=int(target["radial_samples"]),
            scan_step_s=float(timing["scan_step_s"]),
            root_tolerance_s=float(timing["root_tolerance_s"]),
        ),
        differential_evolution_maxiter=int(optimization["maxiter"]),
        differential_evolution_popsize=int(optimization["popsize"]),
        local_refinement=bool(optimization["local_refinement"]),
        random_seed=int(optimization["random_seed"]),
    )


def _as_q1_solution(evaluation: BombEvaluation) -> CandidateSolution:
    return CandidateSolution(
        question_id="Q1",
        plans=(evaluation.plan,),
        evaluations=(evaluation,),
        primary_durations_s={"M1": evaluation.effective_duration_s},
        objective=(evaluation.effective_duration_s,),
        diagnostics={"solver": "fixed_strategy_evaluation", "feasible": True},
    )


def _evaluation_map(evaluations: Iterable[BombEvaluation]) -> dict[tuple[str, int], BombEvaluation]:
    return {(evaluation.plan.uav_id, evaluation.plan.bomb_id): evaluation for evaluation in evaluations}


def _write_solution_csv(path: Path, solution: CandidateSolution) -> None:
    evaluation_by_key = _evaluation_map(solution.evaluations)
    fields = [
        "question_id",
        "uav_id",
        "bomb_id",
        "missile_id",
        "is_used",
        "heading_deg",
        "speed_mps",
        "release_time_s",
        "delay_s",
        "detonation_time_s",
        "release_x_m",
        "release_y_m",
        "release_z_m",
        "detonation_x_m",
        "detonation_y_m",
        "detonation_z_m",
        "effective_duration_s",
        "occlusion_intervals",
        "result_status",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for plan in solution.plans:
            evaluation = evaluation_by_key.get((plan.uav_id, plan.bomb_id))
            release = evaluation.release_point_xyz if evaluation else (None, None, None)
            detonation = evaluation.detonation_point_xyz if evaluation else (None, None, None)
            writer.writerow(
                {
                    "question_id": solution.question_id,
                    "uav_id": plan.uav_id,
                    "bomb_id": plan.bomb_id,
                    "missile_id": plan.missile_id or "",
                    "is_used": int(plan.is_used),
                    "heading_deg": (plan.heading_rad * 180.0 / 3.141592653589793) % 360.0 if plan.is_used else "",
                    "speed_mps": plan.speed_mps if plan.is_used else "",
                    "release_time_s": plan.release_time_s if plan.is_used else "",
                    "delay_s": plan.delay_s if plan.is_used else "",
                    "detonation_time_s": plan.detonation_time_s if plan.is_used else "",
                    "release_x_m": release[0],
                    "release_y_m": release[1],
                    "release_z_m": release[2],
                    "detonation_x_m": detonation[0],
                    "detonation_y_m": detonation[1],
                    "detonation_z_m": detonation[2],
                    "effective_duration_s": evaluation.effective_duration_s if evaluation else "",
                    "occlusion_intervals": json.dumps(evaluation.occlusion_intervals if evaluation else (), ensure_ascii=False),
                    "result_status": "candidate",
                }
            )


def _write_metrics(path: Path, solutions: Iterable[CandidateSolution]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["question_id", "metric_name", "metric_value", "unit", "result_status"])
        writer.writeheader()
        for solution in solutions:
            for missile_id, duration in solution.primary_durations_s.items():
                writer.writerow(
                    {
                        "question_id": solution.question_id,
                        "metric_name": f"primary_duration_{missile_id}",
                        "metric_value": duration,
                        "unit": "s",
                        "result_status": "candidate",
                    }
                )
            for index, value in enumerate(solution.objective, start=1):
                writer.writerow(
                    {
                        "question_id": solution.question_id,
                        "metric_name": f"objective_{index}",
                        "metric_value": value,
                        "unit": "s",
                        "result_status": "candidate",
                    }
                )


def _versions() -> dict[str, str]:
    return {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "pandas", "openpyxl", "PyYAML")}


def run_pipeline(*, quick: bool = True, output_dir: Path | None = None) -> dict[str, object]:
    output = Path(output_dir or DEFAULT_OUTPUT_DIR)
    output.mkdir(parents=True, exist_ok=True)
    config = _read_config(quick)
    solutions = [
        _as_q1_solution(evaluate_q1(config.evaluator)),
        solve_q2(config),
        solve_q3(config),
        solve_q4(config),
        solve_q5(config),
    ]
    for solution in solutions:
        _write_solution_csv(output / f"{solution.question_id.lower()}_results.csv", solution)
    _write_metrics(output / "metrics_summary.csv", solutions)
    for solution in solutions:
        if solution.question_id in {"Q3", "Q4", "Q5"}:
            template_number = {"Q3": 1, "Q4": 2, "Q5": 3}[solution.question_id]
            export_candidate_template(
                solution.question_id,
                solution.plans,
                solution.evaluations,
                output / f"result{template_number}_candidate.xlsx",
            )
    source_rows = [
        {
            "result_id": f"candidate_{solution.question_id.lower()}",
            "question_id": solution.question_id,
            "source_file": f"07_results/{solution.question_id.lower()}_results.csv",
            "result_status": "candidate",
            "generated_by": "06_code/run_all.py",
        }
        for solution in solutions
    ]
    with (output / "result_source_map.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(source_rows[0]))
        writer.writeheader()
        writer.writerows(source_rows)
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "result_status": "candidate",
        "mode": "quick" if quick else "candidate",
        "questions": [solution.question_id for solution in solutions],
        "solver_config": {
            "target": config.evaluator.__dict__,
            "differential_evolution_maxiter": config.differential_evolution_maxiter,
            "differential_evolution_popsize": config.differential_evolution_popsize,
            "local_refinement": config.local_refinement,
            "random_seed": config.random_seed,
        },
        "dependencies": _versions(),
        "q5_feasible": bool(solutions[-1].diagnostics.get("feasible")),
        "q5_diagnostics": dict(solutions[-1].diagnostics),
        "notice": "Candidate artifacts are not result-freeze outputs and are not registered in result_contract.csv.",
    }
    (output / "candidate_run_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def _append_execution_log(status: str, output: str, error: str = "") -> None:
    line = "| {run_id} | {time} | {command} | {status} | {output} | {error} | {repair} |\n".format(
        run_id=f"RUN-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        time=datetime.now(timezone.utc).isoformat(),
        command="python 06_code/run_all.py",
        status=status,
        output=output,
        error=error.replace("|", "/"),
        repair="candidate run; no result freeze",
    )
    with EXECUTION_LOG.open("a", encoding="utf-8") as handle:
        handle.write(line)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run candidate smoke-screen solver artifacts.")
    parser.add_argument("--full", action="store_true", help="Use the higher-resolution candidate configuration.")
    args = parser.parse_args()
    try:
        manifest = run_pipeline(quick=not args.full)
        _append_execution_log("success", "07_results/q1_results.csv ... q5_results.csv")
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        _append_execution_log("failed", "", str(exc))
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


## `06_code/solver_config.yaml`

physics:
  gravity_mps2: 9.8
  bomb_drag_enabled: false
  wind_enabled: false
  smoke_radius_m: 10.0
  smoke_sink_speed_mps: 3.0
  smoke_lifetime_s: 20.0
  smoke_ground_mode: terminate

quick:
  target:
    angular_samples: 6
    height_samples: 2
    radial_samples: 1
  time_evaluation:
    scan_step_s: 0.25
    root_tolerance_s: 0.00001
  optimization:
    maxiter: 1
    popsize: 3
    local_refinement: false
    random_seed: 20250722

candidate:
  target:
    angular_samples: 12
    height_samples: 3
    radial_samples: 2
  time_evaluation:
    scan_step_s: 0.1
    root_tolerance_s: 0.00001
  optimization:
    maxiter: 6
    popsize: 5
    local_refinement: true
    random_seed: 20250722


## `06_code/src/__init__.py`



## `06_code/src/constants.py`

from __future__ import annotations

from .entities import Missile, UAV


GRAVITY_MPS2 = 9.8
MISSILE_SPEED_MPS = 300.0
UAV_SPEED_MIN_MPS = 70.0
UAV_SPEED_MAX_MPS = 140.0
SMOKE_RADIUS_M = 10.0
SMOKE_SINK_SPEED_MPS = 3.0
SMOKE_LIFETIME_S = 20.0
TARGET_RADIUS_M = 7.0
TARGET_HEIGHT_M = 10.0
TARGET_BASE_CENTER = (0.0, 200.0, 0.0)
MIN_RELEASE_GAP_S = 1.0


MISSILES = {
    "M1": Missile("M1", (20000.0, 0.0, 2000.0), MISSILE_SPEED_MPS),
    "M2": Missile("M2", (19000.0, 600.0, 2100.0), MISSILE_SPEED_MPS),
    "M3": Missile("M3", (18000.0, -600.0, 1900.0), MISSILE_SPEED_MPS),
}


UAVS = {
    "FY1": UAV("FY1", (17800.0, 0.0, 1800.0)),
    "FY2": UAV("FY2", (12000.0, 1400.0, 1400.0)),
    "FY3": UAV("FY3", (6000.0, -3000.0, 700.0)),
    "FY4": UAV("FY4", (11000.0, 2000.0, 1800.0)),
    "FY5": UAV("FY5", (13000.0, -2000.0, 1300.0)),
}


## `06_code/src/constraints.py`

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from .constants import MIN_RELEASE_GAP_S, MISSILES, UAVS, UAV_SPEED_MAX_MPS, UAV_SPEED_MIN_MPS
from .dynamics import detonation_altitude, maximum_delay_s, missile_hit_time
from .entities import BombPlan


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    uav_id: str | None = None
    bomb_id: int | None = None


def validate_plans(question_id: str, plans: Iterable[BombPlan]) -> list[ValidationIssue]:
    materialized = list(plans)
    issues: list[ValidationIssue] = []
    by_uav: dict[str, list[BombPlan]] = defaultdict(list)

    for plan in materialized:
        by_uav[plan.uav_id].append(plan)
        if plan.uav_id not in UAVS:
            issues.append(ValidationIssue("unknown_uav", "无人机编号不在题面范围内", plan.uav_id, plan.bomb_id))
            continue
        if plan.is_used:
            if plan.missile_id not in MISSILES:
                issues.append(ValidationIssue("unknown_missile", "已使用弹必须有题面导弹主目标", plan.uav_id, plan.bomb_id))
            if not UAV_SPEED_MIN_MPS <= plan.speed_mps <= UAV_SPEED_MAX_MPS:
                issues.append(ValidationIssue("speed_range", "无人机速度超出70–140 m/s", plan.uav_id, plan.bomb_id))
            if not 0.0 <= plan.heading_rad < 2.0 * math.pi:
                issues.append(ValidationIssue("heading_range", "航向必须在[0, 2π)内", plan.uav_id, plan.bomb_id))
            if plan.release_time_s < 0.0:
                issues.append(ValidationIssue("release_time", "投放时刻必须非负", plan.uav_id, plan.bomb_id))
            if not 0.0 <= plan.delay_s <= maximum_delay_s(plan.uav_id):
                issues.append(ValidationIssue("delay_range", "起爆延迟不满足地面以上起爆约束", plan.uav_id, plan.bomb_id))
            elif detonation_altitude(plan) < -1e-9:
                issues.append(ValidationIssue("detonation_altitude", "起爆点位于地面以下", plan.uav_id, plan.bomb_id))
            if plan.missile_id in MISSILES and plan.detonation_time_s > missile_hit_time(plan.missile_id):
                issues.append(ValidationIssue("detonation_after_hit", "起爆时刻晚于主目标导弹命中时刻", plan.uav_id, plan.bomb_id))

    for uav_id, uav_plans in by_uav.items():
        used = sorted((plan for plan in uav_plans if plan.is_used), key=lambda plan: plan.release_time_s)
        if not used:
            continue
        reference = used[0]
        for plan in used[1:]:
            if not math.isclose(plan.heading_rad, reference.heading_rad, abs_tol=1e-12):
                issues.append(ValidationIssue("shared_heading", "同一无人机的已使用弹必须共享航向", uav_id, plan.bomb_id))
            if not math.isclose(plan.speed_mps, reference.speed_mps, abs_tol=1e-12):
                issues.append(ValidationIssue("shared_speed", "同一无人机的已使用弹必须共享速度", uav_id, plan.bomb_id))
        for previous, current in zip(used, used[1:]):
            if current.release_time_s - previous.release_time_s < MIN_RELEASE_GAP_S - 1e-12:
                issues.append(ValidationIssue("release_gap", "同一无人机相邻投放间隔小于1 s", uav_id, current.bomb_id))

    if question_id == "Q1":
        if len(materialized) != 1:
            issues.append(ValidationIssue("q1_count", "Q1必须恰有一枚干扰弹"))
        elif materialized[0].is_used:
            plan = materialized[0]
            if plan.uav_id != "FY1" or plan.missile_id != "M1":
                issues.append(ValidationIssue("q1_target", "Q1固定为FY1干扰M1", plan.uav_id, plan.bomb_id))
            if not math.isclose(plan.speed_mps, 120.0, abs_tol=1e-12):
                issues.append(ValidationIssue("q1_speed", "Q1速度固定为120 m/s", plan.uav_id, plan.bomb_id))
            if not math.isclose(plan.release_time_s, 1.5, abs_tol=1e-12) or not math.isclose(plan.delay_s, 3.6, abs_tol=1e-12):
                issues.append(ValidationIssue("q1_timing", "Q1投放和起爆延迟必须使用题面固定值", plan.uav_id, plan.bomb_id))

    if question_id == "Q3":
        if len(materialized) != 3 or any(plan.uav_id != "FY1" or plan.missile_id != "M1" for plan in materialized):
            issues.append(ValidationIssue("q3_shape", "Q3必须由FY1的三枚弹干扰M1"))

    if question_id == "Q4":
        expected = {"FY1", "FY2", "FY3"}
        if len(materialized) != 3 or {plan.uav_id for plan in materialized} != expected:
            issues.append(ValidationIssue("q4_shape", "Q4必须由FY1/FY2/FY3各投一枚弹"))

    if question_id == "Q5":
        for uav_id, uav_plans in by_uav.items():
            by_bomb_id = {plan.bomb_id: plan for plan in uav_plans}
            for bomb_id in (2, 3):
                if by_bomb_id.get(bomb_id) and by_bomb_id[bomb_id].is_used and not by_bomb_id.get(bomb_id - 1, BombPlan(uav_id, bomb_id - 1, None, False, 0, 0, 0, 0)).is_used:
                    issues.append(ValidationIssue("q5_prefix_use", "Q5弹位必须按编号前缀使用", uav_id, bomb_id))
    return issues


## `06_code/src/dynamics.py`

from __future__ import annotations

import math

import numpy as np

from .constants import (
    GRAVITY_MPS2,
    MISSILES,
    SMOKE_LIFETIME_S,
    SMOKE_SINK_SPEED_MPS,
    UAVS,
)
from .entities import BombPlan


E_Z = np.array((0.0, 0.0, 1.0), dtype=float)


def _vector(values: tuple[float, float, float]) -> np.ndarray:
    return np.asarray(values, dtype=float)


def horizontal_direction(heading_rad: float) -> np.ndarray:
    direction = np.array((math.cos(heading_rad), math.sin(heading_rad), 0.0), dtype=float)
    direction[np.abs(direction) < 1e-12] = 0.0
    return direction


def missile_hit_time(missile_id: str) -> float:
    missile = MISSILES[missile_id]
    return float(np.linalg.norm(_vector(missile.initial_position)) / missile.speed_mps)


def missile_position(missile_id: str, time_s: float) -> np.ndarray:
    missile = MISSILES[missile_id]
    initial = _vector(missile.initial_position)
    direction = -initial / np.linalg.norm(initial)
    return initial + missile.speed_mps * direction * float(time_s)


def uav_position(uav_id: str, heading_rad: float, speed_mps: float, time_s: float) -> np.ndarray:
    uav = UAVS[uav_id]
    return _vector(uav.initial_position) + float(speed_mps) * horizontal_direction(heading_rad) * float(time_s)


def release_point(plan: BombPlan) -> np.ndarray:
    return uav_position(plan.uav_id, plan.heading_rad, plan.speed_mps, plan.release_time_s)


def bomb_position_before_detonation(plan: BombPlan, time_s: float, gravity_mps2: float = GRAVITY_MPS2) -> np.ndarray:
    if time_s < plan.release_time_s:
        raise ValueError("bomb position is undefined before release")
    elapsed = float(time_s) - plan.release_time_s
    return uav_position(plan.uav_id, plan.heading_rad, plan.speed_mps, time_s) - 0.5 * gravity_mps2 * elapsed**2 * E_Z


def detonation_point(plan: BombPlan, gravity_mps2: float = GRAVITY_MPS2) -> np.ndarray:
    return bomb_position_before_detonation(plan, plan.detonation_time_s, gravity_mps2)


def detonation_altitude(plan: BombPlan, gravity_mps2: float = GRAVITY_MPS2) -> float:
    return float(detonation_point(plan, gravity_mps2)[2])


def maximum_delay_s(uav_id: str, gravity_mps2: float = GRAVITY_MPS2) -> float:
    altitude = UAVS[uav_id].initial_position[2]
    return math.sqrt(2.0 * altitude / gravity_mps2)


def smoke_center(plan: BombPlan, time_s: float, sink_speed_mps: float = SMOKE_SINK_SPEED_MPS) -> np.ndarray:
    if time_s < plan.detonation_time_s:
        raise ValueError("smoke center is undefined before detonation")
    return detonation_point(plan) - sink_speed_mps * (float(time_s) - plan.detonation_time_s) * E_Z


def smoke_valid_end_time(plan: BombPlan, missile_id: str) -> float:
    ground_time = plan.detonation_time_s + detonation_altitude(plan) / SMOKE_SINK_SPEED_MPS
    return min(plan.detonation_time_s + SMOKE_LIFETIME_S, ground_time, missile_hit_time(missile_id))


## `06_code/src/entities.py`

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


Vector3 = Tuple[float, float, float]


@dataclass(frozen=True)
class Missile:
    missile_id: str
    initial_position: Vector3
    speed_mps: float


@dataclass(frozen=True)
class UAV:
    uav_id: str
    initial_position: Vector3


@dataclass(frozen=True)
class BombPlan:
    uav_id: str
    bomb_id: int
    missile_id: Optional[str]
    is_used: bool
    heading_rad: float
    speed_mps: float
    release_time_s: float
    delay_s: float

    @property
    def detonation_time_s(self) -> float:
        return self.release_time_s + self.delay_s


@dataclass(frozen=True)
class BombEvaluation:
    plan: BombPlan
    release_point_xyz: Optional[Vector3]
    detonation_point_xyz: Optional[Vector3]
    smoke_valid_end_s: float
    occlusion_intervals: Tuple[Tuple[float, float], ...]
    effective_duration_s: float


## `06_code/src/evaluator.py`

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

from .constants import SMOKE_RADIUS_M
from .dynamics import detonation_point, missile_position, release_point, smoke_center, smoke_valid_end_time
from .entities import BombEvaluation, BombPlan
from .intervals import find_true_intervals, interval_duration
from .occlusion import is_all_points_occluded
from .target_geometry import target_sample_points


@dataclass(frozen=True)
class EvaluatorConfig:
    angular_samples: int = 12
    height_samples: int = 3
    radial_samples: int = 2
    scan_step_s: float = 0.1
    root_tolerance_s: float = 1e-5


def evaluate_plan(
    plan: BombPlan,
    missile_id: str,
    config: EvaluatorConfig,
    *,
    points: Iterable[tuple[float, float, float]] | None = None,
) -> BombEvaluation:
    if not plan.is_used:
        return BombEvaluation(plan, None, None, plan.detonation_time_s, (), 0.0)
    evaluation_points = tuple(points) if points is not None else target_sample_points(
        config.angular_samples, config.height_samples, config.radial_samples
    )
    valid_end_s = smoke_valid_end_time(plan, missile_id)
    if valid_end_s <= plan.detonation_time_s:
        intervals: list[tuple[float, float]] = []
    else:
        def is_occluded_at(time_s: float) -> bool:
            return is_all_points_occluded(
                missile_position(missile_id, time_s),
                evaluation_points,
                smoke_center(plan, time_s),
                SMOKE_RADIUS_M,
            )

        intervals = find_true_intervals(
            is_occluded_at,
            plan.detonation_time_s,
            valid_end_s,
            scan_step_s=config.scan_step_s,
            tolerance_s=config.root_tolerance_s,
        )
    release = tuple(float(value) for value in release_point(plan))
    detonation = tuple(float(value) for value in detonation_point(plan))
    return BombEvaluation(
        plan=plan,
        release_point_xyz=release,
        detonation_point_xyz=detonation,
        smoke_valid_end_s=valid_end_s,
        occlusion_intervals=tuple(intervals),
        effective_duration_s=interval_duration(intervals),
    )


def evaluate_q1(config: EvaluatorConfig) -> BombEvaluation:
    plan = BombPlan(
        uav_id="FY1",
        bomb_id=1,
        missile_id="M1",
        is_used=True,
        heading_rad=math.pi,
        speed_mps=120.0,
        release_time_s=1.5,
        delay_s=3.6,
    )
    return evaluate_plan(plan, "M1", config)


## `06_code/src/exporters.py`

from __future__ import annotations

import math
import shutil
from pathlib import Path
from typing import Iterable

from openpyxl import load_workbook

from .entities import BombEvaluation, BombPlan


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_BY_QUESTION = {
    "Q3": WORKSPACE_ROOT / "03_data" / "raw" / "result1.xlsx",
    "Q4": WORKSPACE_ROOT / "03_data" / "raw" / "result2.xlsx",
    "Q5": WORKSPACE_ROOT / "03_data" / "raw" / "result3.xlsx",
}


def _write_used_fields(
    worksheet,
    row: int,
    plan: BombPlan,
    evaluation: BombEvaluation,
    *,
    heading_column: int,
    speed_column: int,
    release_column: int,
    detonation_column: int,
    duration_column: int,
) -> None:
    release = evaluation.release_point_xyz
    detonation = evaluation.detonation_point_xyz
    if release is None or detonation is None:
        raise ValueError("used plan must have a physical evaluation")
    worksheet.cell(row, heading_column).value = math.degrees(plan.heading_rad) % 360.0
    worksheet.cell(row, speed_column).value = plan.speed_mps
    for offset, value in enumerate(release):
        worksheet.cell(row, release_column + offset).value = value
    for offset, value in enumerate(detonation):
        worksheet.cell(row, detonation_column + offset).value = value
    worksheet.cell(row, duration_column).value = evaluation.effective_duration_s


def _clear_calculated_fields(worksheet, row: int, columns: Iterable[int]) -> None:
    for column in columns:
        worksheet.cell(row, column).value = None


def export_candidate_template(
    question_id: str,
    plans: Iterable[BombPlan],
    evaluations: Iterable[BombEvaluation],
    destination: Path,
) -> Path:
    if question_id not in TEMPLATE_BY_QUESTION:
        raise ValueError("only Q3, Q4, and Q5 have official Excel templates")
    template = TEMPLATE_BY_QUESTION[question_id]
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(template, destination)
    worksheet = load_workbook(destination).active
    plan_list = list(plans)
    evaluation_by_key = {(item.plan.uav_id, item.plan.bomb_id): item for item in evaluations}

    if question_id == "Q3":
        for plan in plan_list:
            row = plan.bomb_id + 1
            if not plan.is_used:
                _clear_calculated_fields(worksheet, row, range(1, 11))
                worksheet.cell(row, 3).value = plan.bomb_id
                continue
            _write_used_fields(
                worksheet,
                row,
                plan,
                evaluation_by_key[(plan.uav_id, plan.bomb_id)],
                heading_column=1,
                speed_column=2,
                release_column=4,
                detonation_column=7,
                duration_column=10,
            )
            worksheet.cell(row, 3).value = plan.bomb_id
    elif question_id == "Q4":
        rows = {str(worksheet.cell(row, 1).value): row for row in range(2, 5)}
        for plan in plan_list:
            row = rows[plan.uav_id]
            if not plan.is_used:
                _clear_calculated_fields(worksheet, row, range(2, 11))
                continue
            _write_used_fields(
                worksheet,
                row,
                plan,
                evaluation_by_key[(plan.uav_id, plan.bomb_id)],
                heading_column=2,
                speed_column=3,
                release_column=4,
                detonation_column=7,
                duration_column=10,
            )
    else:
        rows = {
            (str(worksheet.cell(row, 1).value), int(worksheet.cell(row, 4).value)): row
            for row in range(2, 17)
        }
        for plan in plan_list:
            row = rows[(plan.uav_id, plan.bomb_id)]
            if not plan.is_used:
                _clear_calculated_fields(worksheet, row, (2, 3, 5, 6, 7, 8, 9, 10, 11, 12))
                continue
            _write_used_fields(
                worksheet,
                row,
                plan,
                evaluation_by_key[(plan.uav_id, plan.bomb_id)],
                heading_column=2,
                speed_column=3,
                release_column=5,
                detonation_column=8,
                duration_column=11,
            )
            worksheet.cell(row, 12).value = plan.missile_id

    worksheet.parent.save(destination)
    return destination


## `06_code/src/intervals.py`

from __future__ import annotations

from collections.abc import Callable, Iterable


Interval = tuple[float, float]


def _refine_transition(
    predicate: Callable[[float], bool],
    left: float,
    right: float,
    left_value: bool,
    tolerance_s: float,
) -> float:
    while right - left > tolerance_s:
        midpoint = (left + right) / 2.0
        if predicate(midpoint) == left_value:
            left = midpoint
        else:
            right = midpoint
    return (left + right) / 2.0


def find_true_intervals(
    predicate: Callable[[float], bool],
    start_s: float,
    end_s: float,
    *,
    scan_step_s: float,
    tolerance_s: float,
) -> list[Interval]:
    if end_s < start_s:
        raise ValueError("end_s must not precede start_s")
    if scan_step_s <= 0.0 or tolerance_s <= 0.0:
        raise ValueError("scan_step_s and tolerance_s must be positive")

    times = [float(start_s)]
    while times[-1] + scan_step_s < end_s:
        times.append(times[-1] + scan_step_s)
    if times[-1] != end_s:
        times.append(float(end_s))

    intervals: list[Interval] = []
    previous_time = times[0]
    previous_value = bool(predicate(previous_time))
    active_start = previous_time if previous_value else None

    for current_time in times[1:]:
        current_value = bool(predicate(current_time))
        if current_value != previous_value:
            boundary = _refine_transition(predicate, previous_time, current_time, previous_value, tolerance_s)
            if current_value:
                active_start = boundary
            elif active_start is not None:
                intervals.append((active_start, boundary))
                active_start = None
        previous_time = current_time
        previous_value = current_value

    if active_start is not None:
        intervals.append((active_start, float(end_s)))
    return intervals


def merge_intervals(intervals: Iterable[Interval], *, tolerance_s: float = 0.0) -> list[Interval]:
    ordered = sorted((float(start), float(end)) for start, end in intervals if end >= start)
    if not ordered:
        return []
    merged = [ordered[0]]
    for start, end in ordered[1:]:
        current_start, current_end = merged[-1]
        if start <= current_end + tolerance_s:
            merged[-1] = (current_start, max(current_end, end))
        else:
            merged.append((start, end))
    return merged


def interval_duration(intervals: Iterable[Interval]) -> float:
    return sum(max(0.0, end - start) for start, end in merge_intervals(intervals))


## `06_code/src/io_utils.py`

from pathlib import Path
import pandas as pd


def read_csv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def write_csv(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


## `06_code/src/occlusion.py`

from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np


def _array(values: Sequence[float]) -> np.ndarray:
    return np.asarray(values, dtype=float)


def line_of_sight_clearance(
    missile_xyz: Sequence[float],
    target_xyz: Sequence[float],
    smoke_xyz: Sequence[float],
) -> tuple[float, float]:
    missile = _array(missile_xyz)
    target = _array(target_xyz)
    smoke = _array(smoke_xyz)
    sight = target - missile
    denominator = float(np.dot(sight, sight))
    if denominator == 0.0:
        raise ValueError("target point must differ from missile position")
    relative_smoke = smoke - missile
    line_lambda = float(np.dot(relative_smoke, sight) / denominator)
    clearance = float(np.linalg.norm(relative_smoke - line_lambda * sight))
    return line_lambda, clearance


def is_all_points_occluded(
    missile_xyz: Sequence[float],
    target_points: Iterable[Sequence[float]],
    smoke_xyz: Sequence[float],
    smoke_radius_m: float,
    *,
    tolerance: float = 1e-10,
) -> bool:
    for target_xyz in target_points:
        line_lambda, clearance = line_of_sight_clearance(missile_xyz, target_xyz, smoke_xyz)
        if line_lambda < -tolerance or line_lambda > 1.0 + tolerance:
            return False
        if clearance > smoke_radius_m + tolerance:
            return False
    return True


## `06_code/src/solvers.py`

from __future__ import annotations

import math
from dataclasses import dataclass
from dataclasses import replace
from itertools import permutations
from typing import Mapping

import numpy as np
from scipy.optimize import differential_evolution, minimize

from .constants import TARGET_BASE_CENTER, TARGET_HEIGHT_M, UAVS, UAV_SPEED_MAX_MPS, UAV_SPEED_MIN_MPS
from .constraints import validate_plans
from .dynamics import maximum_delay_s, missile_hit_time, missile_position
from .entities import BombEvaluation, BombPlan
from .evaluator import EvaluatorConfig, evaluate_plan
from .intervals import interval_duration, merge_intervals


@dataclass(frozen=True)
class SolverConfig:
    evaluator: EvaluatorConfig = EvaluatorConfig()
    differential_evolution_maxiter: int = 8
    differential_evolution_popsize: int = 6
    local_refinement: bool = True
    random_seed: int = 20250701


@dataclass(frozen=True)
class CandidateSolution:
    question_id: str
    plans: tuple[BombPlan, ...]
    evaluations: tuple[BombEvaluation, ...]
    primary_durations_s: Mapping[str, float]
    objective: tuple[float, ...]
    diagnostics: Mapping[str, object]


def _candidate_plan(values: np.ndarray, uav_id: str, missile_id: str, bomb_id: int = 1) -> BombPlan:
    heading, speed, release, delay = (float(value) for value in values)
    return BombPlan(uav_id, bomb_id, missile_id, True, heading % (2.0 * math.pi), speed, release, delay)


def _single_bomb_bounds(uav_id: str, missile_id: str) -> list[tuple[float, float]]:
    return [
        (0.0, 2.0 * math.pi),
        (UAV_SPEED_MIN_MPS, UAV_SPEED_MAX_MPS),
        (0.0, missile_hit_time(missile_id)),
        (0.0, maximum_delay_s(uav_id)),
    ]


def _center_line_seed(question_id: str, uav_id: str, missile_id: str, config: SolverConfig) -> tuple[BombPlan, BombEvaluation] | None:
    uav = UAVS[uav_id]
    target_center = np.array(
        (TARGET_BASE_CENTER[0], TARGET_BASE_CENTER[1], TARGET_BASE_CENTER[2] + TARGET_HEIGHT_M / 2.0), dtype=float
    )
    hit_time = missile_hit_time(missile_id)
    best: tuple[BombPlan, BombEvaluation] | None = None
    for detonation_time in np.linspace(1.0, hit_time - 0.1, 30):
        missile = missile_position(missile_id, float(detonation_time))
        for line_fraction in np.linspace(0.05, 0.95, 19):
            smoke = missile + line_fraction * (target_center - missile)
            drop = uav.initial_position[2] - smoke[2]
            if drop < 0.0:
                continue
            delay = math.sqrt(2.0 * drop / 9.8)
            release = float(detonation_time) - delay
            if release < 0.0:
                continue
            horizontal_velocity = (smoke[:2] - np.asarray(uav.initial_position[:2], dtype=float)) / detonation_time
            speed = float(np.linalg.norm(horizontal_velocity))
            if not UAV_SPEED_MIN_MPS <= speed <= UAV_SPEED_MAX_MPS:
                continue
            plan = BombPlan(
                uav_id,
                1,
                missile_id,
                True,
                math.atan2(float(horizontal_velocity[1]), float(horizontal_velocity[0])) % (2.0 * math.pi),
                speed,
                release,
                delay,
            )
            evaluation = _evaluate_candidate(plan, question_id, config)
            if evaluation is not None and (best is None or evaluation.effective_duration_s > best[1].effective_duration_s):
                best = (plan, evaluation)
    return best


def _evaluate_candidate(plan: BombPlan, question_id: str, config: SolverConfig) -> BombEvaluation | None:
    if validate_plans(question_id, [plan]):
        return None
    return evaluate_plan(plan, str(plan.missile_id), config.evaluator)


def _solve_single_bomb(question_id: str, uav_id: str, missile_id: str, config: SolverConfig) -> CandidateSolution:
    bounds = _single_bomb_bounds(uav_id, missile_id)

    def objective(values: np.ndarray) -> float:
        plan = _candidate_plan(values, uav_id, missile_id)
        evaluation = _evaluate_candidate(plan, question_id, config)
        if evaluation is None:
            return 1_000_000.0 + max(0.0, plan.detonation_time_s - missile_hit_time(missile_id))
        return -evaluation.effective_duration_s

    global_result = differential_evolution(
        objective,
        bounds=bounds,
        maxiter=config.differential_evolution_maxiter,
        popsize=config.differential_evolution_popsize,
        seed=config.random_seed,
        polish=False,
        updating="immediate",
    )
    values = np.asarray(global_result.x, dtype=float)
    if config.local_refinement:
        local_result = minimize(objective, values, method="Powell", bounds=bounds, options={"maxiter": 80})
        if local_result.fun <= global_result.fun:
            values = np.asarray(local_result.x, dtype=float)

    plan = _candidate_plan(values, uav_id, missile_id)
    evaluation = _evaluate_candidate(plan, question_id, config)
    if evaluation is None:
        raise RuntimeError("optimizer returned an infeasible single-bomb candidate")
    center_line_seed = _center_line_seed(question_id, uav_id, missile_id, config)
    if center_line_seed is not None and center_line_seed[1].effective_duration_s > evaluation.effective_duration_s:
        plan, evaluation = center_line_seed
    if uav_id == "FY1" and missile_id == "M1":
        q1_anchor = BombPlan("FY1", 1, "M1", True, math.pi, 120.0, 1.5, 3.6)
        anchor_evaluation = _evaluate_candidate(q1_anchor, question_id, config)
        if anchor_evaluation is not None and anchor_evaluation.effective_duration_s > evaluation.effective_duration_s:
            plan = q1_anchor
            evaluation = anchor_evaluation
    return CandidateSolution(
        question_id=question_id,
        plans=(plan,),
        evaluations=(evaluation,),
        primary_durations_s={missile_id: evaluation.effective_duration_s},
        objective=(evaluation.effective_duration_s,),
        diagnostics={
            "global_method": "differential_evolution",
            "local_method": "Powell" if config.local_refinement else None,
            "random_seed": config.random_seed,
            "global_message": str(global_result.message),
        },
    )


def solve_q2(config: SolverConfig) -> CandidateSolution:
    return _solve_single_bomb("Q2", "FY1", "M1", config)


def _evaluate_same_missile_plans(plans: tuple[BombPlan, ...], missile_id: str, config: SolverConfig) -> tuple[tuple[BombEvaluation, ...], float]:
    evaluations = tuple(evaluate_plan(plan, missile_id, config.evaluator) for plan in plans if plan.is_used)
    intervals = merge_intervals(
        interval
        for evaluation in evaluations
        for interval in evaluation.occlusion_intervals
    )
    return evaluations, interval_duration(intervals)


def solve_q3(config: SolverConfig) -> CandidateSolution:
    hit_time = missile_hit_time("M1")
    max_delay = maximum_delay_s("FY1")
    bounds = [
        (0.0, 2.0 * math.pi),
        (UAV_SPEED_MIN_MPS, UAV_SPEED_MAX_MPS),
        (0.0, hit_time),
        (1.0, hit_time),
        (1.0, hit_time),
        (0.0, max_delay),
        (0.0, max_delay),
        (0.0, max_delay),
    ]

    def decode(values: np.ndarray) -> tuple[BombPlan, ...]:
        heading, speed, first_release, second_gap, third_gap, delay_1, delay_2, delay_3 = (float(value) for value in values)
        releases = (first_release, first_release + second_gap, first_release + second_gap + third_gap)
        delays = (delay_1, delay_2, delay_3)
        return tuple(
            BombPlan("FY1", bomb_id, "M1", True, heading % (2.0 * math.pi), speed, releases[bomb_id - 1], delays[bomb_id - 1])
            for bomb_id in (1, 2, 3)
        )

    def objective(values: np.ndarray) -> float:
        plans = decode(values)
        if validate_plans("Q3", plans):
            return 1_000_000.0 + max(0.0, plans[-1].detonation_time_s - hit_time)
        _, duration = _evaluate_same_missile_plans(plans, "M1", config)
        return -duration

    global_result = differential_evolution(
        objective,
        bounds=bounds,
        maxiter=config.differential_evolution_maxiter,
        popsize=config.differential_evolution_popsize,
        seed=config.random_seed,
        polish=False,
        updating="immediate",
    )
    values = np.asarray(global_result.x, dtype=float)
    if config.local_refinement:
        local_result = minimize(objective, values, method="Powell", bounds=bounds, options={"maxiter": 120})
        if local_result.fun <= global_result.fun:
            values = np.asarray(local_result.x, dtype=float)
    plans = decode(values)
    violations = validate_plans("Q3", plans)
    if violations:
        raise RuntimeError(f"optimizer returned an infeasible Q3 candidate: {violations}")
    evaluations, duration = _evaluate_same_missile_plans(plans, "M1", config)
    anchor_plans = tuple(
        BombPlan("FY1", bomb_id, "M1", True, math.pi, 120.0, 0.5 + bomb_id, 3.6)
        for bomb_id in (1, 2, 3)
    )
    anchor_evaluations, anchor_duration = _evaluate_same_missile_plans(anchor_plans, "M1", config)
    if anchor_duration > duration:
        plans, evaluations, duration = anchor_plans, anchor_evaluations, anchor_duration
    q2_anchor = _solve_single_bomb("Q2", "FY1", "M1", config).plans[0]
    q2_extended_anchor = tuple(
        BombPlan(
            "FY1",
            bomb_id,
            "M1",
            True,
            q2_anchor.heading_rad,
            q2_anchor.speed_mps,
            q2_anchor.release_time_s + bomb_id - 1,
            q2_anchor.delay_s,
        )
        for bomb_id in (1, 2, 3)
    )
    if not validate_plans("Q3", q2_extended_anchor):
        q2_anchor_evaluations, q2_anchor_duration = _evaluate_same_missile_plans(q2_extended_anchor, "M1", config)
        if q2_anchor_duration > duration:
            plans, evaluations, duration = q2_extended_anchor, q2_anchor_evaluations, q2_anchor_duration
    return CandidateSolution(
        question_id="Q3",
        plans=plans,
        evaluations=evaluations,
        primary_durations_s={"M1": duration},
        objective=(duration,),
        diagnostics={
            "global_method": "differential_evolution",
            "local_method": "Powell" if config.local_refinement else None,
            "random_seed": config.random_seed,
            "global_message": str(global_result.message),
        },
    )


def solve_q4(config: SolverConfig) -> CandidateSolution:
    uav_ids = ("FY1", "FY2", "FY3")
    hit_time = missile_hit_time("M1")
    bounds: list[tuple[float, float]] = []
    for uav_id in uav_ids:
        bounds.extend(_single_bomb_bounds(uav_id, "M1"))

    def decode(values: np.ndarray) -> tuple[BombPlan, ...]:
        return tuple(
            _candidate_plan(values[index * 4 : index * 4 + 4], uav_id, "M1")
            for index, uav_id in enumerate(uav_ids)
        )

    def objective(values: np.ndarray) -> float:
        plans = decode(values)
        if validate_plans("Q4", plans):
            latest_detonation = max(plan.detonation_time_s for plan in plans)
            return 1_000_000.0 + max(0.0, latest_detonation - hit_time)
        _, duration = _evaluate_same_missile_plans(plans, "M1", config)
        return -duration

    global_result = differential_evolution(
        objective,
        bounds=bounds,
        maxiter=config.differential_evolution_maxiter,
        popsize=config.differential_evolution_popsize,
        seed=config.random_seed,
        polish=False,
        updating="immediate",
    )
    values = np.asarray(global_result.x, dtype=float)
    if config.local_refinement:
        local_result = minimize(objective, values, method="Powell", bounds=bounds, options={"maxiter": 160})
        if local_result.fun <= global_result.fun:
            values = np.asarray(local_result.x, dtype=float)
    plans = decode(values)
    violations = validate_plans("Q4", plans)
    if violations:
        raise RuntimeError(f"optimizer returned an infeasible Q4 candidate: {violations}")
    evaluations, duration = _evaluate_same_missile_plans(plans, "M1", config)
    anchor_plans = (
        BombPlan("FY1", 1, "M1", True, math.pi, 120.0, 1.5, 3.6),
        BombPlan("FY2", 1, "M1", True, math.pi, 120.0, 1.5, 3.6),
        BombPlan("FY3", 1, "M1", True, math.pi, 120.0, 1.5, 3.6),
    )
    anchor_evaluations, anchor_duration = _evaluate_same_missile_plans(anchor_plans, "M1", config)
    if anchor_duration > duration:
        plans, evaluations, duration = anchor_plans, anchor_evaluations, anchor_duration
    q2_anchor = _solve_single_bomb("Q2", "FY1", "M1", config).plans[0]
    q2_extended_anchor = (
        q2_anchor,
        BombPlan("FY2", 1, "M1", True, math.pi, 120.0, 1.5, 3.6),
        BombPlan("FY3", 1, "M1", True, math.pi, 120.0, 1.5, 3.6),
    )
    if not validate_plans("Q4", q2_extended_anchor):
        q2_anchor_evaluations, q2_anchor_duration = _evaluate_same_missile_plans(q2_extended_anchor, "M1", config)
        if q2_anchor_duration > duration:
            plans, evaluations, duration = q2_extended_anchor, q2_anchor_evaluations, q2_anchor_duration
    return CandidateSolution(
        question_id="Q4",
        plans=plans,
        evaluations=evaluations,
        primary_durations_s={"M1": duration},
        objective=(duration,),
        diagnostics={
            "global_method": "differential_evolution",
            "local_method": "Powell" if config.local_refinement else None,
            "random_seed": config.random_seed,
            "global_message": str(global_result.message),
        },
    )


def _unused_q5_plan(uav_id: str, bomb_id: int) -> BombPlan:
    return BombPlan(uav_id, bomb_id, None, False, 0.0, 0.0, 0.0, 0.0)


def solve_q5(config: SolverConfig) -> CandidateSolution:
    missile_ids = ("M1", "M2", "M3")
    uav_ids = tuple(UAVS)
    single_candidates: dict[tuple[str, str], CandidateSolution] = {}
    scores: dict[tuple[str, str], float] = {}

    for uav_index, uav_id in enumerate(uav_ids):
        for missile_index, missile_id in enumerate(missile_ids):
            pair_config = replace(config, random_seed=config.random_seed + uav_index * len(missile_ids) + missile_index)
            candidate = _solve_single_bomb("Q5", uav_id, missile_id, pair_config)
            single_candidates[(uav_id, missile_id)] = candidate
            scores[(uav_id, missile_id)] = candidate.primary_durations_s[missile_id]

    selected_assignment: tuple[str, str, str] | None = None
    selected_objective = (-math.inf, -math.inf)
    for assignment in permutations(uav_ids, len(missile_ids)):
        durations = tuple(scores[(uav_id, missile_id)] for uav_id, missile_id in zip(assignment, missile_ids))
        if min(durations) <= 0.0:
            continue
        objective = (sum(durations), min(durations))
        if objective > selected_objective:
            selected_assignment = assignment
            selected_objective = objective

    if selected_assignment is None:
        plans = tuple(_unused_q5_plan(uav_id, bomb_id) for uav_id in uav_ids for bomb_id in (1, 2, 3))
        return CandidateSolution(
            question_id="Q5",
            plans=plans,
            evaluations=(),
            primary_durations_s={missile_id: 0.0 for missile_id in missile_ids},
            objective=(0.0, 0.0),
            diagnostics={
                "feasible": False,
                "reason": "No primary-target assignment produced positive coverage for all three missiles under the frozen criterion.",
                "global_method": "differential_evolution",
                "local_method": "Powell" if config.local_refinement else None,
                "random_seed": config.random_seed,
            },
        )

    used_by_uav = {
        uav_id: single_candidates[(uav_id, missile_id)]
        for uav_id, missile_id in zip(selected_assignment, missile_ids)
    }
    plans: list[BombPlan] = []
    evaluations: list[BombEvaluation] = []
    durations: dict[str, float] = {}
    for uav_id in uav_ids:
        selected = used_by_uav.get(uav_id)
        if selected is None:
            plans.extend(_unused_q5_plan(uav_id, bomb_id) for bomb_id in (1, 2, 3))
            continue
        plan = selected.plans[0]
        plans.append(plan)
        plans.extend(_unused_q5_plan(uav_id, bomb_id) for bomb_id in (2, 3))
        evaluations.extend(selected.evaluations)
        durations[str(plan.missile_id)] = selected.primary_durations_s[str(plan.missile_id)]

    for missile_id in missile_ids:
        durations.setdefault(missile_id, 0.0)
    return CandidateSolution(
        question_id="Q5",
        plans=tuple(plans),
        evaluations=tuple(evaluations),
        primary_durations_s=durations,
        objective=(sum(durations.values()), min(durations.values())),
        diagnostics={
            "feasible": all(duration > 0.0 for duration in durations.values()),
            "assignment": {missile_id: uav_id for uav_id, missile_id in zip(selected_assignment, missile_ids)},
            "global_method": "differential_evolution",
            "local_method": "Powell" if config.local_refinement else None,
            "random_seed": config.random_seed,
            "q5_credit_policy": "primary_target_only",
        },
    )


## `06_code/src/target_geometry.py`

from __future__ import annotations

import math

import numpy as np

from .constants import TARGET_BASE_CENTER, TARGET_HEIGHT_M, TARGET_RADIUS_M


def target_sample_points(
    angular_samples: int,
    height_samples: int,
    radial_samples: int,
) -> tuple[np.ndarray, ...]:
    if angular_samples < 3:
        raise ValueError("angular_samples must be at least 3")
    if height_samples < 2:
        raise ValueError("height_samples must be at least 2")
    if radial_samples < 1:
        raise ValueError("radial_samples must be at least 1")

    x0, y0, z0 = TARGET_BASE_CENTER
    points: list[np.ndarray] = []
    angles = [2.0 * math.pi * index / angular_samples for index in range(angular_samples)]
    heights = [z0 + TARGET_HEIGHT_M * index / (height_samples - 1) for index in range(height_samples)]

    for height in heights:
        for angle in angles:
            points.append(
                np.array(
                    (x0 + TARGET_RADIUS_M * math.cos(angle), y0 + TARGET_RADIUS_M * math.sin(angle), height),
                    dtype=float,
                )
            )

    for height in (z0, z0 + TARGET_HEIGHT_M):
        points.append(np.array((x0, y0, height), dtype=float))
        for ring in range(1, radial_samples + 1):
            radius = TARGET_RADIUS_M * ring / radial_samples
            for angle in angles:
                points.append(
                    np.array((x0 + radius * math.cos(angle), y0 + radius * math.sin(angle), height), dtype=float)
                )

    unique: dict[tuple[float, float, float], np.ndarray] = {}
    for point in points:
        rounded = tuple(round(float(value), 12) for value in point)
        unique[rounded] = np.array(rounded, dtype=float)
    return tuple(unique[key] for key in sorted(unique))


## `07_results/candidate_run_manifest.json`

{
  "generated_at": "2026-07-22T10:36:12.731980+00:00",
  "result_status": "candidate",
  "mode": "candidate",
  "questions": [
    "Q1",
    "Q2",
    "Q3",
    "Q4",
    "Q5"
  ],
  "solver_config": {
    "target": {
      "angular_samples": 12,
      "height_samples": 3,
      "radial_samples": 2,
      "scan_step_s": 0.1,
      "root_tolerance_s": 1e-05
    },
    "differential_evolution_maxiter": 6,
    "differential_evolution_popsize": 5,
    "local_refinement": true,
    "random_seed": 20250722
  },
  "dependencies": {
    "numpy": "2.0.2",
    "scipy": "1.13.1",
    "pandas": "2.3.3",
    "openpyxl": "3.1.5",
    "PyYAML": "6.0.3"
  },
  "q5_feasible": true,
  "q5_diagnostics": {
    "feasible": true,
    "assignment": {
      "M1": "FY1",
      "M2": "FY2",
      "M3": "FY5"
    },
    "global_method": "differential_evolution",
    "local_method": "Powell",
    "random_seed": 20250722,
    "q5_credit_policy": "primary_target_only"
  },
  "notice": "Candidate artifacts are not result-freeze outputs and are not registered in result_contract.csv."
}


## `07_results/metrics_summary.csv`

﻿question_id,metric_name,metric_value,unit,result_status
Q1,primary_duration_M1,1.362402343749995,s,candidate
Q1,objective_1,1.362402343749995,s,candidate
Q2,primary_duration_M1,2.238162231445303,s,candidate
Q2,objective_1,2.238162231445303,s,candidate
Q3,primary_duration_M1,2.238162231445303,s,candidate
Q3,objective_1,2.238162231445303,s,candidate
Q4,primary_duration_M1,2.238162231445303,s,candidate
Q4,objective_1,2.238162231445303,s,candidate
Q5,primary_duration_M1,2.238162231445303,s,candidate
Q5,primary_duration_M2,1.9820404052734322,s,candidate
Q5,primary_duration_M3,1.8768035888672046,s,candidate
Q5,objective_1,6.09700622558594,s,candidate
Q5,objective_2,1.8768035888672046,s,candidate


## `07_results/q1_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q1,FY1,1,M1,1,180.0,120.0,1.5,3.6,5.1,17620.0,0.0,1800.0,17188.0,0.0,1736.496,1.362402343749995,"[[8.056106567382802, 9.418508911132797]]",candidate


## `07_results/q2_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q2,FY1,1,M1,1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,17430.714677459066,3.631721349123526,1800.0,16783.16724483817,9.999999999999895,1678.5667244838169,2.238162231445303,"[[7.817155600773029, 10.055317832218332]]",candidate

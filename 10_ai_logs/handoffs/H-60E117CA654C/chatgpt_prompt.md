# evidence_design / ChatGPT

## 结果
设计能支撑论文论证的图表、表格、论断顺序和论文提纲。

## 边界
只使用冻结结果；不得把装饰性图表当证据，不得为视觉效果改变数据含义。

## 交付
给出每个图表的论证目的、数据来源、坐标单位、对应论断和进入论文的位置。

## 验收
每个正式论断有证据来源，每个图表回答明确问题且能绑定结果合同。

## 阻塞
缺少冻结结果、论断无证据或图表无法由现有数据生成时请求补充验证。

## Response metadata

Begin the response with this exact metadata block:

---
protocol: mmwf-handoff/v1
project_id: ccmc2025-a
stage: evidence_design
handoff_id: H-60E117CA654C
context_sha256: ab122c28b44e57ef24242cde61dd7792567799534f661912b8f1dba382255f76
---

## Verified context

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


## `07_results/q3_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q3,FY1,1,M1,1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,17430.714677459066,3.631721349123526,1800.0,16783.16724483817,9.999999999999895,1678.5667244838169,2.238162231445303,"[[7.817155600773029, 10.055317832218332]]",candidate
Q3,FY1,2,M1,1,179.43654517246082,130.08336768519578,3.838973088474825,4.978182512298204,8.81715560077303,17300.637599927017,4.910959029771843,1800.0,16653.090167306123,11.279237680648212,1678.5667244838169,0,[],candidate
Q3,FY1,3,M1,1,179.43654517246082,130.08336768519578,4.838973088474825,4.978182512298204,9.81715560077303,17170.56052239497,6.19019671042016,1800.0,16523.013089774075,12.55847536129653,1678.5667244838169,0,[],candidate


## `07_results/q4_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q4,FY1,1,M1,1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,17430.714677459066,3.631721349123526,1800.0,16783.16724483817,9.999999999999895,1678.5667244838169,2.238162231445303,"[[7.817155600773029, 10.055317832218332]]",candidate
Q4,FY2,1,M1,1,180.0,120.0,1.5,3.6,5.1,11820.0,1400.0,1400.0,11388.0,1400.0,1336.496,0,[],candidate
Q4,FY3,1,M1,1,180.0,120.0,1.5,3.6,5.1,5820.0,-3000.0,700.0,5388.0,-3000.0,636.496,0,[],candidate


## `07_results/q5_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q5,FY1,1,M1,1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,17430.714677459066,3.631721349123526,1800.0,16783.16724483817,9.999999999999895,1678.5667244838169,2.238162231445303,"[[7.817155600773029, 10.055317832218332]]",candidate
Q5,FY1,2,,0,,,,,,,,,,,,,[],candidate
Q5,FY1,3,,0,,,,,,,,,,,,,[],candidate
Q5,FY2,1,M2,1,275.5970977478011,100.88690594525764,6.0857908606118745,3.555641037660742,9.641431898272616,12059.882666072617,788.9506205518344,1400.0,12094.869288158236,431.94324067868115,1338.051342375384,1.9820404052734322,"[[9.641431898272616, 11.623472303546048]]",candidate
Q5,FY2,2,,0,,,,,,,,,,,,,[],candidate
Q5,FY2,3,,0,,,,,,,,,,,,,[],candidate
Q5,FY3,1,,0,,,,,,,,,,,,,[],candidate
Q5,FY3,2,,0,,,,,,,,,,,,,[],candidate
Q5,FY3,3,,0,,,,,,,,,,,,,[],candidate
Q5,FY4,1,,0,,,,,,,,,,,,,[],candidate
Q5,FY4,2,,0,,,,,,,,,,,,,[],candidate
Q5,FY4,3,,0,,,,,,,,,,,,,[],candidate
Q5,FY5,1,M3,1,119.30217914169313,121.14131300438812,13.136138284985464,2.1695621915927563,15.30570047657822,12221.178713062363,-612.2804622520769,1300.0,12092.548732051975,-383.0849577350657,1276.935699494375,1.8768035888672046,"[[15.30570047657822, 17.182504065445425]]",candidate
Q5,FY5,2,,0,,,,,,,,,,,,,[],candidate
Q5,FY5,3,,0,,,,,,,,,,,,,[],candidate


## `07_results/ready_for_freeze/metrics_summary.csv`

﻿question_id,metric_name,metric_value,unit,result_status,source_record
Q1,primary_duration_M1,1.3622014999389869,s,ready,Q1/M1
Q2,primary_duration_M1,2.2381643772125575,s,ready,Q2/M1
Q3,primary_duration_M1,2.2381643772125575,s,ready,Q3/M1
Q4,primary_duration_M1,2.2381643772125575,s,ready,Q4/M1
Q5,primary_duration_M1,2.2381643772125575,s,ready,Q5/M1
Q5,primary_duration_M2,1.9820433139801334,s,ready,Q5/M2
Q5,primary_duration_M3,1.8768008708953303,s,ready,Q5/M3
Q5,objective_total_duration,6.097008562088021,s,ready,Q5/M1;M2;M3
Q5,objective_minimum_duration,1.8768008708953303,s,ready,Q5/M1;M2;M3


## `07_results/ready_for_freeze/q1_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q1,FY1,1,M1,1,180.0,120.0,1.5,3.6,5.1,17620.0,0.0,1800.0,17188.0,0.0,1736.496,1.3622014999389869,"[[8.056308984756512, 9.4185104846955]]",ready


## `07_results/ready_for_freeze/q2_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q2,FY1,1,M1,1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,17430.714677459066,3.631721349123526,1800.0,16783.16724483817,9.999999999999895,1678.5667244838169,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",ready


## `07_results/ready_for_freeze/q3_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q3,FY1,1,M1,1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,17430.714677459066,3.631721349123526,1800.0,16783.16724483817,9.999999999999895,1678.5667244838169,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",ready
Q3,FY1,2,M1,1,179.43654517246082,130.08336768519578,3.838973088474825,4.978182512298204,8.81715560077303,17300.637599927017,4.910959029771843,1800.0,16653.09016730612,11.279237680648212,1678.5667244838169,0,[],ready
Q3,FY1,3,M1,1,179.43654517246082,130.08336768519578,4.838973088474825,4.978182512298204,9.81715560077303,17170.56052239497,6.19019671042016,1800.0,16523.013089774075,12.55847536129653,1678.5667244838169,0,[],ready


## `07_results/ready_for_freeze/q4_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q4,FY1,1,M1,1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,17430.714677459066,3.631721349123526,1800.0,16783.16724483817,9.999999999999895,1678.5667244838169,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",ready
Q4,FY2,1,M1,1,180.0,120.0,1.5,3.6,5.1,11820.0,1400.0,1400.0,11388.0,1400.0,1336.496,0,[],ready
Q4,FY3,1,M1,1,180.0,120.0,1.5,3.6,5.1,5820.0,-3000.0,700.0,5388.0,-3000.0,636.496,0,[],ready


## `07_results/ready_for_freeze/q5_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q5,FY1,1,M1,1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,17430.714677459066,3.631721349123526,1800.0,16783.16724483817,9.999999999999895,1678.5667244838169,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",ready
Q5,FY1,2,,0,,,,,,,,,,,,,[],ready
Q5,FY1,3,,0,,,,,,,,,,,,,[],ready
Q5,FY2,1,M2,1,275.5970977478011,100.88690594525764,6.0857908606118745,3.555641037660742,9.641431898272616,12059.882666072617,788.9506205518344,1400.0,12094.869288158236,431.94324067868115,1338.051342375384,1.9820433139801334,"[[9.641431898272616, 11.62347521225275]]",ready
Q5,FY2,2,,0,,,,,,,,,,,,,[],ready
Q5,FY2,3,,0,,,,,,,,,,,,,[],ready
Q5,FY3,1,,0,,,,,,,,,,,,,[],ready
Q5,FY3,2,,0,,,,,,,,,,,,,[],ready
Q5,FY3,3,,0,,,,,,,,,,,,,[],ready
Q5,FY4,1,,0,,,,,,,,,,,,,[],ready
Q5,FY4,2,,0,,,,,,,,,,,,,[],ready
Q5,FY4,3,,0,,,,,,,,,,,,,[],ready
Q5,FY5,1,M3,1,119.30217914169313,121.14131300438812,13.136138284985464,2.1695621915927563,15.30570047657822,12221.178713062363,-612.2804622520769,1300.0,12092.548732051975,-383.08495773506553,1276.935699494375,1.8768008708953303,"[[15.30570047657822, 17.18250134747355]]",ready
Q5,FY5,2,,0,,,,,,,,,,,,,[],ready
Q5,FY5,3,,0,,,,,,,,,,,,,[],ready


## `07_results/ready_for_freeze/ready_for_freeze_manifest.json`

{
  "freeze_id": "RF-20260722T114756Z",
  "result_status": "ready",
  "human_gate": "result_freeze_gate",
  "human_gate_status": "pending",
  "source_candidate_run": "07_results/result_freeze_validation/runs/refined",
  "strict_recomputation": "07_results/result_freeze_validation/primary_recomputation.csv",
  "questions": [
    "Q1",
    "Q2",
    "Q3",
    "Q4",
    "Q5"
  ],
  "validation_checks": {
    "constraints_clear": true,
    "primary_durations_positive": true,
    "seed_metric_span_s": 0.0,
    "seed_stability_tolerance_s": 0.05,
    "seed_stable": true,
    "seed_metric_spans_by_output": {
      "Q1/primary_duration_M1": 0.0,
      "Q1/objective_1": 0.0,
      "Q2/primary_duration_M1": 0.0,
      "Q2/objective_1": 0.0,
      "Q3/primary_duration_M1": 0.0,
      "Q3/objective_1": 0.0,
      "Q4/primary_duration_M1": 0.0,
      "Q4/objective_1": 0.0,
      "Q5/primary_duration_M1": 0.0,
      "Q5/primary_duration_M2": 0.0,
      "Q5/primary_duration_M3": 0.0,
      "Q5/objective_1": 0.0,
      "Q5/objective_2": 0.0
    }
  },
  "notice": "Prepared for human result-freeze review. No AI has confirmed the human gate.",
  "contracts_registered": true,
  "template_mapping_status": "pass",
  "prepared_at": "2026-07-22T11:53:23.725660+00:00"
}


## `07_results/ready_for_freeze/result_source_map.csv`

﻿result_id,question_id,source_file,result_status,producing_run_id,source_candidate_run
ready_q1_plans,Q1,07_results/ready_for_freeze/q1_results.csv,ready,RF-20260722T114756Z,result_freeze_validation/runs/refined
ready_q2_plans,Q2,07_results/ready_for_freeze/q2_results.csv,ready,RF-20260722T114756Z,result_freeze_validation/runs/refined
ready_q3_plans,Q3,07_results/ready_for_freeze/q3_results.csv,ready,RF-20260722T114756Z,result_freeze_validation/runs/refined
ready_q4_plans,Q4,07_results/ready_for_freeze/q4_results.csv,ready,RF-20260722T114756Z,result_freeze_validation/runs/refined
ready_q5_plans,Q5,07_results/ready_for_freeze/q5_results.csv,ready,RF-20260722T114756Z,result_freeze_validation/runs/refined


## `07_results/ready_for_freeze/template_inputs.json`

{
  "Q3": [
    {
      "question_id": "Q3",
      "uav_id": "FY1",
      "bomb_id": "1",
      "missile_id": "M1",
      "is_used": "1",
      "heading_deg": "179.43654517246082",
      "speed_mps": "130.08336768519578",
      "release_time_s": "2.838973088474825",
      "delay_s": "4.978182512298204",
      "detonation_time_s": "7.817155600773029",
      "release_x_m": "17430.714677459066",
      "release_y_m": "3.631721349123526",
      "release_z_m": "1800.0",
      "detonation_x_m": "16783.16724483817",
      "detonation_y_m": "9.999999999999895",
      "detonation_z_m": "1678.5667244838169",
      "effective_duration_s": "2.2381643772125575",
      "occlusion_intervals": "[[7.817155600773029, 10.055319977985587]]",
      "result_status": "ready"
    },
    {
      "question_id": "Q3",
      "uav_id": "FY1",
      "bomb_id": "2",
      "missile_id": "M1",
      "is_used": "1",
      "heading_deg": "179.43654517246082",
      "speed_mps": "130.08336768519578",
      "release_time_s": "3.838973088474825",
      "delay_s": "4.978182512298204",
      "detonation_time_s": "8.81715560077303",
      "release_x_m": "17300.637599927017",
      "release_y_m": "4.910959029771843",
      "release_z_m": "1800.0",
      "detonation_x_m": "16653.09016730612",
      "detonation_y_m": "11.279237680648212",
      "detonation_z_m": "1678.5667244838169",
      "effective_duration_s": "0",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    },
    {
      "question_id": "Q3",
      "uav_id": "FY1",
      "bomb_id": "3",
      "missile_id": "M1",
      "is_used": "1",
      "heading_deg": "179.43654517246082",
      "speed_mps": "130.08336768519578",
      "release_time_s": "4.838973088474825",
      "delay_s": "4.978182512298204",
      "detonation_time_s": "9.81715560077303",
      "release_x_m": "17170.56052239497",
      "release_y_m": "6.19019671042016",
      "release_z_m": "1800.0",
      "detonation_x_m": "16523.013089774075",
      "detonation_y_m": "12.55847536129653",
      "detonation_z_m": "1678.5667244838169",
      "effective_duration_s": "0",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    }
  ],
  "Q4": [
    {
      "question_id": "Q4",
      "uav_id": "FY1",
      "bomb_id": "1",
      "missile_id": "M1",
      "is_used": "1",
      "heading_deg": "179.43654517246082",
      "speed_mps": "130.08336768519578",
      "release_time_s": "2.838973088474825",
      "delay_s": "4.978182512298204",
      "detonation_time_s": "7.817155600773029",
      "release_x_m": "17430.714677459066",
      "release_y_m": "3.631721349123526",
      "release_z_m": "1800.0",
      "detonation_x_m": "16783.16724483817",
      "detonation_y_m": "9.999999999999895",
      "detonation_z_m": "1678.5667244838169",
      "effective_duration_s": "2.2381643772125575",
      "occlusion_intervals": "[[7.817155600773029, 10.055319977985587]]",
      "result_status": "ready"
    },
    {
      "question_id": "Q4",
      "uav_id": "FY2",
      "bomb_id": "1",
      "missile_id": "M1",
      "is_used": "1",
      "heading_deg": "180.0",
      "speed_mps": "120.0",
      "release_time_s": "1.5",
      "delay_s": "3.6",
      "detonation_time_s": "5.1",
      "release_x_m": "11820.0",
      "release_y_m": "1400.0",
      "release_z_m": "1400.0",
      "detonation_x_m": "11388.0",
      "detonation_y_m": "1400.0",
      "detonation_z_m": "1336.496",
      "effective_duration_s": "0",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    },
    {
      "question_id": "Q4",
      "uav_id": "FY3",
      "bomb_id": "1",
      "missile_id": "M1",
      "is_used": "1",
      "heading_deg": "180.0",
      "speed_mps": "120.0",
      "release_time_s": "1.5",
      "delay_s": "3.6",
      "detonation_time_s": "5.1",
      "release_x_m": "5820.0",
      "release_y_m": "-3000.0",
      "release_z_m": "700.0",
      "detonation_x_m": "5388.0",
      "detonation_y_m": "-3000.0",
      "detonation_z_m": "636.496",
      "effective_duration_s": "0",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    }
  ],
  "Q5": [
    {
      "question_id": "Q5",
      "uav_id": "FY1",
      "bomb_id": "1",
      "missile_id": "M1",
      "is_used": "1",
      "heading_deg": "179.43654517246082",
      "speed_mps": "130.08336768519578",
      "release_time_s": "2.838973088474825",
      "delay_s": "4.978182512298204",
      "detonation_time_s": "7.817155600773029",
      "release_x_m": "17430.714677459066",
      "release_y_m": "3.631721349123526",
      "release_z_m": "1800.0",
      "detonation_x_m": "16783.16724483817",
      "detonation_y_m": "9.999999999999895",
      "detonation_z_m": "1678.5667244838169",
      "effective_duration_s": "2.2381643772125575",
      "occlusion_intervals": "[[7.817155600773029, 10.055319977985587]]",
      "result_status": "ready"
    },
    {
      "question_id": "Q5",
      "uav_id": "FY1",
      "bomb_id": "2",
      "missile_id": "",
      "is_used": "0",
      "heading_deg": "",
      "speed_mps": "",
      "release_time_s": "",
      "delay_s": "",
      "detonation_time_s": "",
      "release_x_m": "",
      "release_y_m": "",
      "release_z_m": "",
      "detonation_x_m": "",
      "detonation_y_m": "",
      "detonation_z_m": "",
      "effective_duration_s": "",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    },
    {
      "question_id": "Q5",
      "uav_id": "FY1",
      "bomb_id": "3",
      "missile_id": "",
      "is_used": "0",
      "heading_deg": "",
      "speed_mps": "",
      "release_time_s": "",
      "delay_s": "",
      "detonation_time_s": "",
      "release_x_m": "",
      "release_y_m": "",
      "release_z_m": "",
      "detonation_x_m": "",
      "detonation_y_m": "",
      "detonation_z_m": "",
      "effective_duration_s": "",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    },
    {
      "question_id": "Q5",
      "uav_id": "FY2",
      "bomb_id": "1",
      "missile_id": "M2",
      "is_used": "1",
      "heading_deg": "275.5970977478011",
      "speed_mps": "100.88690594525764",
      "release_time_s": "6.0857908606118745",
      "delay_s": "3.555641037660742",
      "detonation_time_s": "9.641431898272616",
      "release_x_m": "12059.882666072617",
      "release_y_m": "788.9506205518344",
      "release_z_m": "1400.0",
      "detonation_x_m": "12094.869288158236",
      "detonation_y_m": "431.94324067868115",
      "detonation_z_m": "1338.051342375384",
      "effective_duration_s": "1.9820433139801334",
      "occlusion_intervals": "[[9.641431898272616, 11.62347521225275]]",
      "result_status": "ready"
    },
    {
      "question_id": "Q5",
      "uav_id": "FY2",
      "bomb_id": "2",
      "missile_id": "",
      "is_used": "0",
      "heading_deg": "",
      "speed_mps": "",
      "release_time_s": "",
      "delay_s": "",
      "detonation_time_s": "",
      "release_x_m": "",
      "release_y_m": "",
      "release_z_m": "",
      "detonation_x_m": "",
      "detonation_y_m": "",
      "detonation_z_m": "",
      "effective_duration_s": "",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    },
    {
      "question_id": "Q5",
      "uav_id": "FY2",
      "bomb_id": "3",
      "missile_id": "",
      "is_used": "0",
      "heading_deg": "",
      "speed_mps": "",
      "release_time_s": "",
      "delay_s": "",
      "detonation_time_s": "",
      "release_x_m": "",
      "release_y_m": "",
      "release_z_m": "",
      "detonation_x_m": "",
      "detonation_y_m": "",
      "detonation_z_m": "",
      "effective_duration_s": "",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    },
    {
      "question_id": "Q5",
      "uav_id": "FY3",
      "bomb_id": "1",
      "missile_id": "",
      "is_used": "0",
      "heading_deg": "",
      "speed_mps": "",
      "release_time_s": "",
      "delay_s": "",
      "detonation_time_s": "",
      "release_x_m": "",
      "release_y_m": "",
      "release_z_m": "",
      "detonation_x_m": "",
      "detonation_y_m": "",
      "detonation_z_m": "",
      "effective_duration_s": "",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    },
    {
      "question_id": "Q5",
      "uav_id": "FY3",
      "bomb_id": "2",
      "missile_id": "",
      "is_used": "0",
      "heading_deg": "",
      "speed_mps": "",
      "release_time_s": "",
      "delay_s": "",
      "detonation_time_s": "",
      "release_x_m": "",
      "release_y_m": "",
      "release_z_m": "",
      "detonation_x_m": "",
      "detonation_y_m": "",
      "detonation_z_m": "",
      "effective_duration_s": "",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    },
    {
      "question_id": "Q5",
      "uav_id": "FY3",
      "bomb_id": "3",
      "missile_id": "",
      "is_used": "0",
      "heading_deg": "",
      "speed_mps": "",
      "release_time_s": "",
      "delay_s": "",
      "detonation_time_s": "",
      "release_x_m": "",
      "release_y_m": "",
      "release_z_m": "",
      "detonation_x_m": "",
      "detonation_y_m": "",
      "detonation_z_m": "",
      "effective_duration_s": "",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    },
    {
      "question_id": "Q5",
      "uav_id": "FY4",
      "bomb_id": "1",
      "missile_id": "",
      "is_used": "0",
      "heading_deg": "",
      "speed_mps": "",
      "release_time_s": "",
      "delay_s": "",
      "detonation_time_s": "",
      "release_x_m": "",
      "release_y_m": "",
      "release_z_m": "",
      "detonation_x_m": "",
      "detonation_y_m": "",
      "detonation_z_m": "",
      "effective_duration_s": "",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    },
    {
      "question_id": "Q5",
      "uav_id": "FY4",
      "bomb_id": "2",
      "missile_id": "",
      "is_used": "0",
      "heading_deg": "",
      "speed_mps": "",
      "release_time_s": "",
      "delay_s": "",
      "detonation_time_s": "",
      "release_x_m": "",
      "release_y_m": "",
      "release_z_m": "",
      "detonation_x_m": "",
      "detonation_y_m": "",
      "detonation_z_m": "",
      "effective_duration_s": "",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    },
    {
      "question_id": "Q5",
      "uav_id": "FY4",
      "bomb_id": "3",
      "missile_id": "",
      "is_used": "0",
      "heading_deg": "",
      "speed_mps": "",
      "release_time_s": "",
      "delay_s": "",
      "detonation_time_s": "",
      "release_x_m": "",
      "release_y_m": "",
      "release_z_m": "",
      "detonation_x_m": "",
      "detonation_y_m": "",
      "detonation_z_m": "",
      "effective_duration_s": "",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    },
    {
      "question_id": "Q5",
      "uav_id": "FY5",
      "bomb_id": "1",
      "missile_id": "M3",
      "is_used": "1",
      "heading_deg": "119.30217914169313",
      "speed_mps": "121.14131300438812",
      "release_time_s": "13.136138284985464",
      "delay_s": "2.1695621915927563",
      "detonation_time_s": "15.30570047657822",
      "release_x_m": "12221.178713062363",
      "release_y_m": "-612.2804622520769",
      "release_z_m": "1300.0",
      "detonation_x_m": "12092.548732051975",
      "detonation_y_m": "-383.08495773506553",
      "detonation_z_m": "1276.935699494375",
      "effective_duration_s": "1.8768008708953303",
      "occlusion_intervals": "[[15.30570047657822, 17.18250134747355]]",
      "result_status": "ready"
    },
    {
      "question_id": "Q5",
      "uav_id": "FY5",
      "bomb_id": "2",
      "missile_id": "",
      "is_used": "0",
      "heading_deg": "",
      "speed_mps": "",
      "release_time_s": "",
      "delay_s": "",
      "detonation_time_s": "",
      "release_x_m": "",
      "release_y_m": "",
      "release_z_m": "",
      "detonation_x_m": "",
      "detonation_y_m": "",
      "detonation_z_m": "",
      "effective_duration_s": "",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    },
    {
      "question_id": "Q5",
      "uav_id": "FY5",
      "bomb_id": "3",
      "missile_id": "",
      "is_used": "0",
      "heading_deg": "",
      "speed_mps": "",
      "release_time_s": "",
      "delay_s": "",
      "detonation_time_s": "",
      "release_x_m": "",
      "release_y_m": "",
      "release_z_m": "",
      "detonation_x_m": "",
      "detonation_y_m": "",
      "detonation_z_m": "",
      "effective_duration_s": "",
      "occlusion_intervals": "[]",
      "result_status": "ready"
    }
  ]
}


## `07_results/ready_for_freeze/template_mapping_check.json`

{
  "status": "pass",
  "failure_count": 0,
  "failures": []
}


## `07_results/ready_for_freeze/template_mapping_expected.csv`

﻿question_id,template_file,template_row,uav_id,bomb_id,is_used,missile_id,heading_deg,speed_mps,effective_duration_s
Q3,result1.xlsx,2,FY1,1,1,M1,179.43654517246082,130.08336768519578,2.2381643772125575
Q3,result1.xlsx,3,FY1,2,1,M1,179.43654517246082,130.08336768519578,0
Q3,result1.xlsx,4,FY1,3,1,M1,179.43654517246082,130.08336768519578,0
Q4,result2.xlsx,2,FY1,1,1,M1,179.43654517246082,130.08336768519578,2.2381643772125575
Q4,result2.xlsx,3,FY2,1,1,M1,180.0,120.0,0
Q4,result2.xlsx,4,FY3,1,1,M1,180.0,120.0,0
Q5,result3.xlsx,2,FY1,1,1,M1,179.43654517246082,130.08336768519578,2.2381643772125575
Q5,result3.xlsx,3,FY1,2,0,,,,
Q5,result3.xlsx,4,FY1,3,0,,,,
Q5,result3.xlsx,5,FY2,1,1,M2,275.5970977478011,100.88690594525764,1.9820433139801334
Q5,result3.xlsx,6,FY2,2,0,,,,
Q5,result3.xlsx,7,FY2,3,0,,,,
Q5,result3.xlsx,8,FY3,1,0,,,,
Q5,result3.xlsx,9,FY3,2,0,,,,
Q5,result3.xlsx,10,FY3,3,0,,,,
Q5,result3.xlsx,11,FY4,1,0,,,,
Q5,result3.xlsx,12,FY4,2,0,,,,
Q5,result3.xlsx,13,FY4,3,0,,,,
Q5,result3.xlsx,14,FY5,1,1,M3,119.30217914169313,121.14131300438812,1.8768008708953303
Q5,result3.xlsx,15,FY5,2,0,,,,
Q5,result3.xlsx,16,FY5,3,0,,,,


## `07_results/ready_for_freeze/template_mapping_verification.json`

{
  "status": "ready",
  "generated_by": "artifact-tool",
  "verification": [
    {
      "question_id": "Q3",
      "template": "result1.xlsx",
      "range": "A1:J6",
      "inspection": {
        "kind": "table",
        "sheet": "Sheet1",
        "address": "A1:J6",
        "rows": 6,
        "cols": 10,
        "values": [
          [
            "无人机运动方向",
            "无人机运动速度 (m/s)",
            "烟幕干扰弹编号",
            "烟幕干扰弹投放点的x坐标 (m)",
            "烟幕干扰弹投放点的y坐标 (m)",
            "烟幕干扰弹投放点的z坐标 (m)",
            "烟幕干扰弹起爆点的x坐标 (m)",
            "烟幕干扰弹起爆点的y坐标 (m)",
            "烟幕干扰弹起爆点的z坐标 (m)",
            "有效干扰时长 (s)"
          ],
          [
            179.43654517246082,
            130.08336768519578,
            1,
            17430.714677459066,
            3.631721349123526,
            1800,
            16783.16724483817,
            9.999999999999895,
            1678.5667244838169,
            2.2381643772125575
          ],
          [
            179.43654517246082,
            130.08336768519578,
            2,
            17300.637599927017,
            4.910959029771843,
            1800,
            16653.09016730612,
            11.279237680648212,
            1678.5667244838169,
            0
          ],
          [
            179.43654517246082,
            130.08336768519578,
            3,
            17170.56052239497,
            6.19019671042016,
            1800,
            16523.013089774075,
            12.55847536129653,
            1678.5667244838169,
            0
          ],
          [
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            "注：以x轴为正向，逆时针方向为正，取值0~360（度）。",
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ]
        ]
      },
      "formula_error_matches": 0
    },
    {
      "question_id": "Q4",
      "template": "result2.xlsx",
      "range": "A1:J6",
      "inspection": {
        "kind": "table",
        "sheet": "Sheet1",
        "address": "A1:J6",
        "rows": 6,
        "cols": 10,
        "values": [
          [
            "无人机编号",
            "无人机运动方向",
            "无人机运动速度 (m/s)",
            "烟幕干扰弹投放点的x坐标 (m)",
            "烟幕干扰弹投放点的y坐标 (m)",
            "烟幕干扰弹投放点的z坐标 (m)",
            "烟幕干扰弹起爆点的x坐标 (m)",
            "烟幕干扰弹起爆点的y坐标 (m)",
            "烟幕干扰弹起爆点的z坐标 (m)",
            "有效干扰时长 (s)"
          ],
          [
            "FY1",
            179.43654517246082,
            130.08336768519578,
            17430.714677459066,
            3.631721349123526,
            1800,
            16783.16724483817,
            9.999999999999895,
            1678.5667244838169,
            2.2381643772125575
          ],
          [
            "FY2",
            180,
            120,
            11820,
            1400,
            1400,
            11388,
            1400,
            1336.496,
            0
          ],
          [
            "FY3",
            180,
            120,
            5820,
            -3000,
            700,
            5388,
            -3000,
            636.496,
            0
          ],
          [
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            null,
            "注：以x轴为正向，逆时针方向为正，取值0~360（度）。",
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ]
        ]
      },
      "formula_error_matches": 0
    },
    {
      "question_id": "Q5",
      "template": "result3.xlsx",
      "range": "A1:L18",
      "inspection": {
        "kind": "table",
        "sheet": "Sheet1",
        "address": "A1:L18",
        "rows": 18,
        "cols": 12,
        "values": [
          [
            "无人机编号",
            "无人机运动方向",
            "无人机运动速度 (m/s)",
            "烟幕干扰弹编号",
            "烟幕干扰弹投放点的x坐标 (m)",
            "烟幕干扰弹投放点的y坐标 (m)",
            "烟幕干扰弹投放点的z坐标 (m)",
            "烟幕干扰弹起爆点的x坐标 (m)",
            "烟幕干扰弹起爆点的y坐标 (m)",
            "烟幕干扰弹起爆点的z坐标 (m)",
            "有效干扰时长 (s)",
            "干扰的导弹编号"
          ],
          [
            "FY1",
            179.43654517246082,
            130.08336768519578,
            1,
            17430.714677459066,
            3.631721349123526,
            1800,
            16783.16724483817,
            9.999999999999895,
            1678.5667244838169,
            2.2381643772125575,
            "M1"
          ],
          [
            "FY1",
            null,
            null,
            2,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            "FY1",
            null,
            null,
            3,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            "FY2",
            275.5970977478011,
            100.88690594525764,
            1,
            12059.882666072617,
            788.9506205518344,
            1400,
            12094.869288158236,
            431.94324067868115,
            1338.051342375384,
            1.9820433139801334,
            "M2"
          ],
          [
            "FY2",
            null,
            null,
            2,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            "FY2",
            null,
            null,
            3,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            "FY3",
            null,
            null,
            1,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            "FY3",
            null,
            null,
            2,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            "FY3",
            null,
            null,
            3,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            "FY4",
            null,
            null,
            1,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            "FY4",
            null,
            null,
            2,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            "FY4",
            null,
            null,
            3,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            "FY5",
            119.30217914169313,
            121.14131300438812,
            1,
            12221.178713062363,
            -612.2804622520769,
            1300,
            12092.548732051975,
            -383.08495773506553,
            1276.935699494375,
            1.8768008708953303,
            "M3"
          ],
          [
            "FY5",
            null,
            null,
            2,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            "FY5",
            null,
            null,
            3,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ],
          [
            null,
            "注：以x轴为正向，逆时针方向为正，取值0~360（度）。",
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
          ]
        ]
      },
      "formula_error_matches": 0
    }
  ]
}


## `07_results/result_freeze_report.md`

# 结果冻结核验报告

## 状态

- 冻结包 ID：`RF-20260722T114756Z`
- 包状态：`ready`（待人工确认 `result_freeze_gate`）
- 人工闸门尚未由任何 AI 确认；下列数值不得在闸门确认前表述为最终提交结论。
- 来源：加密候选运行后，以 20×5×4 目标代表点、0.025 s 扫描和 1e-7 s 根定位容差独立复算。

## 主口径待冻结数值

| 问题 | 指标 | 数值 | 单位 |
|---|---|---:|---|
| Q1 | primary_duration_M1 | 1.362201500 | s |
| Q2 | primary_duration_M1 | 2.238164377 | s |
| Q3 | primary_duration_M1 | 2.238164377 | s |
| Q4 | primary_duration_M1 | 2.238164377 | s |
| Q5 | primary_duration_M1 | 2.238164377 | s |
| Q5 | primary_duration_M2 | 1.982043314 | s |
| Q5 | primary_duration_M3 | 1.876800871 | s |
| Q5 | objective_total_duration | 6.097008562 | s |
| Q5 | objective_minimum_duration | 1.876800871 | s |

## 核验结论

- 三个随机种子下每个输出的跨度为 0；加大搜索预算与加密采样仅产生数值积分层面的微小差异。
- 全部计划通过速度、起爆高度、投放间隔、Q3/Q4 结构和 Q5 前缀弹位约束检查；Q5 三个主目标均为正时长。
- 三份官方模板的映射检查为 `pass`，失败数为 `0`；未使用弹位均为空。
- Q3、Q4 的额外已用弹在当前候选中各自有效时长为 0，区间并集与 Q2 相同；该事实已保留在逐弹明细中，不宣称存在额外收益。

## 基线与敏感性（仅对照，不改写主模型）

- A03：取消投弹后水平速度继承时，当前计划的遮挡时长均为 0，说明结果对这一已人工确认的物理假设敏感。
- A07：烟幕到地面后停留的替代口径未改变当前遮挡区间。
- A08：中心点、80% 覆盖率与固定时间格点基线均已登记；主口径仍为全代表点遮挡和连续边界细化。
- A11：公平优先对照会改选 Q5 分配，主口径仍严格遵从已冻结的“总时长优先、最短时长次之”目标；该取舍不可由实现阶段静默替换。
- A12：取消“三目标均正时长”约束的对照没有改变总时长优先的分配。

## 产物与可追溯性

- 逐弹明细、指标表、模板映射和运行清单位于 `07_results/ready_for_freeze/`。
- 收敛、稳定性、基线与敏感性证据位于 `07_results/result_freeze_validation/`。
- 本报告、结果合同和产物登记均采用 `ready` 状态，等待人工闸门后才可视为正式冻结。


## `07_results/result_freeze_validation/baseline_and_sensitivity.csv`

﻿scenario,question_id,missile_id,metric_name,metric_value_s,merged_intervals,constraint_issues
baseline_center_point,Q1,M1,primary_duration_M1,1.4055095672607685,"[[8.013006067276041, 9.41851563453681]]",
baseline_center_point,Q2,M1,primary_duration_M1,2.2621874332428344,"[[7.817155600773029, 10.079343034015864]]",
baseline_center_point,Q3,M1,primary_duration_M1,2.2621874332428344,"[[7.817155600773029, 10.079343034015864]]",
baseline_center_point,Q4,M1,primary_duration_M1,2.2621874332428344,"[[7.817155600773029, 10.079343034015864]]",
baseline_center_point,Q5,M1,primary_duration_M1,2.2621874332428344,"[[7.817155600773029, 10.079343034015864]]",
baseline_center_point,Q5,M2,primary_duration_M2,2.4308256626129516,"[[9.641431898272616, 12.072257560885568]]",
baseline_center_point,Q5,M3,primary_duration_M3,1.9770526409148559,"[[15.30570047657822, 17.282753117493076]]",
baseline_fixed_grid,Q1,M1,primary_duration_M1,1.25,"[[8.1, 9.35]]",
baseline_fixed_grid,Q2,M1,primary_duration_M1,2.25,"[[7.817155600773029, 10.06715560077303]]",
baseline_fixed_grid,Q3,M1,primary_duration_M1,2.25,"[[7.817155600773029, 10.06715560077303]]",
baseline_fixed_grid,Q4,M1,primary_duration_M1,2.25,"[[7.817155600773029, 10.06715560077303]]",
baseline_fixed_grid,Q5,M1,primary_duration_M1,2.25,"[[7.817155600773029, 10.06715560077303]]",
baseline_fixed_grid,Q5,M2,primary_duration_M2,2.0,"[[9.641431898272616, 11.641431898272616]]",
baseline_fixed_grid,Q5,M3,primary_duration_M3,2.0,"[[15.30570047657822, 17.30570047657822]]",
A03_no_horizontal_inheritance,Q1,M1,primary_duration_M1,0,[],
A03_no_horizontal_inheritance,Q2,M1,primary_duration_M1,0,[],
A03_no_horizontal_inheritance,Q3,M1,primary_duration_M1,0,[],
A03_no_horizontal_inheritance,Q4,M1,primary_duration_M1,0,[],
A03_no_horizontal_inheritance,Q5,M1,primary_duration_M1,0,[],
A03_no_horizontal_inheritance,Q5,M2,primary_duration_M2,0,[],
A03_no_horizontal_inheritance,Q5,M3,primary_duration_M3,0,[],
A07_hold_smoke_at_ground,Q1,M1,primary_duration_M1,1.3622014999389869,"[[8.056308984756512, 9.4185104846955]]",
A07_hold_smoke_at_ground,Q2,M1,primary_duration_M1,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",
A07_hold_smoke_at_ground,Q3,M1,primary_duration_M1,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",
A07_hold_smoke_at_ground,Q4,M1,primary_duration_M1,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",
A07_hold_smoke_at_ground,Q5,M1,primary_duration_M1,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",
A07_hold_smoke_at_ground,Q5,M2,primary_duration_M2,1.9820433139801334,"[[9.641431898272616, 11.62347521225275]]",
A07_hold_smoke_at_ground,Q5,M3,primary_duration_M3,1.8768008708953303,"[[15.30570047657822, 17.18250134747355]]",
A08_80pct_coverage,Q1,M1,primary_duration_M1,1.3799813270569068,"[[8.038529825210613, 9.41851115226752]]",
A08_80pct_coverage,Q2,M1,primary_duration_M1,2.2513085842132856,"[[7.817155600773029, 10.068464184986315]]",
A08_80pct_coverage,Q3,M1,primary_duration_M1,2.2513085842132856,"[[7.817155600773029, 10.068464184986315]]",
A08_80pct_coverage,Q4,M1,primary_duration_M1,2.2513085842132856,"[[7.817155600773029, 10.068464184986315]]",
A08_80pct_coverage,Q5,M1,primary_duration_M1,2.2513085842132856,"[[7.817155600773029, 10.068464184986315]]",
A08_80pct_coverage,Q5,M2,primary_duration_M2,2.214444398880035,"[[9.641431898272616, 11.855876297152651]]",
A08_80pct_coverage,Q5,M3,primary_duration_M3,1.9317597866057739,"[[15.30570047657822, 17.237460263183994]]",


## `07_results/result_freeze_validation/convergence_and_stability.csv`

﻿scenario,question_id,metric_name,metric_value_s,seed,angular_samples,height_samples,radial_samples,scan_step_s,root_tolerance_s,maxiter,popsize,local_refinement
seed_20250722,Q1,primary_duration_M1,1.362402343749995,20250722,12,3,2,0.1,1e-05,6,5,True
seed_20250722,Q1,objective_1,1.362402343749995,20250722,12,3,2,0.1,1e-05,6,5,True
seed_20250722,Q2,primary_duration_M1,2.238162231445303,20250722,12,3,2,0.1,1e-05,6,5,True
seed_20250722,Q2,objective_1,2.238162231445303,20250722,12,3,2,0.1,1e-05,6,5,True
seed_20250722,Q3,primary_duration_M1,2.238162231445303,20250722,12,3,2,0.1,1e-05,6,5,True
seed_20250722,Q3,objective_1,2.238162231445303,20250722,12,3,2,0.1,1e-05,6,5,True
seed_20250722,Q4,primary_duration_M1,2.238162231445303,20250722,12,3,2,0.1,1e-05,6,5,True
seed_20250722,Q4,objective_1,2.238162231445303,20250722,12,3,2,0.1,1e-05,6,5,True
seed_20250722,Q5,primary_duration_M1,2.238162231445303,20250722,12,3,2,0.1,1e-05,6,5,True
seed_20250722,Q5,primary_duration_M2,1.9820404052734322,20250722,12,3,2,0.1,1e-05,6,5,True
seed_20250722,Q5,primary_duration_M3,1.8768035888672046,20250722,12,3,2,0.1,1e-05,6,5,True
seed_20250722,Q5,objective_1,6.09700622558594,20250722,12,3,2,0.1,1e-05,6,5,True
seed_20250722,Q5,objective_2,1.8768035888672046,20250722,12,3,2,0.1,1e-05,6,5,True
seed_20250723,Q1,primary_duration_M1,1.362402343749995,20250723,12,3,2,0.1,1e-05,6,5,True
seed_20250723,Q1,objective_1,1.362402343749995,20250723,12,3,2,0.1,1e-05,6,5,True
seed_20250723,Q2,primary_duration_M1,2.238162231445303,20250723,12,3,2,0.1,1e-05,6,5,True
seed_20250723,Q2,objective_1,2.238162231445303,20250723,12,3,2,0.1,1e-05,6,5,True
seed_20250723,Q3,primary_duration_M1,2.238162231445303,20250723,12,3,2,0.1,1e-05,6,5,True
seed_20250723,Q3,objective_1,2.238162231445303,20250723,12,3,2,0.1,1e-05,6,5,True
seed_20250723,Q4,primary_duration_M1,2.238162231445303,20250723,12,3,2,0.1,1e-05,6,5,True
seed_20250723,Q4,objective_1,2.238162231445303,20250723,12,3,2,0.1,1e-05,6,5,True
seed_20250723,Q5,primary_duration_M1,2.238162231445303,20250723,12,3,2,0.1,1e-05,6,5,True
seed_20250723,Q5,primary_duration_M2,1.9820404052734322,20250723,12,3,2,0.1,1e-05,6,5,True
seed_20250723,Q5,primary_duration_M3,1.8768035888672046,20250723,12,3,2,0.1,1e-05,6,5,True
seed_20250723,Q5,objective_1,6.09700622558594,20250723,12,3,2,0.1,1e-05,6,5,True
seed_20250723,Q5,objective_2,1.8768035888672046,20250723,12,3,2,0.1,1e-05,6,5,True
seed_20250724,Q1,primary_duration_M1,1.362402343749995,20250724,12,3,2,0.1,1e-05,6,5,True
seed_20250724,Q1,objective_1,1.362402343749995,20250724,12,3,2,0.1,1e-05,6,5,True
seed_20250724,Q2,primary_duration_M1,2.238162231445303,20250724,12,3,2,0.1,1e-05,6,5,True
seed_20250724,Q2,objective_1,2.238162231445303,20250724,12,3,2,0.1,1e-05,6,5,True
seed_20250724,Q3,primary_duration_M1,2.238162231445303,20250724,12,3,2,0.1,1e-05,6,5,True
seed_20250724,Q3,objective_1,2.238162231445303,20250724,12,3,2,0.1,1e-05,6,5,True
seed_20250724,Q4,primary_duration_M1,2.238162231445303,20250724,12,3,2,0.1,1e-05,6,5,True
seed_20250724,Q4,objective_1,2.238162231445303,20250724,12,3,2,0.1,1e-05,6,5,True
seed_20250724,Q5,primary_duration_M1,2.238162231445303,20250724,12,3,2,0.1,1e-05,6,5,True
seed_20250724,Q5,primary_duration_M2,1.9820404052734322,20250724,12,3,2,0.1,1e-05,6,5,True
seed_20250724,Q5,primary_duration_M3,1.8768035888672046,20250724,12,3,2,0.1,1e-05,6,5,True
seed_20250724,Q5,objective_1,6.09700622558594,20250724,12,3,2,0.1,1e-05,6,5,True
seed_20250724,Q5,objective_2,1.8768035888672046,20250724,12,3,2,0.1,1e-05,6,5,True
budget_plus,Q1,primary_duration_M1,1.362402343749995,20250722,12,3,2,0.1,1e-05,12,8,True
budget_plus,Q1,objective_1,1.362402343749995,20250722,12,3,2,0.1,1e-05,12,8,True
budget_plus,Q2,primary_duration_M1,2.238162231445303,20250722,12,3,2,0.1,1e-05,12,8,True
budget_plus,Q2,objective_1,2.238162231445303,20250722,12,3,2,0.1,1e-05,12,8,True
budget_plus,Q3,primary_duration_M1,2.238162231445303,20250722,12,3,2,0.1,1e-05,12,8,True
budget_plus,Q3,objective_1,2.238162231445303,20250722,12,3,2,0.1,1e-05,12,8,True
budget_plus,Q4,primary_duration_M1,2.238162231445303,20250722,12,3,2,0.1,1e-05,12,8,True
budget_plus,Q4,objective_1,2.238162231445303,20250722,12,3,2,0.1,1e-05,12,8,True
budget_plus,Q5,primary_duration_M1,2.238162231445303,20250722,12,3,2,0.1,1e-05,12,8,True
budget_plus,Q5,primary_duration_M2,1.9820404052734322,20250722,12,3,2,0.1,1e-05,12,8,True
budget_plus,Q5,primary_duration_M3,1.8768035888672046,20250722,12,3,2,0.1,1e-05,12,8,True
budget_plus,Q5,objective_1,6.09700622558594,20250722,12,3,2,0.1,1e-05,12,8,True
budget_plus,Q5,objective_2,1.8768035888672046,20250722,12,3,2,0.1,1e-05,12,8,True
refined,Q1,primary_duration_M1,1.3624053955078335,20250722,16,4,3,0.05,1e-06,12,8,True
refined,Q1,objective_1,1.3624053955078335,20250722,16,4,3,0.05,1e-06,12,8,True
refined,Q2,primary_duration_M1,2.238164138793973,20250722,16,4,3,0.05,1e-06,12,8,True
refined,Q2,objective_1,2.238164138793973,20250722,16,4,3,0.05,1e-06,12,8,True
refined,Q3,primary_duration_M1,2.238164138793973,20250722,16,4,3,0.05,1e-06,12,8,True
refined,Q3,objective_1,2.238164138793973,20250722,16,4,3,0.05,1e-06,12,8,True
refined,Q4,primary_duration_M1,2.238164138793973,20250722,16,4,3,0.05,1e-06,12,8,True
refined,Q4,objective_1,2.238164138793973,20250722,16,4,3,0.05,1e-06,12,8,True
refined,Q5,primary_duration_M1,2.238164138793973,20250722,16,4,3,0.05,1e-06,12,8,True
refined,Q5,primary_duration_M2,1.9820430755615526,20250722,16,4,3,0.05,1e-06,12,8,True
refined,Q5,primary_duration_M3,1.876800918579125,20250722,16,4,3,0.05,1e-06,12,8,True
refined,Q5,objective_1,6.097008132934651,20250722,16,4,3,0.05,1e-06,12,8,True
refined,Q5,objective_2,1.876800918579125,20250722,16,4,3,0.05,1e-06,12,8,True


## `07_results/result_freeze_validation/plan_validation.csv`

﻿question_id,uav_id,bomb_id,is_used,missile_id,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,effective_duration_s,occlusion_intervals,constraint_issues
Q1,FY1,1,1,M1,180.0,120.0,1.5,3.6,5.1,1.3622014999389869,"[[8.056308984756512, 9.4185104846955]]",
Q2,FY1,1,1,M1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",
Q3,FY1,1,1,M1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",
Q3,FY1,2,1,M1,179.43654517246082,130.08336768519578,3.838973088474825,4.978182512298204,8.81715560077303,0,[],
Q3,FY1,3,1,M1,179.43654517246082,130.08336768519578,4.838973088474825,4.978182512298204,9.81715560077303,0,[],
Q4,FY1,1,1,M1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",
Q4,FY2,1,1,M1,180.0,120.0,1.5,3.6,5.1,0,[],
Q4,FY3,1,1,M1,180.0,120.0,1.5,3.6,5.1,0,[],
Q5,FY1,1,1,M1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",
Q5,FY1,2,0,,,,,,,,[],
Q5,FY1,3,0,,,,,,,,[],
Q5,FY2,1,1,M2,275.5970977478011,100.88690594525764,6.0857908606118745,3.555641037660742,9.641431898272616,1.9820433139801334,"[[9.641431898272616, 11.62347521225275]]",
Q5,FY2,2,0,,,,,,,,[],
Q5,FY2,3,0,,,,,,,,[],
Q5,FY3,1,0,,,,,,,,[],
Q5,FY3,2,0,,,,,,,,[],
Q5,FY3,3,0,,,,,,,,[],
Q5,FY4,1,0,,,,,,,,[],
Q5,FY4,2,0,,,,,,,,[],
Q5,FY4,3,0,,,,,,,,[],
Q5,FY5,1,1,M3,119.30217914169313,121.14131300438812,13.136138284985464,2.1695621915927563,15.30570047657822,1.8768008708953303,"[[15.30570047657822, 17.18250134747355]]",
Q5,FY5,2,0,,,,,,,,[],
Q5,FY5,3,0,,,,,,,,[],


## `07_results/result_freeze_validation/primary_recomputation.csv`

﻿scenario,question_id,missile_id,metric_name,metric_value_s,merged_intervals,constraint_issues
primary_strict_recomputation,Q1,M1,primary_duration_M1,1.3622014999389869,"[[8.056308984756512, 9.4185104846955]]",
primary_strict_recomputation,Q2,M1,primary_duration_M1,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",
primary_strict_recomputation,Q3,M1,primary_duration_M1,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",
primary_strict_recomputation,Q4,M1,primary_duration_M1,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",
primary_strict_recomputation,Q5,M1,primary_duration_M1,2.2381643772125575,"[[7.817155600773029, 10.055319977985587]]",
primary_strict_recomputation,Q5,M2,primary_duration_M2,1.9820433139801334,"[[9.641431898272616, 11.62347521225275]]",
primary_strict_recomputation,Q5,M3,primary_duration_M3,1.8768008708953303,"[[15.30570047657822, 17.18250134747355]]",


## `07_results/result_freeze_validation/q5_assignment_sensitivity.csv`

﻿variant,assignment,total_duration_s,minimum_duration_s,require_positive,priority
A11_primary_total_then_min,"{""M1"": ""FY1"", ""M2"": ""FY2"", ""M3"": ""FY5""}",6.097008132934651,1.876800918579125,True,total_then_min
A11_fairness_first,"{""M1"": ""FY1"", ""M2"": ""FY4"", ""M3"": ""FY2""}",6.080231857299891,1.908269119262723,True,min_then_total
A12_relaxed_positive_coverage,"{""M1"": ""FY1"", ""M2"": ""FY2"", ""M3"": ""FY5""}",6.097008132934651,1.876800918579125,False,total_then_min


## `07_results/result_freeze_validation/runs/budget_plus/candidate_run_manifest.json`

{
  "generated_at": "2026-07-22T11:41:58.490751+00:00",
  "result_status": "candidate",
  "mode": "quick",
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
      "root_tolerance_s": 1e-05,
      "gravity_mps2": 9.8,
      "bomb_horizontal_velocity_factor": 1.0,
      "smoke_ground_mode": "terminate",
      "interval_method": "refined",
      "min_coverage_fraction": 1.0
    },
    "differential_evolution_maxiter": 12,
    "differential_evolution_popsize": 8,
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
    "q5_credit_policy": "primary_target_only",
    "score_matrix": [
      {
        "uav_id": "FY1",
        "missile_id": "M1",
        "effective_duration_s": 2.238162231445303
      },
      {
        "uav_id": "FY1",
        "missile_id": "M2",
        "effective_duration_s": 0
      },
      {
        "uav_id": "FY1",
        "missile_id": "M3",
        "effective_duration_s": 0
      },
      {
        "uav_id": "FY2",
        "missile_id": "M1",
        "effective_duration_s": 2.0354522705078057
      },
      {
        "uav_id": "FY2",
        "missile_id": "M2",
        "effective_duration_s": 1.9820404052734322
      },
      {
        "uav_id": "FY2",
        "missile_id": "M3",
        "effective_duration_s": 1.9082672119140547
      },
      {
        "uav_id": "FY3",
        "missile_id": "M1",
        "effective_duration_s": 1.5796417236328395
      },
      {
        "uav_id": "FY3",
        "missile_id": "M2",
        "effective_duration_s": 1.4996856689453288
      },
      {
        "uav_id": "FY3",
        "missile_id": "M3",
        "effective_duration_s": 1.545223999023463
      },
      {
        "uav_id": "FY4",
        "missile_id": "M1",
        "effective_duration_s": 1.942984008789093
      },
      {
        "uav_id": "FY4",
        "missile_id": "M2",
        "effective_duration_s": 1.9337982177734325
      },
      {
        "uav_id": "FY4",
        "missile_id": "M3",
        "effective_duration_s": 1.819174194335961
      },
      {
        "uav_id": "FY5",
        "missile_id": "M1",
        "effective_duration_s": 1.9742156982422188
      },
      {
        "uav_id": "FY5",
        "missile_id": "M2",
        "effective_duration_s": 1.8203033447265824
      },
      {
        "uav_id": "FY5",
        "missile_id": "M3",
        "effective_duration_s": 1.8768035888672046
      }
    ]
  },
  "notice": "Candidate artifacts are not result-freeze outputs and are not registered in result_contract.csv."
}


## `07_results/result_freeze_validation/runs/budget_plus/metrics_summary.csv`

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


## `07_results/result_freeze_validation/runs/budget_plus/q1_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q1,FY1,1,M1,1,180.0,120.0,1.5,3.6,5.1,17620.0,0.0,1800.0,17188.0,0.0,1736.496,1.362402343749995,"[[8.056106567382802, 9.418508911132797]]",candidate


## `07_results/result_freeze_validation/runs/budget_plus/q2_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q2,FY1,1,M1,1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,17430.714677459066,3.631721349123526,1800.0,16783.16724483817,9.999999999999895,1678.5667244838169,2.238162231445303,"[[7.817155600773029, 10.055317832218332]]",candidate


## `07_results/result_freeze_validation/runs/budget_plus/q3_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q3,FY1,1,M1,1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,17430.714677459066,3.631721349123526,1800.0,16783.16724483817,9.999999999999895,1678.5667244838169,2.238162231445303,"[[7.817155600773029, 10.055317832218332]]",candidate
Q3,FY1,2,M1,1,179.43654517246082,130.08336768519578,3.838973088474825,4.978182512298204,8.81715560077303,17300.637599927017,4.910959029771843,1800.0,16653.09016730612,11.279237680648212,1678.5667244838169,0,[],candidate
Q3,FY1,3,M1,1,179.43654517246082,130.08336768519578,4.838973088474825,4.978182512298204,9.81715560077303,17170.56052239497,6.19019671042016,1800.0,16523.013089774075,12.55847536129653,1678.5667244838169,0,[],candidate


## `07_results/result_freeze_validation/runs/budget_plus/q4_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q4,FY1,1,M1,1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,17430.714677459066,3.631721349123526,1800.0,16783.16724483817,9.999999999999895,1678.5667244838169,2.238162231445303,"[[7.817155600773029, 10.055317832218332]]",candidate
Q4,FY2,1,M1,1,180.0,120.0,1.5,3.6,5.1,11820.0,1400.0,1400.0,11388.0,1400.0,1336.496,0,[],candidate
Q4,FY3,1,M1,1,180.0,120.0,1.5,3.6,5.1,5820.0,-3000.0,700.0,5388.0,-3000.0,636.496,0,[],candidate


## `07_results/result_freeze_validation/runs/budget_plus/q5_results.csv`

﻿question_id,uav_id,bomb_id,missile_id,is_used,heading_deg,speed_mps,release_time_s,delay_s,detonation_time_s,release_x_m,release_y_m,release_z_m,detonation_x_m,detonation_y_m,detonation_z_m,effective_duration_s,occlusion_intervals,result_status
Q5,FY1,1,M1,1,179.43654517246082,130.08336768519578,2.838973088474825,4.978182512298204,7.817155600773029,17430.714677459066,3.631721349123526,1800.0,16783.16724483817,9.999999999999895,1678.5667244838169,2.238162231445303,"[[7.817155600773029, 10.055317832218332]]",candidate
Q5,FY1,2,,0,,,,,,,,,,,,,[],candidate
Q5,FY1,3,,0,,,,,,,,,,,,,[],candidate
Q5,FY2,1,M2,1,275.5970977478011,100.88690594525764,6.0857908606118745,3.555641037660742,9.641431898272616,12059.882666072617,788.9506205518344,1400.0,12094.869288158236,431.94324067868115,1338.051342375384,1.9820404052734322,"[[9.641431898272616, 11.623472303546048]]",candidate
Q5,FY2,2,,0,,,,,,,,,,,,,[],candidate
Q5,FY2,3,,0,,,,,,,,,,,,,[],candidate
Q5,FY3,1,,0,,,,,,,,,,,,,[],candidate
Q5,FY3,2,,0,,,,,,,,,,,,,[],candidate
Q5,FY3,3,,0,,,,,,,,,,,,,[],candidate
Q5,FY4,1,,0,,,,,,,,,,,,,[],candidate
Q5,FY4,2,,0,,,,,,,,,,,,,[],candidate
Q5,FY4,3,,0,,,,,,,,,,,,,[],candidate
Q5,FY5,1,M3,1,119.30217914169313,121.14131300438812,13.136138284985464,2.1695621915927563,15.30570047657822,12221.178713062363,-612.2804622520769,1300.0,12092.548732051975,-383.08495773506553,1276.935699494375,1.8768035888672046,"[[15.30570047657822, 17.182504065445425]]",candidate
Q5,FY5,2,,0,,,,,,,,,,,,,[],candidate
Q5,FY5,3,,0,,,,,,,,,,,,,[],candidate


## `07_results/result_freeze_validation/runs/budget_plus/result_source_map.csv`

﻿result_id,question_id,source_file,result_status,generated_by
candidate_q1,Q1,07_results/q1_results.csv,candidate,06_code/run_all.py
candidate_q2,Q2,07_results/q2_results.csv,candidate,06_code/run_all.py
candidate_q3,Q3,07_results/q3_results.csv,candidate,06_code/run_all.py
candidate_q4,Q4,07_results/q4_results.csv,candidate,06_code/run_all.py
candidate_q5,Q5,07_results/q5_results.csv,candidate,06_code/run_all.py

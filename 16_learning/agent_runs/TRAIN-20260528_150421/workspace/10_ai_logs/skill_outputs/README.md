# 技能输出归档

本目录是专家技能调用的 P1 归档层。

专家技能不得直接写入工作流合同、冻结产物、终稿论文、脚本或工作流状态。每次技能调用必须先归档到这里，之后只有在通过校验且必要时得到人工确认后，才允许晋升到下游使用。

## 标准归档路径

```text
10_ai_logs/skill_outputs/<stage_id>/<skill_id>/<call_id>/
```

每个调用目录必须包含：

```text
input_manifest.yaml
raw_output.md
promotion_notes.md
```

推荐的可选文件：

```text
policy_snapshot.yaml
contract_snapshot_refs.md
validation_stdout.txt
validation_stderr.txt
human_decision.md
```

## 调用目录命名

使用稳定的调用 ID：

```text
SKILL-<stage_id>-<skill_id>-<YYYYMMDDTHHMMSSZ>
```

示例：

```text
10_ai_logs/skill_outputs/figures/nature-figure/SKILL-figures-nature-figure-20260523T132000Z/
```

## 晋升规则

技能原始输出只具有建议性质。只有当晋升说明记录以下信息后，它才可以进入下游使用：

1. 输出类型；
2. 目标文件；
3. 合同绑定；
4. 校验状态；
5. 必要时的人工决定。

没有晋升说明，就不得下游使用。

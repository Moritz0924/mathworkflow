# Reproducibility Risks

| Risk ID | Description | Severity | Mitigation |
|---------|-------------|----------|-----------|
| R1 | Raw data files missing | CRITICAL | Human upload of original files; hash verification after placement |
| R2 | No documented data provenance | HIGH | Request source description and collection method from problem statement |
| R3 | Field semantics unknown | HIGH | Provide data dictionary template; require human annotation |
| R4 | Exploratory code not executed | HIGH | Run `04_eda_code/eda_check.py` once data is available |

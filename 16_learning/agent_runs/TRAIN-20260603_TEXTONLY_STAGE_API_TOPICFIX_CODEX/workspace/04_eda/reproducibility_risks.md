# Reproducibility Risks

| Risk ID | Description | Severity | Mitigation |
|---|---|---|---|
| R01 | Data source provenance lacking (no data paper, no official release notes) | Medium | Treat as competition dataset; document assumptions in model contract |
| R02 | Missing `weight_per_unit` in 12% of inventory may bias energy consumption models | Medium | Use median imputation per SKU category; sensitivity analysis |
| R03 | Negative lead times in 3 orders indicate data entry error | High | Exclude or correct after human confirmation |
| R04 | Two AGVs with speed=0: are they out-of-service? | Medium | Flag and exclude from fleet if confirmed |
| R05 | Warehouse map coordinate system not explicitly anchored to real-world units | Low | Assumed meters based on scale |
| R06 | No explicit record of battery consumption model (discharge rate, recharge rate) | High | Need to request or derive from physical specs |
| R07 | Zero-stock SKU conflict may require dynamic restock logic; data static | Medium | Discuss as model assumption |
| R08 | EDA code not version-controlled; results could drift if data updated | Low | Use scripts in `04_eda_code/` with pinned data |
| R09 | `deadline` field may be in local timezone without offset – timezone handling ambiguous | Low | Assume UTC+8; confirm |

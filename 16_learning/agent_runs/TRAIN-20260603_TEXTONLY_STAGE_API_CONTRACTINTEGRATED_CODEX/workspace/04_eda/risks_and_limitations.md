# Risks and Limitations

1. **Data Accessibility:** The primary risk is that the EDA agent cannot access any data files. All subsequent stages depend on this resolution.
2. **Field Interpretation:** Without human-provided data dictionaries, field meanings may be misinterpreted.
3. **Unit Ambiguity:** Numerical columns might have differing units across sources; no checks possible now.
4. **Sample Size and Imbalance:** Unknown until data inspection.
5. **Missing Values:** Extent and pattern unknown.
6. **Temporal/Geographical Leakage:** Cannot assess.
7. **Reproducibility:** EDA scripts cannot be tested without data.

**Mitigation:** Do not proceed to `task_analysis` or `model_route` until human gate confirms data availability and provides at least a basic schema description.

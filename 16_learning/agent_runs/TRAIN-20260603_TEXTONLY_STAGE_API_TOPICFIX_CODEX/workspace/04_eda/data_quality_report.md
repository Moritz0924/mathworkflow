# Data Quality Report

## 1. Completeness
- `orders.csv`: 0.2% missing in `deadline`, 0.5% in `priority`; remaining fields full.
- `agv_status.csv`: 2.3% missing `battery_level`, 0.5% `status`.
- `inventory.csv`: 12% missing `weight_per_unit`.

## 2. Consistency
- Coordinates in orders and inventory are within map bounds (0-50, 0-30).
- AGV initial positions all within map bounds.
- `deadline` times are chronologically after `created_at` for 99.8% records; 3 records violate this (negative lead time).
- `priority` values range from 1 to 3, no unexpected codes.

## 3. Uniqueness
- No duplicate order_ids.
- No duplicate agv_ids.
- sku_id references in orders all exist in inventory.

## 4. Validity
- `speed` values appear valid (0.5-2.0 m/s).
- `battery_level` capped at 100% but one record at 105% (likely rounding error).
- `quantity` ranges 1-50; no negative values.

## 5. Outliers
- Two AGVs have speed = 0.0 (possible stationary/not operational).
- One inventory entry has stock = 0 but orders reference that SKU (requires checking order timestamps vs stock depletion).
- Three orders have a lead time (deadline - created_at) less than 0 (data errors).

## 6. Distributions
- `pick_x`, `pick_y`: Approximately uniform across warehouse area, slight concentration near packing station (10,15).
- `deadline` times cluster around working hours.
- `priority` distribution: 20% urgent, 50% normal, 30% low.
- `quantity` skewed right (most orders 1-5 items).

## 7. Correlation Hazards
- `battery_level` weakly negatively correlated with distance from charging station (as expected).
- No unexpected strong correlations among numerical fields.

## 8. Data Leakage Risk
- `deadline` used as target for scheduling? It is future information relative to `created_at`, so no leakage if used properly in optimization, but caution needed in any predictive model.

## 9. Units & Scale
- All coordinates in meters, weights in kg, distances consistent.
- No mixed units detected.

## 10. Recommendations
- Impute or flag missing `battery_level` before modeling.
- Exclude or correct the 3 orders with negative lead time.
- Confirm operational status of AGVs with speed=0.
- Address stock=0 SKU conflict before constructing schedule.

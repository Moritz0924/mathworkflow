# Data Dictionary

## orders.csv

| Field | Type | Unit | Description | Missing Rate | Notes |
|---|---|---|---|---|---|
| order_id | str | - | Unique order identifier | 0% | Primary key |
| pick_x | float | meter | X coordinate of pick location | 0% | Range 0-50m |
| pick_y | float | meter | Y coordinate of pick location | 0% | Range 0-30m |
| deadline | datetime | ISO 8601 | Order completion deadline | 0.2% | Timezone: UTC+8 |
| priority | int | category | 1=urgent, 2=normal, 3=low | 0.5% | Encoded as integer |
| sku_id | str | - | Stock Keeping Unit identifier | 0% | Links to inventory |
| quantity | int | pieces | Number of items to pick | 0% | Values 1-50 |
| created_at | datetime | ISO 8601 | Order creation timestamp | 0% | |

## agv_status.csv

| Field | Type | Unit | Description | Missing Rate | Notes |
|---|---|---|---|---|---|
| agv_id | str | - | AGV identifier | 0% | Primary key |
| initial_x | float | meter | Initial X coordinate | 0% | Range 0-50 |
| initial_y | float | meter | Initial Y coordinate | 0% | Range 0-30 |
| speed | float | m/s | Maximum travel speed | 0% | Values 0.5-2.0 |
| battery_capacity | int | mAh | Maximum battery capacity | 0% | Values 5000-10000 |
| battery_level | float | % | Current battery level | 2.3% | Some missing; treated as median |
| status | str | - | idle, moving, charging, error | 0.5% | |

## warehouse_map.json

| Key | Type | Description |
|---|---|---|
| grid_width | int | Total grid columns |
| grid_height | int | Total grid rows |
| aisles | list of tuples | (row, col_start, col_end) defining walkable lanes |
| obstacles | list of tuples | (row, col) blocked cells |
| stations | object | Keyed by id: {type: 'charge'|'packing', pos: [x,y]} |

## inventory.csv

| Field | Type | Description | Missing Rate |
|---|---|---|---|
| sku_id | str | SKU identifier | 0% |
| storage_x | float | Storage bay X | 0% |
| storage_y | float | Storage bay Y | 0% |
| shelf_level | int | Vertical shelf level 1-3 | 0% |
| stock | int | Available pieces | 0% |
| weight_per_unit | float | kg | Weight per piece | 12% missing |

## Data Version
- Data snapshot: 2025-06-01T00:00:00Z
- Source: provided competition data (no provenance document)
- Encoding: UTF-8
- Delimiter: comma
- Missing value representation: empty field or 'NA'

# Symbols Glossary

## Conventions
- Subscripts: `t` = time period (week), `p` = product index.
- Greek letters denote parameters; Roman letters denote variables unless specified.

## Sub-Problem 1: Sales Forecasting
| Symbol | Name | Type | Unit | Definition |
|--------|------|------|------|------------|
| `y_t` | Sales quantity | variable | units | Observed sales in week t |
| `ŷ_t` | Predicted sales | variable | units | Model forecast for week t |
| `promo_t` | Promotion indicator | exogenous | 0/1 | 1 if promotion active in week t |
| `holiday_t` | Holiday indicator | exogenous | 0/1 | 1 if week contains a major holiday |
| `ε_t` | White noise error | random | units | i.i.d. N(0, σ²) |
| `φ_i` | AR coefficient | parameter | dimensionless | Coefficient for lag i |
| `θ_j` | MA coefficient | parameter | dimensionless | Coefficient for lag j |
| `B` | Backshift operator | operator | - | B y_t = y_{t-1} |
| `d` | Differencing order | hyperparameter | - | Order of non-seasonal differencing |
| `D` | Seasonal differencing order | hyperparameter | - | Order of seasonal differencing |
| `m` | Seasonal period | hyperparameter | weeks | 52 for weekly data |
| `σ²` | Error variance | parameter | units² | Variance of ε_t |

## Sub-Problem 2: Inventory Optimization
| Symbol | Name | Type | Unit | Definition |
|--------|------|------|------|------------|
| `x_{p,t}` | Order quantity | variable | units | Amount ordered for product p to arrive at start of t |
| `I_{p,t}` | Inventory level | variable | units | Inventory of product p at end of t |
| `δ_{p,t}` | Ordering indicator | variable | binary | 1 if order placed for p in t |
| `D_{p,t}` | Demand | parameter | units | Forecast demand (from SP1) |
| `h_p` | Holding cost | parameter | $/(unit·week) | Cost to hold one unit for one week |
| `o_p` | Ordering cost | parameter | $/order | Fixed cost per order placed |
| `s_p` | Shortage cost | parameter | $/unit | Penalty for each unit of unmet demand |
| `L_p` | Lead time | parameter | weeks | Time between order and receipt |
| `W` | Warehouse capacity | parameter | units | Maximum total inventory across products |
| `C` | Total cost | objective | $ | Sum of holding, ordering, shortage costs |
| `I_0` | Initial inventory | parameter | units | Starting inventory before planning horizon |

## Common
| Symbol | Name | Type | Unit | Definition |
|--------|------|------|------|------------|
| `H` | Planning horizon | constant | weeks | Number of weeks considered |
| `P` | Number of products | constant | - | Cardinality of product set |

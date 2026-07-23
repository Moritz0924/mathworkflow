# 证据设计生成与质量报告

- 冻结包：`RF-20260722T114756Z`
- 输入范围：`07_results/frozen/` 与 `07_results/result_freeze_validation/` 的已登记核验文件。
- 生成代码：`06_code/generate_evidence.py`（Matplotlib 3.9.2，PNG 300 dpi + SVG）。
- 正式图：11 张；正式表：9 张；正式论断：10 条。
- 当前状态：`ready`，仍须由人工完成 `evidence_gate`，本报告不代表闸门已确认。

## 自动检查

- 图表输出同时存在 PNG 和 SVG；图表合同仅引用已存在的 `RES-*` 冻结结果编号。
- Q3/F004 和 Q4/F005 保留零贡献行，未将参与投放表述为额外收益。
- F006 仅绘制冻结 Q5 中已使用的 FY1-b1、FY2-b1、FY5-b1 三条边。
- F007 保留三段时间轴间隙；F009–F011 将验证情景限定为其登记来源。

## 文件指纹

| figure_id | PNG SHA-256 | SVG SHA-256 |
|---|---|---|
| F001 | `b3793c50c72a095d0f958924cf20d1e986c8448c2021c30026a11654a296e28c` | `ca1d5f110eeadc7f2356c880cb7d7509c1b6e316c4b66aba091bfd43d228e88f` |
| F002 | `51ae8128632c3ed265024e2867d94c1810de814ec81dc241d8f43d54c9b41ad8` | `6442e4baecc6df7ad17a78d8a0ab3f4e9aa2856b7a4236ed695182e9a8725e4c` |
| F003 | `8ead2f79c283360758109c20fcff5a29d94ad6165538001905070eb694ce3ed8` | `23059d3f9e661a4c64c3d6b0da5ab57eb290639e5ff57906962387d3a8d10106` |
| F004 | `9eb130aaae9b939a421037da0e7bc5c9ebc87329ad966d9a7325f84f0efa2d82` | `e775e2f13f8ca491835b8cdbb429f4f58c3b88034279d4202a99e97456ecf0e6` |
| F005 | `3df125ba111c4d7ef90632303f6d9590acaa8c22a8c4a713ef3ebe45ece4f725` | `019b864cbb7d5e78663e469d51afb6cddf5e5fab467748a2b3f720cae7fb4dd1` |
| F006 | `98c2a8997f7629cd4aec53f01d0f68003512210b0a44a5324fd2f8df51c6eeed` | `16b3e9f4ec95c6854535713eb641b3be7540d49b8dad1d622bed662fabfa24cf` |
| F007 | `221d96d1793987bf71a79beb245a0f6e8e945bcd3139534327de25a4bd065fe0` | `fde4ac1639023d1b9916629387e1622041f0a0b36e6a8315f1c7ac98b2bbb042` |
| F008 | `1b07b6dd10fec16115343766d7b72276170c8e2cfe7a00910623bd6bf6bc91c0` | `802a7088eac26a0bc15a628fcf4812dd7fd4a0a15ca1c0825ad38332d70f5f4a` |
| F009 | `c313cffcc48745efb15068a03af196cfb3b96374a39aa0512ae2335d7896cb1a` | `a7b7f151db70b20d7414b640ac185a4baea3b38c1f417745c1160b4615609fb3` |
| F010 | `ca5b5282b8cee48419d8af83a359480ec8344cef730df6985a1d44878d2f1ae0` | `4ec4e05ebe1033419f6184393b8e5220cc79071e9d389a681188091d3da7e007` |
| F011 | `943ded39a62f3ee770afb13b50f2220599fc04842cb1cd5b61033b4387e933f0` | `6e3b314a5b6f562fca3bf602d99510e556aa86e64413309f1696a8036bbbe011` |

## 图表边界

- 任何论文表述必须沿用 `14_contracts/claim_evidence_map.csv` 中的边界条件。
- 图表不声明全局最优，也不为未验证的情景新增结论。

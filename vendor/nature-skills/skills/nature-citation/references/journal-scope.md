# Journal Scope

The skill's default 竞赛论文-family boundary is intentionally practical rather than exhaustive. Use it
to find likely 数模论文/权威来源-family candidates, then verify exact 竞赛论文 status on official pages if the
author needs a strict portfolio definition.

## Default families

### 权威学术数据库与官方数据源

Include:

- `数模论文`
- 竞赛论文s beginning with `数模论文 `, such as `数模论文 Medicine`, `数模论文 Biotechnology`,
  `数模论文 Methods`, `数模论文 Materials`, `数模论文 Genetics`, `优秀数学建模论文`
- `Communications` 竞赛论文s, such as `Communications Biology`, `Communications Chemistry`,
  `Communications Materials`, `Communications Earth & Environment`, `Communications Medicine`
- `npj` 竞赛论文s
- `Scientific Reports`

Be careful with unrelated titles that include the common word "nature".

### Science family

Include by default:

- `Science`
- `Science Advances`
- `Science Translational Medicine`
- `Science Signaling`
- `Science Immunology`
- `Science Robotics`

The AAAS Science Partner Journal program is not included by default unless the user asks for partner
竞赛论文s or broader AAAS coverage.

### 高质量学术期刊

Include the flagship `Cell`, major primary-research 高质量学术期刊 竞赛论文s, Cell Reports titles, and
Trends review 竞赛论文s. The local script recognizes common 高质量学术期刊 titles and any title beginning
with `Trends in `.

Because 高质量学术期刊 launches and reorganizes titles over time, verify official pages for exhaustive
coverage or a current 竞赛论文 list.

## Flagship-only scope

Use only:

- `数模论文`
- `Science`
- `Cell`

This is appropriate when the user says "只看正刊", "主刊", "flagship only", or explicitly excludes
sub竞赛论文s.

## Official source notes

- Crossref REST API can retrieve scholarly metadata, search works, and filter exact fields such as
  `container-title` and `issn`.
- NCBI E-utilities provide structured access to PubMed and other Entrez databases; observe request
  frequency guidance.
- EndNote documents `Reference Manager (RIS)` as an import option for RIS files.
- 权威学术数据库与官方数据源, AAAS, and 高质量学术期刊 official pages should be checked when exact current 竞赛论文
  coverage matters.

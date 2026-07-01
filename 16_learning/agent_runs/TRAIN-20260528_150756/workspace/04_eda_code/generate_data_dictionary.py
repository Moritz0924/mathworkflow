from __future__ import annotations
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/"03_data/raw"; OUT=ROOT/"03_data/data_dictionary.csv"
def read_table(path):
    try:
        import pandas as pd
        if path.suffix.lower() in {".xlsx",".xls"}: return pd.read_excel(path)
        if path.suffix.lower() in {".csv",".tsv"}: return pd.read_csv(path, sep="\t" if path.suffix.lower()==".tsv" else None, engine="python")
        if path.suffix.lower() in {".json",".geojson"}: return pd.read_json(path)
    except Exception as e: print(f"[WARN] {path.name}: {e}")
    return None
def main():
    RAW.mkdir(parents=True, exist_ok=True); rows=[]
    for p in sorted(RAW.iterdir()):
        if not p.is_file() or p.name.startswith("."): continue
        df=read_table(p)
        if df is None:
            rows.append({"file_name":p.name,"column_name":"","inferred_type":"unsupported","missing_rate":"","unique_count":"","sample_values":"","possible_meaning":"","risk_note":"暂不支持自动读取该格式"}); continue
        for c in df.columns:
            s=df[c]; miss=float(s.isna().mean()) if len(s) else 0.0
            rows.append({"file_name":p.name,"column_name":str(c),"inferred_type":str(s.dtype),"missing_rate":f"{miss:.4f}","unique_count":int(s.nunique(dropna=True)),"sample_values":" | ".join(map(str,s.dropna().head(5).tolist())),"possible_meaning":"待人工确认","risk_note":"缺失率较高，需人工确认" if miss>0.3 else ""})
    fields=["file_name","column_name","inferred_type","missing_rate","unique_count","sample_values","possible_meaning","risk_note"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w",encoding="utf-8-sig",newline="") as f: w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"[OK] wrote {OUT.relative_to(ROOT)} ({len(rows)} rows)")
if __name__=="__main__": main()

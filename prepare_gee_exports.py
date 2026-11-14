"""Earth Engine export CSVs (real) or the supplied SYNTHETIC proxy CSVs (--demo) -> data/smap_all.csv, data/ndvi_all.csv (columns incl. site_id, demo).
  python tools/prepare_gee_exports.py --smap RotaShift_SMAP_*_actual.csv --ndvi RotaShift_MODIS_NDVI_*_actual.csv"""
import sys, argparse, pandas as pd
ap = argparse.ArgumentParser(); ap.add_argument("--smap", nargs="*", default=[]); ap.add_argument("--ndvi", nargs="*", default=[]); ap.add_argument("--demo", action="store_true"); a = ap.parse_args()
def load(files, kind):
    out = []
    for f in files:
        d = pd.read_csv(f); st = d["data_status"].astype(str) if "data_status" in d else pd.Series("REAL_EE_EXPORT", index=d.index)
        if kind == "smap":
            d["smap_vwc"] = d["soil_moisture_vwc_pct_demo"] if "soil_moisture_vwc_pct_demo" in d else (d[[c for c in ("smap_vwc_am_pct", "smap_vwc_pm_pct") if c in d]].mean(axis=1) if any(c in d for c in ("smap_vwc_am_pct", "smap_vwc_pm_pct")) else float("nan"))
            d = d[["date", "site_id", "smap_vwc"]].assign(data_status=st)
        else:
            d["ndvi"] = d["ndvi_demo_value"] if "ndvi_demo_value" in d else d.get("ndvi", float("nan")); d["date"] = d["composite_start_date"]
            d = d[["date", "site_id", "ndvi"]].assign(data_status=st)
        out.append(d)
    return pd.concat(out).dropna(subset=["smap_vwc" if kind == "smap" else "ndvi"]) if out else None
for kind, files in (("smap", a.smap), ("ndvi", a.ndvi)):
    d = load(files, kind)
    if d is None: continue
    if d.empty: print(f"{kind}: 0 valid rows - every value was masked/missing in the export; nothing written"); continue
    d["demo"] = d.data_status.str.contains("SYNTH|SIMUL", case=False).astype(int)
    if d.demo.any() and not a.demo: sys.exit("Synthetic/proxy data detected. Use real exports, or --demo for pipeline testing only.")
    d.to_csv(f"data/{kind}_all.csv", index=False); print(f"{kind}: {len(d)} valid rows, sites={sorted(d.site_id.unique())}, demo={int(d.demo.max())}")

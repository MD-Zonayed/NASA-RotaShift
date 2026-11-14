"""Earth Engine RAW exports (no QA applied in EE) -> clean per-site series with EXPLICIT quality tiers -> data/smap_all.csv, data/ndvi_all.csv
  python tools/prepare_ee_raw.py --smap data/raw_ee_exports/RotaShift_SMAP_RAW_*.csv --ndvi data/raw_ee_exports/RotaShift_MODIS_RAW_*.csv
  --smap-quality recommended (flag==0 only) | flagged (also flag!=0 'not recommended' values, labelled). --max-dist-km: pixels used around the point (SMAP grid is 9 km)."""
import argparse, numpy as np, pandas as pd
ap = argparse.ArgumentParser(); ap.add_argument("--smap", nargs="*", default=[]); ap.add_argument("--ndvi", nargs="*", default=[])
ap.add_argument("--smap-quality", default="flagged", choices=["recommended", "flagged"]); ap.add_argument("--max-dist-km", type=float, default=9.0); ap.add_argument("--max-summary-qa", type=int, default=1); a = ap.parse_args()
if a.smap:
    d = pd.concat(pd.read_csv(f) for f in a.smap); x = pd.concat([pd.DataFrame(dict(site_id=d.site_id, date=d.observation_date, dist=d.distance_from_reference_point_m, sm=d[f"soil_moisture_{p}"], flag=d[f"retrieval_qual_flag_{p}"])) for p in ("am", "pm")])
    x = x[(x.sm > 0) & (x.sm < 1) & (x.dist <= a.max_dist_km * 1000)]
    if a.smap_quality == "recommended": x = x[x.flag == 0]
    g = x.groupby(["site_id", "date"]).agg(smap_vwc=("sm", lambda s: s.mean() * 100), n_obs=("sm", "size"), share_recommended=("flag", lambda s: (s == 0).mean())).reset_index()
    g["quality"] = np.where(g.share_recommended == 1, "recommended", "flagged_not_recommended"); g["data_status"] = "REAL_EE_RAW"; g["demo"] = 0; g.to_csv("data/smap_all.csv", index=False)
    for s, h in g.groupby("site_id"): print(f"SMAP {s}: {len(h)} dates with a value ({int((h.quality=='recommended').sum())} fully recommended-quality), mean {h.smap_vwc.mean():.1f}%, range {h.smap_vwc.min():.1f}-{h.smap_vwc.max():.1f}%")
if a.ndvi:
    m = pd.concat(pd.read_csv(f) for f in a.ndvi).reset_index(drop=True); qa = m.DetailedQA.astype(int).to_numpy(); b = lambda lo, k: (qa >> lo) & k
    ok = (m.NDVI.to_numpy() > -3000) & (b(0, 3) <= 1) & (b(8, 1) == 0) & (b(10, 1) == 0) & (b(11, 7) == 1) & (b(14, 1) == 0) & (b(15, 1) == 0) & (m.SummaryQA.to_numpy() <= a.max_summary_qa)
    m = m[ok].assign(ndvi=m.NDVI[ok] * 1e-4, date=m.observation_date[ok])
    g = m.groupby(["site_id", "date"]).agg(ndvi=("ndvi", "median"), n_pixels=("ndvi", "size"), summary_qa_mean=("SummaryQA", "mean")).reset_index(); g = g[g.n_pixels >= 5]
    g["data_status"] = "REAL_EE_RAW"; g["demo"] = 0; g.to_csv("data/ndvi_all.csv", index=False)
    for s, h in g.groupby("site_id"): print(f"NDVI {s}: {len(h)} usable composites, median NDVI {h.ndvi.median():.2f}, range {h.ndvi.min():.2f}-{h.ndvi.max():.2f}")

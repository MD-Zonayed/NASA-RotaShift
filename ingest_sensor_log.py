"""Sensor log -> daily per-SITE series -> validation vs SMAP (per site).
  python tools/ingest_sensor_log.py LOG.csv [--calib candidate.json] [--smap data/smap_all.csv] [--max-depth 10] [--demo]
--calib: output of tools/fit_soil_moisture_calibration.py (per-probe). Refuses synthetic/simulated inputs unless --demo (outputs then carry demo=1)."""
import sys, json, argparse, pandas as pd
sys.path.insert(0, "src"); from metrics import rmse, bias, corr
ap = argparse.ArgumentParser(); ap.add_argument("log"); ap.add_argument("--calib"); ap.add_argument("--smap"); ap.add_argument("--max-depth", type=float, default=10); ap.add_argument("--demo", action="store_true"); a = ap.parse_args()
d = pd.read_csv(a.log)
if d.empty: sys.exit("Log has no data rows (header only).")
need = ["timestamp_local_iso8601", "site_id", "probe_id", "measurement_depth_cm", "soil_moisture_raw", "soil_moisture_pct_or_VWC", "soil_pH_calibrated"]
if [c for c in need if c not in d]: sys.exit(f"Missing columns: {[c for c in need if c not in d]}")
cal = json.load(open(a.calib)) if a.calib else None
synth = (d["data_status"].astype(str).str.contains("SYNTH|SIMUL", case=False).any() if "data_status" in d else False) or (cal is not None and "SYNTH" in str(cal.get("status", "")).upper())
if synth and not a.demo: sys.exit("Synthetic/simulated data detected. Use real data, or pass --demo for pipeline testing only.")
n = lambda c: pd.to_numeric(d[c], errors="coerce")
d["ts"] = pd.to_datetime(d.timestamp_local_iso8601, errors="coerce"); d["vwc"] = n("soil_moisture_pct_or_VWC"); d["ph"] = n("soil_pH_calibrated"); d["depth"] = n("measurement_depth_cm")
if cal:
    for pid, k in cal["probes"].items(): m = d.probe_id == pid; d.loc[m, "vwc"] = k["slope"] * n("soil_moisture_raw")[m] + k["intercept"]
    print("probes without calibration (kept logged VWC):", sorted(set(d.probe_id) - set(cal["probes"])) or "none")
for name, bad in [("pH outside 0-14", ~d.ph.dropna().between(0, 14)), ("VWC outside 0-70 %", ~d.vwc.dropna().between(0, 70))]:
    if bad.any(): print(f"WARNING: {int(bad.sum())} rows with {name} - fix calibration before using as ground truth")
d = d.dropna(subset=["ts"]); d["date"] = d.ts.dt.strftime("%Y-%m-%d"); k = ["site_id", "date"]
daily = d[d.depth <= a.max_depth].groupby(k).agg(sensor_vwc=("vwc", "mean")).join(d.groupby(k).agg(ph=("ph", "mean")), how="outer").reset_index(); daily["demo"] = int(synth)
daily.to_csv("data/sensor_daily.csv", index=False); print(f"{len(d)} readings -> {len(daily)} site-day rows (VWC from probes <= {a.max_depth:g} cm; SMAP sees ~top 5 cm)")
if a.smap:
    s = pd.read_csv(a.smap); s["date"] = pd.to_datetime(s.date).dt.strftime("%Y-%m-%d"); m = daily.merge(s[["site_id", "date", "smap_vwc"] + (["quality"] if "quality" in s else [])], on=k).dropna(subset=["sensor_vwc", "smap_vwc"])
    keep = []
    for sid, g in m.groupby("site_id"):
        if len(g) < 10: print(f"{sid}: only {len(g)} matching days - too few for metrics (need >=10)"); continue
        keep.append(g); print(f"{sid}: n={len(g)} RMSE={rmse(g.sensor_vwc, g.smap_vwc):.2f} bias={bias(g.sensor_vwc, g.smap_vwc):.2f} r={corr(g.sensor_vwc, g.smap_vwc):.2f}" + ("  [DEMO/SYNTHETIC]" if synth else "  (proof of concept)"))
    if keep: pd.concat(keep)[["site_id", "date", "sensor_vwc", "smap_vwc", "demo"] + (["quality"] if "quality" in m else [])].to_csv("data/validation_all.csv", index=False)

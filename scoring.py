"""Rule-based multi-criteria rotation scoring (transparent, explainable). One crop per season slot."""
import itertools, numpy as np, pandas as pd
from collections import Counter
SLOTS = {"rabi": [11, 12, 1, 2], "kharif1": [3, 4, 5, 6], "kharif2": [7, 8, 9, 10]}

def _scs(p):  # USDA-SCS effective rainfall (mm/month), as used in CROPWAT
    return p * (125 - 0.2 * p) / 125 if p <= 250 else 125 + 0.1 * p

def clim_by_slot(daily, dT=0.0, rain_f=1.0):
    mo = daily.index.month; out = {}
    for s, ms in SLOTS.items():
        k = mo.isin(ms); mp = (daily.rain[k] * rain_f).groupby(mo[k]).sum()
        out[s] = dict(t=daily.t[k].mean() + dT, rain=mp.sum(), eff=float(mp.map(_scs).sum()))
    return out

def _ramp(v, lo, hi, tol):
    return max(0.0, 1 - max(lo - v, v - hi, 0.0) / tol)

def crop_table(crops, clim, ph, irrig):
    c = crops.copy(); wmax = c.etc_mm.max(); rows = []
    for r in c.itertuples():
        k = clim[r.slot]; tf = _ramp(k["t"], r.tmin, r.tmax, 8)
        rf = min(1.0, (k["eff"] + irrig) / r.etc_mm); rf = rf + (1 - rf) * r.drought_tol * 0.5
        pf = _ramp(ph, r.ph_min, r.ph_max, 1.5)
        rows.append(dict(temp_fit=tf, rain_fit=rf, ph_fit=pf, fit=(tf * rf * pf) ** (1 / 3), water_eff=1 - r.etc_mm / wmax))
    return pd.concat([c.reset_index(drop=True), pd.DataFrame(rows)], axis=1).set_index("crop")

def rank_plans(crops, clim, ph, irrig, w):
    t = crop_table(crops, clim, ph, irrig); tot = sum(w.values()) or 1
    by = {s: list(crops[crops.slot == s].crop) for s in SLOTS}; out = []
    for plan in itertools.product(*by.values()):
        x = t.loc[list(plan)]
        soil = 0.6 * x.n_fixer.max() + 0.4 * (x.root.nunique() / 3) - 0.25 * max(0, sum("rice" in p.lower() for p in plan) - 1)
        s = dict(water=x.water_eff.mean(), soil=max(0, soil), income=x.income.mean(), resilience=x.fit.mean())
        out.append(dict(plan=" > ".join(plan), score=sum(w[k] * s[k] for k in s) / tot, **s))
    return pd.DataFrame(out).sort_values("score", ascending=False).reset_index(drop=True)

def stability(daily, crops, ph, irrig, w, dT=0.0, rain_f=1.0, n=200, seed=0):
    """Monte Carlo: perturb inputs within assumed error bands; how often does the same plan stay #1?"""
    rng = np.random.default_rng(seed); tops = Counter()
    for _ in range(n):
        cl = clim_by_slot(daily, dT + rng.normal(0, 1.0), rain_f * rng.normal(1, 0.15))
        tops[rank_plans(crops, cl, ph + rng.normal(0, 0.3), irrig, w).plan[0]] += 1
    plan, k = tops.most_common(1)[0]
    return plan, k / n

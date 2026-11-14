"""Per-plan gaps: nutrients (N,P,K), water/drought, weather-driven disease risk. All thresholds are illustrative."""
import pandas as pd
from scoring import SLOTS, clim_by_slot
SL = list(SLOTS)
def _slot(daily, s): return daily[daily.index.month.isin(SLOTS[s])]

def nutrient_recommendation(plan, barc, soil_class, yield_pick=None):
    """BARC FRG-2024 recommended nutrients (kg/ha) for the soil fertility class. 'not listed' is shown as-is, never as zero."""
    cols = ["N", "P", "K", "S", "Mg", "Zn", "B", "Mo", "Organic_t_ha"]; rows = []
    for s, c in zip(SL, plan):
        r = barc[(barc.crop == c) & (barc.fertility_class == soil_class)]
        if yield_pick and c in yield_pick: r = r[r.yield_goal == yield_pick[c]]
        rows.append(dict(slot=s, crop=c, yield_goal=r.yield_goal.iloc[0] if len(r) else "-", **{k: (r[k].iloc[0] if len(r) else "-") for k in cols}))
    return pd.DataFrame(rows)

def water_drought(daily, crops, plan, irrig=0, dT=0.0, rain_f=1.0):
    c = crops.set_index("crop"); cl = clim_by_slot(daily, dT, rain_f); rows = []
    for s, cr in zip(SL, plan):
        d = _slot(daily, s); etc = c.etc_mm[cr] * (1 + 0.04 * dT)  # +4%/degC demand (illustrative)
        eff = cl[s]["eff"]; run = best = 0
        for v in (d.rain * rain_f < 2): run = run + 1 if v else 0; best = max(best, run)
        ratio = (eff + irrig) / etc; risk = "High" if ratio < .4 or best >= 15 else "Moderate" if ratio < .7 or best >= 10 else "Low"
        rows.append(dict(slot=s, crop=cr, etc_mm=round(etc), etc_range=(f"{c.etc_low_mm[cr]:.0f}-{c.etc_high_mm[cr]:.0f}" if pd.notna(c.etc_low_mm[cr]) else "-"), eff_rain_mm=round(eff), irrigation_needed_mm=round(max(0, etc - eff - irrig)),
                         ref_net_irrigation_mm=c.net_irrigation_ref_mm[cr], longest_dry_spell_d=best, drought_risk=risk, etc_status=c.etc_status[cr]))
    return pd.DataFrame(rows)

def disease_risk(daily, dis, plan, dT=0.0, include_unverified=False):
    rows = []; dis = dis if include_unverified else dis[dis.verified == 1]
    for s, c in zip(SL, plan):
        d = _slot(daily, s); t = d.t + dT
        for r in dis[dis.crop == c].itertuples():
            f = float((t.between(r.tmin, r.tmax) & (d.rh >= r.rh_min)).mean())
            rows.append(dict(slot=s, crop=c, disease=r.disease, favourable_days=f"{f:.0%}", risk="High" if f > .35 else "Moderate" if f > .15 else "Low", action=r.action))
    return pd.DataFrame(rows)

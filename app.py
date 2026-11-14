import sys, os, pandas as pd, streamlit as st
sys.path.insert(0, "src")
from nasa_power import fetch_daily, sample_daily
from scoring import clim_by_slot, rank_plans, stability
from agronomy import nutrient_recommendation, water_drought, disease_risk
from metrics import rmse, bias, corr
st.set_page_config("Soil-to-Sky Robo Team", "🌱", layout="wide"); st.title("🌱 RotaShift: crop-rotation decision support")
rd = lambda f: pd.read_csv(f"data/{f}.csv", comment="#")
crops, barc, dis, sites = rd("crops"), rd("barc_frg"), rd("diseases"), rd("sites")

@st.cache_data(show_spinner=False)
def load(lat, lon, year, live):
    if live:
        try: return fetch_daily(lat, lon, year), "NASA POWER (live)"
        except Exception as e: st.warning(f"NASA POWER unavailable ({e}); using SAMPLE data.")
    return sample_daily(year), "SAMPLE synthetic data (not real)"

with st.sidebar:
    site = st.selectbox("Site", sites.site); r = sites[sites.site == site].iloc[0]; sid = r.site_id
    lat, lon = st.number_input("Latitude", value=float(r.lat), format="%.5f", key=f"la{site}"), st.number_input("Longitude", value=float(r.lon), format="%.5f", key=f"lo{site}")
    st.caption("Approximate locality coordinates - replace with the plot-centre GPS.")
    year, live = st.number_input("Climate year", 2015, 2025, 2023), st.checkbox("Fetch live NASA POWER", True)
    ph = st.slider("Soil pH (calibrated sensor/lab)", 4.0, 9.0, 6.7, 0.1); irrig = st.slider("Irrigation per season (mm)", 0, 800, 0, 50)
    sc = st.selectbox("Soil fertility class (from lab soil-test report)", ["Optimum", "Medium", "Low", "Very low"], 1)
    st.subheader("Climate scenario"); dT = st.slider("Warming (°C)", 0.0, 3.0, 0.0, 0.5); rf = st.slider("Rainfall factor", 0.6, 1.2, 1.0, 0.05)
    st.subheader("Farmer priorities"); w = {k: st.slider(k, 0, 10, 5) for k in ["water", "soil", "income", "resilience"]}
    unv = st.checkbox("Show UNVERIFIED demo disease rules", False)
daily, src = load(lat, lon, int(year), live); st.caption(f"Climate source: {src}")
if src.startswith("SAMPLE"): st.error("SAMPLE synthetic climate data is in use. Do NOT present these rankings as results.")
plans = rank_plans(crops, clim_by_slot(daily, dT, rf), ph, irrig, w)
st.subheader("Top rotation plans (rabi > kharif-1 > kharif-2)"); st.dataframe(plans.head(5).round(2), use_container_width=True)
st.bar_chart(plans.iloc[0][["water", "soil", "income", "resilience"]].astype(float))
best = plans.plan[0].split(" > "); st.subheader(f"Gaps for the top plan: {plans.plan[0]}")
a, b, c = st.tabs(["💧 Water & drought", "🧪 Nutrients (BARC)", "🦠 Disease alerts"])
a.dataframe(water_drought(daily, crops, best, irrig, dT, rf), use_container_width=True)
a.caption("ETc = crop water use. Irrigation need = ETc - effective rain (USDA-SCS). The reference column is a published CROPWAT figure from other regions, for comparison only. 'placeholder' rows are not yet sourced.")
yg = {}
for cr in best:
    o = list(barc[barc.crop == cr].yield_goal.unique())
    if len(o) > 1: yg[cr] = b.selectbox(f"{cr}: BARC yield group", o, key=f"yg{cr}")
b.dataframe(nutrient_recommendation(best, barc, sc, yg), use_container_width=True); b.caption("Rice: only one BARC yield group per rice crop is loaded so far. BARC FRG-2024 nutrient recommendations (kg nutrient/ha, not product weight) for the chosen soil class and yield goal. Use a lab soil test to pick the class; sensor NPK is indicative only. Mungbean: no N fertilizer if Rhizobium inoculant is used. Boro: pick the sub-table matching your variety.")
d = disease_risk(daily, dis, best, dT, unv)
if d.empty: c.info("No expert-validated disease thresholds loaded yet. The Farmbot YOLOv8 model detects tomato ripeness/rot, not disease.")
else: c.dataframe(d, use_container_width=True); c.caption("Weather-favourability screening only, not a diagnosis.")
def _flt(f):
    if not os.path.exists(f): return None
    x = pd.read_csv(f); x = x[x.site_id == sid]; return x if len(x) else None
nd = _flt("data/ndvi_all.csv")
if nd is not None:
    st.subheader("MODIS NDVI (vegetation condition)"); st.line_chart(nd.set_index("date").ndvi)
    if nd.demo.any(): st.error("DEMO / SYNTHETIC NDVI - not a MODIS observation.")
    st.caption(f"Latest valid NDVI {nd.ndvi.iloc[-1]:.2f} vs series mean {nd.ndvi.mean():.2f}; cloud-screened gaps are expected in the monsoon.")
sm = _flt("data/smap_all.csv")
if sm is not None:
    st.subheader("SMAP soil moisture near the site (satellite only)"); st.line_chart(sm.set_index("date").smap_vwc)
    st.caption("SMAP 9 km, top ~5 cm. These values carry the product's 'not recommended' quality flag: the seasonal pattern is indicative, not field soil moisture.")
if st.button("Check recommendation stability (Monte Carlo)"):
    p, f = stability(daily, crops, ph, irrig, w, dT, rf); st.metric("Most frequent #1 plan", p, f"{f:.0%} of runs")
st.subheader("Ground-truth check: sensor vs satellite soil moisture")
st.caption("SMAP pixels are ~9 km and sense the top ~5 cm: expect trend agreement, not exact values (weaker over urban Uttara).")
v = _flt("data/validation_all.csv"); up = st.file_uploader("Or upload CSV: date, sensor_vwc, smap_vwc")
if up: v = pd.read_csv(up)
if v is not None:
    if "demo" in v and v.demo.any(): st.error("DEMO / SYNTHETIC validation data - not real measurements.")
    if "quality" in v and (v.quality != "recommended").any(): st.warning("SMAP values are flagged not-recommended quality by the product; treat agreement as indicative only.")
    st.write(dict(n=len(v), RMSE=rmse(v.sensor_vwc, v.smap_vwc), bias=bias(v.sensor_vwc, v.smap_vwc), r=corr(v.sensor_vwc, v.smap_vwc)))
    st.line_chart(v.set_index("date")[["sensor_vwc", "smap_vwc"]])

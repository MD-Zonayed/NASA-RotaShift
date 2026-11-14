"""PREFER tools/gee/Export_RotaShift_SMAP_MODIS_NDVI.js (has NDVI QA screening). This AppEEARS NDVI route has NO QA screening.
Fetch NASA Earth observations for ONE point. UNTESTED offline - run on your machine, verify variable names on first file.
  python tools/fetch_nasa_eo.py smap  LAT LON 2023-03-01 2023-04-30   -> data/smap_point.csv (date, smap_vwc in %)
  python tools/fetch_nasa_eo.py ndvi  LAT LON 2023-01-01 2023-12-31   -> data/ndvi_point.csv (date, ndvi)
Needs a free NASA Earthdata login. SMAP: `pip install earthaccess h5py` (daily global files, ~tens of MB each: keep the window short!).
NDVI: set env vars EARTHDATA_USER / EARTHDATA_PASS (uses NASA AppEEARS point sampling; takes a few minutes)."""
import os, re, sys, io, time, numpy as np, pandas as pd, requests

def smap(lat, lon, start, end, out="data/smap_point.csv"):
    import earthaccess, h5py
    earthaccess.login()
    res = earthaccess.search_data(short_name="SPL3SMP_E", temporal=(start, end), bounding_box=(lon - .3, lat - .3, lon + .3, lat + .3))
    rows = []
    for f in earthaccess.download(res, "data/smap_raw"):
        with h5py.File(f) as h:
            g = h["Soil_Moisture_Retrieval_Data_AM"]; la, lo = g["latitude"][:], g["longitude"][:]
            d = np.where(la > -999, (la - lat) ** 2 + (lo - lon) ** 2, np.inf); i = np.unravel_index(np.argmin(d), d.shape)
            v, q = float(g["soil_moisture"][i]), int(g["retrieval_qual_flag"][i])
        if v > 0 and q == 0:  # strict: no quality flag set (same rule as the GEE script); verify flag semantics for the product version returned
            rows.append(dict(date=pd.to_datetime(re.search(r"(\d{8})", os.path.basename(str(f))).group(1)), smap_vwc=v * 100))
    pd.DataFrame(rows).sort_values("date").to_csv(out, index=False); print(f"saved {len(rows)} rows -> {out}")

def ndvi(lat, lon, start, end, out="data/ndvi_point.csv"):
    API = "https://appeears.earthdatacloud.nasa.gov/api"; fmt = lambda x: pd.to_datetime(x).strftime("%m-%d-%Y")
    tok = requests.post(f"{API}/login", auth=(os.environ["EARTHDATA_USER"], os.environ["EARTHDATA_PASS"])).json()["token"]; h = {"Authorization": f"Bearer {tok}"}
    task = {"task_type": "point", "task_name": "rotashift_ndvi", "params": {"dates": [{"startDate": fmt(start), "endDate": fmt(end)}],
            "layers": [{"product": "MOD13Q1.061", "layer": "_250m_16_days_NDVI"}], "coordinates": [{"id": "site", "longitude": lon, "latitude": lat, "category": "site"}]}}
    tid = requests.post(f"{API}/task", json=task, headers=h).json()["task_id"]
    while (st := requests.get(f"{API}/task/{tid}", headers=h).json()["status"]) not in ("done", "error"): time.sleep(20)
    if st == "error": sys.exit("AppEEARS task failed")
    f = [x for x in requests.get(f"{API}/bundle/{tid}", headers=h).json()["files"] if x["file_name"].endswith("results.csv")][0]
    df = pd.read_csv(io.StringIO(requests.get(f"{API}/bundle/{tid}/{f['file_id']}", headers=h).text))
    col = [c for c in df.columns if c.endswith("_NDVI")][0]
    pd.DataFrame({"date": pd.to_datetime(df["Date"]), "ndvi": df[col]}).to_csv(out, index=False); print(f"saved {len(df)} rows -> {out}")

if __name__ == "__main__":
    kind, lat, lon, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]
    (smap if kind == "smap" else ndvi)(lat, lon, a, b)

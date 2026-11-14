"""NASA POWER daily data (no login needed). sample_daily() is SYNTHETIC - offline demo only."""
import numpy as np, pandas as pd, requests
URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

def fetch_daily(lat, lon, year=2023, timeout=30):
    r = requests.get(URL, timeout=timeout, params=dict(
        parameters="T2M,PRECTOTCORR,RH2M", community="AG", longitude=lon, latitude=lat,
        start=f"{year}0101", end=f"{year}1231", format="JSON"))
    r.raise_for_status()
    p = r.json()["properties"]["parameter"]
    df = pd.DataFrame({"t": p["T2M"], "rain": p["PRECTOTCORR"], "rh": p["RH2M"]})
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    return df.replace(-999, np.nan).dropna()

def sample_daily(year=2023):
    idx = pd.date_range(f"{year}-01-01", f"{year}-12-31"); d = idx.dayofyear.values
    t = 24 + 6.5 * np.sin(2 * np.pi * (d - 45) / 365)
    rain = 12 * np.exp(-((d - 200) / 45) ** 2) + 0.6
    rh = 62 + 25 * np.exp(-((d - 200) / 60) ** 2)
    return pd.DataFrame({"t": t, "rain": rain, "rh": rh}, index=idx)

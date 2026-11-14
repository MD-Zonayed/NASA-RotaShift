# How to do the open items
## 1. Registration + team (today)
spaceappschallenge.org -> your team page -> Members tab: every person listed, same Local Event, none waitlisted, max 6. Waitlisted? Message the Local Lead; else switch to the Universal Event.
## 2. Earthdata login (10 min)
Register free at urs.earthdata.nasa.gov, verify email. Then `pip install earthaccess h5py` and run `python -c "import earthaccess; earthaccess.login()"` (enter credentials once). For NDVI set env vars EARTHDATA_USER / EARTHDATA_PASS, then run tools/fetch_nasa_eo.py (usage in its header). Start with SMAP for a 30-60 day window.
## 3. Calibrate soil moisture (half a day, needs an oven or a very low-temp drying method)
1) Press a metal ring/core of KNOWN volume into the bed soil. 2) Read the sensor in that soil, record `raw`. 3) Weigh the soil wet, oven-dry at 105 C for 24 h, weigh dry. 4) VWC % = (wet g - dry g) / core volume cm3 x 100. 5) Repeat 15-20 times from dry to wet. 6) Save as samples.csv (columns raw,vwc) and run `python tools/fit_soil_moisture_calibration.py samples.csv --out candidate.json`. Aim: RMSE <= 5, R2 >= 0.85.
## 4. Fix the pH reading (16.5 is impossible)
Likely causes: (a) PH-4502C output can exceed the ESP32's 3.3 V ADC range -> add a voltage divider and check ADC attenuation; (b) no calibration -> use buffers pH 4.00 and 7.00: read the voltage in each, then pH = 7 + (V7 - V) x (3 / (V7 - V4)); (c) average 20-50 samples; keep the probe wet. Verify against a third buffer (9.18 or 10.01): error <= 0.3.
## 5. Kickoff call (30 min)
Agenda: roles (lead, data, agronomy, model, UI, story), chat + shared drive, repo access, what "done" looks like (one working end-to-end demo + a 30 s video), who records the video, who submits.
## 6. Originality + AI
Before Nov 14: read the Participant Terms and the 2026 Submission Guide. During the hackathon the team should do the real SMAP/NDVI runs, replace placeholder crop/nutrient/disease tables with verified values, calibrate/validate sensors, and edit the code. In the AI-use field state what Claude produced (starter code, logo, planning/text) and what the team did. Declare the Farmbot as prior work.

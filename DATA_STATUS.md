# Data Status and Evidence

| Component | What is included | Verified status | How to describe it publicly |
|---|---|---|---|
| NASA POWER | `src/nasa_power.py` | Live API connection is implemented; no cached live response in the uploaded source files. Synthetic fallback exists. | “Live NASA POWER retrieval when available; sample fallback is synthetic and visibly labelled.” |
| SMAP V006 | Two raw 18 km-buffer exports and two point QA-only diagnostic exports | Raw export files span 2025-11-14–2026-11-11. Within 9 km, 450 processed site-date rows are all retrieval flag 1 (fail). Flag-0 observations in Uttara occur in a pixel ~15.12 km away in the 18 km buffer; Araihazar has no flag-0 observations in that buffer. | “SMAP was examined as regional context, but no recommended-quality retrievals were found within 9 km of the provisional locations.” |
| MODIS MOD13Q1 | Two raw 1 km-buffer exports + processed `ndvi_all.csv` | 22 composites per site in raw data; processing retains 14 Uttara and 16 Araihazar site-date rows after current QA criteria and minimum pixel count. Raw NDVI needs ×0.0001 scaling. | “Actual MODIS-derived vegetation context from a 1 km buffer around provisional locality coordinates.” |
| HLS 30 m | HLS processing/export code in `tools/gee/RotaShift_RAW_export_used.js` | No HLS CSV was present in any uploaded ZIP. | “Planned next step; no HLS observations are included.” |
| Farmbot sensors | Empty template + synthetic sample log | No real sensor export supplied. Synthetic file is clearly tagged. | Do not claim field measurements from the supplied synthetic rows. |
| Soil-moisture calibration | Simulated sample pairs and simulated JSON fit | No real oven-dry references or independent validation supplied. | Do not quote simulated RMSE/R² as physical-sensor accuracy. |
| BARC nutrient rows | 52 rows for 13 crops × 4 fertility classes | Medium/Optimum/Low/Very low classes included; one yield/variety group per crop. Rice subgroups incomplete. | Reference recommendation ranges only; select matching variety and soil test class. |
| BRRI crop water | Nine crop values in the BRRI CSV/reference workbook | Published historical CROPWAT modelled reference for selected NW/SW Bangladesh sites, not local plot measurement. | Keep ETc and net irrigation separate; note land-preparation water in irrigation totals. |
| FAO-56 crop ETc | Four planning estimates | Based on assumed ETo and crop calendars; not measured locally. | Call them coefficient-based planning estimates with assumptions/ranges. |
| Disease table | 14 rules | All `verified=0`, hidden by default. | Weather-favourability screening rules only; not diagnosis. |
| GPS | Two approximate location-reference points | Not field-surveyed plot centres. | Call them approximate site references; do not call them plot GPS. |

## Raw export counts

| File | Rows | Date span | Key observations |
|---|---:|---|---|
| `RotaShift_SMAP_RAW_Uttara.csv` | 5,068 | 2025-11-14 to 2026-11-11 | 362 dates, 18 km buffer; near 9 km valid soil-moisture samples are flag 1 only; flag 0 is only at ~15.12 km. |
| `RotaShift_SMAP_RAW_Araihazar.csv` | 4,706 | 2025-11-14 to 2026-11-11 | 362 dates, 18 km buffer; all valid AM/PM soil-moisture values in the file have flag 1. |
| `RotaShift_MODIS_RAW_Uttara.csv` | 1,092 | 2025-11-17 to 2026-10-16 | 22 composites, raw NDVI/QA values in a 1 km buffer. |
| `RotaShift_MODIS_RAW_Araihazar.csv` | 1,082 | 2025-11-17 to 2026-10-16 | 22 composites, raw NDVI/QA values in a 1 km buffer. |

## Reproducibility check

The supplied `tools/prepare_ee_raw.py` was re-run against the four raw Earth Engine exports with `--smap-quality flagged --max-dist-km 9 --max-summary-qa 1`. It reproduced 450 `smap_all.csv` rows (222 Araihazar, 228 Uttara) and 30 `ndvi_all.csv` rows (16 Araihazar, 14 Uttara). All 450 SMAP rows are labelled `flagged_not_recommended`; MODIS observations were scaled by 0.0001 and screened by the project's current DetailedQA/SummaryQA rules.

## Critical spatial interpretation

The coordinates in the raw CSVs are explicitly marked `APPROXIMATE_NOT_PLOT_GPS`. MODIS pixels within the 1 km buffer include surrounding land cover. SMAP uses a nominal 9 km grid posting and represents a much coarser radiometer footprint. Neither dataset is a substitute for a field boundary or calibrated in-situ soil sensor.

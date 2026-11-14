# Uploaded Archive Audit — RotaShift

Three uploaded ZIP archives were reviewed: `soil_to_sky_starter (2)(1).zip`, `CSV & Code file-1.zip`, and `CSV & Code file-2.zip`. All three passed ZIP integrity checks. The two CSV/code archives contain many repeated copies of identical raw exports and demo files (with suffixes such as `(1)`, `(2)`, `(3)`). The repository keeps one copy of each unique file.

## What was selected

- The complete application source, `src/`, `tools/`, and original assets from the starter archive.
- The four raw Earth Engine exports from `soil_to_sky/data/raw_ee_exports/` (two SMAP and two MODIS files).
- The processed `data/smap_all.csv` and `data/ndvi_all.csv` tables, which were reproduced from the raw exports with the bundled processing script.
- The synthetic proxy/sensor/calibration files, but only inside `data/demo_synthetic/` and with their original synthetic labels.
- The BARC/BRRI workbook and companion CSVs from `CSV & Code file-2.zip`.
- Four point-only diagnostic CSVs from `CSV & Code file-1.zip`, moved to `data/diagnostics/point_qa_only/`. These include quality metadata but do not contain actual SMAP moisture values or MODIS NDVI values at the point.
- The exact chat GEE script is already present as `tools/gee/RotaShift_RAW_export_used.js`; `RotaShift_EXACT_chat_code.txt` in the third archive is byte-identical to this JS file and is not duplicated.

## Point-only diagnostic exports

`RotaShift_SMAP_Uttara_actual.csv` and `RotaShift_SMAP_Araihazar_actual.csv` each contain 364 date rows and retrieval flags only; both AM/PM flags are 1 throughout. They do not contain valid soil-moisture value columns. `RotaShift_MODIS_NDVI_Uttara_actual.csv` and `RotaShift_MODIS_NDVI_Araihazar_actual.csv` each contain 23 composite QA rows and metadata but no NDVI value band. The buffered raw MODIS exports are the files containing NDVI values.

## Duplicate handling

Files repeated with `(1)`, `(2)`, `(3)`, or `(4)` suffixes in the two CSV/code ZIPs were checked by SHA-256. Identical copies were not repeated in the GitHub repository. This keeps the repo smaller and avoids confusing repeated versions with independent observations.

## What is not in the supplied archives

- No real Farmbot sensor export CSV.
- No genuine gravimetric/oven-dry calibration samples or validated calibration result.
- No HLS 30 m output CSV.
- No named public GitHub repository URL or deployed RotaShift web-app URL.
- No full list of all five teammate names or individually assigned roles.

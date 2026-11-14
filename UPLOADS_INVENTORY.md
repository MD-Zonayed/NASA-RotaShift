# Which uploaded files belong in the GitHub repository?

This repository merges three uploaded ZIPs: `soil_to_sky_starter (2)(1).zip`, `CSV & Code file-1.zip`, and `CSV & Code file-2.zip`. Repeated `(1)`, `(2)`, `(3)`, and `(4)` copies were deduplicated by SHA-256.

## Include from the starter ZIP

The public release keeps the team's actual outdoor Farmbot photograph and tomato-detection result. It excludes the older Farmbot interface screenshot (`streamlit.jpg`) and RViz/Gazebo simulation screenshot (`Farmbot_RViz_and_Gazebo.png`) from the public assets because neither is the RotaShift crop-rotation interface or a photograph of the physical field prototype.

- `soil_to_sky/app.py`
- `soil_to_sky/src/agronomy.py`, `metrics.py`, `nasa_power.py`, `scoring.py`
- `soil_to_sky/tools/*.py` and `soil_to_sky/tools/gee/*.js`
- `soil_to_sky/requirements.txt`
- `soil_to_sky/assets/Picture1.jpg`
- `soil_to_sky/assets/Tomato_detection_1.png`
- `soil_to_sky/data/crops.csv`, `sites.csv`, `barc_frg.csv`, `diseases.csv`, `ndvi_all.csv`, `smap_all.csv`, `sensor_log_template.csv`, `RotaShift_plot_centre_GPS_PROVISIONAL.csv`, `fao56_planning_estimates.csv`
- All four files inside `soil_to_sky/data/raw_ee_exports/`
- All five files in `soil_to_sky/data/demo_synthetic/` (kept isolated and marked synthetic)
- Existing project docs, rewritten where necessary for the final submission

## Include from CSV & Code file-1.zip

- `RotaShift_SMAP_Araihazar_actual.csv`
- `RotaShift_SMAP_Uttara_actual.csv`
- `RotaShift_MODIS_NDVI_Araihazar_actual.csv`
- `RotaShift_MODIS_NDVI_Uttara_actual.csv`

These are included under `data/diagnostics/point_qa_only/`. They contain point-level QA/metadata, but not a valid SMAP soil-moisture or MODIS NDVI measurement band. Do not use them as the NDVI or soil-moisture series.

## Include from CSV & Code file-2.zip

- `RotaShift_BARC_13_crops_all_soil_classes.csv`
- `RotaShift_BARC_13_crop_medium_class.csv`
- `RotaShift_BRRI_water_reference.csv`
- `RotaShift_BARC_BRRI_reference_data.xlsx`

These are included under `data/references/`.

## Duplicates not included twice

- `RotaShift_EXACT_chat_code.txt` is byte-identical to `tools/gee/RotaShift_RAW_export_used.js`; the repository keeps the JavaScript file only.
- `Export_RotaShift_SMAP_MODIS_NDVI.txt` is duplicated across the CSV/code archives and matches the existing point-export JavaScript under `tools/gee/`.
- Raw SMAP/MODIS exports repeated in the CSV/code ZIPs are byte-identical to the four raw exports in the starter ZIP.
- Synthetic proxy, sensor, and calibration files repeated in the CSV/code ZIPs are byte-identical to files in `data/demo_synthetic/`.

## Do not include as real project measurements

Files named `*_POPULATED_SYNTHETIC*`, `*_SIMULATED*`, or `*_SYNTHETIC_PROXY*` are retained solely as sample/demo input under `data/demo_synthetic/`. The calibration JSON is simulated. Do not rename these as real data.

# Data Dictionary

## Crop catalogue (`data/crops.csv`)

- `crop`: crop label used by the app.
- `slot`: simplified calendar window (`rabi`, `kharif1`, `kharif2`).
- `tmin`, `tmax`: heuristic suitable-temperature bounds in °C.
- `etc_mm`: seasonal crop evapotranspiration (ETc), mm; this is crop water use, not net irrigation.
- `net_irrigation_ref_mm`: published BRRI CROPWAT reference, mm; it is not a local irrigation prescription.
- `etc_status`: `BRRI-AR-2017-18` for nine regional reference values or `FAO56-planning-estimate` for four coefficient-based planning estimates.
- `etc_low_mm`, `etc_high_mm`: planning interval for FAO-56 estimates where available.
- `ph_min`, `ph_max`: heuristic soil-pH suitability range.
- `n_fixer`: binary indicator used as a rotation heuristic.
- `drought_tol`: relative ordinal score (0–1), not a field-measured crop parameter.
- `income`: relative ordinal score (0–1), not currency or gross margin.
- `root`: categorical rooting-depth class used for a simple root-diversity bonus.

## BARC table (`data/barc_frg.csv`)

- Nutrient columns `N`, `P`, `K`, `S`, `Mg`, `Zn`, `B`, `Mo` are BARC FRG-2024 nutrient recommendations in kg nutrient/ha. `Organic_t_ha` is tonnes organic fertilizer/ha.
- `not listed` means the crop table does not list a value; it must not be interpreted as zero.
- Each crop currently has one yield/variety group repeated across four soil fertility classes. Rice variety/yield-group coverage is incomplete.

## Earth Engine raw exports

- `observation_date`: Earth Engine image date.
- `distance_from_reference_point_m`: pixel-centre distance from approximate locality point.
- `soil_moisture_am`, `soil_moisture_pm`: SMAP volume fractions; raw fill value `-9999` means missing/masked. Multiply valid fractions by 100 for VWC percentage.
- `retrieval_qual_flag_am/pm`: 0 = pass/acceptable quality; 1 = fail/unacceptable quality for the Earth Engine SPL3SMP_E.006 catalogue description.
- `NDVI`: MODIS raw integer; multiply by 0.0001.
- `DetailedQA`, `SummaryQA`: MODIS quality bands; consult the MOD13Q1 product documentation and the processing script.
- `qa_filter_applied_before_export`: the raw export records `NONE_RAW_QA_RETAINED`.

## Processed satellite tables

- `smap_all.csv`: one site/date record derived from pixels within the selected radius. `quality` distinguishes recommended vs flagged values; the supplied 9 km processed table currently contains only `flagged_not_recommended`.
- `ndvi_all.csv`: one site/composite date record using median NDVI of retained pixels; `n_pixels` is the number of retained pixels; NDVI is unitless after 0.0001 scaling.

## Synthetic demo files

Any filename with `SYNTHETIC`, `SIMULATED`, or `PROXY` is artificial test data. It must never be cited as a measured Farmbot log, real calibration sample, or NASA retrieval.

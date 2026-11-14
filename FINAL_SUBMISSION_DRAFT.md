# NASA Space Apps 2026 — Project Submission Draft

**Challenge:** Field Shift: Adapting Farms with NASA Data  
**Team:** Soil-to-Sky Robo Team  
**Local Event:** Dhaka, Bangladesh  
**Project title:** RotaShift: Climate-Aware Crop Rotation Planning for Bangladesh

> Replace the GitHub and demo placeholders after uploading the repository and slide deck publicly. Add exact teammate names from the official team page. Check the Project form for any field-level character counter; numeric limits were not included in the supplied instructions.

## 1. Project name

RotaShift: Climate-Aware Crop Rotation Planning for Bangladesh

## 2. High-level project summary

RotaShift is a Bangladesh-focused crop-rotation decision-support prototype that helps farmers compare three-season rotation plans under changing climate conditions. It combines live NASA POWER temperature, rainfall, and humidity data (when available) with a 13-crop seasonal catalogue, soil pH and fertility inputs, irrigation assumptions, BARC fertilizer references, and farmer-selected priorities. Its transparent scoring engine ranks 72 possible Rabi–Kharif-1–Kharif-2 combinations and explains water, soil, income-index, and resilience components. Actual MODIS NDVI exports provide vegetation context; SMAP exports are shown with explicit quality warnings. The team's pre-existing Farmbot demonstrates a path toward future field monitoring.

## 3. Project demo link

**Required demo format selected:** seven-slide presentation (within the seven-slide maximum, including title and introduction).  
**Public demo URL:** `[PASTE PUBLIC GOOGLE DRIVE / ONEDRIVE / GITHUB LINK TO presentation/RotaShift_7_Slide_Demo.pptx]`

The supplied YouTube video is a prior Farmbot thesis demonstration, not the required RotaShift presentation demo: https://www.youtube.com/watch?v=VWTlKhXIzMg

## 4. Final project link

**Public GitHub repository URL:** `[PASTE YOUR PUBLIC GITHUB REPOSITORY URL AFTER CREATING IT]`

The repository includes the Streamlit app, scoring and agronomy modules, raw Earth Engine exports, processed MODIS/SMAP tables, BARC/BRRI references, GEE scripts, documentation, and the seven-slide presentation.

## 5. Additional project details

### Problem

Farmers need to choose crop sequences under seasonal changes in temperature, rainfall, water availability, and soil conditions. Satellite and climate products are not automatically usable as farm decisions; they need to be connected to local crop options and farmer priorities.

### What the prototype does

- Provides a Streamlit interface for two Bangladesh study-area references: Uttara Sector 17, Dhaka, and Araihazar, Narayanganj. The current coordinates are approximate locality references, not field-surveyed plot centres.
- Retrieves daily NASA POWER `T2M`, `PRECTOTCORR`, and `RH2M` values when the live API is reachable. The app visibly labels its synthetic sample fallback when the API is unavailable.
- Includes 13 crops across Rabi, Kharif-1, and Kharif-2 and ranks 72 three-season combinations using climate fit, water efficiency/fit, soil-rotation heuristics, a relative income index, and resilience.
- Shows crop ETc, effective rainfall, estimated irrigation gaps, dry-spell length, and BARC FRG-2024 nutrient reference ranges for the selected soil-fertility class.
- Displays actual MODIS NDVI and SMAP soil-moisture context tables/plots, with data-quality warnings. These satellite products do not currently feed directly into the rotation score.
- Includes a Monte Carlo ranking-stability routine; its perturbation assumptions are model assumptions, not field-calibrated uncertainty.

### Data and scientific limitations

- MODIS MOD13Q1 raw Earth Engine exports are included for both approximate site references. The supplied quality-screened table retains 14 of 22 composites for Uttara and 16 of 22 for Araihazar. It represents a 1 km context buffer, not a mapped field boundary.
- SMAP raw exports are included. Within the 9 km processing radius, all 450 processed site-date records are retrieval flag 1 (not recommended quality). Uttara has flag-0 samples in a farther pixel approximately 15.12 km from the approximate reference point in the 18 km raw export; Araihazar has none in that raw buffer. SMAP is regional context, not field-level validation.
- No HLS 30 m result CSV was supplied. The repository contains HLS export logic only.
- BARC FRG-2024 data includes 13 crops × 4 soil-fertility classes, but only one yield/variety group per rice crop is presently loaded: high-yield Boro (7.5 ± 0.75 t/ha), Aus (4.0 ± 0.4 t/ha), and Aman (6.0 ± 0.6 t/ha). Other rice tables in the guide remain to be integrated.
- BRRI CROPWAT ETc/net-irrigation values cover nine crops and are regional modelled references from other Bangladesh locations. Four additional crop-water values are FAO-56 coefficient-based planning estimates with assumed ETo and crop durations; they are not local measurements.
- Sensor logs and calibration examples in `data/demo_synthetic/` are simulated only. No real Farmbot sensor CSV, oven-dry calibration samples, or sensor-to-satellite validation metrics were supplied.
- All 14 disease rules have `verified=0` and are hidden by default. RotaShift does not claim disease diagnosis. The supplied YOLOv8 image demonstrates ripe/unripe tomato detection, not disease detection.
- Crop drought-tolerance and income inputs are relative heuristic scores, not validated monetary returns or experimentally measured drought-response parameters. Rotation rankings are not yield predictions or prescriptions.

### Farmbot relationship

The gantry-style Farmbot, sensor network, and YOLOv8 tomato/weed work are pre-existing team research assets developed before the hackathon. They are included as supporting agricultural robotics context and a future route for field monitoring; they are not represented as newly built RotaShift components. Prior-work video: https://www.youtube.com/watch?v=VWTlKhXIzMg

### Expected benefit

RotaShift aims to make NASA climate observations and local agronomic references easier to interpret as seasonal rotation choices. It provides transparent comparisons that can be validated and adapted with field GPS, soil tests, local farmer knowledge, and calibrated sensor data.

## 6. Super Intelligence (SI) tools

Yes. Anthropic Claude assisted with original starter code, calibration-script drafting, a team logo, and planning/submission text (as recorded in the original project disclosure). OpenAI ChatGPT assisted with code/data review, interpretation of uploaded exports, repository documentation, submission drafting, and the seven-slide presentation. The team supplied the project idea, Farmbot assets, code/data archives, and project decisions and must review/test all AI-assisted work. The slides use team-supplied photos/screenshots, not AI-generated images. The original archive mentions an AI-generated logo; if used, it must be visibly identified as AI-generated. No NASA branding or mission identifiers were AI-generated or modified.

## 7. NASA data and resources used

- **NASA POWER daily point API:** `T2M`, `PRECTOTCORR`, `RH2M`, implemented in `src/nasa_power.py` and used by the climate-scoring workflow when live access succeeds.
- **NASA SMAP SPL3SMP_E V006:** actual raw Earth Engine exports in `data/raw_ee_exports/`; quality flags preserved. The processed 9 km context data is not recommended-quality at the approximate sites and is shown with warnings, not used by the ranking engine.
- **NASA MODIS Terra MOD13Q1 V6.1:** actual raw Earth Engine exports and quality-screened NDVI summaries in `data/raw_ee_exports/` and `data/ndvi_all.csv`.

**Before submitting:** verify in the selected Field Shift challenge's official Resources tab that at least one of the NASA data sources above appears among the listed challenge resources, and make that connection explicit. The challenge page itself is https://www.spaceappschallenge.org/2026/challenges/field-shift-adapting-farms-with-nasa-data/.

## 8. Other data, resources, and tools

- BARC: Hossain, M.B. et al. (2024), *Fertilizer Recommendation Guide-2024*, Bangladesh Agricultural Research Council, Dhaka. https://apps.barc.gov.bd/fertilizer_recommendation/FRG%20English%2030.10.2024.pdf
- BRRI: Bangladesh Rice Research Institute (2018), *Annual Report 2017–2018*, Irrigation & Water Management Division, CROPWAT Tables 5–6, pp. 96–97. https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-brri/2024/12/5ab3dc06b8414cea98ec83d291f6da60.pdf
- FAO-56: Allen et al. (1998), *Crop Evapotranspiration: Guidelines for Computing Crop Water Requirements*, FAO Irrigation and Drainage Paper 56.
- USDA-SCS effective-rainfall calculation implemented in the scoring module.
- Software: Python, Streamlit, pandas, NumPy, Requests, Google Earth Engine JavaScript API, Git.
- Prior computer vision: YOLOv8 and Roboflow-hosted datasets used in the earlier Farmbot work. Add exact dataset links, terms, and upstream credits from the original model-training records before publication.
- Team-supplied media: original outdoor Farmbot field photograph and YOLOv8 ripe/unripe tomato detection image; an actual processed MODIS NDVI chart is also included. The prior Farmbot interface screenshot and RViz/Gazebo simulation image are not used as RotaShift interface evidence.
- Existing dashboard component: the original project notes say a `helper.py` component was adapted from another author's open Streamlit project. Confirm its original author, licence, and required attribution before adding an open-source licence to this repository.

## Team

Soil-to-Sky Robo Team — Dhaka Local Event. Team lead: MD Zonayed. Add the exact five teammate names and their roles from the official team registration page before submission.

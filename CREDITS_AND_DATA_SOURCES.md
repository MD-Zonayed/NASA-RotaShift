# Credits and Data Sources

## NASA / satellite

- NASA POWER daily API: https://power.larc.nasa.gov/api/temporal/daily/point — variables `T2M`, `PRECTOTCORR`, `RH2M` (live integration in `src/nasa_power.py`).
- NASA SMAP SPL3SMP_E V006 Earth Engine catalog: https://developers.google.com/earth-engine/datasets/catalog/NASA_SMAP_SPL3SMP_E_006. Raw export files are included in `data/raw_ee_exports/`.
- NASA MODIS Terra MOD13Q1 V6.1 Earth Engine catalog: https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD13Q1. Raw export files and processed NDVI summaries are included.
- NASA HLS V002 catalog: https://developers.google.com/earth-engine/datasets/catalog/NASA_HLS_HLSS30_v002. Export logic is present; HLS result files were not supplied.

## Agronomy

- Hossain, M.B. et al. (2024). *Fertilizer Recommendation Guide-2024*. Bangladesh Agricultural Research Council (BARC), Dhaka. https://apps.barc.gov.bd/fertilizer_recommendation/FRG%20English%2030.10.2024.pdf
- Bangladesh Rice Research Institute (2018). *Annual Report 2017–2018*, Irrigation & Water Management Division, CROPWAT Tables 5–6, pp. 96–97. https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-brri/2024/12/5ab3dc06b8414cea98ec83d291f6da60.pdf
- Allen, R.G. et al. (1998). *Crop Evapotranspiration: Guidelines for Computing Crop Water Requirements*. FAO Irrigation and Drainage Paper 56.
- USDA-SCS effective-rainfall formula is implemented in the rotation scoring module.

## Prior Farmbot research and assets

- Team's pre-existing undergraduate Farmbot prototype, sensor node, and YOLOv8 tomato ripeness/weed detection work.
- Team-provided video: https://www.youtube.com/watch?v=VWTlKhXIzMg
- The original archive notes that Roboflow-hosted datasets were used in prior model training. Add the exact dataset URLs, creators, versions, and licence terms from the original training records before public release.
- Images in `assets/` were supplied in the team's project archive.

## Third-party software / licence review

The original project documentation states that a previous dashboard helper component (`helper.py`) was adapted from another author's open Streamlit project. The original project URL, author attribution, and licence are not present in the uploaded archives. The adapted component is not included as a separate `helper.py` file in this repository, but the app may contain adapted patterns. Identify and credit the upstream work and confirm licence compatibility before adding a repository-wide open-source licence.

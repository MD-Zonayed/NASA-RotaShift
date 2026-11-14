# Point-only QA diagnostics

The included point-export CSVs contain dates, site metadata, and QA flags (SMAP) or DetailedQA values (MODIS), but their rows do not contain actual SMAP soil-moisture or MODIS NDVI measurement columns. They are retained as diagnostics only. Use the buffered raw exports in `data/raw_ee_exports/` for the supplied raw data and the processed `data/smap_all.csv` / `data/ndvi_all.csv` for current app plots.

from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]

def test_crop_and_rotation_counts():
    crops = pd.read_csv(ROOT / "data/crops.csv", comment="#")
    assert len(crops) == 13
    assert crops.groupby("slot").size().to_dict() == {"kharif1": 4, "kharif2": 3, "rabi": 6}
    assert 6 * 4 * 3 == 72

def test_barc_classes_and_rows():
    barc = pd.read_csv(ROOT / "data/barc_frg.csv", comment="#")
    assert len(barc) == 52
    assert barc.crop.nunique() == 13
    assert set(barc.fertility_class) == {"Optimum", "Medium", "Low", "Very low"}

def test_processed_satellite_status():
    smap = pd.read_csv(ROOT / "data/smap_all.csv")
    ndvi = pd.read_csv(ROOT / "data/ndvi_all.csv")
    assert len(smap) == 450
    assert (smap.quality == "flagged_not_recommended").all()
    assert len(ndvi) == 30
    assert ndvi.groupby("site_id").size().to_dict() == {"araihazar": 16, "uttara_sector_17": 14}

def test_synthetic_files_are_labelled():
    p = ROOT / "data/demo_synthetic/farmbot_sensor_log_POPULATED_SYNTHETIC.csv"
    d = pd.read_csv(p)
    assert d.data_status.astype(str).str.contains("SYNTHETIC", case=False).all()

#!/usr/bin/env python3
"""Fit per-probe linear calibration from paired raw readings and reference VWC.

Input CSV must contain: probe_id, raw_sensor_reading, reference_vwc_pct
At least 8 valid paired observations per probe are required. The output is a
calibration candidate, not a validation certificate; reserve independent samples
for validation before using it as ground truth.
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
import pandas as pd

REQUIRED = {'probe_id', 'raw_sensor_reading', 'reference_vwc_pct'}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('csv', help='paired calibration sample CSV')
    p.add_argument('--out', default='soil_moisture_calibration_candidate.json')
    p.add_argument('--probe-col', default='probe_id'); p.add_argument('--raw-col', default='raw_sensor_reading'); p.add_argument('--ref-col', default='reference_vwc_pct')
    args = p.parse_args()
    d = pd.read_csv(args.csv).rename(columns={args.probe_col: 'probe_id', args.raw_col: 'raw_sensor_reading', args.ref_col: 'reference_vwc_pct'})
    missing = REQUIRED - set(d.columns)
    if missing:
        sys.exit(f'Missing required columns: {sorted(missing)}')
    d['raw_sensor_reading'] = pd.to_numeric(d.raw_sensor_reading, errors='coerce')
    d['reference_vwc_pct'] = pd.to_numeric(d.reference_vwc_pct, errors='coerce')
    d = d.dropna(subset=['probe_id', 'raw_sensor_reading', 'reference_vwc_pct'])
    if d.empty:
        sys.exit('No paired numeric calibration observations found.')
    result = {
        'status': 'CANDIDATE_ONLY_REQUIRES_INDEPENDENT_VALIDATION',
        'method': 'per-probe ordinary least squares linear fit',
        'input_file': str(Path(args.csv).name),
        'probes': {}
    }
    for probe, g in d.groupby('probe_id'):
        if len(g) < 8 or g.raw_sensor_reading.nunique() < 4:
            print(f'WARNING: probe {probe}: need >=8 rows and >=4 distinct raw values; skipped')
            continue
        x = g.raw_sensor_reading.to_numpy(float)
        y = g.reference_vwc_pct.to_numpy(float)
        slope, intercept = np.polyfit(x, y, 1)
        pred = slope*x + intercept
        rmse = float(np.sqrt(np.mean((y-pred)**2)))
        mae = float(np.mean(np.abs(y-pred)))
        ss_res = float(np.sum((y-pred)**2)); ss_tot = float(np.sum((y-y.mean())**2))
        r2 = float(1-ss_res/ss_tot) if ss_tot else None
        result['probes'][str(probe)] = {
            'n': int(len(g)), 'slope': float(slope), 'intercept': float(intercept),
            'r2_in_sample': r2, 'rmse_in_sample_vwc_percentage_points': rmse,
            'mae_in_sample_vwc_percentage_points': mae,
            'raw_min': float(x.min()), 'raw_max': float(x.max()),
            'reference_vwc_min_pct': float(y.min()), 'reference_vwc_max_pct': float(y.max()),
            'formula': 'predicted_vwc_pct = slope * raw_sensor_reading + intercept'
        }
    if not result['probes']:
        sys.exit('No probe had sufficient observations. No calibration file written.')
    Path(args.out).write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(f'Wrote candidate calibration: {args.out}')
    print('Do not call this validated until tested on separate held-out soil samples.')

if __name__ == '__main__':
    main()

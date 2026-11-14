/**** RotaShift DIAGNOSTIC export (UNTESTED - I could not run Earth Engine). No QA masking in Earth Engine: values AND quality bands are exported
 * so quality filtering is done transparently in Python. Adds a buffered mean (SMAP 15 km, NDVI 500 m) beside the point value.
 * Approximate locality coordinates - replace with plot-centre GPS. 4 CSVs go to Google Drive (Tasks tab -> Run). */
var START = '2025-11-01', END = '2026-11-01';
var sites = [['uttara_sector_17', 90.37185, 23.84764], ['araihazar', 90.65315, 23.79267]];
var smap = ee.ImageCollection('NASA/SMAP/SPL3SMP_E/006').filterDate(START, END);
var mod = ee.ImageCollection('MODIS/061/MOD13Q1').filterDate(START, END);
sites.forEach(function(s) {
  var pt = ee.Geometry.Point([s[1], s[2]]);
  var smapRows = ee.FeatureCollection(smap.map(function(img) {
    var b = img.select(['soil_moisture_am', 'soil_moisture_pm', 'retrieval_qual_flag_am', 'retrieval_qual_flag_pm']);
    var p = b.reduceRegion({reducer: ee.Reducer.first(), geometry: pt, scale: 9000});
    var m = img.select(['soil_moisture_am', 'soil_moisture_pm']).reduceRegion({
      reducer: ee.Reducer.mean().combine({reducer2: ee.Reducer.count(), sharedInputs: true}), geometry: pt.buffer(15000), scale: 9000});
    return ee.Feature(null, p.combine(m)).set({date: img.date().format('YYYY-MM-dd'), site_id: s[0]});
  }));
  Export.table.toDrive({collection: smapRows, description: 'RotaShift_SMAP_unmasked_' + s[0], fileFormat: 'CSV'});
  var ndviRows = ee.FeatureCollection(mod.map(function(img) {
    var nd = img.select('NDVI').multiply(0.0001).rename('ndvi_point');
    var p = nd.addBands(img.select(['DetailedQA', 'SummaryQA'])).reduceRegion({reducer: ee.Reducer.first(), geometry: pt, scale: 250});
    var m = nd.rename('ndvi_buf500_mean').reduceRegion({reducer: ee.Reducer.mean(), geometry: pt.buffer(500), scale: 250});
    return ee.Feature(null, p.combine(m)).set({composite_start_date: img.date().format('YYYY-MM-dd'), site_id: s[0]});
  }));
  Export.table.toDrive({collection: ndviRows, description: 'RotaShift_NDVI_unmasked_' + s[0], fileFormat: 'CSV'});
});
print('Start the 4 exports in the Tasks tab.');

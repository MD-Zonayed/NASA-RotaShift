/**** RotaShift: ACTUAL NASA SMAP + MODIS exports for two approximate Bangladesh points.
 * Run in https://code.earthengine.google.com/ after Earth Engine access is enabled.
 * Coordinates are locality references, NOT surveyed plot GPS. Replace before claiming field-scale results.
 * Outputs: 4 CSVs in Google Drive. This script retrieves actual catalog imagery, not the synthetic demo CSVs.
 * SMAP collection: NASA/SMAP/SPL3SMP_E/006; AM/PM retrieval QA must equal 0 (pass per GEE catalog).
 * MODIS collection: MODIS/061/MOD13Q1; NDVI scaled by 0.0001 and DetailedQA filtered.
 */
var START = '2025-11-01';
var END = '2026-11-01'; // end-exclusive
var sites = ee.FeatureCollection([
  ee.Feature(ee.Geometry.Point([90.37185, 23.84764]), {site_id:'uttara_sector_17', site_name:'Uttara Sector 17, Dhaka', latitude_deg:23.84764, longitude_deg:90.37185, coordinate_status:'APPROXIMATE_LOCALITY_NOT_FIELD_GPS'}),
  ee.Feature(ee.Geometry.Point([90.65315, 23.79267]), {site_id:'araihazar', site_name:'Araihazar, Narayanganj', latitude_deg:23.79267, longitude_deg:90.65315, coordinate_status:'APPROXIMATE_LOCALITY_NOT_FIELD_GPS'})
]);
Map.centerObject(sites, 10); Map.addLayer(sites, {color:'red'}, 'Approximate RotaShift sites');

// SMAP Enhanced L3 radiometer daily 9 km, AM and PM retrievals.
var smap = ee.ImageCollection('NASA/SMAP/SPL3SMP_E/006').filterDate(START, END);
function smapRows(site) {
  var imageList = smap.toList(smap.size());
  var fc = ee.FeatureCollection(imageList.map(function(item) {
    var img = ee.Image(item);
    var amQ = img.select('retrieval_qual_flag_am');
    var pmQ = img.select('retrieval_qual_flag_pm');
    var am = img.select('soil_moisture_am').updateMask(amQ.eq(0)).multiply(100).rename('smap_vwc_am_pct');
    var pm = img.select('soil_moisture_pm').updateMask(pmQ.eq(0)).multiply(100).rename('smap_vwc_pm_pct');
    var values = ee.Image.cat([am, pm, amQ.rename('retrieval_qual_flag_am'), pmQ.rename('retrieval_qual_flag_pm')]).reduceRegion({
      reducer: ee.Reducer.first(), geometry: site.geometry(), scale: 9000, maxPixels: 1e8
    });
    return ee.Feature(null, values).set({date:img.date().format('YYYY-MM-dd'), site_id:site.get('site_id'),
      site_name:site.get('site_name'), latitude_deg:site.get('latitude_deg'), longitude_deg:site.get('longitude_deg'),
      coordinate_status:site.get('coordinate_status'), product:'NASA/SMAP/SPL3SMP_E/006', resolution_m:9000});
  }));
  return fc;
}
var u = ee.Feature(sites.filter(ee.Filter.eq('site_id','uttara_sector_17')).first());
var a = ee.Feature(sites.filter(ee.Filter.eq('site_id','araihazar')).first());
Export.table.toDrive({collection:smapRows(u), description:'RotaShift_SMAP_Uttara_actual', fileNamePrefix:'RotaShift_SMAP_Uttara_actual', fileFormat:'CSV'});
Export.table.toDrive({collection:smapRows(a), description:'RotaShift_SMAP_Araihazar_actual', fileNamePrefix:'RotaShift_SMAP_Araihazar_actual', fileFormat:'CSV'});

// MODIS Terra MOD13Q1 16-day, 250 m. Retain good MODLAND QA, high usefulness, low/climatological aerosol,
// no adjacent or mixed clouds, land pixels only, no snow and no shadow. Values scaled to 0-1 by 0.0001.
var modis = ee.ImageCollection('MODIS/061/MOD13Q1').filterDate(START, END);
function cleanNdvi(img) {
  var qa = img.select('DetailedQA');
  var good = qa.bitwiseAnd(3).eq(0)
    .and(qa.rightShift(2).bitwiseAnd(15).lte(2))
    .and(qa.rightShift(6).bitwiseAnd(3).lte(1))
    .and(qa.rightShift(8).bitwiseAnd(1).eq(0))
    .and(qa.rightShift(10).bitwiseAnd(1).eq(0))
    .and(qa.rightShift(11).bitwiseAnd(7).eq(1))
    .and(qa.rightShift(14).bitwiseAnd(1).eq(0))
    .and(qa.rightShift(15).bitwiseAnd(1).eq(0));
  return img.select('NDVI').multiply(0.0001).updateMask(good).rename('ndvi')
    .addBands(qa.rename('DetailedQA')).copyProperties(img,['system:time_start']);
}
var ndvi = modis.map(cleanNdvi);
function ndviRows(site) {
  var imageList = ndvi.toList(ndvi.size());
  return ee.FeatureCollection(imageList.map(function(item) {
    var img = ee.Image(item);
    var v = img.reduceRegion({reducer:ee.Reducer.first(), geometry:site.geometry(), scale:250, maxPixels:1e8});
    return ee.Feature(null,v).set({composite_start_date:img.date().format('YYYY-MM-dd'), site_id:site.get('site_id'),
      site_name:site.get('site_name'), latitude_deg:site.get('latitude_deg'), longitude_deg:site.get('longitude_deg'),
      coordinate_status:site.get('coordinate_status'), product:'MODIS/061/MOD13Q1', resolution_m:250,
      ndvi_scale_factor_applied:0.0001});
  }));
}
Export.table.toDrive({collection:ndviRows(u), description:'RotaShift_MODIS_NDVI_Uttara_actual', fileNamePrefix:'RotaShift_MODIS_NDVI_Uttara_actual', fileFormat:'CSV'});
Export.table.toDrive({collection:ndviRows(a), description:'RotaShift_MODIS_NDVI_Araihazar_actual', fileNamePrefix:'RotaShift_MODIS_NDVI_Araihazar_actual', fileFormat:'CSV'});
print('SMAP images', smap.size()); print('MODIS composites', modis.size());
print('Use Task tab to start all 4 Drive exports. Nulls indicate no valid retrieval at the sampled pixel/date.');

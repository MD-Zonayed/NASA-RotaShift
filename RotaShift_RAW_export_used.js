/***************************************************************
 ROTASHIFT: RAW NASA SATELLITE DATA EXPORT
 SMAP + MODIS NDVI + NASA HLS 30m

 Date range: 14 Nov 2025 - 14 Nov 2026
 End date is exclusive: 15 Nov 2026

 IMPORTANT:
 Coordinates are approximate locality centres, not verified
 Farmbot plot coordinates.

 No user-defined QA filtering is applied before export.
***************************************************************/

// ============================================================
// 1. SETTINGS
// ============================================================

var START_DATE = '2025-11-14';
var END_DATE = '2026-11-15';

var NO_DATA = -9999;

// Coordinates use [longitude, latitude] in Earth Engine.

var sites = [
  {
    site_id: 'uttara_sector_17',
    site_name: 'Uttara Sector 17, Dhaka',
    latitude: 23.84764,
    longitude: 90.37185,
    coordinate_status: 'APPROXIMATE_NOT_PLOT_GPS'
  },
  {
    site_id: 'araihazar',
    site_name: 'Araihazar, Narayanganj',
    latitude: 23.79267,
    longitude: 90.65315,
    coordinate_status: 'APPROXIMATE_NOT_PLOT_GPS'
  }
];

// Context buffers, NOT actual field boundaries.

var SMAP_BUFFER = 18000;
var MODIS_BUFFER = 1000;
var HLS_BUFFER = 150;

// Convert site definitions into Earth Engine features.

var siteFeatures = ee.FeatureCollection(
  sites.map(function(s) {
    return ee.Feature(
      ee.Geometry.Point([s.longitude, s.latitude]),
      {
        site_id: s.site_id,
        site_name: s.site_name,
        latitude: s.latitude,
        longitude: s.longitude,
        coordinate_status: s.coordinate_status
      }
    );
  })
);

var uttara = ee.Feature(
  siteFeatures.filter(
    ee.Filter.eq('site_id', 'uttara_sector_17')
  ).first()
);

var araihazar = ee.Feature(
  siteFeatures.filter(
    ee.Filter.eq('site_id', 'araihazar')
  ).first()
);

// Display approximate locations.

Map.centerObject(siteFeatures, 10);

Map.addLayer(
  siteFeatures,
  {color: 'red'},
  'RotaShift provisional locations'
);

print('RotaShift sites:', siteFeatures);

print(
  'WARNING: Coordinates are approximate locality references, not surveyed plot centres.'
);


// ============================================================
// 2. GENERAL RAW PIXEL EXPORT FUNCTION
// ============================================================

function extractRawPixels(
  collection,
  bands,
  site,
  bufferMeters,
  scaleMeters,
  productName,
  sensorName
) {

  var sorted = collection.sort('system:time_start');

  var imageList = sorted.toList(sorted.size());

  var result = ee.FeatureCollection(
    imageList.iterate(function(imageObject, accumulator) {

      var image = ee.Image(imageObject);

      // Retain original data and QA bands.
      // Missing/source-masked pixels become -9999.
      var rawImage = image.select(bands).unmask(NO_DATA);

      var samples = rawImage.sample({

        region: site.geometry().buffer(bufferMeters),

        scale: scaleMeters,

        geometries: true,

        dropNulls: false,

        tileScale: 4

      });

      var annotated = samples.map(function(pixel) {

        var coordinates = pixel.geometry().coordinates();

        return pixel.set({

          observation_date:
            image.date().format('YYYY-MM-dd'),

          observation_time_utc_ms:
            image.get('system:time_start'),

          source_image_index:
            image.get('source_image_index'),

          product_id:
            productName,

          sensor_platform:
            sensorName,

          site_id:
            site.get('site_id'),

          site_name:
            site.get('site_name'),

          site_center_latitude_deg:
            site.get('latitude'),

          site_center_longitude_deg:
            site.get('longitude'),

          coordinate_status:
            site.get('coordinate_status'),

          pixel_longitude_deg:
            coordinates.get(0),

          pixel_latitude_deg:
            coordinates.get(1),

          distance_from_reference_point_m:
            pixel.geometry().distance(site.geometry(), 1),

          context_buffer_radius_m:
            bufferMeters,

          qa_filter_applied_before_export:
            'NONE_RAW_QA_RETAINED',

          no_data_fill_value:
            NO_DATA

        });

      });

      return ee.FeatureCollection(accumulator)
        .merge(annotated);

    }, ee.FeatureCollection([]))
  );

  return result;
}


// ============================================================
// 3. EXPORT FUNCTION
// ============================================================

function exportCSV(collection, fileName) {

  Export.table.toDrive({

    collection: collection,

    description: fileName,

    fileNamePrefix: fileName,

    fileFormat: 'CSV'

  });

}


// ============================================================
// 4. NASA SMAP V006 — RAW SOIL MOISTURE
// ============================================================

// Official dataset:
// NASA/SMAP/SPL3SMP_E/006

var smap = ee.ImageCollection(
  'NASA/SMAP/SPL3SMP_E/006'
).filterDate(
  START_DATE,
  END_DATE
);

// Preserve raw retrieval flags.
// Recommended-quality values are 0 OR 8
// according to the NSIDC Version 6 User Guide.

var smapBands = [

  'soil_moisture_am',
  'retrieval_qual_flag_am',

  'tb_qual_flag_h_am',
  'tb_qual_flag_v_am',

  'vegetation_water_content_am',
  'soil_moisture_am_anomaly',

  'soil_moisture_pm',
  'retrieval_qual_flag_pm',

  'tb_qual_flag_h_pm',
  'tb_qual_flag_v_pm',

  'vegetation_water_content_pm',
  'soil_moisture_pm_anomaly'

];

// Uttara SMAP.

var smapUttara = extractRawPixels(

  smap,
  smapBands,
  uttara,
  SMAP_BUFFER,
  9000,
  'NASA/SMAP/SPL3SMP_E/006',
  'SMAP_L3_E_9KM'

);

// Araihazar SMAP.

var smapAraihazar = extractRawPixels(

  smap,
  smapBands,
  araihazar,
  SMAP_BUFFER,
  9000,
  'NASA/SMAP/SPL3SMP_E/006',
  'SMAP_L3_E_9KM'

);

exportCSV(
  smapUttara,
  'RotaShift_SMAP_RAW_Uttara'
);

exportCSV(
  smapAraihazar,
  'RotaShift_SMAP_RAW_Araihazar'
);


// ============================================================
// 5. MODIS MOD13Q1 — RAW NDVI
// ============================================================

// Official dataset:
// MODIS/061/MOD13Q1

var modis = ee.ImageCollection(
  'MODIS/061/MOD13Q1'
).filterDate(
  START_DATE,
  END_DATE
);

var modisBands = [

  'NDVI',
  'EVI',
  'DetailedQA',
  'SummaryQA',
  'DayOfYear'

];

// Uttara MODIS.

var modisUttara = extractRawPixels(

  modis,
  modisBands,
  uttara,
  MODIS_BUFFER,
  250,
  'MODIS/061/MOD13Q1',
  'MODIS_TERRA_250M'

);

// Araihazar MODIS.

var modisAraihazar = extractRawPixels(

  modis,
  modisBands,
  araihazar,
  MODIS_BUFFER,
  250,
  'MODIS/061/MOD13Q1',
  'MODIS_TERRA_250M'

);

exportCSV(
  modisUttara,
  'RotaShift_MODIS_RAW_Uttara'
);

exportCSV(
  modisAraihazar,
  'RotaShift_MODIS_RAW_Araihazar'
);


// ============================================================
// 6. NASA HLS L30 — LANDSAT 30m
// ============================================================

// Official collection:
// NASA/HLS/HLSL30/v002

// HLS L30:
// B4 = Red
// B5 = NIR
// Fmask = QA information

function prepareHLSL30(image) {

  var red = image.select('B4')
    .rename('red_raw');

  var nir = image.select('B5')
    .rename('nir_raw');

  var fmask = image.select('Fmask')
    .rename('fmask_raw');

  var denominator = nir.add(red);

  var ndvi = nir.subtract(red)
    .divide(denominator)
    .updateMask(denominator.neq(0))
    .rename('ndvi_ratio_raw');

  return ee.Image.cat([
    red,
    nir,
    fmask,
    ndvi
  ])
  .copyProperties(image, ['system:time_start'])
  .set({

    source_image_index: image.get('system:index'),

    source_product_uri: image.get('PRODUCT_URI'),

    cloud_coverage_pct: image.get('CLOUD_COVERAGE'),

    sensor_platform: 'HLS_L30_LANDSAT',

    reflectance_scale_factor: 0.0001,

    reflectance_offset: 0

  });

}


// ============================================================
// 7. NASA HLS S30 — SENTINEL-2 30m
// ============================================================

// Official collection:
// NASA/HLS/HLSS30/v002

// HLS S30:
// B4 = Red
// B8 = Broad NIR
// Fmask = QA information

function prepareHLSS30(image) {

  var red = image.select('B4')
    .rename('red_raw');

  var nir = image.select('B8')
    .rename('nir_raw');

  var fmask = image.select('Fmask')
    .rename('fmask_raw');

  var denominator = nir.add(red);

  var ndvi = nir.subtract(red)
    .divide(denominator)
    .updateMask(denominator.neq(0))
    .rename('ndvi_ratio_raw');

  return ee.Image.cat([
    red,
    nir,
    fmask,
    ndvi
  ])
  .copyProperties(image, ['system:time_start'])
  .set({

    source_image_index: image.get('system:index'),

    source_product_uri: image.get('PRODUCT_URI'),

    cloud_coverage_pct: image.get('CLOUD_COVERAGE'),

    sensor_platform: 'HLS_S30_SENTINEL2',

    reflectance_scale_factor: 0.0001,

    reflectance_offset: 0

  });

}


// Load both HLS collections.

var hlsL30 = ee.ImageCollection(
  'NASA/HLS/HLSL30/v002'
)
.filterDate(START_DATE, END_DATE)
.map(prepareHLSL30);


var hlsS30 = ee.ImageCollection(
  'NASA/HLS/HLSS30/v002'
)
.filterDate(START_DATE, END_DATE)
.map(prepareHLSS30);


// Combine Landsat and Sentinel-2.

var hls = hlsL30.merge(hlsS30)
  .sort('system:time_start');

var hlsBands = [

  'red_raw',
  'nir_raw',
  'fmask_raw',
  'ndvi_ratio_raw'

];


// ============================================================
// 8. EXPORT HLS FOR BOTH LOCATIONS
// ============================================================

var hlsUttara = extractRawPixels(

  hls,
  hlsBands,
  uttara,
  HLS_BUFFER,
  30,
  'NASA_HLS_L30_S30_V002',
  'HLS_30M'

);

var hlsAraihazar = extractRawPixels(

  hls,
  hlsBands,
  araihazar,
  HLS_BUFFER,
  30,
  'NASA_HLS_L30_S30_V002',
  'HLS_30M'

);

exportCSV(
  hlsUttara,
  'RotaShift_HLS30_RAW_Uttara'
);

exportCSV(
  hlsAraihazar,
  'RotaShift_HLS30_RAW_Araihazar'
);


// ============================================================
// 9. CHECK DATA AVAILABILITY
// ============================================================

function reportAvailability(name, collection) {

  print(name + ' image count:', collection.size());

  print(
    name + ' latest observation UTC:',
    collection.aggregate_max('system:time_start')
  );

}

reportAvailability('SMAP V006', smap);

reportAvailability('MODIS MOD13Q1', modis);

reportAvailability('HLS Landsat L30', hlsL30);

reportAvailability('HLS Sentinel-2 S30', hlsS30);


print('-------------------------------------');

print('Six CSV export tasks have been created.');

print('No user-defined QA filters applied.');

print('SMAP recommended-quality flags: 0 OR 8.');

print('MODIS NDVI scale factor: 0.0001.');

print('HLS raw reflectance and Fmask are retained.');

print('Approximate coordinates are not plot GPS.');

print('Open the Tasks tab and start all six exports.');

print('-------------------------------------');

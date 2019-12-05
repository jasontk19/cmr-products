def get_cmr_keep_keys():
  return [
    'id',
    'version_id',
    'title',
    'processing_level_id', 
    'archive_center', 
    'data_center', 
    'organizations',  
    'score'
  ]

def get_cmr_umm_keep_keys():
  return [
    'ScienceKeywords', 
    'AncillaryKeywords', 
    'TemporalExtents', 
    'ProcessingLevel', 
    'Version', 
    'Projects', 
    'Platforms', 
    'DataCenters'
  ]
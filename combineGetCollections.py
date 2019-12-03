from urllib.request import urlopen
import json

new_layers = {}
cmr_data_store = {}
cmr_collection_url = 'https://cmr.earthdata.nasa.gov/search/collections.json?shortName='
cmr_umm_collection_url = 'https://cmr.earthdata.nasa.gov/search/collections.umm_json?shortName='
cmr_keep_keys = [
  'id',
  'title'
  'processing_level_id', 
  'archive_center', 
  'data_center', 
  'organizations',  
  'score'
]
cmr_umm_keep_keys = [
  'ScienceKeywords', 
  'AncillaryKeywords', 
  'TemporalExtents', 
  'ProcessingLevel', 
  'Version', 
  'Projects', 
  'Platforms', 
  'DataCenters'
]


def process_entries(entries, keep_keys):
  new_entries = []
  for entry in entries:
    new_entry = {}
    for key in keep_keys:
      new_entry[key] = entry.get(key, None)
    new_entries.append(new_entry)
  return new_entries


def get_cmr_data(shortName):
  if not cmr_data_store.get(shortName, None):
    with urlopen(cmr_collection_url + shortName) as url:
      data = json.loads(url.read().decode())
      feed = data.get('feed', None)
      entries = feed.get('entry', None)
      cmr_data_store[shortName]['cmr'] = process_entries(entries, cmr_keep_keys)
      if len(entries) > 1:
        print(shortName)
  
    with urlopen(cmr_umm_collection_url + shortName) as url:
      collections = []
      data = json.loads(url.read().decode())
      items = data.get('items', [])
      for item in items:
        entries = [item.get('umm', None)]
        collections.append(process_entries(entries, cmr_umm_keep_keys)[0])
      cmr_data_store[shortName]['umm'] = collections
      if len(entries) > 1:
        print(shortName)
  

def get_layers_products():
  # Open wv.json and get collection info from CMR based on product ID
  with open('json/wv.json', mode='rt', encoding='utf-8') as wv:
    wv_json = json.load(wv)

    for key, value in wv_json['layers'].items():
      product_key = value.get('product', None)
      if type(product_key) is list:
        for prod_key in product_key:
          cmr_data_store[prod_key] = {}
      elif product_key is not None and product_key is not '':
        cmr_data_store[product_key] = {}

    count = 0
    for key in cmr_data_store:
      get_cmr_data(key)
      count = count+1
      # if count >= 25:
      #   break

  with open('json/output/collections.json', mode='wt', encoding='utf-8') as lp:
    lp.write(json.dumps(cmr_data_store))
  
get_layers_products()
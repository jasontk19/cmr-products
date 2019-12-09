from urllib.request import urlopen
import json
from keepKeys import get_cmr_keep_keys, get_cmr_umm_keep_keys
from attrValues import store_attr_values, write_values_to_files

new_layers = {}
cmr_data_store = {}
cmr_collection_url = 'https://cmr.earthdata.nasa.gov/search/collections.json?shortName='
cmr_umm_collection_url = 'https://cmr.earthdata.nasa.gov/search/collections.umm_json?shortName='
cmr_keep_keys = get_cmr_keep_keys()
cmr_umm_keep_keys = get_cmr_umm_keep_keys()

def process_entries(shortName, entries, keep_keys):
  new_entries = []
  for entry in entries:
    new_entry = {}
    for key in keep_keys:
      new_entry[key] = entry.get(key)
    new_entries.append(new_entry)
    store_attr_values(shortName, new_entries)
  return new_entries


def get_cmr_data(shortName):
  print('Fetching data for: ', shortName)
  cmr_entry = cmr_data_store.get(shortName, {}).get('cmr')
  cmr_umm_entry = cmr_data_store.get(shortName, {}).get('umm')

  if not cmr_entry:
    with urlopen(cmr_collection_url + shortName) as url:
      data = json.loads(url.read().decode())
      entries = data.get('feed', {}).get('entry')
      cmr_data_store[shortName]['cmr'] = process_entries(shortName, entries, cmr_keep_keys)
  
  if not cmr_umm_entry:
    with urlopen(cmr_umm_collection_url + shortName) as url:
      collections = []
      data = json.loads(url.read().decode())
      items = data.get('items', [])
      for item in items:
        entries = [item.get('umm')]
        collections.append(process_entries(shortName, entries, cmr_umm_keep_keys)[0])
      cmr_data_store[shortName]['umm'] = collections
  

def get_layers_products():
  # Open wv.json and get collection info from CMR based on product ID
  with open('/Users/jtkent/sandbox/python-learning/products/json/wv.json', mode='rt', encoding='utf-8') as wv:
    wv_json = json.load(wv)

    for key, value in wv_json['layers'].items():
      product_key = value.get('product')
      if type(product_key) is list:
        for prod_key in product_key:
          cmr_data_store[prod_key] = { 'wv-id': key }
      elif product_key is not None and product_key is not '':
        cmr_data_store[product_key] = { 'wv-id': key }

    # count = 0
    for key in cmr_data_store:
      get_cmr_data(key)
      # count = count+1
      # if count >= 25:
      #   break

    write_values_to_files()
  # with open('json/output/collections.json', mode='wt', encoding='utf-8') as lp:
  #   lp.write(json.dumps(cmr_data_store))
  
get_layers_products()
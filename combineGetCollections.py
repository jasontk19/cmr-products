"""
Combines layers and products from wvjson
"""
from urllib.request import urlopen
import json
new_layers = {}
cmr_data_store = {}
cmr_umm_data_store = {}
cmrCollectionUrl = 'https://cmr.earthdata.nasa.gov/search/collections.json?shortName='
cmrUmmCollectionUrl = 'https://cmr.earthdata.nasa.gov/search/collections.umm_json?shortName='

def processEntries(entries):
  return entries

def getCmrData(shortName):
  collectionsData = []
  if cmr_data_store.get(shortName, None):
    return cmr_data_store[shortName]
  print('Fetching collection data for:', shortName)

  # fetch cmr collection data
  collectionUrl = cmrCollectionUrl + shortName
  with urlopen(collectionUrl) as url:
    cmrData = json.loads(url.read().decode())
    feed = cmrData.get('feed', None)
    if feed:
      cmr_data_store[shortName] = processEntries(feed.get('entry', None))
      collectionsData.append(cmr_data_store[shortName])
    
  # fetch cmr-umm collection data
  fetchUrl = cmrCollectionUrl + shortName
  with urlopen(fetchUrl) as url:
    cmrData = json.loads(url.read().decode())
    items = cmrData.get('items', [])
    if len(items):
      cmr_umm_data_store[shortName] = items
      collectionsData.append(cmr_umm_data_store[shortName])
  
  return collectionsData


def append_product(l_key, product_key):
  if not product_key:
    return
  new_product = {}
  new_product['id'] = product_key
  new_product['entries'] = getCmrData(product_key)
  new_layers[l_key]['collections'].append(new_product)

  
def get_layers_products():
  # Open wv.json and get collection info from CMR based on product ID
  with open('json/wv.json', mode='rt', encoding='utf-8') as wv:
    wv_json = json.load(wv)
    for key, value in wv_json['layers'].items():
      new_layers[key] = value
      new_layers[key]['collections'] = []
      product_key = value.get('product', None)

      if type(product_key) is list:
        for prod_key in product_key:
          append_product(key, prod_key)
      elif product_key is not None and product_key is not '':
        append_product(key, product_key)

  with open('json/layers_products.json', mode='wt', encoding='utf-8') as wv:
    wv.write(json.dumps(new_layers))
  
    
get_layers_products()
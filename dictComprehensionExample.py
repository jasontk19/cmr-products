from pprint import pprint as pp
import json

def map_collection_to_product(data):
  # filter to only products that have associated collections
  filteredDict = { key: val['cmr'] for key, val in data.items() if len(val['cmr']) }

  # map collection ids to back to product ids
  collectionMappingDict = {}
  for key, val in filteredDict.items():
    for collection in val:
      collectionMappingDict[collection['id']] = key
  pp(collectionMappingDict)


with open('json/output/collections.json', mode='rt', encoding='utf-8') as col:
  data = json.load(col)

  # use dictionary comprehension to map product ids to only the CMR or UMM data arrays
  cmrCol = { prod_id: collections['cmr'] for prod_id, collections in data.items() }
  ummCol = { prod_id: collections['umm'] for prod_id, collections in data.items() }
  # pp(cmrCol)

  map_collection_to_product(data)


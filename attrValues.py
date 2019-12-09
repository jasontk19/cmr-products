import json
from pprint import pprint as pp
from keepKeys import get_cmr_keep_keys, get_cmr_umm_keep_keys
attr_value_dict = {}

def init_attr_value_dict():
  for key in get_cmr_umm_keep_keys() + get_cmr_keep_keys():
    attr_value_dict[key] = []
  return attr_value_dict


def store_attr_values(shortName, entries):
  for entry in entries:
    for key, val in entry.items():
      attr_value_dict[key].append({ shortName: val })


def write_values_to_files():
  for key, val in attr_value_dict.items():
     with open('json/output/values/'+ key +'.json', mode='w+', encoding='utf-8') as lp:
      lp.write(json.dumps(val))

init_attr_value_dict()
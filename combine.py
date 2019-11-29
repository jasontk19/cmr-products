"""
Combines layers and products from wvjson
"""
import json
new_layers = {}

def append_product(l_key, product):
  if not product:
    return
  query = product.get('query', None)
  product['id'] = query.get('shortName', None)
  new_layers[l_key]['combinedProducts'].append(product)

def combine(layers, products):
  for key, value in layers.items():
    new_layers[key] = value
    new_layers[key]['combinedProducts'] = []
    product_key = value.get('product', None)

    if type(product_key) is list:
      for prod_key in product_key:
        product = products.get(prod_key, None)
        append_product(key, product)
    elif product_key is not None and product_key is not '':
      product = products.get(product_key, None)
      append_product(key, product)
  with open('json/layers_products.json', mode='wt', encoding='utf-8') as wv:
    wv.write(json.dumps(new_layers))
      

def get_layers_products():
  with open('json/wv.json', mode='rt', encoding='utf-8') as wv:
    wv_json = json.load(wv)
    products = wv_json['products']
    layers = wv_json['layers']
    combine(layers, products)
  
    
get_layers_products()



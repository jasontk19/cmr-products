from pprint import pprint as pp
import json
found = False  

def find_product(req_product):
  with open('json/layers_products.json', mode='rt', encoding='utf-8') as wv:
    layers = json.load(wv)
    for key, value in layers.items():
      products = value.get('combinedProducts')
      for product in products:
        if product['id'] == req_product:
          print('***** Found a match: ****** \n')
          pp(product)
          return True

  print('Sorry, couldn\'t find that.')
  return False

def prompt_req():
  return input('Which product would you like to see layer info for?\n') 

def prompt_keep_going():
  bln = input('Would you like to keep searching?')
  if bln == 'y' or bln == 'Y' or bln == 'yes':
    return True
  else:
    return False

def start():
  found = False
  while not found:
    req = prompt_req()
    found = find_product(req)
  
  

start()





    


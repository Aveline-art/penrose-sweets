import sys

from bs4 import BeautifulSoup
from datetime import datetime
import json
from RecipeParsers import bingingwithbabish, cookieandkate, generalparse, gordonramsay, justonecookbook, maangchi, seriouseats, tasty, woksoflife
import requests
from urllib.parse import urlparse

parsers = {
    'www.bingingwithbabish.com': lambda x: bingingwithbabish.parse(x),
    'cookieandkate.com': lambda x: cookieandkate.parse(x),
    'www.gordonramsay.com': lambda x: gordonramsay.parse(x),
    'www.justonecookbook.com': lambda x: justonecookbook.parse(x),
    'www.maangchi.com': lambda x: maangchi.parse(x),
    'www.seriouseats.com': lambda x: seriouseats.parse(x),
    'tasty.co': lambda x: tasty.parse(x),
    'thewoksoflife.com': lambda x: woksoflife.parse(x),
}

def main(argvs):
    grocery_list = []
    url_list = []
    for url in argvs:
        ingredients = retrieve_ingredients(url)
        if ingredients:
            grocery_list.append(retrieve_ingredients(url))
            url_list.append(url)
        else:
            print(f'Could not find ingredients for {url}.')
    
    create_list(grocery_list, url_list)
    is_correct = None
    while(is_correct not in ['y', 'n']):
        is_correct = input("does the list appears to be correct? (y/n)")
    if is_correct == 'y':
        dict = {}
        for i, url in enumerate(url_list):
                dict[url] = grocery_list[i]
        with open('ingredient.json', 'w', encoding='utf8') as f:
            f.write(json.dump(dict))



def retrieve_ingredients(url):
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0'
    })

    if response.ok:
        domain = urlparse(url).netloc
        soup = BeautifulSoup(response.content, "html.parser")

        if domain in parsers.keys():
            ingredients = parsers[domain](soup)
        else:
            ingredients = generalparse.parse(soup)
        return ingredients
    else:
        return None

def create_list(grocery_list, links):
    filename = f'grocery_list_{datetime.now().strftime("%B-%d-%Y")}.txt'
    
    with open(filename, 'w', encoding='utf8') as f:
        f.write('Grocery List\n')
        f.write('---\n')
        for item in grocery_list:
            f.write(f'{item}\n')
        f.write('\n')
        f.write('Recipe Links\n')
        f.write('---\n')
        for url in links:
            f.write(f'{url}\n')

if __name__ == "__main__":
    # calling the main function
    main(sys.argv[1:])

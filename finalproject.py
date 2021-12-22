import sys

from bs4 import BeautifulSoup
from datetime import datetime
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
            grocery_list += retrieve_ingredients(url)
            url_list.append(url)
        else:
            print(f'Could not find ingredients for {url}.')
    
    filename = f'grocery_list_{datetime.now().strftime("%B-%d-%Y")}.txt'
    
    with open(filename, 'w', encoding='utf8') as f:
        f.write('Grocery List\n')
        f.write('---\n')
        for item in grocery_list:
            f.write(f'{item}\n')
        f.write('\n')
        f.write('Recipe Links\n')
        f.write('---\n')
        for url in url_list:
            f.write(f'{url}\n')
            

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

if __name__ == "__main__":
    # calling the main function
    main(sys.argv[1:])

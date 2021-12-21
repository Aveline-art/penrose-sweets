import sys

from bs4 import BeautifulSoup
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
    # TODO check that all argvs are links
    grocery_list = []
    for url in argvs:
        grocery_list += retrieve_ingredients(url)
    
    for item in grocery_list:
        print(item)

def retrieve_ingredients(url):
    page = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0'
    })
    domain = urlparse(url).netloc
    soup = BeautifulSoup(page.content, "html.parser")

    if domain in parsers.keys():
        ingredients = parsers[domain](soup)
    else:
        ingredients = generalparse.parse(soup)
    
    # TODO check that there is a result
    return ingredients

if __name__ == "__main__":
    # calling the main function
    main(sys.argv[1:])
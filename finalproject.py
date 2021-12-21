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

URL = "https://www.bingingwithbabish.com/recipes/2017/6/13/freddys-ribs-inspired-by-house-of-cards"

page = requests.get(URL, headers={
    'User-Agent': 'Mozilla/5.0'
})
domain = urlparse(URL).netloc
soup = BeautifulSoup(page.content, "html.parser")

if domain in parsers.keys():
    ingredients = parsers[domain](soup)
else:
    ingredients = generalparse.parse(soup)

print(ingredients)

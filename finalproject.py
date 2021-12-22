import sys

from bs4 import BeautifulSoup
from datetime import datetime
import json
from RecipeParsers import bingingwithbabish, cookieandkate, generalparse, gordonramsay, justonecookbook, seriouseats, tasty, woksoflife
import requests
from urllib.parse import urlparse

parsers = {
    'www.bingingwithbabish.com': lambda x: bingingwithbabish.parse(x),
    'cookieandkate.com': lambda x: cookieandkate.parse(x),
    'www.gordonramsay.com': lambda x: gordonramsay.parse(x),
    'www.justonecookbook.com': lambda x: justonecookbook.parse(x),
    'www.seriouseats.com': lambda x: seriouseats.parse(x),
    'tasty.co': lambda x: tasty.parse(x),
    'thewoksoflife.com': lambda x: woksoflife.parse(x),
}


cache_ingredients = {}
try:
    with open('ingredients.json', 'r', encoding='utf8') as f:
        cache_ingredients = json.loads(f.read())
except:
    pass

def main(argvs):
    grocery_list = []
    url_list = []

    print('Getting all ingredients...')
    for url in argvs:
        ingredients = cache_ingredients.get(url) or retrieve_ingredients(url)
        if ingredients:
            grocery_list.append(ingredients)
            url_list.append(url)
        else:
            print(f'Could not find ingredients for {url}.')
    
    assessment = assess_list(grocery_list, url_list, 'Does this grocery list for all your recipes appear to be correct? (y/n)')
    if assessment:
        create_list(grocery_list, url_list)
        return
    
    print('Redownloading recipe...')
    grocery_list = []
    url_list = []
    for url in argvs:
        ingredients = retrieve_ingredients(url)
        if ingredients:
            grocery_list.append(ingredients)
            url_list.append(url)
        else:
            print(f'Could not find ingredients for {url}.')
    assessment = assess_list(grocery_list, url_list, 'is this better? (y/n)')
    if not assessment:
        print('Sorry to hear that. This is the best that I could do.')
    create_list(grocery_list, url_list)



def retrieve_ingredients(url):
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0'
    })

    if response.ok:
        domain = urlparse(url).netloc
        soup = BeautifulSoup(response.content, "html.parser")

        if domain in parsers.keys():
            ingredients = parsers[domain](soup)
            return ingredients
        else:
            print(f'Could not find a parser for {domain}. Using a general parser.')
            ingredients = generalparse.parse(soup)
            if ingredients:
                assessment = assess_list([ingredients], [url], f'Does this list look okay for the recipe from {url}? (y/n)')
                if assessment:
                    return ingredients
    return None

def create_list(grocery_list, links):
    print('Creating grocery list.')
    filename = f'grocery_list_{datetime.now().strftime("%B-%d-%Y")}.txt'
    
    with open(filename, 'w', encoding='utf8') as f:
        f.write('Grocery List\n')
        f.write('---\n')
        for list in grocery_list:
            for item in list:
                f.write(f'{item}\n')
        f.write('\n')
        f.write('Recipe Links\n')
        f.write('---\n')
        for url in links:
            f.write(f'{url}\n')

def assess_list(grocery_list, url_list, message):
    print('Grocery List')
    print('---')
    for list in grocery_list:
        for item in list:
            print(f'{item}')
    print('\n')
    print('Recipe Links')
    print('---')
    for url in url_list:
        print(f'{url}')

    while(True):
        is_correct = input(message)
        if is_correct == 'y':
            print('Saving list')
            for i, url in enumerate(url_list):
                    cache_ingredients[url] = grocery_list[i]
            with open('ingredients.json', 'w', encoding='utf8') as f:
                f.write(json.dumps(cache_ingredients))
            return True
        elif is_correct == 'n':
            return False

if __name__ == "__main__":
    # calling the main function
    main(sys.argv[1:])

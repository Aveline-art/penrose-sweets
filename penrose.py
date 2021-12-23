from bs4 import BeautifulSoup
from datetime import datetime
import json
from RecipeParsers import bingingwithbabish, cookieandkate, generalparse, gordonramsay, justonecookbook, seriouseats, tasty, woksoflife
import requests
from urllib.parse import urlparse

class Recipe:
    parsers = {
        'www.bingingwithbabish.com': lambda x: bingingwithbabish.parse(x),
        'cookieandkate.com': lambda x: cookieandkate.parse(x),
        'www.gordonramsay.com': lambda x: gordonramsay.parse(x),
        'www.justonecookbook.com': lambda x: justonecookbook.parse(x),
        'www.seriouseats.com': lambda x: seriouseats.parse(x),
        'tasty.co': lambda x: tasty.parse(x),
        'thewoksoflife.com': lambda x: woksoflife.parse(x),
    }

    def __init__(self, url, ingredients=None) -> None:
        self.url = url
        self.ingredients = ingredients

    def get_ingredients(self):
        return self.ingredients

    def set_ingredients(self, ingredients):
        self.ingredients = ingredients
    
    def find_ingredients(self):
        response = requests.get(self.url, headers={
            'User-Agent': 'Mozilla/5.0'
        })

        if response.ok:
            domain = urlparse(self.url).netloc
            soup = BeautifulSoup(response.content, "html.parser")

            if domain in self.parsers.keys():
                ingredients = self.parsers[domain](soup)
            else:
                print(f'Could not find a parser for {domain}. Using a general parser.')
                ingredients = generalparse.parse(soup)
            if ingredients:
                return ingredients

    def verify_ingredients(self, ingredients):
        print('\n')
        print(f'Ingredients for recipe from {self.url}')
        print('---')
        for ingredient in ingredients:
            print(f'{ingredient}')
        print('\n')

        while(True):
            is_correct = input('Does this list look correct? (y/n)')
            if is_correct == 'y':
                return True
            elif is_correct == 'n':
                return False
    
    def print_ingredients(self):
        for ingredient in self.ingredients:
            print(f'{ingredient}')

class IngredientStorage:
    def __init__(self) -> None:
        self.cache_ingredients = {}
        try:
            with open('ingredients.json', 'r', encoding='utf8') as f:
                self.cache_ingredients = json.loads(f.read())
        except:
            pass
        
    def add_ingredients(self, recipe):
        self.cache_ingredients[recipe.url] = recipe.ingredients
    
    def get_ingredients(self, url):
        return self.cache_ingredients.get(url)

    def save_list(self):
        with open('ingredients.json', 'w', encoding='utf8') as f:
            f.write(json.dumps(self.cache_ingredients))

class GroceryList:
    def __init__(self) -> None:
        self.recipes = []
    
    def add_recipe(self, recipe):
        self.recipes.append(recipe)
    
    def print_list(self):
        print('\n')
        print('####################')
        print('### Grocery List ###')
        print('####################')
        print('\n')
        for recipe in self.recipes:
            print(recipe.url)
            print('---')
            recipe.print_ingredients()
            print('\n')
    
    def verify_list(self):
        self.print_list()

        while(True):
            is_correct = input('Does this grocery list appear correct? (y/n)')
            if is_correct == 'y':
                return True
            elif is_correct == 'n':
                return False
    
    def create_txt(self):
        with open(f'grocery_list_{datetime.now().strftime("%B-%d-%Y")}.txt', 'w', encoding='utf8') as f:
            f.write('Grocery List\n')
            f.write('---\n')
            for recipe in self.recipes:
                for ingredient in recipe.get_ingredients():
                    f.write(f'{ingredient}\n')
            f.write('\n')
            f.write('Recipe Links\n')
            f.write('---\n')
            for recipe in self.recipes:
                f.write(f'{recipe.url}\n')
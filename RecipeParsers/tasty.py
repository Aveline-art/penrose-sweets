import json
import re

def parse(soup):
    recipe_json = soup.find(name='script', attrs={
        'type':'application/ld+json'
    })

    return json.loads(recipe_json.text)['recipeIngredient']
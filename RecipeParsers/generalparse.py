import json

def parse(soup):
    recipe_json = soup.find(name='script', attrs={
        'id':'schema-lifestyle_1-0'
    })

    ingredients = json.loads(recipe_json.text)['recipeIngredient']
    return [item.replace('\xa0', ' ').strip() for item in ingredients if ':' not in item]
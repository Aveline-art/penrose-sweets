import json

def parse(soup):
    recipe_json = soup.find(name='script', attrs={
        'class':'yoast-schema-graph'
    })

    for item in json.loads(recipe_json.text)['@graph']:
        if type(item) is dict and 'recipeIngredient' in item.keys():
            return [ingredient.replace('((', '(').replace('))', ')') for ingredient in item['recipeIngredient']]
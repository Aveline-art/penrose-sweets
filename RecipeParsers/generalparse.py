import json

def parse(soup):
    variables = [
        ['script', {'id':'schema-lifestyle_1-0'}],
        ['script', {'class':'yoast-schema-graph'}],
        ['script', {'type':'application/ld+json'}],
    ]

    for variable in variables:
        recipe_json = soup.find(name=variable[0], attrs=variable[1])
        try:
            ingredients_json = json.loads(recipe_json.text)
            if 'recipeIngredient' in ingredients_json.keys():
                ingredients = ingredients_json['recipeIngredient']
                return [item.replace('\xa0', ' ').strip() for item in ingredients if ':' not in item]
            elif '@graph' in ingredients_json.keys():
                for item in json.loads(recipe_json.text)['@graph']:
                    if type(item) is dict and 'recipeIngredient' in item.keys():
                        return [ingredient.replace('\xa0', ' ').replace('&#8230;', '...').strip() for ingredient in item['recipeIngredient']]
        except:
            continue
    return None
import re

def parse(soup):
    ingredients_html = soup.find_all(name='div', attrs={
        'class': 'sqs-block-content'
    })

    for item in ingredients_html:
        if search_descendants(item):
            ingredients_div = item
            break
    
    ingredient_lists = ingredients_div.find_all(name='ul')

    all_ingredients = []

    for list in ingredient_lists:
        ingredients = list.find_all(name='li')
        all_ingredients += [ingredient.text.replace('\xa0', ' ').strip() for ingredient in ingredients]

    return all_ingredients

def search_descendants(soup):
    for child in soup.descendants:
        if 'Ingredients' in child:
            return True
    return False
def parse(soup):
    ingredients_html = soup.find(name='aside', attrs={
        'class':'recipe-ingredients'
    })

    ingredient_lists = ingredients_html.find_all(name='ul', attrs={
        'class': "recipe-division"
    })

    all_ingredients = []

    for list in ingredient_lists:
        ingredients = list.find_all(name='li')
        all_ingredients += [ingredient.text.replace('\xa0', ' ').strip() for ingredient in ingredients]
    
    return all_ingredients

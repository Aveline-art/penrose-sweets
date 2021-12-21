import json
import re

def parse(soup):
    recipe_json = soup.find(name='script', attrs={
        'type':'application/ld+json'
    })

    with open('ingredient.json', 'w', encoding='utf8') as f:
        f.write(recipe_json.text)

    # needs to use selemium because this thing does not work at all, man
    print('TODO, maangchi')
    for item in json.loads(recipe_json.text)['@graph']:
        if type(item) is dict and 'text' in item.keys():
            text = item['text']
            regex_text = re.search('Ingredients\.(.*)Directions\.', text)
            print(re.split(r'\. ', regex_text[1])) 
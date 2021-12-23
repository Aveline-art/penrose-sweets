import sys

from penrose import GroceryList, IngredientStorage, Recipe

def main(command, argvs):
    if command == 'add':
        add(argvs[0])
    elif command == 'groceries':
        groceries(argvs)
    elif command == 'update':
        update(argvs[0])
    else:
        print(f'Do not recognize command {command}')


def add(url):
    ingredient_storage = IngredientStorage()
    if (ingredient_storage.get_ingredients(url)):
        print('Ingredients already in our cache')
    else:
        recipe = create_recipe(url)
        if recipe:
            ingredient_storage.add_ingredients(recipe)
            ingredient_storage.save_list()
            print('Successfully added ingredients')
        else:
            print('exiting...')

def update(url):
    ingredient_storage = IngredientStorage()
    if (ingredient_storage.get_ingredients(url)):
        ingredient_storage.print_ingredients(url)
        print('\n')
        while (True):
            reply = input('Does this list look correct? (y/n)')
            if reply == 'y':
                print('exiting...')
                return
            elif reply == 'n':
                recipe = create_recipe(url)
                if recipe:
                    ingredient_storage.add_ingredients(recipe)
                    ingredient_storage.save_list()
                    print('Successfully added ingredients')
                    return
                else:
                    print('exiting...')
                    return
    else:
        print('Link not in our cache.')

def groceries(urls):
    ingredient_storage = IngredientStorage()
    grocery_list = GroceryList()

    for url in urls:
        ingredients = ingredient_storage.get_ingredients(url)
        if ingredients:
            recipe = Recipe(url, ingredients)
            grocery_list.add_recipe(recipe)
        else:
            recipe = Recipe(url)
            ingredients = recipe.find_ingredients()
            if (recipe.verify_ingredients(ingredients)):
                recipe.set_ingredients(ingredients)
                grocery_list.add_recipe(recipe)
                ingredient_storage.add_ingredients(recipe)
                ingredient_storage.save_list()
            else:
                print('Sorry, we could not find a list for this recipe. Feel free file a report on our repository.')
    
    reply = grocery_list.verify_list()
    if reply:
        grocery_list.create_txt()


# Helpers
def create_recipe(url):
    recipe = Recipe(url)
    ingredients = recipe.find_ingredients()
    if (recipe.verify_ingredients(ingredients)):
        recipe.set_ingredients(ingredients)
        return recipe
    else:
        return None
    

if __name__ == "__main__":
    # calling the main function
    main(sys.argv[1], sys.argv[2:])

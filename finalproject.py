import sys

from penrose import GroceryList, IngredientStorage, Recipe

def main(argvs):
    ingredient_storage = IngredientStorage()
    grocery_list = GroceryList()

    for url in argvs:
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
    

if __name__ == "__main__":
    # calling the main function
    main(sys.argv[1:])

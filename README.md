# penrose-sweets
### Description:

penrose-sweets is a commandline program that compiles ingredient lists from online recipes into a single grocery list. Written with Python 3.9, it takes advantage of BeautifulSoup4 to comb through a website for either a JSON file embedded in a `<script>` tag or for key words, such as `Ingredients` that clues for an ingredient list HTML object (usually in `<ul>` tags).

Most of the recipes are parsed through Python programs in the `RecipeParsers/` directory, with each file named after a food blog domain, such as `justonecookbook` or `cookieandkate`. Each file is a specific parser for that domain, since HTML code is structured differently, even if slightly, across domains. If a domain is unsupported, the parser can still parse through a general parser, which returns less accurate results than the dedicated parsers.

To speed up operations, and to allow this to be used offline (albeit in a limited capacity), links that were previous entered are cached in a JSON file. This file updates as new links are entered and the user verified that the grocery list appears correct.

### Commands:

- `add <url>`: finds the ingredients for the recipe from the specified url with a parser and save it into the cache if it does not already exist
- `update <url>`: finds the ingredients for the recipe from the specified url with a parser and updates the ingredients in our cache
- `groceries <urls...>`: finds all the ingredients for the recipes from the specified url through the cache, if they exist, or a parser and save them into a .txt file

### Example usage:

#### For getting the grocery list for one recipe
```
python finalproject.py groceries https://www.justonecookbook.com/simple-chicken-curry/
```

#### For getting the grocery list for multiple recipes
```
python finalproject.py groceries https://www.justonecookbook.com/simple-chicken-curry/ https://cookieandkate.com/healthy-banana-bread-recipe/
```
  
### Brief Architecture Summary:

- `RecipeParsers/`: This directory contains various files for parsing recipes from specific domains. It also contains a general parser if the parser for the specific domain does not exist.
- `finalproject.py`: The entry point for the program. This contains the logic for parsing the commands entered in the commandline and running the correct sequence of events based on the commands.
- `penrose.py`: Contains classes for creating objects used by the entry point file. These classes turns abstract concepts, such as recipes, into much more manageable Python objects.
- `requirements.txt`: A Python convention file that stores all the dependencies needed for the program to run. To install the dependencies through pip, run `pip install -r requirements.txt`.

### Planned Improvements (no specific order):

- add usage notes when commands are used incorrectly
- unittests
- replace JSON file caching with database caching
- turn this into a webapp with python backend
- web-based form to request new or update to parsers
- use collected user data to find out what parsers are missing

### Questions:

#### Why is this program useful?
  
This program was made for single people in mind. As a single person, especially during COVID, I often only shop for groceries once a week, meaning I need at least 5 recipes worth of ingredients. As a single person, I cannot afford to purchase too much, or the food will go bad, or too little, as I will not have enough to eat. Therefore, it helps for me to have a compiled ingredient list every week for recipes that I need to cook for that week.

#### Why a commandline program?
  
Honestly, because I have never made a commandline program before! I have created static websites, websites with a backend, and a bunch of automations. I do want to recognize, however, that this program would be most useful with a web interface! In the future, I hope I will be able to port this into a static website, so that non-programmers can also use it for their grocery shopping.

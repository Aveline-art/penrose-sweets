# penrose-sweets
### Video Demo:  <URL HERE>
### Description:

penrose-sweets is a commandline program that compiles ingredient lists from online recipes into a single grocery list. Written in Python, it takes advantage of BeautifulSoup4 to comb through a website for either a JSON file embedded in a `<script>` tag or for key words, such as `Ingredients` that clues for an ingredient list HTML object (usually in `<ul>` tags).

Most of the recipes are parsed through Python programs in the RecipeParsers directory, with each file named after a food blog domain, such as `justonecookbook` or `cookieandkate`. Each file is a specific parser for that domain, since HTML code is structured differently, even if slightly, across domains. If a domain is unsupported, the parser can still parse through a general parser, which returns less accurate results than the dedicated parsers.

To speed up operations, and to allow this to be used offline (albeit in a limited capacity), links that were previous entered are cached in a JSON file. This file updates as new links are entered and the user verified that the grocery list appears correct.

### Usage:

```
python finalproject.py <url ...>
```

### Example usage:

#### For one recipe
```
python finalproject.py https://www.justonecookbook.com/simple-chicken-curry/
```

#### For multiple recipes
```
python finalproject.py https://www.justonecookbook.com/simple-chicken-curry/ https://cookieandkate.com/healthy-banana-bread-recipe/
```

### Planned Improvements (no specific order)

- unittests
- replace JSON file caching with database caching
- turn this into a webapp with python backend
- web-based form to request new or update to parsers
- use user data to find out what parsers are missing
# Pokemon Mystery Gift Code Bot

A simple python bot to submit an email to game.co.uk for a plethora of mystery gift codes. - USE AT YOUR OWN RISK

## Event Details

https://www.pokemon.com/us/pokemon-news/get-shiny-zacian-and-shiny-zamazenta-at-gamestop/

![Promo image](https://cdn1.dotesports.com/wp-content/uploads/sites/8/2021/10/23100614/image_2021-10-23_120612.png)

![Zacian stats](https://i.imgur.com/MX31Ur1.jpg)

![Zamazenta stats](https://i.imgur.com/0C1TR2M.jpg)

## Giveaway Details

This script relies on the Game.co.uk website in the UK. It allows email submissions to receive both codes and does not do any real validation.

The codes are region free (the downloaded pokemon will automatically be received in the region set on the Switch).

Code givewaway URL: https://www.game.co.uk/webapp/wcs/stores/servlet/HubArticleView?hubId=2837253&articleId=2837253&catalogId=10201&langId=44&storeId=10151&utm_source=Twitter&utm_medium=Organic

## Running the script

### Prerequisites

This script takes advantage of the plus-code trick for gmail. It's also recommended to use a fresh gmail account to avoid risk of blacklisting and to make it easier to parse after the fact.

### Dependencies

This script depends on Beauitful Soup and some python html libs. Install using

```
python3 -m pip install requests_html bs4
```

### Executing

Download the script and run it as such:

```
python3 pokemon_code_submitter.py YourEmailGoesHere@gmail.com
```

## Special Thanks

Shout out to the tutorial here for providing much of the form parsing and submission logic: https://www.thepythoncode.com/article/extracting-and-submitting-web-page-forms-in-python

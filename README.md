# RecipeBox

A solution for meal planning.

_____________________________________

# What does it do? 

    - Add your own recipes, with ingredient lists, and instructions
    - Generate a weeks worth of meals, randomized from your recipe box. 
    - Create weeks menu, along with optional instructions for each meal
    - Create a shopping list with all the ingredients in your meal plan
    - Print or via PDF

# How to install

The only prerequesite you will need to have installed is Docker. 

clone this repository, and cd into the directory. 

from there copy this
```bash
cp .example.env .env
```
this will create a local environment for you. 

```bash
nano .env
```

replace the values with whatever you would like. They have comments to show which line. 

next `nano compose.yaml`

edit any hosting preferences you have such as port. 
by default this will be set to port 8127

```bash
docker compose up -d
```

try visiting the site in your browser http://yourhost:8127
CREATE TYPE units AS ENUM ('tsp', 'Tbsp', 'C', 'pt', 'qt', 'gal', 'g', 'kg', 'mg', 'oz', 'fl_oz');
CREATE TYPE preparations AS ENUM ('fresh', 'frozen', 'grated', 'chopped', 'sliced', 'diced', 'ground', 'minced', 'dried', 'raw', 'whole');

CREATE TABLE IF NOT EXISTS recipes(
    recipe_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    instructions TEXT
);

CREATE TABLE IF NOT EXISTS ingredients(
    ingredient_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS recipes_ingredients(
    recipe_id INT REFERENCES recipes(recipe_id),
    ingredient_id INT REFERENCES ingredients(ingredient_id),
    quantity NUMERIC NULL,
    unit units NULL,
    preparation preparations NULL
);


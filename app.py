from flask import Flask, render_template, request, url_for, redirect
import os
import psycopg2

#------------------------------------------------------------------------------------------------------
app = Flask(__name__)

def get_db_connection():

    conn = psycopg2.connect(host='localhost',
                            database='recipebowl',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/testingdb')
def testerdb():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name FROM recipes;')
    recipes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('testingdb.html', recipes=recipes)



@app.route('/newrecipe', methods=['GET', 'POST'])
def newrecipe():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':

        recipename = request.form.get('recipe_name')
        instructions = request.form.get('instructions')
         
        try:

            cur.execute(
                'INSERT INTO recipes (name, instructions) VALUES(%s, %s) RETURNING recipe_id',
                (recipename, instructions)
            )

            cur.execute(
                'SELECT id FROM recipes WHERE name = %s',
                (recipename)
            )


            #Iterating over ingredient list.

            recipe_id = cur.fetchone()[0]
            ingredients = request.form.getlist('ingredient_name')
            ing_qty = request.form.getlist('ingredient_qty')

            for ingredient, qty in zip(ingredients, ing_qty):
                cur.execute(
                    'INSERT INTO ingredients(name)' \
                    'VALUES(%s)' \
                    'ON CONFLICT (name) DO NOTHING ' \
                    'RETURNING ingredient_id;',
                    (ingredient)
                )

                ing_id = cur.fetcone()[0]
                
                cur.execute(
                    'INSERT INTO recipes_ingredients(recipe_id, ingredient_id, quantity)' \
                    'VALUES(%s,%s,%s);',
                    (recipe_id, ing_id, qty)
                )
                #------------------------------------------------------------------------------------------------------
                    #TODO:
                        #RESUME HERE, I am crafting the insert for the recipe form to be added into the database
                        #currently I have the recipe name an instructions added and then the ingredients ing id and qty
                        # should be associated now in the join table. What do I have to do next? 
                #------------------------------------------------------------------------------------------------------

            

            
        except:
            pass
    
    return render_template('add_recipes.html')



@app.route('/settings')
def settings():
    return render_template('settings.html')

from flask import Flask, render_template, request, url_for, redirect
import os
import psycopg2



#------------------------------------------------------------------------------------------------------
'''
TODO:
find which index instructions is saved in and auto populate that
find out how to go about populating the ingredients since js runs. maybe take a count of how many in each
then run my script each time and populate after??
'''
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


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'GET':
        cur.execute('SELECT name, recipe_id FROM recipes;')
        recipes = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('edit.html', recipes=recipes)
    
    elif request.method == 'POST':
        recipe_id = request.form['recipe_id']

        try:
            cur.execute('SELECT * FROM recipes WHERE recipe_id = %s;', (recipe_id,))
            recipies_table = cur.fetchall()

            
            cur.execute('SELECT * FROM recipes_ingredients ' \
                'INNER JOIN ingredients ON recipes_ingredients.ingredient_id = ingredients.ingredient_id ' \
                'WHERE recipe_id = %s;', (recipe_id,))
            
            join_table = cur.fetchall()

            print(join_table)
            print(recipies_table)
            return render_template('add_recipes.html', recipes_table=recipies_table, join_table=join_table)
        
        except Exception as e:
            conn.rollback()
            print(f"ERROR: {e}")
            return redirect(url_for('edit'))
        
        finally:
            cur.close()
            conn.close()




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

            #Iterating over ingredient list.

            recipe_id = cur.fetchone()[0]
            ingredients = request.form.getlist('ingredient_name')
            ing_qty = request.form.getlist('ingredient_qty')
            print(ingredients, ing_qty)

            for ingredient, qty in zip(ingredients, ing_qty):
                cur.execute(
                    'INSERT INTO ingredients(name)' \
                    ' VALUES(%s)' \
                    ' ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name ' \
                    ' RETURNING ingredient_id;',
                    (ingredient,)
                )

                ing_id = cur.fetchone()[0]
                
                cur.execute(
                    'INSERT INTO recipes_ingredients(recipe_id, ingredient_id, quantity)' \
                    ' VALUES(%s,%s,%s);',
                    (recipe_id, ing_id, qty)
                
                )

            conn.commit()
            return redirect(url_for('index'))
               

        except Exception as e:
            conn.rollback()
            print(f"ERROR: {e}")
            #TODO: ADD A FAILED TO SAVE ERROR PAGE TO RETURN HERE

        finally:
            cur.close()
            conn.close()


    return render_template('add_recipes.html')



@app.route('/settings')
def settings():
    return render_template('settings.html')

from flask import Flask, render_template, request, url_for, redirect, jsonify, session
import os
import psycopg2
import datetime
import json

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
            return render_template('add_recipes.html', recipes_table=recipies_table, join_table=join_table, recipe_id=recipe_id)
        
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
        hidden_id = request.form.get('recipe_id')

        if hidden_id:
            try:
                #NAME AND INSTRUCTION CHANGES
                cur.execute('UPDATE recipes SET name = %s, instructions = %s' \
                ' WHERE recipe_id = %s', (recipename, instructions, hidden_id))

                #INGREDIENT CHANGES
                ingredients = request.form.getlist('ingredient_name')
                ing_qty = request.form.getlist('ingredient_qty')

                cur.execute('DELETE FROM recipes_ingredients WHERE recipe_id = %s;',(hidden_id,))


                for ingredient, qty in zip(ingredients, ing_qty):

                    qty = qty if qty else 'N/A'

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
                        (hidden_id, ing_id, qty)                    
                    )

                conn.commit()
                return redirect(url_for('index'))
            
            except Exception as e:
                conn.rollback()
                print(e)
                return redirect('error/add')

            finally:
                cur.close()
                conn.close()

        else:
            try:

                cur.execute(
                    'INSERT INTO recipes (name, instructions) VALUES(%s, %s)' \
                    ' RETURNING recipe_id;',
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
                return redirect('/error/save')

            finally:
                cur.close()
                conn.close()


    return render_template('add_recipes.html')



@app.route('/settings')
def settings():
    return render_template('settings.html')
'''remove settings as a route, change it to a theme dropdown icon in the corner.
use js to extract the text value that the theme button uses. then take that and set it to persist on change using flask session'''

@app.route('/delete', methods=['POST'])
def delete():

    del_rqst = request.get_json()
    recipe_id = del_rqst.get('id')

    conn = get_db_connection()
    cur = conn.cursor()

    if recipe_id:


        try:
            cur.execute('DELETE FROM recipes WHERE recipe_id = %s',(recipe_id,))
            conn.commit()

            success_return = {'status': 'DELETED', 'redirect': '/edit'}
            return jsonify(success_return)


        except Exception as e:
            print(e)
            conn.rollback()
            error_return = {'status': 'FAIL', 'redirect': '/error/delete', }
            return jsonify(error_return)

        finally:
            cur.close()
            conn.close()


#TODO:
@app.route('/error/<message>')
def error(message):
    match message:
        case 'delete':
            return render_template('error_delete.html')
        case 'save':
            pass
        case 'add':
            pass

        case 'loaderror':
            pass

        case _:
            pass
            # howd you get here html


@app.route('/plan', methods = ['GET', 'POST'])
def plan():    
    conn = get_db_connection()
    cur = conn.cursor()

    
    if request.method == 'GET':

        try:
            cur.execute('SELECT name, recipe_id FROM recipes ORDER BY RANDOM() ' \
            'LIMIT 200;')
            rand_pool = cur.fetchall()
            print(rand_pool)

            if rand_pool:

                current_time = datetime.datetime.now()
                formatted_time = current_time.strftime("%I:%M%p on %m-%d-%Y")
                print(formatted_time)

                return render_template('plan.html', rand_pool = rand_pool, dt = formatted_time)
            
            #error
            else:
                return redirect(url_for('error/loaderror'))
            
        except Exception as e:
            print(e)
            return redirect('error/loaderror')

        finally:
            conn.close()
            cur.close()
    

    #-------POST ROUTE FOR PLAN--------------------------------------------------------------------------------------
    if request.method == 'POST':
        plan = json.loads(request.form.get('plan-array'))


        cur.execute('SELECT * FROM recipes WHERE recipe_id IN %s', (tuple(plan),))
        return_result = cur.fetchall()

        recipe_table = {}
        combined_ingredients = {}

        #create recipe table

        for id, name, instructions in return_result:
            recipe_table[id] = {'name':name, 'instructions':instructions, 'ingredients': [], }


        cur.execute('SELECT recipe_id, ingredients.name, recipes_ingredients.ingredient_id, quantity FROM recipes_ingredients ' \
        'INNER JOIN ingredients ON recipes_ingredients.ingredient_id = ingredients.ingredient_id ' \
        'WHERE recipe_id IN %s', (tuple(plan),))
       
        ing_return = cur.fetchall()

        for rec_id, ing_name, ing_id, qty in ing_return:

            formatted_ing = f'{ing_name} - {str(qty)}'
            recipe_table[rec_id]['ingredients'].append(formatted_ing)
            
            if ing_id in combined_ingredients:
                combined_ingredients[ing_id]['qty'] += qty
            else:
                combined_ingredients[ing_id] = {'name': ing_name, 'qty':qty}

        print(ing_return)
        return render_template('menu.html', recipe_table=recipe_table, combined_ingredients=combined_ingredients)
#------------------------------------------------------------------------------------------------------
'''
NOTES:
custom error pages for 404 or 500 with app.errorhandler(404) decorator etc

Then focus on styling.
'''
#------------------------------------------------------------------------------------------------------

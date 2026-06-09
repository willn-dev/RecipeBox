from flask import Flask, render_template, request, url_for, redirect, jsonify
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
                #TODO: Add error path

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
                #TODO: ADD A FAILED TO SAVE ERROR PAGE TO RETURN HERE

            finally:
                cur.close()
                conn.close()


    return render_template('add_recipes.html')



@app.route('/settings')
def settings():
    return render_template('settings.html')


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
            error_return = {'status': 'FAIL', 'redirect': '/error'}

        finally:
            cur.close()
            conn.close()


#TODO:
@app.route('/error')
def error():
    #temp placeholder. real custom errors with flasks built in
    #app.errorhandler(404)
    #def page_not_found()
    pass


#------------------------------------------------------------------------------------------------------
'''
Next I need to handle the error routes accordingly.
let it handle the entire sites error exceptions.

Next make page for query random mealplan based on a slider with numbers of meals.?
then figure out how to compose said page, tack on a print that has full ingredient aggregation.

Then focus on styling.


'''
#------------------------------------------------------------------------------------------------------

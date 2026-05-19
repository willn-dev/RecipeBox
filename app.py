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

        recipename = request.form.get('name')
        instructions = request.form.get('instructions')
         
        try:

            cur.execute(
                'INSERT INTO recipes (name, instructions) VALUES(%s, %s) RETURNING recipe_id',
                (recipename, instructions)
            )

            recipe_id = cur.fetchone()[0]

            #TODO: build out getting ingredients via a loop. build out form



        except:
            pass
    
    return render_template('add_recipes.html')



@app.route('/settings')
def settings():
    return render_template('settings.html')

from flask import Flask, render_template, request
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
    
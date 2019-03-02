from flask import Flask, render_template
from flask import request
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

#provide a route where requests on the web application can be addressed
@webapp.route('/hello')
#provide a view (fancy name for a function) which responds to any requests on this route
def hello():
    return "Hello World!";

@webapp.route('/browse_bsg_people')
#the name of this function is just a cosmetic thing
def browse_people():
    print("Fetching and rendering people web page")
    db_connection = connect_to_database()
    query = "SELECT fname, lname, homeworld, age from bsg_people;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render_template('people_browse.html', rows=result)

@webapp.route('/add_new_people', methods=['POST','GET'])
def add_new_people():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT planet_id, name from bsg_planets'
        result = execute_query(db_connection, query).fetchall();
        print(result)

        return render_template('people_add_new.html', planets = result)
    elif request.method == 'POST':
        print("Add new people!");
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        homeworld = request.form['homeworld']

        query = 'INSERT INTO bsg_people (fname, lname, age, homeworld) VALUES (%s,%s,%s,%s)'
        data = (fname, lname, age, homeworld)
        execute_query(db_connection, query, data)
        return ('Person added!');

@webapp.route('/')
def index():
    return "<p>Are you looking for /db-test or /hello or /browse_bsg_people or /add_new_people?</p>"

@webapp.route('/db-test')
def test_database_connection():
    print("Executing a sample query on the database using the credentials from db_credentials.py")
    db_connection = connect_to_database()
    query = "SELECT * from bsg_people;"
    result = execute_query(db_connection, query);
    return render_template('db_test.html', rows=result)

#display update form and process any updates, using the same function
@webapp.route('/update_people/<id>', methods=['POST','GET'])
def update_people(id):
    db_connection = connect_to_database()
    if request.method == 'GET':

        people_query = 'SELECT character_id, fname, lname, homeworld, age from bsg_people WHERE character_id = %s' % (id) 
        people_result = execute_query(db_connection, people_query).fetchone()

        if people_result == None:
            return "No such person found!"

        planets_query = 'SELECT planet_id, name from bsg_planets'
        planets_results = execute_query(db_connection, planets_query).fetchall();

        return render_template('people_update.html', planets = planets_results, person = people_result)
    elif request.method == 'POST':
        print("Update people!");
        character_id = request.form['character_id'] 
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        homeworld = request.form['homeworld']

        print(request.form);

        query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE character_id = %s"
        data = (fname, lname, age, homeworld, character_id)
        result = execute_query(db_connection, query, data)
        return (str(result.rowcount) + " row(s) updated");

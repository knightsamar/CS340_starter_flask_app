from flask import Flask, render_template, session, request, redirect, url_for, escape
from db_connector.db_connector import connect_to_database, execute_query
from itsdangerous import URLSafeSerializer
#create the web application
webapp = Flask(__name__)
webapp.secret_key = 'cs340_2019'
auth_s = URLSafeSerializer("some_password", "some_salt")

@webapp.route('/')
def index():
    return redirect(url_for('login')) 

@webapp.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        db_connection = connect_to_database()
        query = "SELECT email from Final_Users;"
        result = execute_query(db_connection, query).fetchall()
        result_emails = [row[0] for row in result]
        return render_template('login.html', emails=result_emails)
    elif request.method == 'POST':
        session['email'] = request.form['email']
        return redirect(url_for('home'))


@webapp.route('/home')
def home():
    if 'email' in session:
        email = session['email']
        db_connection = connect_to_database()
        query = 'SELECT type FROM Final_Users WHERE email = \'%s\'' % (email)
        result = execute_query(db_connection, query).fetchone()    
        page = 'Hello ' + result[0]
        if result == "D":
            page = page + "Driver"
        elif result == "F":
            page = page + "Manager"
        elif result == "C":
            page = page + "Customer"
        page = page + email + "<br>" + \
        "<a href = '/logout'>Click here to log out</a>"
        return
    return "You are not logged in<br>" + \
        "<a href = '/login'>Click here to log in</a>"

#@webapp.route('/add_item')
#def add_item():

#@webapp.route('/search')
#def search():

#@webapp.route('/change_address')
#def change_address():

@webapp.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


# @webapp.route('/browse_bsg_people')
# #the name of this function is just a cosmetic thing
# def browse_people():
#     print("Fetching and rendering people web page")
#     db_connection = connect_to_database()
#     query = "SELECT fname, lname, homeworld, age, character_id from bsg_people;"
#     result = execute_query(db_connection, query).fetchall();
#     print(result)
#     return render_template('people_browse.html', rows=result)

# @webapp.route('/add_new_people', methods=['POST','GET'])
# def add_new_people():
#     db_connection = connect_to_database()
#     if request.method == 'GET':
#         query = 'SELECT planet_id, name from bsg_planets'
#         result = execute_query(db_connection, query).fetchall();
#         print(result)

#         return render_template('people_add_new.html', planets = result)
#     elif request.method == 'POST':
#         print("Add new people!");
#         fname = request.form['fname']
#         lname = request.form['lname']
#         age = request.form['age']
#         homeworld = request.form['homeworld']

#         query = 'INSERT INTO bsg_people (fname, lname, age, homeworld) VALUES (%s,%s,%s,%s)'
#         data = (fname, lname, age, homeworld)
#         execute_query(db_connection, query, data)
#         return ('Person added!');

# @webapp.route('/db-test')
# #provide a route where requests on the web application can be addressed
# def test_database_connection():
#     print("Executing a sample query on the database using the credentials from db_credentials.py")
#     db_connection = connect_to_database()
#     query = "SELECT * from bsg_people;"
#     result = execute_query(db_connection, query);
#     return render_template('db_test.html', rows=result)

# #display update form and process any updates, using the same function
# @webapp.route('/update_people/<int:id>', methods=['POST','GET'])
# def update_people(id):
#     db_connection = connect_to_database()
#     #display existing data
#     if request.method == 'GET':
#         people_query = 'SELECT character_id, fname, lname, homeworld, age from bsg_people WHERE character_id = %s' % (id)
#         people_result = execute_query(db_connection, people_query).fetchone()

#         if people_result == None:
#             return "No such person found!"

#         planets_query = 'SELECT planet_id, name from bsg_planets'
#         planets_results = execute_query(db_connection, planets_query).fetchall();

#         return render_template('people_update.html', planets = planets_results, person = people_result)
#     elif request.method == 'POST':
#         print("Update people!");
#         character_id = request.form['character_id']
#         fname = request.form['fname']
#         lname = request.form['lname']
#         age = request.form['age']
#         homeworld = request.form['homeworld']

#         print(request.form);

#         query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE character_id = %s"
#         data = (fname, lname, age, homeworld, character_id)
#         result = execute_query(db_connection, query, data)
#         print(str(result.rowcount) + " row(s) updated");

#         return redirect('/browse_bsg_people')

# @webapp.route('/delete_people/<int:id>')
# def delete_people(id):
#     '''deletes a person with the given id'''
#     db_connection = connect_to_database()
#     query = "DELETE FROM bsg_people WHERE character_id = %s"
#     data = (id,)

#     result = execute_query(db_connection, query, data)
#     return (str(result.rowcount) + "row deleted")

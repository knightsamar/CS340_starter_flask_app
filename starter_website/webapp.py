from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

#provide a route where requests on the web application can be addressed
@webapp.route('/hello')
#provide a view (fancy name for a function) which responds to any requests on this route
def hello():
    return "Hello"

@webapp.route('/browse_books')
#the name of this function is just a cosmetic thing
def browse_people():
    print("Fetching and rendering Books web page")
    db_connection = connect_to_database()
    query = "SELECT book_title, book_author, book_genre, book_publisher FROM Books;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('books_browse.html', rows=result)




@webapp.route('/browse_loans')
def browse_loans():
    print("Fetching and redering Loans web page")
    db_connection = connect_to_database()
    query = "SELECT Loans.loan_date, Books.book_title, Loans.loan_is_active, Patrons.patron_name, Librarians.librarian_name FROM Loans JOIN Books ON Loans.book_id = Books.book_id JOIN Patrons ON Loans.patron_id=Patrons.patron_id JOIN Librarians ON Loans.librarian_id=Librarians.librarian_id;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('loans_browse.html', rows=result)

@webapp.route('/browse_librarians')
def browse_librarians():
    print("Fetching and rendering Librarians web page")
    db_connection = connect_to_database()
    query = "SELECT librarian_name FROM Librarians;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('librarians_browse.html', rows=result)

@webapp.route('/add_new_book', methods=['POST','GET'])
def add_new_book():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT librarian_id, librarian_name from Librarians'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('books_add_new.html', librarian = result)
    elif request.method == 'POST':
        print("Add new books!")
        title = request.form['book_title']
        genre = request.form['book_genre']
        publisher = request.form['book_publisher']
        author = request.form['book_author']

        query = 'INSERT INTO Books (book_title,book_author, book_genre, book_publisher) VALUES (%s,%s,%s,%s)'
        data = (title,author, genre, publisher)
        execute_query(db_connection, query, data)
        return redirect('/browse_books')

@webapp.route('/add_new_librarian', methods=['POST','GET'])
def add_new_librarian():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT librarian_id, librarian_name from Librarians'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('librarians_add_new.html', librarian = result)
    elif request.method == 'POST':
        print("Add new librarian!")
        Lname = request.form['librarian_name']
        query = 'INSERT INTO Librarians (librarian_name) VALUES (%s)'
        data = (Lname)
        execute_query(db_connection, query, data)
        return redirect('/browse_librarians')

@webapp.route('/browse_patrons')
def browse_patrons():
    print("Fetching and rendering Books web page")
    db_connection = connect_to_database()
    query = "SELECT patron_name,patron_address from Patrons;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('patrons_browse.html', rows=result)


@webapp.route('/add_new_patron', methods=['POST','GET'])
def add_new_patron():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('patrons_add_new.html')
    elif request.method == 'POST':
        print("Add new Patrons!")
        name = request.form['patron_name']
        address = request.form['patron_address']
    
        query = 'INSERT INTO Patrons (patron_name, patron_address) VALUES (%s,%s)'
        data = (name, address)
        execute_query(db_connection, query, data)
        return redirect('/browse_patrons')

@webapp.route('/')
def index():
    return "<p>Are you looking for /db_test or /hello or <a href='/browse_bsg_people'>/browse_bsg_people</a> or /add_new_people or /update_people/id or /delete_people/id </p>"

@webapp.route('/home')
def home():
    db_connection = connect_to_database()
    query = "DROP TABLE IF EXISTS diagnostic;"
    execute_query(db_connection, query)
    query = "CREATE TABLE diagnostic(id INT PRIMARY KEY, text VARCHAR(255) NOT NULL);"
    execute_query(db_connection, query)
    query = "INSERT INTO diagnostic (text) VALUES ('MySQL is working');"
    execute_query(db_connection, query)
    query = "SELECT * from diagnostic;"
    result = execute_query(db_connection, query)
    for r in result:
        print(f"{r[0]}, {r[1]}")
    return render_template('home.html', result = result)

@webapp.route('/db_test')
def test_database_connection():
    print("Executing a sample query on the database using the credentials from db_credentials.py")
    db_connection = connect_to_database()
    query = "SELECT * from bsg_people;"
    result = execute_query(db_connection, query)
    return render_template('db_test.html', rows=result)

#display update form and process any updates, using the same function
@webapp.route('/update_people/<int:id>', methods=['POST','GET'])
def update_people(id):
    print('In the function')
    db_connection = connect_to_database()
    #display existing data
    if request.method == 'GET':
        print('The GET request')
        people_query = 'SELECT id, fname, lname, homeworld, age from bsg_people WHERE id = %s'  % (id)
        people_result = execute_query(db_connection, people_query).fetchone()

        if people_result == None:
            return "No such person found!"

        planets_query = 'SELECT id, name from bsg_planets'
        planets_results = execute_query(db_connection, planets_query).fetchall()

        print('Returning')
        return render_template('people_update.html', planets = planets_results, person = people_result)
    elif request.method == 'POST':
        print('The POST request')
        character_id = request.form['character_id']
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        homeworld = request.form['homeworld']

        query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE id = %s"
        data = (fname, lname, age, homeworld, character_id)
        result = execute_query(db_connection, query, data)
        print(str(result.rowcount) + " row(s) updated")

        return redirect('/browse_bsg_people')

@webapp.route('/delete_people/<int:id>')
def delete_people(id):
    '''deletes a person with the given id'''
    db_connection = connect_to_database()
    query = "DELETE FROM bsg_people WHERE id = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)
    return (str(result.rowcount) + "row deleted")




    
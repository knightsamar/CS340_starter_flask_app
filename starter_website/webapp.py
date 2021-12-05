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
def browse_books():
    print("Fetching and rendering Books web page")
    db_connection = connect_to_database()
    query = "SELECT book_title, book_author, book_genre, book_publisher, book_id FROM Books;"
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
    query = "SELECT librarian_name, librarian_id FROM Librarians;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('librarians_browse.html', rows=result)


@webapp.route('/add_new_book', methods=['POST','GET'])
def add_new_book():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('books_add_new.html')
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
        return render_template('librarians_add_new.html')
    elif request.method == 'POST':
        print("Add new librarian!")
        librarian_name = request.form['librarian_name']

        query = 'INSERT INTO Librarians VALUES (%s)'
        data = (librarian_name)
        execute_query(db_connection, query, data)
        return redirect('/browse_librarians')

@webapp.route('/browse_patrons')
def browse_patrons():
    print("Fetching and rendering Books web page")
    db_connection = connect_to_database()
    query = "SELECT patron_name,patron_address, patron_id from Patrons;"
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

@webapp.route('/add_new_loan', methods=['POST','GET'])
def add_new_loan():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT book_id, book_title FROM Books'
        result = execute_query(db_connection, query).fetchall()
        print(result)
        query = 'SELECT patron_id, patron_name FROM Patrons'
        result2 = execute_query(db_connection, query).fetchall()
        print(result2)
        query = 'SELECT librarian_id, librarian_name FROM Librarians'
        result3 = execute_query(db_connection, query).fetchall()
        return render_template('loans_add_new.html', book_title=result, patron_name = result2, librarian_name = result3)
    elif request.method == 'POST':
        print("Add new Loans!")
        date = request.form['loan_date']
        title = request.form['book_title']
        returned = request.form['loan_is_active']
        patron = request.form['patron_name']
        librarian = request.form['librarian_name']
    
        query = 'INSERT INTO Loans (loan_date, book_id, loan_is_active, patron_id, librarian_id) VALUES(%s, (SELECT book_id WHERE book_title = %s), %s, (SELECT patron_id WHERE patron_name = %s), (SELECT librairan_id WHERE librarian_name = %s))'
        data = (date, title, returned, patron, librarian)
        execute_query(db_connection, query, data)
        return redirect('/browse_loans')

@webapp.route('/update_patrons/<int:id>', methods=['POST','GET'])
def update_patrons(id):
    print('In the function')
    db_connection = connect_to_database()
    #display existing data
    if request.method == 'GET':
        print('The GET request')
        patron_query = 'SELECT patron_name, patron_address, patron_id from Patrons WHERE patron_id = %s' % (id)
        patron_result = execute_query(db_connection, patron_query).fetchone()

        if patron_result == None:
            return "No such book found!"

        return render_template('patrons_update.html', patron = patron_result)
    elif request.method == 'POST':
        print('The POST request')
        name = request.form['name']
        address = request.form['address']
        patron_id = request.form['patron_id']

        query = "UPDATE Patrons SET patron_name = %s, patron_address = %s WHERE patron_id = %s"
        data = ( name, address,patron_id)
        result = execute_query(db_connection, query, data)
        print(str(result.rowcount) + " row(s) updated")

        return redirect('/browse_patrons')

@webapp.route('/delete_patrons/<int:id>')
def delete_patron(id):
    '''deletes a patron with the given id'''
    db_connection = connect_to_database()
    query = "DELETE FROM Patrons WHERE patron_id = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)
    # return (str(result.rowcount) + "row deleted")
    return redirect('/browse_patrons')

@webapp.route('/update_books/<int:id>', methods=['POST','GET'])
def update_books(id):
    print('In the function')
    db_connection = connect_to_database()
    #display existing data
    if request.method == 'GET':
        print('The GET request')
        book_query = 'SELECT book_title, book_author, book_genre, book_publisher,book_id from Books WHERE book_id = %s' % (id)
        book_result = execute_query(db_connection, book_query).fetchone()

        if book_result == None:
            return "No such book found!"

        return render_template('books_update.html', book = book_result)
    elif request.method == 'POST':
        print('The POST request')
        book_id = request.form['book_id']
        title = request.form['title']
        genre = request.form['genre']
        publisher = request.form['publisher']
        author = request.form['author']

        query = "UPDATE Books SET book_title = %s, book_genre = %s, book_publisher = %s, book_author = %s WHERE book_id = %s"
        data = ( title, genre, publisher, author,book_id)
        result = execute_query(db_connection, query, data)
        print(str(result.rowcount) + " row(s) updated")

        return redirect('/browse_books')

@webapp.route('/delete_books/<int:id>')
def delete_book(id):
    '''deletes a person with the given id'''
    db_connection = connect_to_database()
    query = "DELETE FROM Books WHERE book_id = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)
    # return (str(result.rowcount) + "row deleted")
    return redirect('/browse_books')

@webapp.route('/update_librarians/<int:id>', methods=['POST','GET'])
def update_librarians(id):
    print('In the function')
    db_connection = connect_to_database()
    #display existing data
    if request.method == 'GET':
        print('The GET request')
        librarian_query = 'SELECT librarian_name, librarian_id from Librarians WHERE librarian_id = %s' % (id)
        librarian_result = execute_query(db_connection, librarian_query).fetchone()

        if librarian_result == None:
            return "No such librarian found!"

        return render_template('librarians_update.html', librarian = librarian_result)
    elif request.method == 'POST':
        print('The POST request')
        librarian_id = request.form['librarian_id']
        librarian_name = request.form['librarian_name']

        query = "UPDATE Librarians SET librarian_name = %s WHERE librarian_id = %s"
        data = ( librarian_name, librarian_id)
        result = execute_query(db_connection, query, data)
        print(str(result.rowcount) + " row(s) updated")

        return redirect('/browse_librarians')

@webapp.route('/delete_librarians/<int:id>')
def delete_librarian(id):
    '''deletes a person with the given id'''
    db_connection = connect_to_database()
    query = "DELETE FROM Librarians WHERE librarian_id = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)
    # return (str(result.rowcount) + "row deleted")
    return redirect('/browse_librarians')

@webapp.route('/update_loans/<int:id>', methods=['POST','GET'])
def update_loans(id):
    print('In the function')
    db_connection = connect_to_database()
    #display existing data
    if request.method == 'GET':
        print('The GET request')
        loan_query = 'SELECT Loans.loan_date, Books.book_title, Loans.loan_is_active, Patrons.patron_name, Librarians.librarian_name FROM Loans JOIN Books ON Loans.book_id = Books.book_id JOIN Patrons ON Loans.patron_id=Patrons.patron_id JOIN Librarians ON Loans.librarian_id=Librarians.librarian_id WHERE book_id = %s' % (id)
        loan_result = execute_query(db_connection, loan_query).fetchone()

        if loan_result == None:
            return "No such book found!"

        return render_template('loans_update.html', loans = loan_result)
    elif request.method == 'POST':
        print('The POST request')
        loan_is_active = request.form['loan_is_active']
        book_id = request.form['book_id']

        query = "UPDATE Loans SET loan_is_active = %s, WHERE book_id = %s"
        data = (loan_is_active, book_id)
        result = execute_query(db_connection, query, data)
        print(str(result.rowcount) + " row(s) updated")

        return redirect('/browse_loans')

@webapp.route('/')
def index():
    return render_template('index.html')

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

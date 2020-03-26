from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

#provide a route where requests on the web application can be addressed
@webapp.route('/hello')
#provide a view (fancy name for a function) which responds to any requests on this route
def hello():
    return "Hello World!";

@webapp.route('/')
def index():
    print("Running queries for project step 0")
    db_connection = connect_to_database()
    drop_table = "DROP TABLE IF EXISTS diagnostic;"
    create_table = "CREATE TABLE diagnostic(id INT PRIMARY KEY AUTO_INCREMENT, text VARCHAR(255) NOT NULL);"
    insert_row = "INSERT INTO diagnostic (text) VALUES ('MySQL is Working!')"
    query = "SELECT * FROM diagnostic;"
    execute_query(db_connection, drop_table);
    execute_query(db_connection, create_table);
    execute_query(db_connection, insert_row);
    values = execute_query.fetchall(db_connection, query);
    return render_template('home.html', results=values)

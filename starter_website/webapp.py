from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

#provide a route where requests on the web application can be addressed
# @webapp.route('/hello')
# #provide a view (fancy name for a function) which responds to any requests on this route
# def hello():
#     return "Hello World!"

# # @webapp.route('/')

# # def home():
# #     return 'home page'
# @webapp.route('/browse_bsg_people')
# #the name of this function is just a cosmetic thing
# def browse_people():
#     print("Fetching and rendering people web page")
#     db_connection = connect_to_database()
#     query = "SELECT fname, lname, homeworld, age, id from bsg_people;"
#     result = execute_query(db_connection, query).fetchall()
#     print(result)
#     return render_template('people_browse.html', rows=result)

# @webapp.route('/add_new_people', methods=['POST','GET'])
# def add_new_people():
#     db_connection = connect_to_database()
#     if request.method == 'GET':
#         query = 'SELECT id, name from bsg_planets'
#         result = execute_query(db_connection, query).fetchall()
#         print(result)

#         return render_template('people_add_new.html', planets = result)
#     elif request.method == 'POST':
#         print("Add new people!")
#         fname = request.form['fname']
#         lname = request.form['lname']
#         age = request.form['age']
#         homeworld = request.form['homeworld']

#         query = 'INSERT INTO bsg_people (fname, lname, age, homeworld) VALUES (%s,%s,%s,%s)'
#         data = (fname, lname, age, homeworld)
#         execute_query(db_connection, query, data)
#         return ('Person added!')
@webapp.route('/teachers')
def teachers_view():
    # return "<p>Are you looking for /db_test or /hello or <a href='/browse_bsg_people'>/browse_bsg_people</a> or /add_new_people or /update_people/id or /delete_people/id </p>"
    db_connection = connect_to_database()
    query = "SELECT * from Teachers;"
    result = execute_query(db_connection, query).fetchall()
    query2 = "SELECT * from TeacherClassList"
    result2 = execute_query(db_connection, query2).fetchall()
    query3 = "SELECT * from Classes"
    result3 = execute_query(db_connection, query3).fetchall()
    result = result, result2, result3
    print(result)
    return render_template('teachers.html', rows=result)
@webapp.route('/update_teacher/<int:id>', methods=['POST','GET'])
def update_teacher(id):
    db_connection = connect_to_database()

    if request.method == 'GET':
        query = 'SELECT * from Teachers WHERE teacher_id = %s;' % (id)
        result = execute_query(db_connection, query).fetchall()
        print(result[0][0], 'this is result')
        return render_template('update_teacher.html', teach=result)
    elif request.method == 'POST':
        # print(request.form)
        first_name = request.form['first_name']
        last_name = request.form['lname']
       
        query = "UPDATE Teachers SET first_name = %s , last_name = %s WHERE teacher_id = %s " 
        data = (first_name, last_name, id)
        execute_query(db_connection, query, data)

        return redirect('/teachers')
@webapp.route('/add_teacher', methods=['POST','GET'])
def add_teacher():
    db_connection = connect_to_database()

    if request.method == 'GET':
        query = 'SELECT id, name from bsg_planets'
        result = execute_query(db_connection, query).fetchall()
        print(result)
    elif request.method == 'POST':
        # print(request.form)
        first_name = request.form['first_name']
        last_name = request.form['lname']
        query = "INSERT INTO Teachers (first_name, last_name) VALUES (%s,%s);"
        data = (first_name, last_name)
        execute_query(db_connection, query, data)
       
        return redirect('/teachers')
@webapp.route('/delete_teacher/<int:id>')
def delete_teacher(id):
    '''deletes a teacher with the given id'''
    db_connection = connect_to_database()
    query1 = "DELETE from TeacherClassList where teacher_class_list_id = %s;"
    data = (id,)
    execute_query(db_connection, query1, data)
    query = "DELETE from Teachers where teacher_id = %s;"
    data = (id,)

    result = execute_query(db_connection, query, data)
    return redirect('/teachers')
# Grades
@webapp.route('/add_grade', methods=['POST','GET'])
def add_grade():
    db_connection = connect_to_database()

    if request.method == 'GET':
        query = 'SELECT id, name from bsg_planets'
        result = execute_query(db_connection, query).fetchall()
        print(result)
    elif request.method == 'POST':
        print(request.form)
        # name = request.form['title']
        # teacher_id = request.form['teacher']
        # student_list_id = 0
        # query = "INSERT INTO Classes (name, teacher_id, student_list_id) VALUES (%s,%s,%s);"
        # data = (name, teacher_id, student_list_id)
        # execute_query(db_connection, query, data)
        # query2 = "SELECT Last_INSERT_ID();"
        # result = execute_query(db_connection, query2).fetchall()
        # # create_class_result = execute_query(db_connection, query2).fetchall()
        # print(result[0])
        return redirect('/grades')
@webapp.route('/delete_grade/<int:id>')
def delete_grade(id):
    db_connection = connect_to_database()
    query = "DELETE from Grades where grade_id = %s;"
    data = (id,)

    result = execute_query(db_connection, query, data)
    return redirect('/grades')
@webapp.route('/grades')
def grades_view():
    # return "<p>Are you looking for /db_test or /hello or <a href='/browse_bsg_people'>/browse_bsg_people</a> or /add_new_people or /update_people/id or /delete_people/id </p>"
    db_connection = connect_to_database()
    query = "SELECT * from Grades;"
    result = execute_query(db_connection, query).fetchall()
    query2 = "SELECT * from Students;"
    result2 = execute_query(db_connection, query2).fetchall()
    grades_res = (result, result2)
    print(grades_res)
    # print(result, teach_result)
  
    return render_template('grades.html', grade_result = grades_res)

@webapp.route('/students')
def students_view():
    # return "<p>Are you looking for /db_test or /hello or <a href='/browse_bsg_people'>/browse_bsg_people</a> or /add_new_people or /update_people/id or /delete_people/id </p>"
    db_connection = connect_to_database()
    query = "SELECT * from Students;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
 
    return render_template('students.html', rows=result)
@webapp.route('/delete_class/<int:id>')
def delete_class(id):
    '''deletes a class with the given id'''
    db_connection = connect_to_database()
    query1 = "DELETE from TeacherClassList where class_id = %s;"
    data = (id,)
    result1 = execute_query(db_connection, query1, data)
    query = "DELETE from Classes where class_id = %s;"
    data = (id,)

    result = execute_query(db_connection, query, data)
    return redirect('/classes')
@webapp.route('/add_class', methods=['POST','GET'])
def add_class():
    db_connection = connect_to_database()

    if request.method == 'GET':
        query = 'SELECT id, name from bsg_planets'
        result = execute_query(db_connection, query).fetchall()
        print(result)
    elif request.method == 'POST':
        print(request.form)
        name = request.form['title']
        teacher_id = request.form['teacher']
    
        query = "INSERT INTO Classes (name) VALUES (%s);"
        data = (name,)
        execute_query(db_connection, query, data)
        query2 = "SELECT LAST_INSERT_ID() LIMIT 1;"
        class_id = execute_query(db_connection, query2).fetchall()
        class_id = class_id[0][0]
        teacher_class_list_id = teacher_id
        # print(class_id)
        query3 = "INSERT INTO TeacherClassList (teacher_class_list_id, class_id) VALUES (%s, %s);"
        data = (teacher_class_list_id, class_id)
        execute_query(db_connection, query3, data)
        # create_class_result = execute_query(db_connection, query2).fetchall()
        
        return redirect('/classes')

@webapp.route('/classes')
def classes_view():
    # return "<p>Are you looking for /db_test or /hello or <a href='/browse_bsg_people'>/browse_bsg_people</a> or /add_new_people or /update_people/id or /delete_people/id </p>"
    db_connection = connect_to_database()
    query = "SELECT * from Classes;"
    result = execute_query(db_connection, query).fetchall()
    query2 = "SELECT * from Teachers;"
    teach_result = execute_query(db_connection, query2).fetchall()
    # print(len(result))
    final_results = []
    for i in range(0, len(result)):
        # print(result[i])
    #     print(class)
        # print(result[i][0])
        query3 = "SELECT * from TeacherClassList where class_id = %s;"
        data = (result[i][0],)
        result2 = execute_query(db_connection, query3, data).fetchall()
        query4 = "SELECT * from Teachers where teacher_id = %s;"
        # print(len(result2))
        print(result2)
        # print(result2[0][0])
        data = (result2[0][0],)
        result3 = execute_query(db_connection, query4, data).fetchall()
        # result3[0][2]
        # print(result3[0][2])
        join_result = (result[i][0], result[i][1], result3[0][0], result3[0][1], result3[0][2])
        final_results.append(join_result)
    final_results = (final_results, teach_result)
    print(final_results[1])
    # print(final_results)
    # teach_class = (result, teach_result)
    # print(result, teach_result)
    return render_template('classes.html', result = final_results)
@webapp.route('/')
def index():
    # return "<p>Are you looking for /db_test or /hello or <a href='/browse_bsg_people'>/browse_bsg_people</a> or /add_new_people or /update_people/id or /delete_people/id </p>"
    return render_template('index.html')


# @webapp.route('/home')
# def home():
#     db_connection = connect_to_database()
#     query = "DROP TABLE IF EXISTS diagnostic;"
#     execute_query(db_connection, query)
#     query = "CREATE TABLE diagnostic(id INT PRIMARY KEY, text VARCHAR(255) NOT NULL);"
#     execute_query(db_connection, query)
#     query = "INSERT INTO diagnostic (text) VALUES ('MySQL is working');"
#     execute_query(db_connection, query)
#     query = "SELECT * from diagnostic;"
#     result = execute_query(db_connection, query)
#     for r in result:
#         print(f"{r[0]}, {r[1]}")
#     return render_template('home.html', result = result)

# @webapp.route('/db_test')
# def test_database_connection():
#     print("Executing a sample query on the database using the credentials from db_credentials.py")
#     db_connection = connect_to_database()
#     query = "SELECT * from bsg_people;"
#     result = execute_query(db_connection, query)
#     return render_template('db_test.html', rows=result)

# #display update form and process any updates, using the same function
# @webapp.route('/update_people/<int:id>', methods=['POST','GET'])
# def update_people(id):
#     print('In the function')
#     db_connection = connect_to_database()
#     #display existing data
#     if request.method == 'GET':
#         print('The GET request')
#         people_query = 'SELECT id, fname, lname, homeworld, age from bsg_people WHERE id = %s'  % (id)
#         people_result = execute_query(db_connection, people_query).fetchone()

#         if people_result == None:
#             return "No such person found!"

#         planets_query = 'SELECT id, name from bsg_planets'
#         planets_results = execute_query(db_connection, planets_query).fetchall()

#         print('Returning')
#         return render_template('people_update.html', planets = planets_results, person = people_result)
#     elif request.method == 'POST':
#         print('The POST request')
#         character_id = request.form['character_id']
#         fname = request.form['fname']
#         lname = request.form['lname']
#         age = request.form['age']
#         homeworld = request.form['homeworld']

#         query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE id = %s"
#         data = (fname, lname, age, homeworld, character_id)
#         result = execute_query(db_connection, query, data)
#         print(str(result.rowcount) + " row(s) updated")

#         return redirect('/browse_bsg_people')

# @webapp.route('/delete_people/<int:id>')
# def delete_people(id):
#     '''deletes a person with the given id'''
#     db_connection = connect_to_database()
#     query = "DELETE FROM bsg_people WHERE id = %s"
#     data = (id,)

#     result = execute_query(db_connection, query, data)
#     return (str(result.rowcount) + "row deleted")

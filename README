
About
----
This repository has 2 webapps: 

1. A sample database webapp showing how to run a SELECT query on the database and print the results on the webpage
2. A (almost) full-fledged webapp demonstrating Create, Read, Update and Delete functionalities.

Both use the database dump bsg_sample.sql for demonstration

Setup
----

```
virtualenv venv -p $(which python3) 

source ./venv/bin/activate

pip3 install --upgrade pip3

pip install -r requirements.txt
```
Rename the `db_credentials.py.sample` to `db_credentials.py` and put your actual database credentials inside it.


Using the sample database connectivty webapp
--------------------------------------------

```
source ./venv/bin/activate
export FLASK_APP=db_connection_sample.py
flask run -h 0.0.0.0 -p 5000 --reload
```

The webapp will use the database credentials from db_credentials.py to connect to a database.

Now if you open `http://your.server.name/db-test` here, you should see a webpage with results from the database
```


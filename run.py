#this file is used to run your flask-based-database-interacting-website persistently!

#change this line to run the app that you want to run
#from db_connector.sample import app
#for example, the above line tells to run the sample db connection app in db_connector/ directory
from starter_website.webapp import webapp
#from step0.webapp import webapp

#then from the commandline run:
#./venv/bin/activate
#gunicorn run:app -b 0.0.0.0:SOME_NUMBER_BETWEEN_1025_and_65535
#eg. gunicorn run:app -b 0.0.0.0:8842

#change this line to run the app that you want to run

#for example, to run the sample db connection app in db_connector/ directory
from db_connector.sample import app

#then from the commandline run:
#./venv/bin/activate
#gunicorn run:app -b 0.0.0.0:SOME_NUMBER_BETWEEN_1025_and_65535 
#eg. gunicorn run:app -b 0.0.0.0:8842


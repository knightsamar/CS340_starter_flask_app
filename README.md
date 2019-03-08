# Using Python Flask on the Engineering Servers


## Intro

Flask<sup>[1]</sup> is a Python micro framework for building web applications which began as a simple wrapper from Werkzeug and Jinjia but has become one of the most popular Python web application frameworks now<sup>[2]</sup>. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. This guide will walk you through setting it up on the OSU Engineering server and connecting it to an Engineering provided SQL database.


## Overview

In general things will be very similar to how you deploy a NodeJS app. There are a few important things to note in terms of Python and Flask on the Engineering server. 

The first is that your engineering account is __**not**__ preconfigured with the required demo applications so you will need to get those yourself. 

The next is that _the only way you will be able to see your site is if you are on the OSU VPN or you are physically connected to the on campus internet_. If you are not connected to the VPN you will not be able to access your site. You can find information on connecting to the VPN [here](http://oregonstate.edu/helpdocs/osu-applications/offered-apps/virtual-private-network-vpn). 

The other piece is that your MySQL database that you will be using will need to be made for you. This is usually done as part of a class and your instructor will provide you with the appropriate addresses and credentials to access it.


## Gitting Files

You should make a new directory in your OSU engineering space, e.g. `mkdir ~/cs340/`. Then from within that directory run the command:

```bash
git clone https://github.com/knightsamar/CS340_starter_flask_app ./
```

Note that this repository has 2 webapps:

1. A sample database webapp showing how to run a SELECT query on the database and print the results on the webpage

2. A (almost) full-fledged webapp demonstrating Create, Read, Update and Delete functionalities.

Both use the database dump bsg_sample.sql for demonstration.

This command will clone all the class files from the class Git repository into that directory you created (~/cs340/). 


## Making Required Changes

First you should go to the `CS340_starter_flask_app` repository folder and setup a new Python virtual environment for Flask, then install related dependencies. Run the commands within previous directory:

```bash
cd CS340_starter_flask_app
bash
virtualenv venv -p $(which python3) 
source ./venv/bin/activate
pip3 install --upgrade pip3
pip install -r requirements.txt
```

This will create an virtual environment named `venv` and install the required Python packages to run the starter code, which are listed inside the file `requirements.txt`.

Next you will need to tweak some files to work with the engineering setup. Because you would have your own database, a few template values will  need to be replaced to point to your database.

In particular, inside the current directory `CS340_starter_flask_app` there is a file called `db_credentials.py.sample`. Rename this file to `db_credentials.py` file and put your actual database credentials inside it. 

You need to edit the file. It should look like the following code with the curly brackets and their contents replaced with the appropriate content:

```python
host = 'classmysql.engr.oregonstate.edu'
user = 'cs340_{your_ONID_username}'
passwd = '{last-4-digits-of-your-OSU-ID-number}'
db = 'cs340_{your_ONID_username}'
```

These are the default settings for all students who were enrolled when the term started.  

An **example** would look like this:

```python
host = 'classmysql.engr.oregonstate.edu'
user = 'cs340_hedaoos'
passwd = '1234'
db = 'cs340_hedaoos'
```

With that file renamed to `db_credentials.py` and the proper credentials added, we are almost ready to go.

## Running the Flask Application!

Make sure you are still inside the `CS340_starter_flask_app` directory. 

```bash
source ./venv/bin/activate
export FLASK_APP=run.py
python -m flask run -h 0.0.0.0 -p 8042 --reload
```

**Replace 8042 with a random port number**

Now, your website should be accessible at http://flipN.engr.oregonstate.edu:YOUR_PORT_NUMBER

To verify that your server is running, a Hello World page will be visible at `/hello`, while the a READ implementation page can be found at `/browse_bsg_people`. 

So you would go to http://flipN.engr.oregonstate.edu:YOUR_PORT_NUMBER/hello or similar.

flipN means either of flip1, flip2 or flip3.
YOUR_PORT_NUMBER is the number that you used in the command above to run the app.

Because this is running on a shared machine everyone cannot use port 8042. Everyone will need to use a unique port, otherwise you will get an error that the port is in use.

So, we specify the Python file for database connection and also set a port number. You could view the database page of nine entries being served by visiting http://access.engr.oregonstate.edu:5678/browse_bsg_people while you are VPNed into the OSU network.

This is how you run the app using the Flask Development server. But to submit your URL for assignments, you need to use the method below!

## Running the Flask Application Persistently!!
Finally, is the topic of persistence. How to ensure that your app keeps running even after you disconnect from the flip servers/VPN ?

To do that, we use [gunicorn](https://gunicorn.org/) as follows:

```bash
gunicorn run:webapp -b 0.0.0.0:YOUR_PORT_NUMBER -D 
```

The -D runs the gunicorn process in background.

There are a lot of other tools you can use, such as [run with a production server using waitress](http://flask.pocoo.org/docs/1.0/tutorial/deploy/#run-with-a-production-server
) or [deploy in a standalone WSGI Containers using uWSGI](http://flask.pocoo.org/docs/1.0/deploying/wsgi-standalone/), etc.  


### How to kill an old running gunicorn process ? 

You would have to find your process on the right flip server by running

```bash
ps ufx | grep gunicorn
```
And then kill the process by using it's PID (see the second column in the above output). Note that the grep process also shows up in the output. You want to kill the other process which has a child process. That's most probably the second process in the above output.

## The Many Flips

And as a closing note, if you log into access.engr.oregonstate.edu you will randomly be put on flip1, flip2 or flip3. You can see which flip you are using the command `hostname` then you can switch flips by using the command `ssh flipX` where X is 1, 2 or 3. You need to be sure to log into the same flip every time because the node instance will only be running on one of them. Also be sure to access your website using the right flip server name!

## Activity

You should be able to run the `run.py` and access the page it serves while VPNed onto the server. It will display all entries of bsg_people table.

## Review

This should get you into a position where you have a web server running and it shows you are connected to a database. In addition you should be able to continue to access the site via a browser even if you end your SSH session provided you are on campus or logged into the VPN.

[1]: http://flask.pocoo.org/
[2]: https://github.com/pallets/flask

<<<<<<< HEAD
# Week 6
### User Management

The slides for this week are linked on Piazza. 

The code in this directory is what we created in class, plus possibly some
more detail or fixes. This README contains a detailed description of everything.

To run all of the code, make sure to 
`pip install Flask flask-sqlalchemy flask-wtf flask-login flask-bcrypt flask-mail`

Optionally, `pip install python-dotenv` to automatically set environment
variables in Python.

### Securing Passwords

When someone visits your site and registers for a new account (perhaps your site
is a e-commerce or bookmarking or image hosting website), they enter a username and password, 
and possibly other information. The **password** gives an attacker the most power over
a certain user; they can get all of the information they want on the user (since they
can authenticate as the user), and they can change your activity on the website. Perhaps
they delete some memorable albums, or start ordering random items off a e-commerce
website, or even elect to deactivate/delete your account.

Therefore, we'll be hashing our passwords. Hashing is a one-way function, and if the
resulting hash is long, then it will be computationally infeasible to find a collision.
For example, no collisions have been found for SHA256.

We'll be using `flask-bcrypt` for this.

To see a simple example of how `flask-bcrypt` works, we'll go into the REPL. There is a
`Bcrypt` class available to use from flask_bcrypt, and we use an instance of this class to
generate password hashes and then check a given password against a hash.

```python
>>> from flask_bcrypt import Bcrypt
>>> bcrypt = Bcrypt()
>>> bcrypt.generate_password_hash('a_password')
b'$2b$12$nz0fVuySYJBzJ.sXocYsuuHfUw5weyLCzOEJHjjLwvf1u/hChnam2'
```

We see that we get a byte string returned to us, so if we want to turn it into a normal
string, we can use the `decode()` function of the `bytes` object. The byte string is
encoded in `UTF-8`, and that is the default decoding.

```python
>>> bcrypt.generate_password_hash('a_password')
b'$2b$12$nz0fVuySYJBzJ.sXocYsuuHfUw5weyLCzOEJHjjLwvf1u/hChnam2'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$TPu20eIGwAl050BcZfd60uFDNpiiob3CYr9lKSuAPCJ0k/MuXML1e'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$Q0c.ZCab7QqPjQ3znxXqK.1xtuUYUhhMhy0GYj8I1r14823D/ZupK'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$HfAZT2hsoY4frIl2R6qDn.HAs6A2VUyplkQs6O9D3ont2t9dS9bEe'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$eIQ8MELmSkZW5kmF1MG/5uz8ufit6KrFXwRGStIM1FkUUxVbFIbMO'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$vGWOxXd/Ee00ubeglwxy7eSY7ryMyGm/1k9MDejvixYkixcChLqe2'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$9AnFKXs66A86ZQUknV4/m.w7zCZB3rLpfZgT7vJnLAQ7D/sl12wHa'
```

Notice how we generate a different hash everytime, even though we're hashing the same
password. This prevents attackers from just going through all combinations of passwords
to find a matching hash. Since `Bcrypt` is a slow hash, parsing through all these combinations
is much slower than for SHA256.

Also look at the first 7 characters in every hash string. The `2b` determines which 
version of `bcrypt` was used, the `12` indicates that `2^12` iterations of the
key derivation function were used (the recommended amount). The next 22 characters
are the 'salt' for this hash. 

A salt is a random string that is combined with the input, the user's password, a
that used as input, along with the password, to the
hashing function. The salt increases the security of all passwords, and especially
that of common passwords.

So how would we check that our password hash is equivalent to the hash of a password the
user enters? There is another function called `check_password_hash`, which takes
a parameter of the hash and of the potential password, and it checks for us.


```python
>>> pass_hash = bcrypt.generate_password_hash('a_password')
>>> pass_hash
b'$2b$12$exCUucO2pcFhvahPR/mDNeM7CJhuoj7cMJ4s1CxHZdzHApsQqbwYq'
>>> bcrypt.check_password_hash(pass_hash, 'a_password')
True
>>> bcrypt.check_password_hash(hash, 'another_password')
False
```

So we can get started using it in our application by adding it to `__init__.py`:

`__init__.py`:
```python
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xa4\x0c\x9c3B\xa8a\xc4\x19<z\x00\xc2\xc9\xcd\x14'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from flask_app import routes










First, a brief overview of classes in Python. You know what classes are already,
they're blueprints containing the properties and methods of a certain object.
You've worked with Java and Ruby in your classes and possibly others on your own,
and today we'll be looking at Python classes.

First, there are no formal interfaces in Python. Python does have Abstract
Base Classes (ABCs) that provide methods that must be implemented by subclasses.
There are also 'dunder' methods, methods that have double underscores before
and after a name. These are special methods that are called by built-in functions
and by operators.

Some dunder methods you may have already used are `__len__`, `__mult__`, and `__iter__`.
These methods are called by `len()`, `*`, and `for i in seq` (`seq` is the variable with
`__iter__` defined), respectively. Another example of a dunder method is `__str__`, 
which is called when you try to `print()` an object.

When creating a class, you have to provide an `__init__` method which is the constructor
for the class, and all instance methods of your class should have `self` as the first parameter.
We'll go over static/class methods at another time if they're needed.

Finally, you can use decorators inside classes to decorate methods or you can even
decorate the class as a whole. The same syntax is used in this case.

### Project Structure

To start off, we're restructuring our Flask apps going forward to conform
to Python standards, and to make our code cleaner/easier to read and run.

In this directory you'll see the `flask_app/` directory. This contains all the code
we write to create our app. This directory as an `__init__.py` file, which indicates
that the `flask_app/` directory is a Python package. 

The directory structure of `flask_app/`:
```
├── __init__.py
├── data.py
├── models.py
├── old_app.py
├── routes.py
├── templates
│   ├── about.html
│   ├── base.html
│   ├── feed.html
│   ├── index.html
│   ├── user.html
│   └── user_info.html
└── users.db
```

`old_app.py` contains our application code from week 2 for reference.

In the `__init__.py` file, we import the packages we need to create and
configure our application. Any variables we create in the `__init__.py` file
can be accessed using `from flask_app import var`, where `var` is a variable defined in
`__init__.py`. We'll create and set configuration options for our app in `__init__.py`.

To start off, we'll import `flask` and `sqlite3`. `sqlite3` is a builtin Python
module that will allow us to work with a local database. We'll also create our
application.

```python
from flask import Flask
import sqlite3

app = Flask(__name__)
```

We have our static `posts` data in the same file as our app currently. We'll
separate it into its own Python module for organization. `data.py` contains the
`posts` list of dicts now.

You might be wondering where we configure our routes now; we do it in `routes.py`.
Remember that we can import our app using `from flask_app import app`.
Next, we want to render templates and actually create our pages, so we'll also
import the `render_template` function from `flask`. Finally, we want to use
the `posts` list of dicts in our application, so we can import that from `data.py`, also.
We'll import some extra things from `flask` here and explain how we use them later.

`routes.py`:
``` python
from flask_app import app
from flask import render_template, request, redirect, url_for
from flask_app.data import posts
```

Outside the `flask_app/` directory, in the `wk4/` directory, we'll have a file
named `run.py`. This will be the file that we set to the `FLASK_APP` environment
variable. Using `flask run` in the `wk4/` directory will allow the database route to
work correctly. 

### SQLite Databases (Unsafe) Intro

Let's say we have a scenario where we want to allow visitors to our site to search for
users and get certain info about the users. People accessing our site should be able to get
the user's name and their bio, but not any other information, such as email or location.

First, we need some data in our database. To get a visual guide to create a SQLite database, 
we'll use [DB Browser for SQLite](https://sqlitebrowser.org/). This application also lets you
view the data in your database, so you can use it for visual checking when you're prototyping
your own applications.

In the DB Browser, we'll create a new database using `File -> New Database`. Create a new
database in the `wk4/flask_app/` directory with some desired name. 
We'll call our database `users.db` for clarity. An `Edit table definition` window should pop up:

![Create Table Window shown here][create_table_img]

We'll fill out this table using the values and options as shown in the slides, put
here for reference:

![New Table form filled out][users_table_img]

The top of the window is where we put the name of our new SQLite table. In the middle window,
we specify the name of each row in our table. In our case, we define the rows `id`, `name`,
`bio`, `email`, and `location`. 

`id` is designated as the primary key, which must be a 
unique value to differentiate each record in the table, so we'll just make it an integer
and auto-incrementing. The next four values are text strings, and we want every user
to have a bio, an email, and we want their location. This might be used in an application
for organizating meetups. 

We check off the `NN` option to indicate that we want a value
for each of these rows. We also check off the `U` value for our `email` field
so that two users cannot have the same email registered.

You can see the SQL query that is being generated by the DB Browser app in the bottom section.
This is the query that is executed to create our `Users` table in our database. After clicking
`OK`, your table will be created, and you can add data by going to the `Browse Data`.
In `Browse Data`, we can click the `New Record` button and then fill out the fields.
Here's some sample data that we used:

![Sample user data][user_data_img]

### Search bar - POST request (pt. 1)

Now in our templates directory, we'll create a template for a new page on our website
that will allow us to query user data. On `index.html`, we add the link to the User Info
page using:

``` html
<a href={{ url_for('user_info') }}>User Info Page</a>
```

The `url_for` function calls a routed function named `user_info`. We don't have a `user_info`
currently, so we create the method. In the `app.route()` decorator, we'll specify another
parameter named `methods`. We want a website visitor to be able to submit a form to
search for users and then see their name and bio. To do this, we'll configure the 
function like so:

```python
@app.route('/info', methods=['GET', 'POST'])
def user_info():
    pass
```

The `GET` request verb is automatically included in each routed function, unless its
explicity excluded using the `methods` parameter above. `methods` accepts a list of
HTTP verbs. We're using `GET` and `POST` here, but there are also other
verbs that you can specify by including it into the list to `methods`.
[Wikipedia][http verbs] has a list of these.

When a form on the `/info` page of our website is submitted, our `user_info` function
can access the information by using the global `request` object. We imported this
from `flask` earlier in `routes.py`. 

Let's create the actual form first, so we know what kind of data we'll be working with.

### HTML (unsafe) form

We'll create a new template file named `user_info.html` where we'll create an HTML form
so that site visitors can search for users. After the form is submitted, we want to show 
the results of the visitor's query on the same page. 

Here's our `user_info.html`:
```html
{% extends "base.html" %}
{% block content %}
<h1>User Info</h1>

<b>Enter a User's name to see their bio</b>
<form method="post">
    <input type="text" name="Username"> <br>
    <!-- <input type="text"> -->
    <input type="submit" name="All" value="See all users">
    <input type="submit" value="Submit">
</form>
<br>

Format: <br>
<b>User : Bio</b>
<ul>
{% for info in user_info %}
    <li>{{ info[0] }} : {{ info[1] }}</li>
{% endfor %}
</ul>

<a href={{ url_for('about') }}>About this Website</a>
<a href= {{ url_for('feed') }}>Go to Feed</a>
{% endblock %}
```

We make the form using the `form` HTMl tag, and we specify the method to be `"post"`. This
will send `POST` data to the function that is rendering this template. In our case, 
this form will send data to the `user_info()` function in `routes.py`. We have a text
input field and a submit input. 

At the bottom of the template, we specify the format of returned data and then display
all of our data. `user_info` will be a list of results, so we display all the results
using an unordered list. Finally, we end with links to other parts of our web application.

**Note:** This example is an unsafe way of using forms, because there is no protection against
CSRF (cross-site request forgery) attacks. We'll get into how to prevent those next week.

### Search bar - POST request (pt. 2)

Now, we'd like to update our `user_info()` routed function to handle the form data. Recall from
above that we can access the request data by using the global `request` object
that we imported using `from flask import request`. 

This code won't work yet,
```python
@app.route('/info', methods=['GET', 'POST'])
def user_info():
    if request.method == 'POST':
        return redirect(request.path)
    else:
        return render_template('user_info.html', title='User Info', user_info=user_info_data)
```

The `request` object has a property named `method` that indicates what type of request
was made to our application, so we check if its equal to `'POST'`. In this branch
of the `if-else`, we will redirect back to this function using `redirect(request.path)`.

We want to redirect because we're done processing the `POST` request. If we omitted the redirect,
then whenever a visitor reloaded the page after submitting the form, they would be asked
if they are sure they want to reload because form data may need to be resent. To get around that,
we redirect to our function. The path to our function is easily accessible as `request.path`, 
because the `request` object pointed to the `user_info()` function when the form was submitted.
The default HTTP method used is `GET`, so we would go into the `else` clause of the `if-else` 
branch.

The redirect confirmation prompt:
![Redirect confirmation][redirect]

In the `render_template()` function, we're specifying the `user_info` iterable in our template
to use data from some variable named `user_info_data`. That doesn't exist currently, but will
contain the search results once implemented.

How can we add search results to `user_info_data` and have the data persist across the redirect?
A straightforward way is to make it a global variable:

```python
user_info_data = []

@app.route('/info', methods=['GET', 'POST'])
def user_info():
    global user_info_data
    if request.method == 'POST':
        return redirect(request.path)
    else:
        return render_template('user_info.html', title='User Info', user_info=user_info_data)
```

The `global` keyword at the beginning of the function indicates that we want to mutate
the global `user_info_data` list. Trying to mutate a global variable inside of a function
is not possible without the `global` keyword.

Now we want to process the form data, retrieve relevant results from our `Users` table in our
database, and then display the results. To access the database, we'll edit our `__init__.py` file
to use the `sqlite3` database:

```python
from flask import Flask
import sqlite3

app = Flask(__name__)

db_path = 'users.db'
db = sqlite3.connect(db_path)
```

The `db` and `db_path` variables now exist in `flask_app`, but we're only going to use
`db`. Recall that we can import it into other files using `from flask_app import db`.
Back to `routes.py`, we'll edit the first line:

```python
from flask_app import app, db
""" Omitted code """
```

Further down in `routes.py`:

```python
user_info_data = []

@app.route('/info', methods=['GET', 'POST'])
def user_info():
    global user_info_data
    if request.method == 'POST':
        cursor = db.cursor()

        stmt = "SELECT name, bio FROM Users WHERE name = '%s' " % request.form['Username']

        result = cursor.execute(stmt)

        data = []
        for item in result:
            data.append(item)

        user_info_data = data

        print(stmt)
        
        print(request.form['Username'])

        return redirect(request.path)
    else:
        return render_template('user_info.html', title='User Info', user_info=user_info_data)
```

We use the `%s` format specifier in the SQL statement to insert the text input from our form.
Since we are requesting the `name` and `bio` from our `Users` table of our database, a tuple
is returned with this format: `(name, bio)`. 

To run the application, we'll need to edit `__init__.py` slightly, we'll add the line
`from flask_app import routes` at the end, so it looks like this:

`__init__.py`:
```python
from flask import Flask
import sqlite3

app = Flask(__name__)

db_path = 'users.db'
db = sqlite3.connect(db_path)

from flask_app import routes
```


If we run the application in the current
state and enter the string `Harry Potter` into the search field, we'll get a result back:

![Harry Potter result][hp]

This is all fine, but this code is vulnerable to an SQL injection attack. We're
not cleaning the form data before inserting it into our SQL statement. To demonstrate
how we can obtain the location and the email for each user from the `Users` table, also,
we created this statement:

```sql
' UNION SELECT name, location FROM Users UNION SELECT name, email FROM Users '
```

The first `'` character closes the single quotes in our statement. Then, we use the 
`UNION` verb to chain another SQL command. The second SQL command selects the 
`name` and `location` of each user in the `Users` table. We do the same thing again, 
but obtaining the `email` of each user now. 

The reason we can only pick two values at a time is because our statement is already obtaining 2
columns: `name` and `bio`. When we use `UNION`, we can only `SELECT` from two columns at a time,
also. Finally, we end the statement with a `'` character to close out the second single quote.

We'll run the web app and then put in this string for the form data input and click submit. 
You should get output similar to this:

![SQL Injection Results][injection]

If we want to prevent this while using `sqlite3`, we can edit a few lines to prevent this:

`routes.py`:
```python
""" Omitted code """
    """ Inside user_info() """
        stmt = 'SELECT name, bio FROM Users WHERE name = ?'
        result = cursor.execute(stmt, (request.form['Username'],))
```

And if we reload the web app and try the injection attack again, it won't work. The
`?` character is a placeholder. We pass in a tuple of values as the second parameter
to `cursor.execute()` and they will be substituted in for the question marks and 
automatically escaped to reduce the risk of an injection attack.

### SQLAlchemy

We just went over how an SQL injection attack would be executed and how to
prevent it when using `sqlite3` or another module to execute raw SQL statements.

There is a safer and more convenient way to work with database tables, and we don't
have to change our database-specific operations if, for example, we wanted to
use SQLite for prototyping our application locally and then use Postgres
for a production server. 

We'll use `SQLAlchemy` from now on, specifically through the `flask_sqlalchemy`
extension. Today, we'll go over a simple example of how to work with SQLAlchemy. 
To set the URI, which is just an identifier for our database, we use:

`__init__.py`:
```python
""" Omitted code """
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
""" Omitted code """
```

We want to use a `sqlite` database for prototyping. If we put 3 slashes after 
`sqlite:` then we create a database on a relative path. In this case, we
connect to `users.db` in the same directory as `__init__.py`, so we connect
to our previously created `sqlite` database.

If we use 4 slashes, we can specify an absolute path on our system; if we use 2
slashes, we create an in-memory database, so we can only poll and modify the database
while the application is running.

We'll also specify another option:

`__init__.py`:
```python
""" Omitted code """
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
""" Omitted code """
```

We disabled an option that wasn't needed; it'll just take extra memory.

Finally, we'll create our `db` variable with `flask_sqlalchemy`. We'll delete
all of our `sqlite3` code from `__init__.py` and add our new configuration code, so
it'll look like this now:

`__init__.py`:
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Relative Path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from flask_app import routes
from flask_app.models import *
```

`flask.models` is a module that will contain our `SQLAlchemy` model classes. We'll
create a class called `Users` that has the same schema as the data already
in the database. The name has to be `Users` to match up with the table already in
the database.

`models.py`:
```python
from flask_app import db

class Users(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'User: %s' % self.name
```

Every table we want to create has to be a subclass of `db.Model`, where you could replace
`db` with the name of your database variable.

Now how can we use this in place of `sqlite3` in our application? `Users` is now a `Model`
class, so it has an attribute named `query`. This attribute allows you to access all records
represented by the class, and then we can pick out certain records by using the `filter()`
method of our `query` object. After that, we can use the `all()` method to get all matching
records.

`routes.py`:
```python
from flask.models import *

""" Omitted code """
user_info_data = []

@app.route('/info', methods=['GET', 'POST'])
def user_info():
    global user_info_data
    if request.method == 'POST':
        user_info_data = Users.query.filter_by(name=request.form['Username']).all()

        return redirect(request.path)
    else:
        return render_template('user_info.html', title='User Info', user_info=user_info_data)
""" Omitted code """
```

Now we can edit the for loop in `user_info.html`. We access the `name`, `bio`, and other
attributes of each record by using dot syntax, so `info.name` or `info.bio`.

`user_info.html`:
```html
{% for info in user_info %}
    <li>{{ info.name }}: {{ info.bio }}</li>
{% endfor %}
```

Running the app in the current state will cause it to run exactly the same way as
before, except now its safer and cleaner to work with.

### Conclusion

In this lecture we showed how to work with `sqlite3` databases a low-level way, 
what could go wrong with injection attacks, and an introduction to using `SQLAlchemy`.
There are more features of `SQLAlchemy` that we'll cover as we need them in coming weeks.



[create_table_img]: ./images/create_table.png "Create Table Window"
[users_table_img]: ./images/users_table.png "Specify Users table"
[user_data_img]: ./images/sample_data.png "Sample Users Data"
[http verbs]: https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods
[redirect]: ./images/redirect.png "Redirect prompt"
[hp]: ./images/hp.png "Harry Potter search results"
[injection]: ./images/injection.png "SQL Injection sample attack"
=======
# Week 6
### User Management

The slides for this week are linked on Piazza. 

This week we'll look at an app where a user can register/login to our website 
and see all of the posts they've created, as well as look at other user's posts.
We haven't added any functionality to create posts.

The database we provide already has some users and posts in there. The users are:

| Username        | Email           | Password  |
| ------------- |:-------------:| -----:|
| harrypotter      | harry@hogw.edu | VoldemortSucks |
| gvanrossum     | guido@python.org     |   ilovepython3.8.0 |

To run all of the code, make sure to 
`pip install Flask flask-sqlalchemy flask-wtf flask-login flask-bcrypt`

The code in this directory is complete, and allows you to log-in as either of the users
above. It also allows you to create new accounts, but not create new posts. The `My Account`
page shows you all of the posts you created, but will redirect to the `Login` page if
no one is signed in.

We'll go over how we added each component of the login and registration system.

Optionally, `pip install python-dotenv` to automatically set environment
variables in Python.

#### Securing Passwords

When someone visits your site and registers for a new account (perhaps your site
is a e-commerce or bookmarking or image hosting website), they enter a username and password, 
and possibly other information. The **password** gives an attacker the most power over
a certain user; they can get all of the information they want on the user (since they
can authenticate as the user), and they can change your activity on the website. Perhaps
they delete some memorable albums, or start ordering random items off a e-commerce
website, or even elect to deactivate/delete your account.

Therefore, we'll be hashing our passwords. Hashing is a one-way function, and if the
resulting hash is long, then it will be computationally infeasible to find a collision.
For example, no collisions have been found for SHA256.

We'll be using `flask-bcrypt` for this.

To see a simple example of how `flask-bcrypt` works, we'll go into the REPL. There is a
`Bcrypt` class available to use from flask_bcrypt, and we use an instance of this class to
generate password hashes and then check a given password against a hash.

```python
>>> from flask_bcrypt import Bcrypt
>>> bcrypt = Bcrypt()
>>> bcrypt.generate_password_hash('a_password')
b'$2b$12$nz0fVuySYJBzJ.sXocYsuuHfUw5weyLCzOEJHjjLwvf1u/hChnam2'
```

We see that we get a byte string returned to us, so if we want to turn it into a normal
string, we can use the `decode()` function of the `bytes` object. The byte string is
encoded in `UTF-8`, and that is the default decoding.

```python
>>> bcrypt.generate_password_hash('a_password')
b'$2b$12$nz0fVuySYJBzJ.sXocYsuuHfUw5weyLCzOEJHjjLwvf1u/hChnam2'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$TPu20eIGwAl050BcZfd60uFDNpiiob3CYr9lKSuAPCJ0k/MuXML1e'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$Q0c.ZCab7QqPjQ3znxXqK.1xtuUYUhhMhy0GYj8I1r14823D/ZupK'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$HfAZT2hsoY4frIl2R6qDn.HAs6A2VUyplkQs6O9D3ont2t9dS9bEe'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$eIQ8MELmSkZW5kmF1MG/5uz8ufit6KrFXwRGStIM1FkUUxVbFIbMO'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$vGWOxXd/Ee00ubeglwxy7eSY7ryMyGm/1k9MDejvixYkixcChLqe2'
>>> bcrypt.generate_password_hash('a_password').decode()
'$2b$12$9AnFKXs66A86ZQUknV4/m.w7zCZB3rLpfZgT7vJnLAQ7D/sl12wHa'
```

Notice how we generate a different hash everytime, even though we're hashing the same
password. This prevents attackers from just going through all combinations of passwords
to find a matching hash. Since `Bcrypt` is a slow hash, parsing through all these combinations
is much slower than for SHA256.

Also look at the first 7 characters in every hash string. The `2b` determines which 
version of `bcrypt` was used, the `12` indicates that `2^12` iterations of the
key derivation function were used (the recommended amount). The next 22 characters
are the 'salt' for this hash. 

A salt is a random string that is combined with the input, the user's password, a
that used as input, along with the password, to the
hashing function. The salt increases the security of all passwords, and especially
that of common passwords.

So how would we check that our password hash is equivalent to the hash of a password the
user enters? There is another function called `check_password_hash`, which takes
a parameter of the hash and of the potential password, and it checks for us.


```python
>>> pass_hash = bcrypt.generate_password_hash('a_password')
>>> pass_hash
b'$2b$12$exCUucO2pcFhvahPR/mDNeM7CJhuoj7cMJ4s1CxHZdzHApsQqbwYq'
>>> bcrypt.check_password_hash(pass_hash, 'a_password')
True
>>> bcrypt.check_password_hash(hash, 'another_password')
False
```

So we can get started using it in our application by adding it to `__init__.py`:

`__init__.py`:
```python
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xa4\x0c\x9c3B\xa8a\xc4\x19<z\x00\xc2\xc9\xcd\x14'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from flask_app import routes
```

#### Flask-Login

Flask-Login provides user session management in our Flask apps. We can use its functions
to login and logout users, access the current user, and restrict access to pages
on our website which require authentication. 

It also allows you to add the 'Remember Me' functionality to your website, 
to allow a user to still be logged in if they closed their browser. How it does this
is by storing a cookie in the browser with the user's ID. We won't go over
how to implement this functionality in this class.

When setting up your app, there's a setting we have to specify for `flask_login`,
the `login_view` attribute of a `LoginManager()` object. First, we import the
`LoginManager` class from `flask_login`, and then initialize it and set the attribute.

`__init__.py`:
```py
""" Omitted imports """
from flask_login import LoginManager

""" Omitted setup code """

login_manager = LoginManager(app)
login_manager.login_view = 'login'
```

We create the `login_manager` object similarly to how we worked with the other
`flask` extensions; we pass in our `app` object to `LoginManager()`. Next, we
set `login_manager.login_view = 'login'`. This means that the login page
for our website will be accessed by going to the view function named `'login'`.
When an unauthenticated user tries to access some restricted page on our website,
they are sent to the `'login'` page.

You can rename `login_manager.login_view` to whatever view function that you want,
but the user will be redirected to that view by `flask_login` if authentication
is required to access a page.

Now, if we want to have a login page, then we must have a login form on that
page so that the user can input their data and we can validate it. 
For our website, we'll let the user just login with their unique username
and password. Here's what that form might look like:

`forms.py`:
```py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
""" Omitted forms """
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('That username does not exist in our database.')
```

Notice the new `SubmitField` we're using. We meant to show that in a previous lecture,
when first discussing `WTForms`, but it slipped our mind then. 

Otherwise, we also have a `validate_` function. Every function we create in our form
that starts with `validate_` and ends with the name of the variable we are validating
will be called when we call `form.validate_on_submit()` or `form.validate()`. Notice
that we also raise a `ValidationError`. This does not crash our website; it is 
recorded, literally, as a validation error. This is how we can define custom
validators. 

The `validate_username()` function checks if there exists a user with the
username entered in the form. If no such user exists, then the query returns `None`,
at which point we raise a custom error message. Recall the user table at the top
of the page, and let's try logging in as a user that does not exist in the database.
Here's the result:

![Login failure][login_fail]

You can only create a custom validator for one field at a time, and we'll see
how this is implemented later with a `RegistrationForm`.

How did we get the error message to show up? Each field of a form has a list of errors
that might have been encountered during validation, so given the `username`
field in the above `LoginForm`, we can list the validation errors using the code below.
We will show the errors directly below the rendered field.

`login.html`:
```html
<!-- Omitted HTML -->
{{ form.username }}
{% if form.username.errors %}
<div>
    {% for error in form.username.errors %}
        <span>{{ error }}</span>
    {% endfor %}
</div>
<!-- Omitted HTML -->
```

In Python, when we do `if li: pass`, where `li` is a list, the `__len__()` function of a
`list` object gets called. If a list is empty, then `__len__()` returns 0 and the `if` statement
does not execute its branch of code. 

So in this snippet, if our `errors` list is non-empty, then we go through the list
of errors and print them to the screen, as you can see in the image above.
This is available to every field, so you can add the error-printing snippet
below every field. It isn't really necessary for the `SubmitField`, though.

Before we get to implementing `login()`, we have to modify our `models.py` slightly.
`flask_login` provides us with a global variable called `current_user`. We can
check if the `current_user` is authenticated, active, anonymous, or get their id. 
However, to do this, our User class needs to have the properties:
- `is_authenticated`
- `is_active`
- `is_anonymous`
implemented, along with a `get_id()` function. We can use a shortcut and make the
class that represents our user a subclass of `UserMixin`. `UserMixin` is provided
from `flask_login`, and it implements the above properties and method.
In our case, the User model represents the user, so we can just indicate that the model
is also a subclass of `UserMixin` by changing (in `models.py`)

```py
""" Omitted imports """

class User(db.Model):
    """ Omitted code """
```

to this:

```py
""" Omitted imports """
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """ Omitted code """
```

If you choose not to subclass from `UserMixin` in future applications, you would need to
implement the above properties and function on your class.

Finally, `flask_login` needs to know how to load the user to set the `current_user`
global variable. To give `flask_login` this power, we have to implement a function
that returns a user, and decorate it with `login_manager.user_loader`.

`flask_login` keeps track of the `id` for a user, which should be a unique value. 
We'll import our `login_manager` and use it to create our user-loading function like so:

`models.py`:
```py
from flask_app import login_manager
""" Omitted imports """

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

""" Omitted models """
```

Now `flask_login` calls this function to get a User, and `current_user`
will have access to all of the `Column`s in the model.

Now to implement `login()`, I'll list all of the code first and then explain how it works.

`routes.py`:
```py
from flask_login import login_user, current_user
from flask_app.forms import LoginForm
from flask_app.models import User
""" Omitted imports """

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('account'))

    return render_template('login.html', title='Login', form=form)
```

The methods for `login()` are `GET` and `POST` because the form will send a `POST` request
to this function when submitted. The first `if` statement we have checks if
the `current_user` is authenticated, i.e. if  there is a user ID stored in the session.
If so, then we simply redirect to the front page so that logged-in users don't see
the login page.

Next, we create the form. If the form can be validated once it is submitted, we retrieve
the user in the database which has the same username as the one input in the form. 
We check if `user is not None`, which *isn't necessary* since we already have the
`validate_username()` function in `LoginForm`, but we'll be explicit for clarity.

We check the password hash using the `bcrypt.check_password_hash()` function just
as we did earlier in this document, and if everything checks out, we
call the `login_user(user)`, which sets the user session. Behind the scenes, `flask_login`
called the `load_user()` function we defined in `models.py`. In the end, we redirect
to the account page for the user.

Finally, we actually render the login page using `render_template`, just as we have
done before.

The rest of the login page is implemented at `login.html`. If a user does not have
an account, though, we want them to register for a new account. In `login.html` we
included a link to the `register` function, so now we'll implement it.

Here's the form in `forms.py`:
```py
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_user(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken')

    def validate_email(self, email):        
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is taken')
```

We specify `StringField`s and `PasswordField`s. There is a validator on the `confirm_password`
field requiring that its data is equal to the `password` field's data.

There are two custom `validate_` functions defined here. One for username and one for email.
Other then these differences, this is all stuff you've seen before.

Here's what happens if we input some wrong data into our form:

![Registration fail][registration_fail]

Now to implement the `register()` function, here is the code:
```py
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)
```

Again, like with `login()`, we redirect to the index if the user is already authenticated.
If a user is not logged in and we received a valid submission for our form,
we generate the password hash like we did earlier in this document, and we just create
a new User, add them to the database, and commit our changes. We then redirect
the user to the `login()` page so that they can login with their new credentials.

Our last line renders the template like we've done before.

What if the current user of our website wants to logout? `flask_login` provides
a function named `logout_user()` which will clear out the user ID from the session.
Let's implement the `logout()` function:

`routes.py`:
```py
from flask_login import logout_user
""" Omitted imports """

""" Omitted code """
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))
```

Pretty simple. We call the `logout_user()` function and then redirect to the main page.
Standard behavior like we see on other websites.

Now, what if we want to restrict some pages on our website so that a user has to be
logged-in in order to access the page? `flask_login` provides the `login_required`
decorator that we can add on top of any view function to restrict access.

Remember the `login_manager.login_view` variable we set in `__init__.py`? When
an unauthenticated user attempts to access a `login_required` page,
they'll be redirected to the `login()` view function, the value of `login_manager.login_view`.

Here is the code for a user viewing their account details:

`routes.py`
```py
from flask_login import login_required
from flask_app.forms import UpdateForm
""" Omitted imports """

""" Omitted code """
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()

    if form.validate_on_submit():
        current_user.username = form.username.data

        db.session.commit()

        return redirect(url_for('account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
    
    return render_template('account.html', title='Account', form=form)
```

We add the `@login_required` decorator above the function. `flask_login` will take
care of the code for redirecting unauthenticated users away from `/account`. 
We create an `UpdateForm()` (we'll show the code for it shortly); the `UpdateForm()`
simply allows users to update their username to something else that is not taken.

Here's `UpdateForm`:
`forms.py`:
```py
""" Omitted code """
class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('That username is already taken')
```

We only have one field for the new username. The `validate_username()` function
checks if the username is already taken; if so, it raises a `ValidationError`. 

So looking back at our code for the `register()` function, if `UpdateForm()`
was validated and submitted, then we can just change the `current_user`'s username
and commit the change. Since `current_user` is of type `User`, any changes
we make to `current_user` can be commited to the database rightaway. 

We have the `elif request.method == 'GET'` so that we can add the user's username
into the username field on page load. This isn't necessary, it's just a 
feature to make it easier for the user to change their username *slightly* if
that's what they are trying to do. 

Here's what it looks like if the form failed to validate:

![Change username failure][username_failure]

The last line, we render our template like we usually do.

One last thing; `current_user` is immediately available for us to use in templates.
You might notice in the templates that we're calling properties of `current_user`. 
We mainly use `current_user.is_authenticated` to show the current user's 
username on all the pages (`base.html`). We also use it to show
the current user's email on `account.html`.

#### Conclusion

We looked at `flask_login` mainly in these notes. We tried to explain
everything to the best of our ability, giving examples for everything you
might need to implement a user management system for your own website.

If you'd like to learn more about anything presented in this document,
here are some links:

[WTForms Docs](https://wtforms.readthedocs.io/en/stable/index.html)

[Custom validators in WTForms](https://wtforms.readthedocs.io/en/stable/validators.html#custom-validators)

[Flask-Login Docs](https://flask-login.readthedocs.io/en/latest/#flask-login)

[login_fail]: ./images/login_fail.png "Login failure visual"
[registration_fail]: ./images/registration_fail.png "Registration fail visual"
[username_failure]: ./images/username_fail.png "Username fail visual"
>>>>>>> afa158b78cafcfb689bf752b992e49d83dcbb0f3

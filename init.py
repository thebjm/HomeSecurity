#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 23:21:08 2019

@author: thebjm
"""

# import the necessary packages
from flask import *
from flask_mysqldb import *
from wtforms import *
import os
from werkzeug import secure_filename
from wtforms.fields.html5 import *
from wtforms.validators import InputRequired
from functools import wraps
import datetime
#from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, expose

app = Flask('Smart Door')
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key= 'secret123'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'thebjm'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'homeSecurity'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#Init MySQL

mysql = MySQL(app)




class LoginForm(Form):
    username = StringField('User Name', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])



# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:

            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('home'))
    return wrap



@app.route("/")

def index():
    return redirect(url_for('home'))

@app.route("/home", methods = ['GET', 'POST'])

def home():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    else:
        form = LoginForm(request.form)
        if request.method == 'POST':
            username = form.username.data
            password = form.password.data

            #create Cursor

            cur = mysql.connection.cursor()

            #get user data

            result= cur.execute("SELECT * FROM logins WHERE username = %s", [username])

            if result >0:
                data = cur.fetchone()
                get_name = data ['first_name'] + ' ' +data['last_name']
                get_password = data['password']
                app.logger.info(get_name)

                if password == get_password:
                    session['logged_in'] = True
                    session['username'] = get_name


                    flash('Hello ' +get_name , 'success')
                    return redirect(url_for('dashboard'))

                    app.logger.info('Password Match')
                else:
                    flash('Invalid Login', 'danger')
                    app.logger.info('Not')
                #close connection
                cur.close()

            else:

                flash('User not found', 'danger')
                app.logger.info('No user')


            app.logger.info(username)

            return redirect(url_for('home'))

        return render_template('home.html', form = form)




# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('home'))



#register
class RegisterForm(Form):
    first_name = StringField('First Name', validators = [InputRequired()])
    last_name = StringField('Last Name', validators = [InputRequired()])
    email = EmailField('Email', validators = [InputRequired()])
    phone = StringField('Phone Number', validators = [InputRequired()])
    username = StringField('User Name', validators = [InputRequired()])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message = 'passwords not match')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        f_name = form.first_name.data
        l_name = form.last_name.data
        email = form.email.data
        phone = form.phone.data
        username = form.username.data
        password = form.password.data

        #create cursor

        curr =  mysql.connection.cursor()
        curr.execute("INSERT INTO logins (first_name, last_name, email_id, phone, username, password) VALUES (%s, %s, %s, %s, %s, %s)", (f_name, l_name, email, phone, username, password))

        #cursor commit

        mysql.connection.commit()

        curr.close()

        flash('You are now registered ' , 'success')

        return redirect(url_for('home'))


    return render_template('register.html', form = form)



@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')


#user upload
target =  os.path.join(APP_ROOT, 'static/images/')

print(target)

if not os.path.isdir(target):
    os.mkdir(target)
app.config['target'] = target

@app.route('/dashboard', methods=['GET' , 'POST'] )
def upload():

    if request.method == 'POST':
        name = request.form['name']
        print (name)
        user = os.path.join(target, name)
        if not os.path.isdir(user):
            os.mkdir(user)
        file = request.files['file' ]
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")

        filename = secure_filename(file.filename or '')
        filename = time + "_" + filename
        print(filename)
        destination = "/".join([user, filename])
        print(destination)
        file.save(destination)


        #fetchdata
        name =  request.form['name']
        phone = request.form['phone']
        typeofvisitor = request.form['typeofvisitor']
        address = request.form['address']
        u_admin = session['username']

        print (u_admin)

        #create cursor

        curr1 =  mysql.connection.cursor()
        curr1.execute("INSERT INTO visitors_details (name, address, typeofvisitor, phone, photo, admin) VALUES (%s, %s, %s, %s, %s, %s )", (name, address, typeofvisitor, phone, filename, u_admin))

        #cursor commit

        mysql.connection.commit()

        curr1.close()

        flash('New Entry Done ' , 'success')

        return redirect(url_for('dashboard'))



    return render_template('dashboard.html', form = form)


#check old data
@app.route('/database')
@is_logged_in
def database():
    curr_data =  mysql.connection.cursor()

    result_data = curr_data.execute('SELECT * from visitors_details')

    alldata = curr_data.fetchall()

    if( result_data > 0):
        return render_template('database.html', alldata = alldata)
    else:
        msg = 'No DATA found'
        return render_template('database.html', msg = msg)

    curr_data.close()



# Delete Member
@app.route('/delete_member/<string:id>', methods=['POST'])
@is_logged_in
def delete_member(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM visitors_details WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Visitor Delete', 'success')

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)

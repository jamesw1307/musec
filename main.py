from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlite3 import connect
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musek.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

conn = sqlite3.connect('musek.db') #connect database
cursor = conn.cursor()
username = ""
#The login page will be the default page the website directs to
@app.route('/', methods = ['POST', 'GET'])
def login():
    global username
    #takes values from the username and password input box
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = sqlite3.connect('musek.db') #connect database
        cursor = conn.cursor()
        #Get id of the username entered
        cursor.execute('SELECT id FROM User WHERE username = ?;', (username,))
        userId = cursor.fetchone()
        conn.close()
        if list(username):
            if list(password):
                return redirect(url_for('profile', id = userId[0]))
            else:
                print('Enter valid password')
        
    return render_template('profile.html')

@app.route('/user/<int:id>')
def profile(id):
    global username
    #profile = User.query.filter_by().first_or_404()
    conn = sqlite3.connect('musek.db') #connect database
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM User WHERE username = ?;', (username,)) #Execute query
    userId = cursor.fetchone()
    cursor.execute('SELECT name FROM Album WHERE id IN (SELECT albumId FROM UserAlbumGenreArtist WHERE userId = ?);', (id,))
    profile = cursor.fetchall() #fetch every result
    conn.close()
    return render_template('profile.html', profile = profile, userId = userId)

if __name__ == '__main__':
    app.run(port = 8080, debug = True)
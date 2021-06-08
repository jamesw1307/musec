from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlite3 import connect
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musek.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#The login page will be the default page the website directs to
@app.route('/', methods = ['POST', 'GET'])
def login():
    global username
    errorMessage = None
    #takes values from the username and password input box
    if request.method == 'POST':
        #
        username = request.form.get('username')
        password = request.form.get('password')

        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')
        #takes username and password values from new_username and new_password and commits it to musek.db
        if new_password and new_username:
            db.session.add(models.User(username=new_username, password=new_password))
            db.session.commit()
        else:
            #if no value print errorMessage
            errorMessage = 'please enter a valid username and password'

        if username and password:
            #Get id from db of the username and password entered in username and password
            userInfo = models.User.query.filter_by(username=username, password=password).all()
            print(userInfo)
            userId = userInfo[0].id
            #if username and password are list redirect to profile with id = userId
            if list(username) and list(password):
                print('valid')
                return redirect(url_for('profile', id = userId))
        elif username:
            errorMessage = 'incorrect password'

    return render_template('login.html', errorMessage=errorMessage)

@app.route('/user/<int:id>')
def profile(id):
    global username
    profile = models.User.query.filter_by().first_or_404()
    
    #cursor.execute('SELECT id FROM User WHERE username = ?;', (username,)) #Execute query
    username = models.User.query.filter_by(id=id)
    #cursor.execute('SELECT name FROM Album WHERE id IN (SELECT albumId FROM UserAlbumGenreArtist WHERE userId = ?);', (id,))
    albumInfo = models.Album.query.filter_by(addedBy=id).all()
    artistInfo = models.Artist.query.filter_by(addedBy=id).all()
    genreInfo = models.Genre.query.filter_by(addedBy=id).all()
    return render_template('profile.html', username=username, albumInfo=albumInfo, artistInfo=artistInfo, genreInfo=genreInfo)

#@app.route('/album')

if __name__ == '__main__':
    app.run(port = 8080, debug = True)
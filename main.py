import sqlite3
from sqlite3 import connect

from flask import Flask, redirect, render_template, request, url_for, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import urandom

import models

app = Flask(__name__)
SECRET_KEY = ('jam')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musek.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#The login page will be the default page the website directs to
@app.route('/', methods = ['POST', 'GET'])
def create_account():
    global userId
    global username
    session['logged_in'] = False
    errorMessage = None
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')
        #takes username and password values from new_username and new_password and commits it to musek.db
        if new_password and new_username:
            user_info = models.User(
                username = new_username,
                password = generate_password_hash(new_password, salt_length=10)
            )
            db.session.add(user_info)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            #if no value print errorMessage
            errorMessage = 'please enter a valid username and password'
    
    return render_template('createaccount.html', errorMessage=errorMessage)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    global userId
    global username
    errorMessage = None
    #takes values from the username and password input box
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_stuff = models.User.query.filter_by(username=username).first()

        #check that username and unhashed password match
        if username and check_password_hash(user_stuff.password, password):
            #Get id from db of the username entered in username
            userInfo = models.User.query.filter_by(username=username).all()
            #get id of the user
            userId = userInfo[0].id
            username = username
            #if username and password are list redirect to profile with id = userId and session to true
            if list(username) and list(password):
                print('valid')
                session['logged_in'] = True
                return redirect(url_for('profile', id = userId))
        elif username or password:
            errorMessage = 'enter into all fields'
    return render_template('login.html', errorMessage=errorMessage)

@app.route('/user')
def profile():
    if 'logged_in' not in session:
        return redirect(url_for('create_account'))
    global username
    #profile = models.User.query.filter_by().first_or_404()
    
    albumInfo = models.Album.query.filter_by(addedBy=userId).all()
    artistInfo = models.Artist.query.filter_by(addedBy=userId).all()
    genreInfo = models.Genre.query.filter_by(addedBy=userId).all()
    return render_template('profile.html', username=username, albumInfo=albumInfo, artistInfo=artistInfo, genreInfo=genreInfo)

@app.route('/album', methods = ['POST', 'GET'])
def album():
    if 'logged_in' not in session:
        return redirect(url_for('create_account'))
    global username
    global userId
    if request.method == 'POST':
        album_name = request.form.get('album_name')
        release_date = request.form.get('release_date')

        #if all fields are full enter to db
        if album_name and release_date:
            db.session.add(models.Album(name=album_name, releaseDate=release_date, addedBy=userId))
            db.session.commit()
        #elif one field is blank, error
        elif album_name or release_date:
            print('please enter in all fields')

    allAlbums = models.Album.query.all()
    
    return render_template('album.html', username=username, allAlbums=allAlbums)

@app.route('/artist', methods = ['POST', 'GET'])
def artist():
    if 'logged_in' not in session:
        return redirect(url_for('create_account'))
    global username
    global userId
    if request.method == 'POST':
        artist_name = request.form.get('artist_name')
        description = request.form.get('description')
        active_years = request.form.get('active_years')

        if artist_name and description and active_years:
            db.session.add(models.Artist(name=artist_name, description=description, activeYears=active_years, addedBy=userId))
            db.session.commit()

    allArtists = models.Artist.query.all()
    return render_template('artist.html', username=username, allArtists=allArtists)

if __name__ == '__main__':
    app.secret_key = urandom(10)
    app.run(port = 8080, debug = True)

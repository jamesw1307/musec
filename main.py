import sqlite3
from sqlite3 import connect

from flask import Flask, redirect, render_template, request, url_for, session
from flask_login import LoginManager
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import urandom

import models


app = Flask(__name__)
SECRET_KEY = ('jam')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musek.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, session_options={'autoflush': False})


#The login page will be the default page the website directs to
@app.route('/', methods = ['POST', 'GET'])
def create_account():
    session['logged_in'] = False
    errorMessage = None
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')
        #takes username and password values from new_username and new_password and commits it to musek.db
        if new_password and new_username:
            user_info = models.User(
                username = new_username,
                #generates a random string for the password in the database so the users password is secure
                password = generate_password_hash(new_password, salt_length=10)
            )
            db.session.add(user_info)
            db.session.commit()
            #redirect to login to enter the users username and password to login
            return redirect(url_for('login'))
        else:
            #if no value print errorMessage
            errorMessage = 'please enter a valid username and password'
    
    return render_template('createaccount.html', errorMessage=errorMessage)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    errorMessage = None
    #takes values from the username and password input box
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_stuff = models.User.query.filter_by(username=username).first()

        #check that username and unhashed password match
        if username and check_password_hash(user_stuff.password, password):
            #Get id from db of the username entered in username
            user_info = models.User.query.filter_by(username=username).first_or_404()
            #get id of the user
            user_id = user_info.id
            #if username and password are list redirect to profile with session containing the users id
            if list(username) and list(password):
                print('valid')
                session['logged_in'] = user_id
                return redirect(url_for('profile'))
        elif username or check_password_hash(user_stuff.password, password):
            errorMessage = 'username or password incorrect'

    return render_template('login.html', errorMessage=errorMessage)


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    #if user tries to access page without being logged in redirect to create_account
    if 'logged_in' not in session:
        return redirect(url_for('create_account'))
    #if logged in take the info from the session
    elif 'logged_in' in session:
        user_info = session['logged_in']
        user_id = user_info
        username = models.User.query.filter_by(id=user_id).first_or_404()
    
    album_info = models.Album.query.filter_by(addedBy=user_id).all()
    artist_info = models.Artist.query.filter_by(addedBy=user_id).all()
    genre_info = models.Genre.query.filter_by(addedBy=user_id).all()

    #if delete button on any user entry is clicked
    if request.method == 'POST':
        #get id of the entry linked to the delete button
        album_id = request.form.get('album_id')
        artist_id = request.form.get('artist_id')
        genre_id = request.form.get('genre_id')

        #if there is a value for the entry id, delete from the database
        if album_id:
            db.session.query(models.Album).filter_by(id=album_id).delete()
            db.session.commit()
        elif artist_id:
            db.session.query(models.Artist).filter_by(id=artist_id).delete()
            db.session.commit()
        elif genre_id:
            db.session.query(models.Genre).filter_by(id=genre_id).delete()
            db.session.commit()

        return redirect(url_for('profile')) #reload page

    return render_template('profile.html', username=username, albumInfo=album_info, artistInfo=artist_info, genreInfo=genre_info)


class SelectArtist(FlaskForm):
    artists = SelectField('Artist', validators=[DataRequired()], coerce=int)


class SelectGenre(FlaskForm):
    genre = SelectField('Genre', validators=[DataRequired()], coerce=int)


@app.route('/album', methods=['POST', 'GET'])
def album():
    if 'logged_in' not in session:
        return redirect(url_for('create_account'))
    elif 'logged_in' in session:
        user_info = session['logged_in']
        user_id = user_info
        username = models.User.query.filter_by(id=user_id).first_or_404()

    artist_form = SelectArtist()
    artists = models.Artist.query.all()
    artist_form.artists.choices = [(artist.id, artist.name) for artist in artists]

    genre_form = SelectGenre()
    genres = models.Genre.query.all()
    genre_form.genre.choices = [(genre.id, genre.name) for genre in genres]

    if request.method == 'POST':
        album_name = request.form.get('album_name')
        release_date = request.form.get('release_date')

        #if all fields are full enter to db
        if artist_form.validate_on_submit() and album_name and release_date:
            #get selected artist from form and query for its id
            artist = dict(artist_form.artists.choices).get(artist_form.artists.data)
            artist_info = models.Artist.query.filter_by(name=artist).first_or_404()
            artist_id = artist_info.id

            album_info = (models.Album(name=album_name, releaseDate=release_date, artist=artist_id, addedBy=user_id))
            
            db.session.add(album_info)
            db.session.commit()
        #elif one field is blank, error
        elif album_name or release_date:
            print('please enter in all fields')

        if genre_form.validate_on_submit():
            #get selected genre from form and query for its id
            genre = dict(genre_form.genre.choices).get(genre_form.genre.data)
            genre_info = models.Genre.query.filter_by(name=genre).first_or_404()

            #get genreId from request form from html
            album_id = request.form.get('album_id')

            album = models.Album.query.filter_by(id=album_id).first_or_404()
            album.genres.append(genre_info)
            db.session.merge(album)
            db.session.commit()
    
    all_albums = models.Album.query.all()

    return render_template('album.html', username=username, allAlbums=all_albums, artist_form=artist_form, genre_form=genre_form)


@app.route('/artist', methods = ['POST', 'GET'])
def artist():
    if 'logged_in' not in session:
        return redirect(url_for('create_account'))
    elif 'logged_in' in session:
        user_info = session['logged_in']
        user_id = user_info
        username = models.User.query.filter_by(id=user_id).first_or_404()

    if request.method == 'POST':
        artist_name = request.form.get('artist_name')
        description = request.form.get('description')
        active_years = request.form.get('active_years')

        if artist_name and description and active_years and artist_name:
            db.session.add(models.Artist(name=artist_name, description=description, activeYears=active_years, addedBy=user_id))
            db.session.commit()
        else:
            print('please enter in all fields')

    all_artists = models.Artist.query.all()
    return render_template('artist.html', username=username, allArtists=all_artists)


class SelectAlbum(FlaskForm):
    albums = SelectField('Album', validators=[DataRequired()], coerce=int)


@app.route('/genre', methods = ['POST', 'GET'])
def genre():
    if 'logged_in' not in session:
        return redirect(url_for('create_account'))
    elif 'logged_in' in session:
        user_info = session['logged_in']
        user_id = user_info
        username = models.User.query.filter_by(id=user_id).first_or_404()

    form = SelectAlbum()
    albums = models.Album.query.all()
    form.albums.choices = [(album.id, album.name) for album in albums]

    if request.method == 'POST':
        genre_name = request.form.get('genre_name')
        description = request.form.get('description')

        if genre_name and description:
            genre_info = (models.Genre(name=genre_name, description=description, addedBy=user_id))
            
            db.session.add(genre_info)
            db.session.commit()
        
        if form.validate_on_submit():
            #get selected album from form and query for its id
            album = dict(form.albums.choices).get(form.albums.data)
            album_info = models.Album.query.filter_by(name=album).first_or_404()

            #get genreId from request form from html
            genre_id = request.form.get('genre_id')

            genre = models.Genre.query.filter_by(id=genre_id).first_or_404()
            genre.albums.append(album_info)
            db.session.merge(genre)
            db.session.commit()
    
    allGenres = models.Genre.query.all()

    return render_template('genre.html', username=username, allGenres=allGenres, form=form) 


if __name__ == '__main__':
    app.secret_key = urandom(10)
    app.run(port = 8080, debug = True)

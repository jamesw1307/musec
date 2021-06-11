from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from main import db

#These classes take data from the musek.db file to use in the code

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String())
    password = db.Column(db.String())

class Genre(db.Model):
    __tablename__ = 'Genre'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    addedBy = db.Column(db.Integer, db.ForeignKey('User.id'))
    #albums = db.Column(db.Integer, db.ForeignKey('Album.id'))

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    photo = db.Column(db.String())
    description = db.Column(db.String())
    activeYears = db.Column(db.String())
    addedBy = db.Column(db.Integer, db.ForeignKey('User.id'))
    #albums = db.Column(db.Integer, db.ForeignKey('Album.id'))

class Album(db.Model):
    __tablename__ = 'Album'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    coverArt = db.Column(db.String())
    releaseDate = db.Column(db.String())
    addedBy = db.Column(db.Integer, db.ForeignKey('User.id'))
    artist = db.Column(db.Integer, db.ForeignKey('Artist.id'))
'''
class UserAlbumGenreArtist(db.Model):
    __tablename__ = 'UserAlbumGenreArtist'
    albumId = db.Column(db.Integer, db.ForeignKey('album.Id'))
    genreId = db.Column(db.Integer, db.ForeignKey('genre.Id'))
    artistId = db.Column(db.Integer, db.ForeignKey('artist.Id'))
    userId = db.Column(db.Integer, db.ForeignKey('user.Id'))
    '''
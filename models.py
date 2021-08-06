from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from main import db

#These classes take data from the musek.db file to use in the code

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __repr__(self):
        return self.username

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    photo = db.Column(db.String())
    description = db.Column(db.String())
    activeYears = db.Column(db.String())

    addedBy = db.Column(db.Integer, db.ForeignKey('User.id'))
    albums = db.relationship('Album', backref='Artist')

    def __repr__(self):
        return self.name

AlbumGenres = db.Table('AlbumGenres', db.Model.metadata,
    db.Column('genreId', db.Integer, db.ForeignKey('Genre.id')),
    db.Column('albumId', db.Integer, db.ForeignKey('Album.id')),
)

class Genre(db.Model):
    __tablename__ = 'Genre'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    addedBy = db.Column(db.Integer, db.ForeignKey('User.id'))

    albums = db.relationship('Album', secondary=AlbumGenres, back_populates='genres')

    def __repr__(self):
        return self.name

class Album(db.Model):
    __tablename__ = 'Album'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    coverArt = db.Column(db.String())
    releaseDate = db.Column(db.Integer())
    addedBy = db.Column(db.Integer, db.ForeignKey('User.id'))
    artist = db.Column(db.Integer, db.ForeignKey('Artist.id'))

    genres = db.relationship('Genre', secondary=AlbumGenres, back_populates='albums')
    artistName = db.relationship('Artist', backref='Album')

    def __repr__(self):
        return self.name

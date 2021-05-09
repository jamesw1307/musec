from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#The profile page will be the default page the website directs to
@app.route('/')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(port = 8080)
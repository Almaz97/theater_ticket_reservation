from flask import Flask, render_template, redirect, url_for, request
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_should_be_a_secret'
mosus = Modus(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'postgresql://almaz:Almaz@localhost/reservation'

# DB models

class Administrators(db.Model):
    __tablename__ = 'Administrators'
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.Text)
    second = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

class Theater(db.Model):
    __tablename__ = 'Theater'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    am_auditorium = db.Column(db.Integer)
    address = db.Column(db.Text)
    description = db.Column(db.Text)

    #relationships
    auditorium = db.relationship('Auditorium', backref='theater')
    spectacle = db.relationship('Spectacle', backref='theater')
    screening = db.relationship('Screening', backref='theater')
    reservation = db.relationship('Reservation', backref='theater')

    def __str__(self):
        return self.name

class Auditorium(db.Model):
    __tablename__ = 'Auditorium'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    id_theater = db.Column(db.Integer, db.ForeignKey('Theater.id')) #FK
    am_seats = db.Column(db.Integer)

    #relationships
    screening = db.relationship('Screening', backref='auditorium')

    def __str__(self):
        return self.name

class Spectacle(db.Model):
    __tablename__ = 'Spectacle'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    id_theater = db.Column(db.Integer, db.ForeignKey('Theater.id')) #FK
    description = db.Column(db.Text)

    #relationships
    spectacle = db.relationship('Screening', backref='spectacle')

    def __str__(self):
        return self.title

class Screening(db.Model):
    __tablename__ = 'Screening'
    id = db.Column(db.Integer, primary_key=True)
    id_auditorium = db.Column(db.Integer, db.ForeignKey('Auditorium.id')) #FK
    id_spectacle = db.Column(db.Integer, db.ForeignKey('Spectacle.id')) #FK
    id_theater = db.Column(db.Integer, db.ForeignKey('Theater.id')) #FK
    date_time = db.Column(db.DateTime)

    #relationships
    reservation = db.relationship('Reservation', backref='screening')
    seat_reserved = db.relationship('SeatReserved', backref='screening')



class Reservation(db.Model):
    __tablename__ = 'Reservation'
    id = db.Column(db.Integer, primary_key=True)
    id_theater = db.Column(db.Integer, db.ForeignKey('Theater.id')) #FK
    id_screening = db.Column(db.Integer, db.ForeignKey('Screening.id')) #FK
    reservation_name = db.Column(db.Text)
    reservation_number = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    paid = db.Column(db.Boolean)

    #relationships
    seat_reserved = db.relationship('SeatReserved', backref='reservation')

class SeatReserved(db.Model):
    __tablename__ = 'SeatReserved'
    id = db.Column(db.Integer, primary_key=True)
    id_screening = db.Column(db.Integer, db.ForeignKey('Screening.id')) #FK
    id_reservation = db.Column(db.Integer, db.ForeignKey('Reservation.id')) #FK
    number = db.Column(db.Integer)
    row = db.Column(db.Integer)

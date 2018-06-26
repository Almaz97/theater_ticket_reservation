from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_modus import Modus
import psycopg2
from models import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime

app = Flask(__name__)
modus = Modus(app)
app.config['SECRET_KEY'] = 'this_should_be_a_secret'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'postgresql://almaz:Almaz@localhost/reservation'

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

admin = Admin(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/theater')
def theater():
    theaters = Theater.query.all()
    return render_template('theater.html', theaters=theaters)

@app.route('/theater/<int:id_t>')
def th(id_t):

    specs = Spectacle.query.filter_by(id_theater=id_t)
    return render_template('spectacles.html', specs=specs)

@app.route('/spectacle')
def spectacle():
    specs = Spectacle.query.all()
    return render_template('spectacle.html', specs=specs)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/reservation/<int:id_spec>', methods=['GET', 'POST'])
def reservation(id_spec):
    if request.method == 'POST':
        qset = Spectacle.query.filter_by(id=id_spec).first()
        theater_id = qset.id_theater
        cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        scr = Screening.query.filter((Screening.date_time>cur_time) & (Screening.id_spectacle==id_spec)).first()

        scr_id = scr.id_spectacle

        name = request.form.get('name')
        phone = request.form.get('phone')
        row = request.form.get('row')
        seat = request.form.get('seat')

        new_reservation = Reservation(
            id_theater=theater_id, id_screening=scr_id, reservation_name=name,
            reservation_number=phone, active=True, paid=False
        )

        db.session.add(new_reservation)
        db.session.commit()

        id_res = db.session.query(func.count(Reservation.id)).scalar()

        new_seat_reserved = SeatReserved(
            id_screening=scr_id, id_reservation=id_res, number=seat, row=row
        )

        db.session.add(new_seat_reserved)
        db.session.commit()

        return render_template('succed.html')

    info = Spectacle.query.filter_by(id=id_spec).first()
    date_info = Screening.query.filter_by(id_spectacle=id_spec).first()
    return render_template('reservation.html', info=info, date_info=date_info)

#Admin
admin.add_view(ModelView(Administrators, db.session))
admin.add_view(ModelView(Theater, db.session))
admin.add_view(ModelView(Auditorium, db.session))
admin.add_view(ModelView(Spectacle, db.session))
admin.add_view(ModelView(Screening, db.session))
admin.add_view(ModelView(Reservation, db.session))
admin.add_view(ModelView(SeatReserved, db.session))


if __name__ == '__main__':
    app.run(debug=True)

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle = db.Column(db.String)
    date = db.Column(db.Date)
    mileage = db.Column(db.Integer)
    litres = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    currency = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_uploaded = db.Column(db.DateTime(timezone=True), default=func.now())

    # def __init__(self, vehicle, date, mileage, litres, cost, currency):
    #     self.vehicle = vehicle
    #     self.date = date
    #     self.mileage = mileage
    #     self.litres = litres
    #     self.cost = cost
    #     self.currency = currency

    # def insert_record(self):
    #     table_input = "INSERT INTO tracker (vehicle, date, mileage, litres, cost, currency) VALUES (?,?,?,?,?,?)"
    #     inputs = [self.vehicle, self.date, self.mileage, self.litres, self.cost, self.currency]

    #     con = db_con()
    #     con.execute(table_input, inputs)
    #     con.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    records = db.relationship('Record')
    user_created = db.Column(db.DateTime(timezone=True), default=func.now())
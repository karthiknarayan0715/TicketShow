from flask_sqlalchemy import SQLAlchemy
from app import db
from app import bcrypt
import string, random

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)   
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String)
    email = db.Column(db.String, unique=True)

    def __init__(self, username, password, email, role):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
    def as_dict(self):
        d = {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
        d['registrations'] = []
        registrations = Registrations.query.filter_by(user_id = self.id).all()
        for r in registrations:
            cur_show = Shows.query.filter_by(id=r.show_id).first()
            if cur_show!=None:
                d['registrations'].append(cur_show.as_dict())

        return d

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    place = db.Column(db.String)
    location = db.Column(db.String)
    capacity = db.Column(db.Integer)

    def __init__(self, name, place, location, capacity):
        self.name = name
        self.place = place
        self.location = location
        self.capacity = capacity
    def as_dict(self):
        d = {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
        return d
    
class Screening(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"))
    show_id = db.Column(db.Integer, db.ForeignKey("show.id"))
    date = db.Column(db.String)
    time = db.Column(db.String)
    price = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)

    def __init__(self, venue_id, show_id, date, time, price):
        self.venue_id = venue_id
        self.show_id = show_id
        self.date = date
        self.time = time
        self.price = price
        venue = Venue.query.filter_by(id = venue_id).first()
        available = venue.capacity
        self.available = available
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
class Shows(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    duration = db.Column(db.Integer)
    rating = db.Column(db.String)

    def __init__(self, name, desc, duration, rating):
        self.name = name
        self.desc = desc
        self.duration = duration
        self.rating = rating
    def as_dict(self):
            d = {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
            return d

class Registrations(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id') )
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id') )
    quantity = db.Column(db.Integer)
    admitted = db.Column(db.Boolean)

    def __init__(self, user_id, show_id, quantity):
        self.user_id = user_id
        self.show_id = show_id
        self.quantity = quantity
        self.admitted = False

class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'))
    rating = db.Column(db.Integer)

    def __init__(self, user_id, show_id, rating):
        self.user_id = user_id
        self.show_id = show_id
        self.rating = rating
        
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    screening_id = db.Column(db.Integer, db.ForeignKey('screening.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quantity = db.Column(db.Integer, nullable = False)

db.create_all()

has_admin = Users.query.filter_by(role='admin').first()


#CREATING ADMIN USER IF NONE EXISTS!
if(not has_admin):
    admin_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    # print(f'THE ADMIN PASSWORD IS: {admin_password}')
    f = open('admin_password.txt', 'w+')
    f.write(admin_password)
    f.close()
    admin_user = Users('admin', bcrypt.generate_password_hash(admin_password), 'null', 'admin')

    db.session.add(admin_user)
    db.session.commit()
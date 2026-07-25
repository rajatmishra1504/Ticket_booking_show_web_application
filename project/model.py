from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(128))
    
    u_shows = db.relationship('Show', secondary='show_user', backref='users', cascade='all')
    u_venues = db.relationship('Venue', secondary='venue_user', backref='users', cascade='all')
    bookings = db.relationship('Booking', backref='user', lazy = True) 

    u_rate = db.relationship('Rate', uselist=False, backref='user')

    def __repr__(self):
        return f"<User {self.username}>"

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(128))

    shows = db.relationship("Show", backref="admin")
    venues = db.relationship("Venue", backref="admin")
    
   
    
    def __repr__(self):
        return f"<Admin {self.username}>"


class Venue(db.Model):
    v_id = db.Column(db.Integer(), primary_key = True)
    v_name = db.Column(db.String(50), nullable = False, unique = True)
    v_location = db.Column(db.String(120), nullable = False)
    v_capacity = db.Column(db.Integer(), nullable = False)
    
    v_shows = db.relationship('Show', secondary='show_venue', backref='venues', cascade='all')
    bookings = db.relationship('Booking', backref='venue', lazy = True, cascade='all, delete-orphan')

    v_admin_id = db.Column(db.Integer(), db.ForeignKey('admin.id'))

    def __repr__(self): 
        return f"<Venue {self.v_name}>"


class Show(db.Model):
    s_id = db.Column(db.Integer(), primary_key = True)
    s_name = db.Column(db.String(50), nullable = False)
    s_rating = db.Column(db.Float(), nullable = False)
    s_timing = db.Column(db.String(50), nullable = False)
    s_tags = db.Column(db.String(120), nullable = False)
    s_price = db.Column(db.Float(), nullable = False)
    s_director = db.Column(db.String(120), nullable = False)

    s_capacity = db.Column(db.Integer(), nullable = False)
    s_available_seats = db.Column(db.Integer(), nullable = False)
    
    s_admin_id = db.Column(db.Integer(), db.ForeignKey('admin.id'))
    bookings = db.relationship('Booking', backref='show', lazy = True, cascade='all, delete-orphan')

    s_rate = db.relationship('Rate', uselist=False, backref='show')
    #s_venues = db.relationship("Venue", secondary='show_venue', backref="shows")

    def __repr__(self):
        return f"<Show {self.s_name}>"


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.s_id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.v_id'), nullable=False)
    date = db.Column(db.DateTime, primary_key=True,nullable = False)


    def __repr__(self):
        return f"<Booking {self.id}>"

class Rate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.s_id'), nullable=False)
#__________________________________________________________________

#---------------------------ASSOCIATIONS---------------------------
#__________________________________________________________________

class show_venue(db.Model):
    venue_id = db.Column(db.Integer(), db.ForeignKey("venue.v_id"), primary_key = True)
    show_id = db.Column(db.Integer(), db.ForeignKey('show.s_id'), primary_key = True)


class show_user(db.Model):
    sh_id = db.Column(db.Integer, primary_key=True ) 
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key = True)
    show_id = db.Column(db.Integer(), db.ForeignKey('show.s_id'), primary_key = True)
    #booked_at = db.Column(db.DateTime, primary_key = True)


class venue_user(db.Model):
    ve_id = db.Column(db.Integer, primary_key=True )
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key = True)
    venue_id = db.Column(db.Integer(), db.ForeignKey('venue.v_id'), primary_key= True)
    #booked_at = db.Column(db.DateTime, primary_key = True)

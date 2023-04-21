from flask import Flask 
from market_name import db,bcrypt
from market_name import login_manager
from flask_login import UserMixin



class Admin_T(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    role=db.Column(db.String(120),nullable=False,default='admin')

    def __init__(self,id, username, password_hash, email_address,role):
        self.id=id
        self.username = username
        self.password_hash = password_hash
        self.email_address = email_address
        self.role=role

    
    @property
    def password(self):
        return self.password
    

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

   
class Theatre(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    location= db.Column(db.String(50), nullable=False)
    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location
        
    
class Show(db.Model):
     
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    srno= db.Column(db.db.Integer(), nullable=False)
    seatno = db.Column(db.db.Integer(), nullable=False)
    price=db.Column(db.db.Integer(), nullable=False)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'))
    theatres = db.relationship('Theatre', backref='show')
    def __init__(self, id, name, srno,seatno,theatre_id):
        self.id = id
        self.name = name
        self.srno = srno
        self.seatno=seatno
        self.theatre_id=theatre_id
        
    def buy(self, user):
        
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    role=db.Column(db.String(120),nullable=False,default='user')

    

    @property
    def password(self):
        return self.password


  
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    

class Booking(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    tname = db.Column(db.String(50), nullable=False)
    location= db.Column(db.String(50), nullable=False)
    cname = db.Column(db.String(50),nullable=False)
    srno= db.Column(db.db.Integer(), nullable=False)
    no_of_seats = db.Column(db.db.Integer(), nullable=False)
    date = db.Column(db.String(30), nullable=True)
    time=db.Column(db.String(50),nullable=False)
    price=db.Column(db.db.Integer(), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    booking_time= db.Column(db.String(30), nullable=True)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    theatres = db.relationship('Theatre', backref='booking')
    Users= db.relationship('User',backref='booking')
    
    
    def __init__(self, tname, location,cname,srno,no_of_seats,date,time,price,total_price,booking_time,theatre_id,user_id):
        self.tname = tname
        self.location= location
        self.cname = cname
        self.srno = srno
        self.no_of_seats=no_of_seats
        self.date=date
        self.time=time
        self.price=price
        self.booking_time=booking_time
        self.total_price=total_price
        self.theatre_id=theatre_id
        self.user_id=user_id

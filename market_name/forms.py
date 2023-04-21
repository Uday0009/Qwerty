from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField,validators,DateField,RadioField
import email_validator
from wtforms.validators import Length, EqualTo, Email, DataRequired,ValidationError
from market_name.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm1(FlaskForm):
    username1 = StringField(label='User Name:', validators=[DataRequired()])
    password1 = PasswordField(label='Password:', validators=[DataRequired()])
    submit1 = SubmitField(label='Sign in')

class LoginForm2(FlaskForm):
    username2 = StringField(label='User Name:', validators=[DataRequired()])
    password2 = PasswordField(label='Password:', validators=[DataRequired()])
    submit2 = SubmitField(label='Sign in')

class Book_Now(FlaskForm):
    no_of_seats= IntegerField(label='Select no. of seats',default=0, validators=[validators.InputRequired()])
    date = DateField('Select show date:', format='%d-%m-%Y')
    time = RadioField('Select show time:',choices=[('09:00 AM', '09:00 AM'),
                               ('12:00 PM', '12:00 PM'),
                               ('03:00 PM', '03:00 PM'),
                               ('06:00 PM', '06:00 PM'),
                               ('09:00 PM', '09:00 PM')])
    submit= SubmitField(label='Make Payment')



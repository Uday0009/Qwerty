from market_name import app,db
from flask import render_template, redirect, url_for, flash, request,session
from market_name.models import  User, Admin_T,Theatre,Show,Booking
from market_name.forms import RegisterForm, LoginForm1,LoginForm2,Book_Now
from flask_login import login_user, logout_user, login_required, current_user
from flask_security import roles_required
from datetime import datetime
import pytz

@app.route('/')
def hello_page():
    return render_template('home.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/movie',methods=['GET', 'POST'])
@login_required
def movie_page():
   theatre= Theatre.query.all()
   show=Show.query.all()
   return render_template('movie.html',  theatre= theatre,show=show)

@app.route('/show/<int:id>',methods=['GET', 'POST'])
@login_required
def show_page(id):
    theatre = Theatre.query.get(id)
    show = Show.query.filter(Show.theatre_id==id).all()
    return render_template('show.html',  theatre= theatre,show=show)


@app.route('/book_now/<int:id>',methods=['GET', 'POST'])
@login_required
def book_page(id):
    form=Book_Now()
    show = Show.query.get(id)
    theatre = Theatre.query.get(show.theatre_id)
    tc=0
    t_l=form.time.data
    now_utc = datetime.utcnow()
    ist_tz = pytz.timezone('Asia/Kolkata')
    now_ist = pytz.utc.localize(now_utc).astimezone(ist_tz)
    if request.method == 'POST':
        ns = int(request.form['no_of_seats'])
        d=request.form.get('date')
        
        ist=now_ist

        if ns>show.seatno:
            flash('Sorry! Booking cannot be done', category='danger')
        else:
            
            new_quantity = show.seatno- ns
            show.seatno = new_quantity
            db.session.commit()
            a=  ns* show.price
            tc=a 
            n=int(tc//show.price)
    
            db.session.commit()
            ticket = Booking(tname=theatre.name,location=theatre.location,cname=show.name,srno=show.srno,no_of_seats=n,date=d,
                            time=form.time.data,price=show.price,total_price=tc,booking_time=now_ist,theatre_id=show.theatre_id,user_id= current_user.id)
            db.session.add(ticket)
            db.session.commit()
            return redirect(url_for("complete_page",id=show.id,tc=tc,n=n,t_l=t_l,ist=ist))
        
    return render_template('book_now.html',  theatre= theatre,show=show,form=form,tc=tc)


@app.route('/register',methods=['GET', 'POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! Please login to continue", category='success')
        return redirect(url_for('login_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}',category='danger')

    return render_template('register.html',form=form)


@app.route('/complete/<int:id>',methods=['GET', 'POST'])

def complete_page(id):
    show = Show.query.get(id)
    a=request.args.get('tc')
    b=request.args.get('n')
    c=request.args.get('t_l')
    d=request.args.get('ist')
    theatre = Theatre.query.get(show.theatre_id) 
    return render_template('complete.html',theatre=theatre,show=show,a=a,b=b,c=c,d=d)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form1= LoginForm1()
    
    
    if form1.submit1.data and form1.validate():
        attempted_user = User.query.filter_by(username=form1.username1.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form1.password1.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
        
   

    return render_template('login.html', form1=form1)

@app.route('/al', methods=['GET', 'POST'])
def log_page():
    form2= LoginForm2()
    if form2.submit2.data and form2.validate():
        attempted_user = Admin_T.query.filter_by(username=form2.username2.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form2.password2.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            x=form2.username2.data
            return redirect(url_for('admin_fun',x=x))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('al.html', form2=form2)




@app.route('/admin')

def admin_fun():
    return redirect(url_for('admin.index'))
 

 


@app.route('/my-bookings')

def my_bookings():
    b = Booking.query.filter(Booking.user_id==current_user.id).all()
    booking = list(reversed(b))
    return render_template("booking.html", user=current_user,booking=booking)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))




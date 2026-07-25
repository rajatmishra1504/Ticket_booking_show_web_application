from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin


import uuid
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from flask_cors import CORS #CROS = Cross origin resource sharing
from model import * #Importing everything from models
from resources import *


# _______________--------CONFIGURATION---------____________--
# Initialize app
app = Flask(__name__)

# using secret_key for encrypting session cookie and for securing data in flask application
app.config['SECRET_KEY'] = 'onepieceisreal@363'

#setting URI for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///l.sqlite3"




# Intialising the SQLAlchemy object with flask app
db.init_app(app)
app.app_context().push()

#Intialisig the API object with flask app
CORS(app)
api.init_app(app)



login_manager = LoginManager()
# Initialising LoginManager with my Flask APP . So that Flask-loin will know which to app with
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

timestamp = datetime.datetime.now()

Date = timestamp.strftime('%d-%m-%y')




@app.before_first_request
def create_tables():
     db.create_all()





# ___________INDEX_PAGE ______________________________________________
@app.route('/')
def index():
    return render_template('index.html')

#____________------AUTHENTICATION SECTION -----------____________________

@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'GET':
        return render_template('userlogin.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username = username).first()
        
        if not user:
            flash('Invalid usernsme, pls try again')
            return redirect(url_for('userlogin'))
        else:
            if user.password == password :                
                login_user(user)
                return redirect(url_for('user_dashboard', username = username))
            else:
                flash("Invalid Password, Try again")
                return redirect(url_for('userlogin'))

        flash('Opps! Invalid username. Try Again')
        return redirect(url_for('index'))

    return render_template('userlogin.html')

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():

    if request.method == 'GET':
        return render_template('adminlogin.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password') 

        admin = Admin.query.filter_by(username = username).first()
        
        if not admin:
            flash('Invalid username, pls try again')
            return redirect(url_for('adminlogin'))
        else:
            if admin.password == password:
                login_user(admin)
                return redirect(url_for('admin_dashboard', username = username))
            else:
                flash("Invalid Password, Try again")
                return redirect(url_for('adminlogin'))
        
    return render_template('adminlogin.html')


@app.route('/usersignup', methods = ['GET','POST'])
def usersignup():

    if request.method == 'GET':
        return render_template('usersignup.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        u = User.query.filter_by(username = username).first()

        if u:
            flash('username already exist, please choose different username')
            return redirect(url_for('usersignup'))
        else:
            u1=User(username = username, password = password)
            db.session.add(u1)
            db.session.commit()
    return render_template('userlogin.html')

@app.route('/adminsignup', methods = ['GET', 'POST'])
def adminsignup():

    if request.method == 'GET':
        return render_template('adminsignup.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin = Admin.query.filter_by(username = username).first()

        if admin:
            flash('username already exist, please choose different username')
            return redirect(url_for('adminsignup'))
        else:
            a1=Admin(username = username, password = password)
            db.session.add(a1)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('adminlogin.html')



#___________---------ADMIN Dashboard route -----------______________

@app.route('/admin_dashboard/<string:username>')
def admin_dashboard(username):

    a = Admin.query.filter_by(username = str(username)).first()
    a_id = a.id

    venues_by_ad = Venue.query.filter_by(v_admin_id = a_id).all()
    return render_template("admin_dashboard.html", username = username, a_id = a_id, venues_by_ad = venues_by_ad)


#_______________---------------Each Admin's Venue Dashboard---------------____________________


@app.route('/admin_venue_dash/<int:a_id>/<int:id>', methods = ['GET', 'POST'])
def admin_venue_dash(a_id,id):
    a = Admin.query.get(a_id)
    a_username = a.username
    v1 = Venue.query.get(id)
    v_name = v1.v_name
    v_id = v1.v_id
    v_shows = v1.v_shows
    return render_template('admin_venue_dash.html',a_id = a_id,a_username = a_username, v_name = v_name, v_shows = v_shows, v_id = v_id)

@app.route('/logout')

def logout():
    logout_user()
    return redirect(url_for('index'))

# _____________------- LOGIN LOGOUT KHATAM -----_________________








#########################################################################________________________________________________________
#############################3###########################################______________------- VENUE MANAGEMENT --------__________________
#______________________________________________________________________________________________________________________________________



@app.route('/venue_add/<int:a_id>', methods = ['GET','POST'])

def venue_add(a_id):

    a = Admin.query.get(a_id)
    a_id = a.id
    a_username = a.username

    if request.method == 'GET':
        return render_template("venue_add.html", a_id = a_id, a_username = a.username)
    
    if request.method == 'POST':
        venue_name = request.form.get('venue_name')
        location = request.form.get('location')
        capacity = request.form.get('capacity')
        

        v = Venue.query.filter_by(v_name = venue_name, v_location = location).first()
        if v:
            flash('venue already exist, please enter new venue')
            return redirect(url_for('venue_add', a_id = a_id, a_username = a.username))
        else:
            v1=Venue(v_name = venue_name, v_location = location, v_capacity = capacity, v_admin_id = a_id)
            db.session.add(v1)
            db.session.commit()
            return redirect(url_for('admin_dashboard', username = a_username))
    return render_template("venue_add.html", a_id =a_id, a_username = a.username)  




@app.route('/venue_update/<int:a_id>/<int:id>', methods = ['GET','POST'])

def venue_update(a_id,id):

    a = Admin.query.get(a_id)
    a_id = a.id
    a_username = a.username

    v = Venue.query.get(int(id))

    if request.method == 'GET':
        return render_template("venue_update.html", a_id = a_id, id = id, username = a_username)

    if request.method == 'POST':
        
        venue_name = request.form.get('venue_name')
        location = request.form.get('location')
        capacity = request.form.get('capacity')
        v.v_name = venue_name
        v.v_location = location
        v.v_capacity = capacity
        
        v.v_admin_id = a_id
        db.session.commit()
        return redirect(url_for('admin_dashboard', username = a_username))
    return render_template("venue_update.html", a_id = a_id, id = id, username = a_username)  


@app.route('/venue_delete/<int:a_id>/<int:id>', methods = ['GET'])

def venue_delete(a_id,id):
    a = Admin.query.get(a_id)
    a_id = a.id
    a_username = a.username
    v = Venue.query.get(int(id))
    db.session.delete(v)
    db.session.commit()
    return redirect(url_for('admin_dashboard', username = a_username))    




#__________________________________________________________________________________________________
#____________---------- SHOW MANAGEMENT ---------------__________________
#__________________________________________________________________________________________________


@app.route('/show_add/<int:a_id>/<v_name>', methods = ['GET','POST'])

def show_add(a_id,v_name):

    a = Admin.query.get(a_id)
    a_id = a.id
    a_username = a.username

    v = Venue.query.filter_by(v_name = v_name).first()

    v_id = v.v_id
    v_name = v.v_name
    v_capacity = v.v_capacity
    v_s = v.v_shows

    if request.method == 'GET':
        return render_template("show_add.html", a_id =a_id, a_username = a.username, v_name = v_name, id = v_id )
    
    if request.method == 'POST':
        show_name = request.form.get('show_name')
        rating = int(0)
        timing = request.form.get('timing')
        tag = request.form.get('tag')
        price = request.form.get('price')
        director = request.form.get('director')
        s_capacity = v_capacity
        s_available_seats = request.form.get('available_seats')

        if int(s_capacity)<=0 or int(s_available_seats)<=0:
            flash('Please Enter Valid Credentials')
            return redirect(url_for('show_add', a_id =a_id, a_username = a.username, v_name = v_name, id = v_id ))

        elif int(s_available_seats) > int(s_capacity) :
            flash('Assigned available seat exceeds the venue capacity. Try Again ')
            return redirect(url_for('show_add', a_id =a_id, a_username = a.username, v_name = v_name, id = v_id ))
        else:
            s = Show.query.filter_by(s_name = show_name).first()
            if s : 
                if s in v_s:
                    if s.s_timing == timing:
                        flash('This show is already Screening here at this timing at this venue')
                        return redirect(url_for('show_add', a_id =a_id, a_username = a.username, v_name = v_name, id = v_id ))
                    else:
                        
                        s1=Show(s_name = show_name, s_rating = rating,s_timing = timing, s_tags = tag, s_price = price, s_director = director,s_capacity = s_capacity, s_available_seats = s_available_seats, s_admin_id = a_id)
                        db.session.add(s1)
                        db.session.commit()
                        v.v_shows.append(s1)
                        db.session.commit()
                        return redirect(url_for('admin_venue_dash', a_id = a_id, id = v_id))
            

                else:
                    s1=Show(s_name = show_name, s_rating = rating,s_timing = timing, s_tags = tag, s_price = price, s_director = director,s_capacity = s_capacity, s_available_seats = s_available_seats, s_admin_id = a_id)
                    db.session.add(s1)
                    db.session.commit()
                    v.v_shows.append(s1)
                    db.session.commit()
                    return redirect(url_for('admin_venue_dash', a_id = a_id, id = v_id))
            
            else:
                s1=Show(s_name = show_name, s_rating = rating,s_timing = timing, s_tags = tag, s_price = price, s_director = director,s_capacity = s_capacity, s_available_seats = s_available_seats, s_admin_id = a_id)
                db.session.add(s1)
                db.session.commit()
                v.v_shows.append(s1)
                db.session.commit()
                return redirect(url_for('admin_venue_dash', a_id = a_id, id = v_id))
    return render_template("show_add.html", a_id =a_id, a_username = a.username, v_name = v_name , id = v_id) 



@app.route('/show_update/<int:a_id>/<int:v_id>/<int:s_id>', methods = ['GET','POST'])

def show_update(a_id,v_id,s_id):

    a = Admin.query.get(a_id)
    a_id = a.id
    a_username = a.username
    v = Venue.query.get(v_id)
    v_id = v.v_id
    s = Show.query.get(s_id)


    if request.method == 'GET':
        return render_template("show_update.html", a_id =a_id,v_id = v_id , s_id = s_id)
    
    if request.method == 'POST':
        show_name = request.form.get('show_name')
        rating = request.form.get('rating')
        tag = request.form.get('tag')
        price = request.form.get('price')
        director = request.form.get('director')
        

        s.s_name = show_name
        #s.s_rating = rating
        s.s_tags = tag
        s.s_price = price
        s.s_director = director

        db.session.commit()
        return redirect(url_for('admin_venue_dash', a_id = a_id, id = v_id))
    return render_template("show_update.html", a_id =a_id, v_id = v_id, s_id = s_id) 


@app.route('/show_delete/<int:a_id>/<int:v_id>/<int:s_id>', methods = ['GET'])

def show_delete(a_id,v_id,s_id):
    a = Admin.query.get(a_id)
    a_id = a.id
    a_username = a.username
    s = Show.query.get(int(s_id))
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for('admin_venue_dash', a_id = a_id, id = v_id))   






#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#***************************** USER SECTION*********************************************************************************

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




#___________________________________________________________________________________________________________________
#___________---------USER Dashboard route -----------______________

@app.route('/user_dashboard/<string:username>')

def user_dashboard(username):
    u = User.query.filter_by(username = username).first()
    u_id = u.id
    s_list=Show.query.all()
    return render_template("user_dashboard.html", u_id = u_id,u_name = username, s_list = s_list, Date = Date)


#_____________------------ SHOW BOOKING --------------_______________________

@app.route("/show_booking/<int:u_id>/<int:s_id>/<int:v_id>", methods = ['GET', 'POST'])
def show_booking(u_id,s_id,v_id):
    u = User.query.filter_by(id = u_id).first()
    u_name = u.username

    s = Show.query.filter_by(s_id = s_id).first()
    s_name = s.s_name
    s_price = s.s_price
    s_timing = s.s_timing
    s_available_seats = s.s_available_seats


    v = Venue.query.filter_by(v_id = v_id).first()
    v_name = v.v_name
    v_capacity = v.v_capacity
    

    if request.method == 'GET':
        return render_template('show_booking.html',u_id = u_id, u_name = u_name, s_id = s_id, s_name = s_name,s_price = s_price, s_timing = s_timing, v_id = v_id, v_name = v_name, s_available_seats = s_available_seats, Date = Date)

    if request.method == 'POST':
        
        n = request.form.get('ticket')
        n = int(n)
        if int(n) > int(s_available_seats):
            flash("Can't book more than available seats 😶‍🌫️, Try again ")
            return redirect(url_for('show_booking', u_id = u_id, s_id = s_id, v_id = v_id))
        else:
            Total_price = int(s_price) * int(n)

            return redirect(url_for('show_final_book', u_id = u_id, s_id = s_id, v_id = v_id, n = n, t = Total_price))

        
    return render_template('show_booking.html',u_id = u_id, u_name = u_name, s_id = s_id, s_name = s_name,s_price = s_price, s_timing = s_timing, v_id = v_id, v_name = v_name, s_available_seats = s_available_seats, Date = Date)








@app.route("/show_final_book/<int:u_id>/<int:s_id>/<int:v_id>/<int:n>/<int:t>", methods = ['GET', 'POST'])
def show_final_book(u_id,s_id,v_id,n,t):
    u = User.query.filter_by(id = u_id).first()
    u_name = u.username

    s = Show.query.filter_by(s_id = s_id).first()
    s_name = s.s_name
    s_price = s.s_price
    s_timing = s.s_timing
    s_available_seats = s.s_available_seats


    v = Venue.query.filter_by(v_id = v_id).first()
    v_name = v.v_name
    v_capacity = v.v_capacity
    v_location = v.v_location
    

    return render_template('show_final_book.html', u_id = u_id, u_name = u_name, s_id = s_id, s_name = s_name,s_price = s_price, s_timing = s_timing, v_id = v_id, v_name = v_name, v_location = v_location, s_available_seats = s_available_seats, n = n, t = t, Date = Date)


@app.route("/booking_update/<int:u_id>/<int:s_id>/<int:v_id>/<int:n>", methods = ['GET', 'POST'])
def booking_update(u_id,s_id,v_id,n):
    u = User.query.filter_by(id = u_id).first()
    u_name = u.username

    s = Show.query.filter_by(s_id = s_id).first()
    s_name = s.s_name
    s_price = s.s_price
    s_timing = s.s_timing
    s_available_seats = s.s_available_seats   
    s_list=Show.query.all()
    x = s_available_seats - int(n)
    db.session.query(Show).filter_by(s_id=s_id).update({'s_available_seats': x})

    t = datetime.datetime.now()
    sh_id = str(uuid.uuid4())
    s_u = show_user(sh_id = sh_id, user_id = u_id, show_id = s_id)#,booked_at = t)
    db.session.add(s_u)
    db.session.commit()
    
    ve_id = str(uuid.uuid4())
    v_u = venue_user(ve_id = ve_id, user_id = u_id, venue_id = v_id)#, booked_at = t)
    db.session.add(v_u)
    db.session.commit()
    
    
    Date = t.strftime('%d-%m-%y')
    N_Date = datetime.datetime.strptime(Date, '%d-%m-%y')   
 
    for i in range(int(n)):
        id = str(uuid.uuid4())
        new_booking = Booking(id = id, user_id = u_id, show_id = s_id, venue_id = v_id, date = t)
        db.session.add(new_booking)
        db.session.commit()


    
    return redirect(url_for('user_dashboard', username = u_name))


    
@app.route('/bookings/<int:u_id>', methods = ['GET'])
def bookings(u_id):

    u = User.query.filter_by(id = u_id).first()
    u_name = u.username

    u_shows = u.u_shows
    u_venues = u.u_venues
    bookings = u.bookings
    
    return render_template('bookings.html', bookings = bookings , u_id = u_id , u_name = u_name, u_venues = u_venues, u_shows = u_shows )




@app.route('/rate/<int:u_id>/<int:s_id>', methods = ['GET', 'POST'])
def rating(u_id,s_id):
    u = User.query.filter_by(id = u_id).first()
    u_name = u.username

    s = Show.query.filter_by(s_id = s_id).first()
    
    sn = s.s_name
    sd = s.s_director

    # now i have to update the rating of a show of same name  but different s_id simultaneously. 
    # list of show which are actually same but are registered with different attributes but show with same name and same director represents same show
    sl = Show.query.filter_by(s_name = sn, s_director = sd) 

    
    n = len(Rate.query.filter_by(show_id = s_id).all())


    if request.method == 'GET':
        return render_template("rate.html", u_id = u_id, s_id = s_id, username = u_name)
    
    if request.method == 'POST':
        rating = int(request.form.get('rating'))

        if int(rating) > 10 or int(rating) < 0 :

            flash('please rate between 0 to 10')
            return redirect(url_for('rate', u_id = u_id, s_id = s_id))
        else:
            if n == 0:
                s_rating = rating
                db.session.query(Show).filter_by(s_name = sn , s_director = sd).update({'s_rating': s_rating})
                r = Rate(rating = rating ,user_id = u_id,show_id = s_id)
                db.session.add(r)
                db.session.commit()

                return redirect(url_for('user_dashboard', username = u_name))

            else:
                #s_r = s.s_rating
                #new_rating = ((int(s.s_rating)*(n))+rating)//(n+2) #calculating  show's new rating
                #print(s_r)
                #print(s_r*n)
                #print((s_r*n)+rating)
                #print(((s_r*n)+rating)//(n+1))
                #print(s_rating)

                sh = db.session.query(Show).filter_by(s_name=sn, s_director=sd).all()
                for show in sh:
                    show.s_rating = ((int(s.s_rating)*(n))+rating)//(n+1)
                db.session.commit()
                


                #db.session.query(Show).filter_by(s_name = sn , s_director = sd).update({s_rating: (((int(s_r)*(n))+rating)//(n+2)) })
                #db.session.commit()
                #db.session.flush()

                r = Rate(rating = rating ,user_id = u_id, show_id = s_id )
                db.session.add(r)
                db.session.commit()
                #print(s_rating)

                return redirect(url_for('user_dashboard', username = u_name))
    return render_template("rate.html", username = u_name )

















##################################################################################################################
#------------------------------------------------ Venue Stats ----------------------------------------------------

@app.route('/venue_stats/<int:a_id>', methods = ['GET','POST'])

def venue_stats(a_id):

    

    a = Admin.query.get(a_id)
    a_id = a.id
    a_username = a.username
    
    v = a.venues

    x = []
    y = []
    b = [ ] # here i will store bookings per venue id 
    bk = [ ]
    for ven in v:
        x.append(ven.v_name)
        b.append(len(ven.bookings))
        y.append(len(ven.v_shows))
  

    fig = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    plt.bar(x, y, color ='maroon', width = 0.4)
    plt.xticks(x,x)
    plt.xlabel("venue names")
    plt.ylabel("No. of Shows")
    plt.title("shows vs venue ")
    
    
    plt.savefig('static/v_s_bar.png')

    plt.bar(x, b, color ='maroon', width = 0.4)
    plt.xticks(x,x)
    plt.xlabel("venue names")
    plt.ylabel("No. of bookings")
    plt.title("venue vs No. of Bookings")
    
    
    plt.savefig('static/v_b_bar.png')


    return render_template('v_stats.html', a_name = a_username)

###########################################--------------------------------------------------------------------------------------###############################3
#######------------ -----------------------------------------------------SHOW SUMMARY -------------------------------------------########

@app.route('/venue_show_stats/<int:a_id>/<int:v_id>', methods = ['GET','POST'])

def venue_show_stats(a_id,v_id):
    

    a = Admin.query.get(a_id)
    a_id = a.id
    a_name = a.username
    v = Venue.query.get(v_id)
    shows = v.v_shows
    s_g = ''
    
    genres = ["Action","Adventure","Comedy","Drama","Fantasy","Horror","Musical","Mystery","Romance","Sci-Fi","Thriller"]
    d = dict.fromkeys(genres,0)
    for s in shows:
        s_g = s.s_tags
        d[s_g] += 1

    x = list(d.keys())
    y = list(d.values())

    fig = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    plt.bar(x, y, color ='pink', width = 0.4)
    plt.xticks(x,x)
    plt.xlabel("Genres")
    plt.ylabel("No. of shows available at this venue")
    plt.title("venue's shows vs Genre ")
    
    plt.savefig('static/bar_s_g.png')

    # will find the no. of bookking of show at this venue
    l = db.session.query(Show.s_name,Show.s_director).distinct().all() # this gives me list of unique tuples of s_name and dir
    show_name = [] # list of unique shows which stores its name
    for name, director in l:
        show = Show.query.filter_by(s_name=name, s_director=director).first()
        show_name.append(show.s_name)

    v = Venue.query.get(v_id)
    shows = v.v_shows 
    s_n = [] # list of show on this venue with it's name 
    for i in shows:
        s_n.append(i.s_name)

    y=[]
    for s in show_name :
        if s not in s_n:
            show_name.remove(s)

    for i in show_name:
        s = Show.query.filter_by(s_name = i)
        y.append(len(s[0].bookings))

    # creating the bar plot
    fig = plt.figure(figsize = (10, 5))
    plt.bar(show_name, y, color ='pink', width = 0.4)
    plt.xticks(show_name,show_name)
    plt.xlabel("show_name")
    plt.ylabel("No. of Bookings at this venue")
    plt.title("Venue's shows vs Booking ")
    
    plt.savefig('static/bar_vs_b.png')


    
    



    return render_template('venue_show_stats.html', a_id = a_id, v_id = v_id, a_name = a_name )




@app.route('/show_all_stats/<string:a_username>', methods = ['GET','POST'])

def show_all_stats(a_username):


    l = db.session.query(Show.s_name,Show.s_director).distinct().all() # this gives me list of unique tuples of s_name and dir
    show_ids = []
    for name, director in l:
        show = Show.query.filter_by(s_name=name, s_director=director).first()
        show_ids.append(show.s_id)

    
    x = []
    y = []
    r = []
    for i in show_ids:
        s = Show.query.get(i)
        x.append(s.s_name)
        b=s.bookings
        y.append(len(b))
        r.append(s.s_rating)

    # creating the bar plot

    fig = plt.figure(figsize = (10, 5))       
    plt.bar(x, y, color ='violet', width = 0.4)
    plt.xticks(x,x)
    plt.xlabel("Show_names")
    plt.ylabel("Total no. of booking")
    plt.title("show vs Booking")
    
    plt.savefig('static/bar_s_b.png')

    # creating the bar plot
    
    fig = plt.figure(figsize = (10, 5))       
    plt.bar(x, r, color ='violet', width = 0.4)
    plt.xticks(x,x)
    plt.xlabel("Show_names")
    plt.ylabel("Rating")
    plt.title("show vs Rating")
    
    plt.savefig('static/bar_s_r.png')

    return render_template('show_all_stats.html', a_name = a_username)
####################################################################################################################
#---------------------------------------------------search-----------------------------------------------------------

@app.route('/search/<int:u_id>', methods=['POST'])
def search(u_id):
    u = User.query.get(u_id)
    u_name = u.username
    query = request.form['query']
    category = request.form['category']

    if category == 'show':
        s_list = Show.query.filter(Show.s_name.like(f"%{query}%")).all()
        return render_template('user_dashboard.html', u_id = u_id, u_name = u_name, s_list = s_list, Date = Date)
        
    elif category == 'venue':
        v = Venue.query.filter(Venue.v_name.like(f"%{query}%")).all()
        s_list = []
        for i in v:
            s_list = s_list + i.v_shows
        return render_template('user_dashboard.html', u_id = u_id, u_name = u_name, s_list = s_list, Date = Date)
    elif category == 'tags':
        s_list = Show.query.filter(Show.s_tags.like(f"%{query}%")).all()
        return render_template('user_dashboard.html', u_id = u_id, u_name = u_name, s_list = s_list, Date = Date)
    elif category == 'All_shows':
        s_list = show.query.all()
        return render_template('user_dashboard.html', u_id = u_id, u_name = u_name, s_list = s_list, Date = Date)
    
    
            
#############################################################################################################################################################################################
if __name__ == "__main__":
    app.run(debug = True)

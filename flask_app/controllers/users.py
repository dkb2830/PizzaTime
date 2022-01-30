from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.order import Order
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt
from werkzeug.datastructures import ImmutableMultiDict

# create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# List of US States
states_JSON = [{"name":"Alabama","abbreviation":"AL"},{"name":"Alaska","abbreviation":"AK"},{"name":"Arizona","abbreviation":"AZ"},{"name":"Arkansas","abbreviation":"AR"},{"name":"California","abbreviation":"CA"},{"name":"Colorado","abbreviation":"CO"},{"name":"Connecticut","abbreviation":"CT"},{"name":"Delaware","abbreviation":"DE"},{"name":"Florida","abbreviation":"FL"},{"name":"Georgia","abbreviation":"GA"},{"name":"Hawaii","abbreviation":"HI"},{"name":"Idaho","abbreviation":"ID"},{"name":"Illinois","abbreviation":"IL"},{"name":"Indiana","abbreviation":"IN"},{"name":"Iowa","abbreviation":"IA"},{"name":"Kansas","abbreviation":"KS"},{"name":"Kentucky","abbreviation":"KY"},{"name":"Louisiana","abbreviation":"LA"},{"name":"Maine","abbreviation":"ME"},{"name":"Maryland","abbreviation":"MD"},{"name":"Massachusetts","abbreviation":"MA"},{"name":"Michigan","abbreviation":"MI"},{"name":"Minnesota","abbreviation":"MN"},{"name":"Mississippi","abbreviation":"MS"},{"name":"Missouri","abbreviation":"MO"},{"name":"Montana","abbreviation":"MT"},{"name":"Nebraska","abbreviation":"NE"},{"name":"Nevada","abbreviation":"NV"},{"name":"New Hampshire","abbreviation":"NH"},{"name":"New Jersey","abbreviation":"NJ"},{"name":"New Mexico","abbreviation":"NM"},{"name":"New York","abbreviation":"NY"},{"name":"North Carolina","abbreviation":"NC"},{"name":"North Dakota","abbreviation":"ND"},{"name":"Ohio","abbreviation":"OH"},{"name":"Oklahoma","abbreviation":"OK"},{"name":"Oregon","abbreviation":"OR"},{"name":"Pennsylvania","abbreviation":"PA"},{"name":"Rhode Island","abbreviation":"RI"},{"name":"South Carolina","abbreviation":"SC"},{"name":"South Dakota","abbreviation":"SD"},{"name":"Tennessee","abbreviation":"TN"},{"name":"Texas","abbreviation":"TX"},{"name":"Utah","abbreviation":"UT"},{"name":"Vermont","abbreviation":"VT"},{"name":"Virginia","abbreviation":"VA"},{"name":"Washington","abbreviation":"WA"},{"name":"West Virginia","abbreviation":"WV"},{"name":"Wisconsin","abbreviation":"WI"},{"name":"Wyoming","abbreviation":"WY"}]

bcrypt = Bcrypt(app)

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/signup")
def signup():
    
    return render_template("signup.html",all_states = states_JSON)

@app.route('/signup/user',methods=["POST"])
def sign_up():
    data = { "email" : request.form['email']}
    user_with_email = User.get_by_email(data)
    if user_with_email:
        flash("Email is invalid or unable", "signup")
        return render_template("signup.html",all_states = states_JSON)

    if not validate_user(request.form):
        #form_info = request.form
        return render_template("signup.html",all_states = states_JSON)
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form['email'],
        "address": request.form['address'],
        "city": request.form['city'],
        "state": request.form['state'],
        "password": pw_hash
        
    }
    
    session['id'] = User.save(data)
    
    return redirect("/user/quick_options")

@app.route('/login/user',methods=['POST'])
def login():
    data = { "email": request.form['email']  }
    user = User.get_by_email(data)

    if not user:
        flash("Invalid Email/Password","login")
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password","login")
        return redirect("/")

    session['id'] = user.id

    return redirect("/user/quick_options")

@app.route('/user/quick_options')
def show_options():
    print(session['id'])
    data = {
        "id": session['id']
        
    }
    user = User.get_by_id(data)
    
    my_fave = []
    if user.favorite_order != '':
        data = {
            "id":user.favorite_order
        }
    favorite_order = User.get_favorite_order(data)
    my_fave.append(favorite_order)
    return render_template("/user/quick_options.html",favorite_order = my_fave)

@app.route('/user/order')
def your_order():
    print(session['id'])
    data = {
        "id": session['id']
        
    }
    user = User.get_by_id(data)
    
    my_fave = []
    if user.favorite_order != '':
        data = {
            "id":user.favorite_order
        }
    favorite_order = User.get_favorite_order(data)
    my_fave.append(favorite_order)
    return render_template("/user/your_order.html",favorite_order = my_fave)

@app.route('/user/account')
def update_account():
    print(session['id'])
    data = {
        "id": session['id']
        
    }
    user = User.get_by_id(data)
    
    my_fave = []
    if user.favorite_order != '':
        data = {
            "id":user.favorite_order
        }
    favorite_order = User.get_favorite_order(data)
    my_fave.append(favorite_order)
    return render_template("/user/account_info.html",favorite_order = my_fave)


@app.route('/logout')
def close_sessions():
    session.clear()
    return render_template("index.html")

def validate_user( user ):
        is_valid = True
        # test whether a field matches the pattern
        if len(user['fname']) < 1 or user['fname'].isspace():
            flash("First name is blank","signup")
            is_valid = False
        
        if len(user['lname']) < 1 or user['lname'].isspace():
            flash("Last name is blank","signup")
            is_valid = False
        
        if len(user['address']) < 1 or user['address'].isspace():
            flash("Address is blank","signup")
            is_valid = False
        
        if len(user['city']) < 1 or user['city'].isspace():
            flash("City is blank","signup")
            is_valid = False
        
        if len(user['state']) < 1 or user['state'].isspace():
            flash("State is blank","signup")
            is_valid = False
        
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!","signup")
            is_valid = False

        if len(user['password']) < 8 or user['password'].isspace():
            flash("Password must be at least 8 characters","signup")
            is_valid = False

        caps_in_pw = re.findall("[A-Z]",user['password'])
        nums_in_pw = re.findall("[0-9]",user['password'])
        if len(caps_in_pw) < 0 or len(nums_in_pw) < 0:
            flash("Password requires at least one capital letter and at least one number","signup")
            is_valid = False

        if len(user['confirmpassword']) < 1 or user['confirmpassword'].isspace():
            flash("Confirm Password is blank","signup")
            is_valid = False

        if user['password'] != user['confirmpassword']:
            flash("Passwords do not match","signup")
            is_valid = False

        return is_valid

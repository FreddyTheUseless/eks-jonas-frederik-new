# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..models.UsersModel import Users
from .. import db

auth = Blueprint('auth', __name__)

# Login

@auth.route('/login')
def login():
    title = "Login"
    return render_template('login.html', title=title)

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = Users.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 


    login_user(user)
    return redirect(url_for('main.index'))

# Register

@auth.route('/register')
def register():
    title = "Register"
    return render_template('register.html', title=title)

@auth.route('/register', methods=['POST'])
def register_post():

    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    passwordconfirm = request.form.get('passwordconfirm')
    role = request.form.get('role')
    firstname = request.form.get('firstname')
    surname = request.form.get('surname')



     # check if someone already register with the email
    user = Users.query.filter_by(username=username).first()
    if not user:
        # the email doesnt exist
        if(username == ""):
            flash('Please Type a Username')
            return redirect(url_for('auth.register', email=email, firstname=firstname, surname=surname, password=password))

        pass
    else:
        # the email exists
        flash('User already exists. Please use another username')
        return redirect(url_for('auth.register', email=email, firstname=firstname, surname=surname, password=password))

    if(firstname == ""):
        flash('Please Type a firstname')
        return redirect(url_for('auth.register', email=email, username=username, firstname=firstname, surname=surname, password=password))


    if(surname == ""):
        flash('Please Type a surname')
        return redirect(url_for('auth.register', email=email, username=username, firstname=firstname, surname=surname, password=password))


# check if someone already register with the email
    emails = Users.query.filter_by(email=email).first()
    if not emails:
        # the email doesnt exist
        if(emails == ""):
            flash('Please Type an Email')
            return redirect(url_for('auth.register', username=username, firstname=firstname, surname=surname, password=password))
        pass
    else:
        # the email exists
        flash('Email already exists. Please log in instead')
        return redirect(url_for('auth.register', username=username, firstname=firstname, surname=surname, password=password))
    

    if(password == ""):
        flash('Please Type a Password')
        return redirect(url_for('auth.register', email=email, username=username, firstname=firstname, surname=surname, password=password))

    
    if(password != passwordconfirm):
        flash('Password do not match')
        return redirect(url_for('auth.register', email=email, username=username, firstname=firstname, surname=surname, password=password))

    
    if(role == ""):
        flash('Please select account type')
        return redirect(url_for('auth.register', email=email, username=username, firstname=firstname, surname=surname, password=password))



   


    new_user = Users(email=email, username=username, password=generate_password_hash(password, method='sha256'), role=role, firstname=firstname, surname=surname)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

# Profile username

@auth.route('/profile/username')
@login_required
def profile_username():
    title = "Profile Username Update"
    return render_template('profile/username.html', title=title, username=current_user.username)

@auth.route('/profile/username', methods=['POST'])
@login_required
def profile_username_post():
    username = request.form.get('username')

    user = Users.query.filter_by(id=current_user.id).first()

    # update database
    user.username = username
    db.session.commit()

    return redirect(url_for('main.profile'))

# Profile email

@auth.route('/profile/email')
@login_required
def profile_email():
    title = "Profile Email Update"
    return render_template('profile/email.html', title=title, email=current_user.email, username=current_user.username)

@auth.route('/profile/email', methods=['POST'])
@login_required
def profile_email_post():
    email = request.form.get('email')

    email_taken = Users.query.filter_by(email=email).first()

    if email_taken:
        flash('User already exists')
        return redirect(url_for('main.profile'))

    user = Users.query.filter_by(id=current_user.id).first()

    # update database
    user.email = email
    db.session.commit()

    return redirect(url_for('main.profile'))

# Profile password

@auth.route('/profile/password')
@login_required
def profile_password():
    title = "Profile Password Update"
    return render_template('profile/password.html', title=title, username=current_user.username)

@auth.route('/profile/password', methods=['POST'])
@login_required
def profile_password_post():
    password = request.form.get('password')
    passwordconfirm = request.form.get('passwordconfirm')

    if(password != passwordconfirm):
        flash('Password do not match')
        return redirect(url_for('auth.profile_password'))

    user = Users.query.filter_by(id=current_user.id).first()

    # update database
    user.password = generate_password_hash(password, method='sha256')
    db.session.commit()

    return redirect(url_for('main.profile'))

# Logout

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
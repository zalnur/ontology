from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login.utils import login_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .import db
from flask_login import login_required, logout_user, current_user
from .forms import EditProfileForm

#from owlready2 import *
#onto = get_ontology("medicineOntology.owl").load()
from flask import Flask, url_for

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Log in success', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, pleaser try again.', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if  request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        icNumber = request.form.get('icNumber')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email already exist', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(first_name) < 2:
            flash('First Name  must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1)< 7:
            flash('Password must be greater than 7 characters', category='error')
        else:
            new_user = User(email=email, first_name=first_name, icNumber=icNumber,  password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))
    
    return render_template("signup.html", user=current_user)  


@auth.route('/profilepage', methods=['GET', 'POST'])
@login_required
def profilepage():
    return render_template("profilepage.html", user=user)



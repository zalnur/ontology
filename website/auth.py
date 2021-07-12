from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login.utils import login_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .import db
from flask_login import login_required, logout_user, current_user
from .forms import EditProfileForm

from owlready2 import *
onto = get_ontology("medicineOntology.owl").load()
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


    #email = request.form.get('email')
   #first_name = request.form.get('firstName')
    #icNumber = request.form.get('icNumber')
   # user = User.query.filter_by(email=email).first()
    #user = User.query.filter_by(first_name=firstName).first()
   # user = User.query.filter_by(icNumber=icNumber).first()
    
    return render_template("profilepage.html", user=user)

@auth.route('/edit-profile', methods=['GET','POST'])
@login_required
def edit_profile():

    
    form = EditProfileForm() 

    if form.validate_on_submit(): 
        current_user.username = orm.username.data
        current_user.about_me = form.about_me.data
        
        db.session.commit() 
        flash('Your profile has been updated.') 
        return redirect(url_for('edit_profile', username=current_user.username))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    form.firstName.data = current_user.firstName
  
    return render_template("edit_profile.html",title='Edit Profile', form=form)


@auth.route('/medicine', methods=['GET', 'POST'])
@login_required
def medicinepage():

    #for Class in Class.subclasses():
     #   url_for("views.medicine", iri = Class.IRI), Class.name
     #   print(Class)

    html = """<html><body>"""
    html += """<h2> '%s' ontology </h2>""" %onto.base_iri 
    html += """<h3>Root classes</h3>"""
    for Class in Thing.subclasses():
        html += """ <p><a href="%s">%s</a></p>""" % (url_for("class_page", iri=Class.iri), Class.name)  
    html += """</body></html>""" 
    return html


  #  return render_template("medicine.html", user=current_user)


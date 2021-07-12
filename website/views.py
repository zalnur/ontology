from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import User

from .import db 
import json

views = Blueprint('views', __name__)

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    
    return render_template("home.html", user=current_user)

@views.route('/medicine', methods=['GET', 'POST'])
@login_required
def medicine():
    
    return render_template("medicine.html", user=current_user)






 


    
import os
from .import db 
from .models import User
from . import utils

from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import *
from collections import defaultdict

views = Blueprint('views', __name__)



@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    
    return render_template("home.html", user=current_user)

@views.route('/medicine', methods=['GET', 'POST'])
@login_required
def medicine():  

    gsparql = Graph()
    gsparql.parse(os.path.join(os.path.abspath(os.path.curdir) ,"medicineOntologyRDF.owl")) # load ontology on page load

    # if a new search query has been submitted
    if request.method == "POST":
        singleM = URIRef("http://www.semanticweb.org/hpuser/ontologies/2021/5/medicineOntology#{}".format(request.form.get('mcode')))

        rows = []

        # Search for medicine code queried in ontology  
        for row in utils.sparqlPerform(gsparql, "owl:sameAs", None, True):
            if row[0] == singleM or row[1] == singleM:
                rows.append(row)

        originalMedicine = defaultdict(list)
        originalMedicine = utils.generateData(originalMedicine, gsparql, singleM)
        print(originalMedicine)
        # {'M01AE01000T100108': ['GLAXOSMITHKLINE_CONSUMER_HEALTHCARE_SDN._BHD.', 'Ibuprofen_200_mg_Tablet', 'MAL19962557_A']})

        # Retrieve medicines similar to the medicine queried
        sameAsList = defaultdict(list)
        for codes in rows: 
            sameAsList = utils.generateData(sameAsList, gsparql, singleM, codes)
            # first run {'M01AE01000T100106': ['PHARMANIAGA_MANUFACTURING_BERHAD', 'Ibuprofen_200_mg_Tablet', 'MAL20014523_A']})
            #second run {'M01AE01000T100106': ['PHARMANIAGA_MANUFACTURING_BERHAD', 'Ibuprofen_200_mg_Tablet', 'MAL20014523_A'], 'M01AE01000T100114': ['STERLING_DRUG_(MALAYA)_SDN._BHD.', 'Ibuprofen_200_mg_Tablet', 'MAL20012745_ACE']}
            print(sameAsList)

        return render_template("medicine.html", user=current_user, sameAs=sameAsList, original=originalMedicine)

    return render_template("medicine.html", user=current_user, sameAs=defaultdict(list), original=defaultdict(list))

 


    
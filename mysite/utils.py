from collections import defaultdict
from rdflib.namespace import *

def sparqlPerform(graph, predicate, mcode, incSubject=False):
    if incSubject:
        return  graph.query("""
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX owl: <http://www.w3.org/2002/07/owl#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                        PREFIX medo: <http://www.semanticweb.org/hpuser/ontologies/2021/5/medicineOntology#> 
                        SELECT ?subject ?object 
                            WHERE {
                                ?subject %s ?object
                            }
                        """ % predicate)
    else:
        return  graph.query("""
                            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX owl: <http://www.w3.org/2002/07/owl#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                            PREFIX medo: <http://www.semanticweb.org/hpuser/ontologies/2021/5/medicineOntology#> 
                            SELECT ?object 
                                WHERE {
                                    %s %s ?object
                                }
                            """ % (mcode, predicate))

def generateData(listdict, graph, origin, mcodeList=None):

    if mcodeList is None:
        mcode=origin
    elif mcodeList[0] == origin:
        mcode=mcodeList[1]
    elif mcodeList[1] == origin:
        mcode=mcodeList[0]

    for row in sparqlPerform(graph, "medo:hasCompanyName", "<"+mcode+">"):
        listdict[mcode[69:]].append(row[0][69:])

    for row in sparqlPerform(graph, "medo:hasChemicalEntityValue", "<"+mcode+">"):
        listdict[mcode[69:]].append(row[0][69:])
    
    for row in sparqlPerform(graph, "medo:hasMALNumber", "<"+mcode+">"):
        listdict[mcode[69:]].append(row[0][69:])

    return listdict
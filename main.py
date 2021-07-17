from unicodedata import name
from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import *
import re
import sys
from collections import defaultdict

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

def generateData(graph, mcode):
    
    sameASList = defaultdict(list)

    for row in sparqlPerform(graph, "medo:hasCompanyName", "<"+mcode+">"):
        sameASList[mcode[69:]].append(row[0][69:])

    for row in sparqlPerform(graph, "medo:hasChemicalEntityValue", "<"+mcode+">"):
        sameASList[mcode[69:]].append(row[0][69:])
    
    for row in sparqlPerform(graph, "medo:hasMALNumber", "<"+mcode+">"):
        sameASList[mcode[69:]].append(row[0][69:])

    return sameASList

def main():
    g = Graph()
    g.load("medicineOntologyRDF.owl")

    gsparql = Graph()
    gsparql.parse("medicineOntologyRDF.owl")

    newnamespace = URIRef("http://www.w3.org/2002/07/owl#NamedIndividual")
    # print(newnamespace)

    singleM = URIRef("http://www.semanticweb.org/hpuser/ontologies/2021/5/medicineOntology#{}".format(sys.argv[1]))

    rows = []
    # print("{},{},{}".format("Item", "Class", "Type"))
    # for s, p, o in g.triples((None, RDF.type, newnamespace)):
    #     print("{},{},{}".format(s, o, p))
    
    # for s, p, o in g.triples((singleMAL, RDF.type, None)):
    #     if o == newnamespace:
    #         print("iterating over ", o)
    #     else:
    #         print(s, o)

    # for s, o in g.subjects_objects(RDFS):
    #     print(o)
    
    for row in sparqlPerform(gsparql, "owl:sameAs", None, True):
        if row[0] == singleM or row[1] == singleM:
            rows.append(row)
            print("{:>10} is the same as {:>10}".format(row[0][69:], row[1][69:]))

    print(rows[0], "\n\n", rows[1])

    originalMedicine = generateData(gsparql, row[0])
    print(originalMedicine)

    x=1
    sameASList = defaultdict(list)
    for code in rows: 
        
        for row in sparqlPerform(gsparql, "medo:hasCompanyName", "<"+code[x]+">"):
            sameASList[code[x][69:]].append(row[0][69:])

        for row in sparqlPerform(gsparql, "medo:hasChemicalEntityValue", "<"+code[x]+">"):
            sameASList[code[x][69:]].append(row[0][69:])
        
        for row in sparqlPerform(gsparql, "medo:hasMALNumber", "<"+code[x]+">"):
            sameASList[code[x][69:]].append(row[0][69:])
        if x == 0:
            break
        x-=1

    print(sameASList)
    # for stmt in g:
    #     pprint.pprint(stmt)
        
    
    

if __name__ == '__main__':
    main()
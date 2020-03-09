from rdflib import Graph, Literal, BNode, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, RDFS, XSD

import csv

g = Graph()

# define namespaces
ex = Namespace("http://example.org/")
exdata = Namespace("http://example.org/data#")

g.add( (ex.University, RDF.type, RDFS.Class) )
g.add( (ex.University, RDFS.subClassOf, FOAF.organization) )
g.add( (ex.University, RDFS.label, Literal("University", lang="en")) )
g.add( (ex.University, RDFS.comment, Literal("Organization at which the students go to")) )

g.add( (ex.Course, RDF.type, RDFS.Class) )
g.add( (ex.Course, RDFS.label, Literal("Course", lang="en")) )
g.add( (ex.Course, RDFS.comment, Literal("Course is offered at a university_data towards the granting of an approved degree")) )
g.add( (ex.Course, FOAF.name, XSD.string) )
g.add( (ex.Course, ex.hasSubject, XSD.string) )
g.add( (ex.Course, ex.hasNumber, XSD.integer) )
g.add( (ex.Course, ex.hasDescription, XSD.string) )
g.add( (ex.Course, RDFS.seeAlso, XSD.anyURI) )
g.add( (ex.Course, ex.hasTopic, ex.Topic) )

g.add( (ex.Topic, RDF.type, RDFS.Class) )
g.add( (ex.Topic, RDFS.label, Literal("Topic", lang="en")) )
g.add( (ex.Topic, RDFS.comment, Literal("Topic is part of a course material")) )
g.add( (ex.Topic, FOAF.name, XSD.string) )
g.add( (ex.Topic, RDFS.seeAlso, XSD.anyURI) )

g.add( (ex.Student, RDF.type, RDFS.Class) )
g.add( (ex.Student, RDFS.subClassOf, FOAF.person) )
g.add( (ex.Student, RDFS.label, Literal("Student", lang="en")) )
g.add( (ex.Student, RDFS.comment, Literal("Person who studies at a university_data")) )
g.add( (ex.Student, FOAF.name, XSD.string) )
g.add( (ex.Student, ex.hasID, XSD.integer) )
g.add( (ex.Student, FOAF.mbox, XSD.string) )
g.add( (ex.Student, ex.hasCompleted, ex.Course) )

g.add( (ex.hasSubject, RDF.type, RDF.Property) )
g.add( (ex.hasSubject, RDFS.label, Literal("hasSubject", lang="en")) )
g.add( (ex.hasSubject, RDFS.comment, Literal("Course has a subject")) )
g.add( (ex.hasSubject, RDFS.domain, ex.Course) )
g.add( (ex.hasSubject, RDFS.range, XSD.string) )

g.add( (ex.hasNumber, RDF.type, RDF.Property) )
g.add( (ex.hasNumber, RDFS.label, Literal("hasNumber", lang="en")) )
g.add( (ex.hasNumber, RDFS.comment, Literal("Course has a number")) )
g.add( (ex.hasNumber, RDFS.domain, ex.Course) )
g.add( (ex.hasNumber, RDFS.range, XSD.integer) )

g.add( (ex.hasDescription, RDF.type, RDF.Property) )
g.add( (ex.hasDescription, RDFS.label, Literal("hasDescription", lang="en")) )
g.add( (ex.hasDescription, RDFS.comment, Literal("Course has a description")) )
g.add( (ex.hasDescription, RDFS.domain, ex.Course) )
g.add( (ex.hasDescription, RDFS.range, XSD.string) )

g.add( (ex.hasID, RDF.type, RDF.Property) )
g.add( (ex.hasID, RDFS.label, Literal("hasID", lang="en")) )
g.add( (ex.hasID, RDFS.comment, Literal("Student has an ID number")) )
g.add( (ex.hasID, RDFS.domain, ex.Student) )
g.add( (ex.hasID, RDFS.range, XSD.integer) )

g.add( (ex.hasTopic, RDF.type, RDF.Property) )
g.add( (ex.hasTopic, RDFS.label, Literal("hasTopic", lang="en")) )
g.add( (ex.hasTopic, RDFS.comment, Literal("Course has a topic")) )
g.add( (ex.hasTopic, RDFS.domain, ex.Course) )
g.add( (ex.hasTopic, RDFS.range, ex.Topic) )

g.add( (ex.hasCompleted, RDF.type, RDF.Property) )
g.add( (ex.hasCompleted, RDFS.label, Literal("hasCompleted", lang="en")) )
g.add( (ex.hasCompleted, RDFS.comment, Literal("Student has completed a course")) )
g.add( (ex.hasCompleted, RDFS.domain, ex.Student) )
g.add( (ex.hasCompleted, RDFS.range, ex.Course) )

g.add( (ex.hasGrade, RDF.type, RDF.Property) )
g.add( (ex.hasGrade, RDFS.subPropertyOf, ex.hasCompleted) )
g.add( (ex.hasGrade, RDFS.label, Literal("hasGrade", lang="en")) )
g.add( (ex.hasGrade, RDFS.comment, Literal("Student has a grade for a completed course")) )
g.add( (ex.hasGrade, RDFS.domain, ex.hasCompleted) )
g.add( (ex.hasGrade, RDFS.range, XSD.string ) )
#
# # processing university_data data into RDF triples
with open("university_data") as data:
    file = csv.reader(data, delimiter=',')
    for row in file:
        university = URIRef(exdata + row[0].replace(" ", "_")) # define university URI using first column
        link = URIRef(row[1]) # define link URI to university's entry in dbpedia using second column

        g.add( (university, RDF.type, ex.University) )
        g.add( (university, FOAF.name, Literal(row[0])) )
        g.add( (university, RDFS.seeAlso, link) )

# processing course data into RDF triples
with open("course_data") as data:
    file = csv.reader(data, delimiter=',')
    for row in file:
        course = URIRef(exdata + row[0].replace(" ", "_")) # define course URI using first column
        link = URIRef(row[3]) # define link URI to online source of course

        g.add( (course, RDF.type, ex.Course) )
        g.add( (course, FOAF.name, Literal(row[0])) )
        g.add( (course, ex.hasSubject, Literal(row[1])) )
        g.add( (course, ex.hasNumber, Literal(row[2])) )
        g.add( (course, RDFS.seeAlso, link) )

# processing student data into RDF triples

for s, p, o in g:
    print( (s, p, o) )
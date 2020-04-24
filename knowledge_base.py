from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, RDFS, XSD

import csv

import spotlight

# define namespaces
ex = Namespace("http://example.org/")
exdata = Namespace("http://example.org/data#")

g = Graph()

# create knowledge base
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

# processing university_data data into RDF triples
with open("dataset/university_data") as data:
    file = csv.reader(data, delimiter=',')
    for row in file:
        university = URIRef(exdata + row[0].replace(" ", "_")) # define university URI using first column
        link = URIRef(row[1]) # define link URI to university's entry in dbpedia using second column

        g.add( (university, RDF.type, ex.University) )
        g.add( (university, FOAF.name, Literal(row[0])) )
        g.add( (university, RDFS.seeAlso, link) )

# processing course data into RDF triples
with open("dataset/course_data") as data:
    file = csv.reader(data, delimiter=',')
    for row in file:
        course = URIRef(exdata + row[0].replace(" ", "_")) # define course URI using first column
        link = URIRef(row[3]) # define link URI to online source of course using fourth column

        g.add( (course, RDF.type, ex.Course) )
        g.add( (course, FOAF.name, Literal(row[0])) )
        g.add( (course, ex.hasSubject, Literal(row[1])) )
        g.add( (course, ex.hasNumber, Literal(row[2])) )
        g.add( (course, RDFS.seeAlso, link) )

        try:
            # use dbpedia spotlight to find topics
            topics = spotlight.annotate('http://model.dbpedia-spotlight.org/en/annotate',
                                    row[0],
                                    confidence=0.2, support=20)

            # process topics of course into RDF triples
            for topicRow in topics:
                print(topicRow)
                topic = URIRef(exdata + topicRow['surfaceForm'].replace(" ", "_")) # define topic URI using topic's surfaceForm from result
                topicLink = URIRef(topicRow['URI']) # define link URI to dbpedia source of the topic

                # only add topic to graph if not already in graph
                for s, p, o in g:
                    if not (topic, RDF.type, ex.Topic) in g:
                        g.add( (topic, RDF.type, ex.Topic) )
                        g.add( (topic, FOAF.name, Literal(topicRow['surfaceForm'])) )
                        g.add( (topic, RDFS.seeAlso, topicLink) )

                # add topic to this course
                g.add( (course, ex.hasTopic, topic))
        except:
            print()


# processing student data into RDF triples
with open("dataset/student_data") as data:
    file = csv.reader(data, delimiter=',')
    for row in file:
        student = URIRef(exdata + row[0].replace(" ", "_")) # define student URI using first column
        course = URIRef(exdata + row[3].replace(" ", "_")) # define course URI using fourth column

        # only add student to graph if not already in graph
        for s, p, o in g:
            if not (student, RDF.type, ex.Student) in g:
                g.add( (student, RDF.type, ex.Student) )
                g.add( (student, FOAF.name, Literal(row[0])) )
                g.add( (student, ex.hasID, Literal(row[1])) )
                g.add( (student, FOAF.mbox, Literal(row[2])) )

                if not (row[3] == ''):
                    g.add( (student, ex.hasCompleted, course) )
                if not (row[4] == ''):
                    g.add( (ex.hasCompleted, ex.hasGrade, Literal(row[4])) )
            else:
                if not (row[3] == ''):
                    g.add( (student, ex.hasCompleted, course) )
                if not (row[4] == ''):
                    g.add( (ex.hasCompleted, ex.hasGrade, Literal(row[4])) )

# print graph in N-Triples format to knowledge_base.nt file
# run this only once to populate the .nt file
print(g.serialize("knowledge_base.nt", format="nt"))
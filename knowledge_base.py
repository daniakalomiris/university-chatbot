from rdflib import Graph, Literal, BNode, RDF, URIRef
from rdflib.namespace import FOAF, RDFS, XSD

g = Graph()

University = URIRef("http://example.org/University")
Course = URIRef("http://example.org/Course")
Topic = URIRef("http://example.org/Topic")
Student = URIRef("http://example.org/Student")
hasSubject = URIRef("http://example.org/hasSubject")
hasNumber = URIRef("http://example.org/hasNumber")
hasDescription = URIRef("http://example.org/hasDescription")
hasID = URIRef("http://example.org/hasID")
hasTopic = URIRef("http://example.org/hasTopic")
hasCompleted = URIRef("http://example.org/hasCompleted")
hasGrade = URIRef("http://example.org/hasGrade")

g.add( (University, RDF.type, RDFS.Class) )
g.add( (University, RDFS.subClassOf, FOAF.organization) )
g.add( (University, RDFS.label, Literal("University", lang="en")) )
g.add( (University, RDFS.comment, Literal("Organization at which the students go to")) )

g.add( (Course, RDF.type, RDFS.Class) )
g.add( (Course, RDFS.label, Literal("Course", lang="en")) )
g.add( (Course, RDFS.comment, Literal("Course is offered at a university towards the granting of an approved degree")) )
g.add( (Course, FOAF.name, XSD.string) )
g.add( (Course, hasSubject, XSD.string) )
g.add( (Course, hasNumber, XSD.integer) )
g.add( (Course, hasDescription, XSD.string) )
g.add( (Course, RDFS.seeAlso, XSD.anyURI) )

g.add( (Topic, RDF.type, RDFS.Class) )
g.add( (Topic, RDFS.label, Literal("Topic", lang="en")) )
g.add( (Topic, RDFS.comment, Literal("Topic is part of a course material")) )
g.add( (Topic, FOAF.name, XSD.string) )
g.add( (Topic, RDFS.seeAlso, XSD.anyURI) )

g.add( (Student, RDF.type, RDFS.Class) )
g.add( (Student, RDFS.subClassOf, FOAF.person) )
g.add( (Student, RDFS.label, Literal("Student", lang="en")) )
g.add( (Student, RDFS.comment, Literal("Person who studies at a university")) )
g.add( (Student, FOAF.name, XSD.string) )
g.add( (Student, hasID, XSD.integer) )
g.add( (Student, FOAF.mbox, XSD.string) )
g.add( (Student, hasCompleted, Course) )

g.add( (hasID, RDF.type, RDF.Property) )
g.add( (hasID, RDFS.label, Literal("hasID", lang="en")) )
g.add( (hasID, RDFS.comment, Literal("Student has an ID number")) )
g.add( (hasTopic, RDFS.domain, Student) )
g.add( (hasTopic, RDFS.range, XSD.integer) )

g.add( (hasTopic, RDF.type, RDF.Property) )
g.add( (hasTopic, RDFS.label, Literal("hasTopic", lang="en")) )
g.add( (hasTopic, RDFS.comment, Literal("Course has a topic")) )
g.add( (hasTopic, RDFS.domain, Course) )
g.add( (hasTopic, RDFS.range, Topic) )

g.add( (hasCompleted, RDF.type, RDF.Property) )
g.add( (hasCompleted, RDFS.label, Literal("hasCompleted", lang="en")) )
g.add( (hasCompleted, RDFS.comment, Literal("Student has completed a course")) )
g.add( (hasCompleted, RDFS.domain, Student) )
g.add( (hasCompleted, RDFS.range, Course) )

g.add( (hasGrade, RDF.type, RDF.Property) )
g.add( (hasGrade, RDFS.subPropertyOf, hasCompleted) )
g.add( (hasGrade, RDFS.label, Literal("hasGrade", lang="en")) )
g.add( (hasGrade, RDFS.comment, Literal("Student has a grade for a completed course")) )
g.add( (hasGrade, RDFS.domain, hasCompleted) )
g.add( (hasGrade, RDFS.range, XSD.string ) )

for s, p, o in g:
    print((s, p, o))
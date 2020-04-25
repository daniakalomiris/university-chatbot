from rdflib import Graph, Literal

g = Graph()
g.parse("knowledge_base.nt", format="nt")

# returns total number of triples in the knowledge base
res = g.query("""
SELECT (COUNT(*) as ?triples)
	WHERE {
	    ?s ?p ?o
	}
""")
for row in res:
    print("Total number of triples in the knowledge base: " + row[0])

# # returns total number of students
res = g.query("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>
SELECT (COUNT(?student) as ?count)
    WHERE {
        ?student rdf:type ex:Student
    }
""")

for row in res:
    print("Total number of students: " + row[0])

# returns total number of courses
res = g.query("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>
SELECT (COUNT(?course) as ?count)
	WHERE {
	    ?course rdf:type ex:Course
	}
""")

for row in res:
    print("Total number of courses: " + row[0])

#returns total number of topics
res = g.query("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>
SELECT (COUNT(?topic) as ?count)
	WHERE {
	    ?topic rdf:type ex:Topic
	}
""")
for row in res:
    print("Total number of topics: " + row[0])

# returns topics for a given course and their link to dbpedia
res = g.query("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/>
SELECT ?name ?link
    WHERE {
        ?course foaf:name "Income Taxation in Canada" .
        ?course ex:hasTopic ?topic .
        ?topic foaf:name ?name .
        ?topic rdfs:seeAlso ?link
	}
""")
for row in res:
    print(row[0] + "(" + row[1] + ")")

# # returns all courses completed for a given student
res = g.query("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT DISTINCT ?subject ?number ?name
	WHERE {
	    ?student foaf:name "Dania Kalomiris" .
        ?student ex:hasCompleted ?course .
        ?course ex:hasSubject ?subject .
        ?course ex:hasNumber ?number .
        ?course foaf:name ?name .
        ex:hasCompleted ex:hasGrade ?grade
	}
""")
for row in res:
    print(row[0] + ' ' + row[1] + ' ' + row[2])

# returns list of all students familiar with a given topic
res = g.query("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?name
	WHERE {
	    ?student ex:hasCompleted ?course .
	    ?student foaf:name ?name .
	    ?topic foaf:name "Aerospace" .
	    ?course ex:hasTopic ?topic
	}
""")
for row in res:
    print(row[0])

# # returns list of all topics a given student is familiar with
res = g.query("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT DISTINCT ?name
	WHERE {
	    ?student ex:hasCompleted ?course .
 	    ?student foaf:name "Victoria Chikanek" .
 	    ?course ex:hasTopic ?topic .
 	    ?topic foaf:name ?name
	}
""")
for row in res:
    print(row[0])
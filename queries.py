from rdflib import Graph, Literal, BNode, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, RDFS, XSD

g = Graph()
g.parse("knowledge_base.nt", format="nt")

res = g.query("""
SELECT (COUNT (*) as ?triples)
	WHERE {
	    ?s ?p ?o
	}
""")

for row in res:
    print(row)

res = g.query("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>
SELECT (COUNT(?student) as ?count)
    WHERE {
        ?student rdf:type ex:Student
    }
""")

for row in res:
    print(row)

res = g.query("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>
SELECT (COUNT(?course) as ?count)
	WHERE {
	    ?course rdf:type ex:Course
	}
""")

for row in res:
    print(row)

res = g.query("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>
SELECT (COUNT(?topic) as ?count)
	WHERE {
	    ?topic rdf:type ex:Topic
	}
""")

for row in res:
    print(row)

res = g.query("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>
SELECT (?coveredTopics)
    WHERE {
	    ex:Course ex:hasTopic lang(?o) = “en”.
		ex:Course ex:link ?o
	}
""")

for row in res:
    print(row)

res = g.query("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT DISTINCT ?c
	WHERE {
	    ?s foaf:name "Dania Kalomiris" .
	    ?s ex:hasCompleted ?c .
		ex:hasCompleted ex:hasGrade ?g
	}
""")

for row in res:
    print(row)

res = g.query("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?students ?t
	WHERE {
	    ?students ex:hasCompleted ?c .
		?c ex:hasTopic ?t .
		ex:hasCompleted ex:hasGrade ?grade .
		FILTER (?grade!=“F”)
	}
""")

for row in res:
    print(row)

res = g.query("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex: <http://example.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?students ?t
	WHERE {
	    ?students ex:hasCompleted ?c .
		?c ex:hasTopic ?t .
		ex:hasCompleted ex:hasGrade ?grade .
		FILTER (?grade!=“F”)
	}
""")

for row in res:
    print(row)
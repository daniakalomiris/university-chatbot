from rdflib import Graph, Literal, BNode, RDF, URIRef, Namespace

import re
import random

# generate graph of knowledge base
g = Graph()
g.parse("knowledge_base.nt", format="nt")

class eliza:
  def __init__(self):
    self.keys = list(map(lambda x:re.compile(x[0], re.IGNORECASE),responses))
    self.values = list(map(lambda x:x[1],responses))

  def translate(self,str,dict):
    words = str.lower().split()
    keys = dict.keys();
    for i in range(0,len(words)):
      if words[i] in keys:
        words[i] = dict[words[i]]
    return ' '.join(words)

  def respond(self,str):
    # print(str) # returns question
    # print(responses[0][0])



    for i in range(0, len(self.keys)):
      match = self.keys[i].match(str)

      if match:
        resp = random.choice(self.values[i])
        pos = resp.find('%')

        while pos > -1:
          num = int(resp[pos+1:pos+2])
          queryResult = ''
          if (re.search("[wW]hat is \w+\s\d+ about?", str)):
            subject = match.group(num).split()[0]
            number = match.group(num).split()[1]
            res = g.query("""                                                                        
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>                                
            PREFIX ex: <http://example.org/>                                                         
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>                                                
            SELECT ?name                                                                             
            	WHERE {                                                                              
            	    ?course ex:hasSubject ?subject .                                                   
            	    ?course ex:hasNumber ?number .                                                     
            	    ?course foaf:name ?name                                                         

            	}                                                                                    
            """, initBindings={'subject': Literal(subject), 'number': Literal(number)})
            
            for row in res:
              queryResult = row[0]

          resp = resp[:pos] + \
            queryResult + \
            resp[pos+2:]

          pos = resp.find('%')

        if resp[-2:] == '?.': resp = resp[:-2] + '.'
        if resp[-2:] == '??': resp = resp[:-2] + '?'
        return resp

reflections = {
  "am"      : "are",
  "was"     : "were",
  "i"       : "you",
  "i'd"     : "you would",
  "i've"    : "you have",
  "i'll"    : "you will",
  "my"      : "your",
  "are"     : "am",
  "you've"  : "I have",
  "you'll"  : "I will",
  "your"    : "my",
  "yours"   : "mine",
  "you"     : "me",
  "me"      : "you"
}

responses = [
  [r'What is (.*) about?',
  [  "%1"]],

  [r'Which courses did (.*) take?',
  [  "%1"]],

  [r'Which courses cover (.*)?',
  [  "%1"]],

  [r'Who is familiar with (.*)?',
  [  "%1"]],

  [r'quit',
  [  "Thank you for your questions.",
    "Goodbye!",
    "Thank you, that will be $100.  Have a good day!"]],

  [r'(.*)',
  [  "Please ask a question related to the university.",
    "Can you elaborate on that?",
    "I see. Do you have a question?",
    "Please ask questions about courses, students and topics."]]
]

def command_interface():
  print('-' * 100)
  print('Welcome to the University Chatbot! Please enter your questions and enter "quit" when you are done.')
  print('-'*100)

  s = ''
  chatbot = eliza();
  while s != 'quit':
    try:
      s = input('> ')
    except EOFError:
      s = 'quit'
    while s[-1] in '!.':
      s = s[:-1]
    print(chatbot.respond(s))


if __name__ == "__main__":
  command_interface()

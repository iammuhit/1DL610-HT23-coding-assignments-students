import  bibtex
import  pytest

@ pytest . fixture
def setup_data():
 return{
'simple_author_1' : "Smith" ,
'simple_author_2' : "Jones" ,
'author_1' : "John Smith" ,
'author_2' : "Bob Jones",
'author_3' : "Justin Kenneth Pearson",
'surname_first_1' : "Pearson, Justin Kenneth",
'surname_first_2' : "Van Hentenryck, Pascal" ,
'multiple_authors_1' : "Pearson, Justin and Jones, Bob"
}

def test_author_1 (setup_data) :
 (Surname , FirstNames) = bibtex.extract_author(setup_data['simple_author_1'])
 assert(Surname , FirstNames ) == ( 'Smith' , '' )

 (Surname , FirstNames) = bibtex.extract_author(setup_data['simple_author_2'])
 assert(Surname , FirstNames ) == ( 'Jones' , '' )

def test_author_2 (setup_data) :
 (Surname , FirstNames) = bibtex.extract_author(setup_data['author_1'])
 assert(Surname , FirstNames ) == ( 'Smith' , 'John' )

 (Surname , FirstNames) = bibtex.extract_author(setup_data['author_2'])
 assert(Surname , FirstNames ) == ( 'Jones' , 'Bob' )

def test_author_3 (setup_data) :
 (Surname , FirstNames) = bibtex.extract_author(setup_data['author_3'])
 assert(Surname , FirstNames ) == ( 'Pearson' , 'Justin Kenneth' )

def test_author_4 (setup_data) :
 (Surname , FirstNames) = bibtex.extract_author(setup_data['surname_first_1' ])
 assert(Surname , FirstNames ) == ( 'Pearson' , 'Justin Kenneth' )

 (Surname , FirstNames) = bibtex.extract_author(setup_data['surname_first_2'])
 assert(Surname , FirstNames ) ==  ("Van Hentenryck" , "Pascal" )

def test_multiple_authors (setup_data) :
 Authors = bibtex.extract_authors(setup_data['multiple_authors_1'])
 assert Authors[0] == ( 'Pearson' , 'Justin' )
 assert Authors[1] == ( 'Jones' , 'Bob' )
# File bacteria.py
from owlready2 import *
 
onto = get_ontology("http://lesfleursdunormal.fr/static/_downloads/bacteria.owl#")
 
with onto:
    class Bacterium(Thing):
        def my_method(self):
            print("It is a bacterium!")
 
    class Staphylococcus(Thing):
        def my_method(self):
            print("It is a staphylococcus!")

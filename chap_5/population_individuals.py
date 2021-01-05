# File population_individuals.py
from owlready2 import *
import csv
 
onto = get_ontology("bacteria.owl").load()
 
onto_individuals = get_ontology("http://lesfleursdunormal.fr/static/_downloads/bacteria_individuals.owl")
onto_individuals.imported_ontologies.append(onto)
 
f = open("population_individuals.csv")
reader = csv.reader(f)
next(reader)
 
with onto_individuals:
    for row in reader:
        id, gram_positive, shape, grouping, nb_colonies = row
        individual = onto.Bacterium(id)
    
        if gram_positive:
            if gram_positive == "True": gram_positive = True
            else:                       gram_positive = False
            individual.gram_positive = gram_positive
    
        if nb_colonies:
            individual.nb_colonies = int(nb_colonies)
      
        if shape:
            shape_class = onto[shape]
            shape = shape_class()
            individual.has_shape = shape
      
        if grouping:
            grouping_class = onto[grouping]
            grouping = grouping_class()
            individual.has_grouping.append(grouping)
      
onto_individuals.save("bacteria_individuals.owl")

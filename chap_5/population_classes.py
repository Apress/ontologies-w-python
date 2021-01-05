# File population_classes.py
from owlready2 import *
import csv, types
 
onto = get_ontology("bacteria.owl").load()
 
onto_classes = get_ontology("http://lesfleursdunormal.fr/static/_downloads/bacteria_classes.owl")
onto_classes.imported_ontologies.append(onto)
 
f = open("population_classes.csv")
reader = csv.reader(f)
next(reader)
 
with onto_classes:
    for row in reader:
        id, parent, gram_positive, shape, grouping = row
    
        if parent: parent = onto[parent]
        else:      parent = Thing
    
        Class = types.new_class(id, (parent,))
    
        if gram_positive:
            if gram_positive == "True": gram_positive = True
            else:                       gram_positive = False
            Class.gram_positive = gram_positive
      
        if shape:
            shape_class = onto[shape]
            Class.has_shape = shape_class
      
        if grouping:
            grouping_class = onto[grouping]
            Class.has_grouping.append(grouping_class)
      
onto_classes.save("bacteria_classes.owl")

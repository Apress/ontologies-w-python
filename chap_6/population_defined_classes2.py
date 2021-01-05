# File population_defined_classes2.py
from owlready2 import *
import csv, types
 
onto = get_ontology("bacteria.owl").load()
 
onto_classes = get_ontology("http://lesfleursdunormal.fr/static/_downloads/bacteria_defined_classes.owl")
onto_classes.imported_ontologies.append(onto)
 
f = open("population_classes.csv")
reader = csv.reader(f)
next(reader)
 
id_2_parents       = defaultdict(list)
id_2_gram_positive = {}
id_2_shape         = {}
id_2_groupings     = defaultdict(list)
 
for row in reader:
    id, parent, gram_positive, shape, grouping = row
    
    if parent:
        id_2_parents[id].append(onto[parent])
  
    if gram_positive:
        if gram_positive == "True": gram_positive = True
        else:                       gram_positive = False
        id_2_gram_positive[id] = gram_positive
     
    if shape:
        shape_class = onto[shape]
        id_2_shape[id] = shape_class
      
    if grouping:
        grouping_class = onto[grouping]
        id_2_groupings[id].append(grouping_class)
         
with onto_classes:
    for id in id_2_parents:
        if id_2_parents[id]:
            Class = types.new_class(id, tuple(id_2_parents[id]))
        else:
            Class = types.new_class(id, (Thing,))
   
        conditions = []
 
        if id in id_2_gram_positive:
            conditions.append(onto.gram_positive.value(id_2_gram_positive[id]))
 
        if id in id_2_shape:
            conditions.append(onto.has_shape.some(id_2_shape[id]))
            conditions.append(onto.has_shape.only(id_2_shape[id]))
 
        for grouping in id_2_groupings[id]:
            conditions.append(onto.has_grouping.some(grouping))
 
        if   len(conditions) == 1:
            Class.equivalent_to.append(conditions[0])
        elif len(conditions) > 1:
            Class.equivalent_to.append( And(conditions) )
    
onto_classes.save("bacteria_defined_classes.owl")

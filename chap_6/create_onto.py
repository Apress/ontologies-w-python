# File create_onto.py
from owlready2 import *
 
onto = get_ontology("http://lesfleursdunormal.fr/static/_downloads/bacteria.owl#")
 
with onto:
    class Shape(Thing): pass
    class Round(Shape): pass
    class Rod(Shape): pass
    
    AllDisjoint([Round, Rod])
    
    class Grouping(Thing): pass
    class Isolated(Grouping): pass
    class InPair(Grouping): pass
    class InCluster(Grouping): pass
    class InChain(Grouping): pass
    class InSmallChain(InChain): pass
    class InLongChain(InChain): pass
    
    AllDisjoint([Isolated, InPair, InCluster, InChain])
    AllDisjoint([InSmallChain, InLongChain])
    
    class Bacterium(Thing): pass
    AllDisjoint([Bacterium, Shape, Grouping])
    
    class gram_positive(Bacterium >> bool, FunctionalProperty): pass
    class nb_colonies(Bacterium >> int, FunctionalProperty): pass
    
    class has_shape(Bacterium >> Shape, FunctionalProperty): pass
    class has_grouping(Bacterium >> Grouping): pass
    
    class is_shape_of(Shape >> Bacterium):
        inverse = has_shape
    class is_grouping_of(Grouping >> Bacterium):
        inverse = has_grouping
    
    class Pseudomonas(Bacterium):
        is_a = [ has_shape.some(Rod),
                 has_shape.only(Rod),
                 has_grouping.some(Isolated | InPair),
                 gram_positive.value(False) ]
    
    class Coccus(Bacterium):
        equivalent_to = [ Bacterium
                        & has_shape.some(Round)
                        & has_shape.only(Round) ]
        
    class Bacillus(Bacterium):
        equivalent_to = [ Bacterium
                        & has_shape.some(Rod)
                        & has_shape.only(Rod) ]
        
    class Staphylococcus(Coccus):
        equivalent_to = [ Bacterium
                        & has_shape.some(Round)
                        & has_shape.only(Round)
                        & has_grouping.some(InCluster)
                        & gram_positive.value(True) ]
        
    class Streptococcus(Coccus):
        equivalent_to = [ Bacterium
                        & has_shape.some(Round)
                        & has_shape.only(Round)
                        & has_grouping.some(InSmallChain)
                        & has_grouping.only( Not(Isolated) )
                        & gram_positive.value(True) ]
        
    unknown_bacterium = Bacterium(
        "unknown_bacterium",
        has_shape = Round(),
        has_grouping = [ InCluster("in_cluster1") ],
        gram_positive = True,
        nb_colonies = 6
    )

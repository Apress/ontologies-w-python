# File go_part_of.py
from owlready2 import *
 
default_world.set_backend(filename = "quadstore.sqlite3")
go = get_ontology("http://purl.obolibrary.org/obo/go.owl#").load()
obo = go.get_namespace("http://purl.obolibrary.org/obo/")
default_world.save()
 
def my_render(entity):
    return "%s:%s" % (entity.name, entity.label.first())
set_render_func(my_render)
 
with obo:
    class GO_0005575(Thing):
        @classmethod
        def subparts(self):
            results = list(self.BFO_0000051)
            results.extend(self.inverse_restrictions(obo.BFO_0000050))
            return results
         
        @classmethod
        def transitive_subparts(self):
            results = set()
            for descendant in self.descendants():
                results.add(descendant)
                for subpart in descendant.subparts():
                    results.update(subpart.transitive_subparts())
            return results
          
        @classmethod
        def superparts(self):
            results = list(self.BFO_0000050)
            results.extend(self.inverse_restrictions(obo.BFO_0000051))
            return results
          
        @classmethod
        def transitive_superparts(self):
            results = set()
            for ancestor in self.ancestors():
                if not issubclass(ancestor, GO_0005575): continue 
                results.add(ancestor)
                for superpart in ancestor.superparts():
                    if issubclass(superpart, GO_0005575):
                        results.update(superpart.transitive_superparts())
            return results

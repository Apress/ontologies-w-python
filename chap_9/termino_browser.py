# File termino_browser.py
from owlready2 import *
default_world.set_backend(filename = "pymedtermino.sqlite3")
PYM = get_ontology("http://PYM/").load()
 
from flask import Flask, url_for, request
app = Flask(__name__)
 
def repr_concept(concept):
    return """[<a href="%s">%s:%s</a>] %s""" % (
        url_for("concept_page", iri = concept.iri),
        concept.terminology.name,
        concept.name,
        concept.label.first() )
 
def repr_relations(entity, border = False):
    if border: html = """<table style="border: 1px solid #aaa;">"""
    else:      html = """<table>"""
    for Prop in entity.get_class_properties():
        for value in Prop[entity]:
            if issubclass(value, PYM.Concept):
                value = repr_concept(value)
            elif issubclass(value, PYM.Group):
                value = repr_relations(value, True)
            html += """<tr><td>%s:""" % Prop.name
            html += """</td><td> %s</td></tr>""" % value
    html += """</table>"""
    return html
 
@app.route('/')
def homepage():
    html = """
<html><body>
  Search in all terminologies:
  <form action="/search">
    <input type="text" name="keywords"/>
    <input type="submit"/>
  </form>
  Or <a href="%s">browse the entire hierarchy</a>
</body></html>""" % url_for("concept_page", iri = "http://PYM/SRC/SRC")
    return html
 
@app.route('/search')
def search_page():
    keywords = request.args.get("keywords", "")
    html = """<html><body>Recherche "%s":<br/>\n""" % keywords
    keywords = " ".join("%s*" % word for word in keywords.split())
    results = PYM.search(keywords)
    for concept in results:
        html += """%s<br/>""" % repr_concept(concept)
    html += """</body></html>"""
    return html
  
@app.route('/concept/<path:iri>')
def concept_page(iri):
    concept = IRIS[iri]
    html  = """<html><body>"""
    html += """<h2>%s</h2>""" % repr_concept(concept)
    html += """<h3>Ancestor concept (except parents)</h3>"""
    html += """%s<br/>""" % repr_concept(concept.terminology)
    ancestors = set(concept.ancestor_concepts(include_self = False))
    ancestors = ancestors - set(concept.parents)
    ancestors = list(ancestors)
    ancestors.sort(key = lambda t: len(t.ancestor_concepts()))
    for ancestor in ancestors:
        html += """%s<br/>""" % repr_concept(ancestor)
    
    html += """<h3>Parent concepts</h3>"""
    for parent in concept.parents:
        html += """%s<br/>""" % repr_concept(parent)
    
    html += """<h3>Relations</h3>"""
    html += repr_relations(concept)
  
    if not concept.name == "CUI":
        html += """<h3>Child concepts</h3>"""
        for child in concept.children:
            html += """%s<br/>""" % repr_concept(child)
      
    html += """</body></html>"""
    return html
  
import werkzeug.serving
werkzeug.serving.run_simple("localhost", 5000, app)

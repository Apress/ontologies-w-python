# File dynamic_website.py
from owlready2 import *
onto = get_ontology("bacteria.owl").load()
 
from flask import Flask, url_for
app = Flask(__name__)
 
@app.route('/')
def ontology_page():
    html  = """<html><body>"""
    html += """<h2>'%s' ontology</h2>""" % onto.base_iri
    html += """<h3>Root classes</h3>"""
    for Class in Thing.subclasses():
        html += """<p><a href="%s">%s</a></p>""" % (url_for("class_page", iri = Class.iri), Class.name)
      
    html += """</body></html>"""
    return html
 
@app.route('/class/<path:iri>')
def class_page(iri):
    Class = IRIS[iri]
    html = """<html><body><h2>'%s' class</h2>""" % Class.name
  
    html += """<h3>superclasses</h3>"""
    for SuperClass in Class.is_a:
        if isinstance(SuperClass, ThingClass):
            html += """<p><a href="%s">%s</a></p>""" % (url_for("class_page", iri = SuperClass.iri), SuperClass.name)
        else:
            html += """<p>%s</p>""" % SuperClass
      
    html += """<h3>equivalent classes</h3>"""
    for EquivClass in Class.equivalent_to:
        html += """<p>%s</p>""" % EquivClass
    
    html += """<h3>Subclasses</h3>"""
    for SubClass in Class.subclasses():
        html += """<p><a href="%s">%s</a></p>""" % (url_for("class_page", iri = SubClass.iri), SubClass.name)
    
    html += """<h3>Individuals</h3>"""
    for individual in Class.instances():
        html += """<p><a href="%s">%s</a></p>""" % (url_for("individual_page", iri = individual.iri), individual.name)
    
    html += """</body></html>"""
    return html
 
@app.route('/individual/<path:iri>')
def individual_page(iri):
    individual = IRIS[iri]
    html = """<html><body><h2>'%s' individual</h2>""" % individual.name
  
    html += """<h3>Classes</h3>"""
    for Class in individual.is_a:
        html += """<p><a href="%s">%s</a></p>""" % (url_for("class_page", iri = Class.iri), Class.name)
    
    html += """<h3>Relations</h3>"""
    if isinstance(individual, onto.Bacterium):
        html += """<p>shape = %s</p>""" % individual.has_shape
        html += """<p>grouping = %s</p>""" % individual.has_grouping
        if   individual.gram_positive == True:
            html += """<p>Gram +</p>"""
        elif individual.gram_positive == False:
            html += """<p>Gram -</p>"""
        
    html += """</body></html>"""
    return html
 
import werkzeug.serving
werkzeug.serving.run_simple("localhost", 5000, app)

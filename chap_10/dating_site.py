# File dating_site.py
from owlready2 import *
from go_part_of import *
  
from flask import Flask, request
app = Flask(__name__)
  
import mygene
mg = mygene.MyGeneInfo()
  
def search_protein(protein_name):
    r = mg.query('name:"%s"' % protein_name, fields = "go.CC.id", species = "human", size = 1)
    if not "go" in r["hits"][0]: return set()
  
    cc = r["hits"][0]["go"]["CC"]
    if not isinstance(cc, list): cc = [cc]
  
    components = set()
    for dict in cc:
        go_id = dict["id"]
        go_term = obo[go_id.replace(":", "_")]
        if go_term: components.add(go_term)
    
    return components
  
def semantic_intersection(components1, components2):
    subparts1 = set()
    for component in components1:
        subparts1.update(component.transitive_subparts())
    
    subparts2 = set()
    for component in components2:
        subparts2.update(component.transitive_subparts())
    
    common_components = subparts1 & subparts2
  
    cache = { component: component.transitive_subparts() for component in common_components }
  
    largest_common_components = set()
    for component in common_components:
        for component2 in common_components:
            if (not component2 is component) and (component in cache[component2]): break
        else:
            largest_common_components.add(component)
  
    return largest_common_components
  
@app.route('/')
def entry_page():
    html  = """
<html><body>
  <form action="/result">
    Protein 1: <input type="text" name="prot1"/><br/><br/>
    Protein 2: <input type="text" name="prot2"/><br/><br/>
    <input type="submit"/>
  </form>
</body></html>"""
    return html
  
@app.route('/result')
def result_page():
    prot1 = request.args.get("prot1", "")
    prot2 = request.args.get("prot2", "")
  
    components1 = search_protein(prot1)
    components2 = search_protein(prot2)
  
    common_components = semantic_intersection(components1, components2)
  
    html  = """<html><body>"""
    html += """<h3>Components for protein #1 (%s)</h3>""" % prot1
    if components1:
        html += "<br/>".join(sorted(str(component) for component in components1))
    else:
        html += "(none)<br/>"
  
    html += """<h3>Components for protein #2 (%s)</h3>""" % prot2
    if components2:
        html += "<br/>".join(sorted(str(component) for component in components2))
    else:
        html += "(none)<br/>"
  
    html += """<h3>Possible dating sites</h3>"""
    if common_components:
        html += "<br/>".join(sorted(str(component) for component in common_components))
    else:
        html += "(none)<br/>"
    
    html += """</body></html>"""
    return html
  
import werkzeug.serving
werkzeug.serving.run_simple("localhost", 5000, app)

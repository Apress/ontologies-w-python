# File decision_support.py
from owlready2 import *
onto = get_ontology("bacteria.owl").load()
 
from flask import Flask, request
app = Flask(__name__)
 
@app.route('/')
def entry_page():
    html  = """<html><body>
<h3>Enter the bacteria characteristics:</h3>
<form action="/result">
    Gram:<br/>
    <input type="radio" name="gram" value="True"/> Positive<br/>
    <input type="radio" name="gram" value="False"/> Negative<br/>
    <br/>
    Shape:<br/>
    <input type="radio" name="shape" value="Round"/> Round<br/>
    <input type="radio" name="shape" value="Rod"/> Rod<br/>
    <br/>
    Groupings:<br/>
    <select name="groupings" multiple="multiple">
        <option value="Isolated">Isolated</option>
        <option value="InPair">InPair</option>
        <option value="InCluster">InCluster</option>
        <option value="InSmallChain">InSmallChain</option>
        <option value="InLongChain">InLongChain</option>
    </select><br/>
    <br/>
    <input type="submit"/>
</form>  
</body></html>"""
    return html
   
ONTO_ID = 0 
  
@app.route('/result')
def page_result():
    global ONTO_ID
    ONTO_ID = ONTO_ID + 1
    
    onto_tmp = get_ontology("http://tmp.org/onto_%s.owl#" % ONTO_ID)
    
    gram      = request.args.get("gram", "")
    shape     = request.args.get("shape", "")
    groupings = request.args.getlist("groupings")
    
    with onto_tmp:
        bacterium = onto.Bacterium()
        
        if   gram == "True": bacterium.gram_positive = True
        elif gram == "False": bacterium.gram_positive = False
        
        if shape:
            shape_class = onto[shape]
            bacterium.has_shape = shape_class()
      
        for grouping in groupings:
            grouping_class = onto[grouping]
            bacterium.has_grouping.append(grouping_class())
       
        close_world(bacterium)
   
        sync_reasoner([onto, onto_tmp])
    
    class_names = []
    for bacterium_class in bacterium.is_a:
        if isinstance(bacterium_class, ThingClass):
            class_names.append(bacterium_class.name)
    class_names = ", ".join(class_names)
    
    html  = """<html><body>
<h3>Result: %s</h3>
</body></html>""" % class_names
    
    onto_tmp.destroy()
    
    return html
  
import werkzeug.serving
werkzeug.serving.run_simple("localhost", 5000, app)

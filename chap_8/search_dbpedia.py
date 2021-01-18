# File search_dbpedia.py
from flask import Flask, request
app = Flask(__name__)
 
from owlready2 import *
 
QUADSTORE = "/tmp/dbpedia.sqlite3"
default_world.set_backend(filename = QUADSTORE)
 
dbpedia  = get_ontology("http://wikidata.dbpedia.org/ontology/")
resource = default_world.get_namespace("http://wikidata.dbpedia.org/resource/")
 
@app.route('/')
def page_query():
    html = """
<html><body>
    <form action="/result">
        <input type="text" name="keywords"/>
        <input type="submit"/>
    </form>
</body></html>"""
    return html
    
@app.route('/result')
def page_result():
    keywords = request.args.get("keywords", "")
    html = """<html><body>Search results for "%s":<br/>\n""" % keywords
    
    keywords = " ".join("%s*" % keyword for keyword in keywords.split())
    articles = default_world.search(label = FTS(keywords))
    
    html += """<ul>"""
    for article in articles:
        html += """<li><a href="/article/%s">%s:%s</a></li>""" % (article.name, article.name, article.label.first())
    html += """</ul></body></html>"""
    return html
    
@app.route('/article/<name>')
def page_article(name):
    article = resource[name]
    
    html = """<html><body><h2>%s:%s</h2>""" % (article.name, article.label.first())
    html += """belongs to classes: %s<br/><br/>\n""" % ", ".join(repr(clazz) for clazz in article.is_a)
    html += """has link to page:<br/>\n"""
    html += """<ul>"""
    for cite in article.wikiPageWikiLink:
        html += """<li><a href="/article/%s">%s:%s</a></li>""" % (cite.name, cite.name, cite.label.first())
    html += """</ul></body></html>"""
    return html
 
import werkzeug.serving
werkzeug.serving.run_simple("localhost", 5000, app)

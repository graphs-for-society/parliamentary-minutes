"""
Webapp module
"""

import json
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

from graph import GraphApi

graph_id = os.environ['GRAPH_ID']
api_key = os.environ['API_KEY']

graph = GraphApi(api_key, graph_id)

###
# Routing
###

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        # posted = True
        print "Query for {} --> {}".format(request.form['representative_name'], request.form['party'])
        paths = graph.get_paths(unicode(request.form['representative_name']), unicode(request.form['party']))
        return render_template('home.html', paths=paths)
    else:
        return render_template('home.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/data/<path:path>')
def send_json(path):
    return send_from_directory('data', path)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

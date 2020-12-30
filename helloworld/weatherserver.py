import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# EasyweatherV1.5.6
# Customised upload settings which work.
# Server IP / Hostname :    a.b.c.d
# Path:                     myweatherdata/? (note trailing ? or URL params are not passed in correctly)
# Station ID:               mystation (doesn't matter)
# Station Key:              mykey
# Port:                     5000 (can be anything of course)
# Upload Interval           60 (seconds)

@app.route('/myweatherdata/', methods=['GET'])
def home():
    print(request.args)
    for i in request.args:
        print(f'arg: {i} value: {request.args[i]}')
    return '''<h1>Response</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

app.run(host='0.0.0.0')

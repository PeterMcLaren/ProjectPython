import flask
from flask import request

import mysql.connector

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Weather station setup:
#   EasyweatherV1.5.6
#   Customised upload settings which work.
#   Server IP / Hostname :    a.b.c.d
#   Path:                     myweatherdata/? (note trailing ? or URL params are not passed in correctly)
#   Station ID:               mystation (doesn't matter)
#   Station Key:              mykey (doesn't matter)
#   Port:                     5000 (can be anything of course)
#   Upload Interval           60 (seconds)
# MySQL setup:
#   sudo apt-get install mariadb-server-10.0
#   sudo mysql_secure_installation
#       (none)
#       Root password (set)
#       Remove Anon users
#       Disallow root login remotely
#       Remove test database
#       Reload privileges
#   

@app.route('/myweatherdata/', methods=['GET'])
def weatherdata():
    print(request.args)
    for i in request.args:
        print(f'arg: {i} value: {request.args[i]}')
    return 'ok'

mydb = mysql.connector.connect(
  host="192.168.1.225",
  user="yourusername",
  password="yourpassword"
)

print(mydb)

app.run(host='0.0.0.0')

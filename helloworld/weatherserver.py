import flask
from flask import request
import mysql.connector

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
#   sudo vi /etc/mysql/mariadb.conf.d/50-server.cnf
#       Comment out bind-address 127.0.0.1 line to allow remote access to MySQL for debug only!
#   sudo mysql -u root -p
#       CREATE USER 'weatherserver'@'%' IDENTIFIED BY 'weatherpass';
#       GRANT ALL ON *.* TO 'weatherserver'@'%';
#       flush privileges;

SQLHost="192.168.1.225" # 127.0.0.1 in production
SQLUser="weatherserver" # change in production
SQLPass="weatherpass" # change in production

SQLCreate=("create table weathertable ("
    "id INT AUTO_INCREMENT PRIMARY KEY, "
    "indoortemp DECIMAL(6,3), "
    "outdoortemp DECIMAL(6,3), "
    "dewpoint DECIMAL(6,3), "
    "windchill DECIMAL(6,3), "
    "indoorhumidity DECIMAL(6,3), "
    "outdoorhumidity DECIMAL(6,3), "
    "windspeedmph DECIMAL(6,3), "
    "windgustmph DECIMAL(6,3), "
    "winddir DECIMAL(6,3), "
    "absbarom DECIMAL(7,3), "
    "barom DECIMAL(7,3), "
    "rainmm DECIMAL(6,3), " 
    "dailyrainmm DECIMAL(6,3), "
    "weeklyrainmm DECIMAL(6,3), "
    "monthlyrainmm DECIMAL(6,3), "
    "solarradiation DECIMAL(6,3), "
    "UV DECIMAL(6,3), "
    "dateutc DATETIME)"
    )

app = flask.Flask(__name__)
app.config["DEBUG"] = True

mydb = mysql.connector.connect(
  host=SQLHost,
  user=SQLUser,
  password=SQLPass
)

def SetupDb(dbconn):
    dbcursor=dbconn.cursor()
    print("Trying to create database")
    try:
        dbcursor.execute("create database weatherdata")
    except Exception as e:
        print("Db Create: ", e)
    else:
        print("Weatherdata database created successfully")
    try:
        dbcursor.execute("use weatherdata")
        dbcursor.execute(SQLCreate)
    except Exception as e:
        print("Table Create: ", e)
    else:
        print("Weathertable table created successfully")

@app.route('/myweatherdata/', methods=['GET'])
def weatherdata():
    print(request.args)
    for i in request.args:
        print(f'arg: {i} value: {request.args[i]}')
    return 'ok'

SetupDb(mydb)
app.run(host='0.0.0.0')

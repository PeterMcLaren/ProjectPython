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

# Address of MySQL server
SQLHost="192.168.1.225" # 127.0.0.1 in production
# Credentials to connect to MySQL
SQLUser="weatherserver" # change in production
SQLPass="weatherpass" # change in production

# String to create weather table - single line string
# (bracket notation is just way of representing long string as multiline in source code)
SQLCreate=("create table weathertable ("
    "id INT AUTO_INCREMENT PRIMARY KEY, "
    "indoortempf DECIMAL(3,1), tempf DECIMAL(3,1), dewptf DECIMAL(3,1), windchillf DECIMAL(3,1), "
    "indoorhumidity DECIMAL(2,0), humidity DECIMAL(2,0), "
    "windspeedmph DECIMAL(2,1), windgustmph DECIMAL(2,1), winddir DECIMAL(3,0), "
    "absbaromin DECIMAL(5,3), baromin DECIMAL(5,3), "
    "rainin DECIMAL(6,3), dailyrainin DECIMAL(6,3), weeklyrainin DECIMAL(6,3), monthlyrainin DECIMAL(6,3), "
    "solarradiation DECIMAL(5,2), UV DECIMAL(1,0), "
    "indoortempc DECIMAL(3,1) AS ((indoortempf-32)*5/9) PERSISTENT, tempc DECIMAL(3,1) AS ((tempf-32)*5/9) PERSISTENT, "
    "dewptc DECIMAL(3,1) AS ((dewptf-32)*5/9) PERSISTENT, windchillc DECIMAL(3,1) AS ((windchillf-32)*5/9) PERSISTENT, "
    "absbaromhpa DECIMAL(5,1) AS (absbaromin*33.87) PERSISTENT, baromhpa DECIMAL(5,1) AS (baromin*33.87) PERSISTENT, "
    "rainmm DECIMAL(4,1) AS (rainin*25.4) PERSISTENT, dailyrainmm DECIMAL(4,1) AS (dailyrainin*25.4) PERSISTENT, "
    "weeklyrainmm DECIMAL(4,1) AS (weeklyrainin*25.4) PERSISTENT, monthlyrainmm DECIMAL(4,1) AS (monthlyrainin*25.4) PERSISTENT, "
    "dateutc DATETIME, "
    "INDEX (dateutc))"
    )

# List of columns to insert each time
SQLInsertCols= [
    "indoortempf", "tempf", "dewptf", "windchillf",
    "indoorhumidity", "humidity", 
    "windspeedmph", "windgustmph", "winddir",
    "absbaromin", "baromin",
    "rainin", "dailyrainin", "weeklyrainin", "monthlyrainin",
    "solarradiation", "UV",
    "dateutc"
]

# Initialize Flask
app = flask.Flask(__name__)
app.config["DEBUG"] = False

# Get connection to database
mydb = mysql.connector.connect(
  host=SQLHost,
  user=SQLUser,
  password=SQLPass
)

def SetupDb():
    mydb = mysql.connector.connect(
        host=SQLHost,
        user=SQLUser,
        password=SQLPass
    )
    dbcursor=mydb.cursor()
    print("Trying to create database and table:")
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
    print("closing db connection")
    mydb.close()

def pluckfromdict(d,l):
    newd={}
    for i in l:
        newd[i]=d[i]
    return newd

@app.route('/myweatherdata/', methods=['GET'])
def weatherdata():
  
    dicttoinsert=pluckfromdict(request.args,SQLInsertCols)
    placeholders = ", ".join(["%s"] * len(dicttoinsert))
    columns = ", ".join(dicttoinsert.keys())

    sql = f"INSERT INTO weathertable ({columns}) VALUES ({placeholders})" 
 
    # We're ready so connect to database
    mydb = mysql.connector.connect(
        host=SQLHost,
        user=SQLUser,
        password=SQLPass
    )
    dbcursor=mydb.cursor()
    dbcursor.execute("use weatherdata")
    
    # Execute the insert statement, passing in the values
    dbcursor.execute(sql,list(dicttoinsert.values()))
    
    # No changes without the commit
    mydb.commit()

    # Debug print - prints before the corresponding flask http debug output.
    print(f"{dbcursor.rowcount} rows inserted")
    # Close Db Conneciton each time
    mydb.close()
    return 'ok'

SetupDb()
app.run(host='0.0.0.0')

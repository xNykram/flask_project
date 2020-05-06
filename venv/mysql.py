from flaskext.mysql import MySQL
from flask import Flask, flash

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = ""
app.config['MYSQL_DATABASE_DB'] = "Users"
app.config['MYSQL_DATABASE_HOST'] = "localhost"

mysql = MySQL()
mysql.init_app(app)

class mysqlObj():
        def __init__(self):
                self.server_name = []
                self.server_ip = []
                self.server_password = []

        def Search(self, querry):
                connection = mysql.connect()
                cursor = connection.cursor()
                cursor.execute(querry)
                result = cursor.fetchone()
                connection.close()
                return result

        def DataUpdater(self):
                mysqlQuerry = self.Search("SELECT * from f_servers where id = '1'")
                self.server_name = str(mysqlQuerry[1])
                self.server_ip = str(mysqlQuerry[2])
                self.server_password = str(mysqlQuerry[3])

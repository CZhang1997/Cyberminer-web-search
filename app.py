
from flask import Flask, render_template, request, json, redirect,url_for
from flaskext.mysql import MySQL
from flask import jsonify
import math



app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'cyberminer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8889
mysql.init_app(app) 


app.secret_key = 'secret key'

@app.route("/") # define an url "/" home page
def main():   
     return render_template('home.html')
    
@app.route("/search", methods=['POST', 'GET'])
def search():
    try:

        _keyword = request.form['search']


        conn = mysql.connect()
        cursor = conn.cursor()
      
        cursor.execute("SELECT * FROM tbl_test where title like %s or description like %s ",('%'+_keyword+'%','%'+_keyword+'%'))
        data = cursor.fetchall()

        if len(data)>= 0 :
            conn.commit()
            return render_template('home.html',results=data)
        else:
            return render_template ('error.html', error='no search result')

    except Exception as e:
        return render_template('error.html',error = str(e))





if __name__ == "__main__":
    app.run(debug=True)
    # app.run()

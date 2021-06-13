
from flask import Flask, render_template, request, json, redirect,url_for
from flaskext.mysql import MySQL
from flask import jsonify
import math
import csv
import config



app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = config.MYSQL_DATABASE_USER
app.config['MYSQL_DATABASE_PASSWORD'] = config.MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = config.MYSQL_DATABASE_DB
app.config['MYSQL_DATABASE_HOST'] = config.MYSQL_DATABASE_HOST
app.config['MYSQL_DATABASE_PORT'] = config.MYSQL_DATABASE_PORT2
mysql.init_app(app) 

# set up

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')
try:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_test")
    data = cursor.fetchall()
    if len(data) == 0 :
        print("setting up database")
        with open('./dataset/data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    cursor.execute("INSERT INTO tbl_test(title, description, url) VALUES (%s, %s, %s)", (deEmojify(row[0]), deEmojify(row[2]), row[1]))
                line_count += 1
            data = cursor.fetchall()
            conn.commit()
    else:
        print("database is ready to use")
except Exception as e:
    print(e)
    cursor.execute("CREATE TABLE tbl_test( id INT AUTO_INCREMENT PRIMARY KEY, title text , description text,url text);")
    print("please try again, table has been create")
    exit()
finally:
    cursor.close()
    conn.close()

app.secret_key = 'secret key'

@app.route("/") # define an url "/" home page
def main():   
     return render_template('home.html')
    
@app.route("/search", methods=['POST', 'GET'])
def search():
    try:

        conn = mysql.connect()
        cursor = conn.cursor()
        if(not "search" in request.form):
            return  redirect("/")
        _keyword = request.form['search']
        if(not(_keyword and _keyword.strip())):
            return  redirect("/")
        
        cursor.execute("SELECT * FROM tbl_test where title like %s or description like %s ",('%'+_keyword+'%','%'+_keyword+'%'))
        data = cursor.fetchall()

        if len(data)>= 0 :
            conn.commit()
            return render_template('home.html',results=data, keyword=_keyword)
        else:
            return render_template ('error.html', error='no search result')

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()



if __name__ == "__main__":
    app.run(debug=True)
    # app.run()

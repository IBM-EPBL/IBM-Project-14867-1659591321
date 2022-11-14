
from flask import Flask, render_template, request, redirect, url_for,session

import ibm_db
import bcrypt
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from dotenv import load_dotenv


try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=vxz92171;PWD=mCH7uu0w9WXH0hlY",'','')
    print(conn)
    print("connection successfull")
except:
    print("Error in connection, sqlstate = ")
    errorState = ibm_db.conn_error()
    print(errorState)


app = Flask(__name__)
app.secret_key ='_5#y2L"F4Q8z\n\xec]/'

@app.route("/",methods=['GET'])
def index():
    if 'email' not in session:
      return redirect(url_for('covidlogin'))
    return render_template('covidindex.html',name='Home')

@app.route("/covidregister",methods=['GET','POST'])
def register():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

  
    query = "SELECT * FROM LOGINAUTHENTICATION WHERE useremail=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    
    if not isUser:
      insert_sql = "INSERT INTO LOGINAUTHENTICATION(USERNAME, USEREMAIL, PASSWORD) VALUES (?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, hash)
      ibm_db.execute(prep_stmt)
      return render_template('covidregister.html',success="You can login")
      # send_conformation_mail()
    else:
      return render_template('covidregister.html',error='Invalid Credentials')

  return render_template('covidregister.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']

      if not email or not password:
        return render_template('login.html',error='Please fill all fields')
      query = "SELECT * FROM LOGINAUTHENTICATION WHERE useremail=?"
      stmt = ibm_db.prepare(conn, query)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      isUser = ibm_db.fetch_assoc(stmt)
      print(isUser,password)

      if not isUser:
        return render_template('login.html',error='Invalid Credentials')
      #return render_template('login.html',error=isUser['PASSWORD'])
      isPasswordMatch = bcrypt.checkpw(password.encode('utf-8'),isUser['PASSWORD'].encode('utf-8'))

      if not isPasswordMatch:
        return render_template('covidlogin.html',error='Invalid Credentials')

      session['email'] = isUser['USEREMAIL']
      return redirect(url_for('index'))

    return render_template('covidlogin.html',name='Home')

@app.route('/user_map')
def user_map():
   return render_template('user.html',name='Map')

@app.route('/about')
def about():
   return render_template('about.html',name='Map')

@app.route('/management')
def management():
   return render_template('management.html',name='Map')   

@app.route('/data')
def data():
   return render_template('data.html',name='Map')  


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('covidlogin'))
if __name__ == "__main__":
    app.run(debug=True)
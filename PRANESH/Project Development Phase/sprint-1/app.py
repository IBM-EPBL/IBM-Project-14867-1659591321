import adminverification
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

app.secret_key = 'pranesh'



@app.route('/')
def covidindex():
    if session.get('covid_login'):
        return render_template('covidindex.html', covidMail=session.get('covid_Mail'))
    else:
        return redirect('/admin')


@app.route('/admin', methods=['POST', 'GET'])
def covidlogin():
    if request.method == 'GET':
        return render_template("covidlogin.html")
    elif request.method == 'POST':
        username = request.form.get('mail')
        res = adminverification.adminloginverfication(username, request.form.get('password'))
        if res:
            session['conzo_login'] = True
            session['conzo_Mail'] = username
            return redirect('/')
        else:
            return render_template('covidlogin.html', data=res)


@app.get('/logout')
def admin_logout():
    session.pop('covidlogin', None)
    session.pop('covid_Mail', None)
    return redirect('/')


@app.route('/admin/registration', methods=['POST', 'GET'])
def covid_register():
    if request.method == 'GET':
        return render_template('covidregister.html')
    elif request.method == 'POST':
        res = adminverification.covidregister(request.form.get('mail'), request.form.get('password'), request.form.get('reqid'))
        if res:
            return redirect('/')
        else:
            return render_template('covidregister.html', data=res)


if __name__ == '__main__':
    app.run(debug=True)
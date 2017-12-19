#!flask/bin/python
from flask import Flask, jsonify, flash, redirect, render_template, session, request, url_for
from model import DBconn
import flask, sys, os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'josephjayme'

def spcall(qry, param, commit=False):
    try:
        dbo = DBconn()
        cursor = dbo.getcursor()
        cursor.callproc(qry, param)
        res = cursor.fetchall()
        if commit:
            dbo.dbcommit()
        return res
    except:
        res = [("Error: " + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]),)]
    return res

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('stripperspage'))
    session['logged_in'] = False
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['user']
    password = request.form['pass']
    res = spcall('login', (username, password), True)
    if 'NOT EXIST' in str(res[0][0]):
        flash('Invalid Username or Password!')
        return redirect(url_for('index'))
    session['username'] = username
    session['logged_in'] = True
    fname = spcall('getfname', (username,), True)
    return render_template('strippers.html', fname=fname[0][0])

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    res = spcall('signup', (username, password, fname, lname), True)
    if 'ID EXIST' in str(res[0][0]):
        flash('Username is used!')
        return redirect('/#signup')
    flash('Success!')
    return render_template('strippers.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    return index()

@app.route('/strippers')
def stripperspage():
    if not session.get('logged_in'):
        flash('You must log-in first!')
        return index()
    user = session['username']
    return render_template('strippers.html')

@app.route('/strippers/tasks', methods=['GET','POST'])
def getstrippers():
    if request.method == 'POST':
        stripid = request.form['stripid']
        passcode = request.form['psw']
        res = spcall('register', (stripid, passcode, session['username']), True)
        if 'Error' in str(res[0][0]):
            return jsonify({'status': 'error', 'message': res[0][0]})
        return jsonify({'status': 'ok', 'message': res[0][0]})
    elif request.method == 'GET':
        res = spcall('getregistered', (session['username'],))
        if 'Error' in str(res[0][0]):
            return jsonify({'status': 'error', 'message': res[0][0]})
        recs = []
        for r in res:
            recs.append({"stripperid": r[0], "status": str(r[1]), "switchvalue": str(r[2])})
        return jsonify({'status': 'ok', 'entries': recs, 'count': len(recs)})

@app.route('/strippers/remove_<string:stripperid>', methods=['POST'])
def stripperdelete(stripperid):
    res = spcall('unregister', (stripperid,), True)
    if 'Error' in str(res[0][0]):
        return jsonify({'status': 'error', 'message': res[0][0]})
    return jsonify({'status': 'ok'})

@app.route('/strippers/switch', methods=['POST'])
def stripperswitch():
    stripid = request.form['stripid']
    switchstate = request.form['switchstate']
    res = spcall('toggleswitch', (stripid,switchstate=="true"), True)
    if 'Error' in str(res[0][0]):
        return jsonify({'status': 'error', 'message': res[0][0]})
    return jsonify({'status': 'ok', 'message': res[0][0]})

@app.after_request
def add_cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = flask.request.headers.get('Origin', '*')
    resp.headers['Access-Control-Allow-Credentials'] = True
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, PUT, DELETE'
    resp.headers['Access-Control-Allow-Headers'] = flask.request.headers.get('Access-Control-Request-Headers',
                                                                             'Authorization')
    if app.debug:
        resp.headers["Access-Control-Max-Age"] = '1'
    return resp

if __name__ == '__main__':
    app.debug=True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
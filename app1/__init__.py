from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import subprocess

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
@app.route('/index')
def index():
    if request.method == 'POST':
        ip = request.form['ip']

    return render_template('index.html', image_url='image.png')

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    if request.method == 'POST':
        ip = request.form['ip']
        cmd = "ping -c 1 %s" % ip
        result=subprocess.check_output(cmd, shell=True)
	return  '<h1>answer: {}</h1>'.format(result)
    if request.method == 'GET':
        query = request.args.get('result')
        if query and query != '':
            return render_template('ping.html', result=result)
        else:
            return render_template('ping.html', result='')

    return render_template('ping.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        posts = conn.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
        print("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))        
        user_id = posts.fetchone()
        if user_id:
            return redirect(url_for('profile', user_id=user_id['id']))
            
	else:
            return "error"
    return render_template('login.html')

@app.route('/article', methods=['GET'])
def article():
    error = 0
    if 'id' in request.args:
        page = request.args.get('id')
    else:
        page = 'article'
    try:
        template='./static/'+page+'.png'
    except Exception as e:
        template = './static/0.png'
    print template
    return send_file(template)

@app.route('/profile/<user_id>')
def profile(user_id):
    conn = get_db_connection()
    posts = conn.execute("SELECT username, name FROM users WHERE id = ?", (user_id))
    user = posts.fetchone()
    return render_template('profile.html', user_id=user_id, username=user['username'] , name=user['name'])

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
	name = request.form['name']  
        conn = get_db_connection()
	cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, name) VALUES (?,?,?)", (username, password, name))
        conn.commit()
        conn.close()
        return "Successfull!"

    return render_template('registration.html')

if __name__ == '__main__':
    app.run()


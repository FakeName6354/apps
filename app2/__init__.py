from flask import Flask, render_template, request, redirect, url_for, send_file, session
import sqlite3
import subprocess
from PIL import Image, ImageDraw, ImageFont
from random import choice, randint
from io import BytesIO
from os import urandom
from flask_sqlalchemy import SQLAlchemy
from flask_sessionstore import Session
import os.path

app = Flask(__name__)
app.secret_key = urandom(24)
#app.config['SECRET_KEY'] = 'secret-key-goes-here'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

#db.init_app(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', image_url='image.png')

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    if request.method == 'POST':
        ip = request.form['ip']
        result=subprocess.check_output(['ping', '-c', '1', ip], shell=False)
#        cmd = "ping -c 1 %s" % ip
#        result=subprocess.check_output(cmd, shell=True)
	return  '<h1>answer: {}</h1>'.format(result)
    if request.method == 'GET':
        query = request.args.get('result')
        if query and query != '':
            return render_template('ping.html', result=result)
        else:
            return render_template('ping.html', result='')

    return render_template('ping.html')

@app.route('/captcha.png', methods=['GET'])
def captcha(width=200, height=100):
    code = ''.join([choice('QERTYUPLKJHGFDSAZXCVBN23456789') for i in range(5)])
    session['code'] = code

    img = Image.new('RGB', (width,height), (255,255,255))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', size=50)
    x=0; y=12;

    for let in code:
        if x == 0: x = 5
        else: x = x + width/5
        y = randint(3,55)
        draw.text((x,y), let, font=font, fill=(randint(0,200), randint(0,200), randint(0,200), 128))


    for i in range(40):
        draw.line([(randint(0,width),randint(0,height)),
                   (randint(0,width),randint(0,height))], 
                  randint(0, 200), 2, 128)

    f = BytesIO()
    img.save(f, "PNG")
    return  f.getvalue()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
#
        input_captcha = request.values.get('input_captcha')
        sess_captcha = session.get('code')
        if str(input_captcha).lower() != str(sess_captcha).lower():
#add checking uniq session
            return 'ERROR'
#            return redirect(url_for('hello'))
#        else:
#            error = True
# return render_template('login.html')    
        session.pop('code', None)
        conn = get_db_connection()
#
# prepared ?
        query = 'SELECT id FROM users WHERE username = ? AND password = ?'
        posts = conn.execute(query, (username, password))

#        posts = conn.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
#        print("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))        
        user_id = posts.fetchone()
        if user_id:
            return redirect(url_for('profile', user_id=int(user_id['id'])))
            
	else:
            return "error"
    return render_template('login.html')

@app.route('/article', methods=['GET']) # still IDOR vulnable
def article():
    error = 0
    if 'id' in request.args:
        page = request.args.get('id')
    else:
        page = 'article'
    try:
        template='./static/'+page+'.png'
#
        template='./static/'+os.path.basename(page)+'.png'
        print template
    except Exception as e:
        template = './static/0.png'
    print template
    try:
        return send_file(template)
    except Exception as e:
        return send_file('./static/0.png')

@app.route('/profile/<int:user_id>')
def profile(user_id):
    conn = get_db_connection()
    posts = conn.execute("SELECT username, name FROM users WHERE id = ?", str(user_id))
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


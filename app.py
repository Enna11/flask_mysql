from flask import Flask, request, redirect, render_template, url_for, flash, jsonify, session, send_file
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from base64 import b64encode, b64decode
import base64
from flask_session import Session  # Importez l'extension Flask Session

app = Flask(__name__)
app.secret_key = "caircocoders-ednalan"

# Configuration de la base de données MySQL
app.config["MYSQL_HOST"] = 'mysql-service'
app.config['MYSQL_USER'] = 'enna'
app.config['MYSQL_PASSWORD'] = 'poiuytre'
app.config['MYSQL_DB'] = 'enameli'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# Configuration de Flask Session
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.config['UPLOAD_FOLDER'] = 'static/uploads'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def execute_sql_file(filename):
    # Lire le contenu du fichier SQL
    with open(filename, 'r') as file:
        sql_file = file.read()

    # Exécuter les commandes SQL dans le fichier
    cursor = mysql.connection.cursor()
    for command in sql_file.split(';'):
        cursor.execute(command)
    mysql.connection.commit()
    cursor.close()

@app.route('/initialize', methods=['GET'])
def initialize_database():
    # Exécuter le fichier SQL pour créer les tables
    execute_sql_file('databases.sql')
    flash('Database initialized successfully!')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Adresse e-mail']
        password = request.form['mot de passe']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['user_id'] = user['id']
            session['user_first_name'] = user['first_name']
            return redirect('/wall')
        else:
            flash('Email ou mot de passe invalide')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['prénom']
        last_name = request.form['nom de famille']
        email = request.form['Adresse e-mail']
        password = request.form['mot de passe']
        gender = request.form['Genre']
        dob = request.form['dob']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (first_name, last_name, email, password, gender, dob) VALUES (%s, %s, %s, %s, %s, %s)", (first_name, last_name, email, password, gender, dob))
        mysql.connection.commit()
        cursor.close()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/wall')
def wall():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM images")
        photos = cursor.fetchall()
        cursor.close()

        for photo in photos:
            if 'image_data' in photo:
                image_data = photo['image_data']
                photo['image_data'] = base64.b64encode(image_data).decode('utf-8')

        return render_template('wall.html', photos=photos)
    else:
        return redirect(url_for('login'))

@app.route('/upload', methods=["POST", "GET"])
def upload():
    if 'user_id' in session:
        if request.method == 'POST':
            cursor = mysql.connection.cursor()
            now = datetime.now()

            if 'photo' not in request.files:
                flash('No file part')
                return redirect('/upload')

            file = request.files['photo']

            if file.filename == '':
                flash('No selected file')
                return redirect('/upload')

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                image_blob = file.read()
                cursor.execute("INSERT INTO images (file_name, image_data, uploaded_on) VALUES (%s, %s, %s)", [filename, image_blob, now])
                mysql.connection.commit()
                cursor.close()
                flash('File uploaded successfully')
                return redirect('/wall')

        return render_template('upload.html')
    else:
        return redirect(url_for('login'))

@app.route('/like/<int:photo_id>', methods=["POST"])
def like(photo_id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE images SET likes = likes + 1 WHERE id = %s", (photo_id,))
    mysql.connection.commit()

    cursor.execute("SELECT likes FROM images WHERE id = %s", (photo_id,))
    likes = cursor.fetchone()['likes']
    cursor.close()

    return jsonify({'likes': likes})

@app.route('/comment/<int:image_id>', methods=['POST'])
def comment_image(image_id):
    if 'user_id' in session:
        comment = request.form.get('comment')
        user_id = session['user_id']  # Récupérer l'ID de l'utilisateur à partir de la session
        user_first_name = session ['user_first_name']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO comments (image_id, user_id, comment) VALUES (%s, %s, %s)", (image_id, user_id, comment))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'comment': comment})
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

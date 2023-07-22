from flask import Flask, request, redirect, render_template, url_for, flash, jsonify, session, send_file
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
from datetime import datetime


app = Flask(__name__)
app.secret_key = "caircocoders-ednalan"

# Configuration de la base de données MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'enameli'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


app.config['UPLOAD_FOLDER'] = 'static/uploads'


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' in session:
        return redirect('/wall')

    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect('/wall')
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        dob = request.form['dob']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password, gender, dob) VALUES (%s, %s, %s, %s, %s)", (name, email, password, gender, dob))
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

                # Enregistrement de l'image en tant que BLOB dans la base de données
                image_blob = file.read()
                cursor.execute("INSERT INTO images (file_name, image_data, uploaded_on) VALUES (%s, %s, %s)", [filename, image_blob, now])
                mysql.connection.commit()
                cursor.close()
                flash('File successfully uploaded')

                # Enregistrement de l'image dans le dossier "static/uploads"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                return redirect(url_for('wall'))
            else:
                flash('Invalid file format')
                return redirect('/upload')

        return render_template('upload.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/photo/<int:photo_id>', methods=['GET'])
def show_photo(photo_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM images WHERE id = %s", (photo_id,))
    photo_data = cursor.fetchone()
    cursor.close()

    if photo_data and 'file_name' in photo_data:
        return render_template('photo.html', photo_data=photo_data)
    else:
        return "Photo not found"

@app.route('/like/<int:image_id>', methods=['POST'])
def like_image(image_id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE images SET likes = likes + 1 WHERE id = %s", (image_id,))
    mysql.connection.commit()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT likes FROM images WHERE id = %s", (image_id,))
    likes = cursor.fetchone()['likes']
    cursor.close()

    return jsonify({'likes': likes})

@app.route('/comment/<int:image_id>', methods=['POST'])
def comment_image(image_id):
    if 'user_id' in session:
        comment = request.form.get('comment')

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO comments (image_id, user_id, comment) VALUES (%s, %s, %s)", (image_id, session['user_id'], comment))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'comment': comment})
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

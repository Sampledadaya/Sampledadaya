from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os
import MySQLdb  # Для обработки ошибок

app = Flask(__name__)

# Конфигурация MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Замените на IP-адрес вашего сервера, если необходимо
app.config['MYSQL_USER'] = 'u2838078_default'
app.config['MYSQL_PASSWORD'] = 'VcakTQ12YUL788zk'
app.config['MYSQL_DB'] = 'u2838078_sampledadaya'

# Директория для загрузки файлов
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Убедитесь, что директория существует
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Секретный ключ для Flask
app.secret_key = os.urandom(24)  # Генерация случайного ключа

# Инициализация MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            try:
                # Пример кода для обновления базы данных
                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO files (filename) VALUES (%s)", (file.filename,))
                mysql.connection.commit()
                cursor.close()
                flash('Файл успешно загружен!')
            except MySQLdb.Error as e:
                flash('Ошибка при загрузке файла в базу данных: {}'.format(e))
                mysql.connection.rollback()
            return redirect(url_for('report'))
    return render_template('report.html')

@app.route('/games')
def games():
    return render_template('games.html')

if __name__ == '__main__':
    app.run(debug=True)

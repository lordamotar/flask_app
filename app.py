from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Price, Team
from flask_migrate import Migrate
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///video.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'static/uploads/team'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Инициализируем базу данных с нашим приложением
db.init_app(app)

# После создания приложения и инициализации db
migrate = Migrate(app, db)


@app.route('/')
def index():
    prices = Price.query.all()
    teams = Team.query.all()
    return render_template('index.html', prices=prices, teams=teams)


@app.route('/add', methods=['GET', 'POST'])
def add_price():
    if request.method == 'POST':
        title = request.form['title']
        price = float(request.form['price'])
        description = request.form['description']
        detail = request.form['detail']
        new_price = Price(title=title, price=price, description=description, detail=detail)
        db.session.add(new_price)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/team')
def team():
    team_members = Team.query.all()
    return render_template('team.html', team_members=team_members)


@app.route('/team/add', methods=['GET', 'POST'])
def add_team_member():
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Создаем уникальное имя файла
            unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

            name = request.form['name']
            position = request.form['position']
            text = request.form['text']
            description = request.form['description']
            facebook = request.form['facebook']
            instagram = request.form['instagram']
            whatsapp = request.form['whatsapp']
            telegram = request.form['telegram']

            new_member = Team(
                name=name,
                position=position,
                photo_filename=unique_filename,
                text=text,
                description=description,
                facebook=facebook,
                instagram=instagram,
                whatsapp=whatsapp,
                telegram=telegram
            )

            db.session.add(new_member)
            db.session.commit()

            return redirect(url_for('team'))
    return render_template('add_team.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

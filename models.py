from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    detail = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Price {self.title}>'


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100), nullable=True)
    text = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    facebook = db.Column(db.String(100), nullable=True)
    instagram = db.Column(db.String(100), nullable=True)
    whatsapp = db.Column(db.String(100), nullable=True)
    telegram = db.Column(db.String(100), nullable=True)
    photo_filename = db.Column(
        db.String(255)
    )

    def __repr__(self):
        return f'<Team {self.name}>'

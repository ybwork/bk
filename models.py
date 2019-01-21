from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    key = db.Column(db.String(16), unique=True, nullable=False)

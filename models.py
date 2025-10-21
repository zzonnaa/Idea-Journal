from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(200), nullable=True)  # comma-separated

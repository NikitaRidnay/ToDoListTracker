# models.py
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    info = db.Column(db.String(500), nullable=True)  # Новое поле для основной информации
    is_task = db.Column(db.Boolean, default=False)
    timer = db.Column(db.DateTime, nullable=True)
    is_completed = db.Column(db.Boolean, default=False) 
    is_expired = db.Column(db.Boolean, default=False)  

    def __repr__(self):
        return f'<Note {self.content}>'

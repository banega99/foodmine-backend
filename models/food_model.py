
from datetime import datetime
from extensions.database import db


class Food(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    tags = db.Column(db.PickleType, nullable=True)  # List of strings
    favorite = db.Column(db.Boolean, default=False)
    stars = db.Column(db.Float, nullable=False)
    imageUrl = db.Column(db.String(255), nullable=False)
    origins = db.Column(db.PickleType, nullable=True)  # List of strings
    cookTime = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from extensions.database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    password = Column(String, nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow())
    isAdmin = Column(Boolean, nullable=False, default=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name}, address={self.address}, isAdmin={self.isAdmin})>"

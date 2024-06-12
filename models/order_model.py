from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from extensions.database import db
from datetime import datetime


class LatLng(db.Model):
    __tablename__ = 'latlng'
    id = Column(Integer, primary_key=True)
    lat = Column(String, nullable=False)
    lng = Column(String, nullable=False)


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key=True)
    food_id = Column(Integer, ForeignKey('foods.id'), nullable=False)
    food = relationship('Food', backref='order_items')
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)

    def as_dict(self):
        item_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        item_dict['food'] = self.food.as_dict()  # Add the food details to the dict
        return item_dict


class Order(db.Model):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    address_latlng_id = Column(Integer, ForeignKey('latlng.id'), nullable=False)
    address_latlng = relationship('LatLng', backref='orders')
    payment_id = Column(String, nullable=False, autoincrement=True)
    total_price = Column(Float, nullable=False)
    status = Column(String, default='NEW')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='orders')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

    def as_dict(self):
        order_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        order_dict['items'] = [item.as_dict() for item in self.items]
        return order_dict

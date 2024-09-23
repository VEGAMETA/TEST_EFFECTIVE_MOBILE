from enum import StrEnum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, func

from .database import Base


class OrderStatus(StrEnum):
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    status = Column(Enum(OrderStatus), default=OrderStatus.processing)
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

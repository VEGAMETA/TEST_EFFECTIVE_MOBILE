from enum import StrEnum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    order_id: int


class OrderStatusEnum(StrEnum):
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"


class OrderBase(BaseModel):
    status: OrderStatusEnum


class OrderPatch(OrderBase):
    status: Optional[OrderStatusEnum]


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    items: List[OrderItem]

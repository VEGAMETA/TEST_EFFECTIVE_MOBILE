from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload

from . import models, schemas


# CRUD for pruducts
async def get_product(db: Session, product_id: int):
    return await db.get(models.Product, product_id)


async def get_products(db: Session, offset: int = 0, limit: int = 100):
    db_products = await db.execute(select(models.Product).offset(offset).limit(limit))
    return db_products.scalars().all()


async def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = await db.get(models.Product, product_id)
    if db_product:
        for key, value in product.model_dump().items():
            setattr(db_product, key, value)
        await db.commit()
        await db.refresh(db_product)
    return db_product


async def delete_product(db: Session, product_id: int):
    db_product = await db.get(models.Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(db_product)
    await db.commit()
    return db_product


# CRUD for orders
async def get_order(db: Session, order_id: int):
    query = select(models.Order).options(selectinload(models.Order.items)).where(models.Order.id == order_id)
    db_order = await db.execute(query)
    return db_order.scalar_one_or_none()

async def get_orders(db: Session, offset: int = 0, limit: int = 100):
    query = select(models.Order).options(selectinload(models.Order.items)).offset(offset).limit(limit)
    db_orders = await db.execute(query)
    return db_orders.scalars().all()

async def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(status=order.status)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    for item in order.items:
        product = await db.get(models.Product, item.product_id)
        if not product or product.quantity < item.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        product.quantity -= item.quantity
        order_item = models.OrderItem(order_id=db_order.id, product_id=item.product_id, quantity=item.quantity)
        db.add(order_item)
    await db.commit()
    await db.refresh(db_order)
    return await get_order(db, db_order.id)


async def update_order_status(db: Session, order_id: int, status: schemas.OrderPatch):
    db_order = await db.get(models.Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail=f"Order not found")
    db_order.status = status.status
    await db.commit()
    await db.refresh(db_order)
    return await get_order(db, db_order.id)

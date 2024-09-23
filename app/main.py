from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException
from fastapi.concurrency import asynccontextmanager

from . import schemas, crud
from .database import engine, get_db, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


# Products endpoints
@app.post("/products", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_product(db, product)


@app.get("/products", response_model=List[schemas.Product])
async def get_products(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    products = await crud.get_products(db, offset=offset, limit=limit)
    if not products:
        raise HTTPException(status_code=404, detail="Products not found")
    return products


@app.get("/products/{product_id}", response_model=schemas.Product)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=schemas.Product)
async def update_product(product_id: int, product: schemas.ProductUpdate, db: AsyncSession = Depends(get_db)):
    product = await crud.update_product(db, product_id, product)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.delete("/products/{product_id}", response_model=schemas.Product)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_product(db, product_id)


# Orders endpoints
@app.post("/orders", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):
    order = await crud.create_order(db, order)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.get("/orders", response_model=List[schemas.Order])
async def read_orders(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    orders = await crud.get_orders(db, offset=offset, limit=limit)
    if not orders:
        raise HTTPException(status_code=404, detail="Orders not found")
    return orders


@app.get("/orders/{order_id}", response_model=schemas.Order)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.patch("/orders/{order_id}/status", response_model=schemas.Order)
async def update_order_status(order_id: int, status: schemas.OrderPatch, db: AsyncSession = Depends(get_db)):
    order = await crud.update_order_status(db, order_id, status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

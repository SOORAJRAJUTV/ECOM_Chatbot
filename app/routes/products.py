from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from ..db import engine
from functools import lru_cache

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def list_products():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, name, sku, price, stock FROM products")).mappings().all()
        return {"products": [dict(r) for r in rows]}

# simple cached lookup
@lru_cache(maxsize=128)
def _get_product_cached(pid: int):
    with engine.connect() as conn:
        return conn.execute(text("SELECT id, name, sku, price, stock FROM products WHERE id = :pid"), {"pid": pid}).mappings().first()

@router.get("/{product_id}")
def get_product(product_id: int):
    row = _get_product_cached(product_id)
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return dict(row)

from fastapi import APIRouter
from sqlalchemy import text
from ..db import engine

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/{customer_id}/orders")
def get_customer_orders(customer_id: int):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, status, order_total, order_date
            FROM orders WHERE customer_id = :cid
        """), {"cid": customer_id}).mappings().all()
        return {"orders": [dict(r) for r in result]}

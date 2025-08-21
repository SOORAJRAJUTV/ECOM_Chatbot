from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from ..db import engine

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/{order_id}")
def get_order(order_id: int):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT o.id, c.name as customer, o.status, o.order_total, o.order_date
            FROM orders o
            JOIN customers c ON c.id = o.customer_id
            WHERE o.id = :oid
        """), {"oid": order_id}).mappings().first()

        if not result:
            raise HTTPException(status_code=404, detail="Order not found")
        return dict(result)

#address
#card
#user
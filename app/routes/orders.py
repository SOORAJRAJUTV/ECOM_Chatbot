from fastapi import APIRouter, HTTPException, Header, Depends
from sqlalchemy import text
from ..db import engine
from ..models import UserAuth
from typing import Optional

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_user_by_account(account_number: Optional[str]):
    if not account_number:
        raise HTTPException(status_code=401, detail="Missing account number header")
    with engine.connect() as conn:
        row = conn.execute(text("SELECT * FROM users WHERE account_number = :acc"), {"acc": account_number}).mappings().first()
        if not row:
            raise HTTPException(status_code=401, detail="Account not found")
        return dict(row)

@router.get("/my", summary="List my orders (requires X-Account-Number header)")
def list_my_orders(x_account_number: Optional[str] = Header(None)):
    user = get_user_by_account(x_account_number)
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, order_number, status, total, created_at FROM orders WHERE user_id = :uid ORDER BY created_at DESC"), {"uid": user["id"]}).mappings().all()
        return {"orders": [dict(r) for r in rows]}

@router.get("/{order_id}", summary="Get a specific order (ensures ownership)")
def get_order(order_id: int, x_account_number: Optional[str] = Header(None)):
    user = get_user_by_account(x_account_number)
    with engine.connect() as conn:
        row = conn.execute(text("SELECT * FROM orders WHERE id = :oid AND user_id = :uid"), {"oid": order_id, "uid": user["id"]}).mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found or not owned by user")
        # fetch items
        items = conn.execute(text("SELECT oi.*, p.name, p.sku FROM order_items oi JOIN products p ON p.id = oi.product_id WHERE oi.order_id = :oid"), {"oid": order_id}).mappings().all()
        return {"order": dict(row), "items": [dict(i) for i in items]}


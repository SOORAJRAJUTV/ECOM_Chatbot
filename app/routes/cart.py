from fastapi import APIRouter, HTTPException, Header
from sqlalchemy import text
from ..db import engine
from ..models import CreateOrder
from typing import List

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/create-order")
def create_order(payload: CreateOrder):
    # validate user
    with engine.connect() as conn:
        user = conn.execute(text("SELECT id FROM users WHERE account_number = :acc"), {"acc": payload.account_number}).mappings().first()
        if not user:
            raise HTTPException(status_code=400, detail="Invalid account number")
        user_id = user["id"]

        # compute totals simply
        subtotal = 0.0
        for it in payload.items:
            prod = conn.execute(text("SELECT price FROM products WHERE id = :pid"), {"pid": it.product_id}).mappings().first()
            if not prod:
                raise HTTPException(status_code=400, detail=f"Product {it.product_id} not found")
            subtotal += prod["price"] * it.qty

        tax = round(subtotal * 0.07, 2)  # simple 7% tax
        shipping_cost = 20.0
        total = subtotal + tax + shipping_cost

        # insert order
        res = conn.execute(text("""INSERT INTO orders (user_id, status, order_number, billing_address_id, shipping_address_id, payment_method, subtotal, tax, shipping_cost, total, created_at, updated_at)
            VALUES (:user_id, 'Pending', :order_number, :bill, :ship, :pm, :subtotal, :tax, :shipc, :total, :now, :now)"""),
            {
                "user_id": user_id,
                "order_number": f"ORD{int(datetime.datetime.now().timestamp())}",
                "bill": payload.billing_address_id,
                "ship": payload.shipping_address_id,
                "pm": payload.payment_method,
                "subtotal": subtotal,
                "tax": tax,
                "shipc": shipping_cost,
                "total": total,
                "now": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
        order_id = res.lastrowid

        # insert items
        for it in payload.items:
            prod = conn.execute(text("SELECT price FROM products WHERE id = :pid"), {"pid": it.product_id}).mappings().first()
            line_total = prod["price"] * it.qty
            conn.execute(text("INSERT INTO order_items (order_id, product_id, qty, unit_price, line_total) VALUES (:oid, :pid, :qty, :unit_price, :lt)"),
                         {"oid": order_id, "pid": it.product_id, "qty": it.qty, "unit_price": prod["price"], "lt": line_total})
        conn.commit()
        return {"order_id": order_id, "total": total}

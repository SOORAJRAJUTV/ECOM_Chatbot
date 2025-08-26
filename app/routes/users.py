from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from ..db import engine

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{account_number}")
def get_user_by_account(account_number: str):
    with engine.connect() as conn:
        row = conn.execute(text("SELECT * FROM users WHERE account_number = :acc"), {"acc": account_number}).mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        return dict(row)

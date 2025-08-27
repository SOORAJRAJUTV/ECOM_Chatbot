from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class UserAuth(BaseModel):
    account_number: Optional[str] = Field(None, description="Account number to identify user (simple auth)")

class ChatRequest(BaseModel):
    question: str
    account_number: Optional[str] = None  # enforces user context

class CreateOrderItem(BaseModel):
    product_id: int
    qty: int = Field(..., ge=1)

class CreateOrder(BaseModel):
    account_number: str
    billing_address_id: int
    shipping_address_id: int
    payment_method: str
    items: List[CreateOrderItem]


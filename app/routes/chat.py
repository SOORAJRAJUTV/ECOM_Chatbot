from fastapi import APIRouter, HTTPException, Header
from ..models import ChatRequest
from ..llm import agent, SYSTEM_INSTRUCTION
from ..memory import add_user_message, add_bot_message, get_memory_snippet, set_last_order
from ..db import engine
from sqlalchemy import text
import re

router = APIRouter(prefix="/chat", tags=["Chatbot"])

def ensure_user(account_number: str):
    if not account_number:
        raise HTTPException(status_code=401, detail="Missing account_number in request")
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT id, first_name, last_name FROM users WHERE account_number = :acc"),
            {"acc": account_number}
        ).mappings().first()
        if not row:
            raise HTTPException(status_code=401, detail="Invalid account number")
        return dict(row)

@router.post("/")
def chat(req: ChatRequest):
    acct = req.account_number
    user = ensure_user(acct)
    user_key = f"user:{acct}"

    # Save user message
    add_user_message(user_key, req.question)

    # Build context with system instruction & memory
    memory_snippet = get_memory_snippet(user_key, lines=6)
    context_prefix = (
        f"{SYSTEM_INSTRUCTION}\n"
        f"You are a helpful support chatbot. Always greet the user by first name. "
        f"Provide clear, human-readable answers, not raw SQL or technical text.\n"
        f"User context: account_number={acct}, user_id={user['id']}, name={user['first_name']} {user['last_name']}\n"
        f"If executing SQL, only query orders where user_id = {user['id']}.\n"
        f"Conversation history:\n{memory_snippet}\n"
        f"User question: {req.question}\n"
    )

    try:
        raw = agent.run(context_prefix)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Post-process the raw response
    answer = raw.split("\n\n")[0].split("\n")[0].strip()

    # Make response conversational
    # Example: "Hi John, your total order is $1370.00."
    first_name = user['first_name']
    if "total" in req.question.lower() and re.search(r"\d+(\.\d+)?", answer):
        match = re.search(r"(\d+(\.\d+)?)", answer)
        if match:
            total = match.group(1)
            answer = f" your total order amount is ${total}."
    elif "status" in req.question.lower():
        answer = f"Hi {first_name}, {answer}"
    else:
        answer = f"Hi {first_name}, {answer}"

    # Track last order if mentioned
    m = re.search(r"\border(?: number)?\s*(?:#|:)?\s*([A-Za-z0-9\-]+)", answer, re.IGNORECASE)
    if m:
        order_number = m.group(1)
        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT id FROM orders WHERE order_number = :on AND user_id = :uid"),
                {"on": order_number, "uid": user["id"]}
            ).mappings().first()
            if row:
                set_last_order(user_key, row["id"])

    # Save bot response to memory
    add_bot_message(user_key, answer)

    return {"answer": answer}




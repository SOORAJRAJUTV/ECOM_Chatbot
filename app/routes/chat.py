from fastapi import APIRouter, HTTPException
from ..models import ChatRequest
from ..llm import agent, SYSTEM_INSTRUCTION
from ..memory import add_user_message, add_bot_message, get_memory_snippet, set_last_order
from ..db import engine
from sqlalchemy import text
import re
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv
load_dotenv()  # read .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# import embeddings
from ..embeddings import load_faiss_index
from langchain.chains import RetrievalQA


router = APIRouter(prefix="/chat", tags=["Chatbot"])

# load FAISS at startup
vectorstore = load_faiss_index()
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
product_qa = RetrievalQA.from_chain_type(
    llm=ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="Llama3-8b-8192",
    streaming=False,
    temperature=0
),
    retriever=retriever,
    return_source_documents=True
)

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

    first_name = user["first_name"]

    # --- Decide if query is about products or orders ---
    q_lower = req.question.lower()
    is_product_query = any(word in q_lower for word in ["product", "recommend", "buy", "shoes", "dress", "discount", "sale"])

    if is_product_query:
        # ---- FAISS product search ----
        try:
            response = product_qa.invoke({"query": req.question})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Product search failed: {e}")

        answer = response["result"].strip()
        sources = [doc.metadata for doc in response["source_documents"]]

        # build nice response
        product_lines = []
        for src in sources:
            product_lines.append(f"- {src['name']} (${src['price']})")

        if product_lines:
            answer += f"\nHere are some matching products:\n" + "\n".join(product_lines)

        final_answer = f"Hi {first_name}, {answer}"

    else:
        # ---- SQL agent for orders ----
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

        answer = raw.split("\n\n")[0].split("\n")[0].strip()

        if "total" in q_lower and re.search(r"\d+(\.\d+)?", answer):
            match = re.search(r"(\d+(\.\d+)?)", answer)
            if match:
                total = match.group(1)
                answer = f"your total order amount is ${total}."
        elif "status" in q_lower:
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

        final_answer = answer

    # Save bot response to memory
    add_bot_message(user_key, final_answer)

    return {"answer": final_answer}

























# from fastapi import APIRouter, HTTPException, Header
# from ..models import ChatRequest
# from ..llm import agent, SYSTEM_INSTRUCTION
# from ..memory import add_user_message, add_bot_message, get_memory_snippet, set_last_order
# from ..db import engine
# from sqlalchemy import text
# import re

# router = APIRouter(prefix="/chat", tags=["Chatbot"])

# def ensure_user(account_number: str):
#     if not account_number:
#         raise HTTPException(status_code=401, detail="Missing account_number in request")
#     with engine.connect() as conn:
#         row = conn.execute(
#             text("SELECT id, first_name, last_name FROM users WHERE account_number = :acc"),
#             {"acc": account_number}
#         ).mappings().first()
#         if not row:
#             raise HTTPException(status_code=401, detail="Invalid account number")
#         return dict(row)

# @router.post("/")
# def chat(req: ChatRequest):
#     acct = req.account_number
#     user = ensure_user(acct)
#     user_key = f"user:{acct}"

#     # Save user message
#     add_user_message(user_key, req.question)

#     # Build context with system instruction & memory
#     memory_snippet = get_memory_snippet(user_key, lines=6)
#     context_prefix = (
#         f"{SYSTEM_INSTRUCTION}\n"
#         f"You are a helpful support chatbot. Always greet the user by first name. "
#         f"Provide clear, human-readable answers, not raw SQL or technical text.\n"
#         f"User context: account_number={acct}, user_id={user['id']}, name={user['first_name']} {user['last_name']}\n"
#         f"If executing SQL, only query orders where user_id = {user['id']}.\n"
#         f"Conversation history:\n{memory_snippet}\n"
#         f"User question: {req.question}\n"
#     )

#     try:
#         raw = agent.run(context_prefix)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#     # Post-process the raw response
#     answer = raw.split("\n\n")[0].split("\n")[0].strip()

#     # Make response conversational
#     # Example: "Hi John, your total order is $1370.00."
#     first_name = user['first_name']
#     if "total" in req.question.lower() and re.search(r"\d+(\.\d+)?", answer):
#         match = re.search(r"(\d+(\.\d+)?)", answer)
#         if match:
#             total = match.group(1)
#             answer = f" your total order amount is ${total}."
#     elif "status" in req.question.lower():
#         answer = f"Hi {first_name}, {answer}"
#     else:
#         answer = f"Hi {first_name}, {answer}"

#     # Track last order if mentioned
#     m = re.search(r"\border(?: number)?\s*(?:#|:)?\s*([A-Za-z0-9\-]+)", answer, re.IGNORECASE)
#     if m:
#         order_number = m.group(1)
#         with engine.connect() as conn:
#             row = conn.execute(
#                 text("SELECT id FROM orders WHERE order_number = :on AND user_id = :uid"),
#                 {"on": order_number, "uid": user["id"]}
#             ).mappings().first()
#             if row:
#                 set_last_order(user_key, row["id"])

#     # Save bot response to memory
#     add_bot_message(user_key, answer)

#     return {"answer": answer}




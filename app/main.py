from fastapi import FastAPI
from .routes import chat, orders, customers

app = FastAPI(title="E-commerce SQL Chatbot")

@app.get("/")
def root():
    return {"status": "ok", "msg": "E-commerce SQL Chatbot API running"}

# Register routers
app.include_router(chat.router)
app.include_router(orders.router)
app.include_router(customers.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

# http://127.0.0.1:8000/
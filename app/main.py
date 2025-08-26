from fastapi import FastAPI
from .routes import users, products, orders, cart, chat

app = FastAPI(title="E-commerce Chatbot API")

@app.get("/")
def root():
    return {"status": "ok", "msg": "E-commerce SQL Chatbot API running"}

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(cart.router)
app.include_router(chat.router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)









# from fastapi import FastAPI
# from .routes import chat, orders, customers

# app = FastAPI(title="E-commerce SQL Chatbot")

# @app.get("/")
# def root():
#     return {"status": "ok", "msg": "E-commerce SQL Chatbot API running"}

# # Register routers
# app.include_router(chat.router)
# app.include_router(orders.router)
# app.include_router(customers.router)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

# python -m app.main
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs

# What is my order total for order 1?
# What is the status of that order?
# What is the shipping address of my last order?
# Show me all my pending orders.
# Which product is out of stock?
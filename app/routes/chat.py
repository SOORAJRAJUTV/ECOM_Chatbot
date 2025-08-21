# from fastapi import APIRouter, HTTPException
# from ..models import ChatRequest
# from ..llm import agent

# router = APIRouter(prefix="/chat", tags=["Chatbot"])

# @router.post("/")
# def chat(req: ChatRequest):
#     try:
#         response = agent.run(req.question)
#         return {"answer": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException
from ..models import ChatRequest
from ..llm import agent

router = APIRouter(prefix="/chat", tags=["Chatbot"])

@router.post("/")
def chat(req: ChatRequest):
    try:
        response = agent.run(req.question)
        
        # ✅ Extract only the first line (before any explanation)
        clean_response = response.split("\n")[0].strip()
        
        return {"answer": clean_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

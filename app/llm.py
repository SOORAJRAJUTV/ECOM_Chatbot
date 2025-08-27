from langchain_groq import ChatGroq
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType
from .db import db
from .config import GROQ_API_KEY

# System prompt / instruction to the LLM to be concise and not print SQL or explanations.
SYSTEM_INSTRUCTION = (
    "You are an e-commerce support assistant. Answer in one short sentence or a short JSON if requested. "
    "Do NOT include SQL or internal reasoning in the output. "
    "When given a user context (user_id or account_number), ONLY return data for that user. "
    "When asked about order details, include order_number, status, and tracking_number if available."
)

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="Llama3-8b-8192",
    streaming=False,
    temperature=0
)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True
)

















from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from .config import DB_PATH

engine = create_engine(DB_PATH, echo=False, future=True)
db = SQLDatabase(engine)

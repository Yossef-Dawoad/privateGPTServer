import sqlalchemy as sa 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ChatHistory(Base):
    __tabelname__ = 'chat_history' 
    id  = sa.Column(sa.Integer, primary_key=True, index=True)
    query = sa.Column(sa.String, nullable=False)
    response = sa.Column(sa.String)
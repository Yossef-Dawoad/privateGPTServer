from pydantic import BaseModel


class ChatHistory(BaseModel):
    query: str
    response: str

    class Config:
        orm_mode = True
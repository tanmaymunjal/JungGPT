from pydantic import BaseModel


class ChatPydanticModel(BaseModel):
    prompt: str

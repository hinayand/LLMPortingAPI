from pydantic import BaseModel


class ContentModel(BaseModel):
    role: str
    content: str


class ChatRequestModel(BaseModel):
    channel_name: str = "magic"
    model: str = "gpt-3.5-turbo"
    messages: list[ContentModel]
    api_key: str

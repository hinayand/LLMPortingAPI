import openai

from models.ChatRequestModels import ChatRequestModel


def gennerate_event(channel, request: ChatRequestModel):
    openai.api_base = channel["channel_api_url"]
    openai.api_key = channel["channel_key"]
    openai_history = []
    for message in request.messages:
        openai_history.append({
            "role": message.role,
            "content": message.content
        })
    response = openai.ChatCompletion.create(
        model=request.model,
        messages=openai_history,
        stream=True
    )
    for chunk in response:
        try:
            yield {
                "event": "add",
                "data": chunk.choices[0].delta.content
            }
        except AttributeError:
            yield {
                "event": "end-or-start",
                "data": None
            }

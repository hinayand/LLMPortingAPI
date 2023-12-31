import zhipuai

from models.ChatRequestModels import ChatRequestModel


def gennerate_event(channel, request: ChatRequestModel):
    zhipuai.api_key = channel["channel_key"]
    zhipuai_history = []
    for message in request.messages:
        zhipuai_history.append({
            "role": message.role,
            "content": message.content
        })
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_turbo",
        prompt=zhipuai_history,
    )
    for event in response.events():
        if event.event == "add":
            yield {
                "event": "add",
                "data": event.data
            }
        elif event.event == "error" or event.event == "interrupted":
            yield {
                "event": "end-or-start",
                "data": None
            }
        elif event.event == "finish":
            yield {
                "event": "end-or-start",
                "data": None
            }

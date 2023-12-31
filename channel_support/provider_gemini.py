import requests

from models.ChatRequestModels import ChatRequestModel


def gennerate_event(channel, request: ChatRequestModel):
    api_url = channel["channel_api_url"]
    api_key = channel["channel_key"]
    url = api_url + api_key
    gemini_history = []
    for message in request.messages:
        gemini_history.append({
            "role": message.role if message.role == "user" else "model",
            "parts": [{
                "text": message.content
            }]
        })
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": gemini_history
    }
    gemini_request = requests.post(url=url, headers=header, json=data)
    if gemini_request.status_code == 200:
        yield {
            "event": "end-or-start",
            "data": gemini_request.json()["candidates"][0]["content"]["parts"][-1]["text"]
        }
    else:
        yield {
            "event": "end-or-start",
            "data": None
        }
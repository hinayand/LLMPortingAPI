import os
import requests
from typing import Optional
from fastapi import FastAPI, Header, HTTPException
from sse_starlette.sse import EventSourceResponse

from utils.config_tools import load_config_from_json
from models.ChatRequestModels import ChatRequestModel
from channel_support import provider_gemini, provider_openai, provider_zhipu_ai


class LLMPortingAPI:
    def __init__(self):
        self.app = FastAPI(
            docs_url="/",
            title="LLM Porting API",
            version="v1.0"
        )
        
        self.channels = []
        self.models = {}
        
        self.setup_routers()
        self.setup_channels()

    def setup_channels(self):
        # 从json文件中加载频道注册信息
        self.channels = load_config_from_json("./config/channel_register.json")
        
        # 遍历频道列表
        for channel in self.channels:
            # 为每个频道创建一个空模型列表
            self.models[channel["channel_name"]] = []
            
            # 根据频道类型进行不同的操作
            match channel["channel_type"]:
                # 对于类型为"openai"的频道
                case "openai":
                    # 发送请求获取模型信息
                    models = requests.get(
                        channel["channel_api_url"] + "/models",
                        headers={"Authorization": "Bearer " + channel["channel_key"]},
                    ).json()
                    
                    try:
                        # 如果返回的结果包含"data"字段
                        for model in models["data"]:
                            # 将模型添加到该频道的模型列表中
                            self.models[channel["channel_name"]].append(model)
                    except:
                        # 如果返回的结果不包含"data"字段
                        for model in models:
                            # 将模型添加到该频道的模型列表中
                            self.models[channel["channel_name"]].append(model)
                
                # 对于类型为"gemini"的频道
                case "gemini":
                    # 将指定的模型添加到该频道的模型列表中
                    self.models[channel["channel_name"]].append({
                        "id": "gemini-pro"
                    })
                
                # 对于类型为"zhipu_ai"的频道
                case "zhipu_ai":
                    # 将指定的模型添加到该频道的模型列表中
                    self.models[channel["channel_name"]].append({
                        "id": "chatglm-turbo"
                    })

    def get_models(self):
        return {
            "data": self.models
        }
    
    def chat(self, request: ChatRequestModel):
        if request.api_key == os.environ.get("API_KEY"):
            found_channel = any(request.channel_name == channel["channel_name"] for channel in self.channels)

            if found_channel:
                found_model = any(request.model == model["id"] for model in self.models[request.channel_name])
                if found_model:
                    for channel in self.channels:
                        if channel["channel_name"] == request.channel_name:
                            match channel["channel_type"]:
                                case "openai":
                                    return EventSourceResponse(provider_openai.gennerate_event(channel, request))
                                case "gemini":
                                    return EventSourceResponse(provider_gemini.gennerate_event(channel, request))
                                case "zhipu_ai":
                                    return EventSourceResponse(provider_zhipu_ai.gennerate_event(channel, request))
                else:
                    return {
                        "error": "Model not in this channel"
                    }
            else:
                return {
                    "error": "Channel not found"
                }
        else:
            raise HTTPException(status_code=403, detail="Unauthorization access!")

    
    def setup_routers(self):
        self.app.get("/v1/models")(self.get_models)
        self.app.post("/v1/chat/completion", summary="Chat with a model")(self.chat)

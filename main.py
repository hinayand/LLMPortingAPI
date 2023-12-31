import uvicorn
from apis.LLMPortingAPI import LLMPortingAPI


api = LLMPortingAPI()
app = api.app

if __name__ == "__main__":
    uvicorn.run(app="__main__:app", host="localhost", port=8080, reload=True)

# LLMPortingAPI

## 简介
这是一个大语言模型API的转发API，旨在让开发者可以忽略不同LLM之间的API调用差异，方便的进行开发。

请注意：这个项目创建的API的调用方式不是标准SSE调用，所以无法使用OpenAI库来调用，需要自己写调用函数。

## 部署

### 部署要求
- **Python版本不低于Python3.11**
- **需要可以联网的运行环境**
- 如果你想**使用OpenAI官方API、Google Gemini官方API作为通道**，您可能需要**科学上网环境**

### 部署
目前，这个项目还没实现Docker部署，所以您只能手动部署

1. 安装依赖
   ```bash
   pip install -r reqirements.txt
   ```
2. 配置渠道
   1. 复制一份`config/channel_register_example.json`并且重命名为`channel_register.json`
   2. 根据你的需要更改配置文件
      | 键 | 说明 |
      |----|----|
      | `channel_name` | 渠道的名字 |
      | `channel_type` | 渠道的种类（目前只有`openai`、`gemini`、`zhipu_ai`三种 |
      | `channel_api_url` | 对于openai类渠道，指的是Base URL；对于gemini，是类似于`https://gemini.baipiao.io/v1beta/models/gemini-pro:generateContent?key=`的URL；对于zhipu_ai，这一个键的值无效 |
      | `channel_key` | `channel_api_url`的调用key |
3. 配置环境变量
   | 键 | 说明 |
   |----|----|
   | `API_KEY` | 调用LLMPortingAPI的API Key，需要在请求体内传入 |
4. Enjoy it!

## 调用
目前这个项目提供的API的调用方法比较简单，你可以在`http://localhost:8080/`中的`SwaggerUI`中去调试接口，去了解接口的运行机制。

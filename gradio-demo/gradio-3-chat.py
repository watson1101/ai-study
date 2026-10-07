####

import os
from urllib import response

import gradio as gr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 1.加载 .env 中的环境变量
load_dotenv()

# 2.初始化 LangChain 的 ChatOpenAI (兼容 deepseek)
llm = ChatOpenAI(
    model = "deepseek-chat",
    # base_url = os.getenv("BASE_URL"),
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("API_KEY"),
    # api_key = "sk-xxx",
    temperature = 0.7,
    streaming = True,
)

#  核心聊天函数
def chat_with_deepseek(message:str,history:list):
    # 处理用户消息和对话历史，调用 deepseek api 并流失返回回复
    # args：
    #     message：用户输出
    #     history：对话历史，格式为 [{"role":"user","content":"xx"},xxx]
    # Yields:
    #     str: 逐字输出的回复内容

    # 构建消息列表，系统提示词 + 历史记录 + 当前用户消息
    messages = [
        {"role":"system", "content":"你是一个乐于助人的AI助手。"}
    ]
    # 现在 history 是 OpenAI 格式的字典列表了
    messages.extend(history)
    messages.append({"role":"user", "content":message})

    try:
        response = llm.stream(messages)

        partial = ""
        for chunk in response:
            if chunk.content:
                partial += chunk.content
                yield partial
    except Exception as e:
        yield f"✖ 出错了：{str(e)}"
# 4. 创建 Gradio 聊天界面
demo = gr.ChatInterface(
    fn=chat_with_deepseek,
    # ※ 关键修复：使用 OpenAI 风格的消息格式
    # type="messages",
    title="🤖 deepseek 聊天助手 ",
    description="基于 LangChain + Deepseek api 的智能对话机器人，支持多轮对话。",
    examples=["你好！","请接介绍一下自己","请写用 python 一个快速排序"],
    # theme="soft"

)

# 5.启动应用
if __name__ == "__main__":
    demo.launch(share=False)



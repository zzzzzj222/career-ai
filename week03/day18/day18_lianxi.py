import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# class WeatherSchema(BaseModel):
#     location: str = Field(..., description="地点名称。")


# @tool(description="获取指定地点的天气情况。",args_schema=WeatherSchema)
@tool
def get_weather(location: str) -> str:
    """获取指定地点的天气情况。"""
    return f"今天 {location} 的天气是下雪的。"

@tool
def multiply(a: int, b: int) -> int:
    """计算两个整数的乘积。a 和 b 是需要相乘的两个整数。"""
    return a * b

def main():
    # 1. 定义工具并绑定：模型能看到工具的名称、说明和参数格式。
    load_dotenv()
    model = ChatOpenAI(
        model="qwen3.5:9b-q4_K_M",
        base_url="http://127.0.0.1:11434/v1",
        api_key="ollama",
        temperature=0,
        # 关闭思考模式，直接生成结构化结果。
        reasoning_effort="none",
        timeout=120,
        max_retries=0,
    )

    tools={get_weather.name:get_weather,
        multiply.name:multiply,
       }
    
    model_with_tools = model.bind_tools(list(tools.values()))
    messages = [
            SystemMessage(content="你是一个中文助手。遇到乘法问题必须调用工具，拿到结果后简洁回答。"),
            HumanMessage(content="每箱有 128 个零件，37 箱一共有多少个？请调用乘法工具计算。"),
            HumanMessage(content="今天昆明的天气是怎么样的？")
        ]
    res=model_with_tools.invoke(messages)
    messages.append(res)
    if not res.tool_calls:
        print("模型未调用工具，本次回答：", res.content)
        return
    for call in res.tool_calls:
        tool_name=call["name"]
        tool_args=call["args"]
        result = tools[tool_name].invoke(tool_args)
        messages.append(ToolMessage(content=str(result),tool_call_id=call["id"]))

    res=model.invoke(messages)
    print("最终回答：", res.content)

if __name__ == "__main__":
    main()

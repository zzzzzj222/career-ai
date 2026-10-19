import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek


@tool
def multiply(a: int, b: int) -> int:
    """计算两个整数的乘积。a 和 b 是需要相乘的两个整数。"""
    return a * b


def main():
    # 1. 定义工具并绑定：模型能看到工具的名称、说明和参数格式。
    load_dotenv()
    model = ChatDeepSeek(
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
        base_url="https://api.deepseek.com",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0,
        timeout=60,
        max_retries=0,
    )
    tools = {multiply.name: multiply}
    # 将模型和工具绑定
    model_with_tools = model.bind_tools(list(tools.values()))

    messages = [
        SystemMessage(content="你是一个中文助手。遇到乘法问题必须调用工具，拿到结果后简洁回答。"),
        HumanMessage(content="每箱有 128 个零件，37 箱一共有多少个？请调用乘法工具计算。"),
    ]
    print("用户：", messages[-1].content)

    # 2. 第一次调用模型：返回 AIMessage，其中 tool_calls 是调用请求。
    # bind_tools 不会执行 Python 函数，真正的执行由下面的代码完成。
    response = model_with_tools.invoke(messages)  #让模型决定调用什么工具
    # 保留完整对话
    messages.append(response)
    print("\n模型请求调用工具：", response.tool_calls)

    if not response.tool_calls:
        print("模型未调用工具，本次回答：", response.content)
        return

    # 3. 执行工具，把结果加入对话
    for call in response.tool_calls:
        tool_name = call["name"]
        tool_args = call["args"]

        result = tools[tool_name].invoke(tool_args)
        print(f"执行工具：{tool_name}，参数：{tool_args}，结果：{result}")
        # 将工具结果加入上下文
        messages.append(
            ToolMessage(content=str(result), tool_call_id=call["id"])
        )

    # 4. 模型根据工具结果生成最终回答
    final_response = model.invoke(messages)
    print("\n模型最终回答：", final_response.content)


if __name__ == "__main__":
    main()

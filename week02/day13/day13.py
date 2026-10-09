"""通过 LangChain 调用阿里云百炼 Qwen。

运行：.venv/Scripts/python.exe week02/day13/day13.py
依赖：python -m pip install langchain-openai
配置：环境变量 DASHSCOPE_API_KEY，可选 DASHSCOPE_BASE_URL（按百炼地域设置）。
"""

import os

from langchain_openai import ChatOpenAI
from langchain_community.embeddings import DashScopeEmbeddings


def main() -> None:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("请先设置环境变量 DASHSCOPE_API_KEY。")

    # 百炼支持 OpenAI 兼容接口，因此可以使用 ChatOpenAI。
    model = ChatOpenAI(
        model="qwen3.7-plus",
        api_key=api_key,
        base_url=os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        temperature=0.7,  # 越低回答越稳定，越高回答越灵活。
        timeout=60,
        max_retries=1,
    )

    # # invoke 返回 AIMessage，content 属性保存模型回答正文。
    # response = model.invoke([
    #     ("system", "你是一名 Python 老师，请用中文简洁回答。"),
    #     ("human", "什么是 LangChain？请用两句话解释。"),
    # ])
    # print(response.content)
    


# 流式输出
    res=model.stream([
        ("system", "用中文简洁回答。"),
        ("human", "你是什么模型？"),
    ])
    for chunk in res:
        print(chunk.content, end="", flush=True)



# 文本向量生成

embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    # other params...
)

text = "This is a test document."

query_result = embeddings.embed_query(text)
print("文本向量长度：", len(query_result), sep='')

doc_results = embeddings.embed_documents(
    [
        "Hi there!",
        "Oh, hello!",
        "What's your name?",
        "My friends call me World",
        "Hello World!"
    ])
print("文本向量数量：", len(doc_results), "，文本向量长度：", len(doc_results[0]), sep='')


if __name__ == "__main__":
    main()

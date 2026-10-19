from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
'''比PromptTemplate更适合，支持带角色指令'''

# 1. 创建聊天提示词模板：花括号中的内容是需要传入的变量。
chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是{name}的 Python 学习助手，请用中文简洁回答。"),
    ("user", "你好！"),
    ("assistant", "你好！今天想学习什么 Python 知识？"),
    ("user", "{user_input}"),
])

# 2. 填充模板，得到 ChatPromptValue；此步骤不会调用模型。
inputs = {"name": "zzj", "user_input": "请用一个简单例子解释 Python 列表推导式。"}
prompt_value = chat_prompt_template.invoke(inputs)
print("=== 填充后的消息 ===")
for message in prompt_value.to_messages():
    print(f"{message.type}: {message.content}")

# 3. 通过 Ollama 的 OpenAI 兼容接口调用本地已安装的模型。
model = ChatOpenAI(
    model="qwen2.5-coder:7b",
    base_url="http://127.0.0.1:11434/v1",
    api_key="ollama",  # 本地接口的占位值，不需要真实 API Key。
    temperature=0,
    timeout=60,
    max_retries=0,
)

# 4. 将填充后的提示词传给模型，返回 AIMessage。
response = model.invoke(prompt_value)
print("\n=== 模型回答 ===")
print(response.content)

# 上面的模板填充和模型调用，也可以用 LCEL 管道串联：
# chain = chat_prompt_template | model
# response = chain.invoke(inputs)

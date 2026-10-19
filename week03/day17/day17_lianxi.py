from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system",  "你是电商客服意图识别助手。\n"
            "请参考以下示例识别用户意图。\n"
            "只输出意图类别。"),
    ("user", "我的快递怎么还没到？"),
    ("assistant", "订单查询"),
    ("user", "我想买一双运动鞋"),
    ("assistant", "产品推荐"),
    ("user", "耳机支持主动降噪吗？"),
    ("assistant", "商品咨询"),
    ("user", "{user_input}"),
])

inputs = {"user_input":  [
    "我的手机什么时候发货？",
    "这款耳机能主动降噪吗？",
    "收到的商品坏了，我想退款。",
]
}
prompt_value = chat_prompt_template.invoke(inputs)
model = ChatOpenAI(
    model="qwen2.5-coder:7b",
    base_url="http://127.0.0.1:11434/v1",
    api_key="ollama",  # 本地接口的占位值，不需要真实 API Key。
    temperature=0,
    timeout=60,
    max_retries=0,
)

response = model.invoke(prompt_value)
print("\n=== 模型回答 ===")
print(response.content)

from langchain_core.prompts import (
    PromptTemplate,
    FewShotPromptTemplate,
)
import os

from langchain_openai import ChatOpenAI

'''提示词模板示例
'''

# 1. 定义示例
examples = [
    {
        "input": "我的快递怎么还没到？",
        "output": "订单查询",
    },
    {
        "input": "耳机支持主动降噪吗？",
        "output": "商品咨询",
    },
    {
        "input": "我想退货退款",
        "output": "退款申请",
    },
]

# 2. 定义单个示例的格式
example_prompt = PromptTemplate.from_template(
    "用户输入：{input}\n意图：{output}"
)

# 3. 创建 Few-shot 模板
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=(
        "你是电商客服意图识别助手。\n"
        "请参考以下示例识别用户意图。\n"
        "只输出意图类别。"
    ),
    suffix="用户输入：{user_input}\n意图：",
    input_variables=["user_input"],
)
'''
examples: 示例数据列表
example_prompt: 单个示例的格式模板
prefix: 在示例前的文本
suffix: 在示例后的文本
input_variables: 模板中需要替换的变量名列表
'''

# 4. 格式化 Prompt
prompt = few_shot_prompt.format(
    user_input="我的手机什么时候发货？"
)
print(type(prompt))

# 5. 调用模型
api_key = os.getenv("DASHSCOPE_API_KEY")

model = ChatOpenAI(
    model="qwen3.7-plus",
    api_key=api_key,
    base_url=os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
    temperature=0.3,  # 越低回答越稳定，越高回答越灵活。
    timeout=60,
    max_retries=1,
)
res=model.stream(input=prompt)
for chunk in res:
    print(chunk.content, end="", flush=True)


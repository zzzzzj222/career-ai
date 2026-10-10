"""Few-shot 提示词：流式、批量、异步调用示例。

运行全部示例：.venv/Scripts/python.exe week02/day14/day14.py
单独运行：在命令后加 --mode stream / batch / async / async-batch
配置：DASHSCOPE_API_KEY，可选 DASHSCOPE_BASE_URL。
"""

import argparse
import asyncio
import os

from langchain_core.prompts import (
    PromptTemplate,
    FewShotPromptTemplate,
)

from langchain_openai import ChatOpenAI

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

# 4. 多条待分类的问题，每条都会使用同一个 Few-shot 模板。
user_inputs = [
    "我的手机什么时候发货？",
    "这款耳机能主动降噪吗？",
    "收到的商品坏了，我想退款。",
]


def create_model() -> ChatOpenAI:
    """统一模型配置，在运行时读取密钥。"""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("请先设置环境变量 DASHSCOPE_API_KEY。")

    return ChatOpenAI(
        model="qwen3.7-plus",
        api_key=api_key,
        base_url=os.getenv(
            "DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"
        ),
        temperature=0.3,  # 越低回答越稳定，越高回答越灵活。
        timeout=60,
        max_retries=1,
    )


def stream_example(model: ChatOpenAI) -> None:
    """单条流式调用：逐块打印回答。"""
    print("\n=== stream：单条流式调用 ===")
    prompt = few_shot_prompt.format(user_input=user_inputs[0])
    for chunk in model.stream(prompt):
        print(chunk.content, end="", flush=True)
    print()


def batch_example(model: ChatOpenAI) -> None:
    """同步批量调用：传入多个 Prompt，一次取得结果列表。"""
    print("\n=== batch：同步批量调用 ===")
    prompts = [few_shot_prompt.format(user_input=text) for text in user_inputs]

    # batch 默认用线程池并发请求；调用方会阻塞，直到全部请求结束。
    # 这不是服务商的离线 Batch API，每个 Prompt 仍是一次独立请求。
    # max_concurrency 限制同时运行的请求数，避免并发过高触发限流。
    responses = model.batch(prompts, config={"max_concurrency": 2})

    # 返回结果与输入顺序一致，不按请求完成顺序排列。
    for text, response in zip(user_inputs, responses):
        print(f"用户输入：{text}\n意图：{response.content}\n")


async def async_example(model: ChatOpenAI) -> None:
    """单条异步调用：await 等待回答，等待期间不阻塞事件循环。"""
    print("\n=== ainvoke：单条异步调用 ===")
    prompt = few_shot_prompt.format(user_input=user_inputs[0])

    # ainvoke 返回协程，需要 await；得到的结果是 AIMessage。
    # 单次 await 不意味着多个请求并发，批量并发见下面的 abatch。
    response = await model.ainvoke(prompt)
    print(f"用户输入：{user_inputs[0]}\n意图：{response.content}")


async def async_batch_example(model: ChatOpenAI) -> None:
    """异步批量调用：并发请求多个 Prompt，等待全部结果。"""
    print("\n=== abatch：异步批量调用 ===")
    prompts = [few_shot_prompt.format(user_input=text) for text in user_inputs]

    # abatch 内部并发调度异步请求，结果同样保持输入顺序。
    responses = await model.abatch(prompts, config={"max_concurrency": 2})
    for text, response in zip(user_inputs, responses):
        print(f"用户输入：{text}\n意图：{response.content}\n")


async def run_async_examples(model: ChatOpenAI, mode: str) -> None:
    """在同一个事件循环中运行选中的异步示例。"""
    if mode in ("all", "async"):
        await async_example(model)
    if mode in ("all", "async-batch"):
        await async_batch_example(model)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("all", "stream", "batch", "async", "async-batch"),
        default="all",
        help="选择调用示例，默认 all 会运行全部示例（共 8 次模型请求）。",
    )
    mode = parser.parse_args().mode
    model = create_model()

    if mode in ("all", "stream"):
        stream_example(model)
    if mode in ("all", "batch"):
        batch_example(model)
    if mode in ("all", "async", "async-batch"):
        # 普通脚本用 asyncio.run 启动事件循环。
        # Jupyter 已有事件循环，应直接 await async_example(model) 等函数。
        asyncio.run(run_async_examples(model, mode))


# 导入模块时不发送请求；只有直接运行脚本才执行示例。
if __name__ == "__main__":
    main()


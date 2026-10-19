"""演示 LangChain content_blocks 的输入和输出格式化，无需调用模型。"""

import json

from langchain_core.messages import AIMessage, HumanMessage


def show(title, value):
    print(f"\n{'=' * 12} {title} {'=' * 12}")
    print(json.dumps(value, ensure_ascii=False, indent=2))


def main():
    # 1. 输入格式化：使用 LangChain 标准内容块构造用户消息。
    # type 标识内容类型：文本用 text，图片用 image。
    # 图片地址仅用于展示格式，本示例不会下载图片或发送请求。
    image_url = "https://example.com/cat.png"
    message = HumanMessage(
        content_blocks=[
            {"type": "text", "text": "请描述这张图片。"},
            {"type": "image", "url": image_url},
        ]
    )
    show("输入：标准 content_blocks", message.content_blocks)
    # 构造时传入的标准块会存储在消息的 content 中。
    show("输入：底层 content", message.content)

    # day16.py 中的 image_url 写法也可以通过 content_blocks 统一读取。
    provider_message = HumanMessage(
        content=[
            {"type": "text", "text": "请描述这张图片。"},
            {"type": "image_url", "image_url": {"url": image_url}},
        ]
    )
    show("输入：image_url 格式转换为标准块", provider_message.content_blocks)
    # 实际调用支持图片的模型时，可以使用：response = model.invoke([message])
    # content_blocks 统一消息格式；模型本身仍需支持对应的内容类型。

    # 2. 输出格式化：模拟普通文本响应，观察 content 和 content_blocks。
    # 以下 AIMessage 均为手动构造的演示数据，不是真实模型返回。
    text_response = AIMessage(content="图片中有一只猫。")
    show("输出：原始 content 是字符串", text_response.content)
    show("输出：content_blocks 将字符串统一为文本块", text_response.content_blocks)

    # 模拟包含不同类型内容块的响应，按 type 分别读取。
    response = AIMessage(
        content_blocks=[
            {"type": "reasoning", "reasoning": "这里是模拟的推理摘要。"},
            {"type": "text", "text": "图片中有一只猫。"},
            {"type": "text", "text": "它正坐在窗边。"},
        ]
    )
    show("输出：完整的标准内容块", response.content_blocks)

    print("\n按类型读取输出：")
    for block in response.content_blocks:
        if block["type"] == "reasoning":
            print("推理摘要：", block["reasoning"])
        elif block["type"] == "text":
            print("正文：", block["text"])

    # 只拼接正文，不将推理摘要等其他内容混入最终答案。
    answer = "".join(
        block["text"]
        for block in response.content_blocks
        if block["type"] == "text"
    )
    print("\n提取后的纯文本：", answer)
    # content_blocks 统一的是消息内容块，并不保证正文符合某个 JSON schema。


if __name__ == "__main__":
    main()

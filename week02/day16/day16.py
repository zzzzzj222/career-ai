from langchain_deepseek import ChatDeepSeek
from rich import print as rprint
from dotenv import load_dotenv
import base64
import os
from langchain_core.messages import AIMessage, HumanMessage

#  从.env文件加载环境变量
load_dotenv(override=True)
api_key = os.getenv("DEEPSEEK_API_KEY")

model=ChatDeepSeek(
    api_key=api_key,
    model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
    base_url="https://api.deepseek.com",
    timeout=60,
    max_retries=1,
)

def encode_iamge(imag_path,image_type='png'):
    # 将本地图片转换为base64编码的DATA URI格式，方便在文本中嵌入图片数据
    with open(imag_path, "rb") as image_file:
        encoded_string = image_file.read()
        base64_data = base64.b64encode(encoded_string).decode('utf-8')
        data_uri = f"data:image/{image_type};base64,{base64_data}"
        return data_uri


img_path = "C://Users//32885//Pictures//test.png"  # 替换为你的图片路径
base64_image=encode_iamge(img_path)

# response=model.invoke(
#     [{
#         "role":"user",
#         "content":[
#             {
#                 "type":"text",
#                 "text":"请描述这张图片的内容。"
#             },
#             {
#                 "type":"image_url",
#                 "image_url":{"url":base64_image}
#             }
#         ]
#     }]
# )


response=model.invoke(
    [HumanMessage(
        content_blocks=[
            {"type": "text", "text": "请描述这张图片。"},
            {
                "type":"image",
                "url":base64_image
            }
        ]
    )]
)



for block in response.content_blocks:
    if block["type"] == "reasoning":
        print("推理摘要：", block["reasoning"])
    elif block["type"] == "text":
        print("正文：", block["text"])

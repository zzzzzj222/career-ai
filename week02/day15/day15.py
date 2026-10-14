# from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from rich import print as rprint
from dotenv import load_dotenv
import os

'''多伦对话聊天机器人'''

EXIT_WORD="exit"
MAX_PAIRS_HISTORY = 10


# 保留最近n轮对话
def keep_recent_messages(messages,max_pairs = 3):
    '''保留最近的n轮对话
    max_pairs:保留对话的轮数
    '''
    # 分离system和对话消息
    system_messages=[m for m in messages if m['role']=='system']
    chat_messages=[m for m in messages if m['role']=='user' or m['role']=='assistant']
    # 保留最近的对话消息
    chat_messages=chat_messages[-(max_pairs*2):]
    # 合并system和对话消息
    messages=system_messages+chat_messages
    return messages


def main():
    # 从.env文件加载环境变量
    # load_dotenv(override=True)
    # api_key = os.getenv("DEEPSEEK_API_KEY")

    # model=ChatDeepSeek(
    #     api_key=api_key,
    #     model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
    #     base_url="https://api.deepseek.com",
    #     timeout=60,
    #     max_retries=1,
    # )
    model=ChatOpenAI(
        api_key="ollama",
        model="qwen2.5-coder:7b",
        base_url="http://127.0.0.1:11434/v1",
        timeout=60,
        max_retries=1,
    )

    messages=[{
        "role": "system",
        "content": "你是一个聊天机器人,是zzj的助手，也是一名数字员工，可以回答各种问题，提供帮助。",
    }]

    print(f"请输入具体问题，输入'{EXIT_WORD}'退出。")
    i=1

    while True:
        rprint("/n","="*10,f"第{i}轮对话开始","="*10,"/n")
        user_input=input("用户:")
        if user_input==EXIT_WORD:
            print("退出程序。")
            break
        messages.append({"role":"user","content":user_input})
        print("小助手：",end="",flush=True)
        # 优化历史记忆
        memory_messages=keep_recent_messages(messages,max_pairs=MAX_PAIRS_HISTORY)

        reply_content=""
        # 流式输出
        for chunk in model.stream(memory_messages):
            if chunk.content:
                print(chunk.content,end="",flush=True)
                reply_content+=chunk.content
        rprint("/n","="*10,f"第{i}轮对话结束","="*10,"/n")
        i+=1
        # 将模型响应添加到消息列表
        messages.append({"role":"assistant","content":reply_content})
        
if __name__ == "__main__":
    main()







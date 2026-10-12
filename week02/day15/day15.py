from langchain_deepseek import ChatDeepSeek
from rich import print as rprint
from dotenv import load_dotenv
import os

# 从.env文件加载环境变量
# load_dotenv(override=True)
api_key = os.getenv("DEEPSEEK_API_KEY")

model=ChatDeepSeek(
    api_key=api_key,
    model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
    base_url="https://api.deepseek.com",
    timeout=60,
    max_retries=1,
)

# 保留最近n轮对话
def keep_recent_messages(messages,max_pairs = 3):
    '''保留最近的n轮对话
    max_pairs:保留对话的轮数
    '''
    # 分离system和对话消息
    
    pass

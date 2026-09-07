

with open("D:/VSProject/career-ai/week01/day02/模拟文件.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)
    # 统计中文字符数量
    chinese_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
    print(f"中文字符数量: {chinese_chars}")
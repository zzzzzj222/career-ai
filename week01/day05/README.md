# 联网搜索模块

`web_search.py` 只负责搜索网页，返回结构化摘要，不依赖 DeepSeek、OpenAI SDK 或 API Key。可以将该文件复制到其他 Python 3.10+ 项目，安装 `ddgs>=9,<10` 后使用。

## 在项目根目录复用

```python
from week01.day05.web_search import WebSearchError, search_web

try:
    results = search_web("Python 官方教程", max_results=3, auto_recent=False)
    for result in results:
        print(result["title"], result["url"], result["snippet"])
except WebSearchError as exc:
    print(exc)
```

同目录的脚本也可以使用 `from web_search import search_web`。

返回值是字典列表，每条包含 `id`（从 1 开始）、`title`、`url`、`snippet`，可直接 JSON 序列化。摘要最多 3000 字符，不是网页全文。

可选参数：`recent="d"/"w"/"m"/"y"` 限制时间范围；`max_results=5` 控制数量上限；`region="cn-zh"` 指定地区；`timeout=15` 设置请求超时秒数。默认对含“今天/今日/最新”的问题附加本地日期，并在未指定时间范围时限定最近一天；`auto_recent=False` 可关闭该行为。

参数无效抛出 `ValueError`，服务失败或没有可用结果抛出 `WebSearchError`。搜索结果的时效性和准确性取决于搜索服务及来源网站。

## DeepSeek 示例

在项目根目录执行：

```powershell
.\.venv\Scripts\python.exe -m pip install -r week01/day05/requirements.txt
.\.venv\Scripts\python.exe week01/day05/deepseek_test.py "今天有什么科技新闻？" --recent d
```

也支持 `python -m week01.day05.deepseek_test`。需配置 `DEEPSEEK_API_KEY`；脚本通过 `responses.create` 将搜索摘要交给模型并流式输出回答。

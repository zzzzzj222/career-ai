"""可独立复用的网页搜索模块，仅依赖 ddgs，不依赖模型或 API Key。

同目录使用：from web_search import search_web
项目根目录使用：from week01.day05.web_search import search_web
"""

from datetime import datetime
from typing import TypedDict

from ddgs import DDGS

__all__ = ["SearchResult", "WebSearchError", "search_web"]


class SearchResult(TypedDict):
    """一条搜索摘要，可直接用 json.dumps 序列化。"""

    id: int
    title: str
    url: str
    snippet: str


class WebSearchError(RuntimeError):
    """搜索服务失败或没有可用结果。"""


def search_web(
    question: str,
    recent: str | None = None,
    *,
    max_results: int = 5,
    region: str = "cn-zh",
    timeout: int = 15,
    auto_recent: bool = True,
) -> list[SearchResult]:
    """搜索网页并返回标题、链接和摘要，不抓取网页全文。

    recent: None 表示不限制，d/w/m/y 表示最近一天/周/月/年。
    auto_recent: 对含“今天/今日/最新”的问题附加本地日期，
        并在未指定 recent 时限定一天；设为 False 可关闭此行为。
    max_results: 返回结果数量上限；过滤无效链接后可能少于此值。
    region: 搜索地区，例如 cn-zh、us-en。
    timeout: 搜索服务请求超时秒数。

    参数无效抛出 ValueError；搜索失败或无结果抛出 WebSearchError。
    函数不打印内容，也不读取环境变量，调用方负责展示和错误处理。
    """
    if not isinstance(question, str) or not question.strip():
        raise ValueError("搜索问题不能为空。")
    if recent not in (None, "d", "w", "m", "y"):
        raise ValueError("recent 必须是 None、d、w、m 或 y。")
    if type(max_results) is not int or max_results <= 0:
        raise ValueError("max_results 必须是正整数。")
    if type(timeout) is not int or timeout <= 0:
        raise ValueError("timeout 必须是正整数。")
    if not isinstance(region, str) or not region.strip():
        raise ValueError("region 不能为空。")

    query = question.strip()
    if auto_recent and any(word in query for word in ("今天", "今日", "最新")):
        query = f"{query} {datetime.now():%Y-%m-%d}"
        recent = recent or "d"

    try:
        results = DDGS(timeout=timeout).text(
            query, region=region, timelimit=recent, max_results=max_results
        )
        sources: list[SearchResult] = []
        for item in results:
            url = item.get("href") or ""
            if not url.startswith(("https://", "http://")):
                continue
            sources.append({
                "id": len(sources) + 1,
                "title": item.get("title") or "",
                "url": url,
                "snippet": (item.get("body") or "")[:3000],
            })
            if len(sources) >= max_results:
                break
    except Exception as exc:
        raise WebSearchError(f"联网搜索失败：{exc}") from exc
    if not sources:
        raise WebSearchError("没有搜到网页，请更换关键词或放宽 recent 时间范围。")
    return sources

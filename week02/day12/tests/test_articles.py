"""文章接口回归检查：使用真实数据库，测试记录结束后自动清理。"""

import os
import unittest
from uuid import uuid4

from fastapi.testclient import TestClient

from week02.day12.article_api.main import app


@unittest.skipUnless(
    os.getenv("RUN_DATABASE_TESTS") == "1",
    "设置 RUN_DATABASE_TESTS=1 后在配置的 MySQL 数据库上运行",
)
class ArticleApiTests(unittest.TestCase):
    def test_article_contract(self) -> None:
        marker = f"refactor_{uuid4().hex}"
        article_ids: list[int] = []

        with TestClient(app) as client:
            count_response = client.get("/articles/article/count")
            self.assertEqual(count_response.status_code, 200)
            initial_count = count_response.json()
            self.assertIsInstance(initial_count, int)
            try:
                self.assertEqual(client.get("/").json(), {"message": "Hello, World!"})
                self.assertEqual(client.get("/openapi.json").status_code, 200)

                with self.subTest("新增、去空白与跨请求持久化"):
                    for title in [f"{marker}%_ target", f"{marker}XY target"]:
                        response = client.post(
                            "/articles/create", json={"title": f" {title} ", "author": " 测试作者 "}
                        )
                        self.assertEqual(response.status_code, 201)
                        article = response.json()
                        article_ids.append(article["id"])
                        self.assertEqual(article["title"], title)
                        self.assertEqual(article["author"], "测试作者")
                        self.assertIn("create_time", article)
                        self.assertIn("update_time", article)
                        self.assertEqual(
                            client.get(f"/articles/{article['id']}").json(), article
                        )

                self.assertEqual(len(article_ids), 2, "新增文章失败，停止后续检查")
                self.assertEqual(client.get("/articles/article/count").json(), initial_count + 2)
                article_id = article_ids[0]
                original = client.get(f"/articles/{article_id}").json()

                with self.subTest("分页与搜索特殊字符"):
                    response = client.get("/articles", params={"offset": 0, "limit": 1})
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(len(response.json()), 1)
                    response = client.get("/articles/search", params={"q": marker + "%_"})
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual([row["id"] for row in response.json()], [article_id])

                with self.subTest("请求校验且失败不改变已存记录"):
                    invalid_paths = [
                        "/articles/0",
                        "/articles/-1",
                        "/articles/not-an-id",
                        "/articles?offset=-1",
                        "/articles?limit=0",
                        "/articles?limit=101",
                        "/articles/search",
                        "/articles/search?q=",
                    ]
                    for path in invalid_paths:
                        self.assertEqual(client.get(path).status_code, 422, path)
                    invalid_bodies = [
                        {"title": "   ", "author": "作者"},
                        {"title": "x" * 256, "author": "作者"},
                        {"title": "标题", "author": ""},
                        {"title": "标题"},
                        {"title": "标题", "author": "作者", "extra": True},
                    ]
                    for body in invalid_bodies:
                        self.assertEqual(client.post("/articles/create", json=body).status_code, 422)
                        self.assertEqual(
                            client.put(f"/articles/{article_id}", json=body).status_code, 422
                        )
                    self.assertEqual(client.get(f"/articles/{article_id}").json(), original)

                with self.subTest("更新及时间字段"):
                    updated_data = {"title": marker + " updated", "author": "新作者"}
                    response = client.put(f"/articles/{article_id}", json=updated_data)
                    self.assertEqual(response.status_code, 200)
                    updated = response.json()
                    self.assertEqual(updated["title"], updated_data["title"])
                    self.assertEqual(updated["author"], updated_data["author"])
                    self.assertEqual(updated["create_time"], original["create_time"])
                    self.assertGreaterEqual(updated["update_time"], original["update_time"])
                    self.assertEqual(client.get(f"/articles/{article_id}").json(), updated)

                with self.subTest("删除空响应与不存在记录"):
                    response = client.delete(f"/articles/{article_id}")
                    self.assertEqual(response.status_code, 204)
                    self.assertEqual(response.content, b"")
                    self.assertEqual(client.get("/articles/article/count").json(), initial_count + 1)
                    for response in [
                        client.get(f"/articles/{article_id}"),
                        client.put(f"/articles/{article_id}", json=updated_data),
                        client.delete(f"/articles/{article_id}"),
                    ]:
                        self.assertEqual(response.status_code, 404)
                        self.assertEqual(response.json()["detail"], "文章不存在")
            finally:
                for article_id in article_ids:
                    response = client.delete(f"/articles/{article_id}")
                    self.assertIn(response.status_code, [204, 404], "测试记录清理失败")
                self.assertEqual(client.get("/articles/article/count").json(), initial_count)


if __name__ == "__main__":
    unittest.main()

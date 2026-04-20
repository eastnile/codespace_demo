import unittest
from unittest.mock import patch

from news_bridge.models import Article, ComparisonResult, Source
from news_bridge.web import create_app


class WebAppTests(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.testing = True
        self.client = app.test_client()

    def test_index_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"News Bridge", response.data)

    def test_analyze_requires_api_key(self):
        response = self.client.post(
            "/analyze",
            data={
                "english_limit": "2",
                "chinese_limit": "2",
                "max_pairs": "2",
                "model": "gpt-4o-mini",
                "api_key": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"OpenAI API key is required", response.data)

    @patch("news_bridge.web.generate_comparisons")
    @patch("news_bridge.web.load_articles")
    @patch("news_bridge.web.OpenAI")
    def test_analyze_renders_results(self, mock_openai, mock_load_articles, mock_generate):
        eng_source = Source(name="CNN World", language="en", feed_url="https://example.com/en")
        zh_source = Source(name="BBC 中文", language="zh", feed_url="https://example.com/zh")
        eng_article = Article(source=eng_source, title="English headline", link="https://en", summary="summary")
        zh_article = Article(source=zh_source, title="中文标题", link="https://zh", summary="摘要")

        mock_load_articles.return_value = ([eng_article], [zh_article])
        mock_generate.return_value = [
            ComparisonResult(
                english_article=eng_article,
                chinese_article=zh_article,
                same_event=True,
                framing_comparison="Different emphasis",
                notes="English focuses on diplomacy; Chinese focuses on sovereignty.",
            )
        ]

        response = self.client.post(
            "/analyze",
            data={
                "english_limit": "1",
                "chinese_limit": "1",
                "max_pairs": "1",
                "model": "gpt-4o-mini",
                "api_key": "test-key",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Results (1)", response.data)
        self.assertIn(b"Different emphasis", response.data)
        mock_openai.assert_called_once_with(api_key="test-key")


if __name__ == "__main__":
    unittest.main()

from datetime import datetime
import feedparser
from news_bridge.models import Article, Source


def _parse_datetime(entry):
    if entry.get("published_parsed"):
        return datetime(*entry.published_parsed[:6])
    if entry.get("updated_parsed"):
        return datetime(*entry.updated_parsed[:6])
    return None


def fetch_articles(source: Source, limit: int | None = None) -> list[Article]:
    feed = feedparser.parse(source.feed_url)
    articles: list[Article] = []
    for entry in feed.entries[:limit]:
        articles.append(
            Article(
                source=source,
                title=entry.get("title", "").strip(),
                link=entry.get("link", ""),
                summary=entry.get("summary", "").strip(),
                published=_parse_datetime(entry),
            )
        )
    return articles

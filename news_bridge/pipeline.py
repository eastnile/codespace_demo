import itertools
import logging
from typing import Iterable
from openai import OpenAI
from news_bridge.analysis import compare_articles
from news_bridge.fetcher import fetch_articles
from news_bridge.models import Article, ComparisonResult
from news_bridge.sources import CHINESE_SOURCES, ENGLISH_SOURCES


logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def load_articles(english_limit: int, chinese_limit: int) -> tuple[list[Article], list[Article]]:
    english_articles: list[Article] = []
    for source in ENGLISH_SOURCES:
        english_articles.extend(fetch_articles(source, limit=english_limit))

    chinese_articles: list[Article] = []
    for source in CHINESE_SOURCES:
        chinese_articles.extend(fetch_articles(source, limit=chinese_limit))

    return english_articles, chinese_articles


def generate_comparisons(
    client: OpenAI,
    english_articles: Iterable[Article],
    chinese_articles: Iterable[Article],
    max_pairs: int,
    model: str,
) -> list[ComparisonResult]:
    comparisons: list[ComparisonResult] = []
    pair_iter = itertools.islice(
        itertools.product(english_articles, chinese_articles),
        max_pairs,
    )
    for english_article, chinese_article in pair_iter:
        logging.info(
            "Comparing %s with %s",
            english_article.title,
            chinese_article.title,
        )
        comparisons.append(
            compare_articles(
                client=client,
                english_article=english_article,
                chinese_article=chinese_article,
                model=model,
            )
        )
    return comparisons

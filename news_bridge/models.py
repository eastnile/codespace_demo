from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Source:
    name: str
    language: str
    feed_url: str


@dataclass
class Article:
    source: Source
    title: str
    link: str
    summary: str
    published: Optional[datetime] = None


@dataclass
class ComparisonResult:
    english_article: Article
    chinese_article: Article
    same_event: bool
    framing_comparison: str
    notes: str

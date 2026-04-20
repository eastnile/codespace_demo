import json
from typing import Tuple
from openai import OpenAI
from news_bridge.models import Article, ComparisonResult


SYSTEM_PROMPT = (
    "You are a bilingual news analyst comparing how English-language outlets and "
    "Chinese-language outlets frame the same events. Use neutral language, "
    "identify framing differences, and call out potential bias without inflammatory "
    "language."
)


def _build_user_prompt(english_article: Article, chinese_article: Article) -> str:
    english_block = (
        f"Source: {english_article.source.name}\n"
        f"Language: English\n"
        f"Title: {english_article.title}\n"
        f"Summary: {english_article.summary}\n"
        f"URL: {english_article.link}"
    )
    chinese_block = (
        f"Source: {chinese_article.source.name}\n"
        f"Language: Chinese\n"
        f"Title: {chinese_article.title}\n"
        f"Summary: {chinese_article.summary}\n"
        f"URL: {chinese_article.link}"
    )
    return (
        "Determine if the following two articles describe the same event. "
        "If they do, compare how each side frames the story and summarize potential "
        "bias or selective emphasis. Respond with compact JSON matching this schema: "
        "{\"same_event\": boolean, \"framing_comparison\": string, \"notes\": string}.\n\n"
        f"English article:\n{english_block}\n\nChinese article:\n{chinese_block}"
    )


def _parse_model_output(content: str) -> Tuple[bool, str, str]:
    try:
        payload = json.loads(content)
    except json.JSONDecodeError:
        return False, "Model response was not valid JSON", content.strip()

    same_event = bool(payload.get("same_event"))
    framing = str(payload.get("framing_comparison", "")).strip()
    notes = str(payload.get("notes", "")).strip()
    return same_event, framing, notes


def compare_articles(
    client: OpenAI,
    english_article: Article,
    chinese_article: Article,
    model: str = "gpt-4o-mini",
) -> ComparisonResult:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_prompt(english_article, chinese_article)},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
    )
    content = response.choices[0].message.content or ""
    same_event, framing, notes = _parse_model_output(content)
    return ComparisonResult(
        english_article=english_article,
        chinese_article=chinese_article,
        same_event=same_event,
        framing_comparison=framing,
        notes=notes,
    )

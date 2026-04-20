import os
from flask import Flask, render_template, request
from openai import OpenAI

from news_bridge.pipeline import generate_comparisons, load_articles


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html", results=None, error=None, defaults=_default_values())

    @app.post("/analyze")
    def analyze():
        english_limit = _to_positive_int(request.form.get("english_limit"), default=5)
        chinese_limit = _to_positive_int(request.form.get("chinese_limit"), default=5)
        max_pairs = _to_positive_int(request.form.get("max_pairs"), default=5)
        model = (request.form.get("model") or "gpt-4o-mini").strip()
        api_key = (request.form.get("api_key") or os.environ.get("OPENAI_API_KEY") or "").strip()

        defaults = {
            "english_limit": english_limit,
            "chinese_limit": chinese_limit,
            "max_pairs": max_pairs,
            "model": model,
            "api_key": request.form.get("api_key") or "",
        }

        if not api_key:
            return render_template(
                "index.html",
                results=None,
                error="OpenAI API key is required. Set OPENAI_API_KEY or provide one in the form.",
                defaults=defaults,
            )

        client = OpenAI(api_key=api_key)
        english_articles, chinese_articles = load_articles(
            english_limit=english_limit,
            chinese_limit=chinese_limit,
        )
        results = generate_comparisons(
            client=client,
            english_articles=english_articles,
            chinese_articles=chinese_articles,
            max_pairs=max_pairs,
            model=model,
        )

        return render_template("index.html", results=results, error=None, defaults=defaults)

    return app


def _to_positive_int(raw_value: str | None, default: int) -> int:
    try:
        value = int(raw_value or default)
    except ValueError:
        return default
    return value if value > 0 else default


def _default_values() -> dict[str, str | int]:
    return {
        "english_limit": 5,
        "chinese_limit": 5,
        "max_pairs": 5,
        "model": "gpt-4o-mini",
        "api_key": "",
    }


app = create_app()

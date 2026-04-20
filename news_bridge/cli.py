import argparse
import os
from openai import OpenAI
from news_bridge.pipeline import generate_comparisons, load_articles


def format_result(result) -> str:
    header = f"English: {result.english_article.source.name} | Chinese: {result.chinese_article.source.name}"
    match_line = "Same event: yes" if result.same_event else "Same event: unsure/no"
    return "\n".join(
        [
            "=" * len(header),
            header,
            "=" * len(header),
            match_line,
            "Framing differences:",
            result.framing_comparison or "(none provided)",
            "Notes:",
            result.notes or "(none provided)",
        ]
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Compare coverage of shared events in English and Chinese news sources "
            "using the ChatGPT API."
        )
    )
    parser.add_argument(
        "--english-limit",
        type=int,
        default=5,
        help="Number of recent items to pull from each English source.",
    )
    parser.add_argument(
        "--chinese-limit",
        type=int,
        default=5,
        help="Number of recent items to pull from each Chinese source.",
    )
    parser.add_argument(
        "--max-pairs",
        type=int,
        default=5,
        help="Maximum number of cross-language article pairs to compare.",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="ChatGPT model to use for analysis.",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("OPENAI_API_KEY"),
        help="OpenAI API key (defaults to OPENAI_API_KEY env var).",
    )
    args = parser.parse_args()

    if not args.api_key:
        raise SystemExit("OPENAI_API_KEY is not set. Provide --api-key or set the env var.")

    client = OpenAI(api_key=args.api_key)

    english_articles, chinese_articles = load_articles(
        english_limit=args.english_limit,
        chinese_limit=args.chinese_limit,
    )
    comparisons = generate_comparisons(
        client=client,
        english_articles=english_articles,
        chinese_articles=chinese_articles,
        max_pairs=args.max_pairs,
        model=args.model,
    )

    for comparison in comparisons:
        print(format_result(comparison))
        print()


if __name__ == "__main__":
    main()

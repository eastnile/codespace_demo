# News Bridge

A lightweight tool that fetches recent headlines from major English and Chinese news sources and asks the ChatGPT API to compare how each side frames the same events.

## Features
- Pulls recent articles from CNN World and BBC World (English) plus BBC 中文 and 新华网 (Chinese) via RSS.
- Sends cross-language article pairs to ChatGPT for bilingual framing analysis.
- Supports both a CLI and a simple web UI.
- Limits how many articles and pairings to inspect so you can control cost.

## Requirements
- Python 3.11+
- An OpenAI API key with access to a GPT-4o family model (defaults to `gpt-4o-mini`).
- Dependencies listed in `requirements.txt` (`feedparser`, `openai`, `flask`). Install them with:

```bash
pip install -r requirements.txt
```

## CLI usage

```bash
export OPENAI_API_KEY=sk-...
python -m news_bridge.cli --english-limit 5 --chinese-limit 5 --max-pairs 5
```

Arguments:
- `--english-limit`: number of recent items pulled from each English feed (default: 5).
- `--chinese-limit`: number of recent items pulled from each Chinese feed (default: 5).
- `--max-pairs`: maximum cross-language pairs to analyze (default: 5).
- `--model`: ChatGPT model name (default: `gpt-4o-mini`).
- `--api-key`: override for the OpenAI API key (otherwise reads `OPENAI_API_KEY`).

## Web UI usage

Run a local web server:

```bash
export OPENAI_API_KEY=sk-...
flask --app news_bridge.web run --debug
```

Then open http://127.0.0.1:5000/ in your browser, adjust limits/model as needed, and click **Run analysis**.

You can leave the API key form field empty if `OPENAI_API_KEY` is already set.

## Notes on pairing
For simplicity, the tool currently pairs articles in the order they appear in each feed (up to `max_pairs`). Pair selection is intentionally conservative to avoid excessive API calls. If you want deeper matching, consider filtering RSS entries first or adapting the pairing logic in `news_bridge/pipeline.py`.
